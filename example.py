import asyncio

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    session = None

    try:
        await client.start()
        print("Copilot client started.")

        session = await client.create_session(
            model="auto",
            tools={"available_tools": []},
        )
        print("Session created successfully.")

        prompt = prompt = """
            Write a Python program that separates a list of integers into even and odd numbers.

            Use this list:
            [12, 7, 9, 24, 0, -3, -8, 15, 20]

            Requirements:
            - Create a function named separate_even_odd(numbers).
            - Return two lists containing the even and odd numbers.
            - Use a loop and the modulo operator.
            - Print both lists.
            - Briefly explain the logic and show the expected output.
            """

        print("Sending the requirement to Copilot...")
        response = await session.send_and_wait(prompt)

        print("\nCopilot response:")
        if response and isinstance(response.data, AssistantMessageData):
            print(response.data.content)
        else:
            raise RuntimeError("Copilot completed without returning a text reply.")

    finally:
        try:
            if session is not None:
                await session.disconnect()
                print("\nSession disconnected.")
        finally:
            await client.stop()
            print("Copilot client stopped.")


if __name__ == "__main__":
    asyncio.run(main())