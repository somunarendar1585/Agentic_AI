import asyncio
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    skill_folder = str(
        Path(__file__).parent / "skills" / "meeting-summary"
    )

    session = await client.create_session(
        model="auto",
        permissions={"on_request": PermissionHandler.approve_all},
        skills={
            "enabled": True,
            "directories": [skill_folder],
        },
    )

    response = await session.send_and_wait(
        """
Use the meeting-summary skill to summarize these notes:

The team decided to release the login update on Friday.
Ravi will finish testing by Thursday.
Sita will update the user guide.
"""
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())