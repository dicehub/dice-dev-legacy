import QtQuick 2.4
import DICE.App 1.0

import DICE.App.Dakota 1.0

Body {
    Card {
        Subheader { text: "Choose Method" }
        DropDown {
            id: selectedExperiment
            label: "Method"
            methodName: "experiment_method"
            getModelMethod: "get_experiment_method_model"
        }
    }
    Card {
        enabled: selectedExperiment.currentText !== 'none'
        visible: enabled

        Subheader { text: selectedExperiment.currentText + " - Settings" }
        Dace {}
    }
}

