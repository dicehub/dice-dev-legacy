import DICE.App 1.0
import DICE.App.Foam 1.0

Card {
    property var path

    Subheader { text: "GAMG Preconditioner Options" }
    FoamDropDown {
        label: "Agglomerator"
        getModelMethod: "gamg_agglomerations"
        path: "system/fvSolution solvers p preconditioner agglomerator"
    }
    FoamToggleButton {
        label: "Cache Agglomeration"
        path: "system/fvSolution solvers p preconditioner cacheAgglomeration"
    }
    FoamValue {
        label: "Merge Levels"
        path: "system/fvSolution solvers p preconditioner mergeLevels"
        dataType: "int"
    }
    FoamDropDown {
        label: "Preconditioner"
        getModelMethod: "symmetric_preconditioners"
        path: "system/fvSolution solvers p preconditioner preconditioner"
        methodName: "solver_preconditioner"
    }
    FoamValue {
        label: "Tolerance"
        path: "system/fvSolution solvers p preconditioner nCellsInCoarsestLevel"
    }
    FoamValue {
        label: "Tolerance"
        path: "system/fvSolution solvers p preconditioner tolerance"
    }
    FoamValue {
        label: "Relative Tolerance"
        path: "system/fvSolution solvers p preconditioner relTol"
    }
    FoamValue {
        label: "Minimum Iterations"
        path: "system/fvSolution solvers p preconditioner minIter"
        dataType: "int"
    }
    FoamValue {
        label: "Maximum Iterations"
        path: "system/fvSolution solvers p preconditioner maxIter"
        dataType: "int"
    }
    FoamDropDown {
        label: "Smoother"
        getModelMethod: "symmetric_matrix_smoothers"
        path: "system/fvSolution solvers p preconditioner smoother"
    }
    FoamValue {
        label: "Pre Sweeps"
        path: "system/fvSolution solvers p preconditioner nPreSweeps"
        dataType: "int"
    }
    FoamValue {
        label: "Pre Sweeps Level Multiplier"
        path: "system/fvSolution solvers p preconditioner preSweepsLevelMultiplier"
        dataType: "int"
    }
    FoamValue {
        label: "Post Sweeps"
        path: "system/fvSolution solvers p preconditioner nPostSweeps"
        dataType: "int"
    }
    FoamValue {
        label: "Post Sweeps Level Multiplier"
        path: "system/fvSolution solvers p preconditioner postSweepsLevelMultiplier"
        dataType: "int"
    }
    FoamValue {
        label: "Max Post Sweeps"
        path: "system/fvSolution solvers p preconditioner maxPostSweeps"
        dataType: "int"
    }
    FoamValue {
        label: "Finest Sweeps"
        path: "system/fvSolution solvers p preconditioner nFinestSweeps"
        dataType: "int"
    }
    FoamToggleButton {
        label: "Interpolate Correction"
        path: "system/fvSolution solvers p preconditioner interpolateCorrection"
    }
    FoamToggleButton {
        label: "Direct Solve Coarsest"
        path: "system/fvSolution solvers p preconditioner directSolveCoarsest"
    }
}
