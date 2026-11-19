import asyncio

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    session = await client.create_session(
        model="auto",
        tools={"available_tools": []},
        system_message={
            "mode": "append",
            "content": """
            You are a Python tutor helping a beginner.
            Use simple English.
            Keep explanations under 100 words.
            Include one short Python code example.
            Finish with one practice question.
            """,
        },
    )

    response = await session.send_and_wait(
        "Explain how a Python for functions works."
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())