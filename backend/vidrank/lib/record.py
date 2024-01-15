from pydantic import BaseModel

from vidrank.lib.choice_set import ChoiceSet


class Record(BaseModel):
    id: str
    choice_set: ChoiceSet
