import argparse
import sys
import ldap
import sqlite3
from ldap_con import get_ldap
import ldap.modlist as modlist


DB_DIR = "/root/workspace/rogue/project/app/rogue3.db"



def get_user(username, vpc_env):
  
  # check to see if user is first present in trusted list
  
  trust_query = 'select user_name, category, uid  from user_ref where user_name="%s"' % username
  db_query = 'select ssh_pub_key, fingerprint from user_details where user_name="%s"' % username

  trust_data = execute_query(trust_query)  
  # details : [(u'sagnik.kundu@hp.com', u'devops', 1000)]

  db_data = execute_query(db_query)

  if (trust_data != []):
    print "trusted user !!"
    ldap_user = str(trust_data[0][0])
    ldap_uid = str(trust_data[0][2])
    ldap_grp = str(trust_data[0][1])

    if (db_data != []):
      print "user data present"
      ssh_key = db_data[0][0]
      user_fp = db_data[0][1]

      # updating ldap db:
      print "Adding the user to LDAP"
      completion = ldap_add(ldap_user, ldap_grp, ldap_uid)
      
      if completion:
        print "LDAP Updated , updating the status table for starttime"
        stats ,db = update_status(ldap_user, vpc_env)
        if stats:        
          db.commit()
          print 'User status successfully updated.'
        else:
          print 'Error!! User status could not be updated.'
      else:
        print 'Error!! User could not be added to LDAP'
    else:
      print 'Error !! User Data no found.'
  else:
    print 'Error !! Not a trusted User.'  
    

def execute_query(query):
  db = get_con()
  result = db.execute(query).fetchall()
  return result


def ldap_add(username, group, uid):

  completion = False
  con = get_ldap()
  user = str(username)
  sn = str(user.split('@')[0].split('.')[1])
  group = group.lower()

  if group == 'dev':
    gid = '20000'
  elif group == 'qa':
    gid = '21000'
  else:
    gid = '22000'

  # The dn of our new entry/object
  dn="uid=%s,ou=people,dc=lightaria,dc=com" % user
  
  # generate unique uidNumber for each user
  #uid = get_uidNum()
   
  
  # A dict to help build the "body" of the object
  attr = {'objectclass': ['top', 'person', 'posixAccount', 'shadowAccount'],
          'cn': [user],
          'sn': [sn],
          'uid': [user],
          'uidNumber': [uid],
          'gidNumber': [gid],
          'loginShell': ['/bin/zsh'],
          'homeDirectory': ['']}

  print(type(attr))
  # Convert our dict to nice syntax for the add-function using modlist-module
  ldif = modlist.addModlist(attr)

  # Do the actual synchronous add-operation to the ldapserver
  try:
    con.add_s(dn,ldif)
  except ldap.LDAPError, e:
    print "Error : %s " % str(e)
    
  # disconnect and free resources when done
  con.unbind_s()
  completion=True

  return completion


def update_status(username, category):

  stats = False
  db = get_con()

  status = 'active'
  try:
    db.execute('insert into access_status (user_name, status, env) values (?, ?, ?)' , (username, status, category))
  except:
    err = "Error !!  %s" % sys.exc_info()[0]
    print "Error : %s" % err

  result = db.execute('select * from access_status where user_name=?',(username,)).fetchall()

  if(result != []):
    print "status updated "
    stats = True
    return (stats, db)
  else:
    print "status update failed."
    return stats


def get_con():
  con = sqlite3.connect(DB_DIR)
  con.row_factory = sqlite3.Row
  return con


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Takes username and vpc name')
  parser.add_argument('-n', action='store', dest='user_name',
                    help='Provide the username or userid')
  parser.add_argument('-e', action='store', dest='vpc_env',
                    help='Provide the vpc env')

  results = parser.parse_args()

  #pass the user_name received to get_user()
  get_user(results.user_name, results.vpc_env)



