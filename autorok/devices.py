from dataclasses import dataclass

@dataclass
class Device:
    driver: str
    available_channels: tuple
    active_channels: list
    options: list

DSLogicPlus = Device("dreamsourcelab-dslogic", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), [0, 1, 2, 3, 4,
    5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [""])

Demo = Device("demo", ("A0", "A1", "A2", "A3", "A4", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7"), ["A0", "A1", "A2",
    "A3", "A4", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7"], [""])
