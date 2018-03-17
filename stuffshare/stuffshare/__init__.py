import os
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'stuffshare.db'),
    SECRET_KEY=os.urandom(24),
    USERNAME='admin',
    PASSWORD='password'
))


import posts
import stuffshare
