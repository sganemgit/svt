
# @author Shady Ganem <shady.ganem@intel.com>

import logging
import os
from core.utilities.colors import colors
import threading

class log:

    def __init__(self, testname, level = 'INFO'):
        self.lock = threading.Lock()
        if level == 'NOTSET':
            self.level = logging.NOTSET
        elif level == 'DEBUG':
            self.level = logging.DEBUG
        elif level == 'INFO':
            self.level = logging.INFO
        elif level == 'WARNING':
            self.level = logging.WARNING
        elif level == 'ERROR':
            self.level = logging.ERROR
        elif level == 'CRITICAL':
            self.level = logging.CRITICAL
        else:
            self.level = logging.DEBUG

        self.filepath = "/home/{}/logs/{}/testlog.log".format(os.environ["USER"], testname)
        directory = os.path.dirname(self.filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)

        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename = self.filepath, level = self.level, format = LOG_FORMAT, filemode = 'w')
        self.logger = logging.getLogger()

    def info(self, msg = "", color = None):
        with self.lock:
            if color == 'r':
                print(colors.Red(msg))
            elif color == 'b':
                print(colors.Blue(msg))
            elif color == 'g':
                print(colors.Green(msg))
            elif color == 'o':
                print(colors.Orange(msg))
            else:
                print(msg)
            self.logger.info(msg)

    def debug(self, msg = ""):
        with self.lock:
            print(colors.Blue(msg))
            self.logger.debug(msg)

    def warning(self, msg = ""):
        with self.lock:
            print(colors.Orange(msg))
            self.logger.warning(msg)

    def error(self, msg = ""):
        with self.lock:
            print(colors.Red(msg))
            self.logger.error(msg)

    def critical(self, msg = ""):
        with self.lock:
            print(colors.Red(msg))
            self.logger.critical(msg)

if __name__ == "__main__":
    log = log("testlog")
    log.info("info message")
    log.debug("debug message")
    log.error("error message")
    log.warning("warnign message")
    log.critical("critical message")
