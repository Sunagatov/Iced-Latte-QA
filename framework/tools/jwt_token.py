import base64
import jwt
import datetime

from configs import JWT_SECRET


def generate_jwt_token(email='', expired=False):
    # Payload for the token
    if not expired:
        payload = {
            "sub": email,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
    else:
        payload = {
            "sub": email,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
        }

    # Secret key (base64 encoded)
    encoded_secret_key = JWT_SECRET
    # Decoding the secret key from base64
    secret_key = base64.b64decode(encoded_secret_key)

    # Generating the token
    token = jwt.encode(payload, secret_key, algorithm="HS256", headers={"alg": "HS256"})
    return token
