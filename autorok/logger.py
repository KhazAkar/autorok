import enum
import logging
import sys
import pathlib

# Defining available levels for logging

class LOG_LEVEL(enum.IntEnum):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

def configure_logging(filename: pathlib.Path, level: LOG_LEVEL):
    """
    Function to configure project logger
    Parameters
    ----------
    filename : str
        Name of the file to write logging data
    level : int
        Level defining, from 0 to 50

    """
    # Creating logger with level#
    log = logging.getLogger("autorok") 
    log.setLevel(level.value)
    # Define formatting #
    formatting = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    # Make this log into a file with defined formatting #
    filelogging = logging.FileHandler(filename)
    filelogging.setLevel(level.value)
    filelogging.setFormatter(formatting)
    # Create StreamLogging
    consolelogging = logging.StreamHandler(sys.stdout)
    consolelogging.setFormatter(formatting)
    # Finally, add file handling logger to logger #
    log.addHandler(filelogging)
    log.addHandler(consolelogging)
    