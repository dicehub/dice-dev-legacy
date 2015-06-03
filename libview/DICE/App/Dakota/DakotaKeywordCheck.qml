import QtQuick 2.4

Item {
    id: root

    property bool exists
    property string path

    function createDict(defaultValue) {
        if (defaultValue === undefined) defaultValue = {}
        app.call("create_dict_in_path", [path, defaultValue], function(returnValue) {checkIfKeywordExists()})
    }

    function removeKeyword() {
        app.call("remove_from_dict", [path], function(returnValue) {checkIfKeywordExists()})
    }

    function checkIfKeywordExists() {
        app.call("dakota_keyword_exists", [path], function(returnValue) {exists = returnValue} )
    }

    onPathChanged: {
        if (path !== undefined) {
            checkIfKeywordExists()
        }
    }
}
