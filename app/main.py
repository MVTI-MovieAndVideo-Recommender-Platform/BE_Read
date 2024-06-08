import re
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)


# 예외 처리
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


# 예외 처리
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


# MongoDB 설정
MONGODB_URL = "mongodb://admin:mvtiserver@15.165.248.69:27017/admin"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.content
collection = db.media


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


def normalize_string(s: Optional[str]) -> str:
    return s.replace(" ", "")


def search_titles(term: List[str], and_or: Optional[str]) -> dict:
    return {
        and_or: [
            {"title": {"$regex": ".*".join(normalize_string(title)), "$options": "i"}}
            for title in term
        ]
    }


def search_genres(term: List[str], and_or: Optional[str]) -> dict:
    return {and_or: [{"genre": {"$regex": genre, "$options": "i"}} for genre in term]}


def search_overviews(term: List[str], and_or: Optional[str]) -> dict:
    return {and_or: [{"overview": {"$regex": keyword, "$options": "i"}} for keyword in term]}


def search_directors(term: List[str], and_or: Optional[str]) -> dict:
    directors = [i.replace(" ", "") for i in term]
    regex_pattern = [f".*{''.join(f'(?=.*{char})' for char in i)}.*" for i in directors]
    return {
        and_or: [
            {"director": {"$elemMatch": {"$regex": regex, "$options": "i"}}}
            for regex in regex_pattern
        ]
    }


def search_actors(term: List[str], and_or: Optional[str]) -> dict:
    actors = [i.replace(" ", "") for i in term]
    regex_pattern = [f".*{''.join(f'(?=.*{char})' for char in i)}.*" for i in actors]
    return {
        and_or: [
            {"actor": {"$elemMatch": {"$regex": regex, "$options": "i"}}} for regex in regex_pattern
        ]
    }


def search_countrys(term: List[str], and_or: Optional[str]) -> dict:
    return {and_or: [{"origin_country": {"$regex": country, "$options": "i"}} for country in term]}


def search_platforms(term: List[str], and_or: Optional[str]) -> dict:
    return {and_or: [{"platform": {"$regex": platform, "$options": "i"}} for platform in term]}


def parse_date(date_str: Optional[str]) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


def search_periods(start: Optional[str], end: Optional[str]) -> dict:
    # 날짜 범위 설정
    start_date_obj = parse_date(start) if start else datetime(1990, 1, 1)
    end_date_obj = parse_date(end) if end else datetime.today()

    return {"release_date": {"$gte": start_date_obj, "$lte": end_date_obj}}


@app.get("/search")
async def get_search(
    anything: List[str] = Query(None),
    titles: List[str] = Query(None),
    genres: List[str] = Query(None),
    keywords: List[str] = Query(None),
    directors: List[str] = Query(None),
    actors: List[str] = Query(None),
    platforms: List[str] = Query(None),
    countries: List[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    isfilter: bool = False,
    contentype: int = 0,
    page: int = 1,
    page_size: int = 100,
):
    if (
        not titles
        and not genres
        and not keywords
        and not directors
        and not actors
        and not platforms
        and not countries
        and not start_date
        and not end_date
    ) and not anything:
        raise HTTPException(status_code=400, detail="No Data!")
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be 1 or greater.")
    if isfilter:
        query = {"$and": []}
        if titles:
            query["$and"].append(search_titles(titles, "$or"))
        if genres:
            query["$and"].append(search_genres(genres, "$and"))

        if keywords:
            query["$and"].append(search_overviews(keywords, "$and"))

        if directors:
            query["$and"].append(search_directors(directors, "$or"))

        if actors:
            query["$and"].append(search_actors(actors, "$and"))

        if platforms:
            query["$and"].append(search_platforms(platforms, "$and"))

        if countries:
            query["$and"].append(search_countrys(countries, "$or"))

        if start_date or end_date:
            query["$and"].append(search_periods(start_date, end_date))
        if not query["$and"]:
            raise HTTPException(status_code=400, detail="No query to filter!")
        # mod_value 설정
        else:
            if contentype == 1:  # 영화
                query["$and"].append({"id": {"$mod": [2, 1]}})  # 홀수
            elif contentype == 2:  # 시리즈
                query["$and"].append({"id": {"$mod": [2, 0]}})  # 짝수

    else:
        query = {"$or": []}
        query["$or"].append(search_titles(anything, "$or"))
        query["$or"].append(search_genres(anything, "$and"))
        query["$or"].append(search_overviews(anything, "$and"))
        query["$or"].append(search_directors(anything, "$or"))
        query["$or"].append(search_actors(anything, "$and"))
        if not query["$or"]:
            raise HTTPException(status_code=400, detail="No query!")
        # mod_value 설정
        else:
            if contentype == 1:  # 영화
                query["$and"] = [{"id": {"$mod": [2, 1]}}]  # 홀수
            elif contentype == 2:  # 시리즈
                query["$and"] = [{"id": {"$mod": [2, 0]}}]  # 짝수

    # 전체 문서 수 조회
    total_count = await collection.count_documents(query)

    # 페이지네이션
    skip = (page - 1) * page_size
    results = collection.find(query, {"_id": 0}).skip(skip).limit(page_size)

    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size,
        "results": await results.to_list(length=page_size),
    }


@app.get("/")
def test():
    return "Hello this is mvti read server"
