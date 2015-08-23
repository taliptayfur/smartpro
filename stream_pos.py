#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class ScreenPosWindow(QtGui.QWidget):
	
	def __init__(self, x, y, width, height, f_setPosition):
		QtGui.QWidget.__init__(self)
		self.x, self.y = x, y

		self.width, self.height = width, height
		self.f_setPosition = f_setPosition

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
		pen = QtGui.QPen(QtCore.Qt.blue, 0, QtCore.Qt.SolidLine)
		qp.setPen(pen)

		qp.setBrush(QtGui.QColor(0, 0, 0, 160))
		qp.drawRect(0,0, self.geometry().width(), self.geometry().height())

		qp.setCompositionMode (QtGui.QPainter.CompositionMode_Source)
		qp.setBrush(QtGui.QColor(0, 255, 0, 0))
		qp.drawRect(self.x, self.y, self.width, self.height)
		qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)

	def mousePressEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton: # fare sol tusa ilk tiklandiginda farenin koordinatlari aliniyor
			self.x1 = event.pos().x()
			self.y1 = event.pos().y()

	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			self.tmp = self.x
			self.tmp -= self.x1 - event.pos().x()

			if self.tmp >= 0 and self.tmp + self.width <= self.geometry().width(): # eger fark eklenince sınırları geçmiyorsa yap
				self.x -= self.x1 - event.pos().x()

			self.tmp = self.y
			self.tmp -= self.y1 - event.pos().y()
			
			if self.tmp >= 0 and self.tmp + self.height <= self.geometry().height():
				self.y -= self.y1 - event.pos().y()

			self.x1 = event.pos().x()
			self.y1 = event.pos().y()

		self.f_setPosition(self.x, self.y)
		self.update()

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			self.close()
		elif e.key() == QtCore.Qt.Key_Left:
			if self.x - 5 >= 0:
				self.x -= 5
		elif e.key() == QtCore.Qt.Key_Right:
			if self.x + 5 + self.width<= self.geometry().width():
				self.x += 5
		elif e.key() == QtCore.Qt.Key_Up:
			if self.y - 5 >= 0:
				self.y -= 5
		elif e.key() == QtCore.Qt.Key_Down:
			if self.y - 5 + self.height<= self.geometry().height():
				self.y += 5

		self.update()
		self.f_setPosition(self.x, self.y)

	def closeEvent(self, event):
		print "ScreenPosWindow.closeEvent"
