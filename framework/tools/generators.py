from random import choice
from string import ascii_lowercase


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
