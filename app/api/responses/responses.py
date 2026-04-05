"""
This module defines standardized response classes for the API.
"""


class Response(dict):
    """
    Base class for API responses.
    Inherits from dict to allow dictionary-like access to response properties.
    """

    success: bool = False
    """Indicates if the operation was successful."""
    status_code: int
    """The HTTP status code for the response."""
    data: object | None
    """The actual data payload of the response."""
    message: str
    """A human-readable message describing the response."""

    def __init__(
        self, success: bool, status_code: int = 0, message="", data=None
    ) -> None:
        """
        Initializes a new Response object.

        Args:
            success (bool): True if the operation succeeded, False otherwise.
            status_code (int): The HTTP status code.
            message (str): A descriptive message for the response.
            data (object | None): The data payload.
        """
        self.success = success
        self.status_code = status_code
        self.message = message
        self.data = data


class SuccessResponse(Response):
    """
    A specific response class for successful API operations.
    Defaults success to True and status_code to 200.
    """

    def __init__(self, status_code=200, message="", data=None) -> None:
        """
        Initializes a new SuccessResponse object.

        Args:
            status_code (int): The HTTP status code (defaults to 200).
            message (str): A descriptive message for the response.
            data (object | None): The data payload.
        """
        super().__init__(
            success=True, status_code=status_code, message=message, data=data
        )


class ErrorResponse(Response):
    """
    A specific response class for unsuccessful (error) API operations.
    Defaults success to False and status_code to 400.
    """

    def __init__(self, status_code=400, message="", data=None) -> None:
        """
        Initializes a new ErrorResponse object.

        Args:
            status_code (int): The HTTP status code (defaults to 400).
            message (str): A descriptive error message.
            data (object | None): Optional error details or data.
        """
        super().__init__(
            success=False, status_code=status_code, message=message, data=data
        )
