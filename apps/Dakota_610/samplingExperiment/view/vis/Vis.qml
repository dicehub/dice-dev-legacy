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
        if (reloadWebEngine) {
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
            runJavaScript(changePlotSize(webEngineView.width, webEngineView.height))
        }
        onHeightChanged: {
            runJavaScript(changePlotSize(webEngineView.width, webEngineView.height))
        }
        onLoadingChanged: {
            if (!loading) {
                runJavaScript(changePlotSize(webEngineView.width, webEngineView.height))
            }
        }
    }

    function changePlotSize(width, height) {
        return "Bokeh.Collections('Plot').at(0).set('plot_width'," + width*0.95 + ");"
        + "Bokeh.Collections('Plot').at(0).set('plot_height'," + height*0.9 + ");"
    }
}
