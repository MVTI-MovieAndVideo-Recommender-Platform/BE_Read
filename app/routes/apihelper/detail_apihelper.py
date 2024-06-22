import asyncio

from database import mongo_conn
from routes.apihelper import execute_task


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
    rating_info, preference_info, media_info = await asyncio.gather(
        execute_task(rating_task, "Rating Task"),
        execute_task(preference_task, "Preference Task"),
        execute_task(media_task, "Media Task"),
    )
    return (
        rating_info if rating_info else None,
        preference_info if preference_info else None,
        media_info,
    )
