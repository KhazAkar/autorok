from pathlib import Path
import typing
import configparser
import enum

class Destination(enum.Enum):
    STDOUT = "stdout"
    FILE = "file"

class Log:
    def __init__(self):
        self.status: bool = None
        self.output_dst: Destination = None 
        self.live_cfg: typing.Dict[str] = {}
        self.file_cfg: Path = Path()
        self.__cfg_parser = configparser.ConfigParser()

    def __preconfigure(self):
        self.file_cfg = Path('.')
        self.live_cfg['LogPath']= self.file_cfg
        self.live_cfg['OutputDst'] = Destination.STDOUT.value 

    def enable_logging(self):
        self.__preconfigure()
        self.status = True
        return self.status

    def disable_logging(self):
        self.status = False
        return self.status

