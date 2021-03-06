import os
import sqlite3
import sys
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

sys.dont_write_bytecode = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'stuffshare.db'),
    SECRET_KEY=os.urandom(24),
    USERNAME='admin',
    PASSWORD='password'
))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def db_execute(query, params=None):
    try:
        db = get_db()
        if params:
            results = db.execute(query, params).fetchall()
        else:
            results = db.execute(query).fetchall()
        db.commit()
        return results
    except Exception as e:
        flash(str(e))
        return None


import views.posts
import views.login
import views.bids
import views.notifications


if __name__ == '__main__':
    app.run()
