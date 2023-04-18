from fastapi import FastAPI

from controller.background_removal_controller import \
    router as background_removal_router

app = FastAPI()

app.include_router(background_removal_router, )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
