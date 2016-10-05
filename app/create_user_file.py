import shutil, os.path
from db_to_ldap import get_con


def create_userfile(env):

    db = get_con()
    user_file = '/root/workspace/rogue/project/app/%s.user_file' % env
    user_bpk = '/root/workspace/rogue/project/app/%s.user_file.bpk' % env

#    auth_file = '/root/workspace/rogue/project/app/%s.auth_file' % env    
#    auth_bpk = '/root/workspace/rogue/project/app/%s.auth_file.bpk' % env

    if os.path.exists(user_file):
        shutil.copyfile(user_file, user_bpk)

#    if os.path.exists(auth_file):
#        shutil.copyfile(auth_file, auth_bpk)


    result1 = db.execute("select user_name from access_status where env=? ", (env,)).fetchall()
    with open(user_file, 'w+') as f:
        for user in result1:
            f.write(user[0])
            f.write("\n")

#    result2 = db.execute("select a.ssh_pub_key from user_details as a, access_status as b  where b.user_name = a.user_name and b.env=? ", (env,)).fetchall()
#    with open(auth_file, 'w+') as f:
#        for key in result2:
#            f.write(key[0])
#            f.write("\n")

