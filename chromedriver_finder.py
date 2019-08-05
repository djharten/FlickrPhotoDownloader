import os
import sys
from string import ascii_uppercase
from os import path


class ChromedriverFinder:

    def __init__(self, os_type):
        self.name = "chromedriver.exe"
        self.os_type = os_type

    def find_chromedriver(self):
        drive_list = self.get_all_drives()
        for drive in drive_list:
            for root, dirs, files in os.walk(drive):
                if self.name in files:
                    return os.path.join(drive, root, self.name)
        print("Error! Chromedriver does not seem to be installed on your machine. Please install it and"
              " try again.")
        sys.exit()

    def get_all_drives(self):
        if self.os_type == "Windows":
            drive_list = []
            for drive in ascii_uppercase:
                full_drive_path = drive + ":\\"
                if path.exists(full_drive_path):
                    drive_list.append(full_drive_path)
            return drive_list
        else:
            return "/"
