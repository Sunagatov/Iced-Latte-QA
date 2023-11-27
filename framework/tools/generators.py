from random import choice
from string import ascii_lowercase
import random
import string
from faker import Faker

fake = Faker()


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
        "email": fake.email(),
    }
