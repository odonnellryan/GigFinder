from peewee import SqliteDatabase, Model, IntegerField, TextField, DateTimeField

database = SqliteDatabase('gigFinder.db')

class GigFinder(Model):
    class Meta:
        database = database

class Gigs(GigFinder):
    website_supplied_id = TextField
    name = TextField(null=True, default=None)
    url = TextField(null=True)
    location = TextField(null=True)
    datetime = DateTimeField(null=True)
    details = TextField(null=True)

def insert_into_db(data):
    with database.atomic():
        for item in data:
            Gigs.create_or_get(website_supplied_id=item['website_supplied_id'], name=item['name'], url=item['url'],
                               location=item['location'], datetime=item['datetime'], details=item['details'])