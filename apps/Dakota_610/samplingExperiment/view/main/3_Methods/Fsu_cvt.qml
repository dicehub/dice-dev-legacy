import DICE.App 1.0
import DICE.App.Dakota 1.0


Card {
    enabled: selectedExperiment.currentRealText === 'fsu_cvt'
    visible: enabled
    visibleShadowAndBorder: false
    expanderVisible: false

    BodyText {
        text: "Design of Computer Experiments - Centroidal Voronoi Tessellation."
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
    DakotaKeyword {
        label: "latinize"
        path: "input.in method latinize"
    }
}

