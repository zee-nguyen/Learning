from flask import Flask, jsonify, request
from service import Service
from api_client import APIClient
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
service = Service(os.getenv('BASE_URL'))
api_client = APIClient(service)


@app.route('/posts', methods=['GET'])
def get_posts():
    # get query params from the request
    params = request.args.to_dict()
    endpoint = 'posts'
    try:
        posts = api_client.get_data(endpoint, params)
        return jsonify({'status': 'success', 'posts': posts}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': 'Error getting posts'}), 500


if __name__ == '__main__':
    app.run(debug=True)
