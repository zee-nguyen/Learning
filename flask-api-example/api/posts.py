from flask import Blueprint, request, jsonify
from services import PostService
import logging

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('/', methods=['GET'])
def get_posts():
    posts, status_code = PostService.get_posts()
    if isinstance(posts, list):
        return jsonify([post.to_dict() for post in posts]), status_code
    else:
        return jsonify(post.to_dict()), status_code

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post, status_code = PostService.get_post(post_id)
    return jsonify(post.to_dict()) if isinstance(post, Post) else jsonify(post), status_code

@posts_bp.route('/', methods=['POST'])
def create_post():
    post_data = request.json
    new_post, status_code = PostService.create_post(post_data)
    return jsonify(new_post.to_dict()), status_code

@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post_data = request.json
    updated_post, status_code = PostService.update_post(post_id, post_data)
    return jsonify(updated_post.to_dict()) if isinstance(updated_post, Post) else jsonify(updated_post), status_code

@posts_bp.route('/<int:post_id>', methods=['PATCH'])
def partial_update_post(post_id):
    post_data = request.json
    updated_post, status_code = PostService.partial_update_post(post_id, post_data)

    return jsonify(updated_post.to_dict()) if isinstance(updated_post, Post) else jsonify(update_post), status_code
