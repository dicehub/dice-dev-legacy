import DICE.App 1.0
import DICE.App.Dakota 1.0


Card {
    enabled: selectedExperiment.currentRealText === 'psuade_moat'
    visible: enabled
    visibleShadowAndBorder: false
    expanderVisible: false

    BodyText {
        text: "Morris One-at-a-Time."
        horizontalAlignment: Text.AlignHCenter
    }
    DakotaValue {
        label: "Samples"
        path: "input.in method samples"
        dataType: "int"
    }
    DakotaValue {
        label: "Seed"
        path: "input.in method seed"
        dataType: "int"
    }
}
