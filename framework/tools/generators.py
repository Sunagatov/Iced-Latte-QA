import base64
import datetime
import random
import string
from random import choice
from typing import Optional, Any

import bcrypt
import jwt
from faker import Faker

from configs import DEFAULT_PASSWORD, JWT_SECRET

faker = Faker()


def generate_string(length: int, additional_characters: list = None) -> str:
    """Generating a string of the specified length with the possibility of adding special characters

    Args:
        length:                 length of the generated string;
        additional_characters:  addition of special characters.
    """
    result = [choice(string.ascii_lowercase) for _ in range(length)]
    if additional_characters:
        result += additional_characters

    return "".join(result)


def generate_user(
        first_name_length: Optional[int] = None,
        last_name_length: Optional[int] = None,
        password: str = DEFAULT_PASSWORD,
        with_address: bool = False,
        **kwargs
):
    """
    Generate a user with customizable attributes.

    Args:
        first_name_length: Optional[int] - Length of the first name.
        last_name_length: Optional[int] - Length of the last name.
        password: password for user.
        with_address: Include address information if True.
        **kwargs: Additional attributes to override.

    Returns:
        dict: Generated user data.
    """
    encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user_data = {
        "id": faker.uuid4(),
        "firstName": generate_string(first_name_length)
        if first_name_length is not None
        else faker.first_name(),
        "lastName": generate_string(last_name_length)
        if last_name_length is not None
        else faker.last_name(),
        "email": faker.email(),
        "birthDate": faker.date_of_birth().strftime("%Y-%m-%d"),
        "phoneNumber": faker.phone_number(),
        "stripeCustomerToken": faker.uuid4(),
        "password": password,
        "hashed_password": encrypted_password,
    }

    if with_address:
        user_data["address"] = {
            "country": faker.country(),
            "city": faker.city(),
            "line": faker.street_address(),
            "postcode": faker.postcode(),
        }

    user_data.update(kwargs)

    return user_data


def generate_jwt_token(email: str = "", expired: bool = False) -> str:
    """Generating a JWT token

    Args:
        email: user email
        expired: flag for expired token (True - expired, False - not expired)
    """

    payload = {"sub": email, "iat": datetime.datetime.now(datetime.timezone.utc)}
    if expired:
        payload["exp"] = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(seconds=1)
    else:
        payload["exp"] = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(days=1)

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
        password_length: int, first_name_length: int, last_name_length: int, email: Any = faker.email()
) -> dict:
    """Function for generation random user data

    Args:
        email: email to register
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
        "email": email,
    }


def generate_numeric_password(length: int) -> str:
    """ Generate a numeric password.

    Parameters:
    - length: int, the length of the password to generate.

    Returns:
    - A string representing the generated password.
    """

    return ''.join(
        str(random.randint(0, 9)) for _ in range(length)
    )


def append_random_to_local_part_email(domain: str = "", email_local_part: str = "", length_random_part: int = 5):
    """Generates a random email address based on the existing prefix and domain email.

    Args:
        length_random_part: Length of the random part of the email address.
        email_local_part: Prefix of the existing email address.
        domain: Domain of the existing email address.
    """
    random_part = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_random_part))
    return f"{email_local_part}{random_part}@{domain}"
