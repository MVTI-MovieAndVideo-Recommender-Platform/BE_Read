import random
from datetime import datetime, timedelta

from database import mongo_conn
from routes.apihelper import keyword_content


# 상위 20개의 미디어를 추천하는 함수
async def get_top_media():
    # 오늘 날짜와 1달 전 날짜 계산
    today = datetime.now()
    one_month_ago = today - timedelta(days=60)
    pipeline = [
        {"$match": {"release_date": {"$gte": one_month_ago, "$lte": today}}},
        {"$addFields": {"rating_score": {"$multiply": ["$rating_value", "$rating_count"]}}},
        {"$sort": {"rating_score": -1}},
        {"$limit": 20},
        {
            "$project": {
                "_id": 0,
                "id": 1,
                "title": 1,
                "rating_value": 1,
                "rating_count": 1,
                "posterurl_count": 1,
            }
        },
    ]
    return [media async for media in mongo_conn.content.media.aggregate(pipeline)]


def get_keyword_content_indices() -> dict:
    # 키 목록에서 랜덤으로 5개의 키워드 선택
    random_keywords = random.sample(list(keyword_content.keys()), 5)

    # 선택된 키워드 및 해당 내용 출력
    return {keyword: keyword_content[keyword] for keyword in random_keywords}


# user_id와 media_id를 인자로 받아 데이터를 쿼리하는 함수 정의
# async def get_matching_data(media_id_list):
#     # 쿼리를 동시에 실행
#     media_task = mongo_conn.content.media.find_one(
#         {"id": id}, {"_id": 0, "backdropurl": 0, "posterurl": 0}
#     )
#     return media_task
