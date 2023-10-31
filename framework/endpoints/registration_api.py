import requests
from faker import Faker
import random

fake = Faker()


# Function for generating password
def generate_password():
    length = random.randint(6, 50)  # This will generate a random number between 6 and 60 (both inclusive).
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    special_chars = "!@#№$%&*/"
    all_chars = letters + digits + special_chars
    password = ''.join(random.choice(all_chars) for _ in range(length))

    # If the generated password doesn't contain a special character, insert one at a random position.
    if not any(char in special_chars for char in password):
        random_index = random.randint(0, length - 1)
        password = password[:random_index] + random.choice(special_chars) + password[random_index:]
    if not any(char in digits for char in password):
        random_index = random.randint(0, length - 1)
        password = password[:random_index] + random.choice(digits) + password[random_index:]
    if not any(char in letters for char in password):
        random_index = random.randint(0, length - 1)
        password = password[:random_index] + random.choice(letters) + password[random_index:]

    return password


#  Function to create random user data for HTTP request
def generate_user_data():
    return {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "password": generate_password(),
        "email": fake.email()
    }


