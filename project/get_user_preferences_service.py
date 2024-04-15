from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class UserPreferenceDetail(BaseModel):
    """
    Key value pair detailing the user's stored preferences.
    """

    preference_key: str
    preference_value: str


class GetUserPreferencesResponse(BaseModel):
    """
    A detailed layout of the user's stored preferences for QR code generation and customization, encapsulating various preference parameters.
    """

    preferences: List[UserPreferenceDetail]


async def get_user_preferences() -> GetUserPreferencesResponse:
    """
    Retrieves the user's stored preferences for QR code generation and customization.

    This function interacts with the database to fetch the user's stored QR code generation and customization preferences.
    It compiles these preferences into a structured format suitable for further processing or presentation.

    Returns:
        GetUserPreferencesResponse: A detailed layout of the user's stored preferences for QR code generation and customization, encapsulating various preference parameters.

    Example:
        get_user_preferences()
        > GetUserPreferencesResponse(preferences=[UserPreferenceDetail(preference_key='color', preference_value='#000000')])
    """
    user_preferences = await prisma.models.UserPreference.prisma().find_many()
    preferences_details = [
        UserPreferenceDetail(
            preference_key=preference.preferenceKey,
            preference_value=preference.preferenceValue,
        )
        for preference in user_preferences
    ]
    return GetUserPreferencesResponse(preferences=preferences_details)
