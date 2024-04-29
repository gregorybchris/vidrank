from typing import Dict, Optional

from pydantic import BaseModel

from vidrank.lib.utilities.typing_utilities import JsonObject
from vidrank.lib.youtube.thumbnail import Thumbnail


class ThumbnailSet(BaseModel):
    default: Optional[Thumbnail]
    standard: Optional[Thumbnail]
    medium: Optional[Thumbnail]
    high: Optional[Thumbnail]
    maxres: Optional[Thumbnail]

    def get_highest_resolution(self) -> Optional[Thumbnail]:
        if self.maxres is not None:
            return self.maxres
        if self.high is not None:
            return self.high
        if self.medium is not None:
            return self.medium
        if self.standard is not None:
            return self.standard
        if self.default is not None:
            return self.default
        return None

    @classmethod
    def from_dict(cls, thumbnail_set_dict: JsonObject) -> "ThumbnailSet":
        thumbnail_set_kwargs: Dict[str, Optional[Thumbnail]] = {}
        for size in ["default", "standard", "medium", "high", "maxres"]:
            if size in thumbnail_set_dict and thumbnail_set_dict[size] is not None:
                thumbnail_dict = thumbnail_set_dict[size]
                thumbnail = Thumbnail(
                    width=thumbnail_dict["width"],
                    height=thumbnail_dict["height"],
                    url=thumbnail_dict["url"],
                )
                thumbnail_set_kwargs[size] = thumbnail
            else:
                thumbnail_set_kwargs[size] = None
        return ThumbnailSet(**thumbnail_set_kwargs)
