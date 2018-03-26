from stuffshare import *
from functools import wraps

from flask import flash, redirect, url_for


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        signup_username = request.form['username']
        signup_email = request.form['email']
        signup_password = request.form['password']
        db = get_db()
        db.execute('insert into users (email, name, password_hash) values (?, ?, ?)',
                [signup_email, signup_username, signup_password])
        db.commit()
        flash('Welcome to stuffshare!') 
        return redirect(url_for('login'))
    return render_template("signup.html")


