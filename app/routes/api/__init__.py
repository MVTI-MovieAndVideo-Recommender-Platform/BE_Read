from fastapi.routing import APIRoute
from routes.api.search_api import get_search

get_search_route = APIRoute(path="/search", endpoint=get_search, methods=["GET"])
