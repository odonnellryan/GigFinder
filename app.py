from flask import Flask, jsonify, render_template
import settings
from db import get_recent_gigs
import tasks
from json_schema import GigSchema
from craigslist import  craigslist_locations

app = Flask(__name__)
app.config.from_object(settings)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gigs/<provider>/')
@app.route('/gigs/')
def gigs(provider=None):
    gigs = get_recent_gigs()
    schema = GigSchema(many=True)
    result = schema.dump(list(gigs))
    return jsonify({'gigs': result.data})


@app.route('/update_craigslist/')
def update_craigslist():
    tasks.celery_craigslist_task.delay(craigslist_locations.locations)
    return "Craigslist update process run!"

if __name__ == "__main__":
    port = 5555
    app.run(port=port, debug=True)
