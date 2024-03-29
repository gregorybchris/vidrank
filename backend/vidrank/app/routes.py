import logging
from typing import Any, List
from uuid import uuid4

from fastapi import APIRouter
from fastapi import HTTPException as HttpException
from pydantic import BaseModel

from vidrank import __version__ as package_version
from vidrank.app.app_state import AppState
from vidrank.lib.choice_set import ChoiceSet
from vidrank.lib.matcher import Matcher
from vidrank.lib.ranking.ranker import Ranker
from vidrank.lib.record import Record

logger = logging.getLogger(__name__)

router = APIRouter()

N_VIDEOS_PER_RESPONSE = 6


class GetStatusResponse(BaseModel):
    status: str


@router.get(name="Status", path="/", description="Get the API status.")
def get_status() -> GetStatusResponse:
    return GetStatusResponse(status="healthy")


class GetVersionResponse(BaseModel):
    version: str


@router.get(name="Version", path="/version", description="Get the API version.")
def get_version() -> GetVersionResponse:
    return GetVersionResponse(version=package_version)


class GetVideosResponse(BaseModel):
    videos: List[Any]


@router.get(name="Videos", path="/videos", description="Get videos.")
def get_videos() -> GetVideosResponse:
    app_state = AppState.get()
    next_videos = Matcher.match(app_state, N_VIDEOS_PER_RESPONSE)

    return GetVideosResponse(videos=[video.serialize() for video in next_videos])


class PostSubmitRequest(BaseModel):
    choice_set: ChoiceSet


class PostSubmitResponse(BaseModel):
    record_id: str
    videos: List[Any]


@router.post(name="Submit", path="/submit", description="Post submit.")
def post_submit(request: PostSubmitRequest) -> PostSubmitResponse:
    app_state = AppState.get()
    next_videos = Matcher.match(app_state, N_VIDEOS_PER_RESPONSE)

    record_id = str(uuid4())
    record = Record(
        id=record_id,
        choice_set=request.choice_set,
    )
    app_state.record_tracker.add(record)
    return PostSubmitResponse(record_id=record_id, videos=[video.serialize() for video in next_videos])


class PostUndoRequest(BaseModel):
    record_id: str


class PostUndoResponse(BaseModel):
    videos: List[Any]


@router.post(name="Undo", path="/undo", description="Post undo.")
def post_undo(request: PostUndoRequest) -> PostUndoResponse:
    app_state = AppState.get()
    record = app_state.record_tracker.pop(request.record_id)
    if record is None:
        raise HttpException(status_code=404, detail="Videos no longer available")

    video_ids = [choice.video_id for choice in record.choice_set.choices]
    next_videos = list(app_state.youtube_facade.iter_videos(video_ids))

    return PostUndoResponse(videos=[video.serialize() for video in next_videos])


class PostSkipRequest(BaseModel):
    choice_set: ChoiceSet


class PostSkipResponse(BaseModel):
    record_id: str
    videos: List[Any]


@router.post(name="Skip", path="/skip", description="Post skip.")
def post_skip(request: PostSkipRequest) -> PostSkipResponse:
    app_state = AppState.get()
    next_videos = Matcher.match(app_state, N_VIDEOS_PER_RESPONSE)

    record_id = str(uuid4())
    record = Record(
        id=record_id,
        choice_set=request.choice_set,
    )
    app_state.record_tracker.add(record)
    return PostSkipResponse(record_id=record_id, videos=[video.serialize() for video in next_videos])


class ResponseRanking(BaseModel):
    video: Any
    rank: int
    rating: float


class GetRankingsResponse(BaseModel):
    rankings: List[ResponseRanking]


@router.get(name="Rankings", path="/rankings", description="Get rankings.")
def get_rankings() -> GetRankingsResponse:
    app_state = AppState.get()

    records = app_state.record_tracker.load()
    rankings = Ranker.rank(records)
    video_ids = [ranking.video_id for ranking in rankings]
    videos = list(app_state.youtube_facade.iter_videos(video_ids))
    video_map = {video.id: video for video in videos}

    response_rankings = []
    for ranking in rankings:
        video = video_map[ranking.video_id]
        response_ranking = ResponseRanking(
            video=video.serialize(),
            rank=ranking.rank,
            rating=ranking.rating,
        )
        response_rankings.append(response_ranking)

    return GetRankingsResponse(rankings=response_rankings)
