from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CheckPermissionResponse(BaseModel):
    """
    Response model indicating whether the user is authorized to perform the specified action. Includes a boolean flag and an optional message in case of unauthorized access.
    """

    is_authorized: bool
    message: Optional[str] = None


async def check_permission(token: str, action: str) -> CheckPermissionResponse:
    """
    Checks if the currently authenticated user has permission to perform a specific action or access certain data.

    This function fetches the user associated with the provided token from the APIKeys table. It checks the user's role and determines if they are authorized to perform the requested action. Restrictions are applied based on predetermined rules for different user roles. An administrator can perform any action, while a general user has restricted access.

    Args:
    token (str): The authentication token of the user. This token is used to identify and authenticate the user.
    action (str): The specific action the user is attempting to perform. This will be used to check against the user's permissions.

    Returns:
    CheckPermissionResponse: Response model indicating whether the user is authorized to perform the specified action. Includes a boolean flag and an optional message in case of unauthorized access.

    Example:
        token = 'your_api_key_token'
        action = 'create_qr_code'
        response = await check_permission(token, action)
        if response.is_authorized:
            print('Authorized to perform the action')
        else:
            print(f'Unauthorized: {response.message}')
    """
    api_key = await prisma.models.APIKey.prisma().find_unique(where={"key": token})
    if api_key is None:
        return CheckPermissionResponse(
            is_authorized=False, message="Invalid API Token."
        )
    user = await prisma.models.User.prisma().find_unique(where={"id": api_key.userId})
    if user is None:
        return CheckPermissionResponse(is_authorized=False, message="User not found.")
    if action == "create_qr_code":
        if user.role in [
            prisma.enums.Role.PREMIUMUSER,
            prisma.enums.Role.ADMINISTRATOR,
        ]:
            return CheckPermissionResponse(is_authorized=True)
        else:
            return CheckPermissionResponse(
                is_authorized=False,
                message="User does not have the required permissions to perform this action.",
            )
    return CheckPermissionResponse(
        is_authorized=False, message="Unknown or unauthorized action."
    )
