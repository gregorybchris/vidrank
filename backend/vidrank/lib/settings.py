from pydantic import BaseModel

from vidrank.lib.matching_settings import MatchingSettings


class Settings(BaseModel):
    matching_settings: MatchingSettings
