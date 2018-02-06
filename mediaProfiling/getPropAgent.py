# -*- coding: utf-8 -*-
#!/usr/bin/python
import datetime
import threading

from common.contant import *
from common.deviceInfo import *

setDEBUG(False)

JSON_LOCAL_FILE = None
INFO_FILEFULLNAME = "data\\modelInfo4getprop.data"
HASHKEY_FILEFULLNAME = "data\\modelInfo4getprop.hashkey"
MIN_SLEEPTIME = 60
MAX_SLEEPTIME = 15 * 60

def getPropRefinded4ELK(deviceId):
    global JSON_LOCAL_FILE
    if JSON_LOCAL_FILE == None:
        property = getPropFromDevice(DEVICE_ID)
    else:
        property = JSON_LOCAL_FILE
    for key in property.keys():
        if key in property.keys():
            for searchKey in property.keys():
                if key in searchKey and searchKey != key:
                    del property[searchKey]
                    printEx("%s:%s --> %s" % ("del", searchKey, 'due to ' + key))

    printEx("%s:%s" % ("len(property)", len(property)))
    return property

def getHashkeyThisDevice4ELK(deviceId):
    global JSON_LOCAL_FILE
    needFields = [
        "ro.product.manufacturer",
        "ro.product.model",
        "ro.product.board",
        "ro.board.platform",
        "ro.hardware",
        "ro.boot.hardware",
        "ro.chipname",
        "ro.arch",
        "ro.product.cpu.abi",
        "ro.build.version.release",
        "ro.build.version.sdk",
    ]

    hashKey = str(len(needFields))
    for field in needFields:
        if JSON_LOCAL_FILE == None:
            reVal =  getValueFromDevice(deviceId, field)
        else:
            try:
                reVal =  JSON_LOCAL_FILE[field].replace(' ', '')
            except KeyError:
                printError("Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1])
        if reVal == None:
            reVal = 'None'
        hashKey = hashKey + '_' + reVal

    printEx("%s:%s" % ("hashKey", hashKey))

    return hashKey
"""
기 수집된 파일을 재 파싱하여 원하는 형태로 다시 재조립할 때 사용했다. 20180205
localFileSelfProcess("C:\\lmcft_log\\common\\modelInfo4getprop.log")
exit(0)
"""
def localFileSelfProcess(fileName):
    global JSON_LOCAL_FILE
    if os.path.exists(fileName):
        with open(fileName) as f:
            lines = f.readlines()
    else:
        lines = []

    for line in lines:
        JSON_LOCAL_FILE = json.loads(line)

        if os.path.exists(HASHKEY_FILEFULLNAME):
            with open(HASHKEY_FILEFULLNAME) as f:
                hashKeys = f.readlines()
        else:
            hashKeys = []

        fGetInfo = True
        hashKey = getHashkeyThisDevice4ELK(None)
        printEx("%s:%s" % ("hashKey", hashKey))

        for pastKey in hashKeys:
            if hashKey in pastKey:
                fGetInfo = False
                break

        printEx("%s:%s" % ("fGetInfo", fGetInfo))

        if fGetInfo:
            with codecs.open(HASHKEY_FILEFULLNAME, 'a', 'utf-8') as f:
                f.write(json.dumps(hashKey, ensure_ascii=False) + "\r\n")
                f.close()

            getprop = getPropRefinded4ELK(None);
            printEx("%s:%s" % ("type(reVal)", type(getprop)))
            if os.path.exists("data") == False:
                mkdirs("data")

            with codecs.open(INFO_FILEFULLNAME, 'a', 'utf-8') as f:
                f.write(json.dumps(getprop, ensure_ascii=False) + "\r\n")
                f.close()
"""
아래를 pythonpath를 추가
  C:\_python\workspace\PycharmProjects\pyTest4AndroidonGithub
python C:\_python\workspace\PycharmProjects\pyTest4AndroidonGithub\mediaProfiling\getPropAgent.py -a
"""
if __name__ == "__main__":
    AUTOMODE = False
    while len(sys.argv) > 1:
        if len(sys.argv) > 1 and '-a' in sys.argv[1]:
            AUTOMODE = True
            sys.argv.pop(1)

    printEx("%s:%s" % ("AUTOMODE", AUTOMODE))
    connected_Devices = []
    sleepTime = MIN_SLEEPTIME
    while True:
        connectingDevices = getRealDevices()
        if os.path.exists(HASHKEY_FILEFULLNAME):
            with open(HASHKEY_FILEFULLNAME) as f:
                hashKeys = f.readlines()
        else:
            hashKeys = []

        #printEx("%s:%s" % ("hashKeys", hashKeys))
        if set(connected_Devices) == set(connectingDevices):
            print(str(sleepTime) + "sec-sleeping."),
            time.sleep(sleepTime)
            sleepTime = sleepTime + MIN_SLEEPTIME
            if sleepTime > MAX_SLEEPTIME:
                sleepTime = MAX_SLEEPTIME
        else:
            connected_Devices = connectingDevices
            sleepTime = MIN_SLEEPTIME
            for DEVICE_ID in connected_Devices:
                try:
                    printEx("%s:%s" % ("DEVICE_ID", DEVICE_ID))
                    fGetInfo = True
                    hashKey = getHashkeyThisDevice4ELK(DEVICE_ID)
                    for pastKey in hashKeys:
                        if hashKey in pastKey:
                            fGetInfo = False
                            break

                    printEx("%s:%s" % ("fGetInfo", fGetInfo))

                    if fGetInfo:
                        with codecs.open(HASHKEY_FILEFULLNAME, 'a', 'utf-8') as f:
                            f.write(json.dumps(hashKey, ensure_ascii=False) + "\r\n")
                            f.close()

                        getprop = getPropRefinded4ELK(DEVICE_ID);
                        printEx("%s:%s" % ("type(reVal)", type(getprop)))
                        if os.path.exists("data") == False:
                            mkdirs("data")

                        with codecs.open(INFO_FILEFULLNAME, 'a', 'utf-8') as f:
                            f.write(json.dumps(getprop, ensure_ascii=False) + "\r\n")
                            f.close()

                        os.system("..\\filebeat\\filebeat-6.1.3-windows-x86_64\\filebeat.exe --once -e -c " + "sys\\filebeat.yml")
                except:
                    printError("Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1])
                finally:
                    excuteTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
                    print("%s-%s." % ("awake", excuteTime)),

        if AUTOMODE == False:
            break