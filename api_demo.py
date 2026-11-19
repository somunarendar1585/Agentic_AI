from copilot import CopilotClient
from copilot.session_events import AssistantMessageData
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str = Field(min_length=1)


@app.post("/ask")
async def ask_copilot(request: PromptRequest):
    client = CopilotClient(mode="coding-agent")
    await client.start()

    try:
        session = await client.create_session(
            model="auto",
            tools={"available_tools": []},
        )

        response = await session.send_and_wait(request.prompt)

        if response and isinstance(response.data, AssistantMessageData):
            return {"answer": response.data.content}

        raise HTTPException(
            status_code=502,
            detail="Copilot did not return a text response.",
        )
    finally:
        await client.stop()