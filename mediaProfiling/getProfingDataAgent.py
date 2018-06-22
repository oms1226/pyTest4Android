# -*- coding: utf-8 -*-
#!/usr/bin/python
import datetime
import threading

from common.contant import *
from common.deviceInfo import *
from os import walk


MIN_SLEEPTIME = 60
MAX_SLEEPTIME = 15 * 60
START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
PROFILE_FILEFULLNAME = "data\\trtc_" + START______TIME + ".profile"
PROFILE_RAW_FILEFOLDER = "rawdata"
setDEBUG(True)

Trtr_Target_fileName_Subfixs = [
    "_trtc.profile",
    "_trtc.setting",
]

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
            for (dirpath, dirnames, rawFilenames) in walk(PROFILE_RAW_FILEFOLDER):
                printEx("%s:%s" % ("dirpath", dirpath))
                printEx("%s:%s" % ("dirnames", dirnames))
                printEx("%s:%s" % ("rawFilenames", rawFilenames))
                break
            if len(rawFilenames) > 0:
                for rawFilename in rawFilenames:
                    rawFullFilename = PROFILE_RAW_FILEFOLDER + "\\" + rawFilename
                    if os.path.isfile(rawFullFilename):
                        with open(rawFullFilename) as f:
                            while True:
                                line = f.readline().replace('\r', '').replace('\n', '')
                                if not line: break
                                RawDatas.append(line)
                            f.close()
                        os.remove(rawFullFilename)

            for id in getRealDevices():
                for Trtr_Target_fileName_Subfix in Trtr_Target_fileName_Subfixs:
                    Trtr_Profiling_fileName = getModelNameFromDevice(id) + Trtr_Target_fileName_Subfix
                    if os.path.isfile(Trtr_Profiling_fileName):
                        os.remove(Trtr_Profiling_fileName)

                    os.system("adb -s " + id + " pull " + "/sdcard/trtc_logs/" + Trtr_Profiling_fileName)

                    if os.path.isfile(Trtr_Profiling_fileName):
                        os.system("adb -s " + id + " shell rm -f " + "/sdcard/trtc_logs/" + Trtr_Profiling_fileName)
                        with open(Trtr_Profiling_fileName) as f:
                            while True:
                                line = f.readline().replace('\r', '').replace('\n', '')
                                if not line: break
                                RawDatas.append(line)
                            f.close()
                        os.remove(Trtr_Profiling_fileName)
        except:
            printError("Main Logic Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1])
        finally:
            if len(RawDatas) > 0:
                for RawData in RawDatas:
                    RawDataJson = json.loads(RawData)
                    """
                  71b17b3ae41bc256f43da5d666d63d36a16f1ea7
                  0.8.0[1236/d15b794d54348969b8e9021aaee2840dc1adbb08]
                  """
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
                        trtc_git_hashcode = trtc_git_hashcode.replace(']', '')
                    elif '/' in trtc_version:
                        trtc_git_revcnt = int(trtc_version.split('/')[0])
                        trtc_git_hashcode = ''.join(trtc_version.split('/')[1:])
                    else:
                        trtc_git_hashcode = trtc_version

                    if '/' in trtc_git_hashcode:
                        trtc_git_hashcode = trtc_git_hashcode.split('/')[0]
                        trtc_build_pc = ''.join(trtc_git_hashcode.split('/')[1:])
                    if '/' in trtc_build_pc:
                        trtc_build_pc = trtc_git_hashcode.split('/')[0]
                        trtc_build_time = ''.join(trtc_git_hashcode.split('/')[1:])

                    RawDataJson['trtc_version_name'] = trtc_version_name
                    RawDataJson['trtc_git_hashcode'] = trtc_git_hashcode
                    RawDataJson['trtc_git_revcnt'] = trtc_git_revcnt
                    RawDataJson['trtc_build_pc'] = trtc_build_pc
                    RawDataJson['trtc_build_time'] = trtc_build_time
                    with codecs.open(PROFILE_FILEFULLNAME, 'a', 'utf-8') as f:
                        f.write(json.dumps(RawDataJson, ensure_ascii=False) + "\r\n")
                        f.close()

                excuteTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
                # os_systemEx("..\\filebeat\\filebeat-6.1.3-windows-x86_64\\filebeat.exe --once -e -c " + "sys\\filebeat.yml")
                os.system(
                    "..\\filebeat\\filebeat-6.1.3-windows-x86_64\\filebeat.exe --once -e -c " + "sys\\filebeat.yml")
                print("%s-%s." % ("awake", excuteTime)),
            else:
                print(str(sleepTime) + "sec-sleeping."),

        time.sleep(sleepTime)

        if AUTOMODE == False:
            break