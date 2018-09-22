import os
from flask import Flask
from flask import jsonify, request
from redis import StrictRedis


app = Flask(__name__)

redis = StrictRedis(
    host=os.getenv('REDIS_HOST', 'redis')
)


@app.route('/', methods=['GET', 'POST'])
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

        redis.set(data['name'], data['value'], ex=data['expires'])

        return jsonify(data), 200

    # Return all keys matching the specified pattern
    pattern = request.args.get('filter', '*')
    events = redis.keys(pattern)

    return jsonify([
        event.decode('ascii') for event in events
    ])


@app.route('/<string:name>', methods=['GET'])
def detail(name):
    value = redis.get(name)

    if not value:
        return jsonify(
            errors={
                'value': 'No value exists for this key.'
            }
        ), 400

    try:
        value = int(value)
    except ValueError:
        pass

    return jsonify(
        value=value
    )
