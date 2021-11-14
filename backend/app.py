from flask import Flask, jsonify, request
from flask_cors import CORS
from search import search_query
from user import *
from contents import indexPage

app = Flask(__name__, static_folder='static', static_url_path='')

CORS(app, origins='*')

app_version = "v1.0"

@app.route('/')
def index_page():
    resp = {}
    resp["error"] = False
    resp["message"] = "Welcome to your personalized bookmark searching service"
    resp["version"] = app_version
    
    return jsonify(resp)


@app.route('/search', methods=['POST'])
def get_search_results():
    resp = {}
    if request.method == 'POST' and request.json != None:
        query = request.json.get("query_string")
        username = request.json.get("username")
        code = request.json.get("code")
        top_n = request.json.get("top_n")
        
        if (validate_user(username, code)):
            resp = search_query(query, username, top_n)
        else:
            resp["error"] = True
            resp["message"] = "cannot validate user request"
            
    return jsonify(resp)

@app.route('/add', methods=['POST'])
def add_bookmark():
    resp = {}
    if request.method == 'POST' and request.json != None:
        bookmark_url = request.json.get("url")
        username = request.json.get("username")
        code = request.json.get("code")
        
        if (validate_user(username, code)):
            resp = indexPage(bookmark_url, get_user(username, code))
        else:
            resp["error"] = True
            resp["message"] = "cannot validate user request"
            
    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
