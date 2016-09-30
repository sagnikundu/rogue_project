
from db_to_ldap import execute_query

def create_userfile():
    query = "select user_name from access_status"
    userfile = 'user_file'
    result = execute_query(query)
    print result
    for user in result:
        with open(userfile, 'a+') as f:
            f.write(user[0])
            f.write("\n")
