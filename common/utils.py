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
        proc = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
        printEx( command )
        fd_popen = proc.stdout

        fileList = fd_popen.read().strip()
        for file in fileList.split('\n'):
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
    proc = subprocess.Popen(("adb -s " + deviceId + " shell input tap " + location).split(' '),
                            stdout=subprocess.PIPE)
    fd_popen = proc.stdout
    content = fd_popen.read().strip()
    for line in content.split('\n'):
        printEx( "tap " + location )

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

def getDateInDevice(deviceId):
    reVal = None
    proc = subprocess.Popen(("adb -s " + deviceId + " shell date +%H%M").split(' '), stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\n'):
        reVal = list(line)
    printEx( "%s:%s" % ("date +%H%M", str(reVal)) )

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))
    return reVal

def getPidInDevice(deviceId, processName):
    reVal = 0
    proc = subprocess.Popen(("adb -s " + deviceId + " shell ps").split(' '), stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\n'):
        if processName in line:
            reVal = int(line.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').split(' ')[1])
            break

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

"""
gta2slteskt:/ # dumpsys activity activities | grep mFocusedActivity
  mFocusedActivity: ActivityRecord{9784bc6d0 u0 com.skt.prod.dialer/com.skt.prod.incall.lib.ui.activities.incall.InCallActivity t2188}
gta2slteskt:/ # dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'
  mCurrentFocus=Window{deacd13d0 u0 com.skt.prod.dialer/com.skt.prod.incall.lib.ui.activities.incall.InCallActivity}
  mFocusedApp=AppWindowToken{6522dd token=Token{31446b4 ActivityRecord{9784bc6d0 u0 com.skt.prod.dialer/com.skt.prod.incall.lib.ui.activities.incall.InCallActivity t2188}}}
"""
def getCurrentActivity(deviceId):
    reVal = 'None'

    proc = subprocess.Popen(
        ("adb -s " + deviceId + " shell dumpsys activity activities").split(' '), stdout=subprocess.PIPE)
    content = proc.stdout.read().strip()
    mFocusedActivity = None
    for line in content.split('\n'):
        if 'mFocusedActivity' in line:
            splitLine = line.split(' ')
            if (len(splitLine) - 2) >= 0:
                mFocusedActivity = splitLine[len(splitLine) - 2]
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    proc = subprocess.Popen(
        ("adb -s " + deviceId + " shell dumpsys window windows").split(' '), stdout=subprocess.PIPE)
    content = proc.stdout.read().strip()
    mCurrentFocus = None
    mFocusedApp = None
    for line in content.split('\n'):
        if 'mCurrentFocus' in line:
            mCurrentFocus = line.split(' ')[-1]
        elif 'mFocusedApp' in line:
            splitLine = line.split(' ')
            if (len(splitLine) - 2) >= 0:
                mFocusedApp = splitLine[len(splitLine) - 2]
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    printEx("%s(%s)" % ("mFocusedActivity", mFocusedActivity))
    printEx("%s(%s)" % ("mCurrentFocus", mCurrentFocus))
    printEx("%s(%s)" % ("mFocusedApp", mFocusedApp))

    if mFocusedActivity != None and mFocusedActivity == mFocusedApp: #and mFocusedApp in mCurrentFocus:
        reVal = mFocusedActivity.replace('/', '')
    if reVal != 'None' and mFocusedApp != None:
        reVal = mFocusedApp.replace('/', '')

    return reVal


def isScreenON(deviceId):
    reVal = False
    proc = subprocess.Popen(
        ("adb -s " + deviceId + " shell dumpsys power").split(' '), stdout=subprocess.PIPE)
    content = proc.stdout.read().strip()
    for line in content.split('\n'):
        if 'mScreenOn' in line:
            if 'ON' in line:
                reVal = True
                break
        elif 'Display' in line and 'Power:' in line :
            if 'ON' in line:
                reVal = True
                break
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def screenTurnON(deviceId):
    while isScreenON(deviceId) == False:
        inputKeyEventInDevice(deviceId, 'KEYCODE_POWER')

def screenTurnOFF(deviceId):
    while isScreenON(deviceId) == True:
        inputKeyEventInDevice(deviceId, 'KEYCODE_POWER')

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
            proc = subprocess.Popen(("adb -s " + deviceId + " shell am start -a android.intent.action.MAIN -n " + componentName).split(' '), stdout=subprocess.PIPE)
            printEx("%s(%s)" % ("count In inner_Process()", count))
            content = proc.stdout.read().strip()
            for line in content.split('\n'):
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

def installAPK(deviceId, fullpathName, packageName):
    if packageName != None:
        command = "adb -s " + deviceId + " shell pm clear " + packageName
        printEx("%s(%s)" % (command, 'begin'))
        os_systemEx(command)
        printEx("%s(%s)" % (command, '__end'))
    command = "adb -s " + deviceId + " install -r -d " + fullpathName
    printEx("%s(%s)" % (command, 'begin'))
    os_systemEx(command)
    printEx("%s(%s)" % (command, '__end'))

def inputKeyEventInDevice(deviceId, key_event):
    proc = subprocess.Popen(("adb -s " + deviceId + " shell input keyevent " + key_event).split(' '), stdout=subprocess.PIPE)
    time.sleep(5)
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

def inputKeyEventInDevice(deviceId, key_event):
    proc = subprocess.Popen(("adb -s " + deviceId + " shell input keyevent " + key_event).split(' '), stdout=subprocess.PIPE)
    time.sleep(5)
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

def killProcessInDevice(deviceId, pid):
    reVal = ''
    proc = subprocess.Popen(("adb -s " + deviceId + " shell kill -9 " + str(pid)).split(' '), stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\n'):
            reVal = reVal + line

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def execCmdBackground(command):
    try:
        proc = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
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
        #proc = subprocess.Popen(("adb -s " + deviceId + " shell monkey " + context + " &").split(' '), stdout=subprocess.PIPE)
        proc = subprocess.Popen(("adb -s " + deviceId + " shell monkey " + context).split(' '), stdout=subprocess.PIPE)
        time.sleep(5)
        try:
            proc.kill()
        except:
            printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))
    else:
        reVal = 'already started!'

    return reVal


def runRestartApp(deviceId, packageName, activityName):
    reVal = 0
    pid = getPidInDevice(deviceId, packageName)
    if pid != 0:
        killProcessInDevice(deviceId, pid)
        time.sleep(5)

    proc = subprocess.Popen(("adb -s " + deviceId + " shell am start -a android.intent.action.MAIN -n " + packageName + '/' + activityName).split(' '), stdout=subprocess.PIPE)
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
