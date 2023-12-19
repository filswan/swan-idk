""" Token Related functionalities"""

import requests
from src.swan.constants.constants import SWAN_API, TOKEN_VALIDATION
from src.swan.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanConnectionError,
    SwanTimeoutError,
    SwanRequestError,
)
from src.swan.exceptions.task_exceptions import SwanTaskInvalidInputError


def validate_token(token):
    """
    Validate an API token by sending it to the server.

    This function sends a POST request to the APIs validation endpoint
    with the provided API token. It returns the server's response indicating
    whether the token is valid or invalid.

    Args:
        token (str): The API token to be validated.

    Returns:
        dict: A dictionary containing the server's response, including
              the status of the token ('Token Validated' or 'Token Invalid')
              and the response status code.

    Example:
        response = validate_api_token("your_api_token")
    """

    if not token:
        raise SwanTaskInvalidInputError("Please Provide TASK ID")

    # The endpoint for validating the API token
    endpoint = f"{SWAN_API}/{TOKEN_VALIDATION}"

    try:
        # Sending the POST request to the server with the API token
        response = requests.post(endpoint, data={"api_token": token})
        # Ensure the response was successful
        response.raise_for_status()

    except requests.exceptions.HTTPError as errh:
        # Raise a custom HTTPError
        raise SwanHTTPError(f"HTTP Error: {errh}") from errh

    except requests.exceptions.ConnectionError as errc:
        # Raise a custom ConnectionError
        raise SwanConnectionError(f"Connection Error: {errc}") from errc

    except requests.exceptions.Timeout as errt:
        # Raise a custom TimeoutError
        raise SwanTimeoutError(f"Timeout Error: {errt}") from errt

    except requests.exceptions.RequestException as err:
        # Raise a custom RequestError
        raise SwanRequestError(f"Request Exception: {err}") from err

    else:
        # Parsing the JSON response from the server
        response_data = response.json()
        response_data["status_code"] = response.status_code
        return response_data
