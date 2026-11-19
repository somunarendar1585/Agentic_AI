from copilot import CopilotClient
from copilot.session_events import AssistantMessageData
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()             	# Creates the web application.


class PromptRequest(BaseModel):                 # Defines the incoming JSON, which must contain a nonempty prompt string.
    prompt: str = Field(min_length=1)


@app.post("/ask")                                 #	Handles POST requests sent to /ask.
async def ask_copilot(request: PromptRequest):
    client = CopilotClient(mode="coding-agent")
    await client.start()

    try:
        session = await client.create_session(
            model="auto",
            tools={"available_tools": []},
        )

        response = await session.send_and_wait(request.prompt)   # Reads the prompt supplied by the caller   

        if response and isinstance(response.data, AssistantMessageData):
            return {"answer": response.data.content}                 # Returns Copilot’s answer as JSON

        raise HTTPException(
            status_code=502,
            detail="Copilot did not return a text response.",
        )
    finally:
        await client.stop()

