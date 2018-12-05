#!/usr/bin/python  
# -*- coding: utf-8 -*-
import os, stat, glob, sys
from os import walk
import subprocess, os, signal
import shutil
from dateutil import parser
import datetime
import codecs
import threading
from sys import platform as _platform
from common.deviceInfo import *
from common.utils import *

reload(sys)
sys.setdefaultencoding('utf-8')

def InterruptableEvent():
    e = threading.Event()

    def patched_wait():
        while not e.is_set():
            e._wait(3)

    e._wait = e.wait
    e.wait = patched_wait
    return e

def kill_meAndchild_processes(pid, sig=signal.SIGTERM):
        ps_command = subprocess.Popen("ps -e -o pid -o ppid -o command | grep %d" % pid, shell=True, stdout=subprocess.PIPE)
        ps_output = ps_command.stdout.read()
        retcode = ps_command.wait()
        assert retcode == 0, "ps command returned %d" % retcode
        for line in ps_output.split("\n")[:-1]:
            if 'ps -e -o pid -o ppid -o command' not in line and "grep" not in line:
                iPid = int(line.split(' ')[0])
                print("%s:%s" % ('iPid', iPid))
                os.kill(iPid, sig)

if __name__ == "__main__":
    START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    procs = []
    tcpdumpfiles = {}
    SAVEDIR = '/Users/oms1226/_log'
    CUSTOM_NAME = ''
    myName = sys.argv[0].split('/')[-1].split('.')[0]
    print("%s:%s" % ("myName", myName))
    while len(sys.argv) > 1:
        if len(sys.argv) > 1 and '--where' in sys.argv[1]:
            argfullname = sys.argv[1].split('=')
            if len(argfullname) == 2:
                if argfullname[0] == '--where':
                    SAVEDIR = argfullname[1]
            sys.argv.pop(1)
        elif len(sys.argv) > 1 and '--name' in sys.argv[1]:
            argfullname = sys.argv[1].split('=')
            if len(argfullname) == 2:
                if argfullname[0] == '--name':
                    CUSTOM_NAME = argfullname[1]
            sys.argv.pop(1)
        else:
            sys.argv.pop(1)
    print("%s:%s" % ('SAVEDIR', SAVEDIR))
    print("%s:%s" % ('CUSTOM_NAME', CUSTOM_NAME))
    connectIds = getRealDevices()
    if CUSTOM_NAME == '':
        TARGET_DIR = SAVEDIR + "/" + myName + "_" + START______TIME
    else:
        TARGET_DIR = SAVEDIR + "/" + myName + "_" + START______TIME + "_" + CUSTOM_NAME
    if len(connectIds) > 0:
        if not os.path.exists(TARGET_DIR):
            os.makedirs(TARGET_DIR)

    for deviceID in connectIds:
        os.system('adb -s ' + deviceID + " root")
        phoneNumber = getPhoneNumberFromDevice(deviceID)
        printEx("[%s:%s]" % ("phoneNumber", phoneNumber))
        manufacture = getManufacturerFromDevice(deviceID)
        printEx("[%s:%s]" % ("manufacture", manufacture))
        board = getBoardFromDevice(deviceID)
        printEx("[%s:%s]" % ("board", board))
        abi = getAbiFromDevice(deviceID)
        printEx("[%s:%s]" % ("abi", abi))
        model = getModelNameFromDevice(deviceID)
        printEx("[%s:%s]" % ("model", model))
        osversion = getOSVersionFromDevice(deviceID)
        printEx("[%s:%s]" % ("osversion", osversion))
        filenamePrefix = START______TIME + "_" + phoneNumber + "_" + manufacture + "_" + board + "_" + abi + "_" + model + "_" + osversion
        os.system('adb -s ' + deviceID + " logcat -c")
        logfilename = TARGET_DIR + '/' + filenamePrefix + '_LOGCAT.log'
        proc = subprocess.Popen(("adb -s " + deviceID + " logcat -v threadtime > " + logfilename), shell=True)
        print("%s:%s" % ('proc.pid', proc.pid))
        procs.append(proc)
        pcapfilename = filenamePrefix + '_TCPDUMP.pcap'
        proc = subprocess.Popen(("adb -s " + deviceID + " shell tcpdump -i any -p -s 0 -w /sdcard/" + pcapfilename), shell=True)
        print("%s:%s" % ('proc.pid', proc.pid))
        procs.append(proc)
        tcpdumpfiles[deviceID] = '/sdcard/' + pcapfilename

    #time.sleep(10)
    event = InterruptableEvent()
    try:
        event.wait()
    except KeyboardInterrupt:
        print "Received KeyboardInterrupt"

    for proc in procs:
        kill_meAndchild_processes(proc.pid)

    for deviceID in connectIds:
        os.system('adb -s ' + deviceID + ' pull ' + tcpdumpfiles[deviceID] + ' ' + TARGET_DIR + '/')
        os.system('adb -s ' + deviceID + ' shell rm -rf ' + tcpdumpfiles[deviceID])







if False:
        procs.append(proc)
        args = {}
        args["DEVICE_ID"] = deviceID
        args["tag"] = 'ALL'
        args["logfullfilename"] = "/Users/oms1226/_log/logcatAndtcpdump" + "_" + str(10) + ".log"
        print("%s:%s" % ('logfullfilename', args["logfullfilename"]))
        time.sleep(10)
        LOGPROCESS, LOGINFO = getProc4LogCat(**args)
        time.sleep(10)
        print("%s:%s" % ('LOGPROCESS', LOGPROCESS))
        print("%s:%s" % ('LOGINFO', LOGINFO))






