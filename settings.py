from datetime import timedelta
from craigslist import craigslist_locations

CELERYBEAT_SCHEDULE = {
    'scrape_craigslist_once_a_day': {
        'task': 'tasks.scrape',
        'schedule': timedelta(days=2),
        'args': craigslist_locations.locations
    },
}
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_TIMEZONE = 'UTC'
GET_CRAIGSLIST_POST_DETAILS = False
