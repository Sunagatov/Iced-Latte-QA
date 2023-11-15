import random
import string
from faker import Faker

fake = Faker()


def generate_password(length: int) -> str:
    """
     Function generates and returns random generated password.
     Args:
         length (int): length of password
    """
    letters = string.ascii_letters
    digits = string.digits
    special_chars = "!@%*$&"
    all_chars = digits + special_chars + letters
    password = ''.join(random.choice(all_chars) for _ in range(length))

    """Digits and letters is required char in password. This statement add 1 digits and letter to the password" \
       if it absent during generation random password """
    if all(char not in digits for char in password):
        random_index = random.randint(0, length - 1)
        password = password[:random_index] + random.choice(digits) + password[random_index:]
    if all(char not in letters for char in password):
        random_index = random.randint(0, length - 1)
        password = password[:random_index] + random.choice(letters) + password[random_index:]

    return password


def generate_user_data(password_len: int = None, length_first_name: int = None, length_last_name: int = None) -> dict:
    """
    Function for generation random user data
    Args:
        password_len: length generated password
        length_first_name: length generated string
        length_last_name:  length generated string
    """
    first_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(length_first_name))
    last_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(length_last_name))
    return {
        "firstName": first_name,
        "lastName": last_name,
        "password": generate_password(password_len),
        "email": fake.email(),
    }


