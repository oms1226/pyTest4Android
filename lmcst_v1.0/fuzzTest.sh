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
	#PIXEL NOS
	if [[ "${deviceID}" == *"HT"* ]]
	then
	    phoneNumLineNum_Index=14
	else
        #SM-G930S NOS
        phoneNumLineNum_Index=15
	fi
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
packageName=com.skt.prod.dialer
launchactivityName=com.skt.prod.dialer.activities.main.MainActivity
echo "packageName is ${packageName}"
logTag=TPhoneLite
echo "logTag is ${logTag}"
#lintLinkRootUrl=file://172.23.107.213/build/lint
lintLinkRootUrl="none"
echo "lintLinkRootUrl is [${lintLinkRootUrl}]"
PYTHONEXEC=/cygdrive/c/Python27/python.exe
APPKILL=false
RANDOM_SEED=1
RANDOM=${RANDOM_SEED}
################################################################################
echo "this is ${0}"
if [[ "$(uname -s)" == *"Darwin"* ]]
then
#mac patch start point!!
    start=`expr "$0" : /`
    end=`expr index "$0" .sh`
else
    start=`expr index "$0" /`
    end=`expr index "$0" .sh`
fi
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
#to be deleted!
#throttle=1000
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
#duringHours=1
echo "duringHours is ${duringHours}"
#throttle=1500;retryCount=30000;201702222000 - 201702230032

START_TIME=`eval date +%Y%m%d%H%M`
echo "START_TIME is ${START_TIME}"

EXPECT_END_TIME=`eval date +%Y%m%d%H%M -d '+${duringHours}hours'`
echo "EXPECT_END_TIME is ${EXPECT_END_TIME}"

POLLING_DELAY=1

UUID=$(adb -s ${deviceID} shell getprop | grep 'ro.product.manufacturer' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":")
UUID=${UUID}$(adb -s ${deviceID} shell getprop | grep 'ro.product.model' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":")
UUID=${UUID}$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.release' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":")
UUID=${UUID}$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.incremental' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":")
UUID=${UUID}[${phoneNum}]
UUID=${UUID}[${POLLING_DELAY}]

echo "ro.product.manufacturer" "$(adb -s ${deviceID} shell getprop | grep 'ro.product.manufacturer' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":")" >> ./${ID_FILENAME}_json.txt
echo "ro.product.model" "$(adb -s ${deviceID} shell getprop | grep 'ro.product.model' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":")" >> ./${ID_FILENAME}_json.txt
echo "ro.build.version.release" "$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.release' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":")" >> ./${ID_FILENAME}_json.txt
echo "ro.build.version.incremental" "$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.incremental' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":")" >> ./${ID_FILENAME}_json.txt
echo "phoneNum" "$phoneNum" >> ./${ID_FILENAME}_json.txt
echo "POLLING_DELAY" "$POLLING_DELAY" >> ./${ID_FILENAME}_json.txt

TIMEID=[${START_TIME}][${EXPECT_END_TIME}][${duringHours}][${throttle}]
echo "TIMEID is ${TIMEID}"

containInWordsCount=0
function containInSuppressedWords ()
{
	#in the middle of hanging all system
	containInWordsCount=0
	
	if [ ! -n "$(cat ./rawinfo_${ID_FILENAME}_windows.txt)" ]; then
		echo "fileContent is nothing!"
		containInWordsCount=9999
	fi
	#generic_x86_64:/ # dumpsys window windows
	#Can't find service: window
	TARGET_STRING="find service: window"
	eval "grep -c -i '${TARGET_STRING}' ./rawinfo_${ID_FILENAME}_windows.txt > ./MATCH_COUNT.txt"
	matchcount=$(cat ./MATCH_COUNT.txt)
	rm -f ./MATCH_COUNT.txt
	containInWordsCount=$((${matchcount} + ${containInWordsCount}))
	
	#generic_x86_64:/ # dumpsys window windows
	#Service dumps disabled due to hung system process.
	TARGET_STRING="Service dumps disabled due to hung system process."
	eval "grep -c -i '${TARGET_STRING}' ./rawinfo_${ID_FILENAME}_windows.txt > ./MATCH_COUNT.txt"
	matchcount=$(cat ./MATCH_COUNT.txt)
	rm -f ./MATCH_COUNT.txt
	containInWordsCount=$((${matchcount} + ${containInWordsCount}))

	echo "containInWordsCount is ${containInWordsCount}"
	
	if [ ! -n "$(adb devices | grep ${deviceID})" ]
	then
		echo "deviceID[${deviceID}] probably turn off!"
		containInWordsCount=0
	fi
}

`adb -s ${deviceID} shell dumpsys window windows > rawinfo_${ID_FILENAME}_windows.txt`
sleep ${POLLING_DELAY}
containInSuppressedWords
while [ ${containInWordsCount} -gt  0 ]
do
	#root      1297  1     1342620 84204 poll_sched 7566343957aa S zygote64
	pid=$(adb -s ${deviceID} shell ps | grep 'zygote' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
	echo "pid[zygote] is [${pid}]"
	KILL_STATUS=`adb shell kill -9 ${pid}` 
	echo "KILL_STATUS is [${KILL_STATUS}]"		
	
	pid=$(adb -s ${deviceID} shell ps | grep 'zygote64' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
	echo "pid[zygote64] is [${pid}]"
	KILL_STATUS=`adb shell kill -9 ${pid}` 
	echo "KILL_STATUS is [${KILL_STATUS}]"	
	sleep 120
	`adb -s ${deviceID} shell dumpsys window windows > rawinfo_${ID_FILENAME}_windows.txt`
	sleep ${POLLING_DELAY}
	containInSuppressedWords
done

unit=20
wm_size=$(adb -s ${deviceID} shell wm size | tail -n 1)
wm_size_width=$(echo ${wm_size} | cut -f3 -d " " | cut -f1 -d "x" | sed 's/\r//g' | sed 's/\n//g')
wm_size_height=$(echo ${wm_size} | cut -f3 -d " " | cut -f2 -d "x" | sed 's/\r//g' | sed 's/\n//g')
echo "wm_size_width is [${wm_size_width}]"
echo "wm_size_height is [${wm_size_height}]"
echo "wm_size_width" "$wm_size_width" >> ./${ID_FILENAME}_json.txt
echo "wm_size_height" "$wm_size_height" >> ./${ID_FILENAME}_json.txt

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

if [ "$1" ]
then
    lmcst_ratio=${1}
    shift
else
    lmcst_ratio=0
fi
echo "lmcst_ratio" "$lmcst_ratio" >> ./${ID_FILENAME}_json.txt

if [ "$1" ]
then
    TARGET_Classifier_XML=${1}
    shift
else
    TARGET_Classifier_XML=NONE
fi
echo "TARGET_Classifier_XML" "$TARGET_Classifier_XML" >> ./${ID_FILENAME}_json.txt

if [ "$isPreProcess" == "yes" ]
then
	preProcessShellName=preProcessCheck
	echo "./${preProcessShellName}.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${uploadRootDir}' '${lintLinkRootUrl}' '${lmcst_ratio}'"
	eval "./${preProcessShellName}.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${uploadRootDir}' '${lintLinkRootUrl}' '${lmcst_ratio}'"
	if [ "$?" == "0" ]
	then
		echo "preProcessCheck.sh success"
	else
		echo "preProcessCheck.sh is failed"
		exit 1
	fi
fi
echo "isPreProcess" "$isPreProcess" >> ./${ID_FILENAME}_json.txt

TOTAL_ACTIVITY_NUM=0
if [ -e ${uploadRootDir}/AndroidManifest.xml ]
then
    echo "${uploadRootDir}/AndroidManifest.xml exist"
    TOTAL_ACTIVITY_NUM=$(cat ${uploadRootDir}/AndroidManifest.xml | grep "<activity" | wc -l)
    echo "TOTAL_ACTIVITY_NUM is [${TOTAL_ACTIVITY_NUM}]"
else
    echo "${uploadRootDir}/AndroidManifest.xml not exist"
fi


if [ "$isPreProcess" != "yes" ]
then
	git_branchName=idontknow
	git_revCount=0
	git_commitValue=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
elif [ -f ./summary.txt ]
then
	sleep 120
	preProcessRow=$(cat ./summary.txt | grep ${preProcessShellName} | grep ${START_TIME})
	if [ ${#preProcessRow[@]} -le 0 ]
	then
		git_branchName=idontknow
		git_revCount=0
		git_commitValue=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
	else
		git_branchName=$(cat ./summary.txt | tail -n 1 | cut -f4 | sed 's/\r//g')
		git_revCount=$(cat ./summary.txt | tail -n 1 | cut -f6 | sed 's/\r//g')
		git_commitValue=$(cat ./summary.txt | tail -n 1 | cut -f5 | sed 's/\r//g')
	fi
fi

echo "git_branchName is [${git_branchName}]"
echo "git_revCount is [${git_revCount}]"
echo "git_commitValue is [${git_commitValue}]"

UUID=${UUID}[${git_branchName}]
UUID=${UUID}[${git_commitValue}]
UUID=${UUID}[${git_revCount}]
if [ ${lmcst_ratio} -gt 0 ]
then
    UUID=${UUID}[lmcst][${lmcst_ratio}][${TARGET_Classifier_XML}]
else
    UUID=${UUID}[lmcft][0][${TARGET_Classifier_XML}]
fi

echo "UUID is ${UUID}"

START_BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")
sleep ${POLLING_DELAY}
echo "START_BATTERY is ${START_BATTERY}"

#eval "adb -s '${deviceID}' shell monkey -p com.skt.prod.tmessage -s 1 -v --throttle '${throttle}' --ignore-crashes --pct-syskeys 0 --pct-appswitch 10 --pct-touch 70 --pct-anyevent 20 '${retryCount}' &"
#eval "adb -s '${deviceID}' shell monkey -p com.skt.prod.tmessage -s 1 -v --throttle '${throttle}' --ignore-crashes --pct-syskeys 0 --pct-appswitch 10 --pct-touch 90 --pct-anyevent 0 '${retryCount}' &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -p '${packageName}' -s '${count}' -v --throttle '${throttle}' --ignore-crashes --pct-syskeys 0 --pct-appswitch 10 --pct-touch 45 --pct-anyevent 0 --pct-motion 45 '${retryCount}' &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -v --throttle '${throttle}' --pct-syskeys 5 --pct-anyevent 5 --pct-appswitch 20 --pct-touch 50 --pct-motion 20 -p '${packageName}' --bugreport --ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes 100 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -v --throttle '${throttle}' --pct-syskeys 5 --pct-anyevent 5 --pct-appswitch 20 --pct-touch 50 --pct-motion 20 -p '${packageName}' --bugreport 100 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -v --throttle '${throttle}' --pct-syskeys 5 --pct-anyevent 5 --pct-appswitch 20 --pct-touch 50 --pct-motion 20 -p '${packageName}' 100 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -v --throttle '${throttle}' --pct-syskeys 5 --pct-anyevent 5 --pct-appswitch 20 --pct-touch 50 --pct-motion 20 -p '${packageName}' 10 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -v --throttle '${throttle}' --pct-syskeys 5 --pct-anyevent 5 --pct-appswitch 20 --pct-touch 50 --pct-motion 20 -p '${packageName}' 1 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -v --pct-syskeys 5 --pct-anyevent 5 --pct-appswitch 20 --pct-touch 50 --pct-motion 20 -p '${packageName}' 100 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' --throttle '${throttle}' -v --pct-syskeys 5 --pct-anyevent 5 --pct-appswitch 20 --pct-touch 50 --pct-motion 20 100 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -v --throttle '${throttle}' --pct-syskeys 5 --pct-anyevent 5 --pct-appswitch 20 --pct-touch 50 --pct-motion 20 -p '${packageName}' 1000 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -v --throttle '${throttle}' -p '${packageName}' 1000 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -p '${packageName}' 1000 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -s '${count}' -p '${packageName}' --delay-appswitch 10000 1000 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey -v --throttle '${throttle}' -s '${count}' -p '${packageName}' --device-sleep-time 10000 1000 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey --kill-process-after-error --throttle '${throttle}' -s '${count}' -p '${packageName}' --device-sleep-time 10000 1000 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey --kill-process-after-error --throttle '${throttle}' -s '${count}' -p '${packageName}' 100 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey --throttle '${throttle}' -s '${count}' -p '${packageName}' 1000 &"
#MONKEY_CMD="adb -s '${deviceID}' shell monkey --throttle '${throttle}' -s '${count}' -p '${packageName}' --pct-touch 30 --pct-motion 10 --pct-flip 30 --pct-pinchzoom 10 --pct-appswitch 10 --pct-syskeys 5 --pct-anyevent 5 100 &"
MONKEY_CMD="adb -s '${deviceID}' shell monkey --throttle '${throttle}' -s '${count}' -p '${packageName}' --pct-touch 30 --pct-motion 10 --pct-flip 30 --pct-pinchzoom 10 --pct-appswitch 10 --pct-syskeys 5 --pct-anyevent 5 50 &"




#echo "./tmessageCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${isPreProcess}' '${lmcst_ratio}' &"
#if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
#then
	echo "./memCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
#fi
echo "./cpuCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then
	echo "./tempCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
fi
echo "./storageCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
#if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
#then
	echo "./tcpNetworkCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
#fi
#if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
#then
	echo "./logCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${logTag}' '${lmcst_ratio}' &"
#fi
if [ ${lmcst_ratio} -gt 0 ]
then
    echo "${PYTHONEXEC} scanning_adb_from_CascadeClassifier.py '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
fi
echo "${PYTHONEXEC} pyLogcatTracking.py '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"

#eval "./tmessageCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${isPreProcess}' > ./rawinfo_${ID_FILENAME}_tmessageLogging_${START_TIME}.txt &"
#read -p "Press enter to continue" nothing
sleep 30
#if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
#then
	eval "./memCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
	sleep ${POLLING_DELAY}
#fi
#if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
#then
	eval "./cpuCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
	sleep ${POLLING_DELAY}
#fi
if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then
	eval "./tempCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
	sleep ${POLLING_DELAY}
fi
#if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
#then
	eval "./storageCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
	sleep ${POLLING_DELAY}
#fi
#if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
#then
	eval "./tcpNetworkCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
	sleep ${POLLING_DELAY}
#fi
#if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
#then
	eval "./logCheck.sh '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${logTag}' '${lmcst_ratio}' &"
	sleep ${POLLING_DELAY}
#fi
if [ ${lmcst_ratio} -gt 0 ]
then
    eval "${PYTHONEXEC} scanning_adb_from_CascadeClassifier.py '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' &"
    sleep ${POLLING_DELAY}
fi

eval "${PYTHONEXEC} pyLogcatTracking.py '${UUID}' '${deviceID}' '${packageName}' '${TIMEID}' '${POLLING_DELAY}' '${lmcst_ratio}' /cygdrive/d/lmcft_log/pyLogcatTracking.log &"
sleep ${POLLING_DELAY}


SURFING_ACTIVITIES=()
SURFING_ACTIVITIES_PLUSDETAILS=()
function checkSurfingLog ()
{
	`adb -s ${deviceID} shell dumpsys window windows > rawinfo_${ID_FILENAME}_windows.txt`
	sleep ${POLLING_DELAY}
	containInSuppressedWords
	while [ ${containInWordsCount} -gt  0 ]
	do
		#root      1297  1     1342620 84204 poll_sched 7566343957aa S zygote64
		pid=$(adb -s ${deviceID} shell ps | grep 'zygote' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
		echo "pid[zygote] is [${pid}]"
		KILL_STATUS=`adb shell kill -9 ${pid}` 
		echo "KILL_STATUS is [${KILL_STATUS}]"	

		pid=$(adb -s ${deviceID} shell ps | grep 'zygote64' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
		echo "pid[zygote64] is [${pid}]"
		KILL_STATUS=`adb shell kill -9 ${pid}` 
		echo "KILL_STATUS is [${KILL_STATUS}]"	

		sleep 120
		`adb -s ${deviceID} shell dumpsys window windows > rawinfo_${ID_FILENAME}_windows.txt`	
		sleep ${POLLING_DELAY}
		containInSuppressedWords
	done
	`cat rawinfo_${ID_FILENAME}_windows.txt | grep 'Window #' | grep ${packageName} > rawinfo_${ID_FILENAME}_windows_Window#_${packageName}.txt`
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
	done < rawinfo_${ID_FILENAME}_windows_Window#_${packageName}.txt

    mFocusedApp=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'mFocusedApp' | sed 's/  */ /g' | sed 's/\r//g' | cut -f6 -d " " | sed 's/}//g' | sed 's/\///g' | sed 's/://g' | sed 's/ //g')
    #currentFocus=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'mCurrentFocus' | sed 's/  */ /g' | sed 's/\r//g' | cut -f4 -d " " | sed 's/}//g')
    currentFocusShort=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'mCurrentFocus' | sed 's/  */ /g' | sed 's/\r//g' | cut -f4 -d " " | sed 's/}//g' | rev | cut -f1 -d "." | rev | cut -f1 -d ":")
    winCount=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'Window #' | head -1  | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " " | sed 's/#//g')
    if [ ! -n "$winCount" ]
    then
        winCount=0
    fi
    lineCount=$(cat rawinfo_${ID_FILENAME}_windows.txt | wc -l)
    if [ ! -n "$lineCount" ]
    then
        lineCount=0
    fi
	currentDetail=${mFocusedApp}_win#${winCount}_total#${lineCount}_${currentFocusShort}
	isExist=false
    for detail in ${SURFING_ACTIVITIES_PLUSDETAILS[@]}
    do
        if [ ${detail} == ${currentDetail} ]
        then
            isExist=true
            break
        fi
    done
    if [ ${isExist} = false ] ; then
        SURFING_ACTIVITIES_PLUSDETAILS[${#SURFING_ACTIVITIES_PLUSDETAILS[*]}]=${currentDetail}
        echo "SURFING_ACTIVITIES_PLUSDETAILS just include new found [${currentDetail}]"
        echo "SURFING_ACTIVITIES_PLUSDETAILS# is [${#SURFING_ACTIVITIES_PLUSDETAILS[*]}]"
        eval "adb -s '${deviceID}' shell screencap -p '/sdcard/rawimg_${ID_FILENAME}_${currentDetail}_${START_TIME}.png'"
        eval "adb -s '${deviceID}' pull '/sdcard/rawimg_${ID_FILENAME}_${currentDetail}_${START_TIME}.png'"
        eval "adb -s '${deviceID}' shell rm '/sdcard/rawimg_${ID_FILENAME}_${currentDetail}_${START_TIME}.png'"
    fi

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
				TARGET_tombstones_NUM=`expr ${TARGET_tombstones_NUM} + 1`
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
				TARGET_anr_NUM=`expr ${TARGET_anr_NUM} + 1`
			else
			        eval "rm './raw_${ID_FILENAME}_${existTargetName}_${START_TIME}_${execTiime}_${fileName}'"
			fi		
			fileName=$(adb -s ${deviceID} shell ls -1 /data/${existTargetName} | tail -n 1 | sed 's/\r//g' | sed 's/\n//g')
		done
	        eval "adb -s '${deviceID}' shell rm -rf '/data/${existTargetName}'"	
	fi
	
	#currentFocus=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'mCurrentFocus' | sed 's/  */ /g' | sed 's/\r//g' | cut -f4 -d " " | sed 's/}//g')
	mFocusedApp=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'mFocusedApp' | grep "${packageName}" | sed 's/  */ /g' | sed 's/\r//g' | cut -f6 -d " " | sed 's/}//g' | sed 's/\///g' | sed 's/://g' | sed 's/ //g')
	echo "stay_count is [${stay_count}]"
	echo "previous_activityinWindows is [${previous_activityinWindows}]"
	echo "mFocusedApp is [${mFocusedApp}]"	
	if [ -n "$mFocusedApp" -a "${previous_activityinWindows}" == "${mFocusedApp}" ]
	then
		stay_count=`expr ${stay_count} + 1`
		if [ ${APPKILL} = true ] ; then
            if [ ${stay_count} -gt 10 ]
            then
                writeTrace "am_force-stop" ${packageName}
                eval "adb -s '${deviceID}' shell \"am force-stop '${packageName}'\""
                stay_count=0
                TARGET_STAYKILL_COUNT=`expr ${TARGET_STAYKILL_COUNT + 1`
                echo "TARGET_STAYKILL_COUNT is [${TARGET_STAYKILL_COUNT}]"
            fi
		fi
	else
		previous_activityinWindows=${mFocusedApp}
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

touchPointCount=0
function getTouchPointonLMCST ()
{
    touchPointCount=0
    tAction=""
    tX=0
    tY=0

    filename=$(ls -1 ./training | grep "${mFocusedApp}_win#${winCount}_total#${lineCount}_${currentFocusShort}" | head -n 1 | sed 's/\r//g' | sed 's/\n//g')
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
        touchPointCount=${index}
        if [ ${#touchPoints[*]} -gt 0 ]
        then
            targetTouchPoint=${touchPoints[$(( $RANDOM % ${index} ))]}
            echo "targetTouchPoint is ${targetTouchPoint}"
            tAction=$(echo ${targetTouchPoint} | cut -f1 -d ",")
            tX=$(echo ${targetTouchPoint} | cut -f2 -d ",")
            tY=$(echo ${targetTouchPoint} | cut -f3 -d ",")
        fi
    fi

    echo "tAction is ${tAction}"
    echo "tX is ${tX}"
    echo "tY is ${tY}"
}

MANUFACTURER="$(adb -s ${deviceID} shell getprop | grep 'ro.product.manufacturer' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"
MODEL="$(adb -s ${deviceID} shell getprop | grep 'ro.product.model' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"
OSVERSION="$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.release' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"
MANUFACTURERVERSION="$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.incremental' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"

#writeTrace tAction tX tY t1X t1Y
function writeTrace ()
{
    echo "MANUFACTURER" "$MANUFACTURER" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "MODEL" "$MODEL" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "OSVERSION" "$OSVERSION" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "MANUFACTURERVERSION" "$MANUFACTURERVERSION" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "MYNUM" "$phoneNum" >> ./${ID_FILENAME}_json_snapshot.txt

    echo "ID_FILENAME" "$ID_FILENAME" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "selfVersion" "1.0" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "execTime" "$(date +"%Y%m%d%H%M%S")" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "hostname" "$(hostname)" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "DEVICE_ID" "$deviceID" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "PACKAGENAME" "$packageName" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "git_branchName" "$git_branchName" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "git_commitValue" "$git_commitValue" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "git_revCount" "$git_revCount" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "START_TIME" "$START_TIME" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "EXPECT_END_TIME" "$EXPECT_END_TIME" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "duringHours" "$duringHours" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "throttle" "$throttle" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "POLLING_DELAY" "$POLLING_DELAY" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "RANDOM_SEED" "$RANDOM_SEED" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "APPKILL" "$APPKILL" >> ./${ID_FILENAME}_json_snapshot.txt

    echo "count" "$count" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "stay_count" "$stay_count" >> ./${ID_FILENAME}_json_snapshot.txt

    `adb -s ${deviceID} shell dumpsys window windows > rawinfo_${ID_FILENAME}_windows.txt`
    mFocusedApp=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'mFocusedApp' | grep "${packageName}" | sed 's/  */ /g' | sed 's/\r//g' | cut -f6 -d " " | sed 's/}//g' | sed 's/\///g' | sed 's/://g' | sed 's/ //g')
    if [ -n "$mFocusedApp" ]
    then
        echo "mFocusedApp" "${mFocusedApp}" >> ./${ID_FILENAME}_json_snapshot.txt
    fi
    if [ -n "$1" ]; then
        echo "tAction" "${1}" >> ./${ID_FILENAME}_json_snapshot.txt
        if [ "${1}" == "tap" ] ; then
            echo "tX" "${2}" >> ./${ID_FILENAME}_json_snapshot.txt
            echo "tY" "${3}" >> ./${ID_FILENAME}_json_snapshot.txt
        elif [ "${1}" == "swipe" ] ; then
            echo "tX" "${2}" >> ./${ID_FILENAME}_json_snapshot.txt
            echo "tY" "${3}" >> ./${ID_FILENAME}_json_snapshot.txt
            echo "t1X" "${4}" >> ./${ID_FILENAME}_json_snapshot.txt
            echo "t1Y" "${5}" >> ./${ID_FILENAME}_json_snapshot.txt
        elif [ "${1}" == "am_start" ] ; then
            echo "tT" "${2}" >> ./${ID_FILENAME}_json_snapshot.txt
        elif [ "${1}" == "am_force-stop" ] ; then
            echo "tT" "${2}" >> ./${ID_FILENAME}_json_snapshot.txt
        elif [ "${1}" == "kill" ] ; then
            echo "tT" "${2}" >> ./${ID_FILENAME}_json_snapshot.txt
        fi
    fi

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

while [ ${EXPECT_END_TIME} -gt  $(date +%Y%m%d%H%M) ]
do
	ACION_LIST=""
	
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
		rand=$(( $RANDOM % 100 ))
		if [ ${rand} -lt 0 ]
		then	
			echo ${MONKEY_CMD}		
			eval ${MONKEY_CMD}
			sleep ${POLLING_DELAY}
		fi
	fi
	
		
#	eval "adb -s '${deviceID}' shell input keyevent 91"
#	ACION_LIST="${ACION_LIST}.keyevent_91"
#	eval "adb -s '${deviceID}' shell input keyevent 164"	
#	ACION_LIST="${ACION_LIST}.keyevent_164"
	rand=$(adb -s ${deviceID} shell dumpsys activity recents | grep '* Recent #0' | grep "${packageName}")
	sleep ${POLLING_DELAY}
	if [ ! -n "$rand" ]
	then
        writeTrace "am_start" ${packageName}/${launchactivityName}
	    eval "adb -s '${deviceID}' shell \"am start -a android.intent.action.MAIN -n '${packageName}'/'${launchactivityName}'\""
		ACION_LIST="${ACION_LIST}.${launchactivityName}"
		sleep ${POLLING_DELAY}
	fi	

	checkSurfingLog
	
isMonkey=$(adb -s ${deviceID} shell ps | grep monkey)
if [ -n "$isMonkey" ]
then
	sleep ${POLLING_DELAY}	
	sleep ${POLLING_DELAY}	
	sleep ${POLLING_DELAY}	
	sleep ${POLLING_DELAY}	
else
	if [ -n "$(echo ${deviceID} | grep emulator)"  ] #"emulator"
	then
		rand=$(( $RANDOM % 100 ))
		if [ ${rand} -lt 0 ]
		then
		    echo "${PYTHONEXEC} incomingCallbyTelent.py"		
		    eval "${PYTHONEXEC} incomingCallbyTelent.py"
		fi
	fi

    tAction=""
	tX=0
	tY=0
	rand=$(( $RANDOM % 100 ))
	if [ ${rand} -lt ${lmcst_ratio} ]
	then
	    `adb -s ${deviceID} shell dumpsys window windows > rawinfo_${ID_FILENAME}_windows.txt`
	    sleep ${POLLING_DELAY}
	    mFocusedApp=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'mFocusedApp' | sed 's/  */ /g' | sed 's/\r//g' | cut -f6 -d " " | sed 's/}//g' | sed 's/\///g' | sed 's/://g' | sed 's/ //g')
	    currentFocusShort=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'mCurrentFocus' | sed 's/  */ /g' | sed 's/\r//g' | cut -f4 -d " " | sed 's/}//g' | rev | cut -f1 -d "." | rev | cut -f1 -d ":")
	    winCount=$(cat rawinfo_${ID_FILENAME}_windows.txt | grep 'Window #' | head -1  | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " " | sed 's/#//g')
	    if [ ! -n "$winCount" ]
	    then
	        winCount=0
	    fi

	    lineCount=$(cat rawinfo_${ID_FILENAME}_windows.txt | wc -l)
	    if [ ! -n "$lineCount" ]
	    then
	        lineCount=0
	    fi
            getTouchPointonLMCST
	    if [ ${tX} -gt 0 -a "${tAction}" == "tap" ]
	    then
                writeTrace "tap" ${tX} ${tY}
                eval "adb -s '${deviceID}' shell input tap '${tX}' '${tY}'"
                ACION_LIST="${ACION_LIST}.clickOnTouch"
                sleep ${POLLING_DELAY}			
	    else
                tAction=""
                tX=0
                tY=0
		touchPointCount=0
	    fi
	    if [ ${touchPointCount} -gt 0 ]
	    then
	            rand=$(( $RANDOM % ${touchPointCount} ))
	            for n in `seq 1 ${rand}`
	            do
		        getTouchPointonLMCST
			if [ ${tX} -gt 0 ]
			then
			    if [ "${tAction}" == "tap" ]
			    then
			            writeTrace "tap" ${tX} ${tY}
		                eval "adb -s '${deviceID}' shell input tap '${tX}' '${tY}'"
		                ACION_LIST="${ACION_LIST}.clickOnTouch"
		                sleep ${POLLING_DELAY}
		            else
		                tAction=""
		                tX=0
		                tY=0
		            fi
			else 
			    break
			fi	    
	            done	
	    fi
        fi

	if [ ${tX} -eq 0 ]
	then
        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 33 ]
        then
            rand=$(( ( $RANDOM % 7 )  + 1 ))
            for n in `seq 1 ${rand}`
            do
                writeTrace "keyevent_back"
                eval "adb -s '${deviceID}' shell input keyevent 4"
                ACION_LIST="${ACION_LIST}.keyevent_back"
                sleep ${POLLING_DELAY}
                checkSurfingLog
            done
        fi
        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 20 ]
        then
            writeTrace "keyevent_home"
            eval "adb -s '${deviceID}' shell input keyevent 3"
            ACION_LIST="${ACION_LIST}.keyevent_home"
            sleep ${POLLING_DELAY}
            checkSurfingLog
        fi
	
	rand=$(adb -s ${deviceID} shell dumpsys activity recents | grep '* Recent #0' | grep "${packageName}")	
	sleep ${POLLING_DELAY}
	if [ ! -n "$rand" ]
	then
        writeTrace "am_start" ${packageName}/${launchactivityName}
	    eval "adb -s '${deviceID}' shell \"am start -a android.intent.action.MAIN -n '${packageName}'/'${launchactivityName}'\""
		ACION_LIST="${ACION_LIST}.${launchactivityName}"
		sleep ${POLLING_DELAY}
	fi
	
        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 50 ]
        then
            mCallState=$(adb -s ${deviceID} shell dumpsys telephony.registry | grep mCallState | cut -f2 -d "=" | sed 's/\r//g' | sed 's/\n//g')
	    sleep ${POLLING_DELAY}
            echo "mCallState is [${mCallState}]"
            #0 indicates idle,
            #1 = ringing and
            #2 = active call
            if [ ${mCallState} -eq 2 ]
            then
                writeTrace "keyevent_endcall"
	            eval "adb -s '${deviceID}' shell input keyevent KEYCODE_ENDCALL"
	            ACION_LIST="${ACION_LIST}.keyevent_endcall"
	            sleep ${POLLING_DELAY}	    
	    fi
        fi	


        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 25 ]
        then
            rand=$(( ( $RANDOM % 10 )  + 1 ))
            for n in `seq 1 ${rand}`
            do
                writeTrace "swipe" $((${wm_size_width}/2)) $((${wm_size_height}/4)) $((${wm_size_width}/2)) $((${wm_size_height}/2))
                eval "adb -s '${deviceID}' shell input swipe '$((${wm_size_width}/2))' '$((${wm_size_height}/4))' '$((${wm_size_width}/2))' '$((${wm_size_height}/2))' 100"
                ACION_LIST="${ACION_LIST}.up->down"
                sleep ${POLLING_DELAY}
            done
        fi

        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 25 ]
        then
            rand=$(( ( $RANDOM % 10 )  + 1 ))
            for n in `seq 1 ${rand}`
            do
                writeTrace "swipe" $((${wm_size_width}/2)) $((${wm_size_height}/4*3)) $((${wm_size_width}/2)) $((${wm_size_height}/2))
                eval "adb -s '${deviceID}' shell input swipe '$((${wm_size_width}/2))' '$((${wm_size_height}/4*3))' '$((${wm_size_width}/2))' '$((${wm_size_height}/2))' 100"
                ACION_LIST="${ACION_LIST}.down->up"
                sleep ${POLLING_DELAY}
            done
        fi

        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 25 ]
        then
            rand=$(( ( RANDOM % 5 )  + 1 ))
            for n in `seq 1 ${rand}`
            do
                writeTrace "tap" $((${wm_size_width}/${unit})) $((${wm_size_height}/${unit}))
                eval "adb -s '${deviceID}' shell input tap '$((${wm_size_width}/${unit}))' '$((${wm_size_height}/${unit}))'"
                ACION_LIST="${ACION_LIST}.up_left"
                sleep ${POLLING_DELAY}
            done
        fi

        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 25 ]
        then
            rand=$(( ( RANDOM % 5 )  + 1 ))
            for n in `seq 1 ${rand}`
            do
                writeTrace "tap" $((${wm_size_width}/${unit}*(${unit}-1))) $((${wm_size_height}/${unit}))
                eval "adb -s '${deviceID}' shell input tap '$((${wm_size_width}/${unit}*(${unit}-1)))' '$((${wm_size_height}/${unit}))'"
                ACION_LIST="${ACION_LIST}.up_right"
                sleep ${POLLING_DELAY}
            done
        fi

        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 25 ]
        then
            rand=$(( ( $RANDOM % 5 )  + 1 ))
            for n in `seq 1 ${rand}`
            do
                writeTrace "tap" $((${wm_size_width}/${unit})) $((${wm_size_height}/${unit}*(${unit}-1)))
                eval "adb -s '${deviceID}' shell input tap '$((${wm_size_width}/${unit}))' '$((${wm_size_height}/${unit}*(${unit}-1)))'"
                ACION_LIST="${ACION_LIST}.down_left"
                sleep ${POLLING_DELAY}
            done
        fi

        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 25 ]
        then
            rand=$(( ( $RANDOM % 5 )  + 1 ))
            for n in `seq 1 ${rand}`
            do
                writeTrace "tap" $((${wm_size_width}/${unit}*(${unit}-1))) $((${wm_size_height}/${unit}*(${unit}-1)))
                eval "adb -s '${deviceID}' shell input tap '$((${wm_size_width}/${unit}*(${unit}-1)))' '$((${wm_size_height}/${unit}*(${unit}-1)))'"
                ACION_LIST="${ACION_LIST}.down_right"
                sleep ${POLLING_DELAY}
            done
        fi
	
        rand=$(( $RANDOM % 100 ))
        if [ ${rand} -lt 20 ]
        then
            rand=$(( ( $RANDOM % 10 ) + 1 ))
            for n in `seq 1 ${rand}`
	    do
		x=$(( ( $RANDOM % ${unit} ) + 1 ))
		y=$(( ( $RANDOM % ${unit} ) + 1 ))
        writeTrace "tap" $((${wm_size_width}/${x})) $((${wm_size_height}/${y}))
        eval "adb -s '${deviceID}' shell input tap '$((${wm_size_width}/${x}))' '$((${wm_size_height}/${y}))'"
        ACION_LIST="${ACION_LIST}.x[$((${wm_size_width}/${x}))]_y[$((${wm_size_height}/${y}))]"
        sleep ${POLLING_DELAY}
        done
        fi	

        checkSurfingLog
		if [ ${APPKILL} = true ] ; then
            rand=$(( $RANDOM % 100 ))
            if [ ${rand} -lt 0 ]
            then
                writeTrace "am_force-stop" ${packageName}
                eval "adb -s '${deviceID}' shell \"am force-stop '${packageName}'\""
                ACION_LIST="${ACION_LIST}.am_force-stop"
                sleep ${POLLING_DELAY}
            fi
        fi
    fi
	if [ -n "$(echo ${deviceID} | grep emulator)"  ] #"emulator"
	then	
	        rand=$(( $RANDOM % 100 ))
	        if [ ${rand} -lt 0 ] #not working!
	        then
			#radio     6354  5862  1471524 73828    ep_poll 7e4ccdf2a62a S com.android.phone
			#in case of emulator, often not using data. However not found reason. So. randomly kill com.android.phone!
			pid=$(adb -s ${deviceID} shell ps | grep 'rild' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
			echo "pid[rild] is [${pid}]"
			writeTrace "kill" "rild"
			KILL_STATUS=`adb shell kill -9 ${pid}` 
			echo "KILL_STATUS is [${KILL_STATUS}]"
			
			pid=$(adb -s ${deviceID} shell ps | grep 'com.android.phone' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
			echo "pid[com.android.phone] is [${pid}]"
			writeTrace "kill" "com.android.phone"
			KILL_STATUS=`adb shell kill -9 ${pid}` 
			echo "KILL_STATUS is [${KILL_STATUS}]"
			sleep 5
		fi
	fi

fi
	echo "---------------------------------------------"
	echo "${ID_FILENAME}_ACION_LIST>>${ACION_LIST}"
	
	sleep ${POLLING_DELAY}
done	

END_TIME=`eval date +%Y%m%d%H%M`

pid=$(adb -s ${deviceID} shell ps | grep 'com.android.commands.monkey' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
sleep ${POLLING_DELAY}
echo "pid[monkey] is [${pid}]"
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

for activity in ${SURFING_ACTIVITIES_PLUSDETAILS[@]}
do
	echo ${activity} >> ./rawinfo_${ID_FILENAME}_SURFING_ACTIVITIES_PLUSDETAILS_${START_TIME}.txt
done

echo "START_TIME is ${START_TIME}"
echo "EXPECT_END_TIME is ${EXPECT_END_TIME}"
echo "END_TIME is ${END_TIME}"
if [ ! -n "${error_reason}" ]
then
	error_reason=none
	END___BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")
	sleep ${POLLING_DELAY}
else
#	END___BATTERY="notCheck"
	END___BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")	
	sleep ${POLLING_DELAY}
fi
echo "START_BATTERY is [${START_BATTERY}]"
echo "END___BATTERY is [${END___BATTERY}]"
if [ ! -n "$(adb devices | grep ${deviceID})" ]
then
	echo "deviceID[${deviceID}] probably turn off!"
fi

echo "TARGET_tombstones_NUM is [${TARGET_tombstones_NUM}]"
echo "TARGET_anr_NUM is [${TARGET_anr_NUM}]"

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${error_reason}\t${#SURFING_ACTIVITIES[*]}\t${TOTAL_ACTIVITY_NUM}\t${START_BATTERY}\t${END___BATTERY}\t${TARGET_tombstones_NUM}\t${TARGET_anr_NUM}\t${TARGET_STAYKILL_COUNT}\t${#SURFING_ACTIVITIES_PLUSDETAILS[*]}" >> ./summary.txt

echo "START_TIME is ${START_TIME}"
echo "EXPECT_END_TIME is ${EXPECT_END_TIME}"
echo "END_TIME is ${END_TIME}"
echo "START_BATTERY is [${START_BATTERY}]"
echo "END___BATTERY is [${END___BATTERY}]"

echo "MANUFACTURER" "$MANUFACTURER" >> ./${ID_FILENAME}_json.txt
echo "MODEL" "$MODEL" >> ./${ID_FILENAME}_json.txt
echo "OSVERSION" "$OSVERSION" >> ./${ID_FILENAME}_json.txt
echo "MANUFACTURERVERSION" "$MANUFACTURERVERSION" >> ./${ID_FILENAME}_json.txt
echo "MYNUM" "$phoneNum" >> ./${ID_FILENAME}_json.txt

echo "hostname" "$(hostname)" >> ./${ID_FILENAME}_json.txt
echo "UUID" "$UUID" >> ./${ID_FILENAME}_json.txt
echo "DEVICE_ID" "$deviceID" >> ./${ID_FILENAME}_json.txt
echo "PACKAGENAME" "$packageName" >> ./${ID_FILENAME}_json.txt
echo "git_branchName" "$git_branchName" >> ./${ID_FILENAME}_json.txt
echo "git_commitValue" "$git_commitValue" >> ./${ID_FILENAME}_json.txt
echo "git_revCount" "$git_revCount" >> ./${ID_FILENAME}_json.txt
echo "ID_FILENAME" "$ID_FILENAME" >> ./${ID_FILENAME}_json.txt
echo "START_TIME" "$START_TIME" >> ./${ID_FILENAME}_json.txt
echo "EXPECT_END_TIME" "$EXPECT_END_TIME" >> ./${ID_FILENAME}_json.txt
echo "duringHours" "$duringHours" >> ./${ID_FILENAME}_json.txt
echo "throttle" "$throttle" >> ./${ID_FILENAME}_json.txt
echo "RANDOM_SEED" "$RANDOM_SEED" >> ./${ID_FILENAME}_json.txt
echo "count" "$count" >> ./${ID_FILENAME}_json.txt
echo "error_reason" "$error_reason" >> ./${ID_FILENAME}_json.txt
echo "SURFING_ACTIVITIES" "${#SURFING_ACTIVITIES[*]}" >> ./${ID_FILENAME}_json.txt
echo "TOTAL_ACTIVITY_NUM" "$TOTAL_ACTIVITY_NUM" >> ./${ID_FILENAME}_json.txt
echo "START_BATTERY" "$START_BATTERY" >> ./${ID_FILENAME}_json.txt
echo "END___BATTERY" "$END___BATTERY" >> ./${ID_FILENAME}_json.txt
echo "TARGET_tombstones_NUM" "$TARGET_tombstones_NUM" >> ./${ID_FILENAME}_json.txt
echo "TARGET_anr_NUM" "$TARGET_anr_NUM" >> ./${ID_FILENAME}_json.txt
echo "APPKILL" "$APPKILL" >> ./${ID_FILENAME}_json.txt
echo "TARGET_STAYKILL_COUNT" "$TARGET_STAYKILL_COUNT" >> ./${ID_FILENAME}_json.txt
echo "SURFING_ACTIVITIES_PLUSDETAILS" "${#SURFING_ACTIVITIES_PLUSDETAILS[*]}" >> ./${ID_FILENAME}_json.txt

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


if [ ! -n "$(adb devices | grep ${deviceID})" ]
then
	echo "deviceID[${deviceID}] probably turn off!"
fi
sleep 180
mkdir ./${START_TIME}
mv ./raw*.* ./${START_TIME}/