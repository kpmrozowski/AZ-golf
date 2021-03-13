import QtQuick 2.12

//import Shapes 1.0
import QtQuick.Window 2.12

Window {
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World!!!")
}
Item {
    width: 300; height: 200

    Ellipse: {
        id: ellipse
        anchors.fill: parent,
        anchors.margins: 50
        color: "blue"
    }
    Timer {
        interval: 2000
        running: true
        onTriggered: ellipse.color = "red"
    }
}

