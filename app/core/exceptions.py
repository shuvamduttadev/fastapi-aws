from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    
    for err in exc.errors():
        field = err["loc"][-1]
        message = err["msg"]

        errors.append({
            "field": field,
            "message": message
        })

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation Error",
            "details": errors
        },
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        },
    )