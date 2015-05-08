import QtQuick 2.4
import DICE.App 1.0

Body {
    Card {
        Subheader { text: "Description" }
        BodyText {
            text: "Sampling experiment"
        }
    }
    Card {
        Subheader { text: "Input" }
        List {
            maxHeight: 300
            width: parent.width
            modelData: app.input_types_model
            delegate: ListItem {
                text: input_type
            }
        }
    }
    Card {
        Subheader { text: "Output" }
        List {
            maxHeight: 300
            width: parent.width
            modelData: app.output_types_model
            delegate: ListItem {
                text: output_type
            }
        }
    }
}
