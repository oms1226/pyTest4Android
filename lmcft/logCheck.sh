#!/bin/sh
echo "this is ${0}"
start=`expr index "$0" /`
end=`expr index "$0" .sh`
ID_FILENAME=${0:$start:$(($end-$start-2))}
echo "ID_FILENAME is ${ID_FILENAME}"
INT_MAX=2147483647
UUID=$1
echo "UUID is ${UUID}"
phoneNum=$(echo ${UUID} | cut -f5 -d "]" | sed 's/\[//g' | sed 's/\]//g')
echo "phoneNum is ${phoneNum}"
git_branchName=$(echo ${UUID} | cut -f6 -d "]" | sed 's/\[//g' | sed 's/\]//g')
git_commitValue=$(echo ${UUID} | cut -f7 -d "]" | sed 's/\[//g' | sed 's/\]//g')
git_revCount=$(echo ${UUID} | cut -f8 -d "]" | sed 's/\[//g' | sed 's/\]//g')

deviceID=$2
echo "deviceID is ${deviceID}"

packageName=$3
echo "packageName is ${packageName}"

TIMEID=$4
echo "TIMEID is ${TIMEID}"
START_TIME=$(echo ${TIMEID} | cut -f1 -d "]" | sed 's/\[//g' | sed 's/\]//g')
EXPECT_END_TIME=$(echo ${TIMEID} | cut -f2 -d "]" | sed 's/\[//g' | sed 's/\]//g')
duringHours=$(echo ${TIMEID} | cut -f3 -d "]" | sed 's/\[//g' | sed 's/\]//g')
throttle=$(echo ${TIMEID} | cut -f4 -d "]" | sed 's/\[//g' | sed 's/\]//g')

POLLING_DELAY=$5

logTag=$6

initNumLogcat=$(adb -s ${deviceID} shell ps | grep logcat | wc -l)

rm -f ./rawinfo_${ID_FILENAME}_${START_TIME}.txt
eval "adb -s '${deviceID}' shell logcat -c"
LOGCAT_CMD="adb -s '${deviceID}' shell logcat DEBUG:F System.err:V AndroidRuntime:E '${logTag}':E *:S >> './rawinfo_${ID_FILENAME}_${START_TIME}.txt' &"
NUM=0


count=0
while [ ${EXPECT_END_TIME} -gt  $(date +%Y%m%d%H%M) ]
do
	if [ ! -n "$(adb devices | grep ${deviceID})" ]
	then
		echo "deviceID[${deviceID}] probably turn off!"
		break
	fi
	
	isPackage=$(adb -s ${deviceID} shell ps | grep ${packageName})
	if [ ! -n "$isPackage" ]
	then
		continue	
	fi

	currentNumLogcat=$(adb -s ${deviceID} shell ps | grep logcat | wc -l)
	echo "initNumLogcat is [${initNumLogcat}]"	
	echo "currentNumLogcat is [${currentNumLogcat}]"
	if [ $(($currentNumLogcat-$initNumLogcat)) -eq 0 ]
	then
		eval ${LOGCAT_CMD}
		echo "LOGCAT_CMD is ${LOGCAT_CMD}"		
	fi
	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`

	sleep ${POLLING_DELAY}
done

for pid in $(adb -s ${deviceID} shell ps | grep 'logcat' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
do
	echo "pid is [${pid}]"
	KILL_STATUS=`adb -s ${deviceID} shell kill -9 ${pid}`
	echo "KILL_STATUS is [${KILL_STATUS}]"
done
sleep 5

for pid in $(adb -s ${deviceID} shell ps | grep 'log' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
do
	echo "pid is [${pid}]"
	KILL_STATUS=`adb -s ${deviceID} shell kill -9 ${pid}`
	echo "KILL_STATUS is [${KILL_STATUS}]"
done
sleep 5

#cat rawinfo_logCheck_201703230010.txt | grep com.skt.prod.tmessage | grep -v " E Yorum" | cut -f1-2 -d " " | uniq | wc -l
#cat rawinfo_logCheck_201703230010.txt | grep " E Yorum" | cut -f1-2 -d " " | uniq | wc -l
#cat rawinfo_logCheck_201703230010.txt | grep " E Yorum" | sed 's/  */ /g' | cut -f 5- -d " " | uniq | wc -l
NUM=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep ${packageName} | grep -v " E ${logTag}" | cut -f1-2 -d " " | uniq | wc -l)
TARGET_E_NUM=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep " E ${logTag}" | cut -f1-2 -d " " | uniq | wc -l)
TARGET_E_NUM_UNIQSTR=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep " E ${logTag}" | sed 's/  */ /g' | cut -f 5- -d " " | uniq | wc -l)
TARGET_PID_NUM=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep "${logTag}" | cut -f3 -d " " | uniq | wc -l)

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${NUM}\t${TARGET_E_NUM}\t${TARGET_E_NUM_UNIQSTR}\t${TARGET_PID_NUM}" >> ./summary.txt

cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep ${packageName} | grep -v " E ${logTag}" | cut -f1-2 -d " " | uniq >> ./rawinfo_${ID_FILENAME}_${START_TIME}_onlyUniqCrash.txt
while read uniqWord
do
	echo "uniqWord is [${uniqWord}]"
	tag=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep "${uniqWord}" | sed 's/  */ /g' | cut -f6 -d " " | head -1)
	echo "tag is [${tag}]"	
	cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep -A50 -B50 "${uniqWord}" | grep "${tag}" >> ./rawinfo_${ID_FILENAME}_${git_revCount}_onlyUniqCrash.txt
done < ./rawinfo_${ID_FILENAME}_${START_TIME}_onlyUniqCrash.txt