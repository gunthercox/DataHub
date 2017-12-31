from flask import Flask
from flask import jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://postgres:secureinsidedockernetwork@database/events'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(120))
    expires = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return '<Event %r>' % self.name

def serialize_event(event):
    return {
        'id': event.id,
        'name': event.name,
        'value': event.value,
        'expires': event.expires
    }


@app.route("/", methods=['GET', 'POST'])
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

        event = Event(
            name=data.get('name'),
            value=data.get('value'),
            expires=data.get('expires')
        )

        db.session.add(event)
        db.session.commit()

        return jsonify(serialize_event(event)), 200

    # Get the last 100 events
    events = Event.query.order_by(Event.id.desc()).limit(100)

    return jsonify([
        serialize_event(e) for e in events
    ])
