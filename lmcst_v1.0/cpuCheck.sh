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


cpu_AVG=0
cpu_MAX=0
cpu_MIN=${INT_MAX}
cpu_SUM=0


count=0

result=0

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
    if [[ "$packageName" == "$Name" ]];then
        echo "PID" "$PID" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "USER" "$USER" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "PR" "$PR" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "NI" "$NI" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "CPU" "$CPU" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "S" "$S" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "THRC" "$THRC" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "VSS" "$VSS" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "RSS" "$RSS" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "PCY" "$PCY" >> ./${ID_FILENAME}_json_snapshot.txt
        echo "Name" "$Name" >> ./${ID_FILENAME}_json_snapshot.txt
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
    `adb -s ${deviceID} shell top -n 1 -d 0 | grep ${packageName} > ./rawinfo_${ID_FILENAME}.txt`
	line_Top=$(cat ./rawinfo_${ID_FILENAME}.txt | sed 's/  */ /g' | sed 's/\r//g')
#	echo "line_Top is [${line_Top}]"
	if [ ! -n "$line_Top" ]
	then
		continue
	fi

	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`
#** MEMINFO in pid 6673 [com.skt.prod.tmessage] **
#                   Pss  Private  Private  Swapped     Heap     Heap     Heap
#                 Total    Dirty    Clean    Dirty     Size    Alloc     Free
#                ------   ------   ------   ------   ------   ------   ------
#  Native Heap    24102    24020        8     3612    45184    29662    15521
#  Dalvik Heap    39414    39240        0     1700    54062    37820    16242

	result=$(echo ${line_Top} | cut -f5 -d " " | sed 's/%//g')

#	cpu_AVG=$((($cpu_AVG*($count-1)+$result)/$count))
	cpu_AVG=`echo "${cpu_AVG} $(($count-1)) ${result} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`	
	cpu_SUM=$(($cpu_SUM+$result))

	if [ ${result} -gt ${cpu_MAX} ]
	then
		cpu_MAX=${result}
	fi

	if [ ${cpu_MIN} -gt ${result} ]
	then
		cpu_MIN=${result}
	fi

#C:\Users\owner>adb shell "top -n 1 | grep com.skt.prod.dialer"
#  PID USER     PR  NI CPU% S  #THR     VSS     RSS PCY Name
#12209 u0_a84   16  -4   0% S    69 2230752K 177092K  fg com.skt.prod.dialer

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

	writeTrace

	echo "============================================="
	echo "${line_Top}"
	echo "filter>>${result}"
	echo "cpu_AVG is ${cpu_AVG}"
	echo "cpu_MAX is ${cpu_MAX}"
	echo "cpu_MIN is ${cpu_MIN}"		
	echo "cpu_SUM is ${cpu_SUM}"	
	echo "---------------------------------------------"	

	sleep ${POLLING_DELAY}
done

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${cpu_AVG}\t${cpu_MAX}\t${cpu_MIN}\t${cpu_SUM}" >> ./summary.txt

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

echo "cpu_AVG" "$cpu_AVG" >> ./${ID_FILENAME}_json.txt
echo "cpu_MAX" "$cpu_MAX" >> ./${ID_FILENAME}_json.txt
echo "cpu_MIN" "$cpu_MIN" >> ./${ID_FILENAME}_json.txt
echo "cpu_SUM" "$cpu_SUM" >> ./${ID_FILENAME}_json.txt

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