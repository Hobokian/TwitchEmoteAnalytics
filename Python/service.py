# service.py reads a json file and creates an API for front end display

from flask import Flask, jsonify, abort, make_response, request, url_for
import json

app = Flask(__name__)


@app.route('/twitchemoteanalytics/api/v1.0', methods=['GET'])
def get_tasks():
    data = json.loads(open('data.json').read())
    return jsonify(data)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
