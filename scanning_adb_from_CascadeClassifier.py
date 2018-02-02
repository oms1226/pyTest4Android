import numpy as np
import cv2
import os
import sys
import time
import random
import subprocess
from pandas import Series, DataFrame
import datetime


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
    cmd = ['adb', '-d', 'shell', 'dumpsys', 'window', 'windows']
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    #data = fd_popen.read().strip()
    reVal = None
    while 1:
        line = fd_popen.readline()
        if not line:
            break
        if "mCurrentFocus" in str(line) :
            reVal = str(line).strip("\r").strip("\n").strip()
            break
    fd_popen.close()

    if reVal != None :
        if "/" in reVal:
            reVal = reVal.split("/")[1].replace("}", "")
        else:
            reVal = reVal.replace("}", "")

    return reVal

#cascade_common_toggle = cv2.CascadeClassifier('common_toggle_list_off_best_until.xml')
cascade_common_toggle = cv2.CascadeClassifier('confirm_lbp_neg_900.xml')
"""
img = cv2.imread('rawimg_fuzztest_com_skt_prod_tmessage__com_skt_prod_tmessage_activities_settings_alarm_TAlarmSettingsActivity_201704121210.png');
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 400, 800)
cv2.imshow('img', img)
k = cv2.waitKey(30) & 0xff
time.sleep(2)
sys.exit()
"""

previousActivity = getCurrentActivity()
stayCount=-1
while 1:
    currentActivity = getCurrentActivity()
    if cmp(previousActivity, currentActivity) == 0 :
        stayCount += 1
    else:
        stayCount = 0
        previousActivity = currentActivity;

    os.system("adb -d shell screencap -p /sdcard/scanning_adb_from_CascadeClassifier.png")
    os.system("adb -d pull /sdcard/scanning_adb_from_CascadeClassifier.png")

    img = cv2.imread('scanning_adb_from_CascadeClassifier.png');


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 50, 50)
    #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 100, 100)
    #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 129, 78)
    #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 120, 120)
    #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, 120, 120, minSize=(140, 100))
    #detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, scaleFactor=1000, minNeighbors=120, minSize=(72, 128))
    #Physical size: 1440x2560
    detect_common_toggle = cascade_common_toggle.detectMultiScale(gray, scaleFactor=2560, minNeighbors=128, minSize=(72, 128))

    if len(detect_common_toggle) > 0 :
        select = random.randrange(0, len(detect_common_toggle))
        index = 0
        touch_x, touch_y = 0, 0
        checkPoint = []
        for (x, y, w, h) in detect_common_toggle:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            checkPoint.append((int(x+w/2), int(y+h/2)))
            print x, y, w, h
            if index == select :
                touch_x, touch_y = int(x+w/2), int(y+h/2)
                cv2.putText(img, 'Button', (x + w / 2, y + h / 2), font, 1, (0, 0, 255), 3, cv2.LINE_AA)
            index += 1

    cv2.putText(img, currentActivity, (10, 1000), font, 1.2, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE)
    width, height = 540, 960
    cv2.resizeWindow('img', width, height)
    cv2.imshow('img', cv2.resize(img, (width, height)))
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    #row = dataFrame.ix[currentActivity]
    #for (x, y) in row['btn']:
        #print x, y
    print "stayCount: " + str(stayCount)
    time.sleep(5)

    if len(detect_common_toggle) == 0 or stayCount > 10 :
        os.system("adb -d shell input keyevent KEYCODE_BACK")
    elif stayCount > 20 :
        os.system("adb -d shell input keyevent KEYCODE_HOME")
    else :
        os.system("adb -d shell input tap " + str(touch_x) + " " + str(touch_y))
        try :
            row = dataFrame.ix[currentActivity]
            #print set(row['btn']) & set(checkPoint)
            intersection_count = len(set(row['btn']).intersection(set(checkPoint)))
            if len(row['btn']) == intersection_count:
                print "same"
            else:
                ratio = float(intersection_count)/float(len(row['btn']))
                print "ratio:" + str(ratio)
                print "not same"
                dataFrame.set_value(currentActivity, 'btn', checkPoint)
                dataFrame.set_value(currentActivity, 'exectime', datetime.datetime.now())
                dataFrame.set_value(currentActivity, 'clickcount', dataFrame.ix[currentActivity]['clickcount']+1)

            if stayCount == 0 :
                dataFrame.set_value(currentActivity, 'visitcount', dataFrame.ix[currentActivity]['visitcount'] + 1)

        except KeyError, e:  ## if failed, report it back to the user ##
            raw_data = {'btn': [checkPoint], 'exectime' : datetime.datetime.now(), "visitcount" : 1, "clickcount" : 1}
            dataFrame = dataFrame.append(DataFrame(raw_data, index=[currentActivity]))
            #dataFrame = dataFrame.append(DataFrame(raw_data))


    print(dataFrame)
    time.sleep(1)
    #sys.exit()


cv2.destroyAllWindows()
sys.exit()

