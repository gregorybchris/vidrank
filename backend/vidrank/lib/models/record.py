from pydantic import BaseModel

from vidrank.lib.models.choice_set import ChoiceSet


class Record(BaseModel):
    id: str
    created_at: int
    choice_set: ChoiceSet
