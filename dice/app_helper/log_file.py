# Standard Python modules
# =======================
import os

# External modules
# ================
from PyQt5.QtCore import pyqtSlot, qDebug


class LogFile:
    def __init__(self, cmd_name, cwd):
        self.__log_file_name = cmd_name
        self.__cwd = cwd
        self.__default_folder_name = "logs"
        self.__log_file_path = os.path.join(self.__cwd, self.__default_folder_name, self.__log_file_name)

        self.log_file = None

        self.open()
        self.close()

    def open(self, mode="w"):
        self.__ensure_dir()
        self.log_file = open(self.__log_file_path, mode)

    def close(self):
        self.log_file.close()

    def write_line(self, line):
        self.open(mode="a")
        self.log_file.write(line)
        self.close()

    def __ensure_dir(self):
        default_folder_path = os.path.join(self.__cwd, self.__default_folder_name)
        if not os.path.exists(default_folder_path):
            os.makedirs(default_folder_path)