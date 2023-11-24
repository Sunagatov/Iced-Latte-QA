from random import choice
from string import ascii_lowercase
from faker import Faker
import bcrypt
import base64
import jwt
import datetime

from configs import DEFAULT_PASSWORD, JWT_SECRET


def generate_string(length: int, additional_characters: list = None) -> str:
    """Generating a string of the specified length with the possibility of adding special characters

    Args:
        length:                 length of the generated string;
        additional_characters:  addition of special characters.
    """
    result = [choice(ascii_lowercase) for _ in range(length)]
    if additional_characters:
        result += additional_characters

    return "".join(result)


def generate_user(password: str = DEFAULT_PASSWORD) -> dict:
    """Generating a user with the specified password

    Args:
        password: password for user
    """

    faker = Faker()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return {
        "id": faker.uuid4(),
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "password": password,
        "hashed_password": hashed_password,
    }


def generate_jwt_token(email: str = '', expired: bool = False) -> str:
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
