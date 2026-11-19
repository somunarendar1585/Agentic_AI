import asyncio

from copilot import CopilotClient, RuntimeConnection
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(
        mode="coding-agent",
        runtime=RuntimeConnection.for_tcp("127.0.0.1", 4321),
    )

    await client.start()
    print("Connected to the external Copilot server.")

    session = await client.create_session(
        model="auto",
        tools={"available_tools": []},
    )

    response = await session.send_and_wait(
        "Explain Python list slicing using one short example."
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()
    print("Python client disconnected.")


if __name__ == "__main__":
    asyncio.run(main())