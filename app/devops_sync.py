#Run this script as a cron every 24 hrs

from db_to_ldap import get_con


# get a db handle
db = get_con()

# query db to get the current list of devops users
devops_users = db.execute("select user_name from users where category='devops'").fetchall()

with open('devops_list', 'w+') as f:
  for user in devops_users:
    f.write(user[0])
    f.write("\n")



