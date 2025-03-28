from re import S
from fastapi import Depends, Security, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from app.exception import CustomException

SECRET_KEY = "8F573CF5A19BCAE3F9D999B7DE4BA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if not exp:
            raise CustomException(status_code=401, message="Token expired")
        if exp and datetime.now(timezone.utc).timestamp > exp:
            raise CustomException(status_code=401, message="Token expired")
        return payload
    except jwt.ExpiredSignatureError:
        raise CustomException(status_code=401, message="Token expired")
    except jwt.InvalidTokenError:
        raise CustomException(status_code=401, message="Invalid token")
