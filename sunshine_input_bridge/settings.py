from enum import Enum
from typing import Optional

from pydantic import BaseModel, BaseSettings


class OutputDeviceType(str, Enum):
    keyboard = "keyboard"
    mouse = "mouse"
    gamepad = "gamepad"


class OutputSetting(BaseModel):
    name: str
    type: OutputDeviceType
    vendor: Optional[int]
    product: Optional[int]
    version: Optional[int]
    phys: Optional[str]
    bustype: Optional[str]


class InputSetting(BaseModel):
    name: Optional[str]
    vendor: Optional[int]
    product: Optional[int]
    device_node: Optional[str]


class InputMapping(BaseModel):
    input: str
    output: str

    def __hash__(self):
        return hash((self.input, self.output))

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, InputMapping)
            and self.input == __value.input
            and self.output == __value.output
        )


class Settings(BaseSettings):
    outputs: dict[str, OutputSetting]
    inputs: dict[str, InputSetting]
    mappings: list[InputMapping]

    class Config:
        fields = {}
        env_file_encoding = "utf-8"
