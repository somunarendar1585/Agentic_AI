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
                You help beginners understand programming errors.
                For every answer, use these three sections:
                1. Cause
                2. Correction
                3. Corrected code
                After the corrected code, include its expected output.
                Use simple English and keep the explanation brief.
                """,
        },
    )

    response = await session.send_and_wait(
        """
            Explain the error in this Python code:

            age = "25"
            next_year_age = age + 1
            print(next_year_age)

        """
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())