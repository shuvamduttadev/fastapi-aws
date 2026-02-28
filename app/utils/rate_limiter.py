"""Rate limiting configuration and utilities"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT_DEFAULT]
)


class RateLimitExceeded(Exception):
    """Rate limit exceeded exception"""
    pass
