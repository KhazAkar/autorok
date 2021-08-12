import subprocess, os
import autorok_devices, autorok_logger

class SigrokCLI():
    def __init__(self, bin_path: str):
        self.detected_devices = list()
        self.bin_path = bin_path
        self.logger = autorok_logger.configure_logging("SigrokCLI", autorok_logger.INFO)
        if not os.file.isfile(bin_path) or not bin_path.endswith(["sigrok-cli", "sigrok-cli.exe"]):
            self.logger.critical("Provided path is not valid. Deleting this instance.")
            del self

    def detect_devices(self):
        """
        Function to automatically detect connected devices and record them to object "database"
        """
        try:
            devices = subprocess.run([self.bin_path, '--scan'], capture_output=True, universal_newlines=True)
        except subprocess.CalledProcessError:
            self.logger.critical("System was not able to scan system for available devices")
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
            self.logger.info(f"System detected following devices: {self.detected_devices}")