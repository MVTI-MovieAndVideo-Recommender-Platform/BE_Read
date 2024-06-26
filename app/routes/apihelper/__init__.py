import base64
import json
import os
import uuid
from datetime import datetime

from pymongo.errors import CollectionInvalid, PyMongoError, ServerSelectionTimeoutError

with open(
    f"{os.path.dirname(os.path.abspath(__file__))}/keyword_content_indices.json",
    "r",
    encoding="utf-8-sig",
) as file:
    keyword_content = json.load(file)


def base64_to_uuid(b64_str: str) -> str:
    # Base64 문자열의 패딩을 복원
    padding = "=" * (4 - len(b64_str) % 4)
    b64_str += padding

    # Base64 문자열을 바이트로 디코딩
    uuid_bytes = base64.urlsafe_b64decode(b64_str)

    # 디코딩한 바이트를 UUID 객체로 변환
    return str(uuid.UUID(bytes=uuid_bytes))


def uuid_to_base64(u: uuid.UUID) -> str:
    # UUID를 바이트로 변환하고 Base64로 인코딩
    return base64.urlsafe_b64encode(u.bytes).rstrip(b"=").decode("utf-8")


def model_to_dict(model_instance):
    data = {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data


# 개별 태스크 실행 및 예외 처리 함수
async def execute_task(task, task_name):
    try:
        result = await task
        return result
    except (CollectionInvalid, ServerSelectionTimeoutError, PyMongoError) as e:
        print(f"Error in {task_name}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error in {task_name}: {str(e)}")
        return None
