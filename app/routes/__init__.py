from fastapi import APIRouter
from routes.api import get_search_route

search_router = APIRouter(tags=["Search"])

search_router.routes.append(get_search_route)
