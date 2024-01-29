localhost:5000

import json
from flask import Flask, jsonify, request

app = Flask(__name__)



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Add your authentication logic here
    # For example, check if the provided username and password are valid

    if username == "test_user" and password == "":
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Login failed'})

@app.route('/get', methods=['GET'])
def get_answer():
    return jsonify({'name': 'alice', 'email': 'alice@outlook.com'})

@app.route('/post', methods=['POST'])
def post_answer():
    return jsonify({'message': 'I am post method and I am working!'})

@app.route('/delete', methods=['DELETE'])
def delete_answer():
    return jsonify({'message': 'I am delete method and I am working!'})

@app.route('/put', methods=['PUT'])
def put_answer():
    return jsonify({'message': 'I am put method and I am working!'})

if __name__ == '__main__':
    app.run(debug=True)