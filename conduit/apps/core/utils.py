import random
import string

DEFAULT_CHAR_STRING = string.ascii_lowercase + string.digits


def generate_random_string(chars=DEFAULT_CHAR_STRING, size=6):
    return ''.join(random.choice(chars) for _ in chars)

def calcChecksum(content):
    sum = 0
    for character in content:
        value = ord(character)
        sum += value
    return str(sum).zfill(4)