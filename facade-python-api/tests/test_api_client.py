from app.api_client import APIClient
import unittest
from unittest.mock import Mock, patch
from dotenv import load_dotenv
import requests
import os

load_dotenv()
base_url = os.getenv("BASE_URL")


class TestAPIClient(unittest.TestCase):
    @patch("app.api_client.requests.get")
    def test_get_data_success(self, mock_get):
        mock_resp = Mock()
        mock_resp_values = [
            {
                "userId": 1,
                "id": 1,
                "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
            }
        ]
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_resp_values
        mock_get.return_value = mock_resp

        api_client = APIClient()

        result = api_client.get_data("posts")
        self.assertEqual(result, mock_resp_values)
        mock_get.assert_called_once_with(f"{base_url}/posts", params=None)

    @patch("app.api_client.requests.get")
    def test_get_data_failture(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError("Error")
        api_client = APIClient()
        with self.assertRaises(requests.exceptions.HTTPError):
            api_client.get_data("posts")


if __name__ == "__main__":
    unittest.main()
