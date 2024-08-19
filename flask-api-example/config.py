import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///posts.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # not tracking modifications to DB
    EXTERNAL_API_URL = os.getenv('EXTERNAL_API_URL', 'https://jsonplaceholder.typicode.com')
