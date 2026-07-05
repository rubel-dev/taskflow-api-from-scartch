import time
from fastapi import Request
from fastapi.responses import JSONResponse

RATE_LIMIT = 100
WINDOW = 60

request_store = {}


async def rate_limit_middleware(
    request: Request,
    call_next
):
    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in request_store:
        request_store[client_ip] = {
            "count": 1,
            "start_time": current_time
        }

        return await call_next(request)

    record = request_store[client_ip]

    time_passed = current_time - record["start_time"]

    if time_passed > WINDOW:
        request_store[client_ip] = {
            "count": 1,
            "start_time": current_time
        }

        return await call_next(request)

    record["count"] += 1

    if record["count"] > RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "message": "Too many requests. Please try again later."
            }
        )

    return await call_next(request)

