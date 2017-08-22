from flask import Flask
from flask import render_template
import arrow
import feedparser
import json

months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
          7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def humanize_date(date):
    arrowed = arrow.get(date)
    return str(arrowed.day) + ' ' + str(months[arrowed.month]) + ' ' + str(arrowed.year)


app = Flask(__name__)


@app.route("/")
def hello():
    d = feedparser.parse(
        'http://www.karkkilanseurakunta.fi/events-portlet/feed/parish')
    ret = []
    max_date = arrow.now().shift(weeks=+1)
    entries = [entry for entry in d.entries if arrow.get(entry.updated) < max_date]
    for entry in entries:
        ret.append([entry.title, entry.summary.replace(
            "&nbsp;", ""), humanize_date(entry.updated)])
    return render_template('main.html', output=ret)