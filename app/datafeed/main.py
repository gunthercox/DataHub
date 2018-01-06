import os
import json
import uuid
import redis
from flask import Flask
from flask import jsonify, request


DEFAULT_EVENT_EXPIRATION_SECONDS = 60

app = Flask(__name__)

db = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', 'redis')
)


def create_event(**data):

    # Create a unique id for the event
    pk = uuid.uuid4().hex

    expiration_seconds = data.get(
        'expires',
        DEFAULT_EVENT_EXPIRATION_SECONDS
    )

    db.set(pk, json.dumps(data), ex=expiration_seconds)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        data = request.get_json()
        errors = []

        if 'name' not in data:
            errors.append('The field "name" is required.')

        if 'value' not in data:
            errors.append('The field "value" is required.')

        if errors:
            return jsonify(errors=errors), 400

        # Save the event in redis
        create_event(**data)

        return jsonify(data), 200

    # Get the last 100 events
    event_hashes = db.scan(cursor=0, count=100)[1]
    events = []

    # Sort the uuid hashes by time
    for event_hash in sorted(event_hashes):
        dump_data = db.get(event_hash)
        events.append(json.loads(dump_data))

    return jsonify(events), 200
