"""Choice set model."""

from pydantic import BaseModel

from vidrank.lib.models.choice import Choice


class ChoiceSet(BaseModel):
    """Choice set model."""

    choices: list[Choice]
