import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        Subheader { text: "Pressure" }
        FoamDropDown {
            label: "Solver"
            modelPath: "foam/system/fvSolution solvers p solver"
            path: "system/fvSolution solvers p solver"
        }
        Subheader { text: "Options" }
        FoamDropDown {
            label: "Preconditioner"
            modelPath: "foam/system/fvSolution solvers p preconditioner"
            path: "system/fvSolution solvers p preconditioner"
        }
        FoamValue {
            label: "Tolerance"
            path: "system/fvSolution solvers p tolerance"
        }
        FoamValue {
            label: "Relative Tolerance"
            path: "system/fvSolution solvers p relTol"
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
