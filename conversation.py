import asyncio

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    session = await client.create_session(
        model="auto",
        tools={"available_tools": []},
    )

    response = await session.send_and_wait(
        "My shopping list contains rice, milk, and apples. "
        "Repeat the list."
    )

    if response and isinstance(response.data, AssistantMessageData):
        print("First response:")
        print(response.data.content)

    response = await session.send_and_wait(
        "Remove milk and add bread. Show my updated shopping list."
    )

    if response and isinstance(response.data, AssistantMessageData):
        print("\nFollow-up response:")
        print(response.data.content)

    await session.disconnect()
    await client.stop()


asyncio.run(main())