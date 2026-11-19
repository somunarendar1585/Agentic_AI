import asyncio

from copilot import CopilotClient
from copilot.session_events import SessionEventType


def handle_event(event):
    if event.type == SessionEventType.ASSISTANT_TURN_START:
        print("\n[Event] Copilot started a turn.", flush=True)

    elif event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        print(event.data.delta_content or "", end="", flush=True)

    elif event.type == SessionEventType.ASSISTANT_MESSAGE:
        print("\n[Event] Complete assistant message received.", flush=True)

    elif event.type == SessionEventType.SESSION_IDLE:
        print("[Event] Session is idle.", flush=True)


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

        await session.send_and_wait(
            "Write a Python countdown from 5 to 1 using a while loop. "
            "Explain each step and show the expected output."
        )

        print("\nThe request finished.")

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())