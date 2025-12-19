from functools import wraps
from flask import request, jsonify

def require_permission(perm: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            if not isinstance(user, dict):
                return jsonify({"error": "Unauthorized"}), 401

            claims = user.get("claims", {}) or {}

            perms = set(claims.get("permissions") or [])
            scopes = set((claims.get("scope") or "").split())

            if perm not in perms and perm not in scopes:
                return jsonify({"error": "Required permission not present"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator