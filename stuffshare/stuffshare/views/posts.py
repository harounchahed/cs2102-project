from stuffshare import *
from login import logged_in


@app.route('/')
def show_posts():
    posts_rows = db_execute(
        'select * from posts order by id desc')
    posts = []
    for post in posts_rows:
        bids = db_execute(
            'select * from bids where post_id = ?', [post["id"]])
        if bids is not None:
            posts.append(dict(id=post["id"],
                              user_email=post["user_email"],
                              title=post["title"],
                              price=post["price"],
                              desc=post["description"],
                              no_bids=len(bids)))
        else:
            posts.append(dict(id=post["id"],
                              user_email=post["user_email"],
                              title=post["title"],
                              price=post["price"],
                              desc=post["description"],
                              no_bids=0))
    return render_template('show_posts.html', posts=posts)


@app.route('/delete_post/<string:user_email>/<int:post_id>', methods=['GET'])
def delete_post(user_email, post_id):
    if not session.get('logged_in'):
        flash("Please log in to your account.")
    elif session['user_email'] != user_email:
        flash("Sorry, you can only delete your own posts.")
    else:
        if db_execute('delete from posts where id = ?', [post_id]) is not None:
            flash('Your post has been deleted.')
    return redirect(url_for('show_user_posts', user_email=user_email))


@app.route('/<string:user_email>/add_post', methods=['POST'])
def add_post(user_email):
    if not session.get('logged_in'):
        flash("Please log in to your account.")
    else:
        if db_execute('insert into posts (title, description, user_email, price) values (?, ?, ?, ?)', [request.form['title'], request.form['desc'], session['user_email'], request.form['price']]) is not None:
            flash('New post was successfully created.')
    return redirect(url_for('show_user_posts', user_email=user_email))


@app.route('/posts/<int:id>', methods=['GET'])
def post_detail(id):
    post = db_execute(
        'select *, (select name from users where email = user_email) name from posts where id = ?', [id])
    bids = db_execute(
        'select *, (select name from users where email = user_email) name from bids where post_id = ?', [id])
    if not post:
        flash("Sorry, that item does not exist")
        return redirect(url_for('show_posts'))
        # Note we access the first item in the list since we only expect one item
    return render_template('post_detail.html', post=post[0], bids=bids)


@app.route('/<string:user_email>/posts', methods=['GET', 'POST'])
def show_user_posts(user_email):
    posts_rows = db_execute(
        'select * from posts where user_email = ? order by id desc', [user_email])
    posts = []
    if posts_rows is not None:
        for post in posts_rows:
            bids = db_execute(
                'select * from bids where post_id = ?', [post["id"]])
            if bids is not None:
                posts.append(dict(id=post["id"],
                                  user_email=post["user_email"],
                                  title=post["title"],
                                  price=post["price"],
                                  desc=post["description"],
                                  no_bids=len(bids)))
            else:
                posts.append(dict(id=post["id"],
                                  user_email=post["user_email"],
                                  title=post["title"],
                                  price=post["price"],
                                  desc=post["description"],
                                  no_bids=0))
    return render_template('user_posts.html', posts=posts, user_email=user_email)
