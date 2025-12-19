import os
import firebase_admin
from firebase_admin import credentials, auth

if not firebase_admin._apps:
    cred = credentials.Certificate(
        os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"]
    )
    firebase_admin.initialize_app(cred)

def verify_firebase_token(token: str) -> dict:
    return auth.verify_id_token(token)