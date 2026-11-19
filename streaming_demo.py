import asyncio

from copilot import CopilotClient
# from copilot.session_events import AssistantMessageDeltaData
from copilot.session_events import SessionEventType

def handle_event(event):
    if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        print(event.data.delta_content or "", end="", flush=True)


async def main():
    client = CopilotClient(mode="coding-agent")
    session = None

    try:
        await client.start()
        print("Copilot client started.")

        session = await client.create_session(
            model="auto",
            tools={"available_tools": []},
            events={"streaming": True},
        )
        print("Session created successfully.")

        session.on(handle_event)

        prompt = prompt = """
            Write a Python function that counts how often each word appears in a sentence.

            Use this sentence:
            "Python is useful and Python is easy to learn"

            Ignore letter case and return a dictionary.
            Explain the solution step by step and show the expected output.
            """

        print("\nCopilot response:")
        await session.send_and_wait(prompt)
        print()

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