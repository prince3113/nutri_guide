import time
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

# In-memory store for rate limiting: user_id -> last_request_time
_last_request_times = {}

def throttle_request(seconds=2):
    """
    Decorator to throttle requests per user ID.
    Limits request frequency to at most one request every `seconds` seconds.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                user_id = get_jwt_identity()
                if user_id:
                    user_id = int(user_id)
                    current_time = time.time()
                    last_time = _last_request_times.get(user_id, 0)
                    if current_time - last_time < seconds:
                        wait_time = int(seconds - (current_time - last_time)) + 1
                        return jsonify({
                            "message": f"Too many requests. Please wait {wait_time} seconds before trying again."
                        }), 429
                    _last_request_times[user_id] = current_time
            except Exception:
                # If JWT is not present or parsing fails, allow the request to proceed without throttling
                pass
            return f(*args, **kwargs)
        return decorated_function
    return decorator
