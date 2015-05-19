"""
Dakota-sampling
===============
Sampling experiment app

Copyright (c) 2014-2015 by DICE Developers
All rights reserved.
"""

# Standard Python modules
# =======================
from collections import OrderedDict
import os
import stat
import copy
import collections

# External modules
# ================
from PyQt5.QtCore import pyqtProperty, pyqtSlot, pyqtSignal,QAbstractListModel

# DICE modules
# ============
from core.dakota.dakotaapp import DakotaApp
from core.dakota.dakota_table_csv import DakotaTableCsv
from core.dakota.dakota_parser import ParsedDakotaInputFile

# App modules
# ============
from .modules.visualization import Visualization


class samplingExperiment(DakotaApp, Visualization):
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
        Visualization.__init__(self)

        # Experiment Methods
        # ==================
        self.experiment_methods = ['dace', 'sampling', 'fsu_cvt', 'fsu_quasi_mc', 'psuade_moat', 'none']

        # Sample Types
        # ============
        self.dace_sample_types = ['box_behnken', 'central_composite', 'grid',
                                  'lhs', 'oa_lhs', 'oas', 'random']

        # Parsed files
        # ============
        self.dakota_input_file = None

        # Input/Output objects
        # ====================
        self.__output_csv = []

    def load(self):
        self.copy_template_folder()

        # Parse input files
        # =================
        self.dakota_input_file = ParsedDakotaInputFile(self.config_path('input.in'))

        # Register input file
        # ===================
        self.register_dakota_file('input.in', self.dakota_input_file)

        # Load function from Visualization module
        # =======================================
        self.__plot_html_path = self.config_path('index.html')
        self.visualization_load()

        # Convert table_out.dat to table_out.csv and load for visualization
        # =================================================================
        if self.status == DakotaApp.FINISHED:
            self.__output_csv = DakotaTableCsv(self.current_run_path())
            x1 = self.__output_csv.x1_data()
            y1 = self.__output_csv.y1_data()
            self.load_data(x1, y1)

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
            x1 = self.__output_csv.x1_data()
            y1 = self.__output_csv.y1_data()
            self.load_data(x1, y1)
            return True

    def __make_executable_by_owner(self, files):
        for f in files:
            file_path = self.current_run_path(f)
            st = os.stat(file_path)
            os.chmod(file_path, st.st_mode | stat.S_IEXEC)

    # Experiment selection
    # ====================
    def get_experiment_method_model(self):
        return self.experiment_methods

    def get_experiment_method(self):
        dak_var = self.dakota_input_file['method']['child']
        for method in self.experiment_methods:
            if method in dak_var:
                return method
        return 'none'

    def set_experiment_method(self, value):
        self.debug('set '+str(value))
        if value == 'dace':
            self.dakota_input_file['method']['child'] = OrderedDict({
                'id_method': {
                    'value': 'method1',
                    'child': {}
                },
                'dace': {
                    'value': '',
                    'child': {}
                },
                'lhs': {
                    'value': '',
                    'child': {}
                },
                'samples': {
                    'value': 50,
                    'child': {}
                },
                'seed': {
                    'value': 52,
                    'child': {}
                }
            })
            self.dakota_input_file.writeFile()
        else:
            return

    def experiment_method_signal_name(self):
        return "method"

    # DACE - Sample Type
    # ==================
    def get_sample_type_model(self):
        return self.dace_sample_types

    def get_sample_type(self):
        dak_var = self.dakota_input_file['method']['child']['dace']['child']
        for sample_type in self.dace_sample_types:
            if sample_type in dak_var:
                return sample_type
        return 'none'

    def set_sample_type(self, value):
        try:
            # remove old sample type
            # ======================
            dak_var = self.dakota_input_file['method']['child']['dace']['child']
            for sample_type in self.dace_sample_types:
                if sample_type in dak_var:
                    del dak_var[sample_type]

            # add new sample type
            # ===================
            dak_var[value] = OrderedDict({
                'value': '',
                'child': {}
            })
            self.dakota_input_file.writeFile()
        except:
            raise KeyError('Could not set sample type')

    def sample_type_signal_name(self):
        pass

    '''
    Output for other Apps
    =====================
    '''
    def dakota_table_csv_out(self):
        return copy.deepcopy(self.__output_csv)