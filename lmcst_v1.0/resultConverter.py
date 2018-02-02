# -*- coding: utf-8 -*-
import getpass
import sys
import time
import os, stat, glob
import telnetlib
import re
import codecs
import traceback
import socket
import json
import shutil

import cv2
from easygui.boxes.fileopen_box import tk
from Tkinter import *
import tkMessageBox
import easygui
import pygame
import winsound
import csv
import subprocess
from time import gmtime, strftime, localtime
import random
import datetime
import glob

from openpyxl import load_workbook
import unicodedata

with open("summary_json.txt") as f:
   content = f.readlines()
for index, line in enumerate(content):
   print line
   try:
      dict = json.loads(line)
   except:
      print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
      sys.exit(1)
   for key in dict.keys():
      value = dict.get(key)
      try:
         value = str(value)
      except:
         pass
      print type(value)
#      if type(value) == unicode:
      print key, value
      #if len(value) != len(value.replace('\"', '')):
      value = value.replace('\"', '')
      print "%s:%s" % ("value", value)
      print "%s:%s" % ("len(value)", str(len(value)))
      print "%s:%s" % ("len(re.sub('[^0-9.]', '', value)", str(len(re.sub('[^0-9.]', '', value))))
      if len(value) == len(re.sub('[^0-9.]', '', value)):
         if len(value) == 1 and value.startswith('0') == True:
            pass
         elif value.startswith('0') == True and value.startswith('0.') == False:
            continue
         if '.' in value:
            dict[key] = float(value)
         else:
            dict[key] = int(value)
#      if 'DalvikHeap_Free_AVG' == key:
#         sys.exit(0)

   with open("summary_json_re.txt", 'a') as f:
      f.write(json.dumps(dict)+ "\r\n")
      f.close()


sys.exit(0)



resultS = dict()
myName = sys.argv[0]
print "%s:%s" % ("myName", myName)
resultS['ID_FILENAME'] = myName

#PS Microsoft.PowerShell.Core\FileSystem::\\Tdds1\tdds1\outputs\tphone_android> adb -s emulator-5554 install -r dialer_x86_13158_44d6a1e.apk
START_TIME = strftime("%Y%m%d%H%M%S", localtime())
resultS['START_TIME'] = START_TIME
TARGET_APP = 'com.skt.prod.dialer'
resultS['TARGET_APP'] = TARGET_APP
TARGET_APP_FOLDERNAME = 'dialer'
resultS['TARGET_APP_FOLDERNAME'] = TARGET_APP_FOLDERNAME
#APK_DIRECTORY = 'Z:\\outputs\\tphone_android\\'
APK_DIRECTORY = '\\\\Tdds1\\tdds1\outputs\\tphone_android\\'


HOST = "localhost"
PORT = 681
emulator_console_auth_token="L0hbQpvCHX9GzpDa"

#DEVICE_ID = "emulator-" + str(PORT)
DEVICE_ID = "emulator-5554"
resultS['DEVICE_ID'] = DEVICE_ID
WAIT_SEC = 10
resultS['WAIT_SEC'] = WAIT_SEC
#user = raw_input("Enter your remote account: ")
#password = getpass.getpass()
#CALL_LIST = ["0222560021", "0318850488", "114", "027547474", "0222738770"]
try_count = 0
die_count = 0
success_count = 0
fail_count = 0
anr_count_detect_file = 0
anr_count_detect_screen = 0
pids = []
dataSet = dict()
WINDOW_WIDTH, WINDOW_HEIGHT = None, None


def selectLatestInAndroid(deviceId, path, prefix):
   global pids
   fileName = None
   fullfileName = None
   #ls -t ????? ???? ????.
   #ls -tr ?????? ???? ????.
   proc = subprocess.Popen("adb -s " + deviceId + " shell ls -t " + path, stdout=subprocess.PIPE)
   fd_popen = proc.stdout
   pids.append(proc.pid)

   fileList = fd_popen.read().strip()
   for file in fileList.split('\r\n'):
     if prefix in file:
         fileName = file
         fullfileName = path + file
         break
   return fileName, fullfileName

def selectLatest(path, prefix):
#   os.system("pushd " + path)
   if path != '':
      CURRENT_PATH = os.getcwd()
      os.chdir(path)
   fileList = glob.glob(prefix)

   latestMtime = 0
   latestFileName = None
   latestfullfileName = None
   for file in fileList:
      mtime = os.stat(file)[stat.ST_MTIME]
      if mtime > latestMtime:
         latestMtime = mtime
         latestFileName = file
         latestfullfileName = path + file

   if path != '':
   #   os.system("popd")
      os.chdir(CURRENT_PATH)
   return latestFileName, latestfullfileName

def getSize4Windows(deviceId):
   global pids
   global WINDOW_WIDTH, WINDOW_HEIGHT

   if WINDOW_WIDTH == None or WINDOW_HEIGHT == None:
      reVal = None
      proc = subprocess.Popen("adb -s " + deviceId + " shell wm size", stdout=subprocess.PIPE)
      fd_popen = proc.stdout
      pids.append(proc.pid)

      content = fd_popen.read().strip()
      # "Physical size: 1440x2560"
      for line in content.split('\r\n'):
         if 'Physical size: ' in line:
            reVal = line.strip('Physical size: ')
            break
      WINDOW_WIDTH = int(reVal.split('x')[0])
      WINDOW_HEIGHT = int(reVal.split('x')[1])

   return WINDOW_WIDTH, WINDOW_HEIGHT

def getMakeBox4Close(filename):
   x, y = 0, 0
   firstWord, lastWord = None, None
   firstIndex, lastIndex = 0, 0
   with open(filename) as f:
      content = f.readlines()
   for index, line in enumerate(content):
      if '닫' in line:
         firstIndex = index
         firstWord = line.split(' ')
      if '기' in line:
         lastIndex = index
         lastWord = line.split(' ')

      if (lastIndex - firstIndex) == 1:
         x = int(firstWord[1]) + int((int(lastWord[3]) - int(firstWord[1]))/2)
         width, height = getSize4Windows(DEVICE_ID)
         y = int(((height - int(firstWord[2])) - (height - int(firstWord[4]))) / 2) + (height - int(firstWord[4]))
         break

   return x, y

def isANR(deviceID, content, command):
   global anr_count_detect_screen
   reVal = False
   if unicode("응답하지않음", 'utf-8') in content:
      reVal = True

   if reVal == True:
      os.system(command + " makebox")
      boxFileName, boxFullFileName = selectLatest('', '*.box')
      x, y = getMakeBox4Close(boxFileName)
      if os.path.isfile(boxFileName):
         os.remove(boxFileName)

      if x > 0 and y > 0:
         anr_count_detect_screen = anr_count_detect_screen + 1
         os.system("adb -s " + deviceID + " shell input tap " + str(x) + " " + str(y))
         print "adb -s " + deviceID + " shell input tap " + str(x) + " " + str(y)
      else:
         print "-------------------------------------------------------------------------"
         print "Detect anr in the windows. But, not find location x(%s) / y(%s)!" % (str(x), str(y))
         print "-------------------------------------------------------------------------"

   return reVal

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

def callEndCall(deviceId):
   global pids
   reVal = None
   proc = subprocess.Popen("adb -s " + deviceId + " shell input keyevent KEYCODE_ENDCALL", stdout=subprocess.PIPE)
   fd_popen = proc.stdout
   pids.append(proc.pid)
   print "callEndCall(%s)" % (deviceId)
   time.sleep(WAIT_SEC)

def loadDataSet(type):
   global dataSet
   print "try file access...."

   if type == 'excel':
      SHEETS = [
         ['20170808_QITP-2116_T114.xlsx', 't114', 'A', 'B', 2, 1001],
      ]

      SHEET = SHEETS[0]
      wb = load_workbook(filename=SHEET[0])
      sheet_ranges = wb[SHEET[1]]
      for column_index in range(SHEET[4], SHEET[5] + 1):
         phonenum, t114, phoneinfo = None, None, None
         try:
            phonenum = sheet_ranges[SHEET[2] + str(column_index)].value
            t114 = sheet_ranges[SHEET[3] + str(column_index)].value
         except:
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

         if phonenum != None and t114 != None:
            try:
               dataSet[phonenum]
            except KeyError:
               dataSet[phonenum] = list()

            dataSet[phonenum] = [t114, ""]
   else:
      with open('call.dat') as f:
         csv_reader = csv.reader(f)
         for index, row in enumerate(csv_reader):
            phonenum, t114, phoneinfo = row
            try:
               dataSet[phonenum]
            except KeyError:
               dataSet[phonenum] = list()

            dataSet[phonenum] = [t114, phoneinfo]

   print "try file access....success!"
   print "total phoneNum: " + str(len(dataSet))

if len(sys.argv) > 1:
   during_hours = int(sys.argv[1])
   resultS['during_hours'] = during_hours
else:
   print "please input during hours!"
   sys.exit()

LOG_COVERAGE='narrow'
if len(sys.argv) > 2:
   #ex.
   #narrow(default)
   #full
   #입력 값 그대로
   LOG_COVERAGE = sys.argv[2]

resultS['LOG_COVERAGE'] = LOG_COVERAGE

hostname = socket.gethostname()
resultS['hostname'] = hostname

apkFileNameInHost, apkFullFileNameInHost = selectLatest(APK_DIRECTORY, TARGET_APP_FOLDERNAME + '_x86_*')
#apkFileNameInHost = None
#apkFullFileNameInHost = None
resultS['apkFullFileNameInHost'] = apkFullFileNameInHost
reVisionCount = None
commitHashCode = None
if apkFileNameInHost != None:
   reVisionCount = apkFileNameInHost.split('_')[2]
   commitHashCode = apkFileNameInHost.split('_')[3].split('.')[0]
else:
   reVisionCount = 'None'
   commitHashCode = 'None'
resultS['reVisionCount'] = reVisionCount
resultS['commitHashCode'] = commitHashCode
#"tphone_" + START_TIME + "_" + str(during_hours) + ".log"
logFileName = TARGET_APP + "_" + str(reVisionCount) + "_" + str(commitHashCode) + "_" + hostname  + "_" + START_TIME + "_" + str(during_hours) + ".log"
failListFileName = "FailList" + "_" + TARGET_APP + "_" + str(reVisionCount) + "_" + str(commitHashCode) + "_" + hostname  + "_" + START_TIME + "_" + str(during_hours) + ".log"
resultFileName = "Result" + "_" + sys.argv[0].split('/')[-1].split('.')[0] + "_" + TARGET_APP + "_" + hostname  + ".log"

def restart_emulator(logType='narrow'):
   global pids
   print "taskkill /F /IM qemu-system-x86_64.exe"
   os.system("taskkill /F /FI \"WindowTitle eq qemu-system*\"")
   os.system("taskkill /F /IM qemu-system-x86_64.exe")
#   os.system("taskkill /F /IM cmd.exe")
#   os.system("taskkill /F /IM adb.exe")
   for pid in pids:
      os.system("taskkill /F /PID " + str(pid))
      print "taskkill /F /PID " + str(pid)
   pids = []

   print 'emulator.bat'
   proc = subprocess.Popen(['emulator.bat'], stdout=subprocess.PIPE)
   pids.append(proc.pid)
   # os.spawnl(os.P_DETACH, 'emulator.bat')
   print 'emulator waiting...'
   time.sleep(WAIT_SEC * 10)
   print 'emulator is complete!'
   os.system('adb -s ' + DEVICE_ID + ' root')
   print 'adb root'

   #   proc = subprocess.Popen(['adb', '-s', DEVICE_ID, 'logcat', '-c'], stdout=subprocess.PIPE, shell=True)
   #   pids.append(proc.pid)
   #   print 'adb logcat -c'
   os.system('adb -s ' + DEVICE_ID + ' logcat -c')
   print 'adb logcat -c'

   if logType == 'full':
      proc = subprocess.Popen(['adb', '-s', DEVICE_ID, 'logcat' '>>', logFileName], stdout=subprocess.PIPE, shell=True)
      pids.append(proc.pid)
#      print 'adb logcat -v time'
      print 'adb logcat'
   elif logType == 'narrow':
      proc = subprocess.Popen(['adb', '-s', DEVICE_ID, 'logcat', '-s', 'TPhone:E', 'DEBUG:F', 'System.err:V',
                               'AndroidRuntime:V ActivityManager:E', '>>', logFileName], stdout=subprocess.PIPE,
                              shell=True)
      pids.append(proc.pid)
      print 'adb logcat -s TPhone:E DEBUG:F System.err:V AndroidRuntime:V ActivityManager:E'
   else:
      proc = subprocess.Popen(['adb', '-s', DEVICE_ID, 'logcat', '-s', logType+':V', 'DEBUG:F', 'System.err:V', 'AndroidRuntime:V ActivityManager:E', '>>', logFileName], stdout=subprocess.PIPE, shell=True)
      pids.append(proc.pid)
      print 'adb logcat -s ' + logType+':V' + ' DEBUG:F System.err:V AndroidRuntime:V ActivityManager:E'

def raise_fatalException():
   global die_count
   global LOG_COVERAGE
   print "emulator is died!"
   die_count = die_count + 1
   print "==============="
   print "die_count: " + str(die_count)
   print "==============="
   restart_emulator(LOG_COVERAGE)


def acceptAndcancel_call(w, tn, callNumber):
   try:
      accept_call(w, tn, callNumber)
      cancel_call(w, tn, callNumber)
   except:
      raise_fatalException()
   print "stoping mainloop()"
   try:
      w.destroy()
   except:
      pass
   #os.system("taskkill /F /FI \"WindowTitle eq tk*\"")

def accept_call(w, tn, callNumber):
   tn.write("gsm accept " + callNumber + "\r\n")
   print "active"
   #   tn.read_until("active") #inbound from 114        : active
   tn.read_until("OK", timeout=60)
   print "OK"

   print "waiting"
   time.sleep(WAIT_SEC)

def cancel_call(w, tn, callNumber):
   tn.write("gsm cancel " + callNumber + "\r\n")
   print "cancel"
   tn.read_until("OK", timeout=60)
   print "OK"
   print "waiting"
   time.sleep(WAIT_SEC)

restart_emulator(LOG_COVERAGE)
proc = subprocess.Popen("adb -s " + DEVICE_ID + " shell rm -rf /data/anr", stdout=subprocess.PIPE,
                        shell=True)
pids.append(proc.pid)

if apkFileNameInHost != None:
   os.system('adb -s ' + DEVICE_ID + ' install -r ' + apkFullFileNameInHost)
   print 'adb -s ' + DEVICE_ID + ' install -r ' + apkFullFileNameInHost

DATA_TYPE='excel'
loadDataSet(DATA_TYPE)
#loadDataSet('')
resultS['len(dataSet)'] = len(dataSet)


START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
EXPECT_END_TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=(during_hours+9))).strftime("%Y%m%d%H%M")

while long(EXPECT_END_TIME) > long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")) :
   CURRENTGMT9TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
   print "EXPECT_END_TIME: " + EXPECT_END_TIME
   print "CURRENTGMT9TIME: " + CURRENTGMT9TIME

   callNumber = dataSet.keys()[random.randrange(0, len(dataSet.keys()))]
   failLogS = dict()
   failLogS['CURRENTGMT9TIME'] = CURRENTGMT9TIME
   try:
      isThereError = False
      isOK_T114 = False
      isOK_PhoneInfo = False
      t114, phoneinfo = dataSet[callNumber]
      try:
         t114 = unicode(t114, 'utf-8')
      except (TypeError):
         pass
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
      failLogS['t114'] = t114

      result = re.findall(u'[\uAC00-\uD7A3]+', t114)
      t114_Hangul = ''.join(result)
      failLogS['t114_Hangul'] = t114_Hangul
      try:
         phoneinfo = unicode(phoneinfo, 'utf-8')
      except (TypeError):
         pass
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

      result = re.findall(u'[\uAC00-\uD7A3]+', phoneinfo)
      phoneinfo_Hangul = ''.join(result)
      failLogS['phoneinfo_Hangul'] = phoneinfo_Hangul
      try:
         callNumber = str(callNumber)
      except:
         pass
         print "[" + callNumber + "]"
         print type(callNumber)
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

      if len(t114) > 0 and len(t114_Hangul) == 0:
         print "-------------------------------------------------------------------------"
         print "callNumber(%s) / t114(%s) don't include hangul in t114." % (callNumber, t114)
         print "-------------------------------------------------------------------------"
         continue

      try_count = try_count + 1
      #os.system("adb -s " + DEVICE_ID + " root")
      print "try telnet connecting..."
      tn = telnetlib.Telnet(HOST, PORT, timeout=60)
      tn.write("auth " + emulator_console_auth_token + "\r\n")
      print "try telnet connecting...success!"

      failLogS['callNumber'] = callNumber
      tn.write("gsm call " + callNumber + "\r\n")
      print "incoming"
      tn.write("gsm list" + "\r\n")
      #   tn.read_until("incoming") #inbound from 114        : incoming
      tn.read_until("OK", timeout=60)
      print "OK"

      print "waiting"
      time.sleep(WAIT_SEC)

      fileName = "incoming_" + callNumber + ".png"
      if os.path.isfile(fileName):
         os.remove(fileName)

      print "adb -s " + DEVICE_ID + " shell " + "screencap -p /sdcard/" + fileName
      #os.system("adb -s " + DEVICE_ID + " shell " + "screencap -p /sdcard/" + fileName)
      #proc = subprocess.Popen("adb -s " + DEVICE_ID + " shell " + "screencap -p /sdcard/" + fileName, stdout=subprocess.PIPE)
      #proc.wait()
      proc = subprocess.Popen("adb -s " + DEVICE_ID + " shell " + "screencap -p /sdcard/" + fileName, stdout=subprocess.PIPE, shell=True)
      pids.append(proc.pid)
      time.sleep(WAIT_SEC)
      pproc = proc

      print "adb -s " + DEVICE_ID + " pull " + "/sdcard/" + fileName
      #os.system("adb -s " + DEVICE_ID + " pull " + "/sdcard/" + fileName)
      #proc = subprocess.Popen("adb -s " + DEVICE_ID + " pull " + "/sdcard/" + fileName, stdout=subprocess.PIPE)
      #proc.wait()
      proc = subprocess.Popen("adb -s " + DEVICE_ID + " pull " + "/sdcard/" + fileName, stdout=subprocess.PIPE, shell=True)
      pids.append(proc.pid)
      time.sleep(WAIT_SEC)
      print "taskkill /F /PID " + str(pproc.pid)
      os.system("taskkill /F /PID " + str(pproc.pid))
      pids.remove(pproc.pid)
      print "taskkill /F /PID " + str(proc.pid)
      os.system("taskkill /F /PID " + str(proc.pid))
      pids.remove(proc.pid)

      if os.path.isfile(fileName):
         print "pproc.pid:" + str(pproc.pid)
         print "proc.pid:" + str(proc.pid)
      else:
         raise Exception('not Working', "adb")
      # proc.wait()

      if os.path.isfile(fileName) == False:
         raise Exception('not Found', fileName)

      img = cv2.imread(fileName)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      cv2.imwrite(fileName, gray)
      tesseractCommand = "tesseract.exe " + fileName + " " + fileName + " -l kor"
      os.system(tesseractCommand)
      try:
         with codecs.open(fileName+".txt", 'rb', encoding='utf8') as f:
            content = f.read()
         print "-------------------------------------------"
         print content
         #hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')
         #hangul = re.compile('[^ ã±-ã£ê°-í£]+')
         #result = hangul.sub('', content)
         result = re.findall(u'[\uAC00-\uD7A3]+', content)
         t114_OCR1 = ''.join(result)
         failLogS['t114_OCR1'] = t114_OCR1
         isThereError = isANR(DEVICE_ID, t114_OCR1, tesseractCommand)
         if isThereError:
            failLogS['error'] = 'anr'
         elif len(t114_Hangul) > 0 and t114_Hangul in t114_OCR1:
            isOK_T114 = True
         print "-------------------------------------------"
         print "call#:[" + callNumber + "]"
         print "OCR:[" + t114_OCR1 + "]"
         print "right:[" + t114_Hangul + "]"
         print "isOK_T114:[" + str(isOK_T114) + "]"
         print "error:[" + str(isThereError) + "]"
         print "-------------------------------------------"

      except:
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
         break

      if isOK_T114 == False and isThereError == False:
         tesseractCommand = "tesseract.exe " + fileName + " " + fileName + "_psm6 --psm 6 -l kor"
         os.system(tesseractCommand)
         try:
            with codecs.open(fileName+"_psm6.txt", 'rb', encoding='utf8') as f:
               content = f.read()
            print "-------------------------------------------"
            print content
            #hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')
            #hangul = re.compile('[^ ã±-ã£ê°-í£]+')
            #result = hangul.sub('', content)
            result = re.findall(u'[\uAC00-\uD7A3]+', content)
            t114_OCR2 = ''.join(result)
            failLogS['t114_OCR2'] = t114_OCR2
            isThereError = isANR(DEVICE_ID, t114_OCR2, tesseractCommand)
            if isThereError:
               failLogS['error'] = 'anr'
            elif len(t114_Hangul) >0 and t114_Hangul in t114_OCR2:
               isOK_T114 = True
            print "-------------------------------------------"
            print "call#:[" + callNumber + "]"
            print "OCR:[" + t114_OCR2 + "]"
            print "right:[" + t114_Hangul + "]"
            print "isOK_T114:[" + str(isOK_T114) + "]"
            print "error:[" + str(isThereError) + "]"
            print "-------------------------------------------"
         except:
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            break

      if isOK_T114 == False and isThereError == False:
         tesseractCommand = "tesseract.exe " + fileName + " " + fileName + "_psm12 --psm 12 -l kor"
         os.system(tesseractCommand)
         try:
            with codecs.open(fileName+"_psm12.txt", 'rb', encoding='utf8') as f:
               content = f.read()
            print "-------------------------------------------"
            print content
            #hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')
            #hangul = re.compile('[^ ã±-ã£ê°-í£]+')
            #result = hangul.sub('', content)
            result = re.findall(u'[\uAC00-\uD7A3]+', content)
            t114_OCR3 = ''.join(result)
            failLogS['t114_OCR3'] = t114_OCR3
            isThereError = isANR(DEVICE_ID, t114_OCR3, tesseractCommand)
            if isThereError:
               failLogS['error'] = 'anr'
            elif len(t114_Hangul) >0 and t114_Hangul in t114_OCR3:
               isOK_T114 = True
            print "-------------------------------------------"
            print "call#:[" + callNumber + "]"
            print "OCR:[" + t114_OCR3 + "]"
            print "right:[" + t114_Hangul + "]"
            print "isOK_T114:[" + str(isOK_T114) + "]"
            print "error:[" + str(isThereError) + "]"
            print "-------------------------------------------"
         except:
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            break

      w = Tk()
      print "isOK_T114: " + str(isOK_T114)
      if isOK_T114:
         notiText = callNumber + " is correct! T114 is " + t114
         label = Label(w, text=notiText, width=len(notiText))
         label.pack()
         try:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
         except:
            #Unexpected error:  <type 'exceptions.RuntimeError'> Failed to play sound
            pass
         #w.after(5000, lambda: w.destroy())
         success_count = success_count + 1
      else:
         if isThereError == False:
            notiText = callNumber + " is Not correct! T114 is " + t114
         else:
            notiText = "There is a ANR during calling " + callNumber

         label = Label(w, text=notiText, width=len(notiText))
         label.pack()
         try:
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
         except:
            #Unexpected error:  <type 'exceptions.RuntimeError'> Failed to play sound
            pass
         fail_count = fail_count + 1

         with codecs.open(failListFileName, 'a', 'utf-8') as f:
            f.write(json.dumps(failLogS, ensure_ascii=False) + "\r\n")
            f.close()

         direcTory = os.getcwd() + '\\failsArchive\\' + START______TIME
         try:
            os.stat(direcTory)
         except:
            #os.mkdir(direcTory)
            os.makedirs(direcTory)
         shutil.move(fileName, direcTory + "\\" + START_TIME + "_" + CURRENTGMT9TIME + "_" + fileName)

         with codecs.open(direcTory + "\\" + START_TIME + "_" + CURRENTGMT9TIME + "_" + fileName + '.txt', 'a', 'utf-8') as f:
            f.write(json.dumps(failLogS, ensure_ascii=False) + "\r\n")
            f.close()

      anrFileNameInDevice, anrFullFileNameInDevice = selectLatestInAndroid(DEVICE_ID, '/data/anr/', 'traces')
      if anrFileNameInDevice != None:
         proc = subprocess.Popen("adb -s " + DEVICE_ID + " pull " + anrFullFileNameInDevice, stdout=subprocess.PIPE,
                                 shell=True)
         pids.append(proc.pid)
         time.sleep(WAIT_SEC)
         proc = subprocess.Popen("adb -s " + DEVICE_ID + " shell rm -f " + anrFullFileNameInDevice, stdout=subprocess.PIPE,
                                 shell=True)
         pids.append(proc.pid)
         direcTory = os.getcwd() + '\\failsArchive\\' + START______TIME
         with codecs.open(anrFileNameInDevice, 'rb', encoding='utf8') as f:
            content = f.read()
         result = re.findall(TARGET_APP, content)
         if len(result) == 0:
            if os.path.isfile(anrFileNameInDevice):
               os.remove(anrFileNameInDevice)
         else:
            try:
               os.stat(direcTory)
            except:
               #os.mkdir(direcTory)
               os.makedirs(direcTory)
            shutil.move(anrFileNameInDevice, direcTory + "\\" + START_TIME + "_" + CURRENTGMT9TIME + "_ANR_" + anrFileNameInDevice)
            anr_count_detect_file = anr_count_detect_file + 1

      print "toast is diplayed!"
      w.after(1000, lambda: acceptAndcancel_call(w, tn, callNumber))
      w.mainloop()
      print "toast is closed!"

      print "==============="
      print "CURRENTGMT9TIME: " + CURRENTGMT9TIME
      print "success__rate: " + str(round(float(success_count) / float(try_count), 5))
      print "success_count: " + str(success_count)
      print "fail____count: " + str(fail_count)
      print "die_____count: " + str(die_count)
      print "try_____count: " + str(try_count)
      print "anrFile_count: " + str(anr_count_detect_file)
      print "anrScr__count: " + str(anr_count_detect_screen)

      resultS['success_count'] = success_count
      resultS['fail_count'] = fail_count
      resultS['die_count'] = die_count
      resultS['try_count'] = try_count
      resultS['anr_count_detect_file'] = anr_count_detect_file
      resultS['anr_count_detect_screen'] = anr_count_detect_screen
      print "==============="

      tn.close()
      print "telnet close!"
      if False:
         checkCount = 0
         while checkCallState(DEVICE_ID) > 0 and checkCount < 10:
            checkCount = checkCount + 1
            callEndCall(DEVICE_ID)
         if checkCount >= 10:
            raise Exception('checkCallState', 'not nomal')
   except:
      print "Main Except::Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
      try:
         w.destroy()
      except:
         pass
      raise_fatalException()
   finally:
      for zippath in glob.iglob(os.path.join(os.getcwd(), '*.png')):
         os.remove(zippath)
      for zippath in glob.iglob(os.path.join(os.getcwd(), '*.txt')):
         os.remove(zippath)

resultS['success_count'] = success_count
resultS['fail_count'] = fail_count
resultS['die_count'] = die_count
resultS['try_count'] = try_count
resultS['anr_count_detect_file'] = anr_count_detect_file
resultS['anr_count_detect_screen'] = anr_count_detect_screen
resultS['success__rate'] = round(float(success_count)/float(try_count),5)

with open(resultFileName, 'a') as f:
   f.write(json.dumps(resultS))
   f.close()
print "==============="
if LOG_COVERAGE == 'narrow':
   print ">>>log analysis is starting..."
   logInspect.uniq(logFileName)
   print ">>>log analysis is completed!"
else:
   print "LOG_COVERAGE: " + LOG_COVERAGE

print "==============="
print "DRUING____HOURS: " + str(during_hours)
print "START______TIME: " + START______TIME
print "EXPECT_END_TIME: " + EXPECT_END_TIME
print "CURRENTGMT9TIME: " + (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
print "last_success__rate: " + str(round(float(success_count)/float(try_count),5))
print "last_success_count: " + str(success_count)
print "last_fail_count___: " + str(fail_count)
print "last_try_____count: " + str(try_count)
print "last_die_____count: " + str(die_count)
print "last_anrFile_count: " + str(anr_count_detect_file)
print "last_anrScr__count: " + str(anr_count_detect_screen)

print "<<<the end!>>>"
#for pid in pids:
#   os.system("taskkill /F /PID " + str(pid))
#   print "taskkill /F /PID " + str(pid)

sys.exit(0)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
##################################################
fileName = '20170818204416_201708191645_incoming_0535637344.png'
os.system("tesseract.exe " + fileName + " " + fileName + " -l kor")
try:
   with codecs.open(fileName + ".txt", 'rb', encoding='utf8') as f:
      content = f.read()
   print "-------------------------------------------"
   print content
   # hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')
   # hangul = re.compile('[^ ã±-ã£ê°-í£]+')
   # result = hangul.sub('', content)
   result = re.findall(u'[\uAC00-\uD7A3]+', content)
   print "-------------------------------------------"
   print result
   print "-------------------------------------------"
   print unicode("응답하지않음", 'utf-8')
   print "-------------------------------------------"
   print isANR(DEVICE_ID, ''.join(result), "tesseract.exe " + fileName + " " + fileName + " -l kor")
except:
   pass
   print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

exit(1)
##################################################
loadDataSet('excel')
failLogS = dict()
callNumber = dataSet.keys()[random.randrange(0, len(dataSet.keys()))]
t114, phoneinfo = dataSet[callNumber]
result = re.findall(u'[\uAC00-\uD7A3]+', t114)
failLogS['t114'] = t114
t114_Hangul = ''.join(result)
print type(t114_Hangul)
print type(t114_Hangul.encode('utf-8'))
failLogS['t114_Hangul'] = t114_Hangul

with codecs.open('fail.txt', 'a', 'utf-8') as f:
   f.write(t114_Hangul + "\r\n")
#   f.write(t114_Hangul.encode('utf-8') + "\r\n")
   f.write(json.dumps(failLogS, ensure_ascii=False) + "\r\n")
   f.close()
exit(0)
##################################################
with open('call.dat') as f:
    csv_reader= csv.reader(f)
    dataSet = dict()
    for index, row in enumerate(csv_reader) :
        phonenum, t114, phoneinfo = row
        try:
            dataSet[phonenum]
        except KeyError:
            dataSet[phonenum] = list()

        dataSet[phonenum] = [t114, phoneinfo]
print len(dataSet)


for phonenum in dataSet.keys() :
   t114, phoneinfo = dataSet[phonenum]
   #phoneinfo = dataSet[phonenum]
   #print dataSet[phonenum]
   #print phonenum, t114, phoneinfo
   print t114
   print type(t114)
   result = re.findall(u'[\uAC00-\uD7A3]+', unicode(t114, 'utf-8'))
   print result
   print ''.join(result)

sys.exit(0)


print "wait"
time.sleep(WAIT_SEC)
print "start"
os.system("adb -s " + DEVICE_ID + " shell " + "radiooptions 9 1 0") #receive call

print "wait"
time.sleep(WAIT_SEC)
print "start"

os.system("adb -s " + DEVICE_ID + " shell " + "radiooptions 1 1 0") #endcall

print "wait"
time.sleep(WAIT_SEC)
print "start"

tn.write("gsm call 027547474" + "\r\n")
tn.read_until("OK")

print "wait"
time.sleep(WAIT_SEC)
print "start"

os.system("adb -s " + DEVICE_ID + " shell " + "radiooptions 10 1 0") #reject call

print "wait"
time.sleep(WAIT_SEC)
print "start"

os.system("adb -s " + DEVICE_ID + " shell " + "radiooptions 1 1 0") #endcall

print "wait"
time.sleep(WAIT_SEC)
print "start"

tn.write("gsm call 0222738770" + "\r\n")
tn.read_until("OK")

print "wait"
time.sleep(WAIT_SEC)
print "start"

os.system("adb -s " + DEVICE_ID + " shell " + "radiooptions 9 1 0") #receive call

print "wait"
time.sleep(WAIT_SEC)
print "start"

os.system("adb -s " + DEVICE_ID + " shell " + "radiooptions 1 1 0") #endcall

print "wait"
time.sleep(WAIT_SEC)
print "start"

tn.close()
print "close!"

#os.system("adb -s " + DEVICE_ID + " shell " + "radiooptions 9 1 0") #receive call
#os.system("adb -s " + DEVICE_ID + " shell " + "radiooptions 10 1 0") #reject call
#s.system("adb -s " + DEVICE_ID + " shell " + "radiooptions 1 1 0") #endcall
#adb shell input keyevent 6 #endcall
#gsm cancel 01098276331

