#!/bin/sh
#./tempCheck.sh '[samsung][SM-G930S][6.0.1][G930SKSE1APL1][201702241543]' 'HT6CN0201431' 'com.skt.prod.tmessage' '201712241643' '2'
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

temp_AVG=0
temp_MAX=0
temp_MIN=${INT_MAX}


count=0
temp=0

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
    echo "temp" "$temp" >> ./${ID_FILENAME}_json_snapshot.txt

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

	result=$(adb -s ${deviceID} shell cat /sys/class/thermal/thermal_zone0/temp | sed 's/\r//g')
	if [ ! -n "$result" ]
	then
		continue
	fi

	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`

	temp=${result}
	echo "temp is [${temp}]"	
	temp_AVG=`echo "${temp_AVG} $(($count-1)) ${temp} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`

	if [ ${temp} -gt ${temp_MAX} ]
	then
		temp_MAX=${temp}
	fi

	if [ ${temp_MIN} -gt ${temp} ]
	then
		temp_MIN=${temp}
	fi

    writeTrace

	echo "============================================="		
	echo "${result}"
	echo "filter>>${temp}"
	echo "temp_AVG is ${temp_AVG}"
	echo "temp_MAX is ${temp_MAX}"
	echo "temp_MIN is ${temp_MIN}"		
	echo "---------------------------------------------"	

	sleep ${POLLING_DELAY}
done

temp_AVG=`echo "${temp_AVG}"|awk '{printf "%.5f", $1 / 1000}'`
temp_MAX=`echo "${temp_MAX}"|awk '{printf "%.5f", $1 / 1000}'`
temp_MIN=`echo "${temp_MIN}"|awk '{printf "%.5f", $1 / 1000}'`

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${temp_AVG}\t${temp_MAX}\t${temp_MIN}" >> ./summary.txt

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
echo "temp_AVG" "$temp_AVG" >> ./${ID_FILENAME}_json.txt
echo "temp_MAX" "$temp_MAX" >> ./${ID_FILENAME}_json.txt
echo "temp_MIN" "$temp_MIN" >> ./${ID_FILENAME}_json.txt

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

