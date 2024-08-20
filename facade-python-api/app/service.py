from .api_client import APIClient


class Service:
    def __init__(self):
        self.client = APIClient()

    def get_data(self, endpoint, params):
        data = self.client.get_data(endpoint, params)
        return data
