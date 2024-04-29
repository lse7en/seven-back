from typing import Any

from fastapi import HTTPException, status
from src.core.constants import ErrorCode


# define custom exceptions


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS


class UsernameTaken(BadRequest):
    DETAIL = ErrorCode.USERNAME_TAKEN


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID


class UserNotFound(NotFound):
    DETAIL = ErrorCode.USER_NOT_FOUND

class RoomNotFound(NotFound):
    DETAIL = ErrorCode.ROOM_NOT_FOUND


class RoomAlreadyStarted(BadRequest):
    DETAIL = ErrorCode.ROOM_ALREADY_STARTED

class RoomPending(BadRequest):
    DETAIL = ErrorCode.ROOM_PENDING

class RoomFinished(BadRequest):
    DETAIL = ErrorCode.ROOM_FINISHED

class CoolDown(BadRequest):
    DETAIL = ErrorCode.COOL_DOWN

class InvalidEdge(BadRequest):
    DETAIL = ErrorCode.INVALID_EDGE

class EdgeAlreadyOn(BadRequest):
    DETAIL = ErrorCode.EDGE_ALREADY_ENABLED

class EdgeAlreadyOff(BadRequest):
    DETAIL = ErrorCode.EDGE_ALREADY_DISABLED
