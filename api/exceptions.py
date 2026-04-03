from fastapi import HTTPException, status

INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentions",
    headers={"WWW-Authenticate": "Bearer"},
)
