import os
import secrets
from urllib.parse import urlencode

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware


load_dotenv()

CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]
CLIENT_SECRET = os.environ["GITHUB_CLIENT_SECRET"]
CALLBACK_URL = "http://127.0.0.1:8000/auth/callback"

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_hex(32),
    same_site="lax",
)


@app.get("/")
async def home():
    return {"message": "Open /login to sign in with GitHub."}


@app.get("/login")
async def login(request: Request):
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state

    parameters = {
        "client_id": CLIENT_ID,
        "redirect_uri": CALLBACK_URL,
        "scope": "read:user",
        "state": state,
    }

    url = "https://github.com/login/oauth/authorize?"
    return RedirectResponse(url + urlencode(parameters))


@app.get("/auth/callback")
async def callback(request: Request):
    expected_state = request.session.pop("oauth_state", None)
    returned_state = request.query_params.get("state", "")

    if not expected_state or not secrets.compare_digest(
        expected_state, returned_state
    ):
        raise HTTPException(400, "Invalid login state. Open /login again.")

    code = request.query_params.get("code")

    if not code:
        raise HTTPException(400, "GitHub authorization was not completed.")

    async with httpx.AsyncClient(timeout=30) as http:
        token_response = await http.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": CALLBACK_URL,
            },
        )

        if token_response.status_code != 200:
            raise HTTPException(502, "GitHub token exchange failed.")

        access_token = token_response.json().get("access_token")

        if not access_token:
            raise HTTPException(400, "GitHub did not issue an access token.")

        user_response = await http.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
        )

        if user_response.status_code != 200:
            raise HTTPException(502, "Could not retrieve the GitHub user.")

        user = user_response.json()

        client = CopilotClient(
        mode="coding-agent",
        github={
            "token": access_token,
            "use_logged_in_user": False,
        },
    )

    try:
        await client.start()

        session = await client.create_session(
            model="auto",
            tools={"available_tools": []},
        )

        response = await session.send_and_wait(
            "Explain Python functions using a short example "
            "that calculates the area of a rectangle."
        )

        if response and isinstance(response.data, AssistantMessageData):
            return {
                "message": "GitHub login and Copilot request successful.",
                "username": user["login"],
                "answer": response.data.content,
            }

        raise HTTPException(
            status_code=502,
            detail="Copilot did not return a text response.",
        )

    finally:
        await client.stop()