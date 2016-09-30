import sqlite3
from datetime import datetime, timedelta
from db_to_ldap import execute_query

query = 'select user_name, timestamp from access_status'
data = execute_query(query)

#data fmt [(u'user1', u'2016-09-28 20:57:18.080140'), (u'user2', u'2016-09-29 12:08:01.872108')]

users = {}

for item in data:
  start_time = datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S.%f")
  end_time = start_time + timedelta(hours=1)
  users[item[0]] = [start_time, end_time]

#print type(users['user1'])
print type(users['user1'][1])

for item in users : 
  diff = str(users[item][1] - users[item][0])
  if(diff >= 1):
  #1 mark the user as active
  #2 remove/update entries from access_status and user_details
  #3 remove key from auth_keys
  #4 update local users file

  #1
    update_user = 'Update users set status='active', start_timestamp='None' where user_name="%s"' % item
    execute_query(update_user)

  #2
    #update_userdetails = 'update  user_details set ssh_pub_key="new_key", fingerprint="new_fp" where user_name="%s"' % item
    #execute_query(update_userdetails)
  
    del_from_access_status = 'delete  from access_status where user_name="%s"' % item
    execute_query(del_from_access_status)
