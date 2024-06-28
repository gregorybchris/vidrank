from pydantic import BaseModel

from vidrank.lib.models.choice import Choice


class ChoiceSet(BaseModel):
    choices: list[Choice]
