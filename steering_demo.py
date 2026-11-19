import asyncio

from copilot import CopilotClient
from copilot.session_events import SessionEventType


def handle_event(event):
    if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        print(event.data.delta_content or "", end="", flush=True)


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    try:
        session = await client.create_session(
            model="auto",
            tools={"available_tools": []},
            events={"streaming": True},
        )

        session.on(handle_event)

        print("Sending the original task...")

        await session.send(
            "Explain Python file handling in detail, including "
            "reading, writing, appending, and several examples."
        )

        print("Sending a steering instruction...\n")

        await session.send_and_wait(
            "Change the explanation to three short bullet points. "
            "Include only one example of reading a text file.",
            mode="immediate",
        )

        print()

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())