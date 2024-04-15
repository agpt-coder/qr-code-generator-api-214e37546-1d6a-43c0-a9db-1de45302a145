from typing import Any, Dict

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserPreferencesResponse(BaseModel):
    """
    Describes the structure of the response after updating user preferences for QR code generation and customization.
    """

    success: bool
    updated_preferences: Dict[str, Any]
    message: str


async def update_user_preferences(
    color: str,
    size: int,
    error_correction_level: str,
    margin: int,
    logo_integration: bool,
    user_id: str,
) -> UpdateUserPreferencesResponse:
    """
    Updates the user's preferences related to QR code generation and customization.

    Args:
        color (str): Preferred color for QR codes. This is a hex color code.
        size (int): Preferred QR code size in pixels.
        error_correction_level (str): The preferred error correction level for QR codes: ['L', 'M', 'Q', 'H'].
        margin (int): Preferred margin for the QR code in pixels.
        logo_integration (bool): Boolean indicating if the user prefers a logo integrated in the QR code.
        user_id (str): The unique identifier of the user for whom preferences are being updated.

    Returns:
        UpdateUserPreferencesResponse: Describes the structure of the response after updating user preferences for QR code generation and customization.

    This function queries the UserPreference model to update the user's preferences if they exist or creates new preferences if they don't. It then returns a response object indicating the success of the operation.
    """
    preferences = {
        "color": color,
        "size": str(size),
        "error_correction_level": error_correction_level,
        "margin": str(margin),
        "logo_integration": str(logo_integration),
    }
    try:
        for key, value in preferences.items():
            preference_exists = await prisma.models.UserPreference.prisma().find_first(
                where={"AND": [{"userId": user_id}, {"preferenceKey": key}]}
            )
            if preference_exists:
                await prisma.models.UserPreference.prisma().update(
                    where={"id": preference_exists.id}, data={"preferenceValue": value}
                )
            else:
                await prisma.models.UserPreference.prisma().create(
                    data={
                        "userId": user_id,
                        "preferenceKey": key,
                        "preferenceValue": value,
                    }
                )
        return UpdateUserPreferencesResponse(
            success=True,
            updated_preferences=preferences,
            message="User preferences updated successfully.",
        )
    except Exception as e:
        return UpdateUserPreferencesResponse(
            success=False,
            updated_preferences={},
            message=f"Failed to update user preferences: {str(e)}",
        )
