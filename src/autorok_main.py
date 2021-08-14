import subprocess, pathlib, typing, logging
import src.autorok_devices, src.autorok_logger
from src.autorok_options import *

class SigrokCLI():
    
    def __init__(self, bin_path: pathlib.Path, log_path : pathlib.Path):
        """
        Initialization method of the class

        Parameters
        ----------
        bin_path : str
            Path to sigrok-cli binary.
        """
        self.detected_devices = list()
        self.bin_path = bin_path
        self.active_channels = None
        self.active_device = None
        self.active_channels = None
        self.active_driver = None
        self.sample_method = None
        self.logger = src.autorok_logger.configure_logging(log_path, src.autorok_logger.INFO)

        if not pathlib.Path.is_file(bin_path) or not str(bin_path).endswith(("sigrok-cli", "sigrok-cli.exe")):
            self.logger.critical("Provided path is not valid. Deleting this instance.")
            del self

    def start_measurement(self) -> logging.Logger:
        raise  NotImplementedError

    def detect_devices(self) -> logging.Logger:
        """
        Nethod to detect all devices.

        Returns
        -------
        logging.Logger
            Logger object.
        """
        try:
            devices = subprocess.run([self.bin_path, SigrokCLIOptions.Scan.value], capture_output=True, universal_newlines=True)
        except subprocess.CalledProcessError:
            return self.logger.critical("System was not able to scan system for available devices")
        else:
            # Parse sigrok-cli output to dict
            str_split = devices.stdout.splitlines()
            str_split[:] = str_split[1:]
            value = {}
            for line in str_split:
                line = line.split(" ")
                value[line[0]] = line[line.index("channels:") + 1 : ]
            # Map data from string to internal Enum scheme
            self.detected_devices = [device for device in value.keys()]
            return self.logger.info(f"System detected following devices: {self.detected_devices}")

    def set_active_channels(self, channels: typing.Union[typing.List[int], typing.List[str]]) -> logging.Logger:
        """
        Method to set active channels for active device properly

        Parameters
        ----------
        channels : typing.Union[typing.List[int], typing.List[str]]
            List of ints/strings for setting active channels for active device

        Returns
        -------
        logging.Logger
            Logger object.

        Raises
        ------
        ValueError
            Is raised, when channel descriptor is out of allowed range, defined in active device enum
        """
        try:
            self.active_channels = channels
            if channels not in self.device_channels:
                self.logger.exception("Channel value out of allowed range")
                raise ValueError("Channel value out of allowed range")
        except ValueError:
                return self.logger.critical(f"Channel value was not able to be set due to channel descriptor out of range")

    def set_active_device(self, device: src.autorok_devices._Device) -> logging.Logger:
        """
        Method to set active device properly

        Parameters
        ----------
        device : Devices
            Enum which contains driver and list of channels for device

        Returns
        -------
        logging.Logger
            Logger object
        """
        try:
            self.active_device = device
            self.active_channels = device.channels
            self.active_driver = device.driver
            return self.logger.info(f"Device {self.active_device}, which uses driver {self.active_driver} and have available channels: {self.device_channels} was properly set as active")
        except Exception:
            return self.logger.critical("Wrong device name, please pass Devices enum")
        

    def set_sampling(self, method: SampleMethod, value: typing.Union[int, None] = 1) -> logging.Logger:
        """
        Method to set sampling method and value properly

        Parameters
        ----------
        method : SampleMethod
           Enum which contains proper option to set sampling method for gathering of data

        Returns
        -------
        logging.Logger
            Logger object.
        """
        try:
            self.sample_method = method
            if self.sample_method == SampleMethod.Continous:
                return self.logger.info("Continous sampling enabled, no passing of value data")
            else:
                self.sampling_value = value
        except Exception:
            return self.logger.exception("Wrong value was passed to the function.")