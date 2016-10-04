from pushkey import delete_from_authfile
from db_to_ldap import  get_con

def auth_check(username):
  db = get_con()
  result = db.execute('select user_name , ssh_pub_key from user_details where user_name=?' ,(username,)).fetchall()

  # [(u'sagnik', u'dummy_key')]
  print result


  user = {}

  for item in result:
    user[item[0]] = item[1]


  for item in user:
    uniq_id = user[item].split()[2]

    #call the delete func and pass this uniq_id 
    out = delete_from_authfile(uniq_id)
    if out:
      print "user deleted from authfile"
    else:
      print "user couldnot be deleted"

