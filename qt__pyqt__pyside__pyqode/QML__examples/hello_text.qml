import QtQuick 2.3

Rectangle {
    width: 360
    height: 360

    Text {
        id: helloText
        objectName: "helloText"

        text: qsTr("Click me!")
        anchors.centerIn: parent
        font.pointSize: 24
        font.bold: true

        MouseArea {
            anchors.fill: parent
            onClicked: {
                helloText.text = qsTr("Hello World!");
            }
        }
    }
}