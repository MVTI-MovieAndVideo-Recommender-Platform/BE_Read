from fastapi.routing import APIRoute
from routes.api.detail_api import detail_func
from routes.api.search_api import get_search
from routes.api.toprank_api import (
    get_top_rank_random_contents,
    re_get_top_rank_random_contents,
)

random_top_rank_route = APIRoute(
    path="/rank_random_20", endpoint=get_top_rank_random_contents, methods=["GET"]
)
re_random_top_rank_route = APIRoute(
    path="/re_rank_random_20", endpoint=re_get_top_rank_random_contents, methods=["GET"]
)
get_search_route = APIRoute(path="/search", endpoint=get_search, methods=["GET"])

get_info_route = APIRoute(path="/media/{id}", endpoint=detail_func, methods=["GET"])
