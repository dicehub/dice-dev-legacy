import QtQuick 2.4

import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        Subheader { text: "Pressure [Pa]" }
        ValueField {
            label: "internalField"
            methodName: "pressure_init_field"
        }
        Subheader { text: "Velocity [m/s]" }
        VectorField {
            methodName: "velocity_init_field"
        }
    }
}
