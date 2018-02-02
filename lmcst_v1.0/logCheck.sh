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
git_branchName=$(echo ${UUID} | cut -f7 -d "]" | sed 's/\[//g' | sed 's/\]//g')
git_commitValue=$(echo ${UUID} | cut -f8 -d "]" | sed 's/\[//g' | sed 's/\]//g')
git_revCount=$(echo ${UUID} | cut -f9 -d "]" | sed 's/\[//g' | sed 's/\]//g')

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

lmcst_ratio=$7
echo "lmcst_ratio is ${lmcst_ratio}"

initNumLogcat=$(adb -s ${deviceID} shell ps | grep logcat | wc -l)

rm -f ./rawinfo_${ID_FILENAME}_${START_TIME}.txt
eval "adb -s '${deviceID}' shell logcat -c"
LOGCAT_CMD="adb -s '${deviceID}' shell logcat DEBUG:F System.err:V AndroidRuntime:E ActivityManager:E '${logTag}':E *:S >> './rawinfo_${ID_FILENAME}_${START_TIME}.txt' &"
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
for pid in $(adb -s ${deviceID} shell ps | grep 'logcat' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
do
	echo "pid[logcat] is [${pid}]"
	KILL_STATUS=`adb -s ${deviceID} shell kill -9 ${pid}`
	echo "KILL_STATUS is [${KILL_STATUS}]"
	sleep 5
done
		eval ${LOGCAT_CMD}
		echo "LOGCAT_CMD is ${LOGCAT_CMD}"		
	fi
	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`

	sleep ${POLLING_DELAY}
done

for pid in $(adb -s ${deviceID} shell ps | grep 'logcat' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
do
	echo "pid[logcat] is [${pid}]"
	KILL_STATUS=`adb -s ${deviceID} shell kill -9 ${pid}`
	echo "KILL_STATUS is [${KILL_STATUS}]"
	sleep 5
done

#for pid in $(adb -s ${deviceID} shell ps | grep 'log' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
#do
#	echo "pid[log] is [${pid}]"
#	KILL_STATUS=`adb -s ${deviceID} shell kill -9 ${pid}`
#	echo "KILL_STATUS is [${KILL_STATUS}]"
#	sleep 5
#done

#cat rawinfo_logCheck_201703230010.txt | grep com.skt.prod.tmessage | grep -v " E Yorum" | cut -f1-2 -d " " | uniq | wc -l
#cat rawinfo_logCheck_201703230010.txt | grep " E Yorum" | cut -f1-2 -d " " | uniq | wc -l
#cat rawinfo_logCheck_201703230010.txt | grep " E Yorum" | sed 's/  */ /g' | cut -f 5- -d " " | uniq | wc -l
NUM=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep ${packageName} | grep -v " E ${logTag}" | cut -f1-2 -d " " | uniq | wc -l)
TARGET_E_NUM=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep " E ${logTag}" | cut -f1-2 -d " " | uniq | wc -l)
TARGET_E_NUM_UNIQSTR=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep " E ${logTag}" | sed 's/  */ /g' | cut -f 5- -d " " | uniq | wc -l)
TARGET_PID_NUM=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep "${logTag}" | cut -f3 -d " " | uniq | wc -l)

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${NUM}\t${TARGET_E_NUM}\t${TARGET_E_NUM_UNIQSTR}\t${TARGET_PID_NUM}" >> ./summary.txt


MANUFACTURER="$(adb -s ${deviceID} shell getprop | grep 'ro.product.manufacturer' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"
MODEL="$(adb -s ${deviceID} shell getprop | grep 'ro.product.model' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"
OSVERSION="$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.release' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"
MANUFACTURERVERSION="$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.incremental' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"

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
echo "count" "$count" >> ./${ID_FILENAME}_json.txt

echo "NUM" "$NUM" >> ./${ID_FILENAME}_json.txt
echo "TARGET_E_NUM" "$TARGET_E_NUM" >> ./${ID_FILENAME}_json.txt
echo "TARGET_E_NUM_UNIQSTR" "$TARGET_E_NUM_UNIQSTR" >> ./${ID_FILENAME}_json.txt
echo "TARGET_PID_NUM" "$TARGET_PID_NUM" >> ./${ID_FILENAME}_json.txt

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


cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep ${packageName} | grep -v " E ${logTag}" | cut -f1-2 -d " " | uniq >> ./rawinfo_${ID_FILENAME}_${START_TIME}_onlyUniqCrash.txt
while read uniqWord
do
	echo "uniqWord is [${uniqWord}]"
	tag=$(cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep "${uniqWord}" | sed 's/  */ /g' | cut -f6 -d " " | head -1)
	echo "tag is [${tag}]"	
	cat ./rawinfo_${ID_FILENAME}_${START_TIME}.txt | grep -A50 -B50 "${uniqWord}" | grep "${tag}" >> ./rawinfo_${ID_FILENAME}_${git_revCount}_onlyUniqCrash.txt
done < ./rawinfo_${ID_FILENAME}_${START_TIME}_onlyUniqCrash.txt