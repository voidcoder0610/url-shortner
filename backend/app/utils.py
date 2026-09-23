# 62 unique characters: 10 numbers + 26 lowercase + 26 uppercase
BASE62_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num: int) -> str:
    """Takes a positive integer database ID and returns its Base62 string."""
    if num == 0:
        return BASE62_CHARS[0]

    encoded = []
    while num > 0:
        remainder = num % 62
        encoded.append(BASE62_CHARS[remainder])
        num = num // 62

    # Reverse because we collected remainders from least-significant to most-significant
    return "".join(reversed(encoded))


def decode_base62(code: str) -> int:
    """Takes a Base62 short string and converts it back to the integer ID."""
    num = 0
    for char in code:
        num = num * 62 + BASE62_CHARS.index(char)
    return num