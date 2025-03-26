from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class CustomException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(
            status_code=status_code, detail={"message": message, "status": status_code}
        )


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail["message"], "status": exc.status_code},
    )
