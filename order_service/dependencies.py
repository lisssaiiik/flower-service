import requests
from fastapi import HTTPException, Request


def get_current_user(request: Request):   
    access_token = request.cookies.get("flower_access_token")
    headers = {'accept': 'application/json', 'token': access_token}
    response = requests.get('http://127.0.0.1:8000/auth/me', headers=headers, timeout=10)
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Not authorized")
    return response.json()