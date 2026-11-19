import asyncio
from pathlib import Path

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData


async def main():
    trace_file = str(Path(__file__).with_name("traces.jsonl"))

    client = CopilotClient(
        mode="coding-agent",
        observability={
            "telemetry": {
                "exporter_type": "file",
                "file_path": trace_file,
                "capture_content": False,
            }
        },
    )

    await client.start()

    session = await client.create_session(
        model="auto",
        tools={"available_tools": []},
    )

    response = await session.send_and_wait(
        "Explain the difference between a Python list and a tuple "
        "using one short example of each."
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()

    print(f"\nTrace output location: {trace_file}")


if __name__ == "__main__":
    asyncio.run(main())