from stuffshare import *


@app.context_processor
def inject_notification_generator():
    if session.get('logged_in'):
        notification_rows = db_execute(
            'select bidder, post_id, (select title from posts where id = post_id) title from notifications where post_id in (select id from posts where user_email = ?)', [session['user_email']])
        notifications = []
        for row in notification_rows:
            message = "%s has made a bid on your post:" % (
                row['bidder'])
            notifications.append(dict(
                message=message, bidder=row['bidder'], post_id=row['post_id'], title=row['title']))
        return dict(notifications=notifications)
    else:
        return dict(notifications=None)


@app.route('/delete_notification/<string:bidder>/<int:post_id>')
def delete_notification(bidder, post_id):
    db_execute('delete from notifications where bidder = ? and post_id = ?', [
               bidder, post_id])
    return redirect(request.referrer)
