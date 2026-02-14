from fastapi import FastAPI, HTTPException
from app.api.v1.api import api_router as v1_router
from app.core.exceptions import validation_exception_handler, http_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="FastAPI Project",
    description="A sample FastAPI project with a structured layout.",
    version="1.0.0",
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(v1_router, prefix="/api/v1")

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to the FastAPI Project!",
        "version": "1.0.0",
    }
