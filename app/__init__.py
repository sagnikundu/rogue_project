
from flask import Flask, request, json, session, g, redirect, url_for, abort, render_template, flash
import sys
import sqlite3
import sshpubkeys
from datetime import datetime, timedelta
from db_setup import get_db
from create_user_file import create_userfile
from pushkey import update_local_auth_file
from request_for_env import req_env
from greet_mail import greet_mail

app = Flask(__name__)
#from app import app
app.secret_key = 'some_secret_key_xyz'

@app.route('/')
def show_entries():
    return render_template('new_show_entries.html')


@app.route('/add')
def add_entries():
    return render_template('add_entries.html')


@app.route('/request')
def request_access():
    return render_template('request_access.html')



@app.route('/request', methods=['GET', 'POST'])
def request_entry():
    name = str(request.form['username'])
    env = str(request.form['env']).lower()

    flash("User : "+name+" is seeking access for env: "+env)
    # request_for_env.py
    result = find_user(name)
    
    if(result != []):
        flash('Username found in trusted list.. checking user status.')
        user_status = result[0][1]

        print "User-status: %s" % user_status

        if(user_status == 'active'):
            flash('User is active.. adding '+name+' to env: '+env)
            completed, db, end_ts, blackout_ts = req_env(name, env)
            key = db.execute("select ssh_pub_key from user_details where user_name=? ", (name,)).fetchall()
            key = str(key[0][0])

            print "key : %s" % key

            print "Sending greeting mail to : %s" % name
            greet_mail(name, env, end_ts, blackout_ts)

            if completed :
                db.commit()
                flash("User added to: "+env)

                print  "creating %s user file..." % name
                create_userfile(env)
                print "updating %s auth file..." % env
                update_local_auth_file(key, env, name)
            else:
                flash("User couldnot be added to :"+env)
        else:
            flash('User is currently inactive.. wait for the lockdown period to expire ')
    else:
        flash('User is not present in the trusted list, PLEASE send an email to Touchpoint.TigerOps <Touchpoint.TigerOps@hp.com> , to add yourself to the trusted list first !! ')    
    

    return redirect(url_for('request_access'))



@app.route('/add', methods=['GET', 'POST'])
def add_entry():

    #db = get_db()

    key = str(request.form['pub_key'])
    username = str(request.form['username'])
    category = str(request.form['category'])

    result = find_user(username)

    if(result != [] and category.lower() == result[0][3].lower()):
        flash('Username found in trusted list.. checking user status.')

        user_status = result[0][1]
        if(user_status == 'active'):
            flash('User is active.. adding user')
            completed, db = insert_details(username, category, key)

            if completed :
                db.commit()
                flash('New entry was successfully posted')
                
            else:
                flash('New entry could not be added')
        else:
            flash('User is currently inactive.. wait for the lockdown period to expire ')
    else:
        flash('User is not present in the trusted list, PLEASE send an email to Touchpoint.TigerOps <Touchpoint.TigerOps@hp.com> , to add yourself to the trusted list first !! ')
    
    return redirect(url_for('add_entries'))


# users table is the ref table now. Entries to be updated manually here.

def find_user(username):    
    con = get_db()
    try:
        result = con.execute("select * from users where user_name=? ", (username,))

    except sqlite3.IntegrityError as e:
        flash( e.__doc__)
    except:
        err = "Error !!  %s" % sys.exc_info()[0]
        flash(err)

    return result.fetchall()


def insert_details(username, category, key):
    db = get_db()
    completed = False
    key = str(key)
    start_time = datetime.now()
    try:
        user_fp = str(sshpubkeys.SSHKey(key).hash_md5())

        print "start of insert"

        print "verify user" 

        details = verify_all(username)
        print "verification complete"

        if details:
            flash("user already present, now if keys match no need to update else update key")
            fetch_key = get_keys_from_db(username)
            print fetch_key

            if str(fetch_key) == key:
                print "Keys match, no need for update"
            else:
                print "Key mismatch, updating new keys for %s" % username
                db.execute('update user_details set ssh_pub_key=?, fingerprint=? where user_name=?', (key, user_fp, username))

        else:
            print "First time user !! updating user details"
            db.execute('INSERT INTO user_details (user_name, ssh_pub_key, fingerprint) VALUES (?, ?, ?)' , (username, key, user_fp))



    except sqlite3.IntegrityError as e:
        flash( e.__doc__)
        flash('Integrity Error')
    except sqlite3.OperationalError as o:
        flash( o.__doc__)
        flash('Operational error')
    except:
        err = "Error !!  %s" % sys.exc_info()[0]
        flash(err)
    
    status = verify_all(username)
    
    return (status, db)

def get_keys_from_db(username):
    db = get_db()
    result = db.execute('select ssh_pub_key from user_details where user_name=?', (username,)).fetchall()
    print "+++"+username
    print result
    return result[0][0]


def verify_all(username):
    db = get_db()
    result = db.execute("select user_name ,ssh_pub_key from user_details where user_name=? ", (username,))
    if(result.fetchall() == []):
        return False
    else:
        return True

