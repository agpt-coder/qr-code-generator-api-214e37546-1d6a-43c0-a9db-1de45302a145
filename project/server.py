import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import project.api_documentation_service
import project.check_permission_service
import project.create_batch_request_service
import project.customize_qr_code_service
import project.generate_qr_code_service
import project.get_system_logs_service
import project.get_user_preferences_service
import project.login_service
import project.logout_service
import project.security_status_service
import project.update_user_preferences_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="QR Code Generator API 2",
    lifespan=lifespan,
    description="The project focuses on developing an endpoint that primarily receives various types of data, including URLs, text, and contact information, to generate QR codes. Key features of the endpoint include: \n\n1. **Data Handling:** The endpoint is adept at processing different data formats, with a particular emphasis on text inputs, which are the primary type of data it will handle. This capability ensures versatility in the QR codes' applications, enabling users to encode a wide range of information.\n\n2. **Customization:** Users have specific customization requirements for the QR codes, emphasizing the need for distinctive branding elements. The desired customizations include the ability to alter the QR code's color to match the brand identity and the incorporation of a logo within the QR code. This customization extends to modifying the QR code's size to ensure it remains easily scannable from standard distances.\n\n3. **Output Formats:** The preferred format for the generated QR codes is PNG. This choice reflects a balance between wide compatibility across platforms and the quality of the image suitable for various display sizes.\n\n4. **Technical Approach:** The project will leverage Python as the programming language of choice, given its rich ecosystem for image processing and web development. For generating and customizing QR codes, exploration in the `qrcode` library has provided a solid foundation, highlighting capabilities such as basic QR code generation, color customization, and integration of logos. Further customization options have been identified, including altering shapes and patterns within the QR code for aesthetic and functional purposes.\n\n5. **API and Database Design:** FastAPI is selected as the API framework for its performance and ease of use in creating web applications with Python. PostgreSQL will serve as the database solution, ensuring robust data management capabilities for storing information related to the QR codes, such as creation parameters and user data. The ORM of choice will be Prisma, which offers a powerful and easy-to-use interface for connecting the application's Python code with the PostgreSQL database.\n\nThis project summary encapsulates the task requirements and the chosen tech stack for the development of a feature-rich, customizable QR code generation endpoint.",
)


@app.post(
    "/generate", response_model=project.generate_qr_code_service.GenerateQRCodeResponse
)
async def api_post_generate_qr_code(
    data: str,
    data_type: project.generate_qr_code_service.DataType,
    size: int,
    color: str,
    error_correction: project.generate_qr_code_service.ErrorCorrection,
) -> project.generate_qr_code_service.GenerateQRCodeResponse | Response:
    """
    Receives data in supported formats and generates a QR code.
    """
    try:
        res = project.generate_qr_code_service.generate_qr_code(
            data, data_type, size, color, error_correction
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/docs",
    response_model=project.api_documentation_service.APIDocumentationResponse,
)
async def api_get_api_documentation() -> project.api_documentation_service.APIDocumentationResponse | Response:
    """
    Provides documentation for the available API endpoints and their usage.
    """
    try:
        res = project.api_documentation_service.api_documentation()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/security/status",
    response_model=project.security_status_service.SecurityStatusResponse,
)
async def api_get_security_status() -> project.security_status_service.SecurityStatusResponse | Response:
    """
    Provides an overview of the system's current security status and any detected issues.
    """
    try:
        res = await project.security_status_service.security_status()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/logout", response_model=project.logout_service.LogoutResponseModel)
async def api_post_logout(
    token: str,
) -> project.logout_service.LogoutResponseModel | Response:
    """
    Logs out a user, invalidating their current session.
    """
    try:
        res = await project.logout_service.logout(token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/auth/permission/check",
    response_model=project.check_permission_service.CheckPermissionResponse,
)
async def api_get_check_permission(
    token: str, action: str
) -> project.check_permission_service.CheckPermissionResponse | Response:
    """
    Checks if the currently authenticated user has permission to perform a specific action or access certain data.
    """
    try:
        res = await project.check_permission_service.check_permission(token, action)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/preferences",
    response_model=project.get_user_preferences_service.GetUserPreferencesResponse,
)
async def api_get_get_user_preferences() -> project.get_user_preferences_service.GetUserPreferencesResponse | Response:
    """
    Retrieves the user's stored preferences for QR code generation and customization.
    """
    try:
        res = await project.get_user_preferences_service.get_user_preferences()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/batch/create",
    response_model=project.create_batch_request_service.CreateBatchResponse,
)
async def api_post_create_batch_request(
    userId: str,
    qrCodeRequests: List[project.create_batch_request_service.QRCodeRequestInput],
) -> project.create_batch_request_service.CreateBatchResponse | Response:
    """
    Submits a batch request for QR code generation and/or customization.
    """
    try:
        res = await project.create_batch_request_service.create_batch_request(
            userId, qrCodeRequests
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/preferences/update",
    response_model=project.update_user_preferences_service.UpdateUserPreferencesResponse,
)
async def api_put_update_user_preferences(
    color: str,
    size: int,
    error_correction_level: str,
    margin: int,
    logo_integration: bool,
    user_id: str,
) -> project.update_user_preferences_service.UpdateUserPreferencesResponse | Response:
    """
    Updates the user's preferences related to QR code generation and customization.
    """
    try:
        res = await project.update_user_preferences_service.update_user_preferences(
            color, size, error_correction_level, margin, logo_integration, user_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/logs/system", response_model=project.get_system_logs_service.GetSystemLogsResponse
)
async def api_get_get_system_logs(
    start_time: Optional[str],
    end_time: Optional[str],
    log_type: Optional[str],
    page: Optional[int],
    page_size: Optional[int],
) -> project.get_system_logs_service.GetSystemLogsResponse | Response:
    """
    Retrieves logs related to system operations, user activities, and errors.
    """
    try:
        res = await project.get_system_logs_service.get_system_logs(
            start_time, end_time, log_type, page, page_size
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_service.LoginResponse)
async def api_post_login(
    email: str, password: str
) -> project.login_service.LoginResponse | Response:
    """
    Authenticates a user and returns an access token.
    """
    try:
        res = await project.login_service.login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/customize",
    response_model=project.customize_qr_code_service.CustomizeQRCodeResponse,
)
async def api_post_customize_qr_code(
    qr_code_id: str, color: str, logo: Optional[str], size: int
) -> project.customize_qr_code_service.CustomizeQRCodeResponse | Response:
    """
    Applies customization options to a generated QR code.
    """
    try:
        res = await project.customize_qr_code_service.customize_qr_code(
            qr_code_id, color, logo, size
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
