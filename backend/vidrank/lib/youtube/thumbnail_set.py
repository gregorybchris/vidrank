"""Thumbnail set for a YouTube video."""

from typing import Optional

from pydantic import BaseModel

from vidrank.lib.youtube.thumbnail import Thumbnail


class ThumbnailSet(BaseModel):
    """Set of thumbnails for a YouTube video."""

    default: Optional[Thumbnail]
    standard: Optional[Thumbnail]
    medium: Optional[Thumbnail]
    high: Optional[Thumbnail]
    maxres: Optional[Thumbnail]

    def get_highest_resolution(self) -> Optional[Thumbnail]:
        """Get the thumbnail with the highest resolution.

        Returns
        -------
        Optional[Thumbnail]: The thumbnail with the highest resolution.

        """
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
