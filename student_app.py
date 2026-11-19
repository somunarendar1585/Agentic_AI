import asyncio
import sys
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    server_path = str(
        Path(__file__).with_name("student_server.py")
    )

    session = await client.create_session(
        model="auto",
        permissions={"on_request": PermissionHandler.approve_all},
        mcp={
            "servers": {
                "students": {
                    "type": "stdio",
                    "command": sys.executable,
                    "args": [server_path],
                    "tools": ["get_student_marks"],
                }
            }
        },
    )

    response = await session.send_and_wait(
        "Use the students MCP server's get_student_marks tool "
        "to find Ravi's marks. Answer using the returned data."
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())