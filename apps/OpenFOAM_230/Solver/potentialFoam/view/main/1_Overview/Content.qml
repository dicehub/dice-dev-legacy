import DICE.App 1.0

Body {
    Card {
        header: CenteredImage {
            height: 100
            color: "#5D536C"
            source: "images/potentialFoam.svg"
        }
        Subheader { text: "Description" }
        BodyText {
            text: "Simple potential flow solver which can be used to generate starting fields for full Navier-Stokes codes  "
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
