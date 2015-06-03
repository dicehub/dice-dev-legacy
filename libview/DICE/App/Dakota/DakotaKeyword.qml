import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3
import QtQuick.Layouts 1.1

import DICE.App 1.0
import DICE.Theme 1.0
import DICE.Components 1.0 as DC

FocusScope {
    id: root

    property alias path: valueConnector.path
    property alias methodName: valueConnector.methodName
    property alias getMethod: valueConnector.getMethod
    property alias setMethod: valueConnector.setMethod
    property alias changeSignalMethod: valueConnector.changeSignalMethod
    property alias label: label.text
    property alias optional: valueConnector.optional

    property string helpPath: "dakota/"+path

    width: parent.width
    height: Math.max(toggleButton.height, label.height)

    onActiveFocusChanged: {
        if (activeFocus) {
            appWindow.helpPath = root.helpPath
        }
    }

    DakotaValueConnector {
        id: valueConnector

        optional: true
//        enabled: toggleButton.enabled
    }

    MouseArea {
       anchors.fill: parent
       onClicked: root.forceActiveFocus(Qt.MouseFocusReason)
    }

    RowLayout {
        width: parent.width
        height: parent.height
        spacing: 0

        Item {
            Layout.fillWidth: true
            height: parent.height

            BasicText {
                id: label

                width: parent.width
                anchors.verticalCenter: parent.verticalCenter
                text: ""
                color: root.activeFocus ? colors.highlightColor : "#333"
                verticalAlignment: Text.AlignVCenter

                transitions: Transition {
                    ColorAnimation { duration: 300 }
                }
            }
        }

        Item {
            width: 20
            height: parent.height
        }

        Item {
            Layout.fillWidth: true
            height: parent.height

            DC.ToggleButton {
                id: toggleButton

                width: parent.width
                visible: valueConnector.optional
                checked: valueConnector.optionalEnabled
                onCheckedChanged: {
                    if (checked !== valueConnector.optionalEnabled)
                        valueConnector.toggleOptionalEnabled()
                }
                // needs to be here because toglleButton binding is gone after click
                property bool valueConnctorState: valueConnector.optionalEnabled
                onValueConnctorStateChanged: checked = valueConnctorState
            }
        }
    }
}
