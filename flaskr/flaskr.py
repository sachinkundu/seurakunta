import json
import arrow
import time
import schedule
import feedparser
from flask import g
from flask import Flask, render_template, current_app
from apscheduler.schedulers.background import BackgroundScheduler


months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
          7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def humanize_date(date):
    arrowed = arrow.get(date)
    return str(arrowed.day) + ' ' + str(months[arrowed.month]) + ' ' + str(arrowed.year)


app = Flask(__name__)
scheduler = BackgroundScheduler()

def get_feed():
    feed = getattr(g, '_feed', None)
    if feed is None:
        feed = g._feed = feedparser.parse('http://www.karkkilanseurakunta.fi/events-portlet/feed/parish')
    return feed

def refresh_feed():
    with app.app_context():
        print('Refresh feed...')
        g._feed = feedparser.parse('http://www.karkkilanseurakunta.fi/events-portlet/feed/parish')

with app.app_context():
    print(current_app.name)
    scheduler.add_job(refresh_feed, 'interval', days=1)
    scheduler.start()

@app.route("/")
def hello():
    feed = get_feed()
    ret = []
    max_date = arrow.now().shift(weeks=+1)
    entries = [entry for entry in feed.entries if arrow.get(entry.updated) < max_date]
    for entry in entries:
        ret.append([entry.title, entry.summary.replace(
            "&nbsp;", ""), humanize_date(entry.updated)])
    return render_template('main.html', output=ret)
