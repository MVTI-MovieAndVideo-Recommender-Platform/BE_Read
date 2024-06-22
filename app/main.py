from typing import Union

from database import settings
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from routes import router
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware


# jwt 토큰을 검증하는 함수 -> 디코드된 토큰을 반환한다
async def verify_access_token(_jwt: str) -> Union[dict, None]:
    try:
        # JWT 토큰의 최소 길이(헤더, 페이로드, 서명)를 확인합니다.
        if len(_jwt) < 152:  # 실제 필요한 최소 길이로 변경해야 합니다.
            raise HTTPException(status_code=400, detail="토큰 길이가 유효하지 않습니다.")
        # 토큰을 decode한 값을 data에 저장합니다.
        decode_jwt = jwt.decode(_jwt, settings.SERVER_SECRET_KEY, algorithms="HS256")
        return decode_jwt if decode_jwt else None
    except JWTError:
        raise HTTPException(status_code=400, detail="디코딩이 불가합니다.")


class DataValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 기타 검증 로직을 여기에 추가할 수 있습니다.
        # 검증이 통과하면 다음 미들웨어 또는 요청 핸들러로 넘어갑니다.
        try:
            if jwt_token := request.headers.get("jwt", None):
                decode_jwt = await verify_access_token(jwt_token)
                request.state.token = (
                    decode_jwt.get("token") if decode_jwt and decode_jwt.get("token") else None
                )
            else:
                request.state.token = None
        except HTTPException as e:
            # HTTPException 발생 시, 적절한 에러 응답을 반환합니다.
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        print("request.state.token -> ", request.state.token)
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
app.include_router(router, prefix="")


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
