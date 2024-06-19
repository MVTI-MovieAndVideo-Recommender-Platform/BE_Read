import asyncio
from datetime import datetime
from typing import List, Optional

from database import mongo_conn
from fastapi import HTTPException, Query, Request
from routes.apihelper import base64_to_uuid


async def detail_func(id: int, request: Request):
    print(request.state.token)
    if request.state.token and (user_id := base64_to_uuid(request.state.token)):
        rating_data, preference_data, media_data = await get_matching_data(user_id, id, id)
        if rating_data:
            media_data["rating"] = rating_data.get("rating")
        media_data["preference"] = True if preference_data else False
    else:
        media_data = await mongo_conn.content.media.find_one(
            {"id": id}, {"_id": 0, "backdropurl": 0, "posterurl": 0}
        )
    try:
        if not media_data:
            raise HTTPException(status_code=404, detail="No movies found")
        return media_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# user_id와 media_id를 인자로 받아 데이터를 쿼리하는 함수 정의
async def get_matching_data(user_id, media_id, id):
    # 쿼리를 동시에 실행
    rating_task = mongo_conn.review.rating.find_one(
        {"user_id": user_id, "media_id": media_id}, {"_id": 0, "rating": 1}
    )
    preference_task = mongo_conn.review.preference.find_one(
        {"user_id": user_id, "media_id": media_id}, {"_id": 1}
    )
    media_task = mongo_conn.content.media.find_one(
        {"id": id}, {"_id": 0, "backdropurl": 0, "posterurl": 0}
    )

    # 두 개의 쿼리 결과를 동시에 기다림
    # rating_data, preference_data = await asyncio.gather(rating_task, preference_task, media_task)

    return await asyncio.gather(rating_task, preference_task, media_task)
