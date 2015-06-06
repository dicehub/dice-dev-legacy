import QtQuick 2.4
import QtQuick.Controls 1.3

Menu {
    title: "DICE"

    MenuItem {
        action: !!mainWindow.getCoreApp("Home") ? mainWindow.getCoreApp("Home").actions.createNewProjectAction : null
    }
    MenuItem {
        action: !!mainWindow.getCoreApp("Home") ? mainWindow.getCoreApp("Home").actions.loadProjectAction : null
    }
    MenuItem {
        action: !!mainWindow.getCoreApp("Home") ? mainWindow.getCoreApp("Home").actions.openDiceSettingsAction : null
    }

    MenuSeparator {}

    MenuItem {
        action: actions.tooggleToolBar
    }
    MenuItem {
        action: actions.tooggleNaviBar
    }

    MenuSeparator {}

    MenuItem {
        action: actions.quitDiceAction
    }
}
