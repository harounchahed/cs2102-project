from stuffshare import *
from functools import wraps

from flask import flash, redirect, url_for


def logged_in(func):
    @wraps(func)
    def check_logged_in(*args, **kwargs):
        if 'user_email' not in session:
            flash("Please log in to your account.")
            return render_template('login.html')
        else:
            return func(*args, **kwargs)
    return check_logged_in


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        login_user_email = request.form['user_email']
        login_password = request.form['password']
        user_emails = db_execute(
            'select * from users where email = ?', [login_user_email])
        if user_emails is None and login_user_email != app.config['USERNAME']:
            flash('Sorry, the account "{}" does not exist.'.format(login_user_email))
        elif login_password != "password":
            error = "Invalid password"
        else:
            session['logged_in'] = True
            session['user_email'] = request.form['user_email']
            session['name'] = user_emails[0]["name"]
            flash('Logged in.')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error=error)

@app.route('/delete_account')
def delete_account():
      db = get_db()
      db.execute('delete from users where email = ?', [session['user_email']])
      db.commit() 
      session.pop('logged_in', None)
      session.pop('user', None) 
      flash('Your account has been deleted')
      return redirect(url_for('show_entries'))
      if db_execute('delete from users where email = ?', [session['user_email']]) is not None:
        session.pop('logged_in', None)
        session.pop('user_email', None)
        session.pop('name', None)
        flash('Your account has been deleted.')
      return redirect(url_for('show_entries'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_email', None)
    flash('You were logged out')
    return redirect(url_for('show_posts'))


@app.route('/getsession')
def getsession():
    if 'user_email' in session:
        return session['user_email']
    else:
        return 'Not logged in'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        signup_name = request.form['name']
        signup_user_email = request.form['user_email']
        signup_password = request.form['password']
        if db_execute('insert into users (email, name, password_hash) values (?, ?, ?)',
                      [signup_user_email, signup_name, signup_password]) is not None:
            flash('Welcome to stuffshare!')
            return redirect(url_for('show_posts'))
    return render_template("signup.html")


@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if request.method == 'POST':
        db = get_db()
        new_name = request.form['name']
        new_user_email = request.form['user_email']
        new_password = request.form['password']
        if db_execute('UPDATE users SET email= ?, name = ?, password_hash = ? WHERE email = ?',
                      [new_user_email, new_name, new_password, session['user_email']]) is not None:
            session['user_email'] = new_user_email
            session['name'] = new_name
            flash('Profile successfully updated!')
    return render_template("editprofile.html")
