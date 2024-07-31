import pytest
from core.libs.exceptions import FyleError


def test_fyle_error_initialization():
    # Create an instance of FyleError with a custom status code and message
    error = FyleError(status_code=404, message="Resource not found")

    # Check if the status code and message are correctly set
    assert error.status_code == 404
    assert error.message == "Resource not found"


def test_fyle_error_default_status_code():
    # Create an instance of FyleError with a default status code and a custom message
    error = FyleError(status_code=400, message="Bad request")

    # Check if the default status code is correctly set
    assert error.status_code == 400
    assert error.message == "Bad request"


def test_fyle_error_to_dict():
    # Create an instance of FyleError with a custom status code and message
    error = FyleError(status_code=500, message="Internal server error")

    # Convert the error to a dictionary
    error_dict = error.to_dict()

    # Check if the dictionary representation is correct
    assert error_dict == {"message": "Internal server error"}
