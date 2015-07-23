import QtQuick 2.4

import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        Subheader { text: "Run Controls" }

        FoamDropDown {
            label: "Start From"
            modelPath: "foam/controlDict startFrom"
            path: "system/controlDict startFrom"
        }
        FoamValue {
            label: "Start Time"
            path: "system/controlDict startTime"
            dataType: "int"
        }
        FoamDropDown {
            label: "Stop At"
            modelPath: "foam/controlDict stopAt"
            path: "system/controlDict stopAt"
        }
        FoamValue {
            label: "End Time"
            path: "system/controlDict endTime"
            dataType: "int"
        }
        FoamValue {
            label: "\u0394t [s]"
            path: "system/controlDict deltaT"
            dataType: "int"
        }
    }
    Card {
        Subheader { text: "Write Controls" }

        FoamDropDown {
            label: "Write Control"
            modelPath: "foam/controlDict writeControl"
            path: "system/controlDict writeControl"
        }
        FoamValue {
            label: "Write Interval"
            path: "system/controlDict writeInterval"
            dataType: "int"
        }
        FoamValue {
            label: "Purge Write"
            path: "system/controlDict purgeWrite"
            dataType: "int"
        }
        FoamRadioButtonGroup {
            label: "Write Format"
            modelPath: "foam/controlDict writeFormat"
            path: "system/controlDict writeFormat"
        }
        FoamValue {
            label: "Write Precision"
            path: "system/controlDict writePrecision"
            dataType: "int"
        }
        FoamDropDown {
            label: "Write Compression"
            modelPath: "foam/controlDict writeCompression"
            path: "system/controlDict writeCompression"
        }
        FoamDropDown {
            label: "Time Format"
            modelPath: "foam/controlDict timeFormat"
            path: "system/controlDict timeFormat"
        }
        FoamValue {
            label: "Time Precision"
            path: "system/controlDict timePrecision"
            dataType: "int"
        }
        FoamDropDown {
            label: "Graph Format"
            modelPath: "foam/controlDict graphFormat"
            path: "system/controlDict graphFormat"
        }
        FoamToggleButton {
            label: "runTimeModifiable"
            path: "system/controlDict runTimeModifiable"
        }
    }
}
