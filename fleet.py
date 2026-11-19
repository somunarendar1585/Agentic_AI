import asyncio

from copilot import CopilotClient
from copilot.rpc import FleetStartRequest     #	Holds the task sent to Fleet Mode.
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    finished = asyncio.Event()  # Keeps the application waiting for the session to become idle.

    def handle_event(event):
        event_name = event.type.value

        if event_name in (
            "subagent.started",   #	Help you observe worker activity.
            "subagent.completed",
            "subagent.failed",
        ):
            print(f"[Event] {event_name}", flush=True)

        if not event.agent_id:
            if isinstance(event.data, AssistantMessageData):
                print("\nParent response:")
                print(event.data.content)

            if event_name == "session.idle":
                finished.set()

    try:
        session = await client.create_session(
            model="auto",
            permissions={"on_request": PermissionHandler.approve_all},
        )

        session.on(handle_event)

        result = await session.rpc.fleet.start(    # Requests fleet orchestration.
            FleetStartRequest(
                prompt="""
Use two parallel sub-agents for these independent tasks.

Task 1:
Write three manual test cases for login.
Valid credentials open the dashboard.
Invalid credentials display an error.
Both input fields are mandatory.

Task 2:
Write three manual test cases for search.
A matching query returns matching items.
An unmatched query displays "No results".
An empty query displays "Enter a search term".

Each test case needs a scenario and expected result.
Return the combined results under Login and Search headings.
"""
            )
        )

        print("Fleet started:", result.started)  # 	Reports whether Fleet Mode started.

        if result.started:
            await asyncio.wait_for(finished.wait(), timeout=180)  # Limits how long this example waits.

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())