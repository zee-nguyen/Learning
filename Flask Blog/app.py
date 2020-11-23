from flask import Flask, render_template
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__)

# get DB connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    # use row_factory to have name-based access to columns
    # db will return rows that behave like Python dict
    conn.row_factory = sqlite3.Row
    return conn

# get a single post
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)
    
    return post

@app.route('/')
def index():
    conn = get_db_connection()
    # fetch all the rows of the query result
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)