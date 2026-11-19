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
            execution={
                "limits": {
                    "max_ai_credits": 30,
                }
            },
        )

        print("Session created with a 30 AI Credits soft cap.")

        response = await session.send_and_wait(
            "Explain Python exception handling using a short "
            "example that handles invalid number input."
        )

        if response and isinstance(response.data, AssistantMessageData):
            print("\nCopilot response:")
            print(response.data.content)

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())