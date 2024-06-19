import random
from typing import List

from database import mongo_conn
from fastapi import HTTPException, Query


async def get_top_rank_random_contents():
    try:
        media_cursor = (
            mongo_conn.content.media.find({}, {"_id": 0, "id": 1, "title": 1})
            .sort("rating_count", -1)
            .limit(1000)
        )
        medias = await media_cursor.to_list(length=1000)

        if not medias:
            raise HTTPException(status_code=404, detail="No movies found")

        # 랜덤으로 영화 선택
        selected_medias = random.sample(medias, k=20)
        print(
            "previousmedia=" + "previousmedia=".join([f"{i.get('id')}&" for i in selected_medias])
        )
        return {"media": selected_medias}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def re_get_top_rank_random_contents(
    previousmedia: List[int] = Query(..., description="이미 리스트업된 컨텐츠 ID")
):
    try:
        media_cursor = (
            mongo_conn.content.media.find({}, {"_id": 0, "id": 1, "title": 1})
            .sort("rating_count", -1)
            .limit(1000)
        )
        medias = await media_cursor.to_list(length=1000)

        if not medias:
            raise HTTPException(status_code=404, detail="No movies found")

        remaining_media = [media for media in medias if media["id"] not in previousmedia]

        if not remaining_media:
            raise HTTPException(status_code=404, detail="No more movies available to recommend")

        # 랜덤으로 영화 선택
        new_selected_media = random.sample(remaining_media, k=20)

        return {"movies": new_selected_media, "except_media": previousmedia}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
