
import QtQuick 2.0
import QtQuick.Window 2.3

import "."

Window {
    id: root
    visible: true
    width: 1000
    height: 1000
    title: "Paint!"


    Rectangle {
        id: tools
        width: parent.width
        height: 150
        color: "#545454"

        property color paintColor: "#33B5E5"
        property int thickness: 1
        property int spacing: 4

        Column {
            spacing: tools.spacing
            anchors.centerIn: parent

            Row {
                spacing: tools.spacing
                anchors.horizontalCenter: parent.horizontalCenter

                Repeater {
                    model: ["#33B5E5", "#99CC00", "#FFBB33", "#FF4444"]
                    Square {
                        active: tools.paintColor === color
                        color: modelData
                        onClicked: tools.paintColor = color
                    }
                }
            }

            Row {
                spacing: tools.spacing
                anchors.horizontalCenter: parent.horizontalCenter

                Repeater {
                    model: [1,2,3,4,5]

                    Circle {
                        id: circle
                        active: tools.thickness === thickness
                        thickness: modelData
                        text: thickness
                        onClicked: tools.thickness = thickness
                    }
                }
            }
        }

        // строка состояния автосохранения
        Text {
            id: save_status
            anchors {
                right: parent.right
                bottom: parent.bottom
                margins: 8
            }
            color: "white"
            text: "Автосохранение: изменений нет"
        }

    }

    // получаем сигнал saved из Python
    Connections {
        target: _backend

        function onSaved(path, time) {
            save_status.text = "Автосохранение: " + time
        }
    }

    Canvas {
        id: canvas
        objectName: "canvas"    // имя для поиска из Python

        anchors {
            left: parent.left
            right: parent.right
            top: tools.bottom
            bottom: parent.bottom
            margins: 8
        }

        property real lastX
        property real lastY
        property color color: tools.paintColor
        property bool isInitialized: false

        // метод для вызова из Python, возвращает результат сохранения
        function saveCanvas(filePath) {
            return canvas.save(filePath)
        }

        // первая отрисовка — белый фон, чтобы в файле не было прозрачности
        Component.onCompleted: requestPaint()

        onPaint: {
            var ctx = getContext("2d")

            // При первом запуске заливаем холст белым цветом
            if (!isInitialized) {
                ctx.fillStyle = "white"
                ctx.fillRect(0, 0, canvas.width, canvas.height)
                isInitialized = true
                return
            }

            // onPaint вызывается и самим Qt (например, при изменении размера) —
            // рисуем только во время движения с зажатой кнопкой мыши
            if (!paint_area.pressed)
                return

            // Отрисовка линии
            ctx.lineWidth = tools.thickness
            ctx.strokeStyle = canvas.color
            ctx.lineCap = "round"
            ctx.beginPath()
            ctx.moveTo(lastX, lastY)

            lastX = paint_area.mouseX
            lastY = paint_area.mouseY

            ctx.lineTo(lastX, lastY)
            ctx.stroke()

            // сообщаем backend, что рисунок изменился
            _backend.markDirty()
        }

        MouseArea {
            id: paint_area
            anchors.fill: parent

            onPressed: {
                canvas.lastX = mouseX
                canvas.lastY = mouseY
            }

            onPositionChanged: {
                canvas.requestPaint()
            }
        }
    }
}
