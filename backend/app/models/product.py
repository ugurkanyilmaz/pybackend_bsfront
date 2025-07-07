from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    name: str
    popularityScore: float
    weight: float
    images: dict[str, str]
    price: Optional[float] = None