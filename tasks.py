from gigfinder import c
from craigslist import scraper

@c.task
def celery_craigslist_task(craigslist_locations):
    for country in craigslist_locations:
        scraper.craigslist_searcher(craigslist_locations[country])