import asyncio

from database import mongo_conn
from fastapi import HTTPException
from routes.apihelper import execute_task


# user_id와 media_id를 인자로 받아 데이터를 쿼리하는 함수 정의
async def get_matching_data(user_id: str):
    # 비동기 쿼리 실행
    user_task = mongo_conn.member.user.find_one(
        {"_id": user_id}, {"_id": 0, "email": 0, "last_update": 0, "is_delete": 0}
    )
    rating_task = mongo_conn.review.rating.find(
        {"user_id": user_id}, {"media_id": 1, "rating": 1}
    ).to_list(length=None)
    preference_task = mongo_conn.review.preference.find(
        {"user_id": user_id}, {"media_id": 1}
    ).to_list(length=None)
    recommend_task = mongo_conn.recommend.recommendation.find({"user_id": user_id})

    # 태스크를 개별적으로 실행 및 예외 처리
    user_info, rating_info, preference_info, recommend_info = await asyncio.gather(
        execute_task(user_task, "User Task"),
        execute_task(rating_task, "Rating Task"),
        execute_task(preference_task, "Preference Task"),
        execute_task(recommend_task, "Recommend Task"),
    )

    print("user_info : ", user_info)
    print("rating_info : ", rating_info)
    print("preference_info : ", preference_info)
    print("recommend_info : ", recommend_info)

    if user_info:
        user_info["rating_list"] = rating_info if rating_info else None
        user_info["preference_list"] = preference_info if preference_info else None
        user_info["recommend_list"] = recommend_info if recommend_info else None
        return user_info
    else:
        if not user_info:
            raise HTTPException(status_code=404, detail="No User Found")
