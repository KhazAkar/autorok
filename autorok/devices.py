from dataclasses import dataclass
import typing

@dataclass
class Device:
    driver: str
    analog_ch: typing.Union[typing.Sequence[str], None] = None 
    digital_ch: typing.Union[typing.Sequence[str], None] = None 
    available_options: typing.Union[typing.Sequence[str], None] = None 
    
    def __iter__(self):
        return iter((self.driver, self.analog_ch, self.digital_ch, self.available_options))

device_map = {'demo': Device('demo', ['A0', 'A1', 'A2', 'A3', 'A4'],
    ['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'])}


