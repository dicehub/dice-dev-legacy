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
import copy


# DICE modules
# ============
from core.dakota.dakotaapp import DakotaApp
from core.dakota.dakota_table_csv import DakotaTableCsv
from core.dakota.dakota_parser import ParsedDakotaInputFile


class samplingExperiment(DakotaApp):
    """
    dakotaSampling
    ==============
    """

    app_name = "samplingExperiment"
    input_types = []
    output_types = ["dakota_table_csv"]

    def __init__(self, parent, instance_name, status):
        """
        Constructor of samplingExperiment
        :param parent:
        :param instance_name:
        :param status:
        :return:
        """

        DakotaApp.__init__(self, parent, instance_name, status)

        # Parsed files
        # ============
        self.dakota_input_file = None

        # Input/Output objects
        # ====================
        self.__output_csv = []

    def load(self):
        self.copy_template_folder()

        # Parsed files
        # ============
        self.debug("----")
        self.dakota_input_file = ParsedDakotaInputFile(self.config_path('input.in'))
        self.debug("INPUT ---- "+str(self.dakota_input_file))

        # Convert table_out.dat to table_out.csv and load for visualization
        # =================================================================
        if self.status == DakotaApp.FINISHED:
            self.__output_csv = DakotaTableCsv(self.current_run_path())

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
        if self.dakota_exec(["-i", "input.in"]) == 0:
            self.__output_csv = DakotaTableCsv(self.current_run_path())
            return True

    def __make_executable_by_owner(self, files):
        for f in files:
            file_path = self.current_run_path(f)
            st = os.stat(file_path)
            os.chmod(file_path, st.st_mode | stat.S_IEXEC)

    '''
    Output for other Apps
    =====================
    '''
    def dakota_table_csv_out(self):
        return copy.deepcopy(self.__output_csv)