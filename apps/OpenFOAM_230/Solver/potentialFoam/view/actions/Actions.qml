import QtQuick 2.4
import QtQuick.Controls 1.3

Item {

    // External Tools
    // ==============
    property Action openParaview: Action {
        text: "Open Paraview"
        tooltip: text
        iconSource: "images/openParaview.svg"
        iconName: text
        onTriggered:  {
            app.call("open_paraview")
        }
    }

    property Action reloadApp: Action{
        text: "Reload Application"
        iconName: text
        onTriggered: {
            app.call("load")
        }
    }
}
