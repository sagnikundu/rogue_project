import sqlite3
import sys
from datetime import datetime, timedelta
from db_to_ldap import execute_query, get_con
from auth_check import auth_check
from create_user_file import create_userfile

query = 'select user_name, timestamp from access_status'
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


  print "starting time evaluation.." 

  for item in users : 

    print "Checking user: %s "  % item
    print users[item][0]
    #alert_time = users[item][0] - timedelta(minutes=2)
    #if ((users[item][0] - datetime.now()).total_seconds() - (alert_time).total_seconds())

    if((users[item][0] - datetime.now()).total_seconds() <= 0):
      print "found an user with expired timestamp"
      db = get_con()
  
      env = db.execute("select env from access_status where user_name=? ", (item,)).fetchall()

      print "remove key from auth_keys"
      try:
        auth_check(item, env[0][0])
      except:
        err4 = "Error4 !!  %s" % sys.exc_info()[0]
        print err4

      try:
        print "mark the user as active"
        db.execute("update users set status='active', start_timestamp='None' where user_name=? ", (item,))
      except:
        err = "Error1 !!  %s" % sys.exc_info()[0]
        print err


      try:
        db.execute("delete  from access_status where user_name=? ", (item,))
      except:
        err2b = "Error2.b !!  %s" % sys.exc_info()[0]
        print err2b

      print "commit db changes..starting.."
      db.commit()
      print "committed changes ..........."

      print "update local users file"
      try:
        #rem_users = db.execute("select user_name from access_status ").fetchall()
        print "ENV: %s " % env[0][0]

        create_userfile(env[0][0])
      except:
        err3 = "Error3 !!  %s" % sys.exc_info()[0]
        print err3



    else:
      print "timestamp has not expired yet ... "

