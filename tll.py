#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, signal
import subprocess
import shlex

def log(s):
    sys.stderr.write("%s\n" % s)

log("started")

pop = None
streamPop = None

path = "/home/pi/files/"
pipePath = "/home/pi/dosya"

loop = True
trans = None
FNULL = open(os.devnull, 'w')

while loop:
    
    trans = open(pipePath).read()
    log("trans : " + trans)
    
    if trans.find("xdotool",0) != -1:
        print trans.split(' ')
        subprocess.Popen(shlex.split(trans)) # shlex.split ile listeye donustur
    elif trans.find("kill", 0)  != -1:
        if pop == None:
            log("Program yok, kill hatali")
        else:
            pop.terminate()
            pop = None
            log("Program Kapatildi")
    elif trans.find("opengstlaunch-start", 0) != -1 :
        
        log(trans.split(' '))
        

        senderIp = trans.split(' ')[2]
        senderPort = trans.split(' ')[1]

        commandStream = "gst-launch-1.0 -v tcpclientsrc host=" + str(senderIp) + " port=" + str(senderPort) + " ! h264parse ! omxh264dec ! autovideosink sync=false"
        log(shlex.split(commandStream))
        streamPop = subprocess.Popen(shlex.split(commandStream))
    elif trans.find("opengstlaunch-stop", 0) != -1 :
        log(trans.split(' '))
        if streamPop == None:
            log("stream yok kill hatali")
        else:
            streamPop.terminate()
            streamPop = None

    else:
        # program
        if pop == None:
            # yeni ac
            try:
                command = None
                trans = trans.split('.')
                if trans[1] == "png":
                    command = "%s%s%s%s%s%s" %("ristretto ", path, trans[0], ".", trans[1], " --fullscreen")
                    log(command)
                elif trans[1] == "mp4" or trans[1] == "mkv":
                    command = "%s%s%s%s%s%s" %("xterm -e omxplayer ", path, trans[0], ".", trans[1], "")
                elif trans[1] == "pdf":
                    command = "%s%s%s%s%s%s" %("evince ", path, trans[0], ".", trans[1], " --fullscreen ")
                
                pop = subprocess.Popen(shlex.split(command)) # shlex.split ile listeye donustur
                trans = None
            except Exception as e:
                log("Exception: %s" %(e))
                continue
        else:
            # program zaten var. hata ver
            log("Calisan program var!!!")