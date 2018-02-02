# -*- coding: utf-8 -*-
#!/usr/bin/python

import datetime
import threading

from CallRecordingTest.pyCallRecordingTestThread import pyCallRecordingTestThread
from common.deviceInfo import *
from common.utils import *


"""
settings
1)PYTHONPATH 설정
2)pip install SpeechRecognition
3)pip install requests
"""
"""
1)T전화 기본전화로 설정, 화면 세로모드(??), 무음(??)
2)통화 자동 녹음 설정, 작은 수신화면 해제
3)소리샘 비밀번호 0918 설정
4)ADB 연결 확인
C:\_python\workspace\PycharmProjects\lmcst\CallRecordingTest>python pyCallRecordingTestMultiThread.py -a -m 60 -v oms1226
"""
threadLock = threading.Lock()
threadPool = []
AUTOMODE = False

during_mins = 11
LOG_COVERAGE='narrow'
MONKEY = False
FIX_DEVICEID = None
DEMANDS = {}
OPTIONS = {}
#com.nll.acr
PACKGENAME = 'com.skt.prod.dialer'

mkdirs(LMCFT_EXEC_HISTORY)
with open(LMCFT_EXEC_HISTORY, 'a') as f:
    CURRENTGMT9TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y.%m%d.%H:%M:%S")
    f.write(CURRENTGMT9TIME + '> python ' + ' '.join(sys.argv) + "\r\n")
    f.close()

while len(sys.argv) > 1:
    if len(sys.argv) > 1 and '-a' in sys.argv[1]:
        AUTOMODE = True
        sys.argv.pop(1)

    if len(sys.argv) > 1 and '-m' in sys.argv[1]:
        sys.argv.pop(1)
        during_mins = int(sys.argv.pop(1))
    elif len(sys.argv) > 1 and '-h' in sys.argv[1]:
        sys.argv.pop(1)
        during_mins = int(sys.argv.pop(1))*60

    if len(sys.argv) > 1 and '-v' in sys.argv[1]:
        sys.argv.pop(1)
        LOG_COVERAGE = sys.argv.pop(1)

    if len(sys.argv) > 1 and '-monkey' in sys.argv[1]:
        MONKEY = True
        sys.argv.pop(1)

    if len(sys.argv) > 1 and '-debug' in sys.argv[1]:
        setDEBUG(True)
        sys.argv.pop(1)

    if len(sys.argv) > 1 and '-id' in sys.argv[1]:
        sys.argv.pop(1)
        FIX_DEVICEID = sys.argv.pop(1)

    if len(sys.argv) > 1 and '-p' in sys.argv[1]:
        sys.argv.pop(1)
        PACKGENAME = sys.argv.pop(1)

    if len(sys.argv) > 1 and '-demand' in sys.argv[1]:
        sys.argv.pop(1)
        """
       startActivity:com.google.android.googlequicksearchbox/.SearchActivity
       keyValue = "startActivity:com.google.android.googlequicksearchbox/.SearchActivity"
       """
        keyValue = sys.argv.pop(1)
        DEMANDS[keyValue.split(':')[0]] = keyValue.split(':')[1]

    if len(sys.argv) > 1 and '-logcat' in sys.argv[1]:
        sys.argv.pop(1)
        OPTIONS['LOGCAT'] = True
        if len(sys.argv) > 1 and 'tag:' in sys.argv[1]:
            tag = sys.argv.pop(1)
            OPTIONS['TAG'] = tag.split(':')[1]
        if len(sys.argv) > 1 and 'searchword:' in sys.argv[1]:
            word = sys.argv.pop(1)
            OPTIONS['SEARCHWORD'] = word.split(':')[1]
        if len(sys.argv) > 1 and 'reportNum:' in sys.argv[1]:
            word = sys.argv.pop(1)
            OPTIONS['reportNum'] = word.split(':')[1]

print("%s:%s" % ("AUTOMODE", AUTOMODE))
print("%s:%s" % ("during_mins", during_mins))
print("%s:%s" % ("LOG_COVERAGE", LOG_COVERAGE))
print("%s:%s" % ("selfVersion", selfVersion))
print("%s:%s" % ("MONKEY", MONKEY))
print("%s:%s" % ("DEBUG()", DEBUG()))
print("%s:%s" % ("FIX_DEVICEID", FIX_DEVICEID))
print("%s:%s" % ("DEMANDS", DEMANDS))
print("%s:%s" % ("OPTIONS", OPTIONS))
print("%s:%s" % ("PACKGENAME", PACKGENAME))

threadPool = {}
completeLog = []
num = 0
printTime = 0
try:
    run_event = threading.Event()
    run_event.set()
    while True:
        test_list = {}

        time.sleep(5)
        connectIds = getRealDevices()
        for index, id in enumerate(completeLog):
            if id not in connectIds:
                print("%s:%s" % (id, "disconnected!")),
                del completeLog[index]

        for id in connectIds:
            phoneNumber = getPhoneNumberFromDevice(id)
            printEx("%s:%s" % (id, phoneNumber))
            if phoneNumber != None:
                if FIX_DEVICEID == id:
                    test_list[id] = phoneNumber
                elif FIX_DEVICEID == None:
                    test_list[id] = phoneNumber
            else:
                print("%s:%s" % (id, "phoneNumber->None")),

        for i, id in enumerate(test_list.keys()):
            if id not in threadPool.keys() and id not in completeLog:
                thread = pyCallRecordingTestThread(run_event, selfVersion, num, "Thread-" + str(num), id, test_list[id], PACKGENAME,
                                                   None, during_mins, LOG_COVERAGE, MONKEY, DEMANDS, **OPTIONS)
                num = num + 1
                thread.start()
                threadPool[thread.DEVICE_ID] = thread

        time.sleep(5)

        ids = threadPool.keys()
        for id in ids:
            if threadPool[id].isAlive() == False:
                print("%s:%s" % (threadPool[id].MODEL, "idle"))
                completeLog.append(id)
                del threadPool[id]
            else:
                pass
                #print("%s:%s" % (threadPool[id].MODEL, "running"))

        if len(threadPool) == 0:
            #print("All Threads are idle!."),
            time.sleep(15)
            print("."),

        if AUTOMODE == False:
            break
except KeyboardInterrupt:
    run_event.clear()
    printEx( "main KeyboardInterrupt!")

# Wait for all threadPool to complete
for t in threadPool.values():
    t.join()

print "Exiting Main Thread"
exit(0)

DEVICE_ID = "ce041604d87a073904"
DEVICE_ID = "LGF500S6f49b473"

if DEVICE_ID not in getDevices():
    print "%s:%s is not in lists" % ("DEVICE_ID", DEVICE_ID)
    exit(0)
