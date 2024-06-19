from database import settings
from jose import JWTError, jwt


# jwt 토큰을 검증하는 함수 -> 디코드된 토큰을 반환한다
async def verify_access_token(_jwt: str) -> str:
    try:
        # 토큰을 decode한 값을 data에 저장한다.
        # 이 단계에서 decode되지 않으면 당연히 검증된 토큰이 아니다.
        return jwt.decode(_jwt, settings.SERVER_SECRET_KEY, algorithms="HS256")
    except JWTError:
        raise ValueError("디코딩 이 불가합니다.")
