import asyncio
import webbrowser

from copilot import CopilotClient
from copilot.rpc import RemoteEnableRequest, RemoteSessionMode
from copilot.session_events import AssistantMessageData


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    try:
        session = await client.create_session(
            model="auto",
            tools={"available_tools": []},
        )

        response = await session.send_and_wait(
            "Suggest three features for a simple expense-tracking app."
        )

        if response and isinstance(response.data, AssistantMessageData):
            print(response.data.content)

            result = await session.rpc.remote.enable(
            RemoteEnableRequest(mode=RemoteSessionMode.EXPORT)
        )

        print("\nExport started:", result.started)
        print("Remote URL:", result.url)
        print("Warning:", result.warning)

        if result.url:
            print("\nGitHub session URL:", result.url)
            webbrowser.open(result.url)

            await asyncio.to_thread(
                input,
                "\nReview the session, then press Enter here...",
            )
        else:
            print("\nThe runtime did not return a remote-session URL.")

        await session.rpc.remote.disable()
        print("Session history export stopped.")


    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())