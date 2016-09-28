
from flask import Flask, request, json, session, g, redirect, url_for, abort, render_template, flash
import sys
import sqlite3
import sshpubkeys
from db_setup import get_db


app = Flask(__name__)
#from app import app
app.secret_key = 'some_secret_key_xyz'

@app.route('/')
def show_entries():
    entries = ""
    print "connecting to db"
    db = get_db()
    print "connected"
    
    #cur = db.execute('select u.user_name, pk.ssh_pub_key from  users u, user_details pk')

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
    #print result[0][1]
    if(result != [] and category.lower() == result[0][1].lower()):
        flash('Username found in trusted list.. adding user')
        
        completed, db = insert_details(username, category, key)

        if completed :
            db.commit()
            flash('New entry was successfully posted')
        else:
            flash('New entry could not be added')
    else:
        flash('User is not present in the trusted list, PLEASE send an email to Touchpoint.TigerOps <Touchpoint.TigerOps@hp.com> , to add yourself to the trusted list first !! ')
    
    return redirect(url_for('show_entries'))


def find_user(username):
    con = get_db()
    try:
        result = con.execute("select uid, category from user_ref where user_name=? ", (username,))
        
    except sqlite3.IntegrityError as e:
        flash( e.__doc__)
    except:
        flash('Error !!')

    return result.fetchall()


def insert_details(username, category, key):
    db = get_db()
    completed = False
    key = str(key)
    try:
        user_fp = str(sshpubkeys.SSHKey(key).hash_md5())

        db.execute('insert into users (user_name, category) values (?, ?)' , (username, category))

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



def verify_all(username):
    db = get_db()
    result = db.execute("select user_name, category from users where user_name=? ", (username,))
    if(result.fetchall() == []):
        return False
    else:
        return True
