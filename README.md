# DataFeed

DataFeed is an experimental high-throughput data feed designed for
machine consumption.

## Use cases

I need a centralized data feed with a defined format so that distributed
applications can consume and respond to events.

1. Robotics: Multitudes of sensors and systems will gather and post data
   to this data feed. Subscribing applications will watch the feed for
   relevant events that require actions to be performed.
2. Prediction: Event prediction can be performed by analyzing the data
   stream for patterns.

## Architecture / Tech Stack

- A scalable application layer written in [Python](https://www.python.org).
- Load balanced behind [Nginx](https://nginx.org).
- Data stored using [MongoDB](https://www.mongodb.com)

## Data Format

Data should be sent to the API in the form of a POST request with the
following JSON content.

- name: The name of the 'thing' that is reporting the data.
        For example, a GPS sensor.
- value: The sensor value being recorded.
- expires: Optional date at which the record is no longer valid.
           The application that sends the data determines when it expires.

## Data Projections

The following projects the number requests per second that the system
will need to be able to handle based on a hypothetical robotics project.

1. Camera
  - Up to 5 events per second
2. Audio
  - Up to 20 events per second
3. Temperature sensor
  - 1 sample per minute
4. Encoder readings
  - Up to 100 events per second

So about 125 requests per second for incoming event data.

Let's also estimate that there will be 50 subscribers reading
the incoming data at a rate of 1 request per second.

That gives us a grand total of 175 request per second that this
system needs to be able to handle. This is definitely doable.
