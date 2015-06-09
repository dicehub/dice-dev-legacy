import DICE.App 1.0

CheckBoxButton {
    id: root


    property string path
    property var defaultValue: ""


    methodName: "lower_bounds"

    callParameter: {
        if (defaultValue !== "")
            [root.path, defaultValue]
        else
            root.path
    }
//    property alias methodName: __valueConnector.methodName
//    property alias getMethod: __valueConnector.getMethod
//    property alias setMethod: __valueConnector.setMethod
//    property alias changeSignalMethod: __valueConnector.changeSignalMethod

//    property alias callParameter: __valueConnector.callParameter

    property string helpPath: "dakota/"+path

    width: parent.width

    onActiveFocusChanged: {
        if (activeFocus) {
            appWindow.helpPath = root.helpPath
        }
    }

//    valueConnector: DakotaValueConnector {
//        id: __valueConnector
//        path: root.path
//        enabled: root.enabled
//    }
}

