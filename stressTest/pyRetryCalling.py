# -*- coding: utf-8 -*-
#!/usr/bin/python

import datetime
import threading

from CallRecordingTest.pyCallRecordingTestThread import pyCallRecordingTestThread
from common.deviceCompat import getLocationOnDialPad, getLocationOnMainDialPad, getKey4LocationOnDialPad, \
    getLocationXYOnMainDialPad
from common.deviceInfo import *
from common.utils import *


setDEBUG(True)
TARGET_PACKAGENAME = 'com.skt.prod.dialer'
LAUNCH_ACTIVITYNAME= 'com.skt.prod.dialer.activities.main.MainActivity'
JSON_LOCAL_FILE = None
INFO_FILEFULLNAME = "data\\modelInfo4getprop.data"
HASHKEY_FILEFULLNAME = "data\\modelInfo4getprop.hashkey"
FIELDS_FILEFULLNAME = "data\\modelInfo4getprop.fields"
SMALL_DELAY = 3
BASIC_DELAY = 5
MIN_SLEEPTIME = 60
MAX_SLEEPTIME = 15 * 60
EXISTED_FIELD_DEPEND = True


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
    y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 250
    x_y = "%s %s" % (str(x), str(y))
    time.sleep(SMALL_DELAY)
    tapOnDevice(mySelf.DEVICE_ID, x_y)

def tapEndCallOnDevice(mySelf):
    x = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 0) + 100
    y = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 1) + 150
    x_y = "%s %s" % (str(x), str(y))
    time.sleep(SMALL_DELAY)
    tapOnDevice(mySelf.DEVICE_ID, x_y)

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
    def setPartnerNum(self, num):
        self.PARTNERNUM = num

if __name__ == "__main__":
    AUTOMODE = False
    while len(sys.argv) > 1:
        if len(sys.argv) > 1 and '-a' in sys.argv[1]:
            AUTOMODE = True
            sys.argv.pop(1)

    printEx("%s:%s" % ("AUTOMODE", AUTOMODE))
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
        runStartApp(DEVICE_ID, TARGET_PACKAGENAME, LAUNCH_ACTIVITYNAME)

    for i in connected_Devices:
        for j in connected_Devices:
            if i != j:
                selfs[i].setPartnerNum(selfs[j].MYNUM)


    for DEVICE_ID in connected_Devices:
        printEx("%s:%s" % ("phoneNum", str(selfs[DEVICE_ID].MYNUM)))
        printEx("%s:%s" % ("partnerNum", str(selfs[DEVICE_ID].PARTNERNUM)))

    time.sleep(BASIC_DELAY)
    while True:
        connectingDevices = getRealDevices()

        #printEx("%s:%s" % ("hashKeys", hashKeys))
        if len(connectingDevices) != 2:
            printError("len(connectingDevices) is " + str(len(connectingDevices)) + '! But, that is not available!')
            exit(0)

        if set(connected_Devices) != set(connectingDevices):
            printEx("%s:%s" % ("connected_Devices", connected_Devices))
        else:
            connected_Devices = connectingDevices
            sleepTime = MIN_SLEEPTIME


            for DEVICE_ID in connected_Devices:
                try:
                    tapPhoneNumbOnDevice(selfs[DEVICE_ID], selfs[DEVICE_ID].PARTNERNUM)
                    time.sleep(BASIC_DELAY)
                    tapDialOnDevice(selfs[DEVICE_ID])
                    time.sleep(BASIC_DELAY)
                    tapEndCallOnDevice(selfs[DEVICE_ID])
                    time.sleep(BASIC_DELAY)
                except:
                    printError("Main Logic Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1])
                finally:
                    excuteTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
                    print("%s-%s." % ("awake", excuteTime)),
        if AUTOMODE == False:
            break
