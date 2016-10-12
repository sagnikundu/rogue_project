# rogue_project

Overview :

The Lobby project is created to restrict access to users trying to ssh into any private instance in a VPC. Through the implementation of this project any user requesting access to private instances would have to follow a certain protocol. The users would have to first ssh to the jumphost ,from that jumphost the user would be able ssh into any VPC private instances.

Project Rogue application is written with Flask and SQlite3 as backend database. The app can be found here : lobby.lightaria.com


Workflow:

. The user on first loading the app , would be greeted with the application documentation page
. There is a navbar on top. Towards the end of the navbar, we have links to Sign-up and Access to environments
        - The Sign-up link would be used by users trying to access the app for their first time.
            * First time users are requested to send an email to Touchpoint.TigerOps@hp.com. The project devs would be adding the user to the database. The idea behind this is to maintain a list with trusted users. This prevents any anonymous accesses.
            * User enters the username with which he wishes to access the jumphost.
            * The user generates an ssh key pair, and uploads the public key to the app.
            * Updates the UI with the details, selects a category (DEV/QA/DEVOPS) from the dropdown.
            * Submits the details. The app validates the input and updates the sqlite3 db.
            * Once the user is added. The ssh public key would be preserved for future access requests to different VPC's.
            * If in future the user has to update the ssh keys. The sign-in process can be followed all over again.
        - Next we have the Access to environments page. (prereq : Sign-in process for that user must be completed)
            * Through this page the user would be able to request for access to one vpc at a time , eg Stable, Latest, Infogain ... etc
            * The username entered during sign-in process should be used along with the VPC env selected from the dropdown.
            * Once the user submits the request. The app would again validate all the prereqs, and pushes the user/key to the jumphost.
. The user/key would take a few minutes (~ 5 mins) to propagate to the  jumphost (lobby instance) and the private instances for the requested VPC.
. Once propagated the user would be able to ssh into the lobby instance, and to other private instances through it.
. After the access is granted, the user can continue to access the particular vpc for 3 hrs (configurable). At the end of which the user/keys are revoked from the instances/jumphost.
. After the 3rd hour , there would be a locking period of an hour. Inside the locking period the user won't be allowed to request for new accesses.
. After the locking period is over, new requests will be accepted for that user.
. The user will not be granted access to multiple vpcs at the same time.
