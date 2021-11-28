from flask import Flask, request
from flask_cors import CORS
from bookmark import *
import json
import firebase_admin
import pyrebase
from firebase_admin import credentials, auth
from functools import wraps
import os

app = Flask(__name__, static_folder='static', static_url_path='')

CORS(app, origins='*')

app_version = "v1.0"

databaseURL = os.environ.get('DATABASE_URL', '')
if (len(databaseURL) == 0):
    raise RuntimeError('DATABASE_URL is not set')

# Connect to firebase
cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred, {
    'databaseURL': databaseURL
})
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))


def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('authorization'):
            return {'error': True, 'message': f'No token provided'}, 400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'error': True, 'message': f'Invalid token provided.'}, 400
        return f(*args, **kwargs)
    return wrap


@app.route('/api/userinfo')
@check_token
def userinfo():
    return {'data': request.user["uid"]}, 200


@app.route('/api/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'error': True, 'message': f'Error missing email or password'}, 400
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {'error': False, 'message': f'Successfully created user {user.uid}'}, 200
    except:
        return {'error': True, 'message': f'Error creating user'}, 400

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
        return {'error': True, 'message': f'There was an error logging in'}, 400


@app.route('/')
def index_page():
    return {
        "error": False,
        "message": f"Welcome to your personalized bookmark searching service",
        "version": app_version
    }, 200


@app.route('/get_all_bookmarks', methods=['GET'])
@check_token
def get_all_bookmarks():
    try:
        resp = all_bookmarks(request.user["uid"])
        if (resp["error"]):
            return {'error': True, 'message': resp["message"]}, 400

        return resp, 200
    except Exception as e:
        return {'error': True, 'message': str(e)}, 400


@app.route('/search_bookmark', methods=['POST'])
@check_token
def search_bookmark():
    resp = {}
    query = request.form.get("query")
    top_n = request.form.get("top_n")

    if query is None or top_n is None:
        return {'error': True, 'message': f'Error missing query and top_n'}, 400

    try:
        resp = search_with_query(query, top_n, request.user["uid"])
        if (resp["error"]):
            return {'error': True, 'message': resp["message"]}, 400

        return resp, 200
    except Exception as e:
        return {'error': True, 'message': str(e)}, 400


@app.route('/add_bookmark', methods=['POST'])
@check_token
def add_bookmark():
    resp = {}
    bookmark_title = request.form.get("bookmark_name")
    bookmark_url = request.form.get("webpage_url")

    if bookmark_title is None or bookmark_url is None:
        return {'error': True, 'message': f'Error missing bookmark name and url'}, 400

    try:
        resp = add_to_bookmark(
            bookmark_title, bookmark_url, request.user["uid"])
        if (resp["error"]):
            return {'error': True, 'message': resp["message"]}, 400

        return resp, 200
    except Exception as e:
        return {'error': True, 'message': str(e)}, 400


@app.route('/delete_bookmark', methods=['POST'])
@check_token
def delete_bookmark():
    resp = {}
    bookmark_id = request.form.get("bookmark_id")

    if bookmark_id is None:
        return {'error': True, 'message': f'Error missing bookmark id'}, 400

    try:
        resp = delete_from_bookmark(bookmark_id, request.user["uid"])
        if (resp["error"]):
            return {'error': True, 'message': resp["message"]}, 400

        return resp, 200
    except Exception as e:
        return {'error': True, 'message': str(e)}, 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
