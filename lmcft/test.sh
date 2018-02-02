#!/bin/sh

echo "this is ${0}"
start=`expr index "$0" /`
end=`expr index "$0" .sh`
ID_FILENAME=${0:$start:$(($end-$start-2))}
echo "ID_FILENAME is ${ID_FILENAME}"

packageName=com.skt.prod.tmessage
deviceID=ce1115fbd5ad960201
phoneNum=01021462805


currentFocus=$(adb shell dumpsys window windows | grep 'mCurrentFocus' | grep "${packageName}" | sed 's/  */ /g' | sed 's/\r//g' | cut -f4 -d " " | sed 's/}//g')
echo "currentFocus is [${currentFocus}]"
exit 0
echo "{\"process_mem_lastreport\":{\"previousPID\":${previousPID},\"DalvikHeap_Size\":${DalvikHeap_Size},\"DalvikHeapAlloc\":${DalvikHeapAlloc},\"DalvikHeap_Free\":${DalvikHeap_Free},\"NativeHeap_Size\":${NativeHeap_Size},\"NativeHeapAlloc\":${NativeHeapAlloc},\"NativeHeap_Free\":${NativeHeap_Free}}}"
exit 0

TARGET_tombstones_NUM=0
TARGET_anr_NUM=0

existTargetName=tombstones
isExistTarget=$(adb -s ${deviceID} shell ls -1 /data | grep "${existTargetName}" | sed 's/\r//g' | sed 's/\n//g')

if [ -n "$isExistTarget" ]
then
	echo "isExistTarget is [${isExistTarget}]"
	fileName=$(adb -s ${deviceID} shell ls -1 /data/${existTargetName} | tail -n 1 | sed 's/\r//g' | sed 's/\n//g')
	while [ -n "$fileName" ]
	do
		execTiime=`eval date +%Y%m%d%H%M`
	        eval "adb -s '${deviceID}' pull '/data/${existTargetName}/${fileName}' 'raw_${ID_FILENAME}_${existTargetName}_${START_TIME}_${execTiime}_${fileName}'"
	        eval "adb -s '${deviceID}' shell rm '/data/${existTargetName}/${fileName}'"
		num=$(cat ./raw_${ID_FILENAME}_${existTargetName}_${START_TIME}_${execTiime}_${fileName} | grep ${packageName} | wc -l)
		if [ ${num} -gt 0 ]
		then
			echo "${existTargetName} occurs ${num} times"
			TARGET_tombstones_NUM=`expr $TARGET_tombstones_NUM + 1`
		else
		        eval "rm './raw_${ID_FILENAME}_${existTargetName}_${START_TIME}_${execTiime}_${fileName}'"
		fi		
		fileName=$(adb -s ${deviceID} shell ls -1 /data/${existTargetName} | tail -n 1 | sed 's/\r//g' | sed 's/\n//g')
	done
        eval "adb -s '${deviceID}' shell rm -rf '/data/${existTargetName}'"
fi

existTargetName=anr
isExistTarget=$(adb -s ${deviceID} shell ls -1 /data | grep "${existTargetName}" | sed 's/\r//g' | sed 's/\n//g')
if [ -n "$isExistTarget" ]
then
	echo "isExistTarget is [${isExistTarget}]"
	fileName=$(adb -s ${deviceID} shell ls -1 /data/${existTargetName} | tail -n 1 | sed 's/\r//g' | sed 's/\n//g')
	while [ -n "$fileName" ]
	do
		execTiime=`eval date +%Y%m%d%H%M`
	        eval "adb -s '${deviceID}' pull '/data/${existTargetName}/${fileName}' 'raw_${ID_FILENAME}_${existTargetName}_${START_TIME}_${execTiime}_${fileName}'"
	        eval "adb -s '${deviceID}' shell rm '/data/${existTargetName}/${fileName}'"
		num=$(cat ./raw_${ID_FILENAME}_${existTargetName}_${START_TIME}_${execTiime}_${fileName} | grep ${packageName} | wc -l)
		if [ ${num} -gt 0 ]
		then
			echo "${existTargetName} occurs ${num} times"
			TARGET_anr_NUM=`expr $TARGET_anr_NUM + 1`
		else
		        eval "rm './raw_${ID_FILENAME}_${existTargetName}_${START_TIME}_${execTiime}_${fileName}'"
		fi		
		fileName=$(adb -s ${deviceID} shell ls -1 /data/${existTargetName} | tail -n 1 | sed 's/\r//g' | sed 's/\n//g')
	done
        eval "adb -s '${deviceID}' shell rm -rf '/data/${existTargetName}'"	
fi

echo "TARGET_tombstones_NUM is [${TARGET_tombstones_NUM}]"
echo "TARGET_anr_NUM is [${TARGET_anr_NUM}]"
exit 0

rm -f ./rawinfo_logCheck_9673_onlyUniqCrash.txt
while read uniqWord
do
	echo "uniqWord is [${uniqWord}]"
	tag=$(cat ./rawinfo_logCheck_201704060010.txt | grep "${uniqWord}" | sed 's/  */ /g' | cut -f6 -d " " | head -1)
	echo "tag is [${tag}]"	
	cat ./rawinfo_logCheck_201704060010.txt | grep -A50 -B50 "${uniqWord}" | grep "${tag}" >> ./rawinfo_logCheck_9673_onlyUniqCrash.txt
done < ./rawinfo_logCheck_201704060010_onlyUniqCrash.txt

exit 0
arg=s

if [ $(echo $arg | egrep "[0-9]+") ]; then
        echo "number : $arg"
else
        echo "is NOT number : $arg"
fi

exit 0
packageName=com.skt.prod.tmessage
echo "packageName is ${packageName}"
logTag=Yorum

activityinWindows=com.skt.prod.tmessage/com.skt.prod.tmessage.activities.begin.TBeginSplashActivity
echo "activityinWindows is ${activityinWindows}"
activityName=$(echo ${activityinWindows} | sed 's/\./_/g' | sed 's/\//__/g' | sed 's/\r//g' | sed 's/\n//g' | sed 's/\"//g')
#activityName=$(echo ${activityinWindows} | sed 's/.//g' | sed 's/\//__/g')
echo "activityName is ${activityName}"
exit 0

count=0
PYTHONEXEC=/cygdrive/c/Python27/python.exe

cat ./rawinfo_logCheck_201703280010.txt | grep "${logTag}" | cut -f3 -d " " | uniq | wc -l

while read uniqWord
do
	echo "uniqWord is [${uniqWord}]"
	cat ./rawinfo_logCheck_201703271210.txt | grep "${uniqWord}"
done < ./rawinfo_logCheck_201703271210_onlyUniqCrash.txt

exit 0

for pid in $(adb -s ${deviceID} shell ps | grep 'log' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
do
	echo "pid is [${pid}]"
	KILL_STATUS=`adb -s ${deviceID} shell kill -9 ${pid}`
	echo "KILL_STATUS is [${KILL_STATUS}]"
done

#SM-G930S NOS
phoneNumLineNum_Index=15
phoneNum=$(adb -s ${deviceID} shell service call iphonesubinfo ${phoneNumLineNum_Index} | grep 0x00000000 | sed 's/  */ /g' | sed 's/\.//g' | sed "s/'//g" | sed 's/)//g' | sed 's/\r//g' | cut -f7 -d " ")
phoneNum=${phoneNum}$(adb -s ${deviceID} shell service call iphonesubinfo ${phoneNumLineNum_Index} | grep 0x00000010 | sed 's/  */ /g' | sed 's/\.//g' | sed "s/'//g" | sed 's/)//g' | sed 's/\r//g' | cut -f7 -d " ")
echo "phoneNum is [${phoneNum}]"
exit 0

while [ 1 ]
do
    bright_over=$(adb -s ${deviceID} shell settings get system screen_brightness | sed 's/\r//g')
    echo "bright_over is ${bright_over}"
    if [ ${bright_over} -gt 100 ]
    then
        echo "bright 100 over"
        eval "adb -s '${deviceID}' shell settings put system screen_brightness 70"
    else
        echo "bright 100 under"
    fi

	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`

    MSG=$(${PYTHONEXEC} excelReadAndPrint.py | grep "ADDRESS:")
    ADDRESS=$(echo ${MSG} | cut -f1 -d "_" | sed 's/ADDRESS://g' | sed 's/\r//g' | sed 's/\n//g')
    MESSAGE=$(echo ${MSG} | cut -f2 -d "_" | sed 's/MESSAGE://g' | sed 's/\r//g' | sed 's/\n//g')
	echo "ADDRESS is [${ADDRESS}]"
	echo "MESSAGE is [${MESSAGE}]"
	echo "count is [${count}]"
	echo "execTiime is [${execTiime}]"	
#	sleep 60
done

