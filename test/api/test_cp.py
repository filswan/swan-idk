""" Tests for Computing Providers """

import pytest
import requests
from mock.mock import Mock, MagicMock, patch
from src.api.cp import get_all_cp_machines, get_collateral_balance
from src.exceptions.request_exceptions import SwanHTTPError, SwanRequestError, SwanConnectionError


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

    def test_retrieve_collateral_balance_valid_address(self):
        # Mock the requests.get method to return a mock response
        with patch("requests.get") as mock_get:
            # Set up the mock response
            mock_response = Mock()
            mock_response.json.return_value = {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }
            mock_get.return_value = mock_response

            # Call the function with a valid computing provider address
            result = get_collateral_balance("0x1234abcd")

            # Assert that the response is as expected
            assert result == {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }
    # NOTE: do not uncomment before ApiClient changes
    # def test_invalid_address_format(self):
    #     # Arrange
    #     cp_address = "invalid_address"
    #
    #     # Act and Assert
    #     with pytest.raises(SwanRequestError):
    #         get_collateral_balance(cp_address)

    def test_return_error_message(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            # Call the function under test
            with pytest.raises(SwanRequestError) as e:
                get_collateral_balance("0x1234abcd")
            # Assert that the exception message is correct
            assert (
                str(e.value)
                == "SwanRequestError: An unexpected error occurred while retrieving collateral balance"
            )

    def test_get_collateral_balance_request(self):
        # Mock the requests.get method to return a mock response
        with patch("requests.get") as mock_get:
            # Set up the mock response
            mock_response = Mock()
            mock_response.json.return_value = {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }
            mock_get.return_value = mock_response

            # Call the function you're testing
            result = get_collateral_balance("0x1234abcd")

            # Assert that requests.get was called with the correct endpoint
            mock_get.assert_called_once_with(
                "http://swanhub-cali.swanchain.io/cp/collateral/0x1234abcd"
            )

            # Assert that the result is the expected dictionary
            assert result == {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }
