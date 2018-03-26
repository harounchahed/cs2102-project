from stuffshare import *


@app.route('/add_bid/<int:post_id>', methods=['POST'])
def add_bid(post_id):
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into bids (user_email, post_id, offer) values (?, ?, ?)',
               [session['user'], post_id, request.form['offer']])
    db.commit()
    flash('New bid successfully created.')
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
