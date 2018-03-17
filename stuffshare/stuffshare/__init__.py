import os
from flask import Flask
import sys

sys.dont_write_bytecode = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'stuffshare.db'),
    SECRET_KEY=os.urandom(24),
    USERNAME='admin',
    PASSWORD='password'
))
import views.posts
import views.login
