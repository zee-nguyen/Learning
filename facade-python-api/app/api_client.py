import requests
import os
from dotenv import load_dotenv

load_dotenv()


class APIClient:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")

    def get_data(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"

        r = requests.get(url, params=params)
        r.raise_for_status()

        return r.json()
