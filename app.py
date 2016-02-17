from flask import Flask, render_template
import settings
from db import get_recent_gigs, search_for_gigs, Gigs
import tasks
from craigslist import  craigslist_locations
from utils import jsonify_gigs

app = Flask(__name__)
app.config.from_object(settings)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gigs/<provider>/')
@app.route('/gigs/')
def gigs(provider=None):
    gigs = get_recent_gigs()
    return jsonify_gigs(gigs)


@app.route('/search/<path:search_term>/')
def search(search_term):
    gigs = search_for_gigs(search_term)
    return jsonify_gigs(gigs)


@app.route('/update_craigslist/')
def update_craigslist():
    gig = Gigs.create_or_get(url="some test string")
    tasks.celery_craigslist_task(craigslist_locations.locations)
    return "Craigslist update process run!"

if __name__ == "__main__":
    port = 5555
    app.run(port=port, debug=True)
