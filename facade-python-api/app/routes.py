from flask import Blueprint, jsonify, request
from .service import Service
from dotenv import load_dotenv
import requests
import os

load_dotenv()

bp = Blueprint("bp", __name__)
service = Service()


@bp.route("/posts", methods=["GET"])
def get_posts():
    # get query params from the request
    params = request.args.to_dict()
    endpoint = "posts"
    try:
        posts = service.get_data(endpoint, params)
        return jsonify({"status": "success", "posts": posts}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": "Error getting posts"}), 500
