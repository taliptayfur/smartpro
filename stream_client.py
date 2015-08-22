#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, requests
import subprocess
import socket, fcntl, struct
from PyQt4 import QtGui, QtCore, uic

raspberry_ip = "192.168.223.88"
raspberry_port = "8080"
raspberry_ip_page = "whatismyip3534"
raspberry_control_page = raspberry_ip + ":" + raspberry_port + "/" + "control3434"

def get_ip_address(ifname): # http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
	s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	ip = socket.inet_ntoa( fcntl.ioctl(
		s.fileno(), 0x8915, # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
		)[20:24])

	return ip

def what_is_my_ip(server_ip, server_port, server_page):
	#values = {'comm': lauchAndPort}
	#r = requests.get("http://" + raspberry_control_page, params= values)
	r = requests.get("http://" + server_ip + ":" + server_port + "/" + server_page)
	return str(r.content)

win = None
commandList = []

uiMainWindow = uic.loadUiType('mainwindow.ui')[0]

class TestApp(QtGui.QMainWindow, uiMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.screen_window = None
		self.setupUi(self)

		#self.ui.setStyleSheet("*{background-color:rgba(0,0,0,10)}")
		#self.ui.actionExit.triggered.connect(self.close)

		# self.ipSetting.setText( what_is_my_ip(raspberry_ip, raspberry_port, raspberry_ip_page) ) # get ip from web server runs on raspberry pi

		#self.connect(self.ui.advancedButton, QtCore.SIGNAL("clicked()"), changeStackedWidget)
		#self.connect(self.ui.start_button, QtCore.SIGNAL("clicked()"), start_stream)

		#self.connect(self.ui.pos_set_button, QtCore.SIGNAL("clicked()"), self.inflateScreenPos)

	@QtCore.pyqtSlot()
	def on_pos_set_button_clicked(self):
		try:
			#width, height = self.screen_pos.text().split(',')
			#width, height = int(width), int(height)
			width, height = (int(i) for i in self.resolutionSetting.currentText().split('x'))
		except:
			width, height = 640, 480
		try:
			x, y = (int(i) for i in self.screen_pos.text().split(','))
		except:
			x, y = 0, 0

		if self.screen_window != None:
			self.screen_window.close()
		self.screen_window = ScreenPosWindow(x, y, width, height, self.setPosition)

	@QtCore.pyqtSlot()
	def on_start_button_clicked(self):
		_IP = win.ipSetting.text()
		_PORT = win.portSetting.text()
		_MBIT = win.mbitCombo.currentText() + "000" # "20" + "000" gibi
		_RESOLUTION = win.resolutionSetting.currentText()
		_FPS = win.fpsSetting.currentText()
		_BITRATE = win.bitrate_edit.text()
		_MAX_BITRATE = win.max_bitrate_edit.text()
		_SLICE_MAX_SIZE = win.slice_max_size_edit.text()
		_SCREEN_POS = win.screen_pos.text()
		start_stream(_IP, _PORT, _MBIT, _RESOLUTION, _FPS, _BITRATE, _MAX_BITRATE, _SLICE_MAX_SIZE, _SCREEN_POS)
		if stream_info() == True:
			self.start_button.setText("Durdur")
		else:
			self.start_button.setText("Başlat")

	@QtCore.pyqtSlot()
	def on_advancedButton_clicked(self):
		self.stackedWidget.setCurrentIndex( (self.stackedWidget.currentIndex() + 1) % 2)

	def setPosition(self, x, y):
		self.screen_pos.setText("%s,%s" % (x, y))

	def closeEvent(self, event):
		print "TestApp.closeEvent"
		if self.screen_window != None:
			self.screen_window.close()
			self.screen_window = None

	################################################

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
		qp.drawRect(0,0, 1366, 768)

		qp.setCompositionMode (QtGui.QPainter.CompositionMode_Source)
		qp.setBrush(QtGui.QColor(0, 255, 0, 0))
		qp.drawRect(self.x, self.y, self.width, self.height)
		qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
	
	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			self.x = event.pos().x()
			self.y = event.pos().y()

		self.update()

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
		self.f_setPosition(self.x, self.y)

	def closeEvent(self, event):
		print "ScreenPosWindow.closeEvent"

################################### stream ##########################################################

pop = None

def stream_info():
	return pop != None

def start_stream(_IP, _PORT, _MBIT, _RESOLUTION, _FPS, _BITRATE, _MAX_BITRATE, _SLICE_MAX_SIZE, _SCREEN_POS):
	global pop
	# process calistir

	commandList = []
	commandList.append("./server_libav.sh")
	commandList.append(_FPS)
	commandList.append(_RESOLUTION)
	commandList.append(_BITRATE)
	commandList.append(_MAX_BITRATE)
	commandList.append(_SLICE_MAX_SIZE)
	commandList.append(_IP + ':' + _PORT)
	commandList.append(_SCREEN_POS)

	if pop == None:
		pop = subprocess.Popen(commandList)
		lauchAndPort = "opengstlaunch-start " + str(_PORT)
		values = {'comm': lauchAndPort}
		r = requests.get("http://" + raspberry_control_page, params= values)
	else:
		pop.terminate()
		pop = None
		values = {'comm': "opengstlaunch-stop"}
		r = requests.get("http://" + raspberry_control_page, params= values)
		

	# print _IP, _PORT, _MBIT, _RESOLUTION, _FPS, _BITRATE, _MAX_BITRATE

if __name__ == "__main__":
	try:
		app = QtGui.QApplication(sys.argv)
		win = TestApp()
		win.show()
		sys.exit(app.exec_())
	finally:
		if win.screen_window != None:
			win.screen_window = None
			print "finally screen_window"

		if pop != None:
			pop.terminate()
			print "program kapandi"
