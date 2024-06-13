from datetime import datetime
from typing import List, Optional

from database import mongo_conn
from fastapi import HTTPException, Query
from routes.apihelper.search_apihelper import (
    search_actors,
    search_countrys,
    search_directors,
    search_genres,
    search_overviews,
    search_periods,
    search_platforms,
    search_titles,
)


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
    total_count = await mongo_conn.content.media.count_documents(query)

    # 페이지네이션
    skip = (page - 1) * page_size
    results = mongo_conn.content.media.find(query, {"_id": 0}).skip(skip).limit(page_size)

    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size,
        "results": await results.to_list(length=page_size),
    }
