from flask import Flask, render_template
import settings
from db import get_recent_gigs, search_for_gigs, Gigs
from craigslist.scraper import async_requests
from craigslist.craigslist_locations import locations
from utils import jsonify_gigs
from celery import Celery

app = Flask(__name__)
app.config.from_object(settings)


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

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

@celery.task(name='gigfinder.run')
def run(site):
    async_requests(locations['US'], site=site)

@app.route('/update_craigslist/<site>/')
@app.route('/update_craigslist/')
def update_craigslist(site=None):
    run.delay(site)
    return "Craigslist update process run!"

if __name__ == "__main__":
    port = 5555
    app.run(port=port, debug=True)
