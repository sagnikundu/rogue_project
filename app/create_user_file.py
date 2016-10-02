import shutil, os.path
from db_to_ldap import execute_query

userfile = '/root/workspace/rogue/project/app/user_file'
bpk = '/root/workspace/rogue/project/app/user_file.bpk'


if os.path.exists(userfile):
    shutil.copyfile(userfile, bpk)

def create_userfile():
    query = "select user_name from access_status"
    result = execute_query(query)
    #print result
    with open(userfile, 'w+') as f:
        for user in result:
            f.write(user[0])
            f.write("\n")
