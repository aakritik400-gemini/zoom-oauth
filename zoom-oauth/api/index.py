from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import base64
import os

app = FastAPI()

CLIENT_ID = os.environ["ZOOM_CLIENT_ID"]
CLIENT_SECRET = os.environ["ZOOM_CLIENT_SECRET"]
REDIRECT_URI = os.environ["ZOOM_REDIRECT_URI"]


@app.get("/login")
def login():
    url = (
        "https://zoom.us/oauth/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url)


@app.get("/callback")
def callback(code: str):
    auth_header = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    ).decode()

    token_res = requests.post(
        "https://zoom.us/oauth/token",
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
    )
    token_res.raise_for_status()
    token_data = token_res.json()

    access_token = token_data["access_token"]

    user_res = requests.get(
        "https://api.zoom.us/v2/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_res.raise_for_status()

    return JSONResponse({
        "user": user_res.json(),
        "token": token_data
    })
