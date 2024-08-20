class APIClient:
    def __init__(self, service):
        self.service = service

    def get_data(self, endpoint, params):
        data = self.service.get_data(endpoint, params)
        return data
