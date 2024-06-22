from fastapi import HTTPException, Request
from routes.apihelper import base64_to_uuid
from routes.apihelper.user_apihelper import get_matching_data


async def get_user_info(request: Request):
    try:
        if request.state.token and (user_id := base64_to_uuid(request.state.token)):
            print(user_id)
            user_info = await get_matching_data(user_id)
            print("user_info", user_info)
            return user_info
        else:
            raise HTTPException(status_code=404, detail="No User found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
