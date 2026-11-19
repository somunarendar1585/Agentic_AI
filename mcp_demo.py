import asyncio
import sys
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    server_path = str(Path(__file__).with_name("book_server.py"))

    session = await client.create_session(
        model="auto",
        permissions={"on_request": PermissionHandler.approve_all},
        mcp={
            "servers": {
                "books": {
                    "type": "stdio",
                    "command": sys.executable,
                    "args": [server_path],
                    "tools": ["check_book"],
                }
            }
        },
    )

    response = await session.send_and_wait(
        "Look up both books and return one result per line:\n"
        "Learning SQL should return Borrowed.\n"
        "Learning Java should return Book not found."
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


asyncio.run(main())