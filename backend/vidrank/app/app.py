import logging
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vidrank.app.log_config import LogConfig
from vidrank.app.routes import router

dictConfig(LogConfig().model_dump())

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
