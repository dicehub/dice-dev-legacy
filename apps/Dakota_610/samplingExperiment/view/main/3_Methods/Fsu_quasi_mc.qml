import DICE.App 1.0
import DICE.App.Dakota 1.0


Card {
    enabled: selectedExperiment.currentRealText === 'fsu_quasi_mc'
    visible: enabled
    visibleShadowAndBorder: false
    expanderVisible: false

    BodyText {
        text: "Design of Computer Experiments - Quasi-Monte Carlo sampling."
        horizontalAlignment: Text.AlignHCenter
    }
    DakotaValue {
        label: "Samples"
        path: "input.in method samples"
        dataType: "int"
    }
    DakotaKeywordDropDown {
        label: "Method"
        path: "input.in method"
        modelPath: "fsu_quasi_mc sequence_types"
    }
    DakotaKeyword {
        label: "latinize"
        path: "input.in method latinize"
    }
}

