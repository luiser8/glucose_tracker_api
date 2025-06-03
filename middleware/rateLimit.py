from flask import jsonify, request
from datetime import datetime, timedelta
import functools
import os
from collections import defaultdict

request_counts = defaultdict(lambda: defaultdict(list))

def rate_limit():
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.remote_addr
            endpoint = request.endpoint
            now = datetime.now()
            limit = int(os.getenv("LIMIT"))
            per = timedelta(minutes=(int(os.getenv("PER"))))

            request_counts[endpoint][ip] = [t for t in request_counts[endpoint][ip] if now - t < per]

            if len(request_counts[endpoint][ip]) >= limit:
                return jsonify({
                    "error": "Too many requests",
                    "message": f"Rate limit exceeded: {limit} requests per {per}",
                    "status": 429
                }), 429

            request_counts[endpoint][ip].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator
