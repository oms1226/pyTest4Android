# -*- coding: utf-8 -*-
#!/usr/bin/python

import datetime
import random
import socket

from common.deviceCompat import *
from common.deviceInfo import *
from common.utils import *
from sys import platform as _platform



setDEBUG(True)
TARGET_PACKAGENAME = 'com.skt.prod.dialer'
LAUNCH_ACTIVITYNAME= 'com.skt.prod.dialer.activities.main.MainActivity'
INCALL_ACTIVITYNAME= 'com.skt.prod.incall.lib.ui.activities.incall.InCallActivity'
JSON_LOCAL_FILE = None
INFO_FILEFULLNAME = "testResults.data"
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
        if int(mySelf.DENSITY) > 320:
            tapOnDevice(mySelf.DEVICE_ID, getLocationOnMainDialPad(str(num),mySelf.DIALPAD_KEY, int(mySelf.DENSITY)))
        elif int(mySelf.DENSITY) > 280:
            tapOnDevice(mySelf.DEVICE_ID, getLocationOnMainDialPad(str(num),mySelf.DIALPAD_KEY, int(mySelf.DENSITY)))
        else:
            tapOnDevice(mySelf.DEVICE_ID, getLocationOnDialPad(str(num),mySelf.DIALPAD_KEY))

def tapDialOnDevice(mySelf):
    x = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 0)
    if int(mySelf.DENSITY) > 320:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 500
    elif int(mySelf.DENSITY) > 280:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 350
    else:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 150
    x_y = "%s %s" % (str(x), str(y))
    time.sleep(SMALL_DELAY)
    tapOnDevice(mySelf.DEVICE_ID, x_y)

def tapReDialOnDevice(mySelf):
    x = getLocationXYOnMainDialPad('0', mySelf.DIALPAD_KEY, 0)
    if int(mySelf.DENSITY) > 320:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 500
    elif int(mySelf.DENSITY) > 280:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 350
    else:
        y = getLocationXYOnMainDialPad('*', mySelf.DIALPAD_KEY, 1) + 150
    x_y = "%s %s" % (str(x), str(y))
    time.sleep(SMALL_DELAY)
    tapOnDevice(mySelf.DEVICE_ID, x_y)

def tapEndCallOnDevice(mySelf):
    x = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 0) + 100
    if int(mySelf.DENSITY) == 320:
        y = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 1) + 350
    else:
        y = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 1) + 500
    x_y = "%s %s" % (str(x), str(y))
    time.sleep(SMALL_DELAY)
    tapOnDevice(mySelf.DEVICE_ID, x_y)


def processCallSetup(connected_Devices, selfs):
    setupCount = 0
    reVal = True
    for DEVICE_ID in connected_Devices:
        runRestartApp(DEVICE_ID, TARGET_PACKAGENAME, LAUNCH_ACTIVITYNAME)
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
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        args["logfullfilename"] = "./" + "Logcat" + "_" + tagName + '_' + searchName + '_' + SELF.PACKAGENAME + "_" + SELF.hostname + "_" + SELF.MODEL + "_" + SELF.OSVERSION + "_" + START_TIME + ".log"
    elif _platform == "win32":
        args["logfullfilename"] = ".\\" + "Logcat" + "_" + tagName + '_' + searchName + '_' + SELF.PACKAGENAME + "_" + SELF.hostname + "_" + SELF.MODEL + "_" + SELF.OSVERSION + "_" + START_TIME + ".log"
    SELF.LOGFILENAME  = args["logfullfilename"]
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
    def __init__(self, thisFilename, deviceID, selfVersion, apkName, hashcode, revcnt, during_mins):
        self.MYNAME = thisFilename
        self.INSTALLAPKNAME = apkName
        self.trtc_git_hashcode = hashcode
        self.trtc_git_revcnt = revcnt
        self.during_mins = during_mins
        self.KILL_COUNT = 0
        self.TRY_COUNT_ARCALL_OUTGOING = 0
        self.TRY_COUNT_ARCALL_INCOMING = 0
        self.SUCCCOUNT_ARCALL_OUTGOING = 0
        self.SUCCCOUNT_ARCALL_INCOMING = 0
        self.FAILCOUNT_ARCALL_OUTGOING = 0
        self.FAILCOUNT_ARCALL_INCOMING = 0
        self.info = dict()
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
        self.DIENUM = 0
        self.BATTERYLEVEL_START = getBatteryLevel(deviceID)
        self.LOGFILENAME = None
        self.RSRP_SUM = 0
        self.RSRP_COUNT = 0
    def setPartner(self, deviceID, num):
        self.PARTNERID = deviceID
        self.PARTNERNUM = num
    def setLogCat(self, LOGPROCESS, LOGINFO):
        self.LOGPROCESS = LOGPROCESS
        self.LOGINFO = LOGINFO
    def setStartTime(self, sTime):
        self.START______TIME = sTime
    def checkRSRP(self):
        intValue = getRSRPonMobileData(self.DEVICE_ID)
        if intValue != None:
            self.RSRP_SUM += intValue
            self.RSRP_COUNT += 1
    def getAllInfo(self):
        reVal = dict()
        dummy = self.LOGINFO.getAllInfo()
        reVal.update(self.LOGINFO.getInfo(None))
        self.BATTERYLEVEL___END = getBatteryLevel(self.DEVICE_ID)
        self.info['MODEL'] = self.MODEL
        self.info['OSVERSION'] = self.OSVERSION
        self.info['MANUFACTURER'] = self.MANUFACTURER

        self.info['MYNAME'] = self.MYNAME

        self.info['TRY_COUNT_ARCALL_OUTGOING'] = self.TRY_COUNT_ARCALL_OUTGOING
        self.info['TRY_COUNT_ARCALL_INCOMING'] = self.TRY_COUNT_ARCALL_INCOMING
        self.info['SUCCCOUNT_ARCALL_OUTGOING'] = self.SUCCCOUNT_ARCALL_OUTGOING
        self.info['SUCCCOUNT_ARCALL_INCOMING'] = self.SUCCCOUNT_ARCALL_INCOMING
        self.info['FAILCOUNT_ARCALL_OUTGOING'] = self.FAILCOUNT_ARCALL_OUTGOING
        self.info['FAILCOUNT_ARCALL_INCOMING'] = self.FAILCOUNT_ARCALL_INCOMING

        self.info['START______TIME'] = self.START______TIME
        self.info['trtc_git_hashcode'] = self.trtc_git_hashcode
        self.info['trtc_git_revcnt'] = self.trtc_git_revcnt
        self.info['during_mins'] = self.during_mins
        self.info['INSTALLAPKNAME'] = self.INSTALLAPKNAME
        self.info['during_mins'] = self.during_mins
        self.info['BATTERYLEVEL_START'] = self.BATTERYLEVEL_START
        self.info['BATTERYLEVEL___END'] = self.BATTERYLEVEL___END
        self.info['RSRP_AVERAGE'] = self.RSRP_SUM/self.RSRP_COUNT
        self.info['LOGFILENAME'] = self.LOGFILENAME

        self.DIENUM = self.LOGINFO.getInfo('PIDS#') - self.KILL_COUNT -1
        self.info['DIE#'] = self.DIENUM
        reVal.update(self.info)
        return json.dumps(reVal).replace('\\', '')
    def printWellformedInfo(self):
        print("=============================================>")
        print("%s:%s /" % ("MODEL", self.MODEL)),
        print("%s:%s /" % ("OSVERSION", self.OSVERSION)),
        print("%s:%s /" % ("MANUFACTURER", self.MANUFACTURER)),
        print("%s:%d /" % ("during_mins", self.during_mins)),
        print("%s:%s" % ("START______TIME", self.START______TIME))
        print("----------------------------------------------")
        print("%s:%d /" % ("TRY_COUNT_ARCALL_OUTGOING", self.TRY_COUNT_ARCALL_OUTGOING)),
        print("%s:%d /" % ("SUCCCOUNT_ARCALL_OUTGOING", self.SUCCCOUNT_ARCALL_OUTGOING)),
        print("%s:%d" % ("FAILCOUNT_ARCALL_OUTGOING", self.FAILCOUNT_ARCALL_OUTGOING))
        print("%s:%d /" % ("TRY_COUNT_ARCALL_INCOMING", self.TRY_COUNT_ARCALL_INCOMING)),
        print("%s:%d /" % ("SUCCCOUNT_ARCALL_INCOMING", self.SUCCCOUNT_ARCALL_INCOMING)),
        print("%s:%d" % ("FAILCOUNT_ARCALL_INCOMING", self.FAILCOUNT_ARCALL_INCOMING))
        print("%s:%d / " % ("PID#", self.LOGINFO.getInfo('PIDS#'))),
        print("%s:%d" % ("TID#", self.LOGINFO.getInfo('TIDS#')))
        print("%s:%d / " % ("DIE#", self.DIENUM)),
        print("%s:%d" % ("KILL#", self.KILL_COUNT))
        print("%s:%d / " % ("BATTERYLEVEL_START", self.BATTERYLEVEL_START)),
        print("%s:%d / " % ("BATTERYLEVEL___END", self.BATTERYLEVEL___END)),
        print("%s:%f" % ("RSRP_AVERAGE", self.RSRP_SUM/self.RSRP_COUNT))
        print("<=============================================")

"""
<preCondition>
1> 단말 두대만 연결
2> 각 단말의 콜라 히든 메뉴에서 auto mute on, auto answer on
"""
if __name__ == "__main__":
    AUTOMODE = True
    INSTALLAPKNAME = 'None'
    git_hashcode = 'None'
    git_revcnt = -1
    during_mins = 10
    SETUP_SUCESS = True
    NEED_SETUP = True
    while len(sys.argv) > 1:
        printEx("%s:%s" % ("sys.argv", sys.argv))
        if len(sys.argv) > 1 and '-apk' in sys.argv[1]:
            sys.argv.pop(1)
            if len(sys.argv) > 1:
                INSTALLAPKNAME = sys.argv[1]
                sys.argv.pop(1)
        if len(sys.argv) > 1 and '-m' in sys.argv[1]:
            sys.argv.pop(1)
            if len(sys.argv) > 1:
                during_mins = int(sys.argv[1])
                sys.argv.pop(1)
        if len(sys.argv) > 1 and '-hash' in sys.argv[1]:
            sys.argv.pop(1)
            if len(sys.argv) > 1:
                git_hashcode = sys.argv[1]
                sys.argv.pop(1)
        if len(sys.argv) > 1 and '-revcnt' in sys.argv[1]:
            sys.argv.pop(1)
            if len(sys.argv) > 1:
                git_revcnt = sys.argv[1]
                sys.argv.pop(1)
        if len(sys.argv) > 1 and '-nosetup' in sys.argv[1]:
            sys.argv.pop(1)
            NEED_SETUP = False

    printEx("%s:%s" % ("NEED_SETUP", NEED_SETUP))
    printEx("%s:%s" % ("git_hashcode", git_hashcode))
    printEx("%s:%s" % ("git_revcnt", git_revcnt))
    printEx("%s:%s" % ("during_mins", during_mins))
    printEx("%s:%s" % ("INSTALLAPKNAME", INSTALLAPKNAME))
    connected_Devices = getRealDevices()

    # printEx("%s:%s" % ("hashKeys", hashKeys))
    if len(connected_Devices) != 2:
        printError("len(connectingDevices) is " + str(len(connected_Devices)) + '! But, that is not available!')
        exit(0)

    phoneNum = []
    selfs = {}
    myName = sys.argv[0].split('/')[-1]
    print "%s:%s" % ("myName", myName)
    for DEVICE_ID in connected_Devices:
        printEx("%s:%s" % ("DEVICE_ID", DEVICE_ID))
        phoneNum.append(getPhoneNumberFromDevice(DEVICE_ID))
        selfs[DEVICE_ID] = SELF(myName, DEVICE_ID, "None", INSTALLAPKNAME, git_hashcode, git_revcnt, during_mins)
        screenTurnON(DEVICE_ID)
        if INSTALLAPKNAME != 'None':
            installAPK(DEVICE_ID, INSTALLAPKNAME, None)

    for i in connected_Devices:
        for j in connected_Devices:
            if i != j:
                selfs[i].setPartner(selfs[j].DEVICE_ID, selfs[j].MYNUM)

    if NEED_SETUP == True:
        for DEVICE_ID in connected_Devices:
            printEx("%s:%s" % ("phoneNum", str(selfs[DEVICE_ID].MYNUM)))
            printEx("%s:%s" % ("partnerNum", str(selfs[DEVICE_ID].PARTNERNUM)))
            runRestartApp(DEVICE_ID, TARGET_PACKAGENAME, LAUNCH_ACTIVITYNAME)

        SETUP_SUCESS = processCallSetup(connected_Devices, selfs)
        if SETUP_SUCESS == False:
            printError("%s:%s" % ("SETUP_SUCESS", SETUP_SUCESS))
            exit(0)

        time.sleep(BASIC_DELAY)

    NEED2RESET = (SETUP_SUCESS == False)

    START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    for DEVICE_ID in connected_Devices:
        LOGPROCESS, LOGINFO = setLogCat(selfs[DEVICE_ID])
        selfs[DEVICE_ID].setLogCat(LOGPROCESS, LOGINFO)
        selfs[DEVICE_ID].setStartTime(START______TIME)

    endDatetime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9, minutes=during_mins))
    EXPECT_END_TIME = endDatetime.strftime("%Y%m%d%H%M")
    retryCount4NEED2RESET = 0
    faultCount = 0
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
            for DEVICE_ID in connected_Devices:
                selfs[DEVICE_ID].checkRSRP()

            if False:
                while NEED2RESET:
                    NEED2RESET = (processCallSetup(connected_Devices, selfs) == False)
                    retryCount4NEED2RESET = retryCount4NEED2RESET + 1
                    printError("%s:%s" % ("retryCount4NEED2RESET", retryCount4NEED2RESET))
                    for DEVICE_ID in connected_Devices:
                        selfs[DEVICE_ID].KILL_COUNT += 1
                    faultCount = 0
            connected_Devices = connectingDevices
            SELECTED_DEVICEID = connected_Devices[random.randrange(0, len(connected_Devices))]

            try:
                CurrentActivityName = getCurrentActivity(selfs[SELECTED_DEVICEID].DEVICE_ID)
                while LAUNCH_ACTIVITYNAME not in CurrentActivityName:
                    inputKeyEventInDevice(selfs[SELECTED_DEVICEID].DEVICE_ID, 'KEYCODE_BACK')
                    inputKeyEventInDevice(selfs[SELECTED_DEVICEID].DEVICE_ID, 'KEYCODE_HOME')
                    startActivity(selfs[SELECTED_DEVICEID].DEVICE_ID, ("%s/%s" % (TARGET_PACKAGENAME, LAUNCH_ACTIVITYNAME)), 1)
                    time.sleep(BASIC_DELAY)
                    CurrentActivityName = getCurrentActivity(selfs[SELECTED_DEVICEID].DEVICE_ID)
                    faultCount = faultCount + 1
                    if faultCount > MAX_RETRYCOUNT:
                        selfs[SELECTED_DEVICEID].FAILCOUNT_ARCALL_OUTGOING  += 1
                        NEED2RESET = True
                        break


                tapReDialOnDevice(selfs[SELECTED_DEVICEID])
                time.sleep(BASIC_DELAY)
                tapDialOnDevice(selfs[SELECTED_DEVICEID])
                time.sleep(BASIC_DELAY * 2)
                selfs[SELECTED_DEVICEID].TRY_COUNT_ARCALL_OUTGOING += 1
                while (True):
                    CurrentActivityName = getCurrentActivity(selfs[SELECTED_DEVICEID].DEVICE_ID)
                    printEx("%s:%s" % ("getCurrentActivity", CurrentActivityName))
                    if INCALL_ACTIVITYNAME in CurrentActivityName:
                        selfs[SELECTED_DEVICEID].SUCCCOUNT_ARCALL_OUTGOING  += 1
                        break
                    else:
                        time.sleep(BASIC_DELAY)
                    faultCount = faultCount + 1
                    if faultCount > MAX_RETRYCOUNT:
                        selfs[SELECTED_DEVICEID].FAILCOUNT_ARCALL_OUTGOING  += 1
                        NEED2RESET = True
                        break

                selfs[selfs[SELECTED_DEVICEID].PARTNERID].TRY_COUNT_ARCALL_INCOMING += 1
                while (True):
                    CurrentActivityName = getCurrentActivity(selfs[SELECTED_DEVICEID].PARTNERID)
                    printEx("%s:%s" % ("getCurrentActivity", CurrentActivityName))
                    if INCALL_ACTIVITYNAME in CurrentActivityName:
                        selfs[selfs[SELECTED_DEVICEID].PARTNERID].SUCCCOUNT_ARCALL_INCOMING += 1
                        break
                    else:
                        time.sleep(BASIC_DELAY)
                    faultCount = faultCount + 1
                    if faultCount > MAX_RETRYCOUNT:
                        selfs[selfs[SELECTED_DEVICEID].PARTNERID].FAILCOUNT_ARCALL_INCOMING += 1
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
                faultCount = faultCount + 1
                if faultCount > MAX_RETRYCOUNT:
                    NEED2RESET = True
            finally:
                excuteTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
                print("%s-%s." % ("running", excuteTime))


    for DEVICE_ID in connected_Devices:
        if selfs[DEVICE_ID].LOGPROCESS != None:
            try:
                selfs[DEVICE_ID].LOGPROCESS.kill()
            except:
                printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

            printEx("%s:%s" % ("LOGINFO", selfs[DEVICE_ID].getAllInfo()))
        selfs[DEVICE_ID].printWellformedInfo()
        with codecs.open(INFO_FILEFULLNAME, 'a', 'utf-8') as f:
            f.write(selfs[DEVICE_ID].getAllInfo() + "\r\n")
            f.close()
        screenTurnOFF(DEVICE_ID)