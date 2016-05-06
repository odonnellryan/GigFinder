from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'scrape_craigslist_once_a_day': {
        'task': 'gigfinder.scrape',
        'schedule': timedelta(days=1),
        'args': ['cpg']
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_TIMEZONE = 'UTC'
GET_CRAIGSLIST_POST_DETAILS = False
