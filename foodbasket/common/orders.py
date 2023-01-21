from django.utils.crypto import get_random_string


def generate_order_number(length: int = 12) -> str:
    return get_random_string(length=length, allowed_chars="1234567890")
