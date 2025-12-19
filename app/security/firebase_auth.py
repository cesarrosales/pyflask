import os
import firebase_admin
from firebase_admin import credentials, auth
from functools import wraps
from flask import request, jsonify

if not firebase_admin._apps:
    cred = credentials.Certificate(
        os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"]
    )
    firebase_admin.initialize_app(cred)

def require_firebase_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({"error": "Missing Bearer token"}), 401

        token = header.split(" ", 1)[1].strip()

        try:
            decoded = auth.verify_id_token(token)
        except Exception:
            return jsonify({"error": "Invalid Firebase token"}), 401

        # Attach user info if needed later
        request.user = decoded  # uid, email, etc.

        return fn(*args, **kwargs)
    return wrapper