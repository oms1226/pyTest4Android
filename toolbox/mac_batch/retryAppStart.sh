#!/bin/bash

targetApp=com.lge.camera/.CameraAppLauncher
deviceId=LMQ725S7e0f62

while [ 1 ]; do
	echo "adb -s ${deviceId} shell am start -a android.intent.action.MAIN -n ${targetApp}"
    adb -s ${deviceId} shell am start -a android.intent.action.MAIN -n ${targetApp}
    sleep 5    
    echo "adb -s ${deviceId} shell input keyevent KEYCODE_BACK"
    adb -s ${deviceId} shell input keyevent KEYCODE_BACK
    sleep 5
done