from django.utils.crypto import get_random_string


def generate_order_number(length=12):
    return get_random_string(length=length, allowed_chars="1234567890")
