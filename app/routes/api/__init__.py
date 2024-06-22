from fastapi.routing import APIRoute
from routes.api.detail_api import detail_endpoint
from routes.api.search_api import get_search
from routes.api.toprank_api import (
    get_random_keyword_content,
    get_this_week_media_rank,
    get_top_rank_random_contents,
    re_get_top_rank_random_contents,
)
from routes.api.user_api import get_user_info

random_top_rank_route = APIRoute(
    path="/rank_random_20", endpoint=get_top_rank_random_contents, methods=["GET"]
)
re_random_top_rank_route = APIRoute(
    path="/re_rank_random_20", endpoint=re_get_top_rank_random_contents, methods=["GET"]
)
random_keyword_content_route = APIRoute(
    path="/random_keyword_content", endpoint=get_random_keyword_content, methods=["GET"]
)
get_search_route = APIRoute(path="/search", endpoint=get_search, methods=["GET"])

get_info_route = APIRoute(path="/media/{id}", endpoint=detail_endpoint, methods=["GET"])

get_this_week_top_media_route = APIRoute(
    path="/weekly", endpoint=get_this_week_media_rank, methods=["GET"]
)

get_user_info_route = APIRoute(path="/mypage", endpoint=get_user_info, methods=["GET"])
