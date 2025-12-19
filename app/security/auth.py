from functools import wraps
from flask import request, jsonify

from app.security.auth0_auth import verify_auth0_token

def _bearer():
    h = request.headers.get("Authorization", "")
    if not h.startswith("Bearer "):
        return None
    return h.split(" ", 1)[1].strip()

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _bearer()
        if not token:
            return jsonify({"error": "Missing Bearer token"}), 401

        try:
            decoded = verify_auth0_token(token)
            request.user = {"provider": "auth0", "sub": decoded.get("sub"), "claims": decoded}
            return fn(*args, **kwargs)
        except Exception:
            return jsonify({"error": "Unauthorized"}), 401

    return wrapper