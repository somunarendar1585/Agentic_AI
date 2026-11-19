import asyncio

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

        prompt = "What is 2 + 2? Reply with only the number."
        response = await session.send_and_wait(prompt)

        if response is None or not isinstance(response.data, AssistantMessageData):
            raise RuntimeError("Copilot did not return a text reply.")

        print(f"Copilot: {response.data.content}")
    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())