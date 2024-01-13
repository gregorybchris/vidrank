from pydantic import BaseModel


class Thumbnail(BaseModel):
    width: int
    height: int
    url: str
