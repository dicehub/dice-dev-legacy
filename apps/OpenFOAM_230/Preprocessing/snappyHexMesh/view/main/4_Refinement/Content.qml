import QtQuick 2.4

import DICE.App 1.0
import DICE.App.Foam 1.0

import "Tabs"
import "RefinementObjects"
import "../../menus"

Body {
    property alias treeView: treeView

    Card {
        Subheader { text: "Geometry objects" }
        TreeView {
            id: treeView

            maxHeight: 300
            width: parent.width
            modelData: app.treeViewModel
            menu: RightClickMenu {}
        }
    }

    RefinementObjects {}

    TabsCard {
        SurfaceRefinement {}
        RegionRefinement {}
        Layers {}
        FeatureRefinement {}
    }
}
