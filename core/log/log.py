
# @author Shady Ganem <shady.ganem@intel.com>

import logging
import os
from core.utilities.colors import colors
import threading

class log:
    
    def __init__(self, testname, level='INFO'):
        self.lock = threading.Lock()
        if level == 'NOTSET':
            self.level = logging.NOTSET # 0
        elif level == 'DEBUG':
            self.level = logging.DEBUG # 10
        elif level == 'INFO':
            self.level = logging.INFO # 20
        elif level == 'WARNING':
            self.level = logging.WARNING # 30
        elif level == 'ERROR':
            self.level = logging.ERROR #40
        elif level == 'CRITICAL':
            self.level = logging.CRITICAL #50
        else:
            print("Log level {} is not defined. Setting log level to 'INFO'".format(level))
            self.level = logging.INFO

        self.filepath = "/home/{}/logs/{}/testlog.log".format(os.environ["USER"], testname)
        directory = os.path.dirname(self.filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)

        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename=self.filepath, level=self.level, format=log_format, filemode='w')
        self.logger = logging.getLogger()
        #ch = logging.StreamHandler()
        #ch.setLevel(self.level)
        #self.logger.addHandler(ch)

    def debug(self, msg = ""):
        if self.level <= logging.DEBUG:
            with self.lock:
                print(colors.LightBlue(msg))
                self.logger.debug(msg)

    def info(self, msg = "", color = None):
        if self.level <= logging.INFO:
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

    def warning(self, msg = ""):
        if self.level <= logging.WARNING: 
            with self.lock:
                print(colors.Orange(msg))
                self.logger.warning(msg)

    def error(self, msg = ""):
        if self.level <= logging.ERROR:
            with self.lock:
                print(colors.Red(msg))
                self.logger.error(msg)

    def critical(self, msg = ""):
        if self.level <= logging.CRITICAL:
            with self.lock:
                print(colors.Red(msg))
                self.logger.critical(msg)
    
    def line(self):
        self.info(80*"-")

if __name__ == "__main__":
    log = log("testlog")
    log.info("info message")
    log.debug("debug message")
    log.error("error message")
    log.warning("warnign message")
    log.critical("critical message")
