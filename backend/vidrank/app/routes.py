from fastapi import APIRouter
from fastapi.responses import JSONResponse

from vidrank import __version__ as package_version

router = APIRouter()


@router.get(name="Status", description="Get the API status.", path="/")
def get_status() -> JSONResponse:
    return JSONResponse({"status": "healthy"})


@router.get(name="Version", description="Get the API version.", path="/version")
def get_version() -> JSONResponse:
    return JSONResponse({"version": package_version})


@router.get(name="Videos", description="Get videos.", path="/videos")
def get_videos() -> JSONResponse:
    return JSONResponse({"videos": []})
