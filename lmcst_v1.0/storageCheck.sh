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

lmcst_ratio=$6
echo "lmcst_ratio is ${lmcst_ratio}"

AVG=0
MAX=0
MIN=${INT_MAX}
INIT=0

AVG_CACHE=0
MAX_CACHE=0
MIN_CACHE=${INT_MAX}
INIT_CACHE=0

count=0

result=0
result1=0

MANUFACTURER="$(adb -s ${deviceID} shell getprop | grep 'ro.product.manufacturer' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"
MODEL="$(adb -s ${deviceID} shell getprop | grep 'ro.product.model' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"
OSVERSION="$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.release' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"
MANUFACTURERVERSION="$(adb -s ${deviceID} shell getprop | grep 'ro.build.version.incremental' | sed 's/  */ /g' | sed 's/ //g' | sed 's/\r//g' | cut -f2 -d ":" | sed 's/\[//g' | sed 's/\]//g')"


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

    echo "count" "$count" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "STORAGE" "$result1" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "STORAGE_CACHE" "$result" >> ./${ID_FILENAME}_json_snapshot.txt

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

	rm -f ./rawinfo_${ID_FILENAME}.txt
        `adb -s ${deviceID} shell du -sk /data/data/${packageName} > ./rawinfo_${ID_FILENAME}.txt`
	line_Result=$(cat ./rawinfo_${ID_FILENAME}.txt | sed 's/  */ /g' | sed 's/\r//g')
#	echo "line_Result is [${line_Result}]"
	if [ ! -n "$line_Result" ]
	then
		continue
	fi

	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`
#15388   /data/data/com.skt.prod.tmessage

	result=$(echo ${line_Result} | cut -f1 -d " ")
#	AVG=$((($AVG*($count-1)+$result)/$count))
	AVG=`echo "${AVG} $(($count-1)) ${result} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`

	if [ ${result} -gt ${MAX} ]
	then
		MAX=${result}
	fi

	if [ ${MIN} -gt ${result} ]
	then
		MIN=${result}
	fi

	if [ ${count} -eq 1 ]
	then
		INIT=${result}
	fi


	echo "============================================="		
	echo "${line_Result}"
	echo "filter>>${result}"
	echo "STORAGE_AVG  is ${AVG}"
	echo "STORAGE_MAX  is ${MAX}"
	echo "STORAGE_MIN  is ${MIN}"
	echo "STORAGE_INIT is ${INIT}"
	echo "---------------------------------------------"

	result1=${result}
	
	rm -f ./rawinfo_${ID_FILENAME}_cache.txt
    `adb -s ${deviceID} shell du -sk /data/data/${packageName}/cache > ./rawinfo_${ID_FILENAME}_cache.txt`
	line_Result=$(cat ./rawinfo_${ID_FILENAME}_cache.txt | sed 's/  */ /g' | sed 's/\r//g')
#	echo "line_Result is [${line_Result}]"
	if [ ! -n "$line_Result" ]
	then
		continue
	fi

	result=$(echo ${line_Result} | cut -f1 -d " ")

	AVG_CACHE=`echo "${AVG_CACHE} $(($count-1)) ${result} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`

	if [ ${result} -gt ${MAX_CACHE} ]
	then
		MAX_CACHE=${result}
	fi

	if [ ${MIN_CACHE} -gt ${result} ]
	then
		MIN_CACHE=${result}
	fi

	if [ ${count} -eq 1 ]
	then
		INIT_CACHE=${result}
	fi

	writeTrace

	echo "============================================="		
	echo "${line_Result}"
	echo "filter>>${result}"
	echo "STORAGE_AVG_CACHE  is ${AVG_CACHE}"
	echo "STORAGE_MAX_CACHE  is ${MAX_CACHE}"
	echo "STORAGE_MIN_CACHE  is ${MIN_CACHE}"
	echo "STORAGE_INIT_CACHE is ${INIT_CACHE}"
	echo "---------------------------------------------"		

	sleep ${POLLING_DELAY}
done

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${AVG}\t${MAX}\t${MIN}\t${INIT}\t${AVG_CACHE}\t${MAX_CACHE}\t${MIN_CACHE}\t${INIT_CACHE}" >> ./summary.txt

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

echo "AVG" "$AVG" >> ./${ID_FILENAME}_json.txt
echo "MAX" "$MAX" >> ./${ID_FILENAME}_json.txt
echo "MIN" "$MIN" >> ./${ID_FILENAME}_json.txt
echo "INIT" "$INIT" >> ./${ID_FILENAME}_json.txt
echo "AVG_CACHE" "$AVG_CACHE" >> ./${ID_FILENAME}_json.txt
echo "MAX_CACHE" "$MAX_CACHE" >> ./${ID_FILENAME}_json.txt
echo "MIN_CACHE" "$MIN_CACHE" >> ./${ID_FILENAME}_json.txt
echo "INIT_CACHE" "$INIT_CACHE" >> ./${ID_FILENAME}_json.txt

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

