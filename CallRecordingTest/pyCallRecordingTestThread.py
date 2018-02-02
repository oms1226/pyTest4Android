# -*- coding: utf-8 -*-
import codecs
import datetime
from time import mktime
import random
import re
import socket
import threading
import traceback
from sys import platform as _platform

import shutil
import speech_recognition as sr
import sys

from common import deviceCompat
from common.deviceCompat import getLocationOnDialPad, getKey4LocationOnDialPad, getLocationOnDialPad
from common.deviceInfo import *
from common.utils import *
from common.contant import *
#Unexpected error: <type 'exceptions.UnicodeEncodeError'>'ascii' codec can't encode characters in position 43-47: ordinal not in range(128)
reload(sys)
sys.setdefaultencoding('utf-8')

RECORDFOLDERLIST = {
    'com.skt.prod.dialer': '/sdcard/.TPhoneCallRecords/.nomedia/',
    'com.nll.acr': '/storage/emulated/0/ACRCalls/',
    'com.boldbeast.recorder': '/storage/emulated/0/com.boldbeast.recorder/rec/',
    'com.killermobile.totalrecall': '/storage/emulated/0TotalRecall/',
}

RECORDFILE_PREFIXLIST = {
    'com.skt.prod.dialer': 'CallRec_%PHONENUMBER%',
    'com.nll.acr': '%PHONENUMBER%',
    'com.boldbeast.recorder': '',
    'com.killermobile.totalrecall': '',
}

class pyCallRecordingTestThread (threading.Thread):
    def __init__(self, run_event, selfVersion, threadID, name, deviceID, myNum, packageName, appVersion, during_mins,
                 log_coverage, monkey, demands, **options):
        threading.Thread.__init__(self)
        self.__started = run_event
        self.threadID = threadID
        self.name = name

        self.pids = []
        self.resultS = dict()

        self.resultS['selfVersion'] = self.selfVersion = selfVersion
        self.resultS['DEVICE_ID'] = self.DEVICE_ID = deviceID
        self.resultS['MYNUM'] = self.MYNUM = myNum

        self.resultS['WIDTH'] = self.WIDTH =  getWindowWidthFromDumpsys(deviceID)
        self.resultS['HEIGHT'] = self.HEIGHT =  getWindowHeightFromDumpsys(deviceID)
        self.resultS['DENSITY'] = self.DENSITY =  getWindowDensityFromDumpsys(deviceID)
        self.resultS['MANUFACTURER'] = self.MANUFACTURER =  getManufacturerFromDevice(deviceID)
        self.resultS['MODEL'] = self.MODEL =  getModelNameFromDevice(deviceID)
        self.resultS['OSVERSION'] = self.OSVERSION =  getOSVersionFromDevice(deviceID)
        self.resultS['MANUFACTURERVERSION'] = self.MANUFACTURERVERSION =  getManufactureVersionFromDevice(deviceID)
#        self.resultS['SYSTEMPROPERTY'] = self.SYSTEMPROPERTY =  getPropFromDevice(deviceID)

        self.resultS['googlequicksearchbox_versionname'] = getPackageVersionName(deviceID, 'com.google.android.googlequicksearchbox')
        self.resultS['googlequicksearchbox_versioncode'] = getPackageVersionCode(deviceID, 'com.google.android.googlequicksearchbox')

        self.RECORDING_SEC = 20
        self.resultS['RECORDING_SEC'] = self.RECORDING_SEC
        self.WAIT_SEC = 5
        self.resultS['WAIT_SEC'] = self.WAIT_SEC
        self.SMALL_SEC = 1
        self.resultS['SMALL_SEC'] = self.SMALL_SEC
        self.resultS['WAITDEADLINE_SEC'] = self.WAITDEADLINE_SEC = 20
        self.resultS['INCOMING_SETTING_MIN'] = self.INCOMING_SETTING_MIN = 7
        self.LOCALTEST = False
        self.resultS['LOCALTEST'] = self.LOCALTEST
        self.resultS['PACKAGENAME'] = self.PACKAGENAME = packageName
        if RECORDFOLDERLIST.get(packageName) == None:
            self.DEVICE_RECORDFOLDER = '/sdcard/.TPhoneCallRecords/.nomedia/'
        else:
            self.DEVICE_RECORDFOLDER = RECORDFOLDERLIST.get(packageName)
        self.resultS['DEVICE_RECORDFOLDER'] = self.DEVICE_RECORDFOLDER

        self.resultS['APPVERSION'] = self.APPVERSION = appVersion

        self.myName = sys.argv[0].split('/')[-1]
        printEx( "%s:%s" % ("myName", self.myName))
        self.resultS['ID_FILENAME'] = self.myName

        self.hostname = socket.gethostname()
        self.resultS['hostname'] = self.hostname
        self.START_TIME = strftime("%Y%m%d%H%M%S", localtime())
        self.resultS['START_TIME'] = self.START_TIME
        self.during_mins = during_mins
        self.resultS['duringHours'] = during_mins / 60
        self.resultS['LOG_COVERAGE'] = self.LOG_COVERAGE = log_coverage
        self.resultS['MONKEY'] = self.MONKEY = monkey
        self.resultS['DEMANDS'] = self.DEMANDS = demands
        self.resultS['LMCFT_FOLDER_FAIL'] = self.LMCFT_FOLDER_FAIL = LMCFT_FOLDER_FAIL + self.myName.split('.')[0] + "\\" + self.MODEL + "\\" + self.START_TIME + "\\"

        self.failListFileName = self.LMCFT_FOLDER_FAIL + \
                                "FailList" + "_" + self.PACKAGENAME + "_" + self.hostname + "_" + self.MODEL + "_" + self.OSVERSION + "_" + self.START_TIME + "_" + str(during_mins) + ".log"
        self.resultFileName = LMCFT_FOLDER_RESULT + \
                              "Result" + "_" + self.myName.split('.')[0] + ".log"

        if options.get('LOGCAT'):
            self.resultS['LOGCAT'] = self.LOGCAT = options.get('LOGCAT')
            self.resultS['TAG'] = self.TAG = options.get('TAG')
            self.resultS['SEARCHWORD'] = self.SEARCHWORD = options.get('SEARCHWORD')
            self.resultS['reportNum'] = self.REPORTNUM = options.get('reportNum')
            args = {}

            tagName = 'NONE'
            if self.TAG != None:
                tagName = self.TAG.replace(' ', '-')
            searchName = 'NONE'
            if self.SEARCHWORD != None:
                searchName = self.SEARCHWORD

            self.resultS['logfullfilename'] = args["logfullfilename"] = self.LMCFT_FOLDER_FAIL + \
                                "Logcat" + "_" + tagName + '_' + searchName + '_' + self.PACKAGENAME + "_" + self.hostname + "_" + self.MODEL + "_" + self.OSVERSION + "_" + self.START_TIME + "_" + str(during_mins) + ".log"
            args["tag"] = self.TAG
            args["searchWord"] = self.SEARCHWORD
            args["reportNum"] = self.REPORTNUM
            args["DEVICE_ID"] = self.DEVICE_ID
            args["MYNUM"] = self.MYNUM
            args["MODEL"] = self.MODEL
            args["during_mins"] = self.during_mins
            self.LOGPROCESS, self.LOGINFO = getProc4LogCat(**args)
        else:
            self.LOGPROCESS = None
            self.LOGINFO = None

        self.DIALPAD_KEY = getKey4LocationOnDialPad(self.selfVersion, self.APPVERSION, self.MANUFACTURER, self.MODEL, self.WIDTH, self.HEIGHT, self.DENSITY)
        if self.DIALPAD_KEY == None:
            self.resultS['ERROR'] = ".DIALPAD_KEY(None)"

        printEx( "%s:%s" % ("self.resultS", self.resultS))
        sendMessage('01064440681', self.MYNUM, ("%s 모델의 %s 분 통화녹음테스트를 시작." % (self.MODEL, str(self.during_mins))))
        time.sleep(self.WAIT_SEC * 3)


    """
    0 = indicates idle,
    1 = ringing and
    2 = active call
    """
    def checkCallState(self):
        reVal = None
        proc = subprocess.Popen("adb -s " + self.DEVICE_ID + " shell dumpsys telephony.registry | grep mCallState", stdout=subprocess.PIPE)
        fd_popen = proc.stdout
        self.pids.append(proc.pid)

        content = fd_popen.read().strip()
        for line in content.split('\r\n'):
            if 'mCallState' in line:
                reVal = line.strip()
                break
            elif 'not Found' in line:
                reVal = None
                break
        if reVal != None:
            printEx( "checkCallState(%s) --> (%s)" % (self.DEVICE_ID, reVal.split('=')[1]))
            reVal = int(reVal.split('=')[1])

        return reVal

    def callPhone(self, ongoingNumber):
        reVal = True
        waitTime = 0
        try:
            if self.checkCallState() != 0:
                raise Exception('callPhone', self.checkCallState())

            while self.checkCallState() == 0:
                proc = subprocess.Popen(
                    "adb -s " + self.DEVICE_ID + " shell am start -a android.intent.action.CALL tel:" + ongoingNumber,
                    stdout=subprocess.PIPE)
                self.pids.append(proc.pid)
                time.sleep(self.WAIT_SEC)
                waitTime = waitTime + self.WAIT_SEC
                printEx( "%s:%s" % ("waitTime", waitTime))
                if waitTime > self.WAITDEADLINE_SEC:
                    printEx( "%s:%s" % ("Calling", "Fail"))
                    reVal = False
                    break
        except:
            printError("%s:%s" % ("Unexpected error in " + self.MODEL, getExceptionString(sys.exc_info())))
            reVal = False

        return reVal;

    def acceptPhone(self):
        reVal = True
        waitTime = 0
        try:
            if self.checkCallState() != 1:
                raise Exception('acceptPhone', self.checkCallState())
            count = 0
            while self.checkCallState() == 1:
                count = count + 1
                if count > 2:
                    proc = subprocess.Popen("adb -s " + self.DEVICE_ID + " shell radiooptions 9 1 0",
                                            stdout=subprocess.PIPE)
                else:
                    proc = subprocess.Popen("adb -s " + self.DEVICE_ID + " shell input keyevent KEYCODE_CALL",
                                            stdout=subprocess.PIPE)

                self.pids.append(proc.pid)
                time.sleep(self.WAIT_SEC)
                waitTime = waitTime + self.WAIT_SEC
                printEx( "%s:%s" % ("waitTime", waitTime))
                if waitTime > self.WAITDEADLINE_SEC:
                    printEx( "%s:%s" % ("acceptPhone", "Fail"))
                    reVal = False
                    break
        except:
            printError("%s:%s" % ("Unexpected error in " + self.MODEL, getExceptionString(sys.exc_info())))
            reVal = False

        return reVal;



    def endPhone(self):
        reVal = True
        waitTime = 0
        try:
            #if self.checkCallState() == 0:
            #    raise Exception('endPhone', self.checkCallState())
            count = 0
            while self.checkCallState() != 0:
                count = count + 1
                if count > 2:
                    proc = subprocess.Popen("adb -s " + self.DEVICE_ID + " shell radiooptions 10 1 0",
                                            stdout=subprocess.PIPE)
                else:
                    proc = subprocess.Popen("adb -s " + self.DEVICE_ID + " shell input keyevent KEYCODE_ENDCALL", stdout=subprocess.PIPE)

                self.pids.append(proc.pid)
                time.sleep(self.WAIT_SEC)
                waitTime = waitTime + self.WAIT_SEC
                printEx( "%s:%s" % ("waitTime", waitTime))
                if waitTime > self.WAITDEADLINE_SEC:
                    printEx( "%s:%s" % ("endPhone", "Fail"))
                    reVal = False
                    break
        except:
            printError("%s:%s" % ("Unexpected error in " + self.MODEL, getExceptionString(sys.exc_info())))
            reVal = False

        return reVal;


    def covertAudioFile(self, fileName, fileType):
        reVal = fileName + "." + fileType
        if DEBUG():
            if _platform == "linux" or _platform == "linux2":
                os_systemEx("ffmpeg -i " + fileName + " " + reVal)
            else:
                os_systemEx("ffmpeg.exe -i " + fileName + " " + reVal)
        else:
            if _platform == "linux" or _platform == "linux2":
                os_systemEx("ffmpeg -v 0 -i " + fileName + " " + reVal)
            else:
                os_systemEx("ffmpeg.exe -v 0 -i " + fileName + " " + reVal)

        #time.sleep(self.WAIT_SEC*3)

        if os.path.isfile(reVal) == False:
            reVal = None

        return reVal

    def availableIncomingRecording(self):
        reVal = False
        dateHM = getDateInDevice(self.DEVICE_ID)

        limitation = self.WAIT_SEC
        while (limitation >= 10):
            limitation = limitation / 2
        limitation = 10 - limitation

        if limitation > int(dateHM[3]):
            reVal = True

        return reVal

    def isItNowIncomingSettingTime(self):
        reVal = False
        dateHM = getDateInDevice(self.DEVICE_ID)

        if self.INCOMING_SETTING_MIN == int(dateHM[3]):
            reVal = True

        return reVal


    def getSetDateInDevice(self):
        reVal = None
        reVal = getDateInDevice(self.DEVICE_ID)
        if int(reVal[2]) >= 5:
            reVal[2] = '0'
            if int(reVal[0]) < 2:
                if int(reVal[1]) >= 9:
                    reVal[0] = str(int(reVal[0]) + 1)
                    reVal[1] = '0'
                else:
                    reVal[1] = str(int(reVal[1]) + 1)
            else:
                if int(reVal[1]) >= 3:
                    reVal[0] = '0'
                    reVal[1] = '0'
                else:
                    reVal[1] = str(int(reVal[1]) + 1)
        else:
            reVal[2] = str(int(reVal[2])+1)

        reVal[3] = '0'
        return reVal

    def tapPasswordOnDevice(self):
        time.sleep(self.SMALL_SEC)
        time.sleep(self.SMALL_SEC)
        time.sleep(self.SMALL_SEC)
        tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('keypad', self.DIALPAD_KEY))
        time.sleep(self.SMALL_SEC)
        tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('0', self.DIALPAD_KEY))
        time.sleep(self.SMALL_SEC)
        tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('9', self.DIALPAD_KEY))
        time.sleep(self.SMALL_SEC)
        tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('1', self.DIALPAD_KEY))
        time.sleep(self.SMALL_SEC)
        tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('8', self.DIALPAD_KEY))
        time.sleep(self.SMALL_SEC)
        time.sleep(self.WAIT_SEC)
        tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('3', self.DIALPAD_KEY))
        time.sleep(self.WAIT_SEC)
        tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('2', self.DIALPAD_KEY))
        time.sleep(self.WAIT_SEC)
        time.sleep(self.SMALL_SEC)
        time.sleep(self.SMALL_SEC)

    def setMorningCall(self):
        reVal = None
        try:
            if self.checkCallState() != 0:
                raise Exception('setMorningCall', self.checkCallState())

            while self.checkCallState() == 0:
                self.callPhone(self.MYNUM)
                time.sleep(self.SMALL_SEC)

            self.tapPasswordOnDevice()

            reVal = self.getSetDateInDevice()
            for num in reVal:
                printEx( "%s:%s" % ("num", num))
                tapOnDevice(self.DEVICE_ID, getLocationOnDialPad(num, self.DIALPAD_KEY))
                time.sleep(0.5)
            time.sleep(self.WAIT_SEC)
            tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('0', self.DIALPAD_KEY))
            time.sleep(0.5)
            tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('1', self.DIALPAD_KEY))
            time.sleep(self.WAIT_SEC)
            time.sleep(self.WAIT_SEC)
            printEx( "%s:%s" % ("endPhone", self.endPhone()))
        except:
            printError("%s:%s" % ("Unexpected error in " + self.MODEL, getExceptionString(sys.exc_info())))
            reVal = None
        return reVal


    def unSetMorningCall(self):
        reVal = True
        try:
            if self.checkCallState() != 0:
                raise Exception('unSetMorningCall', self.checkCallState())

            while self.checkCallState() == 0:
                self.callPhone(self.MYNUM)
                time.sleep(self.SMALL_SEC)

            self.tapPasswordOnDevice()
            tapOnDevice(self.DEVICE_ID, getLocationOnDialPad('1', self.DIALPAD_KEY))
            time.sleep(self.WAIT_SEC)

            printEx( "%s:%s" % ("endPhone", self.endPhone()))
        except:
            printError("%s:%s" % ("Unexpected error in " + self.MODEL, getExceptionString(sys.exc_info())))
            reVal = False
        return reVal

    def compareDate(self, dateHM):
        reVal = None
        try:
            cDateHM = getDateInDevice(self.DEVICE_ID)
            if cmp(cDateHM, dateHM) == 0:
                reVal = 0
            if reVal == None:
                if int(dateHM[len(dateHM)-1]) == int(cDateHM[len(dateHM)-1]):
                    for i in range(len(dateHM)-2, -1, -1):
                        if int(dateHM[i]) == int(cDateHM[i]):
                            pass
                        else:
                            reVal = 1
                            break
                else:
                    if int(cDateHM[len(dateHM) - 1]) >= self.INCOMING_SETTING_MIN:
                        reVal = -1
                    else:
                        reVal = 1
        except:
            printError("%s:%s" % ("Unexpected error in " + self.MODEL, getExceptionString(sys.exc_info())))
            reVal = 1

        return reVal

    def requestIncomingRecording(self):
        reVal = '0112008585'
        time4MonrningCall = self.setMorningCall()
        printEx( "%s:%s" % ("setMorningCall", time4MonrningCall))

        printEx( "%s:%s" % ("cleanRecordingFileinDevice", self.cleanRecordingFileinDevice()))
        if time4MonrningCall == None:
            raise Exception('setMorningCall', "fail")

        waitTime = 0
        while self.checkCallState() != 1:
            compareIndex = self.compareDate(time4MonrningCall)
            printEx( "%s:%s" % ("compareDate", compareIndex))
            if compareIndex > 0 or self.checkCallState() == 2:
                printEx( "%s:%s" % ("MorningCall", "Fail"))
                reVal = None
                break
            time.sleep(self.WAIT_SEC)
            waitTime = waitTime + self.WAIT_SEC
            printEx( "%s:%s" % ("waitTime", waitTime))

        if reVal != None:
            printEx( "%s:%s" % ("acceptPhone", self.acceptPhone()))
            waitTime = 0
            while waitTime < self.RECORDING_SEC:
                time.sleep(self.SMALL_SEC)
                waitTime = waitTime + self.SMALL_SEC
                printEx( "%s(%s sec)" % ("RECORDING", waitTime))
            printEx( "%s:%s" % ("endPhone", self.endPhone()))
        else:
            printEx( "%s:%s" % ("unSetMorningCall", self.unSetMorningCall()))

        return reVal


    def requestOutcomingRecording(self, phoneNumber):
        phonenumbers = ['114', '1508']
        phonenumbers.append(phoneNumber)
        reVal = phonenumbers[random.randrange(0, len(phonenumbers))]
        printEx( "%s(%s)" % ("reVal", reVal))
        isCalling = self.callPhone(reVal)
        printEx( "%s:%s" % ("callPhone", isCalling))

        if isCalling == False:
            reVal = None
            #raise Exception('requestOutcomingRecording', self.checkCallState())
        else:
            waitTime = 0
            while self.checkCallState() != 2:
                time.sleep(self.WAIT_SEC)
                waitTime = waitTime + self.WAIT_SEC
                printEx( "%s:%s" % ("waitTime", waitTime))
                if waitTime > self.WAITDEADLINE_SEC:
                    printEx( "%s:%s" % ("Dialing", "Fail"))
                    reVal = None
                    break

        if reVal:
            waitTime = 0
            while waitTime < self.RECORDING_SEC:
                time.sleep(self.SMALL_SEC)
                waitTime = waitTime + self.SMALL_SEC
                printEx( "%s(%s sec)" % ("RECORDING", waitTime))
        else:
            pass

        printEx( "%s:%s" % ("endPhone", self.endPhone()))
        return reVal


    def moveRecordFileToLocal(self, ongoingNumber):
        reVal = None
        time.sleep(self.WAIT_SEC)
        waitTime = 0
        while True:
            word = RECORDFILE_PREFIXLIST.get(self.PACKAGENAME).replace('%PHONENUMBER%', ongoingNumber)
            audioFileNameInDevice, audioFullFileNameInDevice = selectLatestInAndroid(self.DEVICE_ID,
                                                                                     self.DEVICE_RECORDFOLDER,
                                                                                     word)
            if audioFileNameInDevice != None:
                break
            time.sleep(self.WAIT_SEC)
            waitTime = waitTime + self.WAIT_SEC
            printEx( "%s:%s" % ("waitTime", waitTime))
            if waitTime > self.WAITDEADLINE_SEC:
                printEx( "%s:%s" % ("FindRecordFile", "Fail"))
                break


        printEx( "%s(%s)" % ("audioFileNameInDevice", audioFileNameInDevice))
        try:
            if audioFileNameInDevice != None:
                proc = subprocess.Popen("adb -s " + self.DEVICE_ID + " pull " + audioFullFileNameInDevice, stdout=subprocess.PIPE,
                                        shell=True)
                self.pids.append(proc.pid)
                time.sleep(self.WAIT_SEC)

                proc = subprocess.Popen("adb -s " + self.DEVICE_ID + " shell rm -f " + audioFullFileNameInDevice,
                                        stdout=subprocess.PIPE,
                                        shell=True)
                self.pids.append(proc.pid)
                time.sleep(self.WAIT_SEC)

                if os.path.isfile(audioFileNameInDevice):
                    reVal = audioFileNameInDevice
        except:
            printError("%s:%s" % ("Unexpected error in " + self.MODEL, getExceptionString(sys.exc_info())))

        return reVal

    def analyzeAudioFile(self, audioName):
        reVal = None
        wavfileName = None
        # recognize speech using Google Speech Recognition
        if audioName != None:
            if os.path.isfile(audioName + ".wav"):
                os.remove(audioName + ".wav")
            wavfileName = self.covertAudioFile(audioName, "wav")

        if wavfileName != None:
            # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "test.wav")
            # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "SPY3_07.mp3") --> not supported
            AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), wavfileName)
            # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
            # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

            # use the audio file as the audio source
            r = sr.Recognizer()
            audio = None
            with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)  # read the entire audio file
            errorStr = None
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                printEx( "%s(%s)" % ("status", "Before r.recognize_google"))
                self.resultS['ALGORITHM'] = 'Google Speech Recognition'
                reVal = r.recognize_google(audio, language="ko-KR", show_all = False)
                printEx( "%s(%s)" % ("reVal", reVal))
                printEx(("Google Speech Recognition thinks you said: " + reVal))
                printEx( "%s(%s)" % ("status", "After r.recognize_google"))
            except sr.UnknownValueError:
                printEx(("Google Speech Recognition could not understand audio"))
                errorStr = getExceptionString(sys.exc_info())
            except sr.RequestError as e:
                printEx(("Could not request results from Google Speech Recognition service; {0}".format(e)))
                errorStr = getExceptionString(sys.exc_info())
            except ValueError:
                print "ValueError"
                errorStr = getExceptionString(sys.exc_info())
            finally:
                pass
        if reVal == None:
            self.resultS['analyzeFNum'] = self.resultS.get('analyzeFNum') + 1
            time.sleep(self.WAIT_SEC * 10)
            raise Exception('analyzeAudioFile', errorStr)

        return reVal

    def cleanRecordingFileinDevice(self):
        reVal = 0
        while True:
            word = RECORDFILE_PREFIXLIST.get(self.PACKAGENAME).replace('%PHONENUMBER%', '')
            audioFileNameInDevice, audioFullFileNameInDevice = selectLatestInAndroid(self.DEVICE_ID, self.DEVICE_RECORDFOLDER, word)
            if audioFileNameInDevice != None:
                proc = subprocess.Popen("adb -s " + self.DEVICE_ID + " shell rm -f " + audioFullFileNameInDevice, stdout=subprocess.PIPE,
                                        shell=True)
                self.pids.append(proc.pid)
                reVal = reVal + 1
            else:
                break

        return reVal

    def resetEnv(self):
        reVal = True
        try:
            sPids = []
            proc = subprocess.Popen('tasklist /svc', stdout=subprocess.PIPE)
            fd_popen = proc.stdout
            content = fd_popen.read().strip()
            for line in content.split('\r\n'):
                if str(filter(str.isdigit, line)) != '':
                    sPids.append(filter(str.isdigit, line))

            for pid in self.pids:
                if pid in sPids:
                    os_systemEx("taskkill /F /PID " + str(pid))
                    printEx( "taskkill /F /PID " + str(pid))
            self.pids = []

            printEx( "%s:%s" % ("endPhone", self.endPhone()))
            printEx( "%s:%s" % ("cleanRecordingFileinDevice", self.cleanRecordingFileinDevice()))
        except:
            printError("%s:%s" % ("Unexpected error in " + self.MODEL, getExceptionString(sys.exc_info())))
            reVal = False
        finally:
            pass

        return reVal

    def run(self):
        printEx( self.availableIncomingRecording())
        print "-----------------------------"

        def printNumResult():
            difference_in_seconds = abs(mktime(endDatetime.timetuple()) - mktime((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).timetuple()))
            difference_in_minutes = round(difference_in_seconds / 60, 2)
            print "==" + self.MODEL + ">>" + ( "%s:%s" % ("START_TIME", self.START_TIME)) + "==="
            print "%s(%s)" % ("outcallSNum", str(outcallSNum)),
            print "%s(%s)" % ("incallSNum", str(incallSNum))
            print "%s(%s)" % ("outcallFNum", str(outcallFNum)),
            print "%s(%s)" % ("incallFNum", str(incallFNum))
            print "%s(%s)" % ("notFoundONum", str(notFoundONum)),
            print "%s(%s)" % ("notFoundINum", str(notFoundINum))
            print "--------------------------------------"
            print "%s(%s)" % ("trycount", str(trycount)),
            print "%s(%s)" % ("analyzeNum", str(analyzeNum))
            print "%s(%s)" % ("perfectSNum", str(perfectSNum)),
            print "%s(%s)" % ("perfectFNum", str(perfectFNum))
            print "%s(%s)" % ("perfectISNum", str(perfectISNum)),
            print "%s(%s)" % ("perfectIFNum", str(perfectIFNum))
            print "%s(%s)" % ("hangulSNum", str(hangulSNum)),
            print "%s(%s)" % ("hangulFNum", str(hangulFNum))
            print "%s(%s)" % ("settingFailNum", str(settingFailNum)),
            print "%s(%s)" % ("exceptNum", str(exceptNum))
            print "--------------------------------------"
            if trycount > 0 and (outcallSNum + outcallFNum) > 0 and (incallSNum + incallFNum) > 0 and analyzeNum > 0:
                print "--------------------------------------"
                print "%s(%s)" % ("outSuccess__rate", str(round(float(perfectSNum - perfectISNum) / float(outcallSNum + outcallFNum), 5)))
                print "%s(%s)" % ("inSuccess__rate", str(round(float(perfectISNum) / float(incallSNum + incallFNum), 5)))
                print "%s(%s)" % ("success__rate", str(round(float(perfectSNum) / float(outcallSNum + outcallFNum + incallSNum + incallFNum), 5)))
            print ">> " + self.MODEL + " >> " + "remainMinutes: " + str(difference_in_minutes) + "<<<<<<<<<"
            print ""

        ANSWERSHEET = {
            '1508':[u'음성통화', u'안녕', u'니다'],#안녕하세요 hd 보이스 고품질 음성통화에 연결 되었습니다
            '114':[u'텔레콤', u'한국', u'환영', u'니다'],#한국서비스품질지수 8년 연속 일이 SK 텔레콤입니다 파티시엘 쓰는 일반
            self.MYNUM:[u'비밀번호', u'서비스', u'눌러', u'니다'],#소리샘 서비스입니다 비밀번호를 눌러주세요 눌러야 할 시간이 지났습니다
            '0112008585':[u'모닝콜', u'지금', u'니다'],#안녕하세요 SK 텔레콤 모닝콜 서비스입니다 지금은 18시 40분입니다
        }

        START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
        endDatetime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9, minutes=self.during_mins))
        EXPECT_END_TIME = endDatetime.strftime("%Y%m%d%H%M")


        trycount=0
        notFoundINum = 0
        notFoundONum = 0
        settingFailNum = 0
        exceptNum = 0
        outcallSNum = 0
        outcallFNum = 0
        incallSNum = 0
        incallFNum = 0
        perfectISNum = 0
        perfectIFNum = 0
        perfectSNum = 0
        perfectFNum = 0
        analyzeNum = 0
        self.resultS['analyzeFNum'] = 0
        hangulSNum = 0
        hangulFNum = 0
        #ongoingNumber = self.requestIncomingRecording()
        #exit(0)

        #self.resultS['error'] = None
        self.resultS['START_BATTERY'] = getBatteryLevel(self.DEVICE_ID)

        while self.DIALPAD_KEY != None and long(EXPECT_END_TIME) > long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")) :
            trycount = trycount + 1
            audioName = None
            ongoingNumber = None
            incoming = False
            success = False
            failLogS = dict()
            CURRENTGMT9TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
            failLogS['CURRENTGMT9TIME'] = CURRENTGMT9TIME
            printEx( "EXPECT_END_TIME: " + EXPECT_END_TIME)
            printEx( "CURRENTGMT9TIME: " + CURRENTGMT9TIME)

            if self.resultS.has_key('error') == False and self.DEVICE_ID not in getRealDevices():
                self.resultS['error'] = "adb is disconnected"

            if self.resultS.has_key('error') == False and getBatteryLevel(self.DEVICE_ID) < 5 and getBatteryLevel(self.DEVICE_ID) >= 0:
                self.resultS['error'] = ("battery status is under %s" % (getBatteryLevel(self.DEVICE_ID)))

            if self.resultS.has_key('error'):
                sendMessage('01064440681', self.MYNUM, ("%s 모델의 %s 분 통화녹음 테스트 중단:%s" % (self.MODEL, str(self.during_mins), self.resultS['error'])))
                break

            printEx( "%s:%s" % ("resetEnv", self.resetEnv()))

            try:
                if self.LOCALTEST == False:
                    incoming = self.isItNowIncomingSettingTime()
                    printEx( "%s:%s" % ("isItNowIncomingSettingTime", incoming))
                    if self.MONKEY:
                        if incoming:
                            while True:
                                pid = getPidInDevice(self.DEVICE_ID, 'com.android.commands.monkey')
                                printEx("%s:%s" % ("pid", pid))
                                if pid > 0:
                                    printEx("%s:%s" % ("killProcessInDevice", killProcessInDevice(self.DEVICE_ID, pid)))
                                else:
                                    break
                        else:
                            printEx("%s:%s" % ("runMonkeyInDevice", runMonkeyInDevice(self.DEVICE_ID, None)))
                    else:
                        while True:
                            pid = getPidInDevice(self.DEVICE_ID, 'com.android.commands.monkey')
                            printEx("%s:%s" % ("pid", pid))
                            if pid > 0:
                                printEx("%s:%s" % ("killProcessInDevice", killProcessInDevice(self.DEVICE_ID, pid)))
                            else:
                                break

                        repeatCount = 3
                        if incoming:
                            repeatCount = 1

                        for funcs in self.DEMANDS.keys():
                            argument = self.DEMANDS[funcs]
                            expression = "%s('%s', '%s', '%s')" % (funcs, self.DEVICE_ID, argument, repeatCount)
                            result = eval(expression)
                            printEx("%s:%s" % (expression, result))

                    if incoming:
                        ongoingNumber = self.requestIncomingRecording()
                        printEx( "%s:%s" % ("requestIncomingRecording", ongoingNumber))
                        if ongoingNumber != None:
                            incallSNum = incallSNum + 1
                        else:
                            incallFNum = incallFNum + 1
                    else:
                        ongoingNumber = self.requestOutcomingRecording(self.MYNUM)
                        printEx( "%s:%s" % ("requestOutcomingRecording", ongoingNumber))
                        if ongoingNumber != None:
                            outcallSNum = outcallSNum + 1
                        else:
                            outcallFNum = outcallFNum + 1

                    if ongoingNumber != None:
                        audioName = self.moveRecordFileToLocal(ongoingNumber)
                        printEx( "%s:%s" % ("moveRecordFileToLocal", audioName))
                        if audioName == None:
                            if incoming:
                                notFoundINum = notFoundINum + 1
                            else:
                                notFoundONum = notFoundONum + 1
                    else:
                        pass

                    if trycount > 10 and trycount == (outcallFNum + incallFNum):
                        self.resultS['error'] = ("adb-calling is out of control(%s)" % ( "%s:%s" % ("trycount", trycount)))
                        raise Exception('adb-calling is out of control', ( "%s:%s" % ("trycount", trycount)))

                else:
                    audioName = "114_1473301954286.wav"
                    ongoingNumber = '114'

                failLogS['ongoingNumber'] = ongoingNumber
                failLogS['audioName'] = audioName
                failLogS['incoming'] = incoming
                if audioName != None:
                    recordingContext = self.analyzeAudioFile(audioName)
                    printEx( "%s:%s" % ("analyzeAudioFile", recordingContext))
                    printEx( "%s:%s" % ("type(recordingContext)", type(recordingContext)))
                    if recordingContext != None:
                        analyzeNum = analyzeNum + 1
                        result = re.findall(u'[\uAC00-\uD7A3]+', recordingContext)
                        recordingContext_Hangul = ''.join(result)
                        printEx( "%s:%s" % ("recordingContext_Hangul", recordingContext_Hangul))
                        printEx( "%s:%s" % ("type(recordingContext_Hangul)", type(recordingContext_Hangul)))
                        if len(recordingContext_Hangul) > 0:
                            hangulSNum = hangulSNum + 1
                        else:
                            hangulFNum = hangulFNum + 1
                        ANSWERSHEET_HangulList = ''
                        for answerWords in ANSWERSHEET[ongoingNumber]:
                            result = re.findall(u'[\uAC00-\uD7A3]+', answerWords)
                            ANSWERSHEET_Hangul = ''.join(result)
                            if len(ANSWERSHEET_HangulList) == 0:
                                ANSWERSHEET_HangulList = ANSWERSHEET_Hangul
                            else:
                                ANSWERSHEET_HangulList = ANSWERSHEET_HangulList + ',' + ANSWERSHEET_Hangul
                            printEx( "%s:%s" % ("ANSWERSHEET_Hangul", ANSWERSHEET_Hangul))
                            printEx( "%s:%s" % ("type(ANSWERSHEET_Hangul)", type(ANSWERSHEET_Hangul)))

                            if len(ANSWERSHEET_Hangul) > 0 and ANSWERSHEET_Hangul in recordingContext_Hangul:
                                success = True
                                perfectSNum = perfectSNum + 1
                                if incoming:
                                    perfectISNum = perfectISNum + 1
                                break
                        if success == False:
                            perfectFNum = perfectFNum + 1
                            if incoming:
                                perfectIFNum = perfectIFNum + 1

                            failLogS['recordingContext_Hangul'] = recordingContext_Hangul
                            failLogS['ANSWERSHEET_HangulList'] = ANSWERSHEET_HangulList
                else:
                    printEx( "%s(%s)" % ("audioName", audioName))
            except KeyboardInterrupt:
                printEx( "KeyboardInterrupt in Thread!")
                raise KeyboardInterrupt
            except:
                printError("%s:%s" % ("Unexpected error in " + self.MODEL,  getExceptionString(sys.exc_info())))
                #self.resultS['sys.exc_info()[0]'] = sys.exc_info()[0]
                #self.resultS['sys.exc_info()[1]'] = sys.exc_info()[1]
                if sys.exc_info()[0] == 'setMorningCall' and sys.exc_info()[1] == 'fail':
                    settingFailNum = settingFailNum + 1
                else:
                    exceptNum = exceptNum + 1

                failLogS['error'] = getExceptionString(sys.exc_info())
                #sendMessage('01064440681', self.MYNUM, ("%s 모델의 %s 분 통화녹음 테스트 도중 에러 발생:%s" % (self.MODEL, str(self.during_mins), getExceptionString(sys.exc_info()))))
                #time.sleep(self.WAIT_SEC * 3)
            finally:
                printEx( "%s(%s)" % ("success", str(success)))
                if len(failLogS) > 0 and success == False:
                    mkdirs(self.LMCFT_FOLDER_FAIL)
                    if audioName != None:
                        if os.path.isfile(audioName + ".wav"):
                            shutil.move(audioName + ".wav",
                                        self.LMCFT_FOLDER_FAIL + audioName + ".wav")
                        if self.LOCALTEST == False:
                            if os.path.isfile(audioName):
                                shutil.move(audioName,
                                            self.LMCFT_FOLDER_FAIL + audioName)

                    mkdirs(self.failListFileName)
                    with codecs.open(self.failListFileName, 'a', 'utf-8') as f:
                        f.write(json.dumps(failLogS, ensure_ascii=False) + "\r\n")
                        f.close()

                printNumResult()
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                print( "%s(%s)" % ("current success", str(success)))
                print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                self.resultS['modified_time'] = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
                self.resultS['trycount'] = trycount
                self.resultS['notFoundINum'] = notFoundINum
                self.resultS['notFoundONum'] = notFoundONum
                self.resultS['exceptNum'] = exceptNum
                self.resultS['settingFailNum'] = settingFailNum

                self.resultS['outcallSNum'] = outcallSNum
                self.resultS['outcallFNum'] = outcallFNum
                self.resultS['incallSNum'] = incallSNum
                self.resultS['incallFNum'] = incallFNum

                self.resultS['perfectISNum'] = perfectISNum
                self.resultS['perfectIFNum'] = perfectIFNum
                self.resultS['perfectSNum'] = perfectSNum
                self.resultS['perfectFNum'] = perfectFNum
                self.resultS['analyzeNum'] = analyzeNum
                self.resultS['hangulSNum'] = hangulSNum
                self.resultS['hangulFNum'] = hangulFNum

                try:
                    self.resultS['outSuccess__rate'] = round(float(perfectSNum-perfectISNum)/float(outcallSNum+outcallFNum),5)
                except:
                    self.resultS['outSuccess__rate'] = 0
                try:
                    self.resultS['inSuccess__rate'] = round(float(perfectISNum)/float(incallSNum+incallFNum),5)
                except:
                    self.resultS['inSuccess__rate'] = 0
                try:
                    self.resultS['success__rate'] = round(float(perfectSNum)/float(outcallSNum + outcallFNum + incallSNum + incallFNum),5)
                except:
                    self.resultS['success__rate'] = 0

                if audioName != None:
                    if os.path.isfile(audioName + ".wav"):
                        os.remove(audioName + ".wav")

                    if self.LOCALTEST == False:
                        if os.path.isfile(audioName):
                            os.remove(audioName)

        if self.MONKEY:
            while True:
                pid = getPidInDevice(self.DEVICE_ID, 'com.android.commands.monkey')
                printEx("%s:%s" % ("pid", pid))
                if pid > 0:
                    printEx("%s:%s" % ("killProcessInDevice", killProcessInDevice(self.DEVICE_ID, pid)))
                else:
                    break

        self.resultS['END_BATTERY'] = getBatteryLevel(self.DEVICE_ID)
        if self.LOGPROCESS != None:
            try:
                self.LOGPROCESS.kill()
            except:
                printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))
            self.resultS['LOGINFO'] = self.LOGINFO.getAllInfo()
            print self.resultS['LOGINFO']

        mkdirs(self.resultFileName)
        printEx("%s:%s" % ("self.resultS", self.resultS))
        with open(self.resultFileName, 'a') as f:
           #f.write(json.dumps(self.resultS) + "\r\n")
           f.write(json.dumps(self.resultS) + "\n")
           f.close()

        if self.DIALPAD_KEY != None and long(EXPECT_END_TIME) > long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")):
            sendMessage('01064440681', self.MYNUM, ("%s 모델의 %s 분 통화녹음테스트를 예기치 않은 문제가 생겨 종료되었습니다." % (self.MODEL, str(self.during_mins))))
        else:
            sendMessage('01064440681', self.MYNUM, ("%s모델의%s분통화녹음테스트를정상적으로종료." % (self.MODEL, str(self.during_mins))))