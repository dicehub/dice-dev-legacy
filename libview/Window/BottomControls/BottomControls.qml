import QtQuick 2.4
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.3

import DICE.Components 1.0
import DICE.Theme 1.0

Rectangle {
    id: bottomControls

    property bool consoleExpanded : false
    property alias button1: cb1

    height: 28
    color: colors.bottomControlsColor

    TopBorder {}

    RowLayout {
        spacing: 10
        height: parent.height
        implicitWidth: 200

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 5
        anchors.topMargin: 0
        anchors.bottomMargin: 0

        ConsoleButton { id: cb1 }
    }

    Row {
        id: row

        property var currentApp: !!mainWindow.getCoreApp("Desk") ? mainWindow.getCoreApp("Desk").deskData.currentApp : null
        property string currentAppName: !!currentApp ? currentApp.name : ""
        property string currentAppStatus: !!currentApp ? currentApp.status : ""
        property color currentAppStatusColor: !!currentApp ? colors.appStatusColors[currentAppStatus] : "#000"


        spacing: 10
        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.verticalCenter: parent.verticalCenter
        height: parent.height

        MenuText {
            visible: !!parent.currentApp
            text: parent.currentAppName
            height: parent.height
            verticalAlignment: "AlignVCenter"
            font.family: fonts.codeTextFont
        }

        Rectangle {
            visible: !!parent.currentApp
            width: 1
            height: parent.height
            color: colors.borderColor
        }

        MenuText {
            visible: !!parent.currentApp
            text: parent.currentAppStatus
            color: parent.currentAppStatusColor
            height: parent.height
            verticalAlignment: "AlignVCenter"
            font.family: fonts.codeTextFont

            MouseArea {
                hoverEnabled: true
                anchors.fill: parent
                onClicked: {
                    statusMenu.__xOffset =
                    statusMenu.__yOffset = -parent.height
                    statusMenu.popup()
                }
            }

            Menu {
                id: statusMenu

                title: "status"
                MenuItem {
                    text: "Set to IDLE"
                    onTriggered: row.currentApp.status = "idle"
                }
            }
        }

        Rectangle {
            width: 1
            height: parent.height
            color: colors.borderColor
        }

        MenuText {
            property int usage: dice.memory.usage / 1024

            text: usage + " MB"
            height: parent.height
            verticalAlignment: "AlignVCenter"
            font.family: fonts.codeTextFont
        }
    }

    function expandConsole() {
        if (consoleExpanded === true)
            consoleExpanded = false;
        else
            consoleExpanded = true;
    }
}
