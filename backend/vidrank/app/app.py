import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vidrank.app.app_state import AppState
from vidrank.app.routes import router

logger = logging.getLogger(__name__)


app = FastAPI()

AppState.init()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
