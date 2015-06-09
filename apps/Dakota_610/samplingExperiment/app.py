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
from collections import OrderedDict

# External modules
# ================
from PyQt5.QtCore import pyqtProperty, pyqtSlot, pyqtSignal,QAbstractListModel

# DICE modules
# ============
from dice.dakota.dakota_app import DakotaApp
from dice.dakota.dakota_table_csv import DakotaTableCsv
from dice.dakota.dakota_parser import ParsedDakotaInputFile

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
        self.experiment_methods = self.get_model_data("method_types")

        # Input file name
        # ===============
        self.input_file_name = "input.in"

        # Parsed files
        # ============
        self.dakota_input_file = None

        # Input/Output objects
        # ====================
        self.__output_csv = []

        # TreeView model for variables in GUI
        # ===================================
        self.__tree_view_model = []

    def load(self):
        self.copy_template_folder()

        # Parse input files
        # =================
        self.dakota_input_file = ParsedDakotaInputFile(self.config_path(self.input_file_name))

        # Register input file
        # ===================
        self.register_dakota_file(self.input_file_name, self.dakota_input_file)

        # Load function from Visualization module
        # =======================================
        self.visualization_load()

        # Convert table_out.dat to table_out.csv and load for visualization
        # =================================================================
        if self.status == DakotaApp.FINISHED:
            self.__output_csv = DakotaTableCsv(self.current_run_path())
            self.load_data(self.__output_csv)

        self.update_tree_view()

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
            self.load_data(self.__output_csv)
            return True

    def __make_executable_by_owner(self, files):
        for f in files:
            file_path = self.current_run_path(f)
            st = os.stat(file_path)
            os.chmod(file_path, st.st_mode | stat.S_IEXEC)

    '''
    TreeView for app
    ================
    '''
    tree_view_model_changed = pyqtSignal(name="treeViewModelChanged")

    @property
    def tree_view_model(self):
        return self.__tree_view_model

    @tree_view_model.setter
    def tree_view_model(self, tree_view_model):
        if self.__tree_view_model != tree_view_model:
            self.__tree_view_model = tree_view_model
            self.tree_view_model_changed.emit()

    treeViewModel = pyqtProperty("QVariantList", fget=tree_view_model.fget, fset=tree_view_model.fset,
                                 notify=tree_view_model_changed)

    def __create_tree_view_model(self):
        descriptors_list = self.get_dakota_var("input.in variables descriptors")
        variables_model = [{
            "text": name,
            "index": i
        } for i, name in enumerate(descriptors_list)]
        # descriptors_count = self.get_dakota_var("input.in variables continuous_design")
        model = variables_model
        return model

    def update_tree_view(self):
        self.tree_view_model = self.__create_tree_view_model()

    '''
    Experiment selection
    ====================
    '''
    # def get_experiment_method_model(self):
    #     return self.experiment_methods

    def get_experiment_method(self, path=None):
        dak_var = self.dakota_input_file['method']
        for method in self.experiment_methods:
            if method in dak_var:
                return method
        return 'none'

    def set_experiment_method(self, path, value):
        if value == "dace":
            self.dakota_input_file['method'] = OrderedDict([
                ('id_method', 'method1'),
                ('dace', ''),
                ('lhs',  ''),
                ('samples', 42),
                ('seed', 42)
            ])
        elif value == "sampling":
            self.dakota_input_file['method'] = OrderedDict([
                ('id_method', 'method1'),
                ('sampling', ''),
                ('sample_type', ''),
                ('lhs', ''),
                ('samples', 42),
                ('seed', 42),
                ('rng', ''),
                ('rnum2', '')
            ])
        elif value == "fsu_cvt":
            self.dakota_input_file['method'] = OrderedDict([
                ('id_method', 'method1'),
                ('fsu_cvt', ''),
                ('samples', 42),
                ('seed', 42)
            ])
        elif value == "fsu_quasi_mc":
            self.dakota_input_file['method'] = OrderedDict([
                ('id_method', 'method1'),
                ('fsu_quasi_mc', ''),
                ('halton', ''),
                ('samples', 42)
            ])
        elif value == "psuade_moat":
            self.dakota_input_file['method'] = OrderedDict([
                ("id_method", "method1"),
                ("psuade_moat", ""),
                ("samples", 42),
                ("seed", 42)
            ])
        else:
            raise KeyError("Not found key "+value)
        self.dakota_input_file.writeFile()

    def experiment_method_signal_name(self, path):
        return self.input_file_name  + " method"

    '''
    Output for other Apps
    =====================
    '''
    def dakota_table_csv_out(self):
        return copy.deepcopy(self.__output_csv)