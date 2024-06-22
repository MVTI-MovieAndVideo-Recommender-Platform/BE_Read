from database import mongo_conn
from fastapi import HTTPException, Request
from routes.apihelper.search_apihelper import (
    search_actors,
    search_countries,
    search_directors,
    search_genres,
    search_overviews,
    search_periods,
    search_platforms,
    search_titles,
)


async def get_search(request: Request, page_size: int = 100):
    page = int(request.query_params.get("page", 1))
    # if int(request.query_params.get("page", 1)) < 1:
    #     raise HTTPException(status_code=400, detail="Page number must be 1 or greater.")
    is_filter = request.query_params.get("isfilter", None)
    terms = (
        request.query_params.getlist("anything") if request.query_params.get("anything") else [""]
    )
    query = {"$and": []} if is_filter else {"$or": []}
    append_query = query["$and"].append if is_filter else query["$or"].append

    if is_filter:
        if titles := request.query_params.getlist("titles"):
            append_query(search_titles(titles, "$or"))
        if genres := request.query_params.getlist("genres"):
            append_query(search_genres(genres, "$and"))
        if keywords := request.query_params.getlist("keywords"):
            append_query(search_overviews(keywords, "$and"))
        if directors := request.query_params.getlist("directors"):
            append_query(search_directors(directors, "$or"))
        if actors := request.query_params.getlist("actors"):
            append_query(search_actors(actors, "$and"))
        if platforms := request.query_params.getlist("platforms"):
            append_query(search_platforms(platforms, "$and"))
        if countries := request.query_params.getlist("countries"):
            append_query(search_countries(countries, "$or"))
        if request.query_params.get("start_date") or request.query_params.get("end_date"):
            append_query(
                search_periods(
                    request.query_params.get("start_date"), request.query_params.get("end_date")
                )
            )

        if not query["$and"]:
            raise HTTPException(status_code=400, detail="No query to filter!")
    else:
        append_query(search_titles(terms, "$or"))
        append_query(search_genres(terms, "$and"))
        append_query(search_overviews(terms, "$and"))
        append_query(search_directors(terms, "$or"))
        append_query(search_actors(terms, "$and"))

        if not query["$or"]:
            raise HTTPException(status_code=400, detail="No query!")

    # mod_value 설정
    contentype = request.query_params.get("contentype")
    if contentype:
        mod_query = {"id": {"$mod": [2, 1]}} if contentype == "1" else {"id": {"$mod": [2, 0]}}
        append_query(mod_query)

    # 전체 문서 수 조회
    total_count = await mongo_conn.content.media.count_documents(query)

    # 페이지네이션
    skip = (page - 1) * page_size
    projection = {"_id": 0}
    results = mongo_conn.content.media.find(query, projection).skip(skip).limit(page_size)

    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size,
        "results": await results.to_list(length=page_size),
    }
