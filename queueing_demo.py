import asyncio

from copilot import CopilotClient
from copilot.session_events import SessionEventType


def handle_event(event):
    if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        print(event.data.delta_content or "", end="", flush=True)

    elif event.type == SessionEventType.ASSISTANT_MESSAGE:
        print("\n--- Assistant message finished ---\n", flush=True)


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

        print("Submitting the first task...")

        await session.send(
            "Start your answer with 'TASK 1'. "
            "Explain Python's sorted() function in four short points."
        )

        print("Submitting the follow-up task...\n")

        await session.send_and_wait(
            "Start your answer with 'TASK 2'. "
            "Now provide two short sorted() examples: "
            "one for numbers and one for words.",
            mode="enqueue",
        )

        print("\nFinished waiting for the follow-up task.")

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())