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

        # # Experiment Methods
        # # ==================
        # self.experiment_methods = ['dace', 'sampling', 'fsu_cvt', 'fsu_quasi_mc', 'psuade_moat', 'none']
        self.experiment_methods = self.get_model_data("method_types")

        # Sample Types
        # ============
        # self.dace_sample_types = ['box_behnken', 'central_composite', 'grid',
        #                           'lhs', 'oa_lhs', 'oas', 'random']
        # self.sampling_sample_types = ['random', 'lhs', 'incremental_lhs', 'incremental_random']
        # self.sampling_nrg_types = ['rnum2', 'mt19937']

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

        # Input file name
        # ===============
        self.input_file_name = "input.in"

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
            x1 = self.__output_csv.x1_data()
            y1 = self.__output_csv.y1_data()
            self.load_data(x1, y1)

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
            x1 = self.__output_csv.x1_data()
            y1 = self.__output_csv.y1_data()
            self.load_data(x1, y1)
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
        self.debug("d-list "+str(descriptors_list))
        variables_model = [{
            "text": name,
            "index": i
        } for i, name in enumerate(descriptors_list)]
        descriptors_count = self.get_dakota_var("input.in variables continuous_design")
        self.debug("descriptors count "+str(descriptors_count))
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
        elif value == "none":
            self.dakota_input_file['method'] = OrderedDict()
        else:
            raise KeyError("Not found key "+value)
        self.dakota_input_file.writeFile()

    def experiment_method_signal_name(self, path):
        return self.input_file_name  + " method"

    # '''
    # DACE - Sample Type
    # ==================
    # '''
    # def get_dace_sample_type_model(self):
    #     return self.dace_sample_types

    # def get_dace_sample_type(self):
    #     dak_var = self.dakota_input_file['method']
    #     for sample_type in self.dace_sample_types:
    #         if sample_type in dak_var:
    #             return sample_type
    #     return 'none'
    #
    # def set_dace_sample_type(self, value):
    #     try:
    #         # remove old dace sample type
    #         # ===========================
    #         dak_var = self.dakota_input_file['method']
    #         for sample_type in self.dace_sample_types:
    #             if sample_type in dak_var:
    #                 del dak_var[sample_type]
    #
    #         # add new dace sample type
    #         # ========================
    #         dak_var[value] = ''
    #         self.dakota_input_file.writeFile()
    #     except:
    #         raise KeyError('Could not set sample type')
    #
    # def dace_sample_type_signal_name(self):
    #     return self.input_file_name

    # '''
    # Sampling - Sample Type
    # ======================
    # '''
    # def get_sampling_sample_type_model(self):
    #     return self.sampling_sample_types

    # def get_sampling_sample_type(self):
    #     dak_var = self.dakota_input_file['method']
    #     for sample_type in self.sampling_sample_types:
    #         if sample_type in dak_var:
    #             return sample_type
    #     return 'none'
    #
    # def set_sampling_sample_type(self, value):
    #     try:
    #         # remove old sampling sample type
    #         # ===============================
    #         dak_var = self.dakota_input_file['method']
    #         for sample_type in self.sampling_sample_types:
    #             if sample_type in dak_var:
    #                 del dak_var[sample_type]
    #
    #         # add new sampling sample type
    #         # ============================
    #         dak_var[value] = ''
    #         self.dakota_input_file.writeFile()
    #     except:
    #         raise KeyError('Could not set sample type')
    #
    # def sampling_sample_type_signal_name(self):
    #     return self.input_file_name

    # Sampling - NRG - Type
    # =====================
    def get_rng_type_model(self):
        return self.sampling_nrg_types

    '''
    Output for other Apps
    =====================
    '''
    def dakota_table_csv_out(self):
        return copy.deepcopy(self.__output_csv)