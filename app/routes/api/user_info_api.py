from datetime import datetime
from typing import List, Optional

from database import mongo_conn
from fastapi import HTTPException, Query, Request


async def detail_func(id: int):
    try:
        media_cursor = await mongo_conn.content.media.find_one({"id": id}, {"_id": 0})

        if not media_cursor:
            raise HTTPException(status_code=404, detail="No movies found")
        return media_cursor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
