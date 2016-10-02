import sqlite3
import sys
from datetime import datetime, timedelta
from db_to_ldap import execute_query, get_con
from pushkey import delete_from_authfile
from create_user_file import create_userfile

query = 'select user_name, timestamp from access_status'
data = execute_query(query)

#data fmt [(u'user1', u'2016-09-28 20:57:18.080140'), (u'user2', u'2016-09-29 12:08:01.872108')]

users = {}

for item in data:
  start_time = datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S.%f")      # unicode to datetime object
  end_time = start_time + timedelta(hours=1)
  users[item[0]] = [start_time, end_time]

print "User List : %s" % users


print "starting time evaluation.." 

for item in users : 

  print "Checking user: %s "  % item
  print users[item][1]
  print type(users[item][1])  

  if((users[item][1] - datetime.now()).total_seconds() <= 0):
    print "found an user with expired timestamp"
    db = get_con()
    try:
      print "mark the user as active"
  #1
      #update_user = 'update users set status="active", start_timestamp="None" where user_name="%s"' % item
      #execute_query(update_user)

      db.execute("update users set status='active', start_timestamp='None' where user_name=? ", (item,))
    except:
      err = "Error1 !!  %s" % sys.exc_info()[0]
      print err

    try:
      print "remove/update entries from access_status and user_details"
  #2
      #update_userdetails = 'update  user_details set ssh_pub_key="new_key", fingerprint="new_fp" where user_name="%s"' % item
      #execute_query(update_userdetails)

      db.execute("update user_details set ssh_pub_key='dummy_key', fingerprint='dummy_fp' where user_name=? ", (item,))
    except:
      err2a = "Error2.a !!  %s" % sys.exc_info()[0]
      print err2a
    try:
      #del_from_access_status = 'delete  from access_status where user_name="%s"' % item
      #execute_query(del_from_access_status)

      db.execute("delete  from access_status where user_name=? ", (item,))
    except:
      err2b = "Error2.b !!  %s" % sys.exc_info()[0]
      print err2b

    print "commit db changes..starting.."
    db.commit()
    print "committed changes ..........."

    print "update local users file"
  #3
    try:
      create_userfile()
    except:
      err3 = "Error3 !!  %s" % sys.exc_info()[0]
      print err3

  #4
    print "remove key from auth_keys"

    try:
      out = delete_from_authfile(item)  
      if out:
        print "user deleted from authfile"
      else:
        print "user couldnot be deleted"
    except:
      err4 = "Error4 !!  %s" % sys.exc_info()[0]
      print err4

