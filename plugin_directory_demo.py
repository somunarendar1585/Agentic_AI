import asyncio
from pathlib import Path

from copilot import CopilotClient, SpawnedStdioRuntimeConnection
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData


async def main():
    plugin_folder = str(
        Path(__file__).resolve().parent / "plugins" / "code-reviewer"
    )

    client = CopilotClient(
        mode="coding-agent",
        runtime=SpawnedStdioRuntimeConnection(  #asks the SDK to start a runtime process and communicate through its standard input and output.
            args=("--plugin-dir", plugin_folder),  # --plugin-dir => tells that runtime which plugin folder to load.
        ),
    )

    await client.start()

    session = await client.create_session(
        model="auto",
        permissions={"on_request": PermissionHandler.approve_all},
        skills={"enabled": True},
    )

    response = await session.send_and_wait(
        """
Use the lint-fix skill from the code-reviewer plugin
to review this Python code:

def square(number):
    return number * 2

print(square(5))

The function should calculate the square of the number.
"""
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())