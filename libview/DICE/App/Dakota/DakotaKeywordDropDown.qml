import DICE.App 1.0

DropDown {
    id: root

    property string path
    callParameter: {
        if (modelPath !== "") {
            [path, getModelMethod, modelPath]
        }
        else {
            [path, getModelMethod]
        }
    }
    property string helpPath: "dakota/"+path+" "+currentText

    methodName: "dakota_keyword"
    changeSignalMethod: ""

    onActiveFocusChanged: {
        if (activeFocus) {
            appWindow.helpPath = root.helpPath
        }
    }
}

