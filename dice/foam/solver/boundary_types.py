# External modules
# ================
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.BoundaryDict import BoundaryDict


class BoundaryTypes():

    @staticmethod
    def boundary_types():
        return ["patch", "wall", "empty", "symmetry", "wedge", "cyclic", "cyclicAMI"]