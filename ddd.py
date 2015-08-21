# Temperature-conversion program using PyQt

import sys
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("mainwindow.ui")[0]                 # Load the UI

class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #self.start_button.clicked.connect(self.start_stream)  # Bind the event handlers
        #self.btn_FtoC.clicked.connect(self.btn_FtoC_clicked)  #   to the buttons
        #self.pos_set_button.clicked.connect(self.inflateScreenPos)
        self.screen_window = None

    @QtCore.pyqtSlot()
    def on_pos_set_button_clicked(self):
        if self.screen_window == None:
            self.screen_window = ScreenPosWindow()
        else :
            self.screen_window = None

    @QtCore.pyqtSlot()
    def on_start_button_clicked(self):
        print "deneme"

    def closeEvent(self, event):
        print "TestApp.closeEvent"
        if self.screen_window != None:
            self.screen_window.close()
            self.screen_window = None

class ScreenPosWindow(QtGui.QWidget):
    x = 0; y = 0;
    width = 10#win.ui.screen_pos.text().split(',')[0]
    height = 10#win.ui.screen_pos.text().split(',')[1]
    
    def __init__(self):
        QtGui.QWidget.__init__(self)

        #http://stackoverflow.com/questions/19944636/pyqt-transparent-background-qglwidget
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        #self.ui.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.showFullScreen()
    
    def paintEvent(self, e): # http://www.zetcode.com/gui/pyqt4/drawing/  -- QTGui.QPen
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()
    
    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.blue, 5, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawRect(self.x, self.y, self.width, self.height)

        #qp.drawLine(self.x, self.y, self.x + self.width, self.y) # yatay ust cizgi
        #qp.drawLine(self.x, self.y, self.x, self.y + self.height) # dikey sol cizgi
        #qp.drawLine(self.x, self.y + self.height, self.x + self.width, self.y + self.height) # yatay alt cizgi
        #qp.drawLine(self.x + self.width, self.y, self.x + self.width, self.y + self.height) # dikey sag cizgi

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_Left:
            self.x -= 5;
            self.update()
        elif e.key() == QtCore.Qt.Key_Right:
            self.x += 5;
            self.update()
        elif e.key() == QtCore.Qt.Key_Up:
            self.y -= 5;
            self.update()
        elif e.key() == QtCore.Qt.Key_Down:
            self.y += 5;
            self.update()

    def closeEvent(self, event):
        pass


app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()