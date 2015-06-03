import QtQuick 2.4
import DICE.App 1.0

import DICE.App.Dakota 1.0

Body {
    Card {
        DakotaKeywordDropDown {
            id: variablesDesign
            label: "Design"
            path: "input.in variables"
            modelPath: "variables_design"
        }
    }

    Card {
        enabled: variablesDesign.currentRealText !== 'none'
        visible: enabled

//        Subheader { text:  variablesDesign.currentRealText + " - Variables"}
        Continuous_design {}
    }
}

