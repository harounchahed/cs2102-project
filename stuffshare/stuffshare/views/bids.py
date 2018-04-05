from stuffshare import *


@app.route('/add_bid/<int:post_id>', methods=['POST'])
def add_bid(post_id):
    if not session.get('logged_in'):
        abort(401)
    try:
        db = get_db()
        db.execute('insert into bids (user_email, post_id, offer) values (?, ?, ?)',
                   [session['user_email'], post_id, request.form['offer']])
        db.commit()
        flash('New bid successfully created.')
    except Exception as e:
        flash(str(e))
    return redirect(url_for('post_detail', id=post_id))


@app.route('/update_bid/<string:user_email>/<int:post_id>', methods=['POST'])
def update_bid(user_email, post_id):
    if not session.get('logged_in'):
        abort(401)
    elif session['user_email'] != user_email:
        flash("Sorry, you can only update your own bids.")
    try:
        db = get_db()
        db.execute('update bids set offer = ? where user_email = ? and post_id = ?',
                   [request.form['offer'], user_email, post_id])
        db.commit()
        flash('Bid successfully updated.')
    except Exception as e:
        flash(str(e))
    return redirect(url_for('post_detail', id=post_id))


@app.route('/delete_bid/<string:user_email>/<int:post_id>', methods=['GET'])
def delete_bid(user_email, post_id):
    if not session.get('logged_in'):
        abort(401)
    elif session['user'] != user_email:
        flash("Sorry, you can only delete your own bids.")
    else:
        db = get_db()
        db.execute('delete from bids where user_email = ? and post_id = ?',
                   [user_email, post_id])
        db.commit()
        flash('Your bid has been deleted.')
    return redirect(url_for('post_detail', id=post_id))
