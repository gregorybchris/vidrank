from typing import List

from pydantic import BaseModel

from vidrank.lib.selection_video import SelectionVideo


class Selection(BaseModel):
    videos: List[SelectionVideo]
