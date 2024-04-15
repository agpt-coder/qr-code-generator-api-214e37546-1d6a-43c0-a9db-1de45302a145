from typing import List, Optional

from pydantic import BaseModel


class LogEntry(BaseModel):
    """
    Represents a single log entry in the system.
    """

    timestamp: str
    type: str
    message: str
    details: Optional[str] = None


class GetSystemLogsResponse(BaseModel):
    """
    Response model for system logs, including paginated logs and metadata.
    """

    logs: List[LogEntry]
    page: int
    total_pages: int
    logs_per_page: int
    total_logs: int


async def get_system_logs(
    start_time: Optional[str],
    end_time: Optional[str],
    log_type: Optional[str],
    page: Optional[int],
    page_size: Optional[int],
) -> GetSystemLogsResponse:
    """
    Retrieves logs related to system operations, user activities, and errors.

    Args:
    start_time (Optional[str]): The starting point of the time range for which logs are requested, in ISO 8601 format.
    end_time (Optional[str]): The ending point of the time range for which logs are requested, also in ISO 8601 format.
    log_type (Optional[str]): Optional filter for the type of logs to retrieve, such as 'error', 'activity', or 'performance'.
    page (Optional[int]): The page number for pagination, starting from 1.
    page_size (Optional[int]): The number of logs to return per page, for pagination control.

    Returns:
    GetSystemLogsResponse: Response model for system logs, including paginated logs and metadata.
    """
    mock_logs = [
        LogEntry(
            timestamp="2023-01-01T12:00:00+00:00",
            type="error",
            message="Example error log",
            details="Error details",
        ),
        LogEntry(
            timestamp="2023-01-02T13:00:00+00:00",
            type="activity",
            message="Example activity log",
            details=None,
        ),
    ]
    if page is None or page_size is None:
        page = 1
        page_size = len(mock_logs)
    filtered_logs = mock_logs
    total_logs = len(filtered_logs)
    total_pages = total_logs // page_size + (1 if total_logs % page_size > 0 else 0)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_logs = filtered_logs[start_index:end_index]
    return GetSystemLogsResponse(
        logs=paginated_logs,
        page=page,
        total_pages=total_pages,
        logs_per_page=len(paginated_logs),
        total_logs=total_logs,
    )
