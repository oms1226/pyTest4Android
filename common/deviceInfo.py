# -*- coding: utf-8 -*-
import codecs
import json
import os
import subprocess

import sys

import time

import thread

from common.utils import printEx, printError, getExceptionString, os_systemEx, sendMessage, mkdirs

reload(sys)
sys.setdefaultencoding('utf-8')

def getWindowHeightFromWM(deviceId):
    reVal = None
    # "Physical size: 1440x2560"
    proc = subprocess.Popen("adb -s " + deviceId + " shell wm size", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        if 'Physical size: ' in line:
            reVal = line.strip('Physical size: ')
            break

    reVal = int(reVal.split('x')[1])
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getWindowWidthFromWM(deviceId):
    reVal = None
    # "Physical size: 1440x2560"
    proc = subprocess.Popen("adb -s " + deviceId + " shell wm size", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        if 'Physical size: ' in line:
            reVal = line.strip('Physical size: ')
            break

    reVal = int(reVal.split('x')[0])
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getWindowDensityFromWM(deviceId):
    reVal = None
    # "Physical size: 1440x2560"
    proc = subprocess.Popen("adb -s " + deviceId + " shell wm density", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        if 'density:' in line:
            reVal = line.split(' ')[-1]

    reVal = int(reVal)
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getWindowWidthFromDumpsys(deviceId):
    """
    herolteskt:/ $ dumpsys window displays | grep dpi
    init=1440x2560 640dpi base=1080x1920 480dpi cur=1080x1920 app=1080x1920 rng=1080x1008-1920x1848
    """
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell dumpsys window displays | grep dpi", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        if 'cur=' in line:
            reVal = line.split('cur=')[1].split(' ')[0]
            if 'base=' in line:
                break

    reVal = int(reVal.split('x')[0])
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getWindowHeightFromDumpsys(deviceId):
    """
    herolteskt:/ $ dumpsys window displays | grep dpi
    init=1440x2560 640dpi base=1080x1920 480dpi cur=1080x1920 app=1080x1920 rng=1080x1008-1920x1848
    """
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell dumpsys window displays | grep dpi", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        if 'cur=' in line:
            reVal = line.split('cur=')[1].split(' ')[0]
            if 'base=' in line:
                break

    reVal = int(reVal.split('x')[1])
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getWindowDensityFromDumpsys(deviceId):
    """
    herolteskt:/ $ dumpsys window displays | grep dpi
    init=1440x2560 640dpi base=1080x1920 480dpi cur=1080x1920 app=1080x1920 rng=1080x1008-1920x1848
    """
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell dumpsys window displays | grep dpi", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        if 'cur=' in line:
            for word in line.split(' '):
                if 'dpi' in word:
                    reVal = word.strip('dpi')
            if 'base=' in line:
                break

    reVal = int(reVal)
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getPhoneNumberFromDevice(deviceId):
    """
    herolteskt:/ $ service call iphonesubinfo 15
    Result: Parcel(
      0x00000000: 00000000 0000000b 00310030 00360030 '........0.1.0.6.'
      0x00000010: 00340034 00300034 00380036 00000031 '4.4.4.0.6.8.1...')
    """
    reVal = ''

    os_systemEx("adb -s " + deviceId + " root")
    for index in (14, 15, 16):
        proc = subprocess.Popen("adb -s " + deviceId + " shell service call iphonesubinfo " + str(index), stdout=subprocess.PIPE)
        fd_popen = proc.stdout

        content = fd_popen.read().strip()
        prefix = False
        for line in content.split('\r\n'):
            if '0x000000' in line:
                reVal = reVal + line.split('\'')[1].replace('.', '')
                if '010' in reVal and prefix == False:
                    reVal = '010' + ''.join(reVal.split('010')[1:])
                    prefix = True

        if '010' in reVal:
            reVal = reVal[:11]
            break
        else:
            reVal = ''

        try:
            proc.kill()
        except:
            printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    if reVal == '':
        reVal = None


    return reVal

def getManufacturerFromDevice(deviceId):
    """
    greatlteks:/ $ getprop | grep 'ro.product.manufacturer'
    [ro.product.manufacturer]: [samsung]
    """
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell getprop | grep 'ro.product.manufacturer'", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = line.split(' ')[-1].replace('[', '').replace(']', '')

    if reVal == '':
        reVal = None
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getModelNameFromDevice(deviceId):
    """
    greatlteks:/ $ getprop | grep 'ro.product.model'
    [ro.product.model]: [SM-N950N]
    """
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell getprop | grep '\[ro.product.model\]'", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = line.split(']:')[-1].replace('[', '').replace(']', '').replace('\r', '').replace('\n', '').replace(' ', '')

    if reVal == '':
        reVal = None
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))
    if reVal == None:
        reVal = 'NONE'

    return reVal

def getOSVersionFromDevice(deviceId):
    """
    greatlteks:/ $ getprop | grep 'ro.build.version.release'
    [ro.build.version.release]: [7.1.1]
    """
    reVal = None

    proc = subprocess.Popen("adb -s " + deviceId + " shell getprop | grep 'ro.build.version.release'", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = line.split(' ')[-1].replace('[', '').replace(']', '').replace(' ', '')

    if reVal == '':
        reVal = None
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getManufactureVersionFromDevice(deviceId):
    """
    greatlteks:/ $ getprop | grep 'ro.build.version.incremental'
    [ro.build.version.incremental]: [N950NKSU1AQHA]
    """
    reVal = None

    proc = subprocess.Popen("adb -s " + deviceId + " shell getprop | grep 'ro.build.version.incremental'", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = line.split(' ')[-1].replace('[', '').replace(']', '').replace('\r', '').replace('\n', '').replace(' ', '')

    if reVal == '':
        reVal = None
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getAbiFromDevice(deviceId):
    reVal = None

    proc = subprocess.Popen("adb -s " + deviceId + " shell getprop | grep '\[ro.product.cpu.abi\]'", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = line.split(' ')[-1].replace('[', '').replace(']', '').replace('\r', '').replace('\n', '').replace(' ', '')
        break

    if reVal == '':
        reVal = None
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getPlatformFromDevice(deviceId):
    reVal = None

    proc = subprocess.Popen("adb -s " + deviceId + " shell getprop | grep '\[ro.board.platform\]'", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = line.split(' ')[-1].replace('[', '').replace(']', '').replace('\r', '').replace('\n', '').replace(' ', '')
        break

    if reVal == '':
        reVal = None
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getBoardFromDevice(deviceId):
    reVal = getPlatformFromDevice(deviceId)

    if reVal == None:
        proc = subprocess.Popen("adb -s " + deviceId + " shell getprop | grep 'ro.product.board'", stdout=subprocess.PIPE)
        fd_popen = proc.stdout

        content = fd_popen.read().strip()
        for line in content.split('\r\n'):
            reVal = line.split(' ')[-1].replace('[', '').replace(']', '').replace('\r', '').replace('\n', '').replace(' ', '')
            break

        if reVal == '':
            reVal = None
        try:
            proc.kill()
        except:
            printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getValueFromDevice(deviceId, field):
    reVal = None

    proc = subprocess.Popen("adb -s " + deviceId + " shell getprop | grep '\[" + field + "\]'", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = line.split(' ')[-1].replace('[', '').replace(']', '').replace('\r', '').replace('\n', '').replace(' ', '')
        break

    if reVal == '':
        reVal = None
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getPropFromDevice(deviceId):
    """
    greatlteks:/ $ getprop
    ...
    [ro.build.version.incremental]: [N950NKSU1AQHA]
    ...
    """
    reVal = "{"

    proc = subprocess.Popen("adb -s " + deviceId + " shell getprop", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = reVal + line.replace('[', '"').replace(']', '"').replace('""0.pool.ntp.org""', '"0.pool.ntp.org"').replace('\r', '').replace('\n', '') + ','
    if reVal.endswith(','):
        reVal = reVal[:-1] + '}'

    reVal = json.loads(reVal)

    printEx( "%s:%s" % ("type(reVal)", type(reVal)) )
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getDevices():
    """
    C:\Users\owner>adb devices
    List of devices attached
    ce041604d87a073904      device
    ce06171633773534027e    device
    """
    reVal = []

    proc = subprocess.Popen("adb devices", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        #if "42f06002482d4f53" in line:
        #    continue
        if 'List of' not in line and 'device' in line:
            reVal.append(line.split('\t')[0])

    #printEx( "%s:%s" % ("type(reVal)", type(reVal)) )
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getBatteryLevel(deviceId):
    """
    greatlteks:/ # dumpsys battery | grep level
      level: 91
    """
    reVal = None

    proc = subprocess.Popen("adb -s " + deviceId + " shell dumpsys battery | grep level", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        if len(line.split(':')) >= 2:
            reVal = line.split(':')[1].strip()
    if reVal != None:
        reVal = int(reVal)
    else:
        reVal = -1
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getPackageVersionName(deviceId, packageName):
    """
    C:\_python\workspace\PycharmProjects\lmcst\CallRecordingTest>adb shell "dumpsys package com.google.android.googlequicksearchbox | grep versionName"
    versionName=6.12.25.21.arm64
    """
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell dumpsys package " + packageName, stdout=subprocess.PIPE)

    content = proc.stdout.read().strip()
    for line in content.split('\r\n'):
        if 'versionName' in line:
            reVal = line.split('=')[1]
            break

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

def getPackageVersionCode(deviceId, packageName):
    """
    C:\_python\workspace\PycharmProjects\lmcst\CallRecordingTest>adb shell "dumpsys package com.google.android.googlequicksearchbox | grep versionCode"
        versionCode=300729371 minSdk=21 targetSdk=24
    """
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell dumpsys package " + packageName, stdout=subprocess.PIPE)

    content = proc.stdout.read().strip()
    for line in content.split('\r\n'):
        if 'versionCode' in line:
            reVal = line.split('=')[1].split(' ')[0]
            break

    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal

class logInfo:
    #print 'adb logcat -v threadtime -s TPhone:E DEBUG:F System.err:V AndroidRuntime:V ActivityManager:E'
    FileForceWriteList = [
        'F DEBUG',
        'System.err',
        'AndroidRuntime',
        'E ActivityManager',
    ]
    def __init__(self):
        self.info = dict()
        self.info['PIDS'] = []
        self.info['TIDS'] = []
        self.info['TAGLIST'] = []
        self.info['TOTAL#'] = 0
        self.info['V'] = 0
        self.info['D'] = 0
        self.info['I'] = 0
        self.info['W'] = 0
        self.info['E'] = 0
        self.info['F'] = 0
    def getAllInfo(self):
        if self.info.has_key('PIDS') and len(self.info['PIDS']) > 0:
            self.info['PIDS#'] = len(set(self.info['PIDS']))
        del self.info['PIDS']
        if self.info.has_key('TIDS') and self.info['TIDS'] > 0:
            self.info['TIDS#'] = len(set(self.info['TIDS']))
        del self.info['TIDS']
        if self.info.has_key('TAGLIST') and len(self.info['TAGLIST']) > 0:
            self.info['TAGLIST#'] = len(set(self.info['TAGLIST']))
        del self.info['TAGLIST']
        return json.dumps(self.info).replace('\\', '')
    def setInfo(self, key, value):
        self.info[key] = value
    def getInfo(self, key):
        return self.info[key]

def getProc4LogCat(**options):
    """
    09-25 16:33:08.961   255   736 V AwesomePlayer: mSecMediaClock clear
    09-25 16:33:08.961  2597  2597 D dalvikvm: Trying to load lib /data/app-lib/com.google.android.gms-3/libgmscore.so 0x420d7590
    """
    os_systemEx("adb -s " + options.get("DEVICE_ID") + " logcat -c")
    def getLogCat(proc, logI, options):
        """
        **options
            logfullfilename, tag, searchWord, reportNum
        """
        logfullfilename = options.get("logfullfilename")
        tag = options.get("tag")
        searchWord = options.get("searchWord")
        reportNum = options.get("reportNum")
        count = 0
        while proc.poll() is None:
            output = proc.stdout.readline()
            #output = output.replace("  ", "")
            output = ' '.join(output.split())

            if logfullfilename != None:
                try:
                    isWriteFile = False
                    for word in logInfo.FileForceWriteList:
                        if word in output:
                            isWriteFile = True
                    if isWriteFile == False and tag == 'ALL':
                        isWriteFile = True
                    if isWriteFile == False and tag != None:
                        if tag in output:
                            isWriteFile = True
                    if searchWord != None:
                        if searchWord in output:
                            isWriteFile = True
                            if reportNum != None:
                                sendMessage(options.get("MYNUM"), reportNum, (
                                "%s 모델의 %s 분 통화녹음테스트 중 로그에서 '%s'가 발견: %s" % (options.get("MODEL"), str(options.get("during_mins")), searchWord, output)))
                                reportNum = None

                    if isWriteFile:
                        printEx("%s:%s" % ("output", output))
                        mkdirs(logfullfilename)
                        #with codecs.open(logfullfilename, 'a', 'utf-8') as f:
                        with open(logfullfilename, 'a') as f:
                            try:
                                f.write(output + "\n")
                            finally:
                                f.close()

                        count = count + 1
                        logI.setInfo('TOTAL#', count)

                        items = output.split(' ')
                        if len(items) >= 7:
                            if tag != None:
                                # PIDS
                                key = 'PIDS'
                                if items[2] != None and int(items[2]) not in logI.getInfo(key):
                                    logI.getInfo(key).append(int(items[2]))

                                # TIDS
                                key = 'TIDS'
                                if items[3] != None and int(items[3]) not in logI.getInfo(key):
                                    logI.getInfo(key).append(int(items[3]))

                                # LOGLEVEL
                                logI.setInfo(items[4], logI.getInfo(items[4]) + 1)

                            key = 'TAGLIST'
                            if ':' in items[5]:
                                items[5] = items[5].split(':')[0]
                            if ' ' in items[5]:
                                items[5] = items[5].strip()

                            if items[5] != None and items[5] not in logI.getInfo(key):
                                logI.getInfo(key).append(items[5])
                except:
                    printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

            #print output

    proc = subprocess.Popen("adb -s " + options.get("DEVICE_ID") + " shell logcat -v threadtime", stdout=subprocess.PIPE)
    logI = logInfo()
    thread.start_new_thread(getLogCat, (proc, logI, options))

    return proc, logI

def getRealDevices():
    reVal = []

    for device in getDevices():
        if 'emulator' not in device:
            reVal.append(device)

    return reVal


NeedFields = {
"ro.product.cpu",
"ro.product.model",
"ro.build.version",
"gsm.operator",
"ro.chipname",
"ro.arch",
"ro.hardware",
"ro.board",
"ro.product.board",
"ro.product.manufacturer",
"ril.modem.board",
"persist.ril.modem.board",
}

def getPropFromDeviceByNeedField(deviceId):
    """
    greatlteks:/ $ getprop
    ...
    [ro.build.version.incremental]: [N950NKSU1AQHA]
    ...
    """
    reVal = "{"

    proc = subprocess.Popen("adb -s " + deviceId + " shell getprop", stdout=subprocess.PIPE)
    fd_popen = proc.stdout

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        isNeed = False
        for field in NeedFields:
            if field in line:
                isNeed = True
        if isNeed:
            reVal = reVal + line.replace('[', '"').replace(']', '"').replace('""0.pool.ntp.org""', '"0.pool.ntp.org"').replace('\r', '').replace('\n', '') + ','
    if reVal.endswith(','):
        reVal = reVal[:-1] + '}'

    reVal = json.loads(reVal)

    printEx( "%s:%s" % ("type(reVal)", type(reVal)) )
    try:
        proc.kill()
    except:
        printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

    return reVal


if __name__ == "__main__":
    myName = sys.argv[0].split('/')[-1]
    print("%s:%s" % ("myName", myName))

    for DEVICE_ID in getDevices():
        print("%s:%s" % ("DEVICE_ID", DEVICE_ID))
        print("%s:%s" % ("call", "oms1226"))
        reVal = getPropFromDevice(DEVICE_ID);
        print("%s:%s" % ("getPropFromDevice", reVal))

        if os.path.exists("C:\\lmcft_log\\common\\") == False:
            mkdirs("C:\\lmcft_log\\common\\")

        with codecs.open("C:\\lmcft_log\\common\\modelInfo4getprop.log", 'a', 'utf-8') as f:
            f.write(json.dumps(reVal, ensure_ascii=False) + "\r\n")
            f.close()

        reVal = getPropFromDeviceByNeedField(DEVICE_ID);
        print("%s:%s" % ("getPropFromDeviceByNeedField", reVal))

        with codecs.open("C:\\lmcft_log\\common\\HD_AR_ShortList.txt", 'a', 'utf-8') as f:
            f.write(json.dumps(reVal, ensure_ascii=False) + "\r\n")
            f.close()

        reVal = getPropFromDeviceByNeedField(DEVICE_ID);
        print("%s:%s" % ("getPropFromDeviceByNeedField", reVal))

        with codecs.open("C:\\lmcft_log\\common\\HD_AR_ShortList_20180129.txt", 'a', 'utf-8') as f:
            f.write(json.dumps(reVal, ensure_ascii=False) + "\r\n")
            f.close()

    if False :
        for DEVICE_ID in getDevices():
            print( "%s:%s" % ("DEVICE_ID", DEVICE_ID) )
            print( "%s:%s" % ("getPropFromDevice", getPropFromDevice(DEVICE_ID)) )
            print( "%s:%s" % ("getWindowWidthFromWM", getWindowWidthFromWM(DEVICE_ID)) )
            print( "%s:%s" % ("getWindowHeightFromWM", getWindowHeightFromWM(DEVICE_ID)) )
            print( "%s:%s" % ("getWindowDensityFromWM", getWindowDensityFromWM(DEVICE_ID)) )

            print( "%s:%s" % ("getWindowWidthFromDumpsys", getWindowWidthFromDumpsys(DEVICE_ID)) )
            print( "%s:%s" % ("getWindowHeightFromDumpsys", getWindowHeightFromDumpsys(DEVICE_ID)) )
            print( "%s:%s" % ("getWindowDensityFromDumpsys", getWindowDensityFromDumpsys(DEVICE_ID)) )

            print( "%s:%s" % ("getManufacturerFromDevice", getManufacturerFromDevice(DEVICE_ID)) )
            print( "%s:%s" % ("getModelNameFromDevice", getModelNameFromDevice(DEVICE_ID)) )
            print( "%s:%s" % ("getOSVersionFromDevice", getOSVersionFromDevice(DEVICE_ID)) )
            print( "%s:%s" % ("getManufactureVersionFromDevice", getManufactureVersionFromDevice(DEVICE_ID)) )
            print( "%s:%s" % ("getPhoneNumberFromDevice", getPhoneNumberFromDevice(DEVICE_ID)) )
            print( "%s:%s" % ("getBatteryLevel", getBatteryLevel(DEVICE_ID)) )


    if False:
        class test:
            def __init__(self):
                self.MODEL = 'test'
                self.MYNUM = '114'
                self.DEVICE_ID = 'ce041604d87a073904'
                argcs = {'tag': 'TPhone',
                         'logfullfilename': 'C:\\lmcft_log\\fail\\\\pyCallRecordingTestMultiThread\\SM-G930S\\20170925184612\\Logcat_TPhone_dalvikvm_com.skt.prod.dialer_SKT1110478-PC_SM-G930S_7.0_20170925184612_10.log',
                         'searchWord': 'dalvikvm', 'reportNum': '01064440681'}
                LOGPROCESS, LOGINFO = getProc4LogCat(self, **argcs)
                time.sleep(10)
                print (LOGINFO.getAllInfo())
                #print( "%s:%s" % ("getLogCat", getProc4LogCat(DEVICE_ID)) )
        test()





