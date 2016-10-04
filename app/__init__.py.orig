
from flask import Flask, request, json, session, g, redirect, url_for, abort, render_template, flash
import sys
import sqlite3
import sshpubkeys
from datetime import datetime, timedelta
from db_setup import get_db
from create_user_file import create_userfile
from pushkey import update_local_auth_file

app = Flask(__name__)
#from app import app
app.secret_key = 'some_secret_key_xyz'

@app.route('/')
def show_entries():
    entries = ""
    print "connecting to db"
    db = get_db()
    print "connected"
    

    cur = db.execute('select * from user_details')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


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
                
                # creating a local copy for the users present in access_status
                print "Creating user file"
                create_userfile()
                print "update authfile"
                if update_local_auth_file(key):
                    print "auth file updated"
                else:
                    print "auth file could not be updated"    
                
            else:
                flash('New entry could not be added')
        else:
            flash('User is currently inactive.. wait for the lockdown period to expire ')
    else:
        flash('User is not present in the trusted list, PLEASE send an email to Touchpoint.TigerOps <Touchpoint.TigerOps@hp.com> , to add yourself to the trusted list first !! ')
    
    return redirect(url_for('show_entries'))


# users table is the ref table now. Entries to be updated manually here.

def find_user(username):
    con = get_db()
    try:
        result = con.execute("select * from users where user_name=? ", (username,))
        
    except sqlite3.IntegrityError as e:
        flash( e.__doc__)
    except:
        flash('Error !!')

    return result.fetchall()


def insert_details(username, category, key):
    db = get_db()
    completed = False
    key = str(key)
    start_time = datetime.now()
    try:
        user_fp = str(sshpubkeys.SSHKey(key).hash_md5())

        print "start of insert"

        db.execute('insert into access_status (user_name, env, timestamp) values (?, ?, ?)' , (username, category, start_time))
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

        db.execute("update users set status='inactive', start_timestamp=? where user_name=? ", (start_time, username))


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

