"""
Dakota-sampling
===============
Sampling experiment app

Copyright (c) 2014-2015 by DICE Developers
All rights reserved.
"""

# Standard Python modules
# =======================
import os
import stat

# DICE modules
# ============
from core.dakota.dakotaapp import DakotaApp


class samplingExperiment(DakotaApp):
    """
    dakotaSampling
    ==============
    """

    app_name = "samplingExperiment"
    input_types = []
    output_types = []

    def __init__(self, parent, instance_name, status):
        """
        Constructor of samplingExperiment
        :param parent:
        :param instance_name:
        :param status:
        :return:
        """

        DakotaApp.__init__(self, parent, instance_name, status)

    def load(self):
        self.copy_template_folder()

    def prepare(self):
        """
        Prepare run folder for running
        :return:
        """
        self.clear_folder_content(self.current_run_path())
        self.copy_folder_content(self.config_path(), self.current_run_path())
        self.__make_executable_by_owner(["dakota_cleanup", "simulator_script"])
        return True

    def run(self):
        self.dakota_exec(["-i", "input.in"])

    def __make_executable_by_owner(self, files):
        for f in files:
            file_path = self.current_run_path(f)
            st = os.stat(file_path)
            os.chmod(file_path, st.st_mode | stat.S_IEXEC)