import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    TabsCard {
        Card {
            Subheader { text: "Pressure" }
            FoamDropDown {
                label: "Solver"
                modelPath: "foam/system/fvSolution solvers p solver"
                path: "system/fvSolution solvers p solver"
            }
            Subheader { text: "Options" }
        }
        Card {
            Subheader { text: "Velocity" }
        }
    }
}
