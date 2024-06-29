from pydantic import BaseModel


class Thumbnail(BaseModel):
    """YouTube video thumbnail model."""

    width: int
    height: int
    url: str
