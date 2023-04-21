from slowapi import Limiter
from slowapi.util import get_remote_address


def create_rate_limiter():
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["5/minute"]
    )
    return limiter
