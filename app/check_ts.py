import sqlite3
import os
import sys
from datetime import datetime, timedelta
from db_to_ldap import execute_query, get_con
from auth_check import auth_check
from create_user_file import create_userfile
from alert_mail import alert_mail

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

    alert_time = users[item][0] - timedelta(minutes=2)
    email_time = users[item][0] - timedelta(minutes=3)
    end = users[item][0]    


    if((email_time - datetime.now()).total_seconds() <= 0 ):


      #check to see if user file is present.
      user = item.strip()
      print user
      u_file = '/root/workspace/rogue/project/app/mail/%s.alert_mail.html' % user
      print u_file

      if os.path.isfile(u_file):
        print " alert email already sent ... skipping ..."
      else:
        print " mail not yet sent ... sending mail ..."
        #cmd = 'echo "hello" >  %s' % u_file
        #print cmd
        #os.system(cmd)
        alert_mail(user, end, alert_time, u_file)
        
        print "Warning mail sent to user.....>"
  
    if ((alert_time - datetime.now()).total_seconds() <= 0):

      print " Lock time reached .....user wont be able to make new request during lock time "
      db = get_con()
  
      env = db.execute("select env from access_status where user_name=? ", (item,)).fetchall()

      print "remove key from auth_keys"
      try:
        auth_check(item, env[0][0])
      except:
        err4 = "Error4 !!  %s" % sys.exc_info()[0]
        print err4
      
      try :
        print "Setting user as locked .. "
        db.execute("update users set status='locked'  where user_name=? ", (item,))
      except:
        err = "Error1 !!  %s" % sys.exc_info()[0]
        print err

      try:
        print "deleting user from status table ..."
        db.execute("delete from access_status where user_name=? ", (item,))
      except:
        err2b = "Error2.b !!  %s" % sys.exc_info()[0]
        print err2b

      print "commit db changes..starting.."
      db.commit()
      print "committed changes ..........."

      print "update local users file"
      try:
        print "ENV: %s " % env[0][0]

        create_userfile(env[0][0])
      except:
        err3 = "Error3 !!  %s" % sys.exc_info()[0]
        print err3


    else:
      print "timestamp has not expired yet ... "

