import os, sys, sqlite3, argparse, subprocess
from db_to_ldap import get_con , execute_query

auth_file = '/root/workspace/rogue/project/app/authorized_keys'

def user_get(username):
  
  query_string = 'select ssh_pub_key from user_details where user_name="%s"' % username
  db_data = execute_query(query_string)
  if (db_data != []):
    ssh_key = db_data[0][0]
    return ssh_key
  else: 
    return False


def update_local_auth_file(key, env, name):
  auth = '/root/workspace/rogue/project/app/%s.auth_file' % env
  update = False
  key=key+"_"+name
  #create a authorized_keys file
  with open(auth, 'a+') as f:
    f.write(key)
    f.write("\n")
    update = True
    
    return update

def delete_from_authfile(user, env):
  auth = '/root/workspace/rogue/project/app/%s.auth_file' % env
  cmd = "sed -i '/ %s/d' %s " % (user, auth)
  p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()
  p_status = p.wait()
  if p_status == 0:
    return True
  else:
    return False
  #os.system(cmd)
        

#if __name__ == '__main__':
#  parser = argparse.ArgumentParser(description='Takes username and pushes users pub_key to authkeys')
#  parser.add_argument('-n', action='store', dest='user_name',
#                    help='Provide the username or userid')

#  results = parser.parse_args()

#  if len(sys.argv) < 2:
#    print "Script accepts one argument, refer: pushkey.py -h (help)"
#    exit(1)
#  else:
#    key =  user_get(results.user_name)
#    if key:
#      update = update_local_auth_file(key)
#      if update:
#        print "%s 's key updated .." % results.user_name.split('@')[0]
#      else:
#        print "auth file could not be updated "
#    else:
#      print  "key not found !!"
