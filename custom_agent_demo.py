import asyncio

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    session = await client.create_session(
        model="auto",
        tools={"available_tools": []},
        agents={
            "definitions": [
                {
                    "name": "python-reviewer",
                    "description": "Reviews short Python code for beginners.",
                    "prompt": """
                        You are a Python code reviewer.
                        Find the main mistake in the supplied code.
                        Explain it in simple English.
                        Show the corrected code.
                        Keep your answer brief.
                        """,
                    "tools": [],
                }
            ],
            "selected": "python-reviewer",
        },
    )

    response = await session.send_and_wait(
        """
            def greet(name):
                print("Hello", name)

                message = greet("Narendar")
                print(message.upper())
            """
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())