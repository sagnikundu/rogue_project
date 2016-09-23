import sys, sqlite3, argparse
from db_to_ldap import get_con , execute_query

def user_get(username):
  
  query_string = 'select ssh_pub_key from user_details where user_name="%s"' % username
  db_data = execute_query(query_string)
  if (db_data != []):
    ssh_key = db_data[0][0]
    return ssh_key
  else: 
    print "key not found in db"


def update_auth_file(key):
  


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Takes username and pushes users pub_key to authkeys')
  parser.add_argument('-n', action='store', dest='user_name',
                    help='Provide the username or userid')

  results = parser.parse_args()

  if len(sys.argv) < 2:
    print "Script accepts one argument, refer: pushkey.py -h (help)"
    exit(1)
  else:
    key =  user_get(results.user_name)
    print key

