#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, requests
import subprocess
import socket, fcntl, struct

from PyQt4 import QtGui, QtCore, uic

def get_ip_address(ifname): # http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
	s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	ip = socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915, # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

	return ip

def what_is_my_ip():
	values = {'comm': lauchAndPort}
	r = requests.get("http://30.10.23.18:8080/control3434", params= values)

class TestApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
 
        self.ui = uic.loadUi('mainwindow.ui')
        self.ui.show()

        self.ui.ipSetting.setText()

        self.connect(self.ui.advancedButton, QtCore.SIGNAL("clicked()"), changeStackedWidget)
        self.connect(self.ui.start_button, QtCore.SIGNAL("clicked()"), start_stream)

pop = None
commandList = []

def start_stream():
	global pop

	_IP = win.ui.ipSetting.text()
	_PORT = win.ui.portSetting.text()
	_MBIT = win.ui.mbitCombo.currentText() + "000"
	_RESOLUTION = win.ui.resolutionSetting.currentText()
	_FPS = win.ui.fpsSetting.currentText()
	_BITRATE = win.ui.bitrate_edit.text()
	_MAX_BITRATE = win.ui.max_bitrate_edit.text()
	_SLICE_MAX_SIZE = win.ui.slice_max_size_edit.text()

	# process calistir

	commandList = []
	commandList.append("./server2.sh")
	commandList.append(_FPS)
	commandList.append(_RESOLUTION)
	commandList.append(_BITRATE)
	commandList.append(_MAX_BITRATE)
	commandList.append(_SLICE_MAX_SIZE)
	commandList.append(_IP + ':' + _PORT)

	if pop == None:
		pop = subprocess.Popen(commandList)
		lauchAndPort = "opengstlaunch-start " + str(_PORT)
		print lauchAndPort
		values = {'comm': lauchAndPort}
		r = requests.get("http://30.10.23.18:8080/control3434", params= values)
	else:
		pop.terminate()
		pop = None
		values = {'comm': "opengstlaunch-stop"}
		r = requests.get("http://30.10.23.18:8080/control3434", params= values)


	# print _IP, _PORT, _MBIT, _RESOLUTION, _FPS, _BITRATE, _MAX_BITRATE

def changeStackedWidget():
	win.ui.stackedWidget.setCurrentIndex( (win.ui.stackedWidget.currentIndex() + 1) % 2)

 
if __name__ == "__main__":
	try:
		app = QtGui.QApplication(sys.argv)
		win = TestApp()
		sys.exit(app.exec_())
	finally: 
		if pop != None:
			pop.terminate()
			print "program kapandi"