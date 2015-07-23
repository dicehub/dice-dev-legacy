import QtQuick 2.4

import DICE.App 1.0
import DICE.App.Foam 1.0
import DICE.Theme 1.0

Body {
    Card {
        Subheader { text: "Boundaries" }
        InputField {
            id: filterKeyword
            label: "Filter"
            onTextChanged: {
                app.call("set_filter_keyword", [text])
            }
        }
        TreeView {
            id: boundaries

            maxHeight: 300
            width: parent.width
            modelData: app.boundariesModel
            rightInfo:  BasicText {
                text: model.type
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    TabsCard {
        enabled: !!boundaries.currentNode

        Card {
            title: "Pressure [Pa]"

            visibleShadowAndBorder: false
            expanderVisible: false

            FoamDropDown {
                id: pressureType

                label: "Type"
                getModelMethod: "pressure_boundary_condition_types"
//                path: boundaries.currentNode ? "0/p boundaryField " + boundaries.currentNode.text + " type" : undefined
                path: boundaries.currentNode.text
                methodName: "pressure_boundary_condition_type"
            }
            FoamValue {
//                enabled: pressureType.currentRealText === "Fixed Value"
                enabled: (["Fixed Value", "Total Pressure"]).indexOf(pressureType.currentRealText) >= 0
                visible: enabled
                label: "Pressure [Pa]"
//                path: "0/p boundaryField " + boundaries.currentNode.text + " value"
                path: boundaries.currentNode.text
                methodName: "pressure_field_value"
            }
        }
        Card {
            title: "Velocity [m/s]"

            visibleShadowAndBorder: false
            expanderVisible: false

            FoamDropDown {
                id: velocityType

                label: "Type"
                getModelMethod: "velocity_boundary_condition_types"
//                path: boundaries.currentNode ? "0/p boundaryField " + boundaries.currentNode.text + " type" : undefined
                path: boundaries.currentNode.text
                methodName: "velocity_boundary_condition_type"
            }
            FoamVector {
                enabled: (["Fixed Value"]).indexOf(velocityType.currentRealText) >= 0
                visible: enabled
                xLabel: "Velocity X"
                yLabel: "Velocity Y"
                zLabel: "Velocity Z"
                path: boundaries.currentNode.text
                methodName: "velocity_field_value"
//                path: boundaries.currentNode ? "0/U boundaryField " + boundaries.currentNode.text + " value 1" : undefined
            }
        }
    }
}
