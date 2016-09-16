#!/usr/bin/env python
import argparse
from db_setup import get_db
from ldap_con import get_ldap, get_uidNum


def get_user(username):
  db = get_db()
  # check to see if user exists in db:
  result = db.execute('select user_name, category from users where user_name="?"', username).fetchone()
  if result['user_name']:
    print "User found"
    user = result['user_name']
    group = result['category']

    print "Adding the user to LDAP"
    completion = ldap_add(user, group)

    if completion == 'True':
      print "on completion update the status table for starttime"
      update_status(db, username, group)
    else:
      print 'Error: User: '+ user + ' could not be added to ldap server'

  else:
    print "User not found in db. Please add the user first !!"



def ldap_add(username, group):

  completion = False
  con = get_ldap()
  user = str(username)
  group = group.lower()

  if group == 'dev':
    gid = '20000'
  else:
    gid = '21000'

  # The dn of our new entry/object
  dn="uid=%s,ou=people,dc=lightaria,dc=com" % user
  
  # generate unique uidNumber for each user
  uid_no = get_uidNum()
  
  # A dict to help build the "body" of the object
  attrs = {}
  attrs['objectclass'] = ['top', 'person', 'posixAccount', 'shadowAccount']
  attrs['cn'] = user
  attrs['uid'] = user
  attrs['uidNumber'] = uid_no
  attrs['gidNumber'] = gid
  attrs['homeDirectory'] = '/home/%s' % user
  attrs['loginShell'] = '/bin/bash'

  # Convert our dict to nice syntax for the add-function using modlist-module
  ldif = modlist.addModlist(attrs)

  # Do the actual synchronous add-operation to the ldapserver
  try:
    con.add_s(dn,ldif)
  except ldap.LDAPError, e:
    print "Error : %s " % str(e)
    
  # disconnect and free resources when done
  con.unbind_s()
  completion=True

  return completion


def update_status(conn, username, category):
  user = str(username)
  category = str(category)
  try:
    conn.execute('insert into access_status (user_name, status, env) values (?, ?, ?)' , (user, 'active', category))
  except sqlite3.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)


# maybe main is not needed:TODO

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Takes username and vpc name')
  parser.add_argument('-n', action='store', dest='user_name',
                    help='Provide the username or userid')
  parser.add_argument('-e', action='store', dest='vpc_env',
                    help='Provide the vpc env')

  results = parser.parse_args()

  #pass the user_name received to get_user()
  get_user(results.user_name)



