from dataclasses import dataclass
from typing import Optional


@dataclass
class Error:
    """Base error class for all Bitcoin MCP errors."""

    message: str
    details: Optional[str] = None

    def __str__(self) -> str:
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


@dataclass
class NetworkError(Error):
    """Error occurred during network communication."""

    def __init__(
        self, message: str = "Network error occurred", details: Optional[str] = None
    ):
        super().__init__(message=message, details=details)


@dataclass
class HTTPError(Error):
    """HTTP request failed with error status code."""

    status_code: Optional[int] = None

    def __init__(
        self,
        message: str = "HTTP request failed",
        status_code: Optional[int] = None,
        details: Optional[str] = None,
    ):
        super().__init__(message=message, details=details)
        self.status_code = status_code

    def __str__(self) -> str:
        if self.status_code:
            base = f"{self.message} (Status: {self.status_code})"
        else:
            base = self.message

        if self.details:
            return f"{base}: {self.details}"
        return base


@dataclass
class TimeoutError(Error):
    """Request timed out."""

    def __init__(
        self, message: str = "Request timed out", details: Optional[str] = None
    ):
        super().__init__(message=message, details=details)


@dataclass
class DataValidationError(Error):
    """Data validation or parsing failed."""

    def __init__(
        self, message: str = "Data validation failed", details: Optional[str] = None
    ):
        super().__init__(message=message, details=details)


@dataclass
class NotFoundError(Error):
    """Requested resource not found."""

    def __init__(
        self, message: str = "Resource not found", details: Optional[str] = None
    ):
        super().__init__(message=message, details=details)


@dataclass
class RateLimitError(Error):
    """API rate limit exceeded."""

    retry_after: Optional[int] = None

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        details: Optional[str] = None,
    ):
        super().__init__(message=message, details=details)
        self.retry_after = retry_after

    def __str__(self) -> str:
        if self.retry_after:
            base = f"{self.message} (Retry after: {self.retry_after}s)"
        else:
            base = self.message

        if self.details:
            return f"{base}: {self.details}"
        return base


@dataclass
class CacheError(Error):
    """Error occurred while accessing cache."""

    def __init__(
        self, message: str = "Cache error occurred", details: Optional[str] = None
    ):
        super().__init__(message=message, details=details)


@dataclass
class ConfigurationError(Error):
    """Configuration is invalid or missing."""

    def __init__(
        self, message: str = "Configuration error", details: Optional[str] = None
    ):
        super().__init__(message=message, details=details)


@dataclass
class ProcessingError(Error):
    """Error occurred during data processing."""

    def __init__(
        self, message: str = "Processing error occurred", details: Optional[str] = None
    ):
        super().__init__(message=message, details=details)
