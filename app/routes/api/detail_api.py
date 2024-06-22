from database import mongo_conn
from fastapi import HTTPException, Request
from routes.apihelper import base64_to_uuid
from routes.apihelper.detail_apihelper import get_matching_data


# 영화 디테일 엔드 포인트
async def detail_endpoint(id: int, request: Request):
    # 회원일떄
    if request.state.token and (user_id := base64_to_uuid(request.state.token)):
        rating_data, preference_data, media_data = await get_matching_data(user_id, id, id)
        if rating_data:
            media_data["rating"] = rating_data.get("rating")
        media_data["preference"] = True if preference_data else False
    else:  # 비회원 일떄
        media_data = await mongo_conn.content.media.find_one(
            {"id": id}, {"_id": 0, "backdropurl": 0, "posterurl": 0}
        )
    try:
        if not media_data:
            raise HTTPException(status_code=404, detail="No movies found")
        return media_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
