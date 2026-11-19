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
            "definitions": [                     # 	Contains the custom agent configuration.
                {
                    "name": "python-error-helper",
                    "description": "Explains Python errors to beginners.",
                    "prompt": """                                                     # Gives the agent instructions about how to answer.
                                You help beginners understand Python errors.
                                Use simple English.
                                Organize each answer into:
                                1. Problem
                                2. Reason
                                3. Corrected code
                                Keep the explanation brief.
                                """,
                    "tools": [],                       # 	Configures the agent with an empty tool list.
                }
            ],
            "selected": "python-error-helper",          # Chooses this agent to handle the conversation.
        },
    )

    response = await session.send_and_wait(
        """
            Explain the problem in this code:

            numbers = [10, 20, 30]
            print(numbers[3])

        """
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())