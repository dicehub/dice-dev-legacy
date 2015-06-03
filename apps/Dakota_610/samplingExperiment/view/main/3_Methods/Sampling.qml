import DICE.App 1.0
import DICE.App.Dakota 1.0


Card {
    enabled: selectedExperiment.currentRealText === 'sampling'
    visible: enabled
    visibleShadowAndBorder: false
    expanderVisible: false

    BodyText {
        text: "Randomly samples variables according to their distributions."
        horizontalAlignment: Text.AlignHCenter
    }
    Subheader {
        horizontalAlignment: Text.AlignHCenter
        text: {
            if (sampleType.currentText === "random")
                return "Random Monte Carlo"
            if (sampleType.currentText === "lhs")
                return "Latin Hypercube Sampling"
            if (sampleType.currentText === "incremental_lhs")
                return "Existing Latin Hypercube Sampling"
            if (sampleType.currentText === "incremental_random")
                return "Existing random sampling "
            else
                return ""
        }
    }
    DakotaKeywordDropDown {
        label: "Sample Type"
        path: "input.in method"
//        getModelMethod: "get_sampling_sample_type_model"
        modelPath: "sample_types sampling"
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
    DakotaKeywordDropDown {
        id: rngType
        label: "Random Number Generator"
        path: "input.in method"
//        methodName: "nrg_type"
        modelPath: "rng_types"
//        getModelMethod: "get_rng_type_model"
    }
}

