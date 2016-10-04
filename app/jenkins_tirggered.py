
#####################################
# get the username, vpc <env_name> from jekins
# check to see if the user is present in access_status
# Once present proceed, or trigger necessary errors
# create env specific authfile and update the file with user key , e.g  <env_name>.authfile
# create file and update it with the user,  <env_name>.userfile
# rsync this files from the jump host.
# we will maintain env specific authfile and userfile
# when an env specific authfile/userfile updates , corresponding  jumphosts/minions rsync's it as well
#
