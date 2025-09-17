import hashlib


def create_secret_token(bot_token: str, secret: str) -> str:
    return hashlib.sha256((bot_token + secret).encode()).hexdigest()

