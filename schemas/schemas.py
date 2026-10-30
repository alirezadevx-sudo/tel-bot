from pydantic import BaseModel, PositiveInt
from typing import Literal

class RandJokeModel(BaseModel):
    joke_id: PositiveInt
    joke_type: Literal['twopart', 'single']
    joke: str