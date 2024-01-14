from pydantic import BaseModel

from vidrank.lib.selection import Selection


class Record(BaseModel):
    id: str
    selection: Selection
