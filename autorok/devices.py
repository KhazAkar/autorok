from dataclasses import dataclass
import typing


@dataclass
class Device:
    driver: str
    port: str = ""
    analog_ch: typing.Union[typing.Sequence[str], None] = None
    digital_ch: typing.Union[typing.Sequence[str], None] = None
    available_options: typing.Union[typing.Sequence[str], None] = None


device_map = {
    'demo': Device('demo', "", ['A0', 'A1', 'A2', 'A3', 'A4'],
                   ['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']),
    'dreamsourcelab-dslogic': Device('dreamsourcelab-dslogic', "", None,
                                     ['0', '1', '2', '3', '4', '5', '6', '7',
                                      '8', '9', '10', '11', '12', '13', '14', '15'])
}
