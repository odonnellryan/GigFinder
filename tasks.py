from celery_setup import c
from db import insert_into_db
from craigslist import scraper
import time

@c.task
def celery_craigslist_task(craigslist_locations):
    insert_into_db(scraper.craigslist_searcher(craigslist_locations))