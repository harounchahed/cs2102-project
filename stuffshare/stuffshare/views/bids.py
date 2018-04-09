from stuffshare import *


@app.route('/add_bid/<int:post_id>', methods=['POST'])
def add_bid(post_id):
    if not session.get('logged_in'):
        flash("Sorry, you must log in.")
    else:
        if db_execute('insert into bids (user_email, post_id, offer) values (?, ?, ?)', [session['user_email'], post_id, request.form['offer']]) != None:
            flash('New bid successfully created.')
    return redirect(url_for('post_detail', id=post_id))


@app.route('/update_bid/<string:user_email>/<int:post_id>', methods=['POST'])
def update_bid(user_email, post_id):
    if not session.get('logged_in'):
        flash("Sorry, you must log in.")
    elif session['user_email'] != user_email:
        flash("Sorry, you can only update your own bids.")
    else:
        if db_execute('update bids set offer = ? where user_email = ? and post_id = ?',
                      [request.form['offer'], user_email, post_id]) != None:
            flash('Bid successfully updated.')
    return redirect(url_for('post_detail', id=post_id))


@app.route('/delete_bid/<string:user_email>/<int:post_id>', methods=['GET'])
def delete_bid(user_email, post_id):
    if not session.get('logged_in'):
        flash("Sorry, you must log in.")
    elif session['user_email'] != user_email:
        flash("Sorry, you can only delete your own bids.")
    else:
        if db_execute('delete from bids where user_email = ? and post_id = ?',
                      [user_email, post_id]) != None:
            flash('Your bid has been deleted.')
    return redirect(url_for('post_detail', id=post_id))
