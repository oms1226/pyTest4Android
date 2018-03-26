# -*- coding: utf-8 -*-
#!/usr/bin/python

import datetime
import random
import socket
import threading

from CallRecordingTest.pyCallRecordingTestThread import pyCallRecordingTestThread
from common.deviceCompat import getLocationOnDialPad, getLocationOnMainDialPad, getKey4LocationOnDialPad, \
    getLocationXYOnMainDialPad
from common.deviceInfo import *
from common.utils import *


setDEBUG(True)
TARGET_PACKAGENAME = 'com.skt.prod.dialer'
LAUNCH_ACTIVITYNAME= 'com.skt.prod.dialer.activities.main.MainActivity'
INCALL_ACTIVITYNAME= 'com.skt.prod.incall.lib.ui.activities.incall.InCallActivity'
JSON_LOCAL_FILE = None
INFO_FILEFULLNAME = "data\\modelInfo4getprop.data"
HASHKEY_FILEFULLNAME = "data\\modelInfo4getprop.hashkey"
FIELDS_FILEFULLNAME = "data\\modelInfo4getprop.fields"
SMALL_DELAY = 3
BASIC_DELAY = 5
MIN_SLEEPTIME = 60
MAX_SLEEPTIME = 15 * 60
EXISTED_FIELD_DEPEND = True
MAX_RETRYCOUNT = 10


def tapPhoneNumbOnDevice(mySelf, tapList):
    for num in tapList:
        time.sleep(SMALL_DELAY)
        printEx("%s:%s" % ("num", str(num)))
        if int(mySelf.DENSITY) > 280:
            tapOnDevice(mySelf.DEVICE_ID, getLocationOnMainDialPad(str(num),mySelf.DIALPAD_KEY))
        else:
            tapOnDevice(mySelf.DEVICE_ID, getLocationOnDialPad(str(num),mySelf.DIALPAD_KEY))

def tapDialOnDevice(mySelf):
    x = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 0)
    if int(mySelf.DENSITY) > 280:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 500
    else:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 150
    x_y = "%s %s" % (str(x), str(y))
    time.sleep(SMALL_DELAY)
    tapOnDevice(mySelf.DEVICE_ID, x_y)

def tapReDialOnDevice(mySelf):
    x = getLocationXYOnMainDialPad('0', mySelf.DIALPAD_KEY, 0)
    if int(mySelf.DENSITY) > 280:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 500
    else:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 150
    x_y = "%s %s" % (str(x), str(y))
    time.sleep(SMALL_DELAY)
    tapOnDevice(mySelf.DEVICE_ID, x_y)

def tapEndCallOnDevice(mySelf):
    x = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 0) + 100
    y = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 1) + 500
    x_y = "%s %s" % (str(x), str(y))
    time.sleep(SMALL_DELAY)
    tapOnDevice(mySelf.DEVICE_ID, x_y)


def processCallSetup(connected_Devices, selfs):
    setupCount = 0
    reVal = True
    for DEVICE_ID in connected_Devices:
        runStartApp(DEVICE_ID, TARGET_PACKAGENAME, LAUNCH_ACTIVITYNAME)
        time.sleep(BASIC_DELAY)
        tapPhoneNumbOnDevice(selfs[DEVICE_ID], selfs[DEVICE_ID].PARTNERNUM)
        time.sleep(BASIC_DELAY)
        tapDialOnDevice(selfs[DEVICE_ID])
        time.sleep(BASIC_DELAY * 2)
        while(True):
            CurrentActivityName = getCurrentActivity(selfs[DEVICE_ID].PARTNERID)
            printEx("%s:%s" % ("getCurrentActivity", CurrentActivityName))
            if INCALL_ACTIVITYNAME in CurrentActivityName:
                break
            else:
                time.sleep(BASIC_DELAY)
            setupCount = setupCount + 1
            if setupCount > MAX_RETRYCOUNT:
                reVal = False
                break
        if reVal == False:
            break

        while(True):
            tapEndCallOnDevice(selfs[DEVICE_ID])
            time.sleep(BASIC_DELAY*2)
            CurrentActivityName = getCurrentActivity(selfs[DEVICE_ID].PARTNERID)
            printEx("%s:%s" % ("getCurrentActivity", CurrentActivityName))
            if LAUNCH_ACTIVITYNAME in CurrentActivityName:
                break
            else:
                time.sleep(BASIC_DELAY)
            setupCount = setupCount + 1
            if setupCount > MAX_RETRYCOUNT:
                reVal = False
                break
        if reVal == False:
            break
    return reVal


def setLogCat(SELF):
    args = {}
    START_TIME = strftime("%Y%m%d%H%M%S", localtime())
    tagName = 'NONE'
    searchName = 'NONE'
    args["logfullfilename"] = ".\\" + "Logcat" + "_" + tagName + '_' + searchName + '_' + SELF.PACKAGENAME + "_" + SELF.hostname + "_" + SELF.MODEL + "_" + SELF.OSVERSION + "_" + START_TIME + ".log"
    args["DEVICE_ID"] = SELF.DEVICE_ID
    args["MYNUM"] = SELF.MYNUM
    args["MODEL"] = SELF.MODEL
    args["tag"] = "TPhone "
    return getProc4LogCat(**args)

"""
아래를 pythonpath를 추가
  C:\_python\workspace\PycharmProjects\pyTest4AndroidonGithub
python C:\_python\workspace\PycharmProjects\pyTest4AndroidonGithub\mediaProfiling\getPropAgent.py -a
"""
class SELF:
    def __init__(self, deviceID, selfVersion):
        self.pids = []
        self.resultS = dict()
        self.selfVersion = selfVersion
        self.APPVERSION = "None"
        self.DEVICE_ID = deviceID
        self.MYNUM = getPhoneNumberFromDevice(deviceID)
        self.WIDTH = getWindowWidthFromDumpsys(deviceID)
        self.HEIGHT = getWindowHeightFromDumpsys(deviceID)
        self.DENSITY = getWindowDensityFromDumpsys(deviceID)
        self.MANUFACTURER = getManufacturerFromDevice(deviceID)
        self.MODEL = getModelNameFromDevice(deviceID)
        self.OSVERSION = getOSVersionFromDevice(deviceID)
        self.MANUFACTURERVERSION = getManufactureVersionFromDevice(deviceID)
        self.DIALPAD_KEY = getKey4LocationOnDialPad(self.selfVersion, self.APPVERSION, self.MANUFACTURER, self.MODEL, self.WIDTH, self.HEIGHT, self.DENSITY)
        self.PACKAGENAME = 'com.skt.prod.dialer'
        self.hostname = socket.gethostname()
    def setPartner(self, deviceID, num):
        self.PARTNERID = deviceID
        self.PARTNERNUM = num
    def setLogCat(self, LOGPROCESS, LOGINFO):
        self.LOGPROCESS = LOGPROCESS
        self.LOGINFO = LOGINFO

if __name__ == "__main__":
    AUTOMODE = True
    INSTALLAPKNAME = 'None'
    during_mins = 1
    SETUP_SUCESS = True
    while len(sys.argv) > 1:
        if len(sys.argv) > 1 and '-a' in sys.argv[1]:
            AUTOMODE = True
            sys.argv.pop(1)
        if '-apk' in sys.argv[1]:
            sys.argv.pop(1)
            if len(sys.argv) > 1:
                INSTALLAPKNAME = sys.argv[1]
                sys.argv.pop(1)
    printEx("%s:%s" % ("AUTOMODE", AUTOMODE))
    printEx("%s:%s" % ("INSTALLAPKNAME", INSTALLAPKNAME))
    connected_Devices = getRealDevices()

    # printEx("%s:%s" % ("hashKeys", hashKeys))
    if len(connected_Devices) != 2:
        printError("len(connectingDevices) is " + str(len(connected_Devices)) + '! But, that is not available!')
        exit(0)

    phoneNum = []
    selfs = {}
    for DEVICE_ID in connected_Devices:
        printEx("%s:%s" % ("DEVICE_ID", DEVICE_ID))
        phoneNum.append(getPhoneNumberFromDevice(DEVICE_ID))
        selfs[DEVICE_ID] = SELF(DEVICE_ID, "None")

    for i in connected_Devices:
        for j in connected_Devices:
            if i != j:
                selfs[i].setPartner(selfs[j].DEVICE_ID, selfs[j].MYNUM)

    if AUTOMODE == False:
        for DEVICE_ID in connected_Devices:
            printEx("%s:%s" % ("phoneNum", str(selfs[DEVICE_ID].MYNUM)))
            printEx("%s:%s" % ("partnerNum", str(selfs[DEVICE_ID].PARTNERNUM)))
            runStartApp(DEVICE_ID, TARGET_PACKAGENAME, LAUNCH_ACTIVITYNAME)

        SETUP_SUCESS = processCallSetup(connected_Devices, selfs)
        if SETUP_SUCESS == False:
            printError("%s:%s" % ("SETUP_SUCESS", SETUP_SUCESS))
            exit(0)

        time.sleep(BASIC_DELAY)

    NEED2RESET = (SETUP_SUCESS == False)
    for DEVICE_ID in connected_Devices:
        LOGPROCESS, LOGINFO = setLogCat(selfs[DEVICE_ID])
        selfs[DEVICE_ID].setLogCat(LOGPROCESS, LOGINFO)

    START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    endDatetime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9, minutes=during_mins))
    EXPECT_END_TIME = endDatetime.strftime("%Y%m%d%H%M")
    while long(EXPECT_END_TIME) > long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")):
        connectingDevices = getRealDevices()

        #printEx("%s:%s" % ("hashKeys", hashKeys))
        if len(connectingDevices) != 2:
            printError("len(connectingDevices) is " + str(len(connectingDevices)) + '! But, that is not available!')
            break

        if set(connected_Devices) != set(connectingDevices):
            printEx("%s:%s" % ("connected_Devices", connected_Devices))
            break
        else:
            retryCount4NEED2RESET = 0
            while NEED2RESET:
                NEED2RESET = (processCallSetup(connected_Devices, selfs) == False)
                retryCount4NEED2RESET = retryCount4NEED2RESET + 1
                printError("%s:%s" % ("retryCount4NEED2RESET", retryCount4NEED2RESET))
            faultCount = 0
            connected_Devices = connectingDevices
            SELECTED_DEVICEID = connected_Devices[random.randrange(0, len(connected_Devices))]

            try:
                tapReDialOnDevice(selfs[SELECTED_DEVICEID])
                time.sleep(BASIC_DELAY)
                tapDialOnDevice(selfs[SELECTED_DEVICEID])
                time.sleep(BASIC_DELAY * 2)
                while (True):
                    CurrentActivityName = getCurrentActivity(selfs[SELECTED_DEVICEID].PARTNERID)
                    printEx("%s:%s" % ("getCurrentActivity", CurrentActivityName))
                    if INCALL_ACTIVITYNAME in CurrentActivityName:
                        break
                    else:
                        time.sleep(BASIC_DELAY)
                    faultCount = faultCount + 1
                    if faultCount > MAX_RETRYCOUNT:
                        NEED2RESET = True
                        break

                while (True):
                    tapEndCallOnDevice(selfs[SELECTED_DEVICEID])
                    time.sleep(BASIC_DELAY * 2)
                    CurrentActivityName = getCurrentActivity(selfs[SELECTED_DEVICEID].PARTNERID)
                    printEx("%s:%s" % ("getCurrentActivity", CurrentActivityName))
                    if LAUNCH_ACTIVITYNAME in CurrentActivityName:
                        break
                    else:
                        time.sleep(BASIC_DELAY)
                    faultCount = faultCount + 1
                    if faultCount > MAX_RETRYCOUNT:
                        NEED2RESET = True
                        break
            except:
                printError("Main Logic Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1])
            finally:
                excuteTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
                print("%s-%s." % ("awake", excuteTime)),
        if AUTOMODE == False:
            break

    for DEVICE_ID in connected_Devices:
        if selfs[DEVICE_ID].LOGPROCESS != None:
            try:
                selfs[DEVICE_ID].LOGPROCESS.kill()
            except:
                printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

            printEx("%s:%s" % ("LOGINFO", selfs[DEVICE_ID].LOGINFO.getAllInfo()))