from peewee import Model, TextField, DateTimeField, IntegerField, SqliteDatabase
import datetime

database = SqliteDatabase('gigs.db', threadlocals=True)


class GigFinder(Model):
    class Meta:
        database = database


class Gigs(GigFinder):
    # add website (for image/logo)
    # add possible tags or category? for example, 'gigs, computers' for craigslist.
    website = TextField(null=True)
    category = TextField(null=True)
    website_supplied_id = TextField(null=True)
    name = TextField(null=True, default=None)
    url = TextField(null=True, unique=True)
    location = TextField(null=True)
    datetime = DateTimeField(null=True)
    details = TextField(null=True)


def search_for_gigs():
    return Gigs.select().where()


def get_recent_gigs():
    return Gigs.select().where(Gigs.datetime >
                               (datetime.datetime.now() + datetime.timedelta(days=-7))).order_by(Gigs.datetime.asc())


def insert_into_db(data):
    with database.atomic():
        for item in data:
            gig = Gigs.create_or_get(website_supplied_id=item['website_supplied_id'], name=item['name'],
                                     url=item['url'],
                                     location=item['location'], datetime=item['datetime'], details=item['details'],
                                     website=item['website'], category=item['category'])

# Gigs.create_table()
