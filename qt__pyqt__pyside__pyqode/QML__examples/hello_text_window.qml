import QtQuick 2.0
import QtQuick.Window 2.0

Window {
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World") //The method qsTr() is used for translations from one language to other.

    Text {
        id: helloText
        text: qsTr("Click me!")
        anchors.centerIn: parent
        font.pointSize: 24; font.bold: true

        MouseArea {
            anchors.fill: parent
            onClicked: {
                helloText.text = "Hello World!";
            }
        }
    }
}