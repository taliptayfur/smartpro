#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, requests
import subprocess
import socket, fcntl, struct
from PyQt4 import QtGui, QtCore, uic

from stream_pos import ScreenPosWindow

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
		start_stream(_IP, _PORT, _MBIT, _RESOLUTION, _FPS, _BITRATE,
					 _MAX_BITRATE, _SLICE_MAX_SIZE, _SCREEN_POS)
		if stream_info() == True:
			self.start_button.setText("Durdur")
		else:
			self.start_button.setText("Başlat")

	@QtCore.pyqtSlot()
	def on_advancedButton_clicked(self):
		self.stackedWidget.setCurrentIndex( (self.stackedWidget.currentIndex() + 1) % 2) # sayfalar arası geçiş

	@QtCore.pyqtSlot(int)
	def on_mbitCombo_activated(self, index):
		self.setMegabitSetting(self.mbitCombo.currentText())

	def setMegabitSetting(self, mbit):
		self.bitrate_edit.setText(str(mbit + "000"))
		self.max_bitrate_edit.setText( str(int(int(mbit + "000") * (1.75))) )

	def setPosition(self, x, y):
		self.screen_pos.setText("%s,%s" % (x, y))

	def closeEvent(self, event):
		print "TestApp.closeEvent"
		if self.screen_window != None:
			self.screen_window.close()
			self.screen_window = None

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
