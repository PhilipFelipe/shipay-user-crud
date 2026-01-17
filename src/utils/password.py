import secrets
import string

import bcrypt


class PasswordHandler:
    @staticmethod
    def hash(password: str) -> str:
        bytes_password = password.encode('utf-8')
        hashed_bytes = bcrypt.hashpw(bytes_password, bcrypt.gensalt(12))
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password, hashed)

    @staticmethod
    def gen_random_password(length: int = 12) -> str:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))
