import traceback
from os import path
from sys import platform as _platform
import os
import subprocess
import time
from time import gmtime, strftime, localtime
import sys

import re
import requests
import thread

from common.contant import *


def selectLatestInAndroid(deviceId, path, word):
    global pids
    fileName = None
    fullfileName = None
    ing = True
    command ="adb -s " + deviceId + " shell ls -1t " + path
    while ing:
        ing = False
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        printEx( command )
        fd_popen = proc.stdout

        fileList = fd_popen.read().strip()
        for file in fileList.split('\r\n'):
            if (word == '' and '.' in file) or (word != '' and word in file):
                fileName = file
                fullfileName = path + file
                printEx( "%s(%s)" % ("fullfileName", fullfileName) )
                break
            elif 'Unknown' in file:
                """
              ls: Unknown option '-t'. Aborting.
              """
                ing = True
                pass

        try:
            proc.kill()
        except:
            printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

        if fileName == None and ing == True:
            command = "adb -s " + deviceId + " shell ls " + path
        else:
            break

    return fileName, fullfileName

def tapOnDevice(deviceId, location):
    proc = subprocess.Popen("adb -s " + deviceId + " shell input tap " + location,
                            stdout=subprocess.PIPE)
    fd_popen = proc.stdout
    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        printEx( "tap " + location )

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

def getDateInDevice(deviceId):
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell date +%H%M", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = list(line)
    printEx( "%s:%s" % ("date +%H%M", str(reVal)) )

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))
    return reVal

def getPidInDevice(deviceId, processName):
    reVal = 0
    proc = subprocess.Popen("adb -s " + deviceId + " shell ps", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        if processName in line:
            reVal = int(line.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').split(' ')[1])
            break

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def startActivity(deviceId, componentName, repeatCount):
    """
    adb shell am start -a android.intent.action.MAIN -n com.google.android.googlequicksearchbox/.SearchActivity
    Starting: Intent { act=android.intent.action.MAIN cmp=com.google.android.googlequicksearchbox/.SearchActivity launchParam=MultiScreenLaunchParams { mDisplayId=0 mBaseDisplayId=0 mFlags=0 } }
    """
    reVal = False

    def inner_Process(deviceId, componentName, repeatCount):
        reVal = False

        count = 0
        printEx("%s(%s)" % ("repeatCount In inner_Process()", repeatCount))
        while count < repeatCount:
            count = count + 1
            proc = subprocess.Popen("adb -s " + deviceId + " shell am start -a android.intent.action.MAIN -n " + componentName, stdout=subprocess.PIPE)
            printEx("%s(%s)" % ("count In inner_Process()", count))
            content = proc.stdout.read().strip()
            for line in content.split('\r\n'):
                if 'Starting' in line:
                    reVal = True

            try:
                proc.kill()
            except:
                printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

            if repeatCount > 1:
                time.sleep(1)

        printEx("%s(%s)" % ("reVal In inner_Process()", reVal))
        return reVal
    
    """
    if repeatCount == 1:
        reVal = inner_Process(deviceId, componentName, int(repeatCount))
    else:
    """
    thread.start_new_thread(inner_Process, (deviceId, componentName, int(repeatCount)))
    reVal = True

    return reVal

def killProcessInDevice(deviceId, pid):
    reVal = ''
    proc = subprocess.Popen("adb -s " + deviceId + " shell kill -9 " + str(pid), stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
            reVal = reVal + line

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def execCmdBackground(command):
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        time.sleep(5)
        #proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

def runMonkeyInDevice(deviceId, context):
    reVal = ''

    pid = getPidInDevice(deviceId, 'com.android.commands.monkey')
    if pid == 0:
        if context == None:
           #context = '--throttle 1000 --pct-appswitch 100 -s 1 -p com.google.android.googlequicksearchbox 9999999'
           context = '--throttle 3000 --pct-appswitch 100 -s 1 -p com.android.bluetooth -p com.samsung.android.contacts -p com.google.android.googlequicksearchbox -p com.skt.prod.dialer -p com.samsung.android.messaging -p com.samsung.android.app.dtv.dmb 9999999'
        #os_systemEx("adb -s " + deviceId + " monkey " + context + " &")
        print "adb -s " + deviceId + " shell monkey " + context + " &"
        #proc = subprocess.Popen("adb -s " + deviceId + " shell monkey " + context + " &", stdout=subprocess.PIPE)
        proc = subprocess.Popen("adb -s " + deviceId + " shell monkey " + context, stdout=subprocess.PIPE)
        time.sleep(5)
        try:
            proc.kill()
        except:
            printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))
    else:
        reVal = 'already started!'

    return reVal


def runStartApp(deviceId, packageName, activityName):
    reVal = 0
    pid = getPidInDevice(deviceId, packageName)
    if pid != 0:
        killProcessInDevice(deviceId, pid)
        time.sleep(5)

    proc = subprocess.Popen("adb -s " + deviceId + " shell am start -a android.intent.action.MAIN -n " + packageName + '/' + activityName, stdout=subprocess.PIPE)
    time.sleep(5)
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    pid = getPidInDevice(deviceId, packageName)
    if pid != 0:
        reVal = pid;

    return reVal

def mkdirs(fullpathName):
    dir = os.path.dirname(fullpathName)
    # create directory if it does not exist
    if not os.path.exists(dir):
        os.makedirs(dir)

def chunkstring(string, length):
    #return re.findall('.{%d}' % length, string)
    return (string[0+i:length+i] for i in range(0, len(string), length))

def sendMessage(sendNumber, receiveNumber, text):
    reVal = -1
    count = 0
    while reVal != 200:
        count = count + 1
        #r = requests.get('http://beta.teafone.com/msggw/sendMsg?sender=%s&receiver=%s&message=%s'% (sendNumber, receiveNumber, text))
        try:
            for chunk in chunkstring(text, 80):
                message = 'http://223.39.126.136/msggw/sendMsg?sender=%s&receiver=%s&message=%s' % (sendNumber, receiveNumber, chunk)
                #message = message.replace('%', '@').replace('"', '').replace("'", "").replace(' ', '_')
                r = requests.get(message)
                printEx(message)
                printEx("%s(%s)" % ("r.status_code", r.status_code))
                reVal = r.status_code
        except:
            printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))
            break

        if count > 3:
            break

    return reVal

def printError (*strs):
    tot = ""
    for string in strs:
        if type(string) is str:
            tot += string
        else:
            tot += str(string)
    print tot

def printEx (*strs):
    if DEBUG():
        tot = ""
        for string in strs:
            if type(string) is str:
                tot += string
            else:
                tot += str(string)
        print tot
def os_systemEx (*strs):
    tot = ""
    for string in strs:
        if type(string) is str:
            tot += string
        else:
            tot += str(string)
    if DEBUG():
        os.system(tot)
    else:
        os.system(tot+ ' > nul')

def getExceptionString(info):
    return ''.join(traceback.format_exception(*info)[-2:]).strip().replace('\n', ': ')

if __name__ == "__main__":
    from common.deviceInfo import *
    for DEVICE_ID in getDevices():
        printEx("%s:%s" % ("runMonkeyInDevice", runMonkeyInDevice(DEVICE_ID, None)))

        while True:
            pid = getPidInDevice(DEVICE_ID, 'com.android.commands.monkey')
            printEx("%s:%s" % ("pid", pid))
            if pid > 0:
                printEx("%s:%s" % ("killProcessInDevice", killProcessInDevice(DEVICE_ID, pid)))
            else:
                break
