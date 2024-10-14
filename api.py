import enum
from typing import Annotated
from livekit.agents import llm
import logging

logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)

class Zone(enum.Enum):
    LIVING_ROOM = "living_room",
    KITCHEN = "kitchen",
    BEDROOM = "bedroom",
    BATHROOM = "bathroom",
    OFFICE = "office"

class AssistantFnc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()

        self._temperature = {
            Zone.LIVING_ROOM: 22,
            Zone.KITCHEN: 21,
            Zone.BEDROOM: 23,
            Zone.BATHROOM: 24,
            Zone.OFFICE: 25
        }

    @llm.ai_callable(description="get the temperature in a specific room")
    def get_temperature(self, zone: Annotated[Zone, llm.TypeInfo(description="The specific zone")]
    ):
        logger.info("get temp - zone %s", zone)
        temp = self._temperature[Zone(zone)]
        return f"The temperature in {zone} is {temp}°C"

    @llm.ai_callable(description="set the temperature in a specific room")
    def set_temperature(self, zone: Annotated[Zone, llm.TypeInfo(description="The specific zone")], temp: Annotated[int, llm.TypeInfo(description="The temperature to set")]
    ):
        logger.info("set temp - zone %s, temp: %s", zone, temp)
        self._temperature[Zone(zone)] = temp
        return f"The temperature in the {zone} is now {temp}C"