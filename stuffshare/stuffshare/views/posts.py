from stuffshare import *
from login import logged_in


@app.route('/')
def show_posts():
    db = get_db()
    posts_rows = db.execute(
        'select * from posts order by id desc').fetchall()
    posts = []
    for post in posts_rows:
        bids = db.execute(
            'select * from bids where post_id = ?', [post["id"]]).fetchall()
        posts.append(dict(id=post["id"],
                          user_email=post["user_email"],
                          title=post["title"],
                          price=post["price"],
                          desc=post["description"],
                          no_bids=len(bids)))
    return render_template('show_posts.html', posts=posts)

@app.route('/delete_post/<string:user_email>/<int:post_id>', methods=['GET'])
def delete_post(user_email, post_id):
    if not session.get('logged_in'):
        abort(401)
    elif session['user'] != user_email:
        flash("Sorry, you can only delete your own posts.")
    else:
        db = get_db()
        db.execute('delete from posts where id = ?',
                   [post_id])
        db.commit()
        flash('Your post has been deleted.')
    return redirect(url_for('show_user_posts', user_email = user_email))

@app.route('/add_post', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into posts (title, description, user_email, price) values (?, ?, ?, ?)',
               [request.form['title'], request.form['desc'], session['user'], request.form['price']])
    db.commit()
    flash('New post was successfully created')
    return redirect(url_for('show_posts'))


@app.route('/posts/<int:id>', methods=['GET'])
def post_detail(id):
    db = get_db()
    post = db.execute(
        'select * from posts where id = ?', [id]).fetchall()
    bids = db.execute(
        'select * from bids where post_id = ?', [id]).fetchall()
    if not post:
        flash("Sorry, that item does not exist")
        return redirect(url_for('show_posts'))
        # Note we access the first item in the list since we only expect one item
    return render_template('post_detail.html', post=post[0], bids=bids)


@app.route('/<string:user_email>/posts', methods=['GET'])
def show_user_posts(user_email):
    db = get_db()
    posts_rows = db.execute(
        'select * from posts where user_email = ? order by id desc', [user_email]).fetchall()
    posts = []
    for post in posts_rows:
        bids = db.execute(
            'select * from bids where post_id = ?', [post["id"]]).fetchall()
        posts.append(dict(id=post["id"],
                          user_email=post["user_email"],
                          title=post["title"],
                          price=post["price"],
                          desc=post["description"],
                          no_bids=len(bids)))
    return render_template('user_posts.html', posts=posts, user_email=user_email)
