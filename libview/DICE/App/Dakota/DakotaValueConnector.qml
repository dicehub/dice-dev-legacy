import QtQuick 2.4

import DICE.App 1.0

PythonValueConnector {
    id: root

    methodName: "dakota_var"

    property alias path: root.callParameter
}

