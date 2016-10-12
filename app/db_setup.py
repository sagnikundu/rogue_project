from flask import Flask, render_template, redirect, url_for, request, g
from sqlite3 import dbapi2 as sqlite3
import os


app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname('app'))
DB = BASE_DIR+'/app/rogue3.db'
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#print DB


def connect_db():
    """Connects to the specific database."""
    # rv = sqlite3.connect(app.config['DATABASE'])
    rv = sqlite3.connect(DB)
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('rogue_schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db



@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



#------------------------------------------------------#


