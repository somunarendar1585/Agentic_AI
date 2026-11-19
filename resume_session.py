import asyncio
from pathlib import Path

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData


async def main():
    id_file = Path(__file__).with_name("saved_session_id.txt")
    session_id = id_file.read_text(encoding="utf-8").strip()

    client = CopilotClient(mode="coding-agent")
    await client.start()

    try:
        session = await client.resume_session(
            session_id,
            tools={"available_tools": []},
        )

        response = await session.send_and_wait(
            "What is my project's name and what does it do?"
        )

        if response and isinstance(response.data, AssistantMessageData):
            print(response.data.content)

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())