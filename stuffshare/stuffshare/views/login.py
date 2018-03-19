from stuffshare import *


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
