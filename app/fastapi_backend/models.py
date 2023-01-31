from pydantic import BaseModel
from enum import Enum


class ItemType(str, Enum):
    anime = "anime"
    manga = "manga"


class SearchedItem(BaseModel):
    name: str
    item_type: ItemType
