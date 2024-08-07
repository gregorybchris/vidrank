import logging
import math
from typing import Annotated

from fastapi import APIRouter, Depends
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


async def app_state_dep() -> AppState:
    """Application state dependency."""
    return AppState.get()


AppStateDep = Annotated[AppState, Depends(app_state_dep)]

N_VIDEOS_PER_RESPONSE = 6


class GetStatusResponse(BaseModel):
    """Model for the response of the status route."""

    status: str


@router.get(name="Status", path="/", description="Get the API status.")
def get_status() -> GetStatusResponse:
    """Get the status of the API."""
    return GetStatusResponse(status="healthy")


class GetVersionResponse(BaseModel):
    """Model for the response of the version route."""

    version: str


@router.get(name="Version", path="/version", description="Get the API version.")
def get_version() -> GetVersionResponse:
    """Route to get the version of the API."""
    return GetVersionResponse(version=package_version)


class PostVideosRequest(BaseModel):
    """Model for the request of the videos route."""

    settings: Settings


class PostVideosResponse(BaseModel):
    """Model for the response of the videos route."""

    videos: list[Video]


@router.post(name="Videos", path="/videos", description="Post videos.")
def post_videos(request: PostVideosRequest, app_state: AppStateDep) -> PostVideosResponse:
    """Route for posting a request for videos.

    Args:
        request (PostVideosRequest): The request for videos.
        app_state (AppStateDep): The application state.

    Returns:
        PostVideosResponse: The response to the request for videos.
    """
    videos = list(Matcher.match(app_state, N_VIDEOS_PER_RESPONSE, request.settings.matching_settings))

    return PostVideosResponse(videos=videos)


class PostSubmitRequest(BaseModel):
    """Model for the request of the submit."""

    choice_set: ChoiceSet
    settings: Settings


class PostSubmitResponse(BaseModel):
    """Model for the response of the submit route."""

    record_id: str
    videos: list[Video]


@router.post(name="Submit", path="/submit", description="Post submit.")
def post_submit(request: PostSubmitRequest, app_state: AppStateDep) -> PostSubmitResponse:
    """Route for posting a submit request.

    Args:
        request (PostSubmitRequest): The request to submit a choice.
        app_state (AppStateDep): The application state.

    Returns:
        PostSubmitResponse: The response to the submit request.
    """
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
    """Model for the request of the undo route."""

    record_id: str


class PostUndoResponse(BaseModel):
    """Model for the response of the undo route."""

    videos: list[Video]
    choice_set: ChoiceSet


@router.post(name="Undo", path="/undo", description="Post undo.")
def post_undo(request: PostUndoRequest, app_state: AppStateDep) -> PostUndoResponse:
    """Route for posting an undo request.

    Args:
        request (PostUndoRequest): The request to undo a choice.
        app_state (AppStateDep): The application state.

    Returns:
        PostUndoResponse: The response to the undo request.

    Raises:
        HttpException: If the record ID is not found.
    """
    record = app_state.record_tracker.pop(request.record_id)
    if record is None:
        raise HttpException(status_code=404, detail="Videos no longer available")

    video_ids = [choice.video_id for choice in record.choice_set.choices]
    videos = list(app_state.youtube_facade.iter_videos(video_ids))

    return PostUndoResponse(videos=videos, choice_set=record.choice_set)


class PostSkipRequest(BaseModel):
    """Model for the request of the skip route."""

    choice_set: ChoiceSet
    settings: Settings


class PostSkipResponse(BaseModel):
    """Model for the response of the skip route."""

    record_id: str
    videos: list[Video]


@router.post(name="Skip", path="/skip", description="Post skip.")
def post_skip(request: PostSkipRequest, app_state: AppStateDep) -> PostSkipResponse:
    """Route for posting a skip request.

    Args:
        request (PostSkipRequest): The request to skip a choice.
        app_state (AppStateDep): The application state.

    Returns:
        PostSkipResponse: The response to the skip request.
    """
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
    """Model for a ranking response."""

    video: Video
    rank: int
    rating: float


class PostRankingsRequest(BaseModel):
    """Model for the request of the rankings route."""

    page_number: int
    page_size: int


class PostRankingsResponse(BaseModel):
    """Model for the response of the rankings route."""

    page_number: int
    n_pages: int
    rankings_page: list[ResponseRanking]


@router.post(name="Rankings", path="/rankings", description="Get rankings.")
def get_rankings(request: PostRankingsRequest, app_state: AppStateDep) -> PostRankingsResponse:
    """Route for getting video rankings."""
    page_number = request.page_number
    if page_number < 1:
        raise HttpException(status_code=400, detail="Page number must be greater than zero")

    page_size = request.page_size
    if page_size < 1:
        raise HttpException(status_code=400, detail="Page size must be greater than zero")

    records = app_state.record_tracker.load()
    rankings = list(Ranker.iter_rankings(records))
    video_ids = [ranking.video_id for ranking in rankings]
    videos = list(app_state.youtube_facade.iter_videos(video_ids))
    video_map = {video.id: video for video in videos}

    # NOTE: We have to fetch all videos in the rankings to find out if any videos
    # are missing from YouTube, otherwise pagination could be incorrect.
    response_rankings = []
    for ranking in rankings:
        if ranking.video_id not in video_map:
            logger.debug("Video with ID %s not found", ranking.video_id)
            continue
        video = video_map[ranking.video_id]
        response_ranking = ResponseRanking(
            video=video,
            rank=ranking.rank,
            rating=ranking.rating,
        )
        response_rankings.append(response_ranking)

    n_pages = math.ceil(len(response_rankings) / page_size)
    if page_number > n_pages:
        raise HttpException(status_code=404, detail="Page not found")

    page_start = (page_number - 1) * page_size
    page_end = page_start + page_size
    rankings_page = response_rankings[page_start:page_end]

    return PostRankingsResponse(
        page_number=page_number,
        n_pages=n_pages,
        rankings_page=rankings_page,
    )
