from service import Service
import unittest
from unittest.mock import Mock, patch
from dotenv import load_dotenv
import requests
import os

load_dotenv()


class TestService(unittest.TestCase):
    @patch("service.requests.get")
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
        base_url = os.getenv("BASE_URL")

        service = Service(base_url)

        result = service.get_data("posts")
        self.assertEqual(result, mock_resp_values)
        mock_get.assert_called_once_with(f"{base_url}/posts", params=None)

    @patch("service.requests.get")
    def test_get_data_failture(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError("Error")
        base_url = os.getenv("BASE_URL")

        service = Service(base_url)
        with self.assertRaises(requests.exceptions.HTTPError):
            service.get_data("posts")


if __name__ == "__main__":
    unittest.main()
