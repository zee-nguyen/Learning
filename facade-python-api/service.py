import requests
from flask import jsonify

class Service:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, endpoint, params=None):
        url = f'{self.base_url}/{endpoint}'

        r = requests.get(url, params=params)
        r.raise_for_status()

        return r.json()
