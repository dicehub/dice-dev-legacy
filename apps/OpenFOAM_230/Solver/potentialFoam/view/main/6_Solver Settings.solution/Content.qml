import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    TabsCard {
        Card {
            title: "Pressure"

            visibleShadowAndBorder: false
            expanderVisible: false

            FoamDropDown {
                id: linearMatrixSolver
                label: "Solver"
//                modelPath: "foam/system/fvSolution solvers p solver"
                getModelMethod: "pressure_fv_solution_solvers"
                path: "system/fvSolution solvers p solver"
                methodName: "pressure_fv_solution_solvers"
            }
            Subheader { text: "Options" }
            Card {
                enabled: linearMatrixSolver.currentRealText === "PCG"
                visible: enabled
                visibleShadowAndBorder: false

                FoamDropDown {
                    id: pcgPreconditioner
                    label: "Preconditioner"
                    getModelMethod: "symmetric_preconditioners"
                    path: "system/fvSolution solvers p preconditioner"
                    methodName: "solver_preconditioner"
                }
                GAMGpreconditioner {
                    enabled: pcgPreconditioner.currentRealText === "GAMG"
                    visible: enabled
                    path: pcgPreconditioner.path
                }
                FoamValue {
                    label: "Tolerance"
                    path: "system/fvSolution solvers p tolerance"
                }
                FoamValue {
                    label: "Relative Tolerance"
                    path: "system/fvSolution solvers p relTol"
                }
                FoamValue {
                    label: "Minimum Iterations"
                    path: "system/fvSolution solvers p minIter"
                    dataType: "int"
                }
                FoamValue {
                    label: "Maximum Iterations"
                    path: "system/fvSolution solvers p maxIter"
                    dataType: "int"
                }
            }
            Card {
                enabled: linearMatrixSolver.currentRealText === "GAMG"
                visible: enabled
                visibleShadowAndBorder: false

                FoamDropDown {
                    label: "Agglomerator"
                    getModelMethod: "gamg_agglomerations"
                    path: "system/fvSolution solvers p agglomerator"
                }
                FoamValue {
                    label: "Merge Levels"
                    path: "system/fvSolution solvers p mergeLevels"
                    dataType: "int"
                }
                FoamDropDown {
                    label: "Preconditioner"
                    getModelMethod: "symmetric_preconditioners"
                    path: "system/fvSolution solvers p preconditioner"
                    methodName: "solver_preconditioner"
                }
                FoamValue {
                    label: "Tolerance"
                    path: "system/fvSolution solvers p tolerance"
                }
                FoamValue {
                    label: "Relative Tolerance"
                    path: "system/fvSolution solvers p relTol"
                }
                FoamValue {
                    label: "Minimum Iterations"
                    path: "system/fvSolution solvers p minIter"
                }
                FoamValue {
                    label: "Maximum Iterations"
                    path: "system/fvSolution solvers p maxIter"
                }
            }
            Card {
                enabled: linearMatrixSolver.currentRealText === "smoothSolver"
                visible: enabled
                visibleShadowAndBorder: false

                FoamDropDown {
                    label: "Preconditioner"
                    getModelMethod: "symmetric_preconditioners"
                    path: "system/fvSolution solvers p preconditioner"
                    methodName: "solver_preconditioner"
                }
                FoamDropDown {
                    label: "Smoother"
                    getModelMethod: "symmetric_matrix_smoothers"
                    path: "system/fvSolution solvers p smoother"
                }
                FoamValue {
                    label: "Tolerance"
                    path: "system/fvSolution solvers p tolerance"
                }
                FoamValue {
                    label: "Relative Tolerance"
                    path: "system/fvSolution solvers p relTol"
                }
                FoamValue {
                    label: "Minimum Iterations"
                    path: "system/fvSolution solvers p minIter"
                }
                FoamValue {
                    label: "Maximum Iterations"
                    path: "system/fvSolution solvers p maxIter"
                }
            }
            Card {
                enabled: linearMatrixSolver.currentRealText === "ICCG"
                visible: enabled
                visibleShadowAndBorder: false

                FoamDropDown {
                    label: "Preconditioner"
                    getModelMethod: "symmetric_preconditioners"
                    path: "system/fvSolution solvers p preconditioner"
                    methodName: "solver_preconditioner"
                }
                FoamValue {
                    label: "Tolerance"
                    path: "system/fvSolution solvers p tolerance"
                }
                FoamValue {
                    label: "Relative Tolerance"
                    path: "system/fvSolution solvers p relTol"
                }
                FoamValue {
                    label: "Minimum Iterations"
                    path: "system/fvSolution solvers p minIter"
                }
                FoamValue {
                    label: "Maximum Iterations"
                    path: "system/fvSolution solvers p maxIter"
                }
            }
        }
        Card {
            title: "Velocity"

            visibleShadowAndBorder: false
            expanderVisible: false
        }
    }
    Card {
        Subheader{ text: "Potential Flow" }
        FoamValue {
            label: "Non Orthogonal Correctors"
            dataType: "int"
            path: "system/fvSolution potentialFlow nNonOrthogonalCorrectors"
        }
    }
}
