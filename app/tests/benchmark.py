"""
Script for testing API performance.
"""
import time
import requests


API_URL = 'http://localhost:5000'


start_time = time.time()

# Test posting records

for i in range(1, 1001):
    requests.post(
        API_URL,
        json={
            'name': 'Benchmarking test entry %s' % i,
            'value': i,
            'expires': 60
        }
    )

post_time = time.time() - start_time

# Test getting records
get_start_time = time.time()

for i in range(1, 1001):
    requests.get(API_URL)

get_time = time.time() - get_start_time

total_execution_time = time.time() - start_time

# Present results

print('Post time: {:.2f} seconds'.format(post_time))

print('Get time:  {:.2f} seconds'.format(get_time))

print('Total execution time: {:.2f} seconds'.format(
    total_execution_time
))
