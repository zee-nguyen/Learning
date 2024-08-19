from flask import Flask, request, jsonify
import requests
import logging
from dotenv import load_dotenv


# load env var
load_dotenv()

# set up Flask app
app = Flask(__name__)

# set up logger
logging.basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Fetch a list of posts from an external API"""
    



if __name__ == '__main__':
    app.run(debug=True)
