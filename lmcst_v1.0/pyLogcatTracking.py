# -*- coding: utf-8 -*-
import json
import socket

import numpy as np
import os
import sys
import time
from time import gmtime, strftime
import random
import subprocess
from pandas import Series, DataFrame
import datetime
from sys import platform as _platform



from common.deviceInfo import *
from common.contant import selfVersion, LMCFT_FOLDER_FAIL, LMCFT_FOLDER_TRACKING, setDEBUG, LMCFT_FOLDER_RESULT

reload(sys)
sys.setdefaultencoding('utf-8')

"""
python pyLogcatTracking.py [unknown][AndroidSDKbuiltforx86_64][7.0][3761695][01049611657][1][master][8b136de][14479][lmcft][0][NONE] emulator-5554 com.skt.prod.dialer [201710110620][201810111620][10][1000] 1 0
"""
if __name__ == '__main__':
    #setDEBUG(True)
    resultS={}

    if len(sys.argv) > 1:
        UUID = sys.argv[1].replace("'", "")
    else:
        sys.exit()

    if len(sys.argv) > 2:
        deviceID = sys.argv[2].replace("'", "")
    else:
        sys.exit()

    if len(sys.argv) > 3:
        packageName = sys.argv[3].replace("'", "")
    else:
        sys.exit()

    if len(sys.argv) > 4:
        TIMEID = sys.argv[4].replace("'", "")
    else:
        sys.exit()

    if len(sys.argv) > 5:
        POLLING_DELAY = sys.argv[5].replace("'", "")
    else:
        sys.exit()

    tagName = 'TPhone'
    if tagName!= None:
        tagName = tagName.replace(' ', '-')
    resultS['TAG'] = tagName

    resultS['selfVersion'] = selfVersion

    myName = sys.argv[0].split('/')[-1]
    resultS['ID_FILENAME'] = myName

    hostname = socket.gethostname()
    resultS['hostname'] = hostname

    print("%s:%s" % ('UUID', UUID))
    print("%s:%s" % ('deviceID', deviceID))
    resultS['DEVICE_ID'] = deviceID
    print("%s:%s" % ('packageName', packageName))
    resultS['PACKAGENAME'] = packageName
    print("%s:%s" % ('TIMEID', TIMEID))
    print("%s:%s" % ('POLLING_DELAY', POLLING_DELAY))
    resultS['POLLING_DELAY'] = int(POLLING_DELAY)

    resultS['MANUFACTURER'] = getManufacturerFromDevice(deviceID)
    resultS['MODEL'] = getModelNameFromDevice(deviceID)
    resultS['OSVERSION'] = getOSVersionFromDevice(deviceID)
    resultS['MANUFACTURERVERSION'] = getManufactureVersionFromDevice(deviceID)
    resultS['MYNUM'] = getPhoneNumberFromDevice(deviceID)

    START_TIME = TIMEID.split("][")[0].replace("[", "").replace("]", "").replace("'", "")
    EXPECT_END_TIME = TIMEID.split("][")[1].replace("[", "").replace("]", "").replace("'", "")
    duringHours = TIMEID.split("][")[2].replace("[", "").replace("]", "").replace("'", "")
    throttle = TIMEID.split("][")[3].replace("[", "").replace("]", "").replace("'", "")

    print("%s:%s" % ('START_TIME', START_TIME))
    resultS['START_TIME'] = START_TIME
    print("%s:%s" % ('EXPECT_END_TIME', EXPECT_END_TIME))
    resultS['EXPECT_END_TIME'] = EXPECT_END_TIME
    print("%s:%s" % ('duringHours', duringHours))
    resultS['duringHours'] = int(duringHours)
    print("%s:%s" % ('throttle', throttle))
    resultS['throttle'] = int(throttle)

    git_branchName = UUID.split("][")[6].replace("[", "").replace("]", "").replace("'", "")
    git_commitValue = UUID.split("][")[7].replace("[", "").replace("]", "").replace("'", "")
    git_revCount = UUID.split("][")[8].replace("[", "").replace("]", "").replace("'", "")

    print("%s:%s" % ('git_branchName', git_branchName))
    resultS['git_branchName'] = git_branchName
    print("%s:%s" % ('git_commitValue', git_commitValue))
    resultS['git_commitValue'] = git_commitValue
    print("%s:%s" % ('git_revCount', git_revCount))
    resultS['git_revCount'] = int(git_revCount)

    print ("CURRENTGMT9TIME: " + (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M"))
    print ("CURRENT____TIME: " + str(datetime.datetime.now()))
    print ("CURRENT____TIME: " + str(time.ctime()))
    print ("CURRENT____TIME: " + datetime.datetime.now().strftime("%Y%m%d%H%M"))
    print ("CURRENTLOCATIME: " + time.strftime("%Y%m%d%H%M", time.localtime()))
    resultFileName = LMCFT_FOLDER_RESULT + "Result_healthCheck" + "_" + myName.split('.')[0] + ".log"

    args = {}
    args["DEVICE_ID"] = deviceID
    args["logfullfilename"] = logfullfilename = LMCFT_FOLDER_FAIL + myName.split('.')[0] + "\\" + START_TIME + "\\" +\
        "Logcat" + "_" + tagName + '_' + packageName + "_" + hostname + "_" + START_TIME + "_" + str(duringHours) + ".log"
    print("%s:%s" % ('logfullfilename', logfullfilename))
    args["tag"] =  tagName

    LOGPROCESS, LOGINFO = getProc4LogCat(**args)

    traceFileName = LMCFT_FOLDER_TRACKING + "trace" + "_" + myName.split('.')[0] + "_" + tagName + '_' + START_TIME + ".log"
    print("%s:%s" % ('traceFileName', traceFileName))

    try:
        while os.path.isfile(logfullfilename) == False:
            print '.',
            time.sleep(15)
            if long(EXPECT_END_TIME) <= long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")):
                break

        if os.path.isfile(logfullfilename) :
            with open(logfullfilename, 'r') as logfullfile:
                if long(EXPECT_END_TIME) > long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")) :
                    mkdirs(traceFileName)
                    where = 0
                    count = 0
                    while True:
                        logResultS = {}
                        logfullfile.seek(where)
                        line = logfullfile.readline()
                        count = count + 1
                        resultS['line#'] = count
                        if line == None or len(line) == 0:
                            time.sleep(10)
                        else:
                            try:
                                resultS['execTime'] = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M%S")
                                print (line)
                                items = line.split(' ')
                                if len(items) >= 7:
                                    key = 'LogTime'
                                    if items[0] and items[1]:
                                        resultS['execTime'] = logResultS[key] = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y") + '-' + items[0] + ' ' + items[1]
                                    # PIDS
                                    key = 'PID'
                                    if items[2]:
                                        logResultS[key] = int(items[2])

                                    key = 'TID'
                                    if items[3]:
                                        logResultS[key] = int(items[2])

                                    # LOGLEVEL
                                    logResultS['LogLV'] = items[4]

                                    key = 'LogTAG'
                                    if ':' in items[5]:
                                        items[5] = items[5].split(':')[0]
                                    if ' ' in items[5]:
                                        items[5] = items[5].strip()
                                    if items[5]:
                                        logResultS[key] = items[5]
                                    key = 'Message'
                                    message = None
                                    if items[6] == ':':
                                        logResultS['Words'] = items[7:]
                                        message = ' '.join(items[7:])
                                    else:
                                        logResultS['Words'] = items[6:]
                                        message = ' '.join(items[6:])
                                    if message:
                                        logResultS[key] = message
                                        logResultS['MessageLength'] = len(message)

                                logResultS.update(resultS)
                                with open(traceFileName, 'a') as f:
                                    f.write(json.dumps(logResultS) + "\n")
                                    f.close()
                                where = logfullfile.tell()
                            except:
                                printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))

                        if long(EXPECT_END_TIME) <= long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")) :
                            break

    finally:
        print ("CURRENTGMT9TIME: " + (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M"))
        print ("CURRENT____TIME: " + str(datetime.datetime.now()))
        print ("CURRENT____TIME: " + str(time.ctime()))
        print ("CURRENT____TIME: " + datetime.datetime.now().strftime("%Y%m%d%H%M"))
        print ("CURRENTLOCATIME: " + time.strftime("%Y%m%d%H%M", time.localtime()))
        resultS['execTime'] = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M%S")

        if LOGPROCESS != None:
            try:
                LOGPROCESS.kill()
            except:
                printError("%s:%s" % ("Unexpected error", getExceptionString(sys.exc_info())))
            resultS['LOGINFO'] = LOGINFO.getAllInfo()
            print (resultS['LOGINFO'])

        with open(resultFileName, 'a') as f:
            f.write(json.dumps(resultS).replace('\\', '') + "\n")
            f.close()

    sys.exit()


"""
10-10 17:39:25.379 3090 3090 E TPhone : [TPhoneSystemAgent][hdvoice_roaming]mHDVoiceAvailable is not same as SettingKey.HDVOICE_AVAILABLE!

"""

