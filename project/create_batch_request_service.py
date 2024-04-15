from enum import Enum
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class DataType(Enum):
    """
    An enumeration type that specifies the different types of data that can be encoded into a QR code.
    """

    URL: str
    TEXT: str
    VCARD: str
    JSON: str
    CSV: str


class ErrorCorrection(Enum):
    """
    Enumeration type that specifies the allowable error correction levels for QR codes.
    """

    LOW: str
    MEDIUM: str
    QUARTILE: str
    HIGH: str


class QRCodeRequestInput(BaseModel):
    """
    Details of a single QR code request within the batch.
    """

    data: str
    dataType: DataType
    size: int
    color: str
    logo: Optional[str] = None
    errorCorrection: ErrorCorrection


class CreateBatchResponse(BaseModel):
    """
    Response model for a submitted batch QR code request. Provides an identifier for the batch request and a message indicating the request has been queued.
    """

    batchRequestId: str
    message: str


async def create_batch_request(
    userId: str, qrCodeRequests: List[QRCodeRequestInput]
) -> CreateBatchResponse:
    """
    Submits a batch request for QR code generation and/or customization.

    Args:
    userId (str): Identifier of the user submitting the batch request.
    qrCodeRequests (List[QRCodeRequestInput]): List of QR code generation or customization requests.

    Returns:
    CreateBatchResponse: Response model for a submitted batch QR code request. Provides an identifier for the batch request and a message indicating the request has been queued.
    """
    batch_request = await prisma.models.BatchRequest.prisma().create(
        data={"userId": userId, "status": "QUEUED"}
    )
    for qr_request in qrCodeRequests:
        await prisma.models.QRCodeRequest.prisma().create(
            data={
                "userId": userId,
                "data": qr_request.data,
                "dataType": qr_request.dataType,
                "size": qr_request.size,
                "color": qr_request.color,
                "logo": qr_request.logo,
                "errorCorrection": qr_request.errorCorrection,
                "format": "PNG",
                "batchRequestId": batch_request.id,
            }
        )
    return CreateBatchResponse(
        batchRequestId=batch_request.id,
        message="Batch request is queued and being processed.",
    )
