from models import db, Post

class PostRepository:
    @staticmethod
    def get_all_posts():
        return Post.query.all()
    
    @staticmethod
    def get_post_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def add_post(post_data):
        new_post = Post(**post_data)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def update_post(post_id, post_data):
        post = Post.query.get(post_id)
        if post:
            for k, v in post_data.items():
                setattr(post, k, v)
            db.session.commit()
        return post

    @staticmethod
    def delete_post(post_id):
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
        return post
