from stuffshare import *
from login import logged_in


def order_by(values):
    def order(e):
        return values.index(e[0])
    return order


@app.route('/')
@app.route('/<string:filter>')
def show_posts(filter=None):
    if filter is None:
        header = "Recent posts"
        activity = None
        posts_rows = db_execute(
            'select *, (select name from users where email = user_email) name from posts order by id desc')
    elif filter == "most_active":
        header = "Posts ranked by most active users"
        activity_rows = db_execute(
            'select (select name from users where email = poster) poster, post_count, ab_count from user_activity')
        activity = activity_rows[:5]
        activity_names = [row[0] for row in activity_rows]
        posts_rows = db_execute(
            'select (select name from users where email = user_email) name, * from posts')
        posts_rows = sorted(posts_rows, key=order_by(activity_names))
    posts = []
    for post in posts_rows:
        bids = db_execute(
            'select * from bids where post_id = ?', [post["id"]])
        if bids is not None:
            no_bids = len(bids)
        else:
            no_bids = 0
        posts.append(dict(id=post["id"],
                          name=post['name'],
                          user_email=post["user_email"],
                          title=post["title"],
                          price=post["price"],
                          description=post["description"],
                          no_bids=no_bids))
    return render_template('show_posts.html', activity=activity, header=header, posts=posts)


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
    accepted_bidder = db_execute(
        'select * from accepted_bids where post_id = ?', [id])
    if accepted_bidder is not None and len(accepted_bidder) == 1:
        accepted_bidder = accepted_bidder[0]['user_email']
    if not post:
        flash("Sorry, that item does not exist")
        return redirect(url_for('show_posts'))
        # Note we access the first item in the list since we only expect one item
    return render_template('post_detail.html', post=post[0], bids=bids, accepted_bidder=accepted_bidder)


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
