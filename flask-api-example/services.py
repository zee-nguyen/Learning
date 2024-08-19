import requests
from config import Config
from repository import PostRepository

class PostService:
    @staticmethod
    def get_posts():
        posts = PostRepository.get_all_posts()
        if posts:
            return posts, 200
        else:
            resp = requests.get(f'{Config.EXTERNAL_API_URL}/posts')
            return resp.json(), resp.status_code

    @staticmethod
    def get_post(post_id):
        post = PostRepository.get_post_by_id(post_id)
        if post:
            return post, 200
        else:
            resp = requests.get(f'{Config.EXTERNAL_API_URL}/posts/{post_id}')
            return resp.json(), resp.status_code

    @staticmethod
    def create_post(post_data):
        new_post = PostRepository.add_post(post_data)
        return new_post, 201

    @staticmethod
    def update_post(post_id, post_data):
        updated_post = PostRepository.update_post(post_id, post_data)
        if updated_post:
            return updated_post, 200
        else:
            resp = requests.put(f'{Config.EXTERNAL_API_URL}/posts/{post_id}', json=post_data)
            return resp.json(), resp.status_code

    @staticmethod
    def partial_update_post(post_id, post_data):
        post = PostRepository.get_post_by_id(post_id)
        if post:
            updated_post = PostRepository.update_post(post_id, post_data)
            return updated_post, 200
        else:
            resp = requests.patch(f'{Config.EXTERNAL_API_URL}/posts/{post_id}')
            return resp.json(), resp.status_code
