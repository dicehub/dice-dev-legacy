import QtQuick 2.4

import DICE.App 1.0

Card {
    enabled: !!treeView.currentNode && treeView.currentNode.model.isRefinementObject
    visible: enabled

    Subheader { text: treeView.currentNodeText + " (" + treeView.currentNodeType +  ")" }

    SearchableBox {
        property bool isSearchableBox: treeView.currentNodeType === "searchableBox"

        enabled: isSearchableBox
        visible: enabled

        min_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " min"
        max_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " max"
    }
    SearchableSphere {
        property bool isSearchableSphere: treeView.currentNodeType === "searchableSphere"

        enabled: isSearchableSphere
        visible: enabled

        centre_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " centre"
        radius_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " radius"
    }
    SearchableCylinder {
        property bool isSearchableCylinder: treeView.currentNodeType === "searchableCylinder"

        enabled: isSearchableCylinder
        visible: enabled

        point_1_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " point1"
        point_2_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " point2"
        radius_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " radius"
    }
    SearchablePlate {
        property bool isSearchablePlate: treeView.currentNodeType === "searchablePlate"

        enabled: isSearchablePlate
        visible: enabled

        origin_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " origin"
        span_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " span"
    }
    SearchablePlane_PointAndNormal {
        property bool isSearchablePlane_PointAndNormal: treeView.currentNodeType === "searchablePlanePaN"

        enabled: isSearchablePlane_PointAndNormal
        visible: enabled

        basePoint_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " pointAndNormalDict basePoint"
        normalVector_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " pointAndNormalDict normalVector"
    }
    SearchablePlane_3Points {
        property bool isSearchablePlane_3Points: treeView.currentNodeType === "searchablePlane3P"

        enabled: isSearchablePlane_3Points
        visible: enabled

        point1_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " embeddedPointsDict point1"
        point2_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " embeddedPointsDict point2"
        point3_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " embeddedPointsDict point3"
    }
    SearchableDisk {
        property bool isSearchableDisk: treeView.currentNodeType === "searchableDisk"

        enabled: isSearchableDisk
        visible: enabled

        origin_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " origin"
        normal_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " normal"
        radius_path: "system/snappyHexMeshDict geometry " + treeView.currentNodeText + " radius"
    }

    FlatButton {
        text: "Delete"
        onClicked: {
            app.call("remove_refinement_object", [treeView.currentNodePath[0]])
        }
    }
}

