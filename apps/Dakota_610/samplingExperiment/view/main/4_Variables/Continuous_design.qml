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
    }

    DakotaValue {
        enabled: !!treeView.currentNode && lowerBoundsOption.checked
        onEnabledChanged: print("CHANGED!!!")
        visible: enabled
        label: "Lower Bound"
        path: "input.in variables lower_bounds " + treeView.currentNode.model.index
    }
    DakotaValue {
        enabled: !!treeView.currentNode && upperBoundsOption.checked
        visible: enabled
        label: "Upper Bound"
        path: "input.in variables upper_bounds " + treeView.currentNode.model.index
    }
    DakotaValue {
        enabled: !!treeView.currentNode && initialPointsOption.checked
        visible: enabled
        label: "Initial Point"
        path: "input.in variables initial_point " + treeView.currentNode.model.index
    }

    Card {
        expanderVisible: false
        visibleShadowAndBorder: false

        Subheader { text: "Options"}

        DakotaOptionButton {
            id: lowerBoundsOption
            text: "Lower Bounds"
            path: "input.in variables lower_bounds"
            defaultValue: Array.apply(null, new Array(treeView.modelData.length)).map(Number.prototype.valueOf, 0);
        }
        DakotaOptionButton {
            id: upperBoundsOption
            text: "Upper Bounds"
            path: "input.in variables upper_bounds"
            defaultValue: Array.apply(null, new Array(treeView.modelData.length)).map(Number.prototype.valueOf, 1);
        }
        DakotaOptionButton {
            id: initialPointsOption
            text: "Initial Points"
            path: "input.in variables initial_point"
            defaultValue: Array.apply(null, new Array(treeView.modelData.length)).map(Number.prototype.valueOf, 0);
        }
    }
}

