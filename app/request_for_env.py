
import sys
from datetime import datetime, timedelta
from db_setup import get_db

###################### LOGIC ########################
# get the username, vpc <env_name> from jekins
# check to see if the user is present in access_status
# Once present proceed, or trigger necessary errors
# create env specific authfile and update the file with user key , e.g  <env_name>.authfile
# create file and update it with the user,  <env_name>.userfile
# rsync this files from the jump host.
# we will maintain env specific authfile and userfile
# when an env specific authfile/userfile updates , corresponding  jumphosts/minions rsync's it as well
######################################################

def req_env(username, env):
  db = get_db()
  completed = False
  start_time = datetime.now()
  try:
    db.execute('insert into access_status (user_name, env, timestamp) values (?, ?, ?)' , (username, env, start_time))


    db.execute("update users set status='inactive', start_timestamp=? where user_name=? ", (start_time, username))
  except:
    err = "Error while add to env : !!  %s" % sys.exc_info()[0]
    flash(err)

  status = verify_all(username)
  return (status, db)




def verify_all(username):
    db = get_db()
    result = db.execute("select user_name ,ssh_pub_key from user_details where user_name=? ", (username,))
    if(result.fetchall() == []):
        return False
    else:
        return True

