from random import choice
from string import ascii_lowercase
import bcrypt
import base64
import jwt
import datetime

from configs import DEFAULT_PASSWORD, JWT_SECRET
import random
import string
from faker import Faker

faker = Faker()


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

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return {
        "id": faker.uuid4(),
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "password": password,
        "hashed_password": hashed_password,
    }


def generate_jwt_token(email: str = "", expired: bool = False) -> str:
    """Generating a JWT token

    Args:
        email: user email
        expired: flag for expired token (True - expired, False - not expired)
    """

    payload = {
        "sub": email,
        "iat": datetime.datetime.utcnow(),
    }
    if expired:
        payload["exp"] = datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
    else:
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    encoded_secret_key = JWT_SECRET
    secret_key = base64.b64decode(encoded_secret_key)
    token = jwt.encode(payload, secret_key, algorithm="HS256", headers={"alg": "HS256"})

    return token


def generate_password(length: int) -> str:
    """Function generates and returns random generated password.

    Args:
         length: length of password
    """
    letters = string.ascii_letters
    digits = string.digits
    special_chars = "!@%*$&"
    all_chars = digits + special_chars + letters
    password = "".join(random.choice(all_chars) for _ in range(length))

    """Digits and letters is required char in password. This statement add 1 digits and letter to the password" \
       if it absent during generation random password """
    if all(char not in digits for char in password):
        random_index = random.randint(0, length - 1)
        password = (
            password[:random_index] + random.choice(digits) + password[random_index:]
        )
    if all(char not in letters for char in password):
        random_index = random.randint(0, length - 1)
        password = (
            password[:random_index] + random.choice(letters) + password[random_index:]
        )

    return password


def generate_user_data(
    password_length: int, first_name_length: int, last_name_length: int
) -> dict:
    """Function for generation random user data

    Args:
        password_length: length generated password
        first_name_length: length generated string
        last_name_length:  length generated string
    """
    first_name = "".join(
        random.choice(string.ascii_lowercase) for _ in range(first_name_length)
    )
    last_name = "".join(
        random.choice(string.ascii_lowercase) for _ in range(last_name_length)
    )
    return {
        "firstName": first_name,
        "lastName": last_name,
        "password": generate_password(password_length),
        "email": faker.email(),
    }
