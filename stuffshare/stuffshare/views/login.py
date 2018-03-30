from stuffshare import *
from functools import wraps

from flask import flash, redirect, url_for


def logged_in(func):
    @wraps(func)
    def check_logged_in(*args, **kwargs):
        if 'user' not in session:
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
        login_email = request.form['username']
        login_password = request.form['password']
        emails = db.execute(
            'select * from users where email = ?', [login_email]).fetchall()
        if not emails and login_email != app.config['USERNAME']:
            flash('Sorry, the account "{}" does not exist.'.format(login_email))
        elif login_password != "password":
            error = "Invalid password"
        else:
            session['logged_in'] = True
            session['user'] = request.form['username']
            print(emails[0]["name"])
            session['name'] = emails[0]["name"]
            flash('Logged in')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/getsession')
def getsession():   
    if 'user' in session:
        return session['user']
    else:
        return 'Not logged in'

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

@app.route('/editprofile', methods=['GET','POST'])
def editprofile():    
    if request.method == 'POST':
        db = get_db()
        new_username = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']  
        try:       
            db.execute('UPDATE users SET  email= ?, name = ?, password_hash = ? WHERE email = ?',   
                    [new_email, new_username, new_password, session['user'] ])
            db.commit()
            session['user'] = new_email
            flash('Profile successfully updates!')
        except Exception as e: 
            flash(str(e))
        return redirect(url_for('editprofile'))
    return render_template("editprofile.html")      
