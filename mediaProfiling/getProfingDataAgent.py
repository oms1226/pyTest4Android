# -*- coding: utf-8 -*-
#!/usr/bin/python
import datetime
import threading

from common.contant import *
from common.deviceInfo import *
from os import walk
import pandas as pd
from sys import platform as _platform


MIN_SLEEPTIME = 60
MAX_SLEEPTIME = 15 * 60
START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
CURRENT_WRITE_LINE = 0
MAX_WRITE_LINE = 5000

def getPROFILE_FILEFULLNAME(time):
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        reVal = ("../../elasticRawDatas/refinedDatas4MyCom/trtc_%s.profile" % time)
    elif _platform == "win32" or _platform == "win64":
        reVal = ("..\\..\\elasticRawDatas\\refinedDatas4MyCom\\trtc_%s.profile" % time)

    return reVal

PROFILE_FILEFULLNAME=getPROFILE_FILEFULLNAME(START______TIME)
PROFILE_RAW_FILEFOLDER = "rawdata"
setDEBUG(True)

Trtr_Target_fileName_Subfixs = [
    ".profile",
    ".setting",
]
Trtr_Target_fileName_Subfixs_InDevice = [
    "_trtc.profile",
    "_trtc.setting",
]

def getFileListInAndroidDevice(cmd, subfixs):
    fd_popen = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE).stdout

    #data = fd_popen.read().strip()
    reVal = []
    while 1:
        line = fd_popen.readline()
        if not line:
            break
        line = str(line).strip("\r").strip("\n").strip()
        for subfix in subfixs:
            if line.endswith(subfix):
                reVal.append(line)
    fd_popen.close()

    return reVal

def getRawDatasInLocalPC(subfixs):
    reVal = []
    for (dirpath, dirnames, rawFilenames) in walk(PROFILE_RAW_FILEFOLDER):
        printEx("%s:%s" % ("dirpath", dirpath))
        printEx("%s:%s" % ("dirnames", dirnames))
        printEx("%s:%s" % ("rawFilenames", rawFilenames))
        break
    if len(rawFilenames) > 0:
        for rawFilename in rawFilenames:
            isGet = False
            for subfix in subfixs:
                if rawFilename.endswith(subfix):
                    isGet = True
            if isGet == False:
                continue

            if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
                rawFullFilename = PROFILE_RAW_FILEFOLDER + "/" + rawFilename
            elif _platform == "win32" or _platform == "win64":
                rawFullFilename = PROFILE_RAW_FILEFOLDER + "\\" + rawFilename

            if os.path.isfile(rawFullFilename):
                with open(rawFullFilename) as f:
                    while True:
                        line = f.readline().replace('\r', '').replace('\n', '')
                        if not line: break
                        reVal.append(line)
                    f.close()
                os.remove(rawFullFilename)
    return reVal

def getRawDatasInDevice():
    reVal = []
    for id in getRealDevices():
        Trtr_Profiling_fileNames = getFileListInAndroidDevice("adb -s " + id + " shell ls " + "/sdcard/trtc_logs",
                                                              Trtr_Target_fileName_Subfixs_InDevice)
        # for Trtr_Target_fileName_Subfix in Trtr_Target_fileName_Subfixs_InDevice:
        #    Trtr_Profiling_fileName = getModelNameFromDevice(id) + Trtr_Target_fileName_Subfix
        for Trtr_Profiling_fileName in Trtr_Profiling_fileNames:
            if os.path.isfile(Trtr_Profiling_fileName):
                os.remove(Trtr_Profiling_fileName)

            os.system("adb -s " + id + " pull " + "/sdcard/trtc_logs/" + Trtr_Profiling_fileName)

            if os.path.isfile(Trtr_Profiling_fileName):
                os.system("adb -s " + id + " shell rm -f " + "/sdcard/trtc_logs/" + Trtr_Profiling_fileName)
                with open(Trtr_Profiling_fileName) as f:
                    while True:
                        line = f.readline().replace('\r', '').replace('\n', '')
                        if not line: break
                        reVal.append(line)
                    f.close()
                os.remove(Trtr_Profiling_fileName)
    return reVal

def getRawCSVsInLocalPC():
    reVal = []
    #ex. DSLAII_20181005180000_GPSA(SM-G950N).GPSB(SM-G930S)_com.skt.trtc.sample_GPSA.csv, DSLAII_20181005180000_GPSA(SM-G950N).GPSB(SM-G930S)_com.skt.trtc.sample_GPSB.csv
    for (dirpath, dirnames, rawFilenames) in walk(PROFILE_RAW_FILEFOLDER):
        printEx("%s:%s" % ("dirpath", dirpath))
        printEx("%s:%s" % ("dirnames", dirnames))
        printEx("%s:%s" % ("rawFilenames", rawFilenames))
        break
    if len(rawFilenames) > 0:
        for rawFilename in rawFilenames:
            if rawFilename.endswith('.csv') == False:
                continue

            if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
                rawFullFilename = PROFILE_RAW_FILEFOLDER + "/" + rawFilename
            elif _platform == "win32" or _platform == "win64":
                rawFullFilename = PROFILE_RAW_FILEFOLDER + "\\" + rawFilename

            if os.path.isfile(rawFullFilename):
                templateDataJson = {}
                filenameSplit = rawFilename.split('_')
                if len(filenameSplit) != 5:
                    printError("%s 's split_length is %s" % (rawFilename, len(filenameSplit)))
                    continue
                templateDataJson["filename"] = rawFilename
                templateDataJson["catagory"] = filenameSplit[0]
                templateDataJson["explicitTime"] = filenameSplit[1]
                templateDataJson["Combination"] = filenameSplit[2]
                templateDataJson["app_name"] = filenameSplit[3].lower()
                templateDataJson["Destination"] = filenameSplit[4].split('.')[0]
                templateDataJson["Identifier"] = filenameSplit[0:3]

                for comb in templateDataJson["Combination"].split('.'):
                    if templateDataJson["Destination"] in comb:
                        templateDataJson["model"] = comb.replace(templateDataJson["Destination"], "").replace("(", "").replace(")", "").upper()
                    else:
                        templateDataJson["partnerModel"] = comb.replace("GPSA", "").replace("GPSB", "").replace("(", "").replace(")", "").upper()

                data = pd.read_csv(rawFullFilename)
                rowDataJson = {}
                for index, row in data[(data['Active Level'] != '-')].iterrows():
                    if row['Destination'].replace(" ", "") == templateDataJson["Destination"]:
                        if row['Source'].replace(" ", "") == 'GPSRemote':
                            if templateDataJson["Destination"] == 'GPSA':
                                rowDataJson["Source"] = 'GPSB'
                            else:
                                rowDataJson["Source"] = 'GPSA'
                            if row['Active Level'] != '-':
                                rowDataJson["ActiveLevel.float"] = float(row['Active Level'])
                            if row['Noise Level'] != '-':
                                rowDataJson["NoiseLevel.float"] = float(row['Noise Level'])
                            if row['POLQA SWB v2.4'] != '-':
                                rowDataJson["POLQASWBv2.4.float"] = float(row['POLQA SWB v2.4'])
                            if row['Offset'] != '-':
                                rowDataJson["Offset.float"] = float(row['Offset'])
                            if row['Offset Minimum'] != '-':
                                rowDataJson["OffsetMinimum.float"] = float(row['Offset Minimum'])
                            if row['Offset Maximum'] != '-':
                                rowDataJson["OffsetMaximum.float"] = float(row['Offset Maximum'])
                            if row['Latitude (Destination)'] != '-' and row['Longitude (Destination)'] != '-':
                                rowDataJson["location"] = "%s,%s" % (row['Latitude (Destination)'], row['Longitude (Destination)'])

                            if row['Time (Destination)'] != '-':
                                try:
                                    # https://docs.python.org/2/library/time.html#time.strftime
                                    Time_Destination = datetime.datetime.strptime(row['Time (Destination)'], "%d %m %Y %H:%M:%S")#ex. 4 10 2018 17:35:31
                                    rowDataJson["execTime"] = Time_Destination.strftime('%Y-%m-%d %H:%M:%S')#"execTime": "2018-10-04 16:49:01.889"
                                except:
                                    printError("expected error for time-data-format: ", sys.exc_info()[0], sys.exc_info()[1])
                                    rowDataJson["execTime"] = templateDataJson["explicitTime"]
                            else:
                                rowDataJson["execTime"] = templateDataJson["explicitTime"]

                            rowDataJson.update(templateDataJson)
                            reVal.append(json.dumps(rowDataJson, ensure_ascii=False))

                os.remove(rawFullFilename)
    return reVal


if __name__ == "__main__":
    AUTOMODE = False
    while len(sys.argv) > 1:
        if len(sys.argv) > 1 and '-a' in sys.argv[1]:
            AUTOMODE = True
            sys.argv.pop(1)

    printEx("%s:%s" % ("AUTOMODE", AUTOMODE))

    sleepTime = MIN_SLEEPTIME
    while True:
        RawDatas = []
        try:
            RawDatas = RawDatas + getRawDatasInLocalPC(Trtr_Target_fileName_Subfixs)
            RawDatas = RawDatas + getRawDatasInDevice()
            RawDatas = RawDatas + getRawCSVsInLocalPC()

        except:
            printError("Main Logic Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1])
        finally:
            if len(RawDatas) > 0:
                for RawData in RawDatas:
                    try:
                        RawDataJson = json.loads(RawData)
                    except:
                        printError("expected error for json-format: ", sys.exc_info()[0], sys.exc_info()[1])
                        printEx("%s:%s" % ("RawData", RawData))
                        continue

                    """
                  71b17b3ae41bc256f43da5d666d63d36a16f1ea7
                  0.8.0[1236/d15b794d54348969b8e9021aaee2840dc1adbb08]
                  """
                    if "os" in RawDataJson.keys() and RawDataJson["os"] == "ios":
                        if "os_sdk_int" in RawDataJson.keys() and "os_sdk_str" not in RawDataJson.keys():
                            RawDataJson['os_sdk_str'] = RawDataJson['os_sdk_int']
                            del RawDataJson['os_sdk_int']
                        if "googTypingNoiseState" in RawDataJson.keys():
                            if RawDataJson["googTypingNoiseState"] == "true":
                                RawDataJson["googTypingNoiseState"] = True
                            elif RawDataJson["googTypingNoiseState"] == "false":
                                RawDataJson["googTypingNoiseState"] = False
                        if "googInitiator" in RawDataJson.keys():
                            if RawDataJson["googInitiator"] == "true":
                                RawDataJson["googInitiator"] = True
                            elif RawDataJson["googInitiator"] == "false":
                                RawDataJson["googInitiator"] = False
                        if "googWritable" in RawDataJson.keys():
                            if RawDataJson["googWritable"] == "true":
                                RawDataJson["googWritable"] = True
                            elif RawDataJson["googWritable"] == "false":
                                RawDataJson["googWritable"] = False

                    if "trtc_version" in RawDataJson:
                        trtc_version_name = "None"
                        trtc_git_hashcode = "None"
                        trtc_git_revcnt = 0
                        trtc_build_pc = "None"
                        trtc_build_time = "None"

                        trtc_version = RawDataJson["trtc_version"]
                        if '[' in trtc_version:
                            trtc_version_name = trtc_version.split('[')[0]
                            trtc_git_hashcode = trtc_version.split('[')[1]
                            if '/' in trtc_git_hashcode:
                                trtc_git_revcnt = int(trtc_git_hashcode.split('/')[0])
                                trtc_git_hashcode = ''.join(trtc_git_hashcode.split('/')[1:])
                            elif '|' in trtc_git_hashcode:
                                trtc_git_revcnt = int(trtc_git_hashcode.split('|')[0])
                                trtc_git_hashcode = ''.join(trtc_git_hashcode.split('|')[1:])
                            trtc_git_hashcode = trtc_git_hashcode.replace(']', '')
                        elif '/' in trtc_version:
                            trtc_git_revcnt = int(trtc_version.split('/')[0])
                            trtc_git_hashcode = ''.join(trtc_version.split('/')[1:])
                        elif '|' in trtc_version:
                            trtc_git_revcnt = int(trtc_version.split('|')[0])
                            trtc_git_hashcode = ''.join(trtc_version.split('|')[1:])
                        else:
                            trtc_git_hashcode = trtc_version

                        if '/' in trtc_git_hashcode:
                            trtc_git_hashcode = trtc_git_hashcode.split('/')[0]
                            trtc_build_pc = ''.join(trtc_git_hashcode.split('/')[1:])
                        elif '|' in trtc_git_hashcode:
                            trtc_git_hashcode = trtc_git_hashcode.split('|')[0]
                            trtc_build_pc = ''.join(trtc_git_hashcode.split('|')[1:])

                        if '/' in trtc_build_pc:
                            trtc_build_pc = trtc_git_hashcode.split('/')[0]
                            trtc_build_time = ''.join(trtc_git_hashcode.split('/')[1:])
                        elif '|' in trtc_build_pc:
                            trtc_build_pc = trtc_git_hashcode.split('|')[0]
                            trtc_build_time = ''.join(trtc_git_hashcode.split('|')[1:])

                        RawDataJson['trtc_version_name'] = trtc_version_name
                        RawDataJson['trtc_git_hashcode'] = trtc_git_hashcode
                        RawDataJson['trtc_git_revcnt'] = trtc_git_revcnt
                        RawDataJson['trtc_build_pc'] = trtc_build_pc
                        RawDataJson['trtc_build_time'] = trtc_build_time

                    with codecs.open(PROFILE_FILEFULLNAME, 'a', 'utf-8') as f:
                        f.write(json.dumps(RawDataJson, ensure_ascii=False) + "\r\n")
                        CURRENT_WRITE_LINE += 1
                        f.close()

                    if CURRENT_WRITE_LINE > MAX_WRITE_LINE :
                        CURRENT_WRITE_LINE = 0
                        START______TIME = str(int(START______TIME) + 1)
                        # PROFILE_FILEFULLNAME = "data\\trtc_" + (datetime.datetime.utcnow() + datetime.timedelta(hours=9, minutes=1)).strftime("%Y%m%d%H%M") + ".profile"
                        PROFILE_FILEFULLNAME = getPROFILE_FILEFULLNAME(START______TIME)

                excuteTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
                if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
                    os.system("../filebeat/filebeat-6.4.2-darwin-x86_64/filebeat --once -e -c " + "sys/filebeat_6.4.2_darwin.yml")
                elif _platform == "win32" or _platform == "win64":
                    # os_systemEx("..\\filebeat\\filebeat-6.1.3-windows-x86_64\\filebeat.exe --once -e -c " + "sys\\filebeat.yml")
                    #os.system("..\\filebeat\\filebeat-6.1.3-windows-x86_64\\filebeat.exe --once -e -c " + "sys\\filebeat.yml")
                    #os.system("..\\filebeat\\filebeat-6.3.2-windows-x86_64\\filebeat.exe --once -e -c " + "sys\\filebeat_6.3.2.yml")
                    os.system("..\\filebeat\\filebeat-6.4.0-windows-x86_64\\filebeat.exe --once -e -c " + "sys\\filebeat_6.4.0.yml")
                print("%s-%s." % ("awake", excuteTime)),
            else:
                print(str(sleepTime) + "sec-sleeping."),

        time.sleep(sleepTime)

        if AUTOMODE == False:
            break