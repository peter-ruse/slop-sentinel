from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from core.config import jwt_settings

ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def password_correct(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=30)})
    encoded_jwt = jwt.encode(
        to_encode, key=jwt_settings.raw_secret_key, algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str):
    return jwt.decode(token, jwt_settings.raw_secret_key, algorithms=[ALGORITHM])
