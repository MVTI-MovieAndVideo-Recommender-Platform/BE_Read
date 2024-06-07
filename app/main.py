import datetime
import json
from typing import List

from bson import json_util
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
    release_date: datetime.datetime = None
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


@app.post("/content/", response_model=MovieResponse)
async def create_content(content: MovieResponse):
    result = await collection.insert_one(content.dict())
    if result.inserted_id:
        content_data = await collection.find_one({"_id": result.inserted_id})
        return content_data
    raise HTTPException(status_code=400, detail="Content could not be created")


@app.get("/content/", response_model=List[MovieResponse])
async def get_all_contents():
    contents = await collection.find().to_list(length=100)
    return contents


def convert_to_json(data):
    return json.loads(json_util.dumps(data))


def normalize_string(s):
    return s.replace(" ", "")


@app.get("/search/genre")
async def get_movie_by_genre(
    genres: List[str] = Query(...), contentype: int = 0, page: int = 1, page_size: int = 100
):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be 1 or greater.")
    query = {"$and": [{"genre": {"$regex": genre, "$options": "i"}} for genre in genres]}
    # 모든 주어진 장르를 포함하는 영화를 찾기 위해 $and를 사용
    if contentype == 1:  # 영화
        query["id"] = {"$mod": [2, 1]}  # id가 홀수인 데이터만
    elif contentype == 2:  # 시리즈
        query["id"] = {"$mod": [2, 0]}  # id가 홀수인 데이터만

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
        "results": await results.to_list(length=None),
    }


# 8-byte 미만의 int로 검색해야함(MongoDB can only handle up to 8-byte ints)
# 타이틀 검색 API
@app.get("/search/title")
async def get_content_by_title(
    title: str, contentype: int = 0, page: int = 1, page_size: int = 100
):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be 1 or greater.")

    regex = ".*".join(normalize_string(title))
    query = {"title": {"$regex": regex, "$options": "i"}}  # 대소문자 구분 없이 검색
    # 모든 주어진 장르를 포함하는 영화를 찾기 위해 $and를 사용
    if contentype == 1:  # 영화
        query["id"] = {"$mod": [2, 1]}  # id가 홀수인 데이터만
    elif contentype == 2:  # 시리즈
        query["id"] = {"$mod": [2, 0]}  # id가 홀수인 데이터만

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
        "results": await results.to_list(length=None),
    }


@app.get("/search/country")
async def get_content_by_country(
    country: str, contentype: int = 0, page: int = 1, page_size: int = 100
):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be 1 or greater.")
    query = {"origin_country": {"$regex": country, "$options": "i"}}  # 대소문자 구분 없이 검색

    # 모든 주어진 장르를 포함하는 영화를 찾기 위해 $and를 사용
    if contentype == 1:  # 영화
        query["id"] = {"$mod": [2, 1]}  # id가 홀수인 데이터만
    elif contentype == 2:  # 시리즈
        query["id"] = {"$mod": [2, 0]}  # id가 홀수인 데이터만

    total_count = await collection.count_documents(query)

    # 페이지네이션
    skip = (page - 1) * page_size
    results = collection.find(query, {"_id": 0}).skip(skip).limit(page_size)
    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size,
        "results": await results.to_list(length=None),
    }


@app.get("/")
def test():
    return "Hello"
