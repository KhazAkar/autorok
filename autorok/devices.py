from dataclasses import dataclass, field
import typing

@dataclass
class Device:
    driver: str
    analog_ch: typing.Union[typing.Sequence[str], None] = None 
    digital_ch: typing.Union[typing.Sequence[str], None] = None 
    available_options: typing.Union[typing.Sequence[str], None] = None 
    
    def __iter__(self):
        return iter((self.driver, self.analog_ch, self.digital_ch, self.available_options))

device_map = {'demo': Device('demo')}


