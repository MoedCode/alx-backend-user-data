#!/usr/bin/env python3
import requests

# Example payload with parameters
payload = {'key1': 'value1', 'key2': 'value2'}

# Making a GET request with parameters
r = requests.get('https://httpbin.org/get', params=payload)

# Printing the URL to see the encoded parameters
print(r.url)
# Output: https://httpbin.org/get?key2=value2&key1=value1
