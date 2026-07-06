class AppError(Exception):
    status_code: int = 400
    error_code: str = "app_error"
    def __init__(self, message: str, *, status_code=None, error_code=None, details=None) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None: self.status_code = status_code
        if error_code is not None: self.error_code = error_code
        self.details = details
class NotFoundError(AppError): status_code = 404; error_code = "not_found"
class ValidationError(AppError): status_code = 422; error_code = "validation_error"
class ConflictError(AppError): status_code = 409; error_code = "conflict"
class AuthenticationError(AppError): status_code = 401; error_code = "authentication_error"
class AuthorizationError(AppError): status_code = 403; error_code = "authorization_error"
