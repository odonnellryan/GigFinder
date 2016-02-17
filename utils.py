from flask import jsonify
from json_schema import GigSchema

def jsonify_gigs(gigs):
    schema = GigSchema(many=True)
    result = schema.dump(list(gigs))
    return jsonify({'gigs': result.data})