import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from .routes.employee import emp

load_dotenv()

app = FastAPI(
    title=os.environ.get("APP_NAME", "Employee Recorder"),
    version=os.environ.get("VERSION", "0.1.0"),
)

app.include_router(router=emp)


@app.get("/", tags=["root"])
async def get_index() -> dict[str, str]:
    return {"status": "Listening..."}


def run_platform() -> None:
    is_dev = True if os.environ.get("DEV", False) else False
    uvicorn.run(app="fastapi_demo.app:app", port=5000, reload=is_dev)
