#!/bin/bash

targetApp=com.lge.camera/.CameraAppLauncher
deviceId=LMQ725S7e0f62

while [ 1 ]; do
    echo "adb -s ${deviceId} shell input tap 550 1920"
    adb -s ${deviceId} shell input tap 550 1920
    sleep 2
    echo "adb -s ${deviceId} shell input tap 220 1920"
    adb -s ${deviceId} shell input tap 220 1920
    sleep 10    
    echo "adb -s ${deviceId} shell input tap 500 1000"
    adb -s ${deviceId} shell input tap 500 1000
    sleep 2
    echo "adb -s ${deviceId} shell input tap 550 1850"
    adb -s ${deviceId} shell input tap 550 1850
    sleep 5
done





