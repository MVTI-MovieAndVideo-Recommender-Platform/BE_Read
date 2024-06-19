from fastapi import APIRouter
from routes.api import (
    get_info_route,
    get_search_route,
    random_top_rank_route,
    re_random_top_rank_route,
)

search_router = APIRouter(tags=["Search"])
top_rank_router = APIRouter(tags=["TopRank"])

search_router.routes.append(get_search_route)
search_router.routes.append(get_info_route)

top_rank_router.routes.append(random_top_rank_route)
top_rank_router.routes.append(re_random_top_rank_route)
# search_router.routes.append(get_search_route2)
