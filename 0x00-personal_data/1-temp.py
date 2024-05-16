#!/usr/bin/env python3
from flask import Flask, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Define a custom formatter
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

# Create a file handler and set its formatter
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)

# Add the file handler to the root logger
logging.getLogger().addHandler(file_handler)


@app.route('/')
def index():
    app.logger.info('User accessed the index page')
    return 'Hello, welcome to the index page!'


@app.route('/error')
def error():
    # Simulate an error
    try:
        result = 10 / 0
    except Exception as e:
        app.logger.error('Error occurred: %s', e, exc_info=True)
        return 'Error occurred: {}'.format(e), 500


@app.route('/info')
def info():
    app.logger.info('User accessed the info page')
    return 'This is an informational page.'


@app.route('/debug')
def debug():
    app.logger.debug('Debug message: request headers: %s', request.headers)
    return 'Debug information logged.'


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
