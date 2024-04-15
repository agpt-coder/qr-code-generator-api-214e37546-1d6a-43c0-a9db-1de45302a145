from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CustomizeQRCodeResponse(BaseModel):
    """
    The outcome of a QR code customization request, providing the resultant QR code image URL or path.
    """

    qr_code_url: str


async def customize_qr_code(
    qr_code_id: str, color: str, logo: Optional[str], size: int
) -> CustomizeQRCodeResponse:
    """
    Applies customization options to a generated QR code.

    Args:
    qr_code_id (str): Identifier of the QR code to customize.
    color (str): The desired color for the QR code. Accepts hexadecimal color codes.
    logo (Optional[str]): URL or path to the logo to integrate into the QR code. Optional.
    size (int): The size of the QR code in pixels, both width and height.

    Returns:
    CustomizeQRCodeResponse: The outcome of a QR code customization request, providing the resultant QR code image URL or path.
    """
    qr_code_request = await prisma.models.QRCodeRequest.prisma().find_unique(
        where={"id": qr_code_id}
    )
    if qr_code_request is None:
        raise ValueError("QRCodeRequest not found.")
    await prisma.models.QRCodeRequest.prisma().update(
        where={"id": qr_code_id}, data={"color": color, "size": size, "logo": logo}
    )
    customized_qr_code_url = (
        f"https://example.com/path/to/customized/qr_code_id_{qr_code_id}.png"
    )
    return CustomizeQRCodeResponse(qr_code_url=customized_qr_code_url)
