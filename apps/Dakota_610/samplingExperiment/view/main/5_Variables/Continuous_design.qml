import DICE.App 1.0
import DICE.App.Dakota 1.0
import DICE.App.Foam 1.0

Card {
    enabled: variablesDesign.currentRealText === 'continuous_design'
    visible: enabled
    visibleShadowAndBorder: false
    expanderVisible: false

    Subheader { text: "Descriptors" }
    TreeView {
        id: treeView
        maxHeight: 300
        width: parent.width
        modelData: app.treeViewModel

        onCurrentNodeChanged: {
            print("INDEX "+currentNode.model.index)
        }
    }

    DakotaValue {
//        enabled: !!treeView.currentNode
//        visible: enabled
        label: "Lower Bound"
        path: "input.in variables lower_bounds " + treeView.currentNode.model.index
        onPathChanged: {
            print("PATH "+path)
        }
    }
    DakotaValue {
//        enabled: !!treeView.currentNode
//        visible: enabled
        label: "Upper Bound"
        path: "input.in variables upper_bounds " + treeView.currentNode.model.index
    }
}

