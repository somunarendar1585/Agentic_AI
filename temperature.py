import asyncio

from copilot import CopilotClient, define_tool
from copilot.session_events import AssistantMessageData
from pydantic import BaseModel, Field


# Define the tool's input.
class TemperatureParams(BaseModel):
    celsius: float = Field(description="Temperature in degrees Celsius")


# Define the function Copilot can call.
@define_tool(
    description="Convert Celsius to Fahrenheit.",
    skip_permission=True,
    defer="never",
)
async def convert_temperature(params: TemperatureParams) -> dict:
    print(f"Tool called with {params.celsius} Celsius")

    fahrenheit = (params.celsius * 9 / 5) + 32
    return {"fahrenheit": fahrenheit}


async def main():
    client = CopilotClient(mode="coding-agent")
    await client.start()

    # Register the tool with the session.
    session = await client.create_session(
        model="auto",
        tools={"definitions": [convert_temperature]},
    )

    response = await session.send_and_wait(
        "Use convert_temperature to convert 30 degrees Celsius to Fahrenheit."
    )

    if response and isinstance(response.data, AssistantMessageData):
        print(response.data.content)

    await session.disconnect()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())