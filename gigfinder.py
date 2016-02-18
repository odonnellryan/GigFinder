from flask import Flask, render_template
import settings
from db import get_recent_gigs, search_for_gigs, Gigs
from craigslist import  craigslist_locations, scraper
from utils import jsonify_gigs
from celery import Celery

app = Flask(__name__)
app.config.from_object(settings)


def make_celery(flask_app):
    celery = Celery(flask_app.import_name, broker=flask_app.config['CELERY_BROKER_URL'])
    celery.conf.update(flask_app.config)
    task_base = celery.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

c = make_celery(app)

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
