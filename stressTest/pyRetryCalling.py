# -*- coding: utf-8 -*-
#!/usr/bin/python

import datetime
import random
import socket

from common.deviceCompat import *
from common.deviceInfo import *
from common.utils import *
from sys import platform as _platform
reload(sys)
sys.setdefaultencoding('utf-8')

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
THRESHOLD_BATTERY_MIN_LEVEL = 5
THRESHOLD_FAULT_MAX_COUNT = 300
selfVersion = '1.0.0'

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

def processCallSetup(connected_Devices, selfs):
    setupCount = 0
    reVal = True
    for DEVICE_ID in connected_Devices:
        runRestartApp(DEVICE_ID, TARGET_PACKAGENAME, LAUNCH_ACTIVITYNAME)
        time.sleep(BASIC_DELAY)
        tapPhoneNumbOnDevice(selfs[DEVICE_ID], selfs[DEVICE_ID].PARTNERNUM)
        time.sleep(BASIC_DELAY)
        tapDialOnDevice(selfs[DEVICE_ID], None)
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
            tapEndCallOnDevice(selfs[DEVICE_ID], None)
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

def setError(SELF, connectingIDs, errorStr):
    for id in connectingIDs:
        if SELF.has_key(id):
            SELF[id].ERROR = errorStr

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
        self.ERROR = 'None'
        self.TRACKINGDATA = []
    def setPartner(self, deviceID, num):
        self.PARTNERID = deviceID
        self.PARTNERNUM = num
    def setLogCat(self, LOGPROCESS, LOGINFO):
        self.LOGPROCESS = LOGPROCESS
        self.LOGINFO = LOGINFO
    def setTime(self, sTime, eTime):
        self.START______TIME = sTime
        self.EXPECT_END_TIME = eTime
    def checkRSRP(self):
        slice = dict()
        rsrpValue = getRSRPonMobileData(self.DEVICE_ID)
        if rsrpValue != None:
            self.RSRP_SUM += rsrpValue
            self.RSRP_COUNT += 1
        slice["unixtime"] = time.time()
        slice["rsrp"] = rsrpValue
        slice["geoip.coordinates"] = getGEOIP(self.DEVICE_ID)
        printEx("%s:%s" % ("slice", slice))
        self.TRACKINGDATA.append(slice)

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
        if self.RSRP_COUNT > 0:
            self.info['RSRP_AVERAGE'] = self.RSRP_SUM/self.RSRP_COUNT
        else:
            self.info['RSRP_AVERAGE'] = -1

        self.info['RSRP'] = representRSRPValue(self.info['RSRP_AVERAGE'])
        self.info['LOGFILENAME'] = self.LOGFILENAME
        self.info['ERROR'] = self.ERROR

        self.DIENUM = self.LOGINFO.getInfo('PIDS#') - self.KILL_COUNT -1
        self.info['DIE#'] = self.DIENUM
        self.info['selfVersion'] = selfVersion
        reVal.update(self.info)
        return json.dumps(reVal).replace('\\', '')
    def printWellformedInfo(self):
        print("===============TEST Results==============>")
        print("%s:%s /" % ("selfVersion", selfVersion)),
        print("%s:%s /" % ("MODEL", self.MODEL)),
        print("%s:%s /" % ("OSVERSION", self.OSVERSION)),
        print("%s:%s /" % ("MANUFACTURER", self.MANUFACTURER)),
        print("%s:%d /" % ("during_mins", self.during_mins)),
        print("%s:%s / " % ("START______TIME", self.START______TIME))
        print("%s:%s" % ("EXPECT_END_TIME", self.EXPECT_END_TIME))
        print("----------------------------------------------")
        print("%s:%d /" % ("TRY_COUNT_ARCALL_OUTGOING", self.TRY_COUNT_ARCALL_OUTGOING)),
        print("%s:%d /" % ("SUCCCOUNT_ARCALL_OUTGOING", self.SUCCCOUNT_ARCALL_OUTGOING)),
        print("%s:%d" % ("FAILCOUNT_ARCALL_OUTGOING", self.FAILCOUNT_ARCALL_OUTGOING))
        print("%s:%d /" % ("TRY_COUNT_ARCALL_INCOMING", self.TRY_COUNT_ARCALL_INCOMING)),
        print("%s:%d /" % ("SUCCCOUNT_ARCALL_INCOMING", self.SUCCCOUNT_ARCALL_INCOMING)),
        print("%s:%d" % ("FAILCOUNT_ARCALL_INCOMING", self.FAILCOUNT_ARCALL_INCOMING))
        print("%s:%s /" % ("PIDS", self.LOGINFO.getInfo('PIDS'))),
        print("%s:%d / " % ("PID#", self.LOGINFO.getInfo('PIDS#'))),
        print("%s:%d" % ("TID#", self.LOGINFO.getInfo('TIDS#')))

        print("%s:%d / " % ("DIE#", self.DIENUM)),
        print("%s:%d" % ("KILL#", self.KILL_COUNT))
        print("%s:%d / " % ("BATTERYLEVEL_START", self.BATTERYLEVEL_START)),
        print("%s:%d / " % ("BATTERYLEVEL___END", self.BATTERYLEVEL___END)),
        if self.RSRP_COUNT > 0:
            print("%s:%f / " % ("RSRP_AVERAGE", self.RSRP_SUM / self.RSRP_COUNT)),
            print("%s:%s" % ("RSRP", representRSRPValue(self.RSRP_SUM / self.RSRP_COUNT)))
        else:
            print("%s:%f / " % ("RSRP_AVERAGE", -1)),
            print("%s:%s" % ("RSRP", representRSRPValue(-1)))
        print("%s:%s" % ("Location",  getGEOIP(self.DEVICE_ID)))
        print("%s:%s" % ("ERROR", self.ERROR))
        print("<=============================================")

    def printSliceInfo(self):
        print("---------------------------------------------->")
        print("%s:%s /" % ("MODEL", self.MODEL)),
        print("%s:%s /" % ("OSVERSION", self.OSVERSION)),
        print("%s:%s /" % ("MANUFACTURER", self.MANUFACTURER)),
        print("%s:%d /" % ("during_mins", self.during_mins)),
        print("%s:%s / " % ("START______TIME", self.START______TIME))
        print("%s:%s" % ("EXPECT_END_TIME", self.EXPECT_END_TIME))
        print("----------------------------------------------")
        print("%s:%d /" % ("TRY_COUNT_ARCALL_OUTGOING", self.TRY_COUNT_ARCALL_OUTGOING)),
        print("%s:%d /" % ("SUCCCOUNT_ARCALL_OUTGOING", self.SUCCCOUNT_ARCALL_OUTGOING)),
        print("%s:%d" % ("FAILCOUNT_ARCALL_OUTGOING", self.FAILCOUNT_ARCALL_OUTGOING))
        print("%s:%d /" % ("TRY_COUNT_ARCALL_INCOMING", self.TRY_COUNT_ARCALL_INCOMING)),
        print("%s:%d /" % ("SUCCCOUNT_ARCALL_INCOMING", self.SUCCCOUNT_ARCALL_INCOMING)),
        print("%s:%d" % ("FAILCOUNT_ARCALL_INCOMING", self.FAILCOUNT_ARCALL_INCOMING))
        print("%s:%s /" % ("PIDS", self.LOGINFO.getInfo('PIDS'))),
        print("%s:%d" % ("PID#", len(self.LOGINFO.getInfo('PIDS'))))
        print("<----------------------------------------------")

def tapReDialOnDevice(mySelf, external):
    x_y = getExternalXY(mySelf.MODEL, external, "D")
    if x_y == None:
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

def tapDialOnDevice(mySelf, external):
    x_y = getExternalXY(mySelf.MODEL, external, "callarD")
    if x_y == None:
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

def tapEndCallOnDevice(mySelf, external):
    x_y = getExternalXY(mySelf.MODEL, external, "E")
    if x_y == None:
        x = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 0)
        if int(mySelf.DENSITY) == 320:
            x = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 0) + 50
            y = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 1) + 350
        else:
            x = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 0) + 100
            y = getLocationXYOnMainDialPad('#', mySelf.DIALPAD_KEY, 1) + 500
        x_y = "%s %s" % (str(x), str(y))
    time.sleep(SMALL_DELAY)
    tapOnDevice(mySelf.DEVICE_ID, x_y)

def getExternalXY(modelName, dicts, type):
    reVal = None
    if dicts != None:
        for m in dicts.keys():
            if (m in modelName) or (modelName in m):
                reVal = dicts[m].get(type)
                if reVal != None:
                    reVal = reVal.replace('X', ' ')
                    break
    return reVal


def printHelp():
    """
global options:
 -a         listen on all network interfaces, not just localhost
 -d         use USB device (error if multiple devices connected)
 -e         use TCP/IP device (error if multiple TCP/IP devices available)
 -s SERIAL  use device with given serial (overrides $ANDROID_SERIAL)
 -t ID      use device with given transport id
 -H         name of adb server host [default=localhost]
 -P         port of adb server [default=5037]
 -L SOCKET  listen on given socket for adb server [default=tcp:localhost:5037]
general commands:
    """
    print unicode("#precondition:")
    print unicode("  1> adb는 어떤 경로에서든 실행할 수 있어야 된다.")
    print unicode("  2> adb devices로 잡히도록 단말 두대만 연결")
    print unicode("  3> 단말 두대 모두 잠금 화면 없이 동작하도록 설정한다.")
    print unicode("  4> 해당 앱의 모든 권한 설정을 On한다.")
    print unicode("  5> 각 단말의 콜라 히든 메뉴에서 auto mute on, auto answer on")
    print unicode("  6> 서로 상대방 전화를 걸어 redial이 가능하게 설정해놓는다.")
    print unicode("  7> 1~6를 다 수행했다면, command창에서 해당 파일을 실행한다.")
    print unicode("#description:")
    print unicode("  별도 옵션 설정을 하지 않는다면, 90분간 두대의 단말이 서로 간에 무작위로 수신과 발신을 반복한다.")
    print unicode("  테스트가 완료되면, 각 단말의 테스트 결과가 테스트 창에 나오며 해당 파일이 위치한 곳에 각 단말의 로그 파일이 생성된다.")
    print unicode("#global options:")
    print unicode(" -apk FILEFULLPATH       test 전에 설치 대상 apk fullpath를 입력해주면, 해당 apk 설치 후 테스트를 진행하게 된다.")
    print unicode(" -needsetup              상대방 단말을 인식하고, 상대방 번호를 확인하는 과정이 필요하다면, 선언한다.")
    print unicode(" -m MINIUTES             테스트 하고 싶은 시간을 분 단위로 설정한다.(ex. -m 60)")
    print unicode(" -hash HASHCODE          테스트 결과에 git commit hashcode를 명시하고 싶을 때 설정한다.")
    print unicode(" -revcnt REVISIOINNUM    테스트 결과에 git revision count를 명시하고 싶을 때 설정한다.")
    print unicode(" -xy {'MODEL':{'D':'Dial좌표','callarD':'콜라Dial좌표','E':'종료좌표'},'MODEL':{'D':'Dial좌표','callarD':'콜라Dial좌표','E':'종료좌표'}}")
    print unicode("                         시스템이 설정한 좌표 값을 쓰지 않고, 직접 커스텀한 좌표를 쓰고 싶을 때 사용하며,")
    print unicode("                         아래와 같이 모델명(사업자 구분 필요없음)과 dial버튼, 콜라dial버튼, 종료버튼 좌표를 순서 상관없이 넣어주면 되며 복수 입력 가능하다.")
    print unicode("                         단, 아래 예제와 같이 빈칸과 \" 는 사용하면 안된다!")
    print unicode("                         ex. -xy \"{'SM-G930':{'D':'500X1750','callarD':'100X1750','E':'1000X1750'},'SHV-E330':{'D':'500X1750','callarD':'100X1750','E':'1000X1750'}}\"")
    print unicode("                         ex. -xy \"{'LM-G710':{'D':'750X2800','callarD':'180X2800','E':'1280X2800'},'LM-Q725':{'D':'500X1900','callarD':'100X1900','E':'1000X1900'}}\"")

"""
json.loads("{'SM-G930':'{'D':'500X1750','callarD':'100X1750','E':'1000X1750'}','SHV-E330':'{'D':'500X1750','callarD':'100X1750','E':'1000X1750'}'}")
C:\_python\workspace\PycharmProjects\pyTest4AndroidonGithub\stressTest>python pyRetryCalling.py -xy "{'LM-G710':{'D':'750X2800','callarD':'180X2800','E':'1280X2800'},'LM-Q725':{'D':'500X1900','callarD':'150X1900','E':'1000X1900'}}" -m 10
"""

if __name__ == "__main__":
    AUTOMODE = True
    INSTALLAPKNAME = 'None'
    git_hashcode = 'None'
    git_revcnt = -1
    during_mins = 90
    SETUP_SUCESS = True
    NEED_SETUP = False
    EXTERNAL_XY = dict()
    while len(sys.argv) > 1:
        if len(sys.argv) > 1 and '--h' in sys.argv[1]:
            sys.argv.pop(1)
            printHelp()
            sys.exit(0)

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
        if len(sys.argv) > 1 and '-needsetup' in sys.argv[1]:
            sys.argv.pop(1)
            NEED_SETUP = True
        if len(sys.argv) > 1 and '-xy' in sys.argv[1]:
            sys.argv.pop(1)
            if len(sys.argv) > 1:
                print sys.argv[1]
                EXTERNAL_XY = json.loads(sys.argv[1].replace("'", "\""))
                sys.argv.pop(1)

    printEx("%s:%s" % ("NEED_SETUP", NEED_SETUP))
    printEx("%s:%s" % ("git_hashcode", git_hashcode))
    printEx("%s:%s" % ("git_revcnt", git_revcnt))
    printEx("%s:%s" % ("during_mins", during_mins))
    printEx("%s:%s" % ("INSTALLAPKNAME", INSTALLAPKNAME))
    printEx("%s:%s" % ("EXTERNAL_XY", EXTERNAL_XY))
    connected_Devices = getRealDevices()

    # printEx("%s:%s" % ("hashKeys", hashKeys))
    if len(connected_Devices) != 2:
        printError("len(connectingDevices) is " + str(len(connected_Devices)) + '! But, that is not available!')
        sys.exit(0)

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
            sys.exit(0)

        time.sleep(BASIC_DELAY)

    NEED2RESET = (SETUP_SUCESS == False)

    START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    endDatetime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9, minutes=during_mins))
    EXPECT_END_TIME = endDatetime.strftime("%Y%m%d%H%M")

    for DEVICE_ID in connected_Devices:
        LOGPROCESS, LOGINFO = setLogCat(selfs[DEVICE_ID])
        selfs[DEVICE_ID].setLogCat(LOGPROCESS, LOGINFO)
        selfs[DEVICE_ID].setTime(START______TIME, EXPECT_END_TIME)

    retryCount4NEED2RESET = 0
    faultCount = 0
    while long(EXPECT_END_TIME) > long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")):
        connectingDevices = getRealDevices()

        #printEx("%s:%s" % ("hashKeys", hashKeys))
        if len(connectingDevices) != 2:
            msg = "len(connectingDevices) is " + str(len(connectingDevices)) + '! But, that is not available!'
            printError(msg)
            setError(selfs, connectingDevices, msg)
            break
        if set(connected_Devices) != set(connectingDevices):
            msg = "%s:%s is changed under testing" % ("connected_Devices", connected_Devices)
            printEx(msg)
            setError(selfs, connectingDevices, msg)
            break
        else:
            DETECTID_4_LOW_BATTERY = None
            for DEVICE_ID in connected_Devices:
                selfs[DEVICE_ID].checkRSRP()
                if getBatteryLevel(DEVICE_ID) < THRESHOLD_BATTERY_MIN_LEVEL:
                    DETECTID_4_LOW_BATTERY = DEVICE_ID
            if DETECTID_4_LOW_BATTERY != None:
                msg = "One(%s) of devices is under the lowbattery(<%d). So test is stopped!" % (DETECTID_4_LOW_BATTERY, THRESHOLD_BATTERY_MIN_LEVEL)
                printError(msg)
                setError(selfs, connectingDevices, msg)
                break
            if faultCount > THRESHOLD_FAULT_MAX_COUNT:
                msg = "fault count(%d) reach the peak(%d). So test is stopped!" % (faultCount, THRESHOLD_FAULT_MAX_COUNT)
                printError(msg)
                setError(selfs, connectingDevices, msg)
                break
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
                    printEx("%s:%s" % ("KEYCODE_BACK", CurrentActivityName))
                    inputKeyEventInDevice(selfs[SELECTED_DEVICEID].DEVICE_ID, 'KEYCODE_HOME')
                    printEx("%s:%s" % ("KEYCODE_HOME", CurrentActivityName))
                    startActivity(selfs[SELECTED_DEVICEID].DEVICE_ID, ("%s/%s" % (TARGET_PACKAGENAME, LAUNCH_ACTIVITYNAME)), 1)
                    time.sleep(BASIC_DELAY)
                    CurrentActivityName = getCurrentActivity(selfs[SELECTED_DEVICEID].DEVICE_ID)
                    printEx("%s:%s" % ("CurrentActivityName", CurrentActivityName))
                    faultCount = faultCount + 1
                    if faultCount > MAX_RETRYCOUNT:
                        selfs[SELECTED_DEVICEID].FAILCOUNT_ARCALL_OUTGOING  += 1
                        NEED2RESET = True
                        break


                tapReDialOnDevice(selfs[SELECTED_DEVICEID], EXTERNAL_XY)
                time.sleep(BASIC_DELAY)
                tapDialOnDevice(selfs[SELECTED_DEVICEID], EXTERNAL_XY)
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
                    tapEndCallOnDevice(selfs[SELECTED_DEVICEID], EXTERNAL_XY)
                    time.sleep(BASIC_DELAY * 2)
                    CurrentActivityName = getCurrentActivity(selfs[SELECTED_DEVICEID].PARTNERID)
                    printEx("%s:%s" % ("getCurrentActivity", CurrentActivityName))
                    if LAUNCH_ACTIVITYNAME not in CurrentActivityName:
                        startActivity(selfs[SELECTED_DEVICEID].PARTNERID, ("%s/%s" % (TARGET_PACKAGENAME, LAUNCH_ACTIVITYNAME)), 1)
                        time.sleep(BASIC_DELAY)
                        CurrentActivityName = getCurrentActivity(selfs[SELECTED_DEVICEID].PARTNERID)
                        printEx("%s:%s" % ("reGetCurrentActivity", CurrentActivityName))

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
                    selfs[DEVICE_ID].printSliceInfo()

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