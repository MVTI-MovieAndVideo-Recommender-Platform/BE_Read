from fastapi import APIRouter
from routes.api import (
    get_info_route,
    get_search_route,
    get_this_week_top_media_route,
    get_user_info_route,
    random_keyword_content_route,
    random_top_rank_route,
    re_random_top_rank_route,
)

router = APIRouter(tags=["ReadServer"])

router.routes.append(get_user_info_route)
router.routes.append(get_search_route)
router.routes.append(get_info_route)
router.routes.append(random_top_rank_route)
router.routes.append(re_random_top_rank_route)
router.routes.append(random_keyword_content_route)
router.routes.append(get_this_week_top_media_route)


# search_router = APIRouter(tags=["Search"])
# top_rank_router = APIRouter(tags=["TopRank"])

# search_router.routes.append(get_search_route)
# search_router.routes.append(get_info_route)

# top_rank_router.routes.append(random_top_rank_route)
# top_rank_router.routes.append(re_random_top_rank_route)
# top_rank_router.routes.append(get_this_week_top_media_route)
# search_router.routes.append(get_search_route2)
