#!/bin/sh

echo "this is ${0}"
start=`expr index "$0" /`
end=`expr index "$0" .sh`
ID_FILENAME=${0:$start:$(($end-$start-2))}
echo "ID_FILENAME is ${ID_FILENAME}"

packageName=com.skt.prod.dialer
deviceID=ce1115fbd5ad960201
deviceID=HT6CN0201431
deviceID=emulator-5554
phoneNum=01021462805
#deviceID=emulator-5554
TARGET_tombstones_NUM=0
echo "TARGET_tombstones_NUM" "$TARGET_tombstones_NUM"
TARGET_tombstones_NUM=`expr $TARGET_tombstones_NUM + 1`
echo "TARGET_tombstones_NUM" "$TARGET_tombstones_NUM"
exit 0

while [ 1 ]
do
rm -f ./rawinfo_${ID_FILENAME}.txt
`adb -s ${deviceID} shell top -n 1 | grep ${packageName} > ./rawinfo_${ID_FILENAME}.txt`
line_Top=$(cat ./rawinfo_${ID_FILENAME}.txt | sed 's/  */ /g' | sed 's/\r//g')
echo "$line_Top"
PID=$(echo ${line_Top} | cut -f1 -d " ")
USER=$(echo ${line_Top} | cut -f2 -d " ")
PR=$(echo ${line_Top} | cut -f3 -d " ")
NI=$(echo ${line_Top} | cut -f4 -d " ")
CPU=$(echo ${line_Top} | cut -f5 -d " " | sed 's/%//g')
S=$(echo ${line_Top} | cut -f6 -d " ")
THRC=$(echo ${line_Top} | cut -f7 -d " ")
VSS=$(echo ${line_Top} | cut -f8 -d " " | sed 's/K//g')
RSS=$(echo ${line_Top} | cut -f9 -d " " | sed 's/K//g')
PCY=$(echo ${line_Top} | cut -f10 -d " ")
Name=$(echo ${line_Top} | cut -f11 -d " ")
if [[ "$packageName" == "$Name" ]];then
    echo "PID" "$PID"
    echo "USER" "$USER"
    echo "PR" "$PR"
    echo "NI" "$NI"
    echo "CPU" "$CPU"
    echo "S" "$S"
    echo "THRC" "$THRC"
    echo "VSS" "$VSS"
    echo "RSS" "$RSS"
    echo "PCY" "$PCY"
    echo "Name" "$Name"
fi
#echo "$result"
sleep 1
done
exit 0

revCount=1234
floatNumber1=0.34
floatNumber2=12.34
notFloatNumber=.1234
intNumber=0
notIntNumber=01

echo "PACKAGENAME" "$packageName" >> ./${ID_FILENAME}_json.txt
echo "DEVICE_ID" "$deviceID" >> ./${ID_FILENAME}_json.txt
echo "phoneNum" "$phoneNum" >> ./${ID_FILENAME}_json.txt
echo "revCount" "$revCount" >> ./${ID_FILENAME}_json.txt
echo "revCount" "test test test" >> ./${ID_FILENAME}_json.txt
echo "floatNumber1" "$floatNumber1" >> ./${ID_FILENAME}_json.txt
echo "floatNumber2" "$floatNumber2" >> ./${ID_FILENAME}_json.txt
echo "notFloatNumber" "$notFloatNumber" >> ./${ID_FILENAME}_json.txt
echo "intNumber" "$intNumber" >> ./${ID_FILENAME}_json.txt
echo "notIntNumber" "$notIntNumber" >> ./${ID_FILENAME}_json.txt

function writeTrace ()
{
    echo "PACKAGENAME" "$packageName" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "DEVICE_ID" "$deviceID" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "phoneNum" "$phoneNum" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "revCount" "$revCount" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "revCount" "test test test" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "floatNumber1" "$floatNumber1" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "floatNumber2" "$floatNumber2" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "notFloatNumber" "$notFloatNumber" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "intNumber" "$intNumber" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "notIntNumber" "$notIntNumber" >> ./${ID_FILENAME}_json_snapshot.txt

    if [ -e ./${ID_FILENAME}_json_snapshot.txt ] ; then
        jsonString="{"
        while read line
        do
            if [[ ${#jsonString} > 1 ]] ; then
            jsonString=${jsonString}","
            fi
            key=$(echo ${line} | cut -f1 -d " ")
            value=$(echo ${line} | cut -f2- -d " ")
            r=${value//[0-9.]/}
            if [[ (-z "$r") && (($value == 0) || ($value == 0.*) || (($value != 0*) && ($value != .*))) ]] ; then
                echo "\"${key}\":${value}"
            jsonString=${jsonString}"\"${key}\":${value}"
            else
                echo "\"${key}\":\"${value}\""
            jsonString=${jsonString}"\"${key}\":\"${value}\""
            fi

        done < ./${ID_FILENAME}_json_snapshot.txt
        rm -f ./${ID_FILENAME}_json_snapshot.txt
        jsonString=${jsonString}"}"
        echo ${jsonString}
        if [ ! -d /cygdrive/c/lmcft_log/tracking ] ; then
            mkdir -p /cygdrive/c/lmcft_log/tracking
        fi
        echo ${jsonString} >> /cygdrive/c/lmcft_log/tracking/trace_${ID_FILENAME}_${START_TIME}.log
    fi
}

writeTrace
exit 0

if [ -e ./${ID_FILENAME}_json.txt ] ; then
	jsonString="{"
	while read line
	do
	    if [[ ${#jsonString} > 1 ]] ; then
		jsonString=${jsonString}","
	    fi
	    key=$(echo ${line} | cut -f1 -d " ")
	    value=$(echo ${line} | cut -f2- -d " ")
	    r=${value//[0-9.]/}
	    if [[ (-z "$r") && (($value == 0) || ($value == 0.*) || (($value != 0*) && ($value != .*))) ]] ; then
	        echo "\"${key}\":${value}"
		jsonString=${jsonString}"\"${key}\":${value}"
	    else
	        echo "\"${key}\":\"${value}\""
		jsonString=${jsonString}"\"${key}\":\"${value}\""
	    fi

	done < ./${ID_FILENAME}_json.txt
	rm -f ./${ID_FILENAME}_json.txt
	jsonString=${jsonString}"}"
	echo ${jsonString}
	echo ${jsonString} >> /cygdrive/c/lmcft_log/result/Result_healthCheck_${ID_FILENAME}.log
fi
exit 0

echo "hostname" "$(hostname)"
exit 0


echo "Can't find service: window" > ./TEMP_VARIABEL.txt
#echo "" > ./TEMP_VARIABEL.txt
containInWordsCount=0

rand=$(adb -s ${deviceID} shell dumpsys activity recents | grep '* Recent #0' | grep "${packageName}")
echo [$rand]
if [ -n "$rand" ]
then	
        echo "in brace"
#        eval "adb -s '${deviceID}' shell \"am start -a android.intent.action.MAIN -n '${packageName}'/'${launchactivityName}'\""		
#	ACION_LIST="${ACION_LIST}.${launchactivityName}"
#	sleep ${POLLING_DELAY}
fi
exit 0
rand=$(( $RANDOM % 100 ))
echo ${rand}
if [ ${rand} -lt 50 ]
then
    mCallState=$(adb -s ${deviceID} shell dumpsys telephony.registry | grep mCallState | cut -f2 -d "=" | sed 's/\r//g' | sed 's/\n//g')
    echo "mCallState is [${mCallState}]"
    #0 indicates idle,
    #1 = ringing and
    #2 = active call
    if [ ${mCallState} -eq 2 ]
    then	    
            eval "adb -s '${deviceID}' shell input keyevent KEYCODE_ENDCALL"
            ACION_LIST="${ACION_LIST}.keyevent_endcall"
            sleep ${POLLING_DELAY}	    
    fi
fi

exit 0
function containInWords ()
{
	containInWordsCount=0
	if [ ! -n "$(cat ./TEMP_VARIABEL.txt)" ]; then
		echo "fileContent is nothing!"
		containInWordsCount=9999
	fi
	#generic_x86_64:/ # dumpsys window windows
	#Can't find service: window
	TARGET_STRING="find service: window"
	eval "grep -c -i '${TARGET_STRING}' ./TEMP_VARIABEL.txt > ./MATCH_COUNT.txt"
	count=$(cat ./MATCH_COUNT.txt)
	rm -f ./MATCH_COUNT.txt
	containInWordsCount=$((${count} + ${containInWordsCount}))
	
	#generic_x86_64:/ # dumpsys window windows
	#Service dumps disabled due to hung system process.
	TARGET_STRING="Service dumps disabled due to hung system process."
	eval "grep -c -i '${TARGET_STRING}' ./TEMP_VARIABEL.txt > ./MATCH_COUNT.txt"
	count=$(cat ./MATCH_COUNT.txt)
	rm -f ./MATCH_COUNT.txt
	containInWordsCount=$((${count} + ${containInWordsCount}))

	echo "containInWordsCount is ${containInWordsCount}"
}
containInWords

echo $(echo ${deviceID} | grep emulator)
if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then
    echo "device"
else
    echo "emulator"
fi
exit 0

mFocusedApp=$(adb -s "${deviceID}" shell dumpsys window windows | grep 'mFocusedApp' | sed 's/  */ /g' | sed 's/\r//g' | cut -f6 -d " " | sed 's/}//g' | sed 's/\///g' | sed 's/://g' | sed 's/ //g')
echo "mFocusedApp is ${mFocusedApp}"
exit 0

for filename in $(ls -1 ./training); do
    tAction=""
    tX=0
    tY=0
    currentFocus=$(adb -s "${deviceID}" shell dumpsys window windows | grep 'mFocusedApp' | sed 's/  */ /g' | sed 's/\r//g' | cut -f6 -d " " | sed 's/}//g' | sed 's/\///g')
    filename=$(echo ${filename} | grep "${currentFocus}" | sed 's/\r//g' | sed 's/\n//g')
    if [ -n "$filename" ]
    then
        echo "filename is ${filename}"
        touchPoints=()
        index=0
        while read line ; do
            touchPoints[$index]=${line}
            index=$(($index+1))
        done < ./training/${filename}
        echo "#touchPoints is ${#touchPoints[*]}"

        if [ ${#touchPoints[*]} -gt 0 ]
        then
            targetTouchPoint=${touchPoints[$(( $RANDOM % ${index} ))]}
            echo "targetTouchPoint is ${targetTouchPoint}"
            tAction=$(echo ${targetTouchPoint} | cut -f1 -d ",")
            tX=$(echo ${targetTouchPoint} | cut -f2 -d ",")
            tY=$(echo ${targetTouchPoint} | cut -f3 -d ",")
            break
        fi
    fi
done
echo "tAction is ${tAction}"
echo "tX is ${tX}"
echo "tY is ${tY}"
echo "adb -s '${deviceID}' shell input tap '${tX}' '${tY}'"
eval "adb -s '${deviceID}' shell input tap '${tX}' '${tY}'"
exit 0

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

