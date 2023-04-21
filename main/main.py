from fastapi import FastAPI, Depends
from slowapi.errors import RateLimitExceeded
from starlette.responses import PlainTextResponse

from controller.background_removal_controller import \
    router as background_removal_router
from middleware.rate_limiter import create_rate_limiter


app = FastAPI()

# Initialize the rate limiter
limiter = create_rate_limiter()
app.state = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler():
    return PlainTextResponse("Too many requests", status_code=429)


# Include the background removal router
app.include_router(background_removal_router, prefix="/v1",
                   dependencies=[Depends(lambda: limiter)])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


