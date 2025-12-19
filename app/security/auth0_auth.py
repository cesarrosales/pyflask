import os
import jwt
from jwt import PyJWKClient

def verify_auth0_token(token: str) -> dict:
    domain = os.environ["AUTH0_DOMAIN"]
    audience = os.environ["AUTH0_AUDIENCE"]
    issuer = f"https://{domain}/"

    jwks_url = f"https://{domain}/.well-known/jwks.json"
    jwks_client = PyJWKClient(jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(token).key

    return jwt.decode(
        token,
        signing_key,
        algorithms=["RS256"],
        audience=audience,
        issuer=issuer,
    )