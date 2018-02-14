# -*- coding: utf-8 -*-
#!/usr/bin/python
import datetime
import threading

from common.deviceInfo import *
from common.utils import *
from xml.etree.ElementTree import parse

SHARD_PREFENCES = "com.skt.trtc.sample_preferences.xml"
MP4_SAVEFOLDER = 'B:\\_MT\\'
#MP4_SAVEFOLDER = 'B:\\stub\\'
TIME_LIMIT = 120
pids = []
setDEBUG(True)

class FuncThread(threading.Thread):
    def __init__(self, run_event, target, *args):
        printEx("%s:%s\n" % (id, "__init__ in thread"))
        self.__started = run_event
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        printEx("%s:%s\n" % (id, "run in thread"))
        self._target(*self._args)

def getShardPreference(xmlFileName, tagName, key):
    reVal = None
    tree = parse(xmlFileName)
    preferences = tree.getroot()
    for item in preferences.iter(tagName):
        if key == item.attrib.get("name"):
            reVal = item.text.replace(" ", "")
            break

    return reVal

connectIds = getRealDevices()

if len(connectIds) != 2:
    if len(connectIds) > 2 or len(connectIds) == 0:
        printError("len(connectIds) is " + str(len(connectIds)) + '! But, that is not available!')
        exit(0)

    raw_input('connected device\'s num is ' + str(len(connectIds)) + '! Is it right?[enter]')


if len(connectIds) == 1:
    TIME_LIMIT = 180
printEx("[%s:%s]" % ("TIME_LIMIT", TIME_LIMIT))
time.sleep(3)

resultSingleFileNameS = dict()

for id in connectIds:
    if os.path.isfile(SHARD_PREFENCES):
        os.remove(SHARD_PREFENCES)

    phoneNumber = getPhoneNumberFromDevice(id)
    printEx("[%s:%s]" % ("phoneNumber", phoneNumber))
    manufacture = getManufacturerFromDevice(id)
    printEx("[%s:%s]" % ("manufacture", manufacture))
    board = getBoardFromDevice(id)
    printEx("[%s:%s]" % ("board", board))
    abi = getAbiFromDevice(id)
    printEx("[%s:%s]" % ("abi", abi))
    model = getModelNameFromDevice(id)
    printEx("[%s:%s]" % ("model", model))
    osversion = getOSVersionFromDevice(id)
    printEx("[%s:%s]" % ("osversion", osversion))
    addtionalFactors = None
    try:
        os.system("adb -s " + id + " root")
        os.system("adb -s " + id + " pull " + "/data/data/com.skt.trtc.sample/shared_prefs/com.skt.trtc.sample_preferences.xml")
        if os.path.isfile(SHARD_PREFENCES) == False:
            raise Exception('NOTFOUND', SHARD_PREFENCES)
        trtc_video_quality_resol = getShardPreference("com.skt.trtc.sample_preferences.xml", "string", "trtc_video_quality_resol")
        if trtc_video_quality_resol == None:
            printError("%s[%s:%s]" % (id, "trtc_video_quality_resol", trtc_video_quality_resol))
            exit(0)
        trtc_video_quality_fps = getShardPreference("com.skt.trtc.sample_preferences.xml", "string", "trtc_video_quality_fps")
        if trtc_video_quality_fps == None:
            printError("%s[%s:%s]" % (id, "trtc_video_quality_fps", trtc_video_quality_fps))
            exit(0)
        trtc_video_quality_max_bitrate = getShardPreference("com.skt.trtc.sample_preferences.xml", "string", "trtc_video_quality_max_bitrate")
        if trtc_video_quality_max_bitrate == None:
            printError("%s[%s:%s]" % (id, "trtc_video_quality_max_bitrate", trtc_video_quality_max_bitrate))
            exit(0)
        #addtionalFactors start
        trtc_perform_videoframehooker_pixcelformat = getShardPreference("com.skt.trtc.sample_preferences.xml", "string",
                                                                        "trtc_perform_videoframehooker_pixcelformat")
        if trtc_perform_videoframehooker_pixcelformat == None:
            printError("%s[%s:%s]" % (
                id, "trtc_perform_videoframehooker_pixcelformat", trtc_perform_videoframehooker_pixcelformat))
        else:
            addtionalFactors = '-' + trtc_perform_videoframehooker_pixcelformat

        trtc_perform_videoframehooker_1_normalizedmaxwidthlandscape = getShardPreference(
            "com.skt.trtc.sample_preferences.xml", "string",
            "trtc_perform_videoframehooker_1_normalizedmaxwidthlandscape")
        if trtc_perform_videoframehooker_1_normalizedmaxwidthlandscape == None:
            printError("%s[%s:%s]" % (
                id, "trtc_perform_videoframehooker_1_normalizedmaxwidthlandscape",
                trtc_perform_videoframehooker_1_normalizedmaxwidthlandscape))
        else:
            addtionalFactors = addtionalFactors + '_' + trtc_perform_videoframehooker_1_normalizedmaxwidthlandscape

        trtc_perform_videoframehooker_2_normalizedmaxwidthlandscape_4dlib = getShardPreference(
            "com.skt.trtc.sample_preferences.xml", "string",
            "trtc_perform_videoframehooker_2_normalizedmaxwidthlandscape_4dlib")
        if trtc_perform_videoframehooker_2_normalizedmaxwidthlandscape_4dlib == None:
            printError("%s[%s:%s]" % (id, "trtc_perform_videoframehooker_2_normalizedmaxwidthlandscape_4dlib", trtc_perform_videoframehooker_2_normalizedmaxwidthlandscape_4dlib))
            addtionalFactors = None
        else:
            addtionalFactors = addtionalFactors + '_' + trtc_perform_videoframehooker_2_normalizedmaxwidthlandscape_4dlib

    except:
        printError(sys.exc_info()[0], sys.exc_info()[1])
        trtc_video_quality_resol = "g1280x720"
        #trtc_video_quality_resol = "g640x480"
        trtc_video_quality_fps="g24"
        trtc_video_quality_max_bitrate="g1800"

    resultSingleFileNameS[id] = manufacture + "_" + board + "_" + abi + "_" + model + "_" + osversion + "_" + trtc_video_quality_resol + "_" + trtc_video_quality_fps + "_" + trtc_video_quality_max_bitrate
    if addtionalFactors != None:
        printEx("%s:%s" % ("addtionalFactors", addtionalFactors))
        resultSingleFileNameS[id] = resultSingleFileNameS[id] + addtionalFactors
    printEx("%s:%s" % ("resultSingleFileNameS[id]", resultSingleFileNameS[id]))

resultPairFileNameS = dict()
START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")

if len(connectIds) == 2:
    for me in connectIds:
        myName = resultSingleFileNameS[me]
        #resultPairFileNameS[me] = "me[" + myName + "]" + "_" + START______TIME + ".mp4"
        for you in connectIds:
            if me != you:
                resultPairFileNameS[me] = "me[" + myName + "]you[" + resultSingleFileNameS[you] + "]" + "_" + START______TIME + ".mp4"
                break
else:
    for me in connectIds:
        myName = resultSingleFileNameS[me]
        resultPairFileNameS[me] = "single[" + myName + "]_" + START______TIME + ".mp4"

"""Bit rate 128000000bps outside acceptable range [100000,100000000]"""
outside_acceptable_range_128000000bps = [
    "SHV-E250",
    "SM-A500",
]
def someOtherFunc(device_id, model, tLimit, filename):
    global pids
    global commands
    global ERRO_DETECT
    global FINISH_COUNT
    fLowBitrate = False
    for abnormalModel in outside_acceptable_range_128000000bps:
        if abnormalModel in model:
            fLowBitrate = True

    if fLowBitrate :
        #os.system("adb -s " + device_id + " shell screenrecord --verbose --bit-rate 100000000 --time-limit " + str(tLimit) + " /sdcard/" + filename)
        proc = subprocess.Popen("adb -s " + device_id + " shell screenrecord --verbose --bit-rate 100000000 --time-limit " + str(tLimit) + " /sdcard/" + filename, stdout=subprocess.PIPE)
        command = "adb -s " + device_id + " shell screenrecord --verbose --bit-rate 100000000 --time-limit " + str(tLimit) + " /sdcard/" + filename
        printEx(command)
    else:
        #os.system("adb -s " + device_id + " shell screenrecord --verbose --bit-rate 128000000 --time-limit " + str(tLimit) + " /sdcard/" + filename)
        proc = subprocess.Popen("adb -s " + device_id + " shell screenrecord --verbose --bit-rate 128000000 --time-limit " + str(tLimit) + " /sdcard/" + filename, stdout=subprocess.PIPE)
        command = "adb -s " + device_id + " shell screenrecord --verbose --bit-rate 128000000 --time-limit " + str(tLimit) + " /sdcard/" + filename
        printEx(command)

    pids.append(proc.pid)
    fd_popen = proc.stdout
    content = fd_popen.read().strip()
    try:
        commands[device_id] = list()
        for line in content.split('\r\n'):
            printEx("%s:%s\n" % (device_id, line))
            commands[device_id].append(line)
            if "outside acceptable range" in line:
                raise Exception('ERRO_DETECT', 'DETECT')
    except:
        ERRO_DETECT = True
    finally:
        commands[device_id].append(command)
        FINISH_COUNT = FINISH_COUNT + 1



threadPool = {}
threadLock = threading.Lock()
run_event = threading.Event()
run_event.set()
commands = {}
FINISH_COUNT = 0
WAIT_SEC = 0

for id in connectIds:
    thread = FuncThread(run_event, someOtherFunc, id, getModelNameFromDevice(id), TIME_LIMIT, resultPairFileNameS[id])
    threadPool[id] = thread

ERRO_DETECT = False

for id in connectIds:
    printEx("%s:%s\n" % (id, "thread-start-call-start"))
    threadPool[id].start()
    printEx("%s:%s\n" % (id, "thread-start-call-end__"))

print "Exiting Main Thread"

ids = threadPool.keys()
for id in ids:
    if threadPool[id].isAlive() == False:
        ERRO_DETECT = True

while ERRO_DETECT == False and FINISH_COUNT < len(connectIds):
    time.sleep(1)
    WAIT_SEC = WAIT_SEC + 1
    printEx("%s:%s // %s:%s" % ('WAIT_SEC', WAIT_SEC, 'FINISH_COUNT', FINISH_COUNT))

if ERRO_DETECT == False:
    for id in ids:
        printEx("%s:%s" % (id, "waiting"))
        threadPool[id].join()
        del threadPool[id]

if len(connectIds) != len(getDevices()):
    printEx("any of Device is disconnected!")
    ERRO_DETECT = True

for pid in pids:
    os.system("taskkill /F /PID " + str(pid))
    printEx("taskkill /F /PID " + str(pid))

for id in connectIds:
    if ERRO_DETECT == False:
        os.system("adb -s " + id + " pull " + "/sdcard/" + resultPairFileNameS[id] + " " + MP4_SAVEFOLDER)
    os.system("adb -s " + id + " shell rm -f " + "/sdcard/" + resultPairFileNameS[id])
for key in commands.keys():
    for command in commands[key]:
        if ERRO_DETECT == False:
            printEx("%s-->%s:%s" % (key, command, "success!"))
        else:
            printEx("%s-->%s:%s" % (key, command, "fail!"))
if ERRO_DETECT:
    printEx("%s:%s" % ('ERROR', "DETECT"))
else:
    printEx("%s:%s" % ('ERROR', "NONE"))

exit(0)

for i in resultPairFileNameS:
    print i, resultPairFileNameS[i]

printEx("%s:%s" % ("trtc_video_quality_resol", getShardPreference("com.skt.trtc.sample_preferences.xml", "string", "trtc_video_quality_resol")))
printEx("%s:%s" % ("trtc_video_quality_fps", getShardPreference("com.skt.trtc.sample_preferences.xml", "string", "trtc_video_quality_fps")))
printEx("%s:%s" % ("trtc_video_quality_max_bitrate", getShardPreference("com.skt.trtc.sample_preferences.xml", "string", "trtc_video_quality_max_bitrate")))


time.sleep(5)



#screenrecord --verbose --bit-rate 64000000 --time-limit 10 /sdcard/demo_240.mp4

#/data/data/com.skt.trtc.sample/shared_prefs/com.skt.trtc.sample_preferences.xml