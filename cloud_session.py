import asyncio

from copilot import (
    CloudSessionOptions,
    CloudSessionRepository,
    CopilotClient,
    RuntimeConnection,
)
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(
        mode="coding-agent",
        runtime=RuntimeConnection.for_spawned_stdio(),
    )

    try:
        await client.start()
        print("Starting the cloud session...")

        session = await client.create_session(
            cloud=CloudSessionOptions(
                repository=CloudSessionRepository(
                    owner="somunarendar1585",
                    name="Agentic_AI",
                    branch="main",
                )
            ),
            permissions={"on_request": PermissionHandler.approve_all},
        )

        print("Cloud session connected.")
        print("Session ID:", session.session_id)

        response = await session.send_and_wait(
            "Perform a read-only review of README.md. "
            "Summarize the project's purpose in three bullet points."
        )

        if response and isinstance(response.data, AssistantMessageData):
            print("\nCopilot response:")
            print(response.data.content)

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())