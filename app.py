from flask import Flask
from db import insert_into_db
from tasks import make_celery
import settings
from craigslist import scraper

app = Flask(__name__)
app.config.from_object(settings)

celery = make_celery(app)

@celery.task
def celery_craigslist_task(craigslist_locations):
    insert_into_db(scraper.craigslist_searcher(craigslist_locations))


if __name__ == "__main__":
    port = 5555
    app.run(host='0.0.0.0', port=port, debug=True)