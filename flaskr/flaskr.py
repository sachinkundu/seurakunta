import json
import arrow
import time
import feedparser
from flask import g
from flask import Flask, render_template, current_app
from apscheduler.schedulers.background import BackgroundScheduler


months = {1: 'Tammikuuta', 2: 'Helmikuuta', 3: 'Maaliskuuta', 4: 'Huhtikuuta', 5: 'Toukokuuta', 6: 'Kesäkuuta', 7: 'Heinäkuuta', 8: 'Elokuuta', 9: 'Syyskuuta', 10: 'Lokakuuta', 11: 'Marraskuuta', 12: 'Joulukuuta'}


def humanize_date(date):
    arrowed = arrow.get(date)
    return str(arrowed.day) + ' ' + str(months[arrowed.month]) + ' ' + str(arrowed.year)

def get_time(date):
    t = arrow.get(date)
    return t.format('HH:mm')

app = Flask(__name__)
scheduler = BackgroundScheduler()

def get_feed():
    feed = getattr(g, '_feed', None)
    if feed is None:
        feed = g._feed = feedparser.parse('http://www.karkkilanseurakunta.fi/events-portlet/feed/parish')
    return feed

def refresh_feed():
    with app.app_context():
        g._feed = feedparser.parse('http://www.karkkilanseurakunta.fi/events-portlet/feed/parish')

with app.app_context():
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
            "&nbsp;", ""), humanize_date(entry.updated), get_time(entry.updated)])
    return render_template('main.html', output=ret)
