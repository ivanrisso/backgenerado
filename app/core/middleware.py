#app/core/middleware.py
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import logging
import traceback

logger = logging.getLogger("uvicorn.error")

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"❌ Error inesperado: {repr(exc)}")
            traceback.print_exc()
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Ocurrió un error inesperado. Por favor intente más tarde."
                }
            )
