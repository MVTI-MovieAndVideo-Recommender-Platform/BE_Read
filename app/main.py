from auth.jwt import verify_access_token
from fastapi import Depends, FastAPI, Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from routes import search_router, top_rank_router
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class DataValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        jwt = request.headers.get("jwt", None)
        # jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6Ii1aNG1XUG1WV3RTU0VzUFJyR29iRGciLCJwcm92aWRlciI6Im5hdmVyIn0.1zyu3hVQp4Ql_X6KIIMCHrYKxc2ZW0K0HIVnqlmm_6U"
        # jwt = ""
        print(jwt)
        if jwt:
            # 기타 검증 로직을 여기에 추가할 수 있습니다.
            # 검증이 통과하면 다음 미들웨어 또는 요청 핸들러로 넘어갑니다.
            request.state.token = (
                decode_jwt
                if (decode_jwt := (await verify_access_token(jwt)).get("token"))
                else None
            )
            print("request.state.token -> ", request.state.token)
        else:
            request.state.token = None
        # # print(request.query_params.getlist("media_id[]"))
        response = await call_next(request)
        return response


app = FastAPI(root_path="/info")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)
app.add_middleware(DataValidationMiddleware)
app.include_router(search_router, prefix="")
app.include_router(top_rank_router, prefix="")


# 예외 처리
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


# 예외 처리
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/")
def test():
    return "Hello this is mvti read server"
