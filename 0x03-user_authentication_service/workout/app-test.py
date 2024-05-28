#!/usr/bin/env python3
import requests

# Data to send in the POST request
data = {'key': 'value'}

# Make a POST request to the Flask endpoint
response = requests.post('http://127.0.0.1:5005/example_endpoint', json=data)

# Print the response
print(response.json())
