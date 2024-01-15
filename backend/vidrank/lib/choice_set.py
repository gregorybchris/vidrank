from typing import List

from pydantic import BaseModel

from vidrank.lib.choice import Choice


class ChoiceSet(BaseModel):
    choices: List[Choice]
