from datetime import datetime
from typing import List

from pydantic import BaseModel


class MovieResponse(BaseModel):
    id: int = None
    title: str = None
    release_date: datetime = None
    runtime: int = None
    certification: str = None
    genre: List[str] = None
    origin_country: str = None
    overview: str = None
    director: str = None
    actor: List[str] = None
    platform: List[str] = None
    rating_value: float = None
    rating_count: int = None
    poseterurl_count: int = None
    backdropurl_count: int = None
    posterurl: List[str] = None
    backdropurls: List[str] = None
