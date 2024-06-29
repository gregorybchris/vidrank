from pydantic import BaseModel

from vidrank.lib.models.choice_set import ChoiceSet


class Record(BaseModel):
    """Record model."""

    id: str
    created_at: int
    choice_set: ChoiceSet
