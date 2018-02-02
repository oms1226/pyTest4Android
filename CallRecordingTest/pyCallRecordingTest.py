# -*- coding: utf-8 -*-
import codecs
import json
import random

import re
import socket

import datetime
import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path
from sys import platform as _platform
import os

import subprocess

import time
from time import gmtime, strftime, localtime
import sys

import cv2

resultS = dict()

DEVICE_ID = "ce06171633773534027e"
#DEVICE_ID = "5210b498f4ec344f"
#DEVICE_ID = "ce0916097c6ab53502"

MYNUM = '01021486330'
resultS['MYNUM'] = MYNUM
RECORDING_SEC = 25
resultS['RECORDING_SEC'] = RECORDING_SEC
WAIT_SEC = 5
resultS['WAIT_SEC'] = WAIT_SEC
SMALL_SEC = 1
resultS['SMALL_SEC'] = SMALL_SEC
pids = []
LOCALTEST = False
resultS['LOCALTEST'] = LOCALTEST
DEVICE_RECORDFOLDER = '/sdcard/.TPhoneCallRecords/.nomedia/'
resultS['DEVICE_RECORDFOLDER'] = DEVICE_RECORDFOLDER
TARGET_APP = 'com.skt.prod.dialer'
resultS['TARGET_APP'] = TARGET_APP


myName = sys.argv[0].split('/')[-1]
print "%s:%s" % ("myName", myName)
resultS['ID_FILENAME'] = myName

hostname = socket.gethostname()
resultS['hostname'] = hostname
START_TIME = strftime("%Y%m%d%H%M%S", localtime())
resultS['START_TIME'] = START_TIME

if len(sys.argv) > 1:
    during_hours = int(sys.argv[1])
else:
    during_hours = 1
resultS['during_hours'] = during_hours

LOG_COVERAGE='narrow'
if len(sys.argv) > 2:
   #ex.
   #narrow(default)
   #full
   #입력 값 그대로
   LOG_COVERAGE = sys.argv[2]
resultS['LOG_COVERAGE'] = LOG_COVERAGE

failListFileName = "FailList" + "_" + TARGET_APP + "_" + hostname  + "_" + START_TIME + "_" + str(during_hours) + ".log"
resultFileName = "Result" + "_" + myName.split('.')[0] + "_" + TARGET_APP + "_" + hostname  + ".log"

def selectLatestInAndroid(deviceId, path, prefix):
   global pids
   fileName = None
   fullfileName = None
   proc = subprocess.Popen("adb -s " + deviceId + " shell ls -t " + path, stdout=subprocess.PIPE)
   fd_popen = proc.stdout
   pids.append(proc.pid)

   fileList = fd_popen.read().strip()
   for file in fileList.split('\r\n'):
     if prefix in file:
         fileName = file
         fullfileName = path + file
         print "%s(%s)" % ("fullfileName", fullfileName)
         break
   return fileName, fullfileName

"""
0 = indicates idle,
1 = ringing and
2 = active call
"""
def checkCallState(deviceId):
    global pids
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell dumpsys telephony.registry", stdout=subprocess.PIPE)
    fd_popen = proc.stdout
    pids.append(proc.pid)

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        if 'mCallState' in line:
            reVal = line.strip()
            break

    print "checkCallState(%s) --> (%s)" % (deviceId, reVal.split('=')[1])
    return int(reVal.split('=')[1])

def callPhone(deviceId, phonenumber):
    global pids
    reVal = True
    waitTime = 0
    try:
        if checkCallState(DEVICE_ID) != 0:
            raise Exception('callPhone', checkCallState(DEVICE_ID))

        while checkCallState(DEVICE_ID) == 0:
            proc = subprocess.Popen(
                "adb -s " + deviceId + " shell am start -a android.intent.action.CALL tel:" + phonenumber,
                stdout=subprocess.PIPE)
            pids.append(proc.pid)
            time.sleep(WAIT_SEC)
            waitTime = waitTime + WAIT_SEC
            print "%s:%s" % ("waitTime", waitTime)
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        reVal = False

    return reVal;

def acceptPhone(deviceId):
    global pids
    reVal = True
    waitTime = 0
    try:
        if checkCallState(DEVICE_ID) != 1:
            raise Exception('acceptPhone', checkCallState(DEVICE_ID))

        while checkCallState(DEVICE_ID) == 1:
            proc = subprocess.Popen("adb -s " + deviceId + " shell input keyevent KEYCODE_CALL",
                                    stdout=subprocess.PIPE)
            pids.append(proc.pid)
            time.sleep(WAIT_SEC)
            waitTime = waitTime + WAIT_SEC
            print "%s:%s" % ("waitTime", waitTime)
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        reVal = False

    return reVal;



def endPhone(deviceId):
    global pids
    reVal = True
    waitTime = 0
    try:
        if checkCallState(DEVICE_ID) == 0:
            raise Exception('endPhone', checkCallState(DEVICE_ID))

        while checkCallState(DEVICE_ID) != 0:
            proc = subprocess.Popen("adb -s " + deviceId + " shell input keyevent KEYCODE_ENDCALL", stdout=subprocess.PIPE)
            pids.append(proc.pid)
            time.sleep(WAIT_SEC)
            waitTime = waitTime + WAIT_SEC
            print "%s:%s" % ("waitTime", waitTime)
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        reVal = False

    return reVal;


def covertAudioFile(fileName, fileType):
    reVal = fileName + "." + fileType
    if _platform == "linux" or _platform == "linux2":
        os.system("ffmpeg -i " + fileName + " " + reVal)
    else:
        os.system("ffmpeg.exe -i " + fileName + " " + reVal)

    if os.path.isfile(reVal) == False:
        reVal = None

    return reVal


def getDateInDevice(deviceId):
    reVal = None
    proc = subprocess.Popen("adb -s " + deviceId + " shell date +%H%M", stdout=subprocess.PIPE)
    fd_popen = proc.stdout
    pids.append(proc.pid)

    content = fd_popen.read().strip()
    for line in content.split('\r\n'):
        reVal = list(line)
    print "%s:%s" % ("date +%H%M", str(reVal))
    return reVal

def availableIncomingRecording(deviceId):
    reVal = False
    dateHM = getDateInDevice(deviceId)

    limitation = WAIT_SEC
    while (limitation >= 10):
        limitation = limitation / 2
    limitation = 10 - limitation

    if limitation > int(dateHM[3]):
        reVal = True

    return reVal

def isItNowIncomingSettingTime(deviceId):
    reVal = False
    dateHM = getDateInDevice(deviceId)

    if 7 == int(dateHM[3]):
        reVal = True

    return reVal


def getSetDateInDevice(deviceId):
    reVal = None
    reVal = getDateInDevice(deviceId)
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

def getLocationOnDialPad(number):
    dialpad = {'1':(200,1100), '2':(500,1100), '3':(800,1100),
    '4':(200,1250), '5':(500,1250), '6':(800,1250),
    '7':(200,1400), '8':(500,1400), '9':(800,1400),
    '*':(200,1550), '0':(500,1550), '#':(800,1550),
    'keypad': (700, 1750),
    }
    return "%s %s" % (str(dialpad[number][0]), str(dialpad[number][1]))

def tapOnDevice(deviceId, location):
    proc = subprocess.Popen("adb -s " + deviceId + " shell input tap " + location,
                            stdout=subprocess.PIPE)
    pids.append(proc.pid)

def setMorningCall(deviceId, phoneNum):
    reVal = None
    try:
        if checkCallState(deviceId) != 0:
            raise Exception('setMorningCall', checkCallState(deviceId))

        while checkCallState(deviceId) == 0:
            callPhone(deviceId, phoneNum)
            time.sleep(SMALL_SEC)

        tapOnDevice(deviceId, getLocationOnDialPad('keypad'))
        time.sleep(WAIT_SEC)

        tapOnDevice(deviceId, getLocationOnDialPad('0'))
        time.sleep(SMALL_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('9'))
        time.sleep(SMALL_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('1'))
        time.sleep(SMALL_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('8'))
        time.sleep(WAIT_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('3'))
        time.sleep(WAIT_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('2'))
        time.sleep(WAIT_SEC)
        time.sleep(WAIT_SEC)
        reVal = getSetDateInDevice(deviceId)
        for num in reVal:
            print "%s:%s" % ("num", num)
            tapOnDevice(deviceId, getLocationOnDialPad(num))
            time.sleep(SMALL_SEC)
        time.sleep(WAIT_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('0'))
        time.sleep(SMALL_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('1'))
        time.sleep(WAIT_SEC)
        time.sleep(WAIT_SEC)
        print "%s:%s" % ("endPhone", endPhone(deviceId))
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        reVal = None
    return reVal


def unSetMorningCall(deviceId, phoneNum):
    reVal = True
    try:
        if checkCallState(deviceId) != 0:
            raise Exception('setMorningCall', checkCallState(deviceId))

        while checkCallState(deviceId) == 0:
            callPhone(deviceId, phoneNum)
            time.sleep(SMALL_SEC)

        tapOnDevice(deviceId, getLocationOnDialPad('keypad'))
        time.sleep(WAIT_SEC)

        tapOnDevice(deviceId, getLocationOnDialPad('0'))
        time.sleep(SMALL_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('9'))
        time.sleep(SMALL_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('1'))
        time.sleep(SMALL_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('8'))
        time.sleep(WAIT_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('3'))
        time.sleep(WAIT_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('2'))
        time.sleep(WAIT_SEC)
        time.sleep(WAIT_SEC)
        tapOnDevice(deviceId, getLocationOnDialPad('1'))
        time.sleep(WAIT_SEC)
        time.sleep(WAIT_SEC)
        print "%s:%s" % ("endPhone", endPhone(deviceId))
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        reVal = False
    return reVal

def compareDate(deviceId, dateHM):
    reVal = None
    try:
        cDateHM = getDateInDevice(deviceId)
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
                reVal = -1
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        reVal = 1

    return reVal

def requestIncomingRecording(deviceId, num):
    reVal = '0112008585'
    time4MonrningCall = setMorningCall(DEVICE_ID, num)
    print "%s:%s" % ("setMorningCall", time4MonrningCall)
    print "%s:%s" % ("cleanRecordingFileinDevice", cleanRecordingFileinDevice(DEVICE_ID))

    waitTime = 0
    while checkCallState(DEVICE_ID) != 1:
        compareIndex = compareDate(DEVICE_ID, time4MonrningCall)
        print "%s:%s" % ("compareDate", compareIndex)
        if compareIndex > 0 or checkCallState(DEVICE_ID) == 2:
            print "%s:%s" % ("MorningCall", "Fail")
            reVal = None
            break
        time.sleep(WAIT_SEC)
        waitTime = waitTime + WAIT_SEC
        print "%s:%s" % ("waitTime", waitTime)

    if reVal != None:
        print "%s:%s" % ("acceptPhone", acceptPhone(DEVICE_ID))
        waitTime = 0
        while waitTime < RECORDING_SEC:
            time.sleep(SMALL_SEC)
            waitTime = waitTime + SMALL_SEC
            print "%s(%s sec)" % ("RECORDING", waitTime)
        print "%s:%s" % ("endPhone", endPhone(DEVICE_ID))
    else:
        print "%s:%s" % ("unSetMorningCall", unSetMorningCall(DEVICE_ID, num))

    return reVal


def requestOutcomingRecording(deviceId, num):
    phonenumbers = ['114', '1508']
    phonenumbers.append(num)
    reVal = phonenumbers[random.randrange(0, len(phonenumbers))]
    print "%s(%s)" % ("reVal", reVal)
    print "%s:%s" % ("callPhone", callPhone(DEVICE_ID, reVal))

    waitTime = 0
    while checkCallState(DEVICE_ID) != 2:
        if waitTime > 20:
            print "%s:%s" % ("Dialing", "Fail")
            reVal = None
            break
        time.sleep(WAIT_SEC)
        waitTime = waitTime + WAIT_SEC
        print "%s:%s" % ("waitTime", waitTime)

    if reVal:
        waitTime = 0
        while waitTime < RECORDING_SEC:
            time.sleep(SMALL_SEC)
            waitTime = waitTime + SMALL_SEC
            print "%s(%s sec)" % ("RECORDING", waitTime)
    else:
        pass

    print "%s:%s" % ("endPhone", endPhone(DEVICE_ID))
    return reVal


def moveRecordFileToLocal(deviceId, ongoingNumber):
    reVal = None
    audioFileNameInDevice, audioFullFileNameInDevice = selectLatestInAndroid(deviceId,
                                                                             DEVICE_RECORDFOLDER,
                                                                             'CallRec_' + ongoingNumber)
    print "%s(%s)" % ("audioFileNameInDevice", audioFileNameInDevice)
    if audioFileNameInDevice != None:
        proc = subprocess.Popen("adb -s " + deviceId + " pull " + audioFullFileNameInDevice, stdout=subprocess.PIPE,
                                shell=True)
        pids.append(proc.pid)
        time.sleep(WAIT_SEC)

        proc = subprocess.Popen("adb -s " + deviceId + " shell rm -f " + audioFullFileNameInDevice,
                                stdout=subprocess.PIPE,
                                shell=True)
        pids.append(proc.pid)
        time.sleep(WAIT_SEC)

        if os.path.isfile(audioFileNameInDevice):
            reVal = audioFileNameInDevice

    return reVal

def analyzeAudioFile(DEVICE_ID, audioName):
    reVal = None
    wavfileName = None
    # recognize speech using Google Speech Recognition
    if audioName != None:
        if os.path.isfile(audioName + ".wav"):
            os.remove(audioName + ".wav")
        wavfileName = covertAudioFile(audioName, "wav")

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

        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print "%s(%s)" % ("status", "Before r.recognize_google")
            reVal = r.recognize_google(audio, language="ko-KR")
            print("Google Speech Recognition thinks you said: " + reVal)
            print "%s(%s)" % ("status", "After r.recognize_google")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except ValueError:
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        finally:
            pass
    return reVal

def cleanRecordingFileinDevice(deviceId):
    reVal = 0
    while True:
        audioFileNameInDevice, audioFullFileNameInDevice = selectLatestInAndroid(DEVICE_ID, DEVICE_RECORDFOLDER, 'CallRec_')
        if audioFileNameInDevice != None:
            proc = subprocess.Popen("adb -s " + DEVICE_ID + " shell rm -f " + audioFullFileNameInDevice, stdout=subprocess.PIPE,
                                    shell=True)
            pids.append(proc.pid)
            reVal = reVal + 1
        else:
            break

    return reVal

def resetEnv(deviceId):
    global pids
    reVal = True
    try:
       for pid in pids:
          os.system("taskkill /F /PID " + str(pid))
          print "taskkill /F /PID " + str(pid)
       pids = []
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        reVal = False
    finally:
        pass

    return reVal


print availableIncomingRecording(DEVICE_ID)
print "-----------------------------"

if LOCALTEST == False:
    print "%s:%s" % ("endPhone", endPhone(DEVICE_ID))
    print "%s:%s" % ("cleanRecordingFileinDevice", cleanRecordingFileinDevice(DEVICE_ID))

def printNumResult():
    print "======================================"
    print "%s(%s)" % ("outcallSNum", str(outcallSNum))
    print "%s(%s)" % ("outcallFNum", str(outcallFNum))
    print "%s(%s)" % ("incallSNum", str(incallSNum))
    print "%s(%s)" % ("incallFNum", str(incallFNum))
    print "%s(%s)" % ("recordISNum", str(recordISNum))
    print "%s(%s)" % ("recordIFNum", str(recordIFNum))
    print "--------------------------------------"
    print "%s(%s)" % ("trycount", str(trycount))
    print "%s(%s)" % ("notFoundNum", str(notFoundNum))
    print "%s(%s)" % ("analyzeNum", str(analyzeNum))
    print "%s(%s)" % ("recordSNum", str(recordSNum))
    print "%s(%s)" % ("recordFNum", str(recordFNum))
    if trycount > 0 and (outcallSNum + outcallFNum) > 0 and (incallSNum + incallFNum) > 0 :
        print "--------------------------------------"
        print "%s(%s)" % ("outSuccess__rate", str(round(float(recordSNum - recordISNum) / float(outcallSNum + outcallFNum), 5)))
        print "%s(%s)" % ("inSuccess__rate", str(round(float(recordISNum) / float(incallSNum + incallFNum), 5)))
        print "%s(%s)" % ("success__rate", str(round(float(recordSNum) / float(analyzeNum), 5)))
    print "======================================"

ANSWERSHEET = {
    '1508':u'음성통화',#안녕하세요 hd 보이스 고품질 음성통화에 연결 되었습니다
    '114':u'텔레콤',#한국서비스품질지수 8년 연속 일이 SK 텔레콤입니다 파티시엘 쓰는 일반
    MYNUM:u'비밀번호',#소리샘 서비스입니다 비밀번호를 눌러주세요 눌러야 할 시간이 지났습니다
    '0112008585':u'모닝콜',#안녕하세요 SK 텔레콤 모닝콜 서비스입니다 지금은 18시 40분입니다
}

START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
EXPECT_END_TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=(during_hours+9))).strftime("%Y%m%d%H%M")

trycount=0
notFoundNum = 0
outcallSNum = 0
outcallFNum = 0
incallSNum = 0
incallFNum = 0
recordISNum = 0
recordIFNum = 0
recordSNum = 0
recordFNum = 0
analyzeNum = 0

while long(EXPECT_END_TIME) > long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")) :
    trycount = trycount + 1
    audioName = None
    ongoingNumber = None
    incoming = False
    success = False
    failLogS = dict()
    resultS['sys.exc_info()[0]'] = None
    resultS['sys.exc_info()[1]'] = None
    CURRENTGMT9TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    failLogS['CURRENTGMT9TIME'] = CURRENTGMT9TIME
    print "EXPECT_END_TIME: " + EXPECT_END_TIME
    print "CURRENTGMT9TIME: " + CURRENTGMT9TIME

    print "%s:%s" % ("resetEnv", resetEnv(DEVICE_ID))

    try:
        if LOCALTEST == False:
            incoming = isItNowIncomingSettingTime(DEVICE_ID)
            print "%s:%s" % ("isItNowIncomingSettingTime", incoming)
            if incoming:
                ongoingNumber = requestIncomingRecording(DEVICE_ID, MYNUM)
                print "%s:%s" % ("requestIncomingRecording", ongoingNumber)
                if ongoingNumber != None:
                    incallSNum = incallSNum + 1
                else:
                    incallFNum = incallFNum + 1
            else:
                ongoingNumber = requestOutcomingRecording(DEVICE_ID, MYNUM)
                print "%s:%s" % ("requestOutcomingRecording", ongoingNumber)
                if ongoingNumber != None:
                    outcallSNum = outcallSNum + 1
                else:
                    outcallFNum = outcallFNum + 1

            if ongoingNumber != None:
                audioName = moveRecordFileToLocal(DEVICE_ID, ongoingNumber)
                print "%s:%s" % ("moveRecordFileToLocal", audioName)
            else:
                pass

        else:
            audioName = "114_1473301954286.wav"
            ongoingNumber = '114'

        failLogS['ongoingNumber'] = ongoingNumber
        failLogS['audioName'] = audioName
        failLogS['incoming'] = incoming
        if audioName != None:
            recordingContext = analyzeAudioFile(DEVICE_ID, audioName)
            print "%s:%s" % ("analyzeAudioFile", recordingContext)
            print "%s:%s" % ("type(recordingContext)", type(recordingContext))
            if recordingContext != None:
                analyzeNum = analyzeNum + 1
                result = re.findall(u'[\uAC00-\uD7A3]+', recordingContext)
                recordingContext_Hangul = ''.join(result)
                print "%s:%s" % ("recordingContext_Hangul", recordingContext_Hangul)
                print "%s:%s" % ("type(recordingContext_Hangul)", type(recordingContext_Hangul))

                result = re.findall(u'[\uAC00-\uD7A3]+', ANSWERSHEET[ongoingNumber])
                ANSWERSHEET_Hangul = ''.join(result)
                print "%s:%s" % ("ANSWERSHEET_Hangul", ANSWERSHEET_Hangul)
                print "%s:%s" % ("type(ANSWERSHEET_Hangul)", type(ANSWERSHEET_Hangul))
                if len(ANSWERSHEET_Hangul) > 0 and ANSWERSHEET_Hangul in recordingContext_Hangul:
                    success = True
                    recordSNum = recordSNum + 1
                    if incoming:
                        recordISNum = recordISNum + 1
                else:
                    recordFNum = recordFNum + 1
                    if incoming:
                        recordIFNum = recordIFNum + 1

                    failLogS['recordingContext_Hangul'] = recordingContext_Hangul
                    failLogS['ANSWERSHEET_Hangul'] = ANSWERSHEET_Hangul

            if os.path.isfile(audioName + ".wav"):
                os.remove(audioName + ".wav")

            if LOCALTEST == False:
                if os.path.isfile(audioName):
                    os.remove(audioName)
        else:
            print "%s(%s)" % ("audioName", audioName)
            notFoundNum = notFoundNum + 1

        print "%s(%s)" % ("success", str(success))
        printNumResult()
        if len(failLogS) > 0 and success == False:
            with codecs.open(failListFileName, 'a', 'utf-8') as f:
                f.write(json.dumps(failLogS, ensure_ascii=False) + "\r\n")
                f.close()
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        resultS['sys.exc_info()[0]'] = sys.exc_info()[0]
        resultS['sys.exc_info()[1]'] = sys.exc_info()[1]
        break
    finally:
        resultS['modified_time'] = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
        resultS['trycount'] = trycount
        resultS['notFoundNum'] = notFoundNum

        resultS['outcallSNum'] = outcallSNum
        resultS['outcallFNum'] = outcallFNum
        resultS['incallSNum'] = incallSNum
        resultS['incallFNum'] = incallFNum

        resultS['recordISNum'] = recordISNum
        resultS['recordIFNum'] = recordIFNum
        resultS['recordSNum'] = recordSNum
        resultS['recordFNum'] = recordFNum
        resultS['analyzeNum'] = analyzeNum
        try:
            resultS['outSuccess__rate'] = round(float(recordSNum-recordISNum)/float(outcallSNum+outcallFNum),5)
        except:
            resultS['outSuccess__rate'] = 0
        try:
            resultS['inSuccess__rate'] = round(float(recordISNum)/float(incallSNum+incallFNum),5)
        except:
            resultS['inSuccess__rate'] = 0
        try:
            resultS['success__rate'] = round(float(recordSNum)/float(analyzeNum),5)
        except:
            resultS['success__rate'] = 0

with open(resultFileName, 'a') as f:
   f.write(json.dumps(resultS) + "\r\n")
   f.close()

exit(0)
