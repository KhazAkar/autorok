import logging

# Defining available levels for logging

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

def configure_logging(filename: str, level: int) -> logging.Logger:
    """
    Function to configure project logger
    Parameters
    ----------
    filename : str
        Name of the file to write logging data
    level : int
        Level defining, from 0 to 50
    Returns
    -------
    log: logging.Logger
        Logger object to log into
    """
    # Creating logger with level#
    log = logging.getLogger("autorok") 
    log.setLevel(level)
    # Define formatting #
    formatting = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    # Make this log into a file with defined formatting #
    filelogging = logging.FileHandler(filename)
    filelogging.setLevel(level)
    filelogging.setFormatter(formatting)
    # Finally, add file handling logger to logger #
    log.addHandler(filelogging)
    return log