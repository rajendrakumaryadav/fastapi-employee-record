import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes.designation import designation_router
from .routes.employee import emp
from .routes.frontend import frontend_routes

# Loading environment during the runtime of Application
load_dotenv()

# Initializing application
app = FastAPI(
    title=os.environ.get("APP_NAME", "Employee Recorder"),
    version=os.environ.get("VERSION", "0.1.0"),
)

# Adding static folder accessible
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/js", StaticFiles(directory="static/js"), name="js")
app.mount("/images", StaticFiles(directory="static/images"), name="images")


# Adding routes to main Application
app.include_router(router=emp)
app.include_router(router=frontend_routes)
app.include_router(router=designation_router, tags=["Designation"])


# Health check endpoint
@app.get(
    "/health", tags=["Health"], description="Provide status of FastAPI server"
)
async def get_index() -> dict[str, str]:
    return {"status": "Listening..."}


# Firing up platform.
def run_platform() -> None:
    is_dev = True if os.environ.get("DEV", False) else False
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app="fastapi_demo.app:app", port=port, reload=is_dev)
