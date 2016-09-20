
from flask import Flask, request, json, session, g, redirect, url_for, abort, render_template, flash
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
    if(result == []):
        completed, db = insert_details(username, category, key)

        if completed :
            db.commit()
            flash('New entry was successfully posted')
        else:
            flash('New entry could not be added')
    else:
        flash('User already exists')
    
    return redirect(url_for('show_entries'))


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
    user_fp = str(sshpubkeys.SSHKey(key).hash())

    try:
        db.execute('insert into users (user_name, category) values (?, ?)' , (username, category))

        db.execute('INSERT INTO user_details (user_name, ssh_pub_key, fingerprint) VALUES (?, ?, ?)' , (username, key, user_fp))

    except sqlite3.IntegrityError as e:
        flash( e.__doc__)
        flash('Integrity Error')
    except sqlite3.OperationalError as o:
        flash( o.__doc__)
        flash('Operational error')
    except:
        flash('Unexpected Error')

    return (True, db)


