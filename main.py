try:
    from PySide2 import QtCore, QtWidgets
    from PySide2 import QtGui
except ImportError:
    from PyQt5 import QtCore
    from PyQt5 import QtGui


def hex2QColor(c):
    r=int(c[0:2],16)
    g=int(c[2:4],16)
    b=int(c[4:6],16)
    return QtGui.QColor(r,g,b)


class RoundedWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RoundedWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.draggable = True
        self.dragging_threshould = 5
        self.__mouse_pressed_position = None
        self._mouse_move_positions = None
        self.backgroundColor = hex2QColor("6272a4")
        self.foregroundColor = hex2QColor("333333")
        self.broder_radius = 10
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(QtWidgets.QSizeGrip(self), 0,
                         QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.setMinimumSize(400, 400)

    def paintEvent(self, event):
        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.foregroundColor)
        qp.setBrush(self.backgroundColor)
        qp.drawRoundedRect(0, 0, s.width(), s.height(),
                           self.broder_radius, self.broder_radius)
        qp.end()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == QtCore.Qt.LeftButton:
            self.__mouse_pressed_position = event.globalPos()                # global
            self._mouse_move_positions = event.globalPos() - self.pos()    # local
        super(RoundedWindow, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & QtCore.Qt.LeftButton:
            global_position = event.globalPos()
            moved = global_position - self.__mouse_pressed_position

            if moved.manhattanLength() > self.dragging_threshould:
                difference = global_position - self._mouse_move_positions
                self.move(difference)
                self._mouse_move_positions = global_position - self.pos()
        super(RoundedWindow, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mouse_pressed_position is not None:
            if event.button() == QtCore.Qt.LeftButton:
                moved = event.globalPos() - self.__mouse_pressed_position
                if moved.manhattanLength() > self.dragging_threshould:
                    event.ignore()
                self.__mouse_pressed_position = None

        super(RoundedWindow, self).mouseReleaseEvent(event)

        if event.button() == QtCore.Qt.RightButton:
            QtWidgets.QApplication.exit()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = RoundedWindow()
    main.show()
    sys.exit(app.exec_())