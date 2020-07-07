from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/command', methods=['POST'])

def run_command():
    req = request.get_json()
    print(req)
    res = make_response(jsonify({"reponse": req}), 201)
    return res
