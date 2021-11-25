from flask import Flask, jsonify, request
from flask_cors import CORS
from search import search_query
from user import *
from contents import indexPage
import json
import firebase_admin
import pyrebase
from firebase_admin import credentials, auth
from functools import wraps

app = Flask(__name__, static_folder='static', static_url_path='')

CORS(app, origins='*')

app_version = "v1.0"

# Connect to firebase
cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))


def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'}, 400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message': 'Invalid token provided.'}, 400
        return f(*args, **kwargs)
    return wrap


@app.route('/api/userinfo')
@check_token
def userinfo():
    return {'data': request.user}, 200


@app.route('/api/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'}, 400
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {'message': f'Successfully created user {user.uid}'}, 200
    except:
        return {'message': 'Error creating user'}, 400

# Api route to get a new token for a valid user


@app.route('/api/token', methods=['POST'])
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'}, 400


@app.route('/')
def index_page():
    resp = {}
    resp["error"] = False
    resp["message"] = "Welcome to your personalized bookmark searching service"
    resp["version"] = app_version

    return jsonify(resp)


@app.route('/get_all_bookmarks', methods=['GET'])
@check_token
def get_all_bookmarks():
    resp = all_bookmarks(request.user)
    
    return jsonify(resp)


@app.route('/search_bookmark', methods=['POST'])
@check_token
def search_bookmark():
    resp = {}
    if request.json != None:
        query = request.json.get("query")
        top_n = request.json.get("top_n")

        resp = search_query(query, top_n, request.user)
    else:
        resp["error"] = True
        resp["message"] = "no json request object found"
    return jsonify(resp)


@app.route('/add_bookmark', methods=['POST'])
def add_bookmark():
    resp = {}
    if request.json != None:
        bookmark_title = request.json.get("bookmark_name")
        bookmark_url = request.json.get("webpage_url")

        resp = indexPage(bookmark_title, bookmark_url, request.user)
    else:
        resp["error"] = True
        resp["message"] = "no json request object found"

    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
