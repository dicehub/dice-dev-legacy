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

    Card {
        enabled: !!boundaries.currentNode

        FoamDropDown {
            id: boundaryType

            label: "Boundary Type"
            getModelMethod: "boundary_types"
            path: boundaries.currentNode ? "constant/polyMesh/boundary " + boundaries.currentNodePath[0] + " type" : undefined
            setMethod: "set_boundary_type"
        }
    }

    Card {
        Subheader {text: "Settings for " + boundaries.currentNode.model.type + " Patch"}
        enabled: !!boundaries.currentNode && (["cyclic", "cyclicAMI"]).indexOf(boundaries.currentNode.model.type) >= 0
        visible: enabled

        FoamDropDown {
            id: neigbourPatch

            label: "Neighbour Patch"
            getModelMethod: "get_boundaries_list"
            path: "constant/polyMesh/boundary " + boundaries.currentNodePath[0] + " neighbourPatch"
        }

        FoamDropDown {
            id: transformationType

            label: "Transform"
            modelPath: "foam/boundaryField derivedType cyclicAMI transform"
            path: "constant/polyMesh/boundary " + boundaries.currentNodePath[0] + " transform"
        }

        FoamValue {
            label: "Match Tolerance"
            path: "constant/polyMesh/boundary " + boundaries.currentNodePath[0] + " matchTolerance"
        }

        FoamValue {
            optional: true
            label: "Low Weight Correction"
            path: "constant/polyMesh/boundary " + boundaries.currentNodePath[0] + " lowWeightCorrection"
        }
    }
}
