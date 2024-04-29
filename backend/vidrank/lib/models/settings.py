from pydantic import BaseModel

from vidrank.lib.models.matching_settings import MatchingSettings


class Settings(BaseModel):
    matching_settings: MatchingSettings
