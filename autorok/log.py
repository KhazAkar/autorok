import typing
import logging
import pathlib
import configparser


class Log:
    def __init__(self):
        self.status: bool = None
        self.live_cfg: typing.Dict[str] = {}
        self.file_cfg: pathlib.Path = pathlib.Path()
        self.__cfg_parser = configparser.ConfigParser()

    def enable_logging(self):
        self.status = True
        return self.status

    def disable_logging(self):
        self.status = False
        return self.status

