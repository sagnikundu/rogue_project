
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
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
    cur = db.execute('select u.user_name, pk.ssh_pub_key from  users u, user_details pk')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()

    key = str(request.form['pub_key'])
    #k = "xxxxtestkeyzzzz"
    #key = str(k)
    username = str(request.form['username'])
    category = str(request.form['category'])
        
#    user_fp = str(sshpubkeys.SSHKey(key).hash_md5())

    user_fp = str(sshpubkeys.SSHKey(key).hash())
    db.execute('insert into users (user_id,user_name, category) values (?, ?, ?)' , (1, username, category))

    db.execute('INSERT INTO user_details (id, user_name, ssh_pub_key, fingerprint) VALUES (?, ?, ?, ?)' , (1, username, key, user_fp))
 
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


#@app.route('/login', methods=['GET', 'POST'])
#def login():

#    error = None
#    if request.method == 'POST':

#        username = request.form['username']
#        pub_key = request.form['pub_key']
#        category = request.form['category']
        
#        completion = validate(username, pub_key, category)

#        return redirect(url_for('show_entries'))
#    return render_template('login.html', error=error)


#def validate(username, pub_key, category):

#    db = get_db()
#    pub_key = "dsdsdjnfownsfk"
#    category = "devops"

#    completion = False
#    cur = db.execute("select u.user_name, ud.ssh_pub_key from users u, user_details ud WHERE user_name=?" % (username))
#    entries = cur.fetchall()
#    if entries != NULL:
#      flash("User data already exists")
#      return render_template('show_entries.html', entries=entries)
#    else:
#      flash("New User, Adding to DB ...")
      

