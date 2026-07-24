import time

from starlette.middleware.base import BaseHTTPMiddleware

from backend.api.core.logger import logger


class RequestLoggerMiddleware(

    BaseHTTPMiddleware

):

    async def dispatch(

        self,

        request,

        call_next

    ):

        start = time.time()

        response = await call_next(request)

        elapsed = round(

            time.time() - start,

            3

        )

        logger.info(

            f"{request.method} "

            f"{request.url.path} "

            f"{response.status_code} "

            f"{elapsed}s"

        )

        return response