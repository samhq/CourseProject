from flask import Flask, jsonify, request
from flask_cors import CORS
from bm25_search import search_query

app = Flask(__name__, static_folder='static', static_url_path='')

CORS(app, origins='*')


@app.route('/')
def index_page():
    return app.send_static_file('index.html')


@app.route('/search_query', methods=['POST'])
def get_query_search_results():
    resp = {}
    if request.method == 'POST' and request.json != None:
        query = request.json.get("query_string")
        username = request.json.get("username")
        top_n = request.json.get("top_n")
        resp = search_query(query, username, top_n)
    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
