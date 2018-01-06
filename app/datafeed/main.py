import os
from flask import Flask
from flask import jsonify, request
from flask_pymongo import PyMongo, DESCENDING
from bson import json_util


app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv(
    'MONGO_URI',
    'mongodb://database/events'
)

mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():

    if request.method == 'POST':

        data = request.get_json()
        errors = []

        if 'name' not in data:
            errors.append('The field "name" is required.')

        if 'value' not in data:
            errors.append('The field "value" is required.')

        if 'expires' not in data:
            data['expires'] = None

        if errors:
            return jsonify(errors=errors), 400

        mongo.db.events.insert_one(data)

        return app.response_class(
            response=json_util.dumps(data),
            status=200,
            mimetype='application/json'
        )

    if request.method == 'DELETE':

        # Find any expired events
        mongo.db.events.delete_many({
            'expires': {
                '$exists': True,
                '$ne': None
            },
            '$where': (
                'function() {'
                'var now = new Date();'
                'var expirationDate = obj._id.getTimestamp();'
                'expirationDate.setSeconds('
                'expirationDate.getSeconds() + obj.expires'
                ');'
                'return expirationDate < now;'
                '}'
            )
        })

        return app.response_class(
            status=200,
            mimetype='application/json'
        )

    # Get the last 100 events
    events = mongo.db.events.find().sort(
        '_id', DESCENDING
    ).limit(100)

    return app.response_class(
        response=json_util.dumps(events),
        status=200,
        mimetype='application/json'
    )
