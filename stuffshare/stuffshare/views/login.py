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
        user_emails = db.execute(
            'select * from users where email = ?', [login_user_email]).fetchall()
        if not user_emails and login_user_email != app.config['USERNAME']:
            flash('Sorry, the account "{}" does not exist.'.format(login_user_email))
        elif login_password != "password":
            error = "Invalid password"
        else:
            session['logged_in'] = True
            session['user_email'] = request.form['user_email']
            session['name'] = user_emails[0]["name"]
            flash('Logged in')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error=error)


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
        db = get_db()
        db.execute('insert into users (email, name, password_hash) values (?, ?, ?)',
                   [signup_user_email, signup_name, signup_password])
        db.commit()
        flash('Welcome to stuffshare!')
        return redirect(url_for('login'))
    return render_template("signup.html")


@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if request.method == 'POST':
        db = get_db()
        new_name = request.form['name']
        new_user_email = request.form['user_email']
        new_password = request.form['password']
        try:
            db.execute('UPDATE users SET  email= ?, name = ?, password_hash = ? WHERE email = ?',
                       [new_user_email, new_name, new_password, session['user_email']])
            db.commit()
            session['user_email'] = new_user_email
            flash('Profile successfully updated!')
        except Exception as e:
            flash(str(e))
        return redirect(url_for('editprofile'))
    return render_template("editprofile.html")
