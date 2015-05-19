import QtQuick 2.4
import DICE.App 1.0

import DICE.App.Dakota 1.0

Card {
    title: { text: selectedExperiment.currentText + " - Settings" }
    
    enabled: selectedExperiment.currentText === 'dace'
    visible: enabled
    visibleShadowAndBorder: false
    expanderVisible: false

    BodyText {
        text: "Design and Analysis of Computer Experiments."
        horizontalAlignment: Text.AlignHCenter
    }

    BodyText {
        horizontalAlignment: Text.AlignHCenter
        text: {
            if (sampleType.currentText == "grid")
                return "Grid Sampling"
            if (sampleType.currentText == "random")
                return "Pure Random Sampling"
            if (sampleType.currentText == "oas")
                return "Orthogonal Array Sampling"
            if (sampleType.currentText == "lhs")
                return "Latin Hypercube Sampling"
            if (sampleType.currentText == "oa_lhs")
                return "Orthogonal Array Latin Hypercube Sampling"
            if (sampleType.currentText == "box_behnken")
                return "Box-Behnken"
            if (sampleType.currentText == "central_composite")
                return "Central Composite Design"
            else
                return ""
        }
    }
    DropDown {
        id: sampleType
        label: "Sample Type"
        methodName: "sample_type"
        getModelMethod: "get_sample_type_model"
        enabled: selectedExperiment.currentText == "dace"
        visible: enabled
    }

    DakotaValue {
        label: "Samples"
        path: "method samples"
        dataType: "int"
    }
    DakotaValue {
        label: "Seed"
        path: "method seed"
        dataType: "int"
        enabled: {
            if (selectedExperiment.currentText == "dace"
                    || selectedExperiment.currentText == "sampling")
                return true
            else
                return false
        }
        visible: enabled
    }
}
