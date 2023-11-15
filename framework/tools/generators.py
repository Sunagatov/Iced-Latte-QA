from random import choice
from string import ascii_lowercase
from faker import Faker
import bcrypt

from configs import DEFAULT_PASSWORD


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


def generate_user(password=DEFAULT_PASSWORD):
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
