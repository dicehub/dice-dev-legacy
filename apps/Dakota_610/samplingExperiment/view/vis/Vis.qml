import QtQuick 2.4
import QtWebEngine 1.0

import DICE.App 1.0

Rectangle {
    id: root

    property string plotHTMLpath: app.plotHTMLPath
    property bool reloadWebEngine: app.reloadWebEngine

    onPlotHTMLpathChanged: {
        webEngineView.load(plotHTMLpath)
    }

    onReloadWebEngineChanged: {
        print(reloadWebEngine)
        if (reloadWebEngine) {
            print("Reload")
            webEngineView.reload()
        }
    }

    anchors.fill: parent

    WebEngineView {
        id: webEngineView

        function load(url) {
            webEngineView.url = url
        }

        anchors.fill: parent
        onWidthChanged: {
            app.setPlotWidth(width*0.95)
        }
        onHeightChanged: {
            app.setPlotHeight(height*0.90)
        }
    }
}
