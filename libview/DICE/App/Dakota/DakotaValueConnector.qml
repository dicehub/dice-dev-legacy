import QtQuick 2.4

import DICE.App 1.0

PythonValueConnector {
    id: root

    methodName: "dakota_var"

    property bool optional: false
    property bool optionalEnabled: false

    property bool notOptionalOrEnabled: !optional || optionalEnabled

    property alias path: root.callParameter

    function toggleOptionalEnabled() {
        if (path !== "") {
            app.call("set_invalid_or_remove_var", [path, !optionalEnabled], function(returnValue) {
                optionalEnabled = !optionalEnabled
            })
        }
    }

    function deleteDakotaVar() {
        if (optionalEnabled) {
            optionalEnabled = false
            toggleOptionalEnabled()
        }
    }

    function __loadOptionalEnabled() {
        if (path !== "") {
            app.call("dakota_keyword_exists", [path], function(returnValue) {
                optionalEnabled = returnValue
                if (returnValue)
                    load() // load the value if the dakota_keyword exists
            })
        }
    }

    Component.onCompleted: {
        if (optional)
            __loadOptionalEnabled()
    }

    property Connections parentConn: Connections {
        target: parent
        onVisibleChanged: {
            if (root.optional)
                root.__loadOptionalEnabled()
        }
    }

    onEnabledChanged: {
        if (optional && !enabled)
            value = ""

        if (optional)
            __loadOptionalEnabled()
    }

    onPathChanged: {
        load()
        if (optional)
            __loadOptionalEnabled()
    }
}

