"""
snappyHexMesh
=============
DICE solver app based on potentalFoam in OpenFOAM (http://www.openfoam.org/)

Copyright (c) 2014-2015 by DICE Developers
All rights reserved.
"""

# Standard Python modules
# =======================
import os

# External modules
# ================
from PyQt5.QtCore import pyqtSignal, pyqtSlot, pyqtProperty
from PyFoam.Applications.CreateBoundaryPatches import CreateBoundaryPatches
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.BoundaryDict import BoundaryDict
from PyFoam.Basics.DataStructures import Field, Vector

# DICE modules
# ============
from dice.foam_app import FoamApp
from dice.foam.solver.boundary_types import BoundaryTypes


class potentialFoam(FoamApp, BoundaryTypes):
    """
    potentialFoam
    =============
    Simple potential flow solver which can be used to generate starting fields for full Navier-Stokes codes.
    """

    app_name = "potentialFoam"
    input_types = ["foam_mesh"]
    output_types = ["foam_solution_result"]
    min_input_apps = 1
    max_input_apps = 1

    def __init__(self, parent, instance_name, status):

        FoamApp.__init__(self, parent, instance_name, status)  # initialize the base class
        BoundaryTypes.__init__(self)

        # Input/Output objects
        # ====================
        # self.__input_dict = {}
        self.__input_mesh_object = None
        self.__output_solution = None

        # Boundaries model for GUI
        # ========================
        self.__boundaries_model = []

        # Parsed files
        # ============
        self.__boundary_dict = None
        self.__p_dict = None
        self.__U_dict = None
        self.__control_dict = None
        self.__fv_solutions = None

        # Field editing
        # =============
        self.current_selected_patch_name = None

        # Filter key word for patches
        # ===========================
        self.filter_key_word = ""

    def load(self):
        self.copy_template_folder()

        # Parsed files
        # ============
        self.__p_dict = ParsedParameterFile(self.config_path('0/p'))
        self.__U_dict = ParsedParameterFile(self.config_path('0/U'))
        self.__control_dict = ParsedParameterFile(self.config_path('system/controlDict'))
        self.__fv_solutions = ParsedParameterFile(self.config_path('system/fvSolution'))

        # Registered files
        # ================
        self.register_foam_file('0/p', self.__p_dict)
        self.register_foam_file('0/U', self.__U_dict)
        self.register_foam_file('system/controlDict', self.__control_dict)
        self.register_foam_file('system/fvSolution', self.__fv_solutions)

    def prepare(self):
        """
        Copy all necessary folders for running potentialFoam
        :return:
        """
        self.copy_folder_content(self.config_path('system'), self.current_run_path('system'), overwrite=True)
        self.copy_folder_content(self.config_path('constant'), self.current_run_path('constant'), overwrite=True)
        self.copy_folder_content(self.config_path('0'), self.current_run_path('0'), overwrite=True)
        poly_mesh_folder_path = os.path.dirname(self.__input_mesh_object.boundary_dict_path())
        self.copy_folder_content(poly_mesh_folder_path, self.current_run_path('constant', 'polyMesh'), overwrite=True)
        return True

    def run(self):
        return self.__serial_run()

    def __serial_run(self):
        solver = self.__control_dict['application']
        if self.foam_exec([solver, "-case", self.current_run_path()]) == 0:
            self.__handle_successful_run()
            return True
        else:
            self.__handle_failed_run()
            return False

    def __handle_successful_run(self):
        self.debug("Successfull run!")
        pass

    def __handle_failed_run(self):
        pass

    def foam_mesh_in(self, foam_mesh):
        self.__input_dict = foam_mesh
        try:
            self.__input_mesh_object = next(iter(self.__input_dict.values()))
            boundary_dict_path = self.__input_mesh_object.boundary_dict_path()
            config_boundary_path = self.config_path("constant", "polyMesh")
            file_path = self.config_path("constant", "polyMesh", self.__input_mesh_object.boundary_real_name())
            if not os.path.exists(file_path):
                self.copy(boundary_dict_path, config_boundary_path)
                self.create_default_boundary_patches()

            # Boundary dict
            # =============
            self.__boundary_dict = BoundaryDict(self.config_path())
            self.register_foam_file('constant/polyMesh/boundary', self.__boundary_dict)
            self.update_boundaries_model()
        except StopIteration:
            pass

    def create_default_boundary_patches(self):
        """
        Creates default patches for field files in zero time folder.
        For potentialFoam: p, U.
        :return:
        """
        boundary_file_names = os.listdir(self.config_path("0"))
        for file_name in boundary_file_names:
            boundary_file_object = CreateBoundaryPatches(self.config_path("0", file_name))
            boundary_file_object.run()

    '''
    Filter keyword for patches
    ==========================
    '''
    def set_filter_keyword(self, keyword):
        self.filter_key_word = keyword
        self.update_boundaries_model()

    '''
    Model of all boundaries in constant/boundary file
    ==================================================
    '''
    boundaries_model_changed = pyqtSignal(name="boundariesModelChanged")

    @property
    def boundaries_model(self):
        return self.__boundaries_model

    @boundaries_model.setter
    def boundaries_model(self, boundaries_model):
        if self.__boundaries_model != boundaries_model:
            self.__boundaries_model = boundaries_model
            self.boundaries_model_changed.emit()

    boundariesModel = pyqtProperty("QVariantList", fget=boundaries_model.fget, fset=boundaries_model.fset,
                                   notify=boundaries_model_changed)

    def __create_boundaries_model(self):
        boundaries = self.__boundary_dict.patches()
        boundaries_model = [{
            'text': boundary,
            'type': self.__boundary_dict.getValueDict()[boundary]["type"],
        } for boundary in boundaries if self.filter_key_word in boundary]
        return boundaries_model

    def update_boundaries_model(self):
        self.boundaries_model = self.__create_boundaries_model()

    '''
    Boundary names list
    ===================
    '''
    def get_boundaries_list(self):
        return self.__boundary_dict.patches()

    '''
    Boundary types
    ==============
    '''
    def set_boundary_type(self, path, value):
        file_name, var_path = self.split_path(path)
        patch_name = var_path[0]
        group_list = None
        if patch_name in self.__boundary_dict:
            if value in ("wall", "patch", "empty", "symmetry", "symmetryPlane", "wedge"):
                if "inGroups" in self.__boundary_dict[patch_name]:
                    group_list = self.__boundary_dict[patch_name]["inGroups"]
                self.__boundary_dict[patch_name] = {
                    "type": value,
                    "nFaces": self.__boundary_dict[patch_name]["nFaces"],
                    "startFace": self.__boundary_dict[patch_name]["startFace"]
                }
                if group_list:
                    self.__boundary_dict[patch_name]["inGroups"] = group_list
            elif value == "cyclic":
                if "inGroups" in self.__boundary_dict[patch_name]:
                    group_list = self.__boundary_dict[patch_name]["inGroups"]
                self.__boundary_dict[patch_name] = {
                    "type" : "cyclic",
                    "matchTolerance" : 1e-4,
                    "transform": "noOrdering",
                    "lowWeightCorrection": 0.2,
                    "nFaces": self.__boundary_dict[patch_name]["nFaces"],
                    "startFace": self.__boundary_dict[patch_name]["startFace"],
                    "neighbourPatch": ""
                }
                if group_list:
                    self.__boundary_dict[patch_name]["inGroups"] = group_list
                self.set_cyclic_pressure_boundary(patch_name)
            elif value == "cyclicAMI":
                if "inGroups" in self.__boundary_dict[patch_name]:
                    group_list = self.__boundary_dict[patch_name]["inGroups"]
                self.__boundary_dict[patch_name] = {
                    "type" : "cyclicAMI",
                    "matchTolerance" : 1e-4,
                    "transform": "noOrdering",
                    "lowWeightCorrection": 0.2,
                    "nFaces": self.__boundary_dict[patch_name]["nFaces"],
                    "startFace": self.__boundary_dict[patch_name]["startFace"],
                    "neighbourPatch": ""
                }
                if group_list:
                    self.__boundary_dict[patch_name]["inGroups"] = group_list
                self.set_cyclic_ami_pressure_boundary(patch_name)
            self.__boundary_dict.writeFile()
            self.update_boundaries_model()
        else:
            self.debug("Patch name not in boundaries")

    '''
    Pressure Field
    ==============
    '''
    def set_cyclic_pressure_boundary(self, patch_name):
        self.__p_dict["boundaryField"][patch_name] = {
            "type": "cyclic",
            "value": Field(0)
        }
        self.__p_dict.writeFile()

    def set_cyclic_ami_pressure_boundary(self, patch_name):
        self.__p_dict["boundaryField"][patch_name] = {
            "type": "cyclicAMI",
            "value": Field(0)
        }
        self.__p_dict.writeFile()

    # Field Initialization
    # ====================
    def get_pressure_init_field(self):
        return self.__p_dict["internalField"].val

    def set_pressure_init_field(self, value):
        self.__p_dict["internalField"].val = value
        self.__p_dict.writeFile()

    def pressure_init_field_signal_name(self):
        return "0/p"

    def pressure_boundary_condition_types(self):
        return ["Fixed Value", "Total Pressure", "Zero Gradient"]

    # Boundary conditions
    # ===================
    def get_pressure_boundary_condition_type(self, patch_name):
        if patch_name in self.__p_dict["boundaryField"]:
            condition_type = self.__p_dict["boundaryField"][patch_name]["type"]
            if condition_type == "fixedValue":
                return "Fixed Value"
            elif condition_type == "totalPressure":
                return "Total Pressure"
            elif condition_type == "zeroGradient":
                return "Zero Gradient"
        else:
            return []

    def set_pressure_boundary_condition_type(self, patch_name, condition_type):
        default_pressure_value = 0
        if patch_name in self.__p_dict["boundaryField"]:
            if condition_type == "Fixed Value":
                self.__p_dict["boundaryField"][patch_name] = {
                    "type": "fixedValue",
                    "value": Field(default_pressure_value)
                }
            elif condition_type == "Total Pressure":
                self.__p_dict["boundaryField"][patch_name] = {
                    "type": "totalPressure",
                    "p0": Field(default_pressure_value),
                    "U": "U",
                    "phi": "phi",
                    "rho": "none",
                    "psi": "none",
                    "gamma": 1,
                    "value": Field(default_pressure_value)
                }
            elif condition_type == "Zero Gradient":
                self.__p_dict["boundaryField"][patch_name] = {
                    "type": "zeroGradient"
                }
            self.__p_dict.writeFile()
        else:
            raise KeyError(self.debug("Patch name not available"))

    def pressure_boundary_condition_type_signal_name(self):
        return "0/p"

    # Pressure field value
    # ====================
    def get_pressure_field_value(self, patch_name):
        if patch_name in self.__p_dict["boundaryField"]:
            if "value" in self.__p_dict["boundaryField"][patch_name]:
                return self.__p_dict["boundaryField"][patch_name]["value"].val

    def set_pressure_field_value(self, patch_name, value):
        if patch_name in self.__p_dict["boundaryField"]:
            self.__p_dict["boundaryField"][patch_name]["value"].val = value
            if "p0" in self.__p_dict["boundaryField"][patch_name]:
                self.__p_dict["boundaryField"][patch_name]["p0"].val = value
            self.__p_dict.writeFile()

    def pressure_field_value_signal_name(self):
        return "0/p"

    '''
    Velocity Field
    ==============
    '''
    def set_cyclic_velocity_boundary(self, patch_name):
        self.__U_dict["boundaryField"][patch_name] = {
            "type": "cyclic",
            "value": Field(0)
        }
        self.__U_dict.writeFile()

    def set_cyclic_ami_velocity_boundary(self, patch_name):
        self.__U_dict["boundaryField"][patch_name] = {
            "type": "cyclicAMI",
            "value": Field(0)
        }
        self.__U_dict.writeFile()

    # Field Initialization
    # ====================
    def get_velocity_init_field(self, coordinate):
        return self.__U_dict["internalField"].val[int(coordinate)]

    def set_velocity_init_field(self, coordinate, value):
        self.__U_dict["internalField"].val[int(coordinate)] = value
        self.__U_dict.writeFile()

    def velocity_init_field_signal_name(self, coordinate):
        return "0/U"

    # Boundary conditions
    # ===================
    def velocity_boundary_condition_types(self):
        return ["Fixed Value", "Zero Gradient"]

    def get_velocity_boundary_condition_type(self, patch_name):
        if patch_name in self.__U_dict["boundaryField"]:
            condition_type = self.__U_dict["boundaryField"][patch_name]["type"]
            if condition_type == "fixedValue":
                return "Fixed Value"
            elif condition_type == "zeroGradient":
                return "Zero Gradient"
        else:
            return []

    def set_velocity_boundary_condition_type(self, patch_name, condition_type):
        default_velocity_vector = Vector(0, 0, 0)
        if patch_name in self.__U_dict["boundaryField"]:
            if condition_type == "Fixed Value":
                self.__U_dict["boundaryField"][patch_name] = {
                    "type": "fixedValue",
                    "value": Field(default_velocity_vector)
                }
            elif condition_type == "Zero Gradient":
                self.__U_dict["boundaryField"][patch_name] = {
                    "type": "zeroGradient"
                }
            self.__U_dict.writeFile()
        else:
            raise KeyError(self.debug("Patch name not available"))

    def velocity_boundary_condition_type_signal_name(self):
        return "0/U"

    # Velocity field vector
    # =====================
    def get_velocity_field_value(self, path):
        patch_name = path.split()[0]
        coordinate = path.split()[1]
        if patch_name in self.__U_dict["boundaryField"]:
            if "value" in self.__U_dict["boundaryField"][patch_name]:
                return self.__U_dict["boundaryField"][patch_name]["value"].val[int(coordinate)]

    def set_velocity_field_value(self, path, value):
        patch_name = path.split()[0]
        coordinate = path.split()[1]
        if patch_name in self.__U_dict["boundaryField"]:
            self.__U_dict["boundaryField"][patch_name]["value"].val[int(coordinate)] = value
            self.__U_dict.writeFile()

    def velocity_field_value_signal_name(self, coordinate):
        return "0/U"

    '''
    Solver Settings
    ===============
    '''
    

    '''
    External Tools
    ==============
    '''
    def open_paraview(self):
        paraview = self.dice.settings.value(self, ['ParaView', 'paraview'])
        current_foam_path = self.current_run_path("view.foam")
        if not os.path.exists(current_foam_path):
            with open(current_foam_path, 'a'):
                os.utime(current_foam_path, None)
        self.run_process([paraview, current_foam_path])