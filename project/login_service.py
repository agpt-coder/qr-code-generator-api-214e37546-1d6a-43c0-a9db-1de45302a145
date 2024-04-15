import bcrypt
import prisma
import prisma.models
from fastapi import HTTPException
from jose import jwt
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    Contains the access token granted upon successful authentication. This token is to be used for subsequent requests requiring authentication.
    """

    access_token: str
    token_type: str


async def login(email: str, password: str) -> LoginResponse:
    """
    Authenticates a user and returns an access token.

    Args:
        email (str): The user's email address used for login.
        password (str): The user's password in plaintext, which will be hashed server-side for verification.

    Returns:
        LoginResponse: Contains the access token granted upon successful authentication. This token is to be used for subsequent requests requiring authentication.

    Raises:
        HTTPException: With status code 404 if the user is not found.
        HTTPException: With status code 401 if the password does not match.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    password_match = bcrypt.checkpw(
        password.encode("utf8"), user.hashedPassword.encode("utf8")
    )
    if not password_match:
        raise HTTPException(status_code=401, detail="Incorrect password")
    secret_key = "SECRET_KEY"
    algorithm = "HS256"
    data = {"sub": user.id}
    access_token = jwt.encode(data, secret_key, algorithm=algorithm)
    return LoginResponse(access_token=access_token, token_type="bearer")
