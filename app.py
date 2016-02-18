from flask import Flask, render_template
import settings
from db import get_recent_gigs, search_for_gigs, Gigs
import tasks
from craigslist import  craigslist_locations, scraper
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

@app.route('/update_craigslist/<site>/')
@app.route('/update_craigslist/')
def update_craigslist(site=None):
    scraper.async_requests(craigslist_locations.locations['US'], site=site)
    return "Craigslist update process run!"

if __name__ == "__main__":
    port = 5555
    app.run(port=port, debug=True)
