import asyncio
from pathlib import Path

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    try:
        session = await client.create_session(
            model="auto",
            tools={"available_tools": []},
        )

        response = await session.send_and_wait(
            "My project is named TaskTrack. "
            "It helps a team assign tasks and track deadlines. "
            "Summarize this in one sentence."
        )

        if response and isinstance(response.data, AssistantMessageData):
            print(response.data.content)

        id_file = Path(__file__).with_name("saved_session_id.txt")
        id_file.write_text(session.session_id, encoding="utf-8")

        print("\nSaved session ID:", session.session_id)

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())