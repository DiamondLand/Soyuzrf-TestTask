from fastapi import HTTPException, status

class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

    @classmethod
    def get_dict(cls):
        return {"detail": cls.detail}

def generate_responses(errors: list):
    return {err.status_code: {"description": err.detail} for err in errors}

class EmailRegisteredException(BaseHTTPException):
    def __init__(self):
        super().__init__(status.HTTP_400_BAD_REQUEST, "Email already registered")

class CredentialsException(BaseHTTPException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
