import prisma
import prisma.models
from pydantic import BaseModel


class LogoutResponseModel(BaseModel):
    """
    Provides confirmation on the successful invalidation of the user's session token.
    """

    message: str


async def logout(token: str) -> LogoutResponseModel:
    """
    Logs out a user, invalidating their current session.

    This function requires an authentication token as its input. It checks if the token exists
    in the database and, if found, invalidates it to log out the user effectively.
    The function returns a LogoutResponseModel object, indicating the operation's success.

    Args:
    token (str): The authentication token provided by the user at the time of login, which is to be invalidated upon logout.

    Returns:
    LogoutResponseModel: Provides confirmation on the successful invalidation of the user's session token.

    Example:
    logout_response = await logout('some_valid_token_string')
    > LogoutResponseModel(message='Successfully logged out.')
    """
    existing_token = await prisma.models.APIKey.prisma().find_unique(
        where={"key": token}
    )
    if not existing_token:
        return LogoutResponseModel(message="Invalid token.")
    await prisma.models.APIKey.prisma().delete(where={"id": existing_token.id})
    return LogoutResponseModel(message="Successfully logged out.")
