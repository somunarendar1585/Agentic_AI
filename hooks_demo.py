import asyncio

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData


async def on_prompt_submitted(input_data, invocation):
    print("\n[Hook] A prompt was submitted.")
    print("[Hook] Prompt:", input_data["prompt"])
    return None


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    session = await client.create_session(
        model="auto",
        tools={"available_tools": []},
        hooks={
            "handlers": {
                "on_user_prompt_submitted": on_prompt_submitted,
            }
        },
    )

    response = await session.send_and_wait(
        "Write a Python function that finds the largest number "
        "in a nonempty list. Explain it briefly."
    )

    if response and isinstance(response.data, AssistantMessageData):
        print("\nCopilot response:")
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())