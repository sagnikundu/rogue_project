import sqlite3
import os
import sys
from datetime import datetime, timedelta
from db_to_ldap import execute_query, get_con

query = "select user_name, start_timestamp from users where status='locked'"

data = execute_query(query)

if data == []:
  print "no active entries in db"
else:
  users = {}
  for item in data:
    start_time = datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S.%f")      # unicode to datetime object
    end_time = start_time + timedelta(minutes=5)
    users[item[0]] = [end_time]

  print "User List : %s" % users


  print "Start time evaluation...." 

  for item in users :
    print "Checking locked user: %s "  % item
    end_time = users[item][0]

    if((end_time - datetime.now()).total_seconds() <= 0):
      
      print "End time reached. Marking the user: %s  as active" % item
      try:
        db = get_con()
        print "changing DB ...."
        db.execute("update users set status='active', start_timestamp='None' where user_name=? ", (item,))
      except:
        err = "Error1 !!  %s" % sys.exc_info()[0]
        print err      
      print "commit db changes..starting.."
      db.commit()
      print "committed changes ..........."
      print "deleting the warning mail file for the user"
      user = item.strip()
      u_file = '/root/workspace/rogue/project/app/mail/%s.alert_mail.html' % user
      os.remove(u_file)
      print "mail file deleted ..."
