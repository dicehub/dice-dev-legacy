import QtQuick 2.4
import DICE.App 1.0

import DICE.App.Dakota 1.0

Body {
    Card {
        Subheader { text: "Choose Method" }
        DakotaKeywordDropDown {
            id: selectedExperiment
            label: "Method"
            path: "input.in method"
            modelPath: "method_types"
            methodName: "experiment_method"
        }
    }

    Card {
        enabled: selectedExperiment.currentRealText !== 'none'
        visible: enabled

        Subheader { text: selectedExperiment.currentRealText + " - Settings" }
        Dace {}
        Sampling {}
        Fsu_cvt {}
        Fsu_quasi_mc {}
        Psuade_moat {}
    }
}

