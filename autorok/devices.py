from dataclasses import dataclass
import typing

__all__ = ['Device']


@dataclass(repr=False)
class Device:
    """
    Dataclass containing metadata about measurement device, used in device_map dict, which indicates currently supported
    measurement devices.
    """
    driver: str
    port: str = ""
    analog_ch: typing.Union[typing.Sequence[str], None] = None
    digital_ch: typing.Union[typing.Sequence[str], None] = None
    available_options: typing.Union[typing.Sequence[str], None] = None

    def __repr__(self):
        return f"Device driver: {self.driver} on {self.port if self.port else 'NULL Port'}"


device_map = {
    'demo':
    Device('demo', "", ['A0', 'A1', 'A2', 'A3', 'A4'],
           ['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']),
    'dreamsourcelab-dslogic':
    Device('dreamsourcelab-dslogic', "", None, [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
        '13', '14', '15'
    ]),
    'brymen-bmXXX-dmm':
    Device('serial-dmm', "", [""], [""])
}
