from django.utils.crypto import get_random_string


def generate_username(length: int = 20) -> str:
    return get_random_string(length=length, allowed_chars="abcdefghijklmnopqrstuvwxyz")
