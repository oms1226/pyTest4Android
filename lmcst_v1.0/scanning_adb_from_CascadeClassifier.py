import numpy as np
import cv2
import os
import sys
import time
from time import gmtime, strftime
import random
import subprocess
from pandas import Series, DataFrame
import datetime
from sys import platform as _platform

"""
print len(set([1,2,3,4,5]).intersection(set([1,2,3,4,5])))
sys.exit()

raw_data = {'col0': [1, 2, 3, 4],
            'col1': [10, 20, 30, 40],
            'col2': [100, 200, 300, 400]}

date = ['16.02.29', '16.02.26', '16.02.25', '16.02.24']
data = DataFrame(raw_data, index=date)

print(data)

raw_data1 = {'col0': [5],
            'col1': [50],
            'col2': [500]}
date = ['16.02.24']
data = data.append(DataFrame(raw_data1, index=date))
print(data)
sys.exit()
"""

dataFrame = DataFrame({}, index=[])
def getCurrentActivity():
    cmd = ['adb', '-s', deviceID, 'shell', 'dumpsys', 'window', 'windows']
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    #data = fd_popen.read().strip()
    reVal = None
    currentFocus = None
    lineCnt = 0
    while 1:
        line = fd_popen.readline()
        if not line:
            break
        if "mFocusedApp" in str(line) :
            reVal = str(line).strip("\r").strip("\n").strip()

        if "mCurrentFocus" in str(line) :
            currentFocus = str(line).strip("\r").strip("\n").strip()

        lineCnt = lineCnt + 1
    fd_popen.close()

    if reVal != None :
        if "/" in reVal:
            reVal = reVal.split(" ")[4].replace("}", "").replace("/", "")
        else:
            reVal = reVal.replace("}", "")

        if currentFocus != None:
            if "." in currentFocus:
                currentFocus = currentFocus.split(".")[-1].replace("}", "")
            else:
                currentFocus = currentFocus.split(" ")[-1].replace("}", "")

            currentFocus = currentFocus.split(":")[0]
        else:
            currentFocus = ""

        winCount = getWindowCount()
        reVal = reVal + "_win#" + str(winCount) + "_total#" + str(lineCnt) + "_" + str(currentFocus)

    return reVal

def getWindowSize():
    cmd = ['adb', '-s', deviceID, 'shell', 'wm', 'size']
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    #data = fd_popen.read().strip()
    reVal = None
    while 1:
        line = fd_popen.readline()
        if not line:
            break
        if "Physical size:" in str(line) :
            reVal = str(line).strip("Physical size:").strip("\r").strip("\n").strip()
            break
    fd_popen.close()

    if reVal != None :
        reVal_X = reVal.split("x")[0]
        reVal_Y = reVal.split("x")[1]

    return int(reVal_X), int(reVal_Y)

def getWindowCount():
    cmd = ['adb', '-s', deviceID, 'shell', 'dumpsys', 'window', 'windows']
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    #data = fd_popen.read().strip()
    reVal = 0
    while 1:
        line = fd_popen.readline()
        if not line:
            break
        if "Window #" in str(line) :
            reVal = line.split(" ")[3].replace("#", "").strip("\r").strip("\n").strip()
            break
    fd_popen.close()

    return int(reVal)

"""
img = cv2.imread('rawimg_fuzztest_com_skt_prod_tmessage__com_skt_prod_tmessage_activities_settings_alarm_TAlarmSettingsActivity_201704121210.png');
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 400, 800)
cv2.imshow('img', img)
k = cv2.waitKey(30) & 0xff
time.sleep(2)
sys.exit()
cd /cygdrive/c/_python/workspace/PycharmProjects/lmcst/lmcst_v1.0
/cygdrive/c/Python27/python.exe scanning_adb_from_CascadeClassifier.py '[google][AOSPonmsm8996][7.1.1][eng.suser.20170331.165132][01049611657][trunk_dev][c423dd75][9699]' 'HT6CN0201431' 'com.skt.prod.tmessage' '[201704201955][201704202055][1][3000]' '2'
python scanning_adb_from_CascadeClassifier.py '[samsung][SM-G930S][7.0][G930SKSE1DQB5][01031951658][trunk_dev][c423dd75][9699]' 'ce1115fbd5ad960201' 'com.skt.prod.tmessage' '[201704221211][201704222211][10][3000]' '2'
python scanning_adb_from_CascadeClassifier.py '[google][AOSPonmsm8996][7.1.1][eng.suser.20170331.165132][01049611657][trunk_dev][c423dd75][9699]' 'HT6CN0201431' 'com.skt.prod.tmessage' '[201704221048][201704221348][3][3000]' '2'
/cygdrive/c/Python27/python.exe scanning_adb_from_CascadeClassifier.py '[google][AOSPonmsm8996][7.1.1][eng.suser.20170331.165132][01049611657][trunk_dev][c423dd75][9699][lmcst][50]' 'HT6CN0201431' 'com.skt.prod.tmessage' '[201704241205][201704251007][3][3000]' '2' '50'
"""
if __name__ == '__main__':
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

    print "UUID" + "={" + UUID + "}"
    print "deviceID" + "={" + deviceID + "}"
    print "packageName" + "={" + packageName + "}"
    print "TIMEID" + "={" + TIMEID + "}"
    print "POLLING_DELAY" + "={" + POLLING_DELAY + "}"

    START_TIME = TIMEID.split("][")[0].replace("[", "").replace("]", "").replace("'", "")
    EXPECT_END_TIME = TIMEID.split("][")[1].replace("[", "").replace("]", "").replace("'", "")
    duringHours = TIMEID.split("][")[2].replace("[", "").replace("]", "").replace("'", "")
    throttle = TIMEID.split("][")[3].replace("[", "").replace("]", "").replace("'", "")
    try:
        TARGET_Classifier_XML = UUID.split("][")[10].replace("[", "").replace("]", "").replace("'", "")
    except:
        TARGET_Classifier_XML = 'confirm_lbp_neg_900.xml'


    print "START_TIME" + "={" + START_TIME + "}"
    print "EXPECT_END_TIME" + "={" + EXPECT_END_TIME + "}"
    print "duringHours" + "={" + duringHours + "}"
    print "throttle" + "={" + throttle + "}"

    print "EXPECT_END_TIME: " + EXPECT_END_TIME
    print "CURRENTGMT9TIME: " + (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    print "CURRENT____TIME: " + str(datetime.datetime.now())
    print "CURRENT____TIME: " + str(time.ctime())
    print "CURRENT____TIME: " + datetime.datetime.now().strftime("%Y%m%d%H%M")
    print "CURRENTLOCATIME: " + time.strftime("%Y%m%d%H%M", time.localtime())


    # cascade_common_toggle = cv2.CascadeClassifier('common_toggle_list_off_best_until.xml')
    cascade_common_toggle = cv2.CascadeClassifier(TARGET_Classifier_XML)
    # cascade_common_toggle = cv2.CascadeClassifier('confirm_74_44_haar_neg_900.xml')

    previousActivity = getCurrentActivity()

    #print "previousActivity: " + previousActivity
    #print "winCount: " + str(winCount)
    #sys.exit()
    stayCount=-1
    while long(EXPECT_END_TIME) > long((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")) :
        currentActivity = getCurrentActivity()
        if cmp(previousActivity, currentActivity) == 0 :
            stayCount += 1
        else:
            stayCount = 0
            previousActivity = currentActivity;

        os.system("adb -s " + deviceID + " shell screencap -p /sdcard/scanning_adb_from_CascadeClassifier.png")
        if _platform == "linux" or _platform == "linux2":
            # linux
            pass
        elif _platform == "darwin":
            # MAC OS X
            pass
        elif _platform == "win32":
            # Windows
            pass

        os.system("adb -s " + deviceID + " pull /sdcard/scanning_adb_from_CascadeClassifier.png training")

        img = cv2.imread('./training/scanning_adb_from_CascadeClassifier.png');


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 50, 50)
        #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 100, 100)
        #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 129, 78)
        #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 120, 120)
        #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 120, 120, minSize=(140, 100))
        #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, scaleFactor=1000, minNeighbors=120, minSize=(72, 128))
        #Physical size: 1440x2560
        width, height = getWindowSize()
        print "width, height = " + str(width) + ", " + str(height)

        detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, scaleFactor=height, minNeighbors=(height/20), minSize=((width/20), (height/20)))
        checkPoint = []
        select = -1
        if len(detect_common_toggle) > 0:
            select = random.randrange(0, len(detect_common_toggle))
            index = 0
            touch_x, touch_y = 0, 0
            for (x, y, w, h) in detect_common_toggle:
                checkPoint.append((int(x + w / 2), int(y + h / 2)))
                if index == select:
                    touch_x, touch_y = int(x + w / 2), int(y + h / 2)
                index += 1

        #row = dataFrame.ix[currentActivity]
        #for (x, y) in row['tap']:
            #print x, y
        print "stayCount: " + str(stayCount)
        #time.sleep(5)
        NEED_FILEWRITE = False
        if len(detect_common_toggle) == 0 or stayCount > 10 :
            pass
            #os.system("adb -s " + deviceID + " shell input keyevent KEYCODE_BACK")
        elif stayCount > 20 :
            pass
            #os.system("adb -s " + deviceID + " shell input keyevent KEYCODE_HOME")
        else :
            #os.system("adb -s " + deviceID + " shell input tap " + str(touch_x) + " " + str(touch_y))
            try :
                row = dataFrame.ix[currentActivity]
                #print set(row['tap']) & set(checkPoint)
                print "len(set(row['tap']): " + str(len(row['tap']))
                intersection_count = len(set(row['tap']).intersection(set(checkPoint)))
                if len(row['tap']) == intersection_count:
                    print "same"
                else:
                    ratio = float(intersection_count)/float(len(row['tap']))
                    print "ratio:" + str(ratio)
                    print "not same"
                    dataFrame.set_value(currentActivity, 'exectime', str(datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M"))
                    dataFrame.set_value(currentActivity, 'click#', dataFrame.ix[currentActivity]['click#']+1)
                    dataFrame.set_value(currentActivity, 'tap', checkPoint)
                    dataFrame.set_value(currentActivity, 'tap#', len(detect_common_toggle))
                    NEED_FILEWRITE = True

                if stayCount == 0 :
                    dataFrame.set_value(currentActivity, 'visit#', dataFrame.ix[currentActivity]['visit#'] + 1)

            except KeyError, e:  ## if failed, report it back to the user ##
                print "KeyError: ", sys.exc_info()[0], sys.exc_info()[1]
                raw_data = {'exectime' : (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M"), 'visit#' : 1, 'click#' : 1, 'tap': [checkPoint], 'tap#' : len(detect_common_toggle)}
                dataFrame = dataFrame.append(DataFrame(raw_data, index=[currentActivity]))
                #dataFrame = dataFrame.append(DataFrame(raw_data))
                NEED_FILEWRITE = True
            except:
                print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        if NEED_FILEWRITE :
            f = open("./training/rawDetectBtn_" + currentActivity + ".txt", 'w+')
            f.writelines(["tap,%s\n" % str(item).replace(" ", "").replace("(", "").replace(")", "").strip() for item in checkPoint])
            f.close()

        if len(detect_common_toggle) > 0:
            index = 0
            for (x, y, w, h) in detect_common_toggle:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                print x, y, w, h
                if index == select:
                    pass
                cv2.putText(img, 'tap', (x + w / 2, y + h / 2), font, 1, (0, 0, 255), 3, cv2.LINE_AA)
                index += 1

        cv2.putText(img, currentActivity, (10, 1000), font, 1.0, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        # cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE)
        width, height = 540, 960
        cv2.resizeWindow('img', width, height)
        cv2.imshow('img', cv2.resize(img, (width, height)))
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        cv2.imwrite("./rawDetectImg_" + currentActivity + "_" + START_TIME + ".png", img)
        #time.sleep(1)
        #sys.exit()

    print(dataFrame)
    dataFrame.to_csv("./training/rawDataFrame_" + TARGET_Classifier_XML.replace(".xml", "") + "_" + START_TIME + ".csv")
    #df.to_csv(file_name, sep='\t', encoding='utf-8')

    cv2.destroyAllWindows()
    sys.exit()

