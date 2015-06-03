import QtQuick 2.4
import DICE.App 1.0

import DICE.App.Dakota 1.0

Body {
    Card {
        Subheader { text: "Environment Information" }
        DakotaValue {
            label: "Tabular Graphics File"
            path: "input.in environment tabular_graphics_file"
            readOnly: true
        }
        DakotaValue {
            label: "Method Pointer"
            path: "input.in environment method_pointer"
            readOnly: true
        }
    }
}

