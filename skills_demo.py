import asyncio
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    skills_folder = str(Path(__file__).parent / "skills")

    session = await client.create_session(
        model="auto",
        permissions={"on_request": PermissionHandler.approve_all},
        skills={
            "enabled": True,
            "directories": [skills_folder],
        },
    )

    response = await session.send_and_wait(
        """
Use the work-update skill to rewrite these notes:

fixed login bug
tested password reset
updated setup instructions
"""
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())