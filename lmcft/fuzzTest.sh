#!/bin/sh
##need to complete manually#####################################################
if [ "$1" == "-deviceID" ]
then
	shift
	deviceID=${1}
	shift
else
	deviceID=ce1115fbd5cea11b01
	#deviceID=276db6c3
	#deviceID=ce1015faf3f91e0a01
fi
if [ "$1" == "-phoneNum" ]
then
	shift
	phoneNum=${1}
	shift
else
	#SM-G930S NOS
	phoneNumLineNum_Index=15
	phoneNum=$(adb -s ${deviceID} shell service call iphonesubinfo ${phoneNumLineNum_Index} | grep 0x00000000 | sed 's/  */ /g' | sed 's/\.//g' | sed "s/'//g" | sed 's/)//g' | sed 's/\r//g' | cut -f7 -d " ")
	phoneNum=${phoneNum}$(adb -s ${deviceID} shell service call iphonesubinfo ${phoneNumLineNum_Index} | grep 0x00000010 | sed 's/  */ /g' | sed 's/\.//g' | sed "s/'//g" | sed 's/)//g' | sed 's/\r//g' | cut -f7 -d " ")
fi

if [ "$1" == "-uploadRootDir" ]
then
	shift
	uploadRootDir=${1}
	shift
else
	uploadRootDir=/cygdrive/z
fi
echo "uploadRootDir is [${uploadRootDir}]"

echo "deviceID is [${deviceID}]"
echo "phoneNum is [${phoneNum}]"
packageName=com.skt.prod.tmessage
launchactivityName=com.skt.prod.tmessage.activities.begin.TBeginSplashActivity
echo "packageName is ${packageName}"
logTag=Yorum
echo "logTag is ${logTag}"
lintLinkRootUrl=file://172.23.107.213/build/lint
echo "lintLinkRootUrl is [${lintLinkRootUrl}]"
################################################################################
echo "this is ${0}"
start=`expr index "$0" /`
end=`expr index "$0" .sh`
ID_FILENAME=${0:$start:$(($end-$start-2))}
echo "ID_FILENAME is ${ID_FILENAME}"

if [ "$1" ]
then
	throttle=${1}	
	shift
else
	#throttle=5000
	echo -n "How fast is your test controling throttle?(ex. 5000)"
	read throttle
fi
echo "throttle is ${throttle}"

retryCount=90000

if [ "$1" ]
then
	duringHours=${1}
	shift
else
	echo -n "How long is during hours?(ex. 12)"
	read duringHours
fi
echo "duringHours is ${duringHours}"
#throttle=1500;retryCount=30000;201702222000 - 201702230032

START_TIME=`eval date +%Y%m%d%H%M`
echo "START_TIME is ${START_TIME}"

EXPECT_END_TIME=`eval date +%Y%m%d%H%M -d '+${duringHours}hours'`
echo "EXPECT_END_TIME is ${EXPECT_END_TIME}"

POLLING_DELAY=2

UUID=$(adb -s ${deviceID} shell getprop | grep 'ro.product.manufacturer' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
UUID=${UUID}$(adb -s ${deviceID} shell getprop | grep 'ro.product.model' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
UUID=${UUID}$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.release' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
UUID=${UUID}$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.incremental' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
UUID=${UUID}[${phoneNum}]

TIMEID=[${START_TIME}][${EXPECT_END_TIME}][${duringHours}][${throttle}]
echo "TIMEID is ${TIMEID}"

unit=20
wm_size=$(adb -s ${deviceID} shell wm size | tail -n 1)
wm_size_width=$(echo ${wm_size} | cut -f3 -d " " | cut -f1 -d "x" | sed 's/\r//g' | sed 's/\n//g')
wm_size_height=$(echo ${wm_size} | cut -f3 -d " " | cut -f2 -d "x" | sed 's/\r//g' | sed 's/\n//g')
echo "wm_size_width is [${wm_size_width}]"
echo "wm_size_height is [${wm_size_height}]"


count=0
error_reason=""
TARGET_tombstones_NUM=0
TARGET_anr_NUM=0
TARGET_STAYKILL_COUNT=0
stay_count=0
previous_activityinWindows=${launchactivityName}

echo "pwd is $(pwd)"

if [ "$1" ]
then
	isPreProcess=${1}
	shift
else
#	read -p "Press enter to continue" nothing
	echo -n "Do you need to exec preProcess?(ex. yes or no)"
	read isPreProcess	
fi

echo "isPreProcess is [${isPreProcess}]"

if [ "$isPreProcess" == "yes" ]
then
	preProcessShellName=preProcessCheck
	echo "./${preProcessShellName}.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${uploadRootDir}' '${lintLinkRootUrl}'"
	eval "./${preProcessShellName}.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${uploadRootDir}' '${lintLinkRootUrl}'"
	if [ "$?" == "0" ]
	then
		echo "preProcessCheck.sh success"
	else
		echo "preProcessCheck.sh is failed"
		exit 1
	fi
fi

if [ "$isPreProcess" != "yes" ]
then
	git_branchName=idontknow
	git_revCount=0
	git_commitValue=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
elif [ ! -n "$(cat ./summary.txt | grep ${preProcessShellName} | grep ${START_TIME})" ]
then
	git_branchName=idontknow
	git_revCount=0
	git_commitValue=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
else
	git_branchName=$(cat ./summary.txt | tail -n 1 | cut -f4 | sed 's/\r//g')
	git_revCount=$(cat ./summary.txt | tail -n 1 | cut -f6 | sed 's/\r//g')
	git_commitValue=$(cat ./summary.txt | tail -n 1 | cut -f5 | sed 's/\r//g')
fi

echo "git_branchName is [${git_branchName}]"
echo "git_revCount is [${git_revCount}]"
echo "git_commitValue is [${git_commitValue}]"

UUID=${UUID}[${git_branchName}]
UUID=${UUID}[${git_commitValue}]
UUID=${UUID}[${git_revCount}]
echo "UUID is ${UUID}"

START_BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")
echo "START_BATTERY is ${START_BATTERY}"

#eval "adb -s '${deviceID}' shell monkey -p com.skt.prod.tmessage -s 1 -v --throttle '${throttle}' --ignore-crashes --pct-syskeys 0 --pct-appswitch 10 --pct-touch 70 --pct-anyevent 20 '${retryCount}' &"
#eval "adb -s '${deviceID}' shell monkey -p com.skt.prod.tmessage -s 1 -v --throttle '${throttle}' --ignore-crashes --pct-syskeys 0 --pct-appswitch 10 --pct-touch 90 --pct-anyevent 0 '${retryCount}' &"
MONKEY_CMD="adb -s '${deviceID}' shell monkey -p '${packageName}' -s '${count}' -v --throttle '${throttle}' --ignore-crashes --pct-syskeys 0 --pct-appswitch 10 --pct-touch 45 --pct-anyevent 0 --pct-motion 45 '${retryCount}' &"

echo "./tmessageCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${isPreProcess}' &"
echo "./memCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
echo "./cpuCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
echo "./tempCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
echo "./storageCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
echo "./tcpNetworkCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
echo "./logCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"

eval "./tmessageCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${isPreProcess}' > ./rawinfo_${ID_FILENAME}_tmessageLogging_${START_TIME}.txt &"
#read -p "Press enter to continue" nothing
sleep 30
eval "./memCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
eval "./cpuCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
eval "./tempCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
eval "./storageCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
eval "./tcpNetworkCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' &"
eval "./logCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${logTag}' &"
sleep 1

SURFING_ACTIVITIES=()
function checkSurfingLog ()
{
	`adb -s ${deviceID} shell dumpsys window windows | grep 'Window #' | grep ${packageName} > rawinfo_${ID_FILENAME}_windows.txt`
	while read line
	do
		activityinWindows=$(echo ${line} | sed 's/  */ /g' | sed 's/\r//g' | cut -f5 -d " " | sed 's/}://g')
		isExist=false
		for activity in ${SURFING_ACTIVITIES[@]}
		do
			if [ ${activity} == ${activityinWindows} ]
			then
				isExist=true
				break
			fi
		done
		if [ ${isExist} = false ] ; then
			SURFING_ACTIVITIES[${#SURFING_ACTIVITIES[*]}]=${activityinWindows}
			echo "SURFING_ACTIVITIES just include new found [${activityinWindows}]"		
			echo "SURFING_ACTIVITIES# is [${#SURFING_ACTIVITIES[*]}]"
			activityName=$(echo ${activityinWindows} | sed 's/\./_/g' | sed 's/\//__/g' | sed 's/\r//g' | sed 's/\n//g')
		        eval "adb -s '${deviceID}' shell screencap -p '/sdcard/rawimg_${ID_FILENAME}_${activityName}_${START_TIME}.png'"
		        eval "adb -s '${deviceID}' pull '/sdcard/rawimg_${ID_FILENAME}_${activityName}_${START_TIME}.png'"
		        eval "adb -s '${deviceID}' shell rm '/sdcard/rawimg_${ID_FILENAME}_${activityName}_${START_TIME}.png'"
		fi
	done < rawinfo_${ID_FILENAME}_windows.txt
	
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
	
	currentFocus=$(adb -s "${deviceID}" shell dumpsys window windows | grep 'mCurrentFocus' | grep "${packageName}" | sed 's/  */ /g' | sed 's/\r//g' | cut -f4 -d " " | sed 's/}//g')
	if [ ${previous_activityinWindows} == ${currentFocus} ]
	then
		stay_count=`expr $stay_count + 1`
		if [ ${stay_count} -gt 100 ]
		then
			eval "adb -s '${deviceID}' shell \"am force-stop '${packageName}'\""
			stay_count=0
			TARGET_STAYKILL_COUNT=`expr $TARGET_STAYKILL_COUNT + 1`			
		fi
	else
		previous_activityinWindows=${currentFocus}
		stay_count=0
	fi
}

function keepDataStatus ()
{
    airplane_mode_on=$(adb -s ${deviceID} shell settings get global airplane_mode_on | sed 's/\r//g')
    echo "airplane_mode_on is ${airplane_mode_on}"
    if [ ${airplane_mode_on} -gt 0 ]
    then
        echo "airplane_mode_on on"
        eval "adb -s '${deviceID}' shell settings put global airplane_mode_on 0"
        eval "adb -s '${deviceID}' shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false"
    else
        echo "airplane_mode_on off"
    fi

    mobile_data_on=$(adb -s ${deviceID} shell settings get global mobile_data | sed 's/\r//g')
    echo "mobile_data_on is ${mobile_data_on}"
    if [ ${mobile_data_on} -gt 0 ]
    then
        echo "mobile_data_on on"
    else
        echo "mobile_data_on off"
        eval "adb -s '${deviceID}' shell svc data enable"
    fi

    wifi_on=$(adb -s ${deviceID} shell settings get global wifi_on | sed 's/\r//g')
    echo "wifi_on is ${wifi_on}"
    if [ ${wifi_on} -gt 0 ]
    then
        echo "wifi_on on"
        eval "adb -s '${deviceID}' shell svc wifi disable"
    else
        echo "wifi_on off"
    fi
    
    bright_over=$(adb -s ${deviceID} shell settings get system screen_brightness | sed 's/\r//g')
    echo "bright_over is ${bright_over}"
    if [ ${bright_over} -gt 40 ]
    then
        echo "bright 40 over"
        eval "adb -s '${deviceID}' shell settings put system screen_brightness 40"
    else
        echo "bright 40 under"
    fi
    
    mode_ringer=$(adb -s ${deviceID} shell settings get global mode_ringer | sed 's/\r//g')
    echo "mode_ringer is ${mode_ringer}"
    if [ ${mode_ringer} -gt 0 ]
    then
        echo "can ringer"
        eval "adb -s '${deviceID}' shell service call audio 14 i32 0 s16 '${packageName}'"
    else
        echo "ringer is nothing"
    fi
}

while [ ${EXPECT_END_TIME} -gt  $(date +%Y%m%d%H%M) ]
do
	if [ ! -n "$(adb devices | grep ${deviceID})" ]
	then
		echo "deviceID[${deviceID}] probably turn off!"
		error_reason=${error_reason}."error_occur_turnoff"		
		break
	fi

	keepDataStatus

	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`
	isMonkey=$(adb -s ${deviceID} shell ps | grep monkey)
	if [ ! -n "$isMonkey" ]
	then
		eval ${MONKEY_CMD}
	fi
	
	ACION_LIST=""
		
#	eval "adb -s '${deviceID}' shell input keyevent 91"
#	ACION_LIST="${ACION_LIST}.keyevent_91"
#	eval "adb -s '${deviceID}' shell input keyevent 164"	
#	ACION_LIST="${ACION_LIST}.keyevent_164"
	rand=$(adb -s ${deviceID} shell dumpsys activity recents | grep '* Recent #0' | grep '${packageName}')	
	if [ ! -n "$rand" ]
	then	
	        eval "adb -s '${deviceID}' shell \"am start -a android.intent.action.MAIN -n '${packageName}'/'${launchactivityName}'\""
		ACION_LIST="${ACION_LIST}.${launchactivityName}"
		sleep 1		
	fi	

	checkSurfingLog
		
	rand=$(( $RANDOM % 100 ))
	if [ ${rand} -lt 33 ]
	then
		rand=$(( ( RANDOM % 7 )  + 1 ))
		for n in `seq 1 ${rand}`
		do
			eval "adb -s '${deviceID}' shell input keyevent 4"
			ACION_LIST="${ACION_LIST}.keyevent_back"
			sleep 1			
			checkSurfingLog
		done
	fi
	rand=$(( $RANDOM % 100 ))	
	if [ ${rand} -lt 20 ]
	then	
		eval "adb -s '${deviceID}' shell input keyevent 3"
		ACION_LIST="${ACION_LIST}.keyevent_home"
		sleep 1			
		checkSurfingLog
	fi
	


	rand=$(adb -s ${deviceID} shell dumpsys activity recents | grep '* Recent #0' | grep '${packageName}')	
	if [ ! -n "$rand" ]
	then	
	        eval "adb -s '${deviceID}' shell \"am start -a android.intent.action.MAIN -n '${packageName}'/'${launchactivityName}'\""
		ACION_LIST="${ACION_LIST}.${launchactivityName}"
		sleep 1		
	fi	

	rand=$(( $RANDOM % 100 ))
	if [ ${rand} -lt 25 ]
	then
		rand=$(( ( RANDOM % 10 )  + 1 ))
		for n in `seq 1 ${rand}`
		do
			eval "adb -s '${deviceID}' shell input swipe '$((${wm_size_width}/2))' '$((${wm_size_height}/4))' '$((${wm_size_width}/2))' '$((${wm_size_height}/2))' 100"
			ACION_LIST="${ACION_LIST}.up->down"
			sleep 1
		done
	fi
	
	rand=$(( $RANDOM % 100 ))
	if [ ${rand} -lt 25 ]
	then
		rand=$(( ( RANDOM % 10 )  + 1 ))
		for n in `seq 1 ${rand}`
		do
			eval "adb -s '${deviceID}' shell input swipe '$((${wm_size_width}/2))' '$((${wm_size_height}/4*3))' '$((${wm_size_width}/2))' '$((${wm_size_height}/2))' 100"
			ACION_LIST="${ACION_LIST}.down->up"
			sleep 1			
		done
	fi
	
	rand=$(( $RANDOM % 100 ))
	if [ ${rand} -lt 25 ]
	then
		rand=$(( ( RANDOM % 5 )  + 1 ))
		for n in `seq 1 ${rand}`
		do
			eval "adb -s '${deviceID}' shell input tap '$((${wm_size_width}/${unit}))' '$((${wm_size_height}/${unit}))'"
			ACION_LIST="${ACION_LIST}.up_left"
			sleep 1			
		done
	fi
	
	rand=$(( $RANDOM % 100 ))
	if [ ${rand} -lt 25 ]
	then
		rand=$(( ( RANDOM % 5 )  + 1 ))
		for n in `seq 1 ${rand}`
		do
			eval "adb -s '${deviceID}' shell input tap '$((${wm_size_width}/${unit}*(${unit}-1)))' '$((${wm_size_height}/${unit}))'"
			ACION_LIST="${ACION_LIST}.up_right"
			sleep 1			
		done
	fi	
	
	rand=$(( $RANDOM % 100 ))
	if [ ${rand} -lt 25 ]
	then
		rand=$(( ( RANDOM % 5 )  + 1 ))
		for n in `seq 1 ${rand}`
		do
			eval "adb -s '${deviceID}' shell input tap '$((${wm_size_width}/${unit}))' '$((${wm_size_height}/${unit}*(${unit}-1)))'"
			ACION_LIST="${ACION_LIST}.down_left"
			sleep 1			
		done
	fi
	
	rand=$(( $RANDOM % 100 ))
	if [ ${rand} -lt 25 ]
	then
		rand=$(( ( RANDOM % 5 )  + 1 ))
		for n in `seq 1 ${rand}`
		do
			eval "adb -s '${deviceID}' shell input tap '$((${wm_size_width}/${unit}*(${unit}-1)))' '$((${wm_size_height}/${unit}*(${unit}-1)))'"
			ACION_LIST="${ACION_LIST}.down_right"
			sleep 1			
		done
	fi
	
	checkSurfingLog
		
	rand=$(( $RANDOM % 100 ))	
	if [ ${rand} -lt 0 ]
	then
	        eval "adb -s '${deviceID}' shell \"am force-stop '${packageName}'\""	
		ACION_LIST="${ACION_LIST}.am_force-stop"
		sleep 1		
	fi
	
	echo "---------------------------------------------"
	echo "${ID_FILENAME}_ACION_LIST>>${ACION_LIST}"
	
	sleep ${POLLING_DELAY}
done	

END_TIME=`eval date +%Y%m%d%H%M`

pid=$(adb -s ${deviceID} shell ps | grep 'com.android.commands.monkey' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
echo "pid is [${pid}]"
KILL_STATUS=`adb shell kill -9 ${pid}` 
echo "KILL_STATUS is [${KILL_STATUS}]"

echo "SURFING_ACTIVITIES is [${SURFING_ACTIVITIES[@]}]"
echo "SURFING_ACTIVITIES# is [${#SURFING_ACTIVITIES[*]}]"
echo "throttle is [${throttle}]"
echo "duringHours is [${duringHours}]"
rm -f ./rawinfo_${ID_FILENAME}SURFING_ACTIVITIES.txt
for activity in ${SURFING_ACTIVITIES[@]}
do
	echo ${activity} >> ./rawinfo_${ID_FILENAME}_SURFING_ACTIVITIES_${START_TIME}.txt
done

echo "START_TIME is ${START_TIME}"
echo "EXPECT_END_TIME is ${EXPECT_END_TIME}"
echo "END_TIME is ${END_TIME}"
if [ ! -n "${error_reason}" ]
then
	error_reason=none
	END___BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")
else
#	END___BATTERY="notCheck"
	END___BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")	
fi
echo "START_BATTERY is [${START_BATTERY}]"
echo "END___BATTERY is [${END___BATTERY}]"
if [ ! -n "$(adb devices | grep ${deviceID})" ]
then
	echo "deviceID[${deviceID}] probably turn off!"
fi

TOTAL_ACTIVITY_NUM=0
if [ -e ${uploadRootDir}/AndroidManifest.xml ]
then
    echo "${uploadRootDir}/AndroidManifest.xml exist"
    TOTAL_ACTIVITY_NUM=$(cat ${uploadRootDir}/AndroidManifest.xml | grep "<activity" | wc -l)
    echo "TOTAL_ACTIVITY_NUM is [${TOTAL_ACTIVITY_NUM}]"
else
    echo "${uploadRootDir}/AndroidManifest.xml not exist"
fi

echo "TARGET_tombstones_NUM is [${TARGET_tombstones_NUM}]"
echo "TARGET_anr_NUM is [${TARGET_anr_NUM}]"

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${error_reason}\t${#SURFING_ACTIVITIES[*]}\t${TOTAL_ACTIVITY_NUM}\t${START_BATTERY}\t${END___BATTERY}\t${TARGET_tombstones_NUM}\t${TARGET_anr_NUM}\t${TARGET_STAYKILL_COUNT}" >> ./summary.txt
echo "START_TIME is ${START_TIME}"
echo "EXPECT_END_TIME is ${EXPECT_END_TIME}"
echo "END_TIME is ${END_TIME}"
echo "START_BATTERY is [${START_BATTERY}]"
echo "END___BATTERY is [${END___BATTERY}]"
if [ ! -n "$(adb devices | grep ${deviceID})" ]
then
	echo "deviceID[${deviceID}] probably turn off!"
fi
sleep 180
mkdir ./${START_TIME}
mv ./raw*.* ./${START_TIME}/