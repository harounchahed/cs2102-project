from stuffshare import *


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
                          bids=bids))
    return render_template('show_posts.html', posts=posts)


@app.route('/add_post', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into posts (title, description, user_email, price) values (?, ?, ?, ?)',
               [request.form['title'], request.form['desc'], "hello@gmail.com", request.form['price']])
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
