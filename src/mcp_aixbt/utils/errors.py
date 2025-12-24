"""Custom exceptions for MCP AIXBT Server."""


class AIXBTError(Exception):
    """Base exception for AIXBT API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class RateLimitError(AIXBTError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: int | None = None) -> None:
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class AuthenticationError(AIXBTError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid API key") -> None:
        super().__init__(message, status_code=401)


class NotFoundError(AIXBTError):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)


class BudgetExceededError(AIXBTError):
    """Raised when x402 budget limit is exceeded."""

    def __init__(self, message: str, limit_type: str = "unknown") -> None:
        super().__init__(message, status_code=402)
        self.limit_type = limit_type
