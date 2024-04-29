import logging
from typing import List

from fastapi import APIRouter
from fastapi import HTTPException as HttpException
from pydantic import BaseModel

from vidrank import __version__ as package_version
from vidrank.app.app_state import AppState
from vidrank.lib.matching.matcher import Matcher
from vidrank.lib.models.choice_set import ChoiceSet
from vidrank.lib.models.record import Record
from vidrank.lib.models.settings import Settings
from vidrank.lib.ranking.ranker import Ranker
from vidrank.lib.utilities.datetime_utilities import get_timestamp
from vidrank.lib.utilities.identifier_utilities import get_identifier
from vidrank.lib.youtube.video import Video

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


class PostVideosRequest(BaseModel):
    settings: Settings


class PostVideosResponse(BaseModel):
    videos: List[Video]


@router.post(name="Videos", path="/videos", description="Post videos.")
def post_videos(request: PostVideosRequest) -> PostVideosResponse:
    app_state = AppState.get()

    videos = list(Matcher.match(app_state, N_VIDEOS_PER_RESPONSE, request.settings.matching_settings))

    return PostVideosResponse(videos=videos)


class PostSubmitRequest(BaseModel):
    choice_set: ChoiceSet
    settings: Settings


class PostSubmitResponse(BaseModel):
    record_id: str
    videos: List[Video]


@router.post(name="Submit", path="/submit", description="Post submit.")
def post_submit(request: PostSubmitRequest) -> PostSubmitResponse:
    app_state = AppState.get()
    videos = list(Matcher.match(app_state, N_VIDEOS_PER_RESPONSE, request.settings.matching_settings))

    record_id = get_identifier()
    created_at = get_timestamp()
    record = Record(
        id=record_id,
        created_at=created_at,
        choice_set=request.choice_set,
    )
    app_state.record_tracker.add(record)
    return PostSubmitResponse(record_id=record_id, videos=videos)


class PostUndoRequest(BaseModel):
    record_id: str


class PostUndoResponse(BaseModel):
    videos: List[Video]
    choice_set: ChoiceSet


@router.post(name="Undo", path="/undo", description="Post undo.")
def post_undo(request: PostUndoRequest) -> PostUndoResponse:
    app_state = AppState.get()
    record = app_state.record_tracker.pop(request.record_id)
    if record is None:
        raise HttpException(status_code=404, detail="Videos no longer available")

    video_ids = [choice.video_id for choice in record.choice_set.choices]
    videos = list(app_state.youtube_facade.iter_videos(video_ids))

    return PostUndoResponse(videos=videos, choice_set=record.choice_set)


class PostSkipRequest(BaseModel):
    choice_set: ChoiceSet
    settings: Settings


class PostSkipResponse(BaseModel):
    record_id: str
    videos: List[Video]


@router.post(name="Skip", path="/skip", description="Post skip.")
def post_skip(request: PostSkipRequest) -> PostSkipResponse:
    app_state = AppState.get()
    videos = list(Matcher.match(app_state, N_VIDEOS_PER_RESPONSE, request.settings.matching_settings))

    record_id = get_identifier()
    created_at = get_timestamp()
    record = Record(
        id=record_id,
        created_at=created_at,
        choice_set=request.choice_set,
    )
    app_state.record_tracker.add(record)
    return PostSkipResponse(record_id=record_id, videos=videos)


class ResponseRanking(BaseModel):
    video: Video
    rank: int
    rating: float


class GetRankingsResponse(BaseModel):
    rankings: List[ResponseRanking]


@router.get(name="Rankings", path="/rankings", description="Get rankings.")
def get_rankings() -> GetRankingsResponse:
    app_state = AppState.get()

    records = app_state.record_tracker.load()
    rankings = list(Ranker.iter_rankings(records))
    video_ids = [ranking.video_id for ranking in rankings]
    videos = list(app_state.youtube_facade.iter_videos(video_ids))
    video_map = {video.id: video for video in videos}

    response_rankings = []
    for ranking in rankings:
        if ranking.video_id not in video_map:
            logger.debug(f"Video with ID {ranking.video_id} not found")
            continue
        video = video_map[ranking.video_id]
        response_ranking = ResponseRanking(
            video=video,
            rank=ranking.rank,
            rating=ranking.rating,
        )
        response_rankings.append(response_ranking)

    return GetRankingsResponse(rankings=response_rankings)
