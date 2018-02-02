import os

import psutil
import subprocess

import time

import sys

from common.utils import printError, getExceptionString, execCmdBackground, os_systemEx

if __name__ == "__main__":
    if os.path.isfile('requirements.txt') == True:
        os.system('pip install -r requirements.txt')
        #os_systemEx('pip install -r requirements.txt')

    isFilebeat = False
    for process in [p.name() for p in psutil.process_iter()]:
        if 'filebeat' in process:
            isFilebeat = True
    print("%s:%s" % ('isFilebeat', isFilebeat))
    if isFilebeat == False:
        CURRENT_PATH = os.getcwd()
        os.chdir('filebeat\\filebeat-5.6.3-windows-x86_64')
        execCmdBackground('filebeat -e -c filebeat.yml')
        os.chdir(CURRENT_PATH)
    print("%s:%s" % ('isEnd', 'True'))