from pydantic import BaseModel, Field
from typing import List

class ItemIn(BaseModel):
    name: str = Field(..., min_length=1)
    path: str = Field(..., min_length=2, pattern=r"^(.*/)([^/]*)$")

class ItemOut(ItemIn):
    id: int
