from functools import wraps
from flask import request, jsonify, g
import jwt
import os
from datetime import datetime
from dateutil.parser import parse
from services.usersAuth import usersAuthSrv
from middleware.responseHttpUtils import responseHttpUtils

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        users_auth_service = usersAuthSrv()

        if "Authorization" not in request.headers:
            return jsonify(responseHttpUtils().response("Authorization token is missing", 401, None)), 401

        auth_header = request.headers["Authorization"]
        if not auth_header.startswith('Bearer '):
            return jsonify(responseHttpUtils().response("Invalid authorization format", 401, None)), 401

        token = auth_header.split()[1]
        if not token:
            return jsonify(responseHttpUtils().response("Empty token", 401, None)), 401

        try:
            secret_key = os.getenv("SECRET_KEY")
            if not secret_key:
                raise ValueError("SECRET_KEY not configured")

            data = jwt.decode(
                jwt=token,
                key=secret_key,
                algorithms=[os.getenv("ALGORITHM", "HS256")]
            )

            user_auth = users_auth_service.getByIdSrv(data["id"])
            if not user_auth or not user_auth[0]:
                return jsonify(responseHttpUtils().response("User not found", 401, None)), 401

            token_iat = datetime.fromtimestamp(data["exp"])
            updated_at = user_auth[0]["updatedat"]

            if updated_at:
                if isinstance(updated_at, str):
                    try:
                        updated_at_dt = parse(updated_at)
                    except ValueError as e:
                        try:
                            updated_at = updated_at.split('.')[0]
                            updated_at_dt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S")
                        except ValueError:
                            updated_at_dt = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
                else:
                    updated_at_dt = updated_at

                if token_iat < updated_at_dt:
                    return jsonify(responseHttpUtils().response(
                        "Token has been invalidated by a newer token",
                        401,
                        None
                    )), 401

            g.user = data
            g.current_token = token

        except jwt.ExpiredSignatureError:
            return jsonify(responseHttpUtils().response("Token expired", 401, None)), 401
        except jwt.InvalidTokenError:
            return jsonify(responseHttpUtils().response("Invalid token", 401, None)), 401
        except Exception as e:
            return jsonify(responseHttpUtils().response(
                f"Authorization error: {str(e)}",
                401,
                None
            )), 401

        return f(*args, **kwargs)

    return decorated_function
