import QtQuick 2.4
import QtQuick.Controls 1.2
import DICE.App 1.0

Body {

    Card {
        FlatButton {
            text: "run"
            onClicked: app.call("run")
        }

        TextArea {
            id: textArea
            width: parent.width
            height: 500
            Keys.onPressed: {
                var key = event.text.replace(/^\s+|\s+$/g, '')
                switch (event.key) {
                case Qt.Key_Enter:
                    key = "\n"
                    break;
                case Qt.Key_Return:
                    key = "\n"
                    break;
                case Qt.Key_Space:
                    key = " "
                    break
                }
                app.call("send_key", [key])
            }
            Component.onCompleted: {
                app.setCallback("outputReceived", function(output) {
                    textArea.text += output
                })
            }
        }
    }
}
