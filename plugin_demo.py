import asyncio
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    plugin_folder = str(
        Path(__file__).parent / "plugins" / "email-helper"
    )

    session = await client.create_session(
        model="auto",
        permissions={"on_request": PermissionHandler.approve_all},
        plugins={
            "directories": [plugin_folder],
        },
        skills={
            "enabled": True,
        },
    )

    response = await session.send_and_wait(
        """
Use the short-email skill from the email-helper plugin.

Write an email to my manager asking to move our meeting
from 2 PM to 3 PM today because of a training session.

My name is Narendar.
"""
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())