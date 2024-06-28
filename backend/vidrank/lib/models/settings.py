"""Application settings model."""

from pydantic import BaseModel

from vidrank.lib.models.matching_settings import MatchingSettings


class Settings(BaseModel):
    """Application settings model."""

    matching_settings: MatchingSettings
