class APIException(Exception):
    """Base exception for API errors."""


class APIConnectionError(APIException):
    """Raised when a connection to the API fails."""


class APINotFoundError(APIException):
    """Raised when the requested resource is not found (404)."""


class APIUnauthorizedError(APIException):
    """Raised when the API key is invalid or missing (401)."""


class APIRateLimitError(APIException):
    """Raised when the API rate limit is exceeded (429)."""


class APIServerError(APIException):
    """Raised when the API returns a server error (5xx)."""
