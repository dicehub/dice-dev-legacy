import DICE.App 1.0

CheckBoxButton {
    id: root

    property string path
    property var defaultValue: ""


    methodName: "dakota_option"

    callParameter: {
        if (defaultValue !== "")
            [root.path, defaultValue]
        else
            root.path
    }

    property string helpPath: "dakota/"+path

    width: parent.width

    onActiveFocusChanged: {
        if (activeFocus) {
            appWindow.helpPath = root.helpPath
        }
    }
}

