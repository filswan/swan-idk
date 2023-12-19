""" Tests for Computing Providers """

import pytest
import requests
from mock.mock import Mock, MagicMock, patch
from src.swan.api.cp import get_all_cp_machines
from src.swan.exceptions.request_exceptions import SwanHTTPError, SwanRequestError


class TestComputingProviders:
    def test_retrieve_all_cp_machines(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "data": {
                "hardware": [
                    {"name": "Machine 1", "cpu": "Intel i7", "ram": "16GB"},
                    {"name": "Machine 2", "cpu": "AMD Ryzen 5", "ram": "8GB"},
                    {"name": "Machine 3", "cpu": "Intel i5", "ram": "12GB"},
                ]
            },
        }
        mock_response.raise_for_status.return_value = None
        requests.get = MagicMock(return_value=mock_response)

        # Call the function under test
        result = get_all_cp_machines()

        # Assert that the result is the expected list of hardware configurations
        expected_result = [
            {"name": "Machine 1", "cpu": "Intel i7", "ram": "16GB"},
            {"name": "Machine 2", "cpu": "AMD Ryzen 5", "ram": "8GB"},
            {"name": "Machine 3", "cpu": "Intel i5", "ram": "12GB"},
        ]
        assert result == expected_result

    def test_function_raises_httperror_if_api_call_fails(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.HTTPError):
            with pytest.raises(SwanHTTPError):
                get_all_cp_machines()

    def test_failed_api_response(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            with pytest.raises(SwanRequestError):
                get_all_cp_machines()
