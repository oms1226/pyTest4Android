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

pkgUID=$(adb -s ${deviceID} shell dumpsys package ${packageName} | grep 'userId' | tail -n 1 | sed 's/ //g' | sed 's/userId=//g' | sed 's/\r//g')
echo "pkgUID is [${pkgUID}]"

if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then
while [ ! -n "$(adb -s ${deviceID} shell ls /proc/uid_stat | grep ${pkgUID})" ]
do
	echo "$(adb -s ${deviceID} shell ls /proc/uid_stat | grep ${pkgUID})"
	sleep ${POLLING_DELAY}
done
else
rx_bytes=6
tx_bytes=8
uid_tag_int=4
cnt_set=5
Zero_value=0
One_value=0

while [ ! -n "$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==0{printf $'$uid_tag_int'}')" ]
do
	echo "$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==0{printf $'$uid_tag_int'}')"
	sleep ${POLLING_DELAY}
done
fi
AVG_RCV=0
MAX_RCV=0
MIN_RCV=${INT_MAX}
SUM_RCV=0

if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then
while [ ! -n "$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_rcv)" ]
do
	echo "$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_rcv)"
	sleep ${POLLING_DELAY}
done
INIT_RCV=$(adb -s ${deviceID} shell cat /proc/uid_stat/${pkgUID}/tcp_rcv | sed 's/\r//g')
else
Zero_value=$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==0{printf $'$rx_bytes'}')
One_value=$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==1{printf $'$rx_bytes'}')
INIT_RCV=`expr $Zero_value + $One_value`
fi
AVG_SND=0
MAX_SND=0
MIN_SND=${INT_MAX}
SUM_SND=0

if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then
while [ ! -n "$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_snd)" ]
do
	echo "$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_snd)"
	sleep ${POLLING_DELAY}
done
INIT_SND=$(adb -s ${deviceID} shell cat /proc/uid_stat/${pkgUID}/tcp_snd | sed 's/\r//g')
else
Zero_value=$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==0{printf $'$tx_bytes'}')
One_value=$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==1{printf $'$tx_bytes'}')
INIT_SND=`expr $Zero_value + $One_value`
fi

count=0
result_rcv=0
result_snd=0

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
    echo "rcv" "$result_rcv" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "snd" "$result_snd" >> ./${ID_FILENAME}_json_snapshot.txt

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
if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then
	isFile=$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_snd)
else
	isFile=$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==0{printf $'$uid_tag_int'}')
fi
	if [ ! -n "$isFile" ]
	then
		continue	
	fi
if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then	
	isFile=$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_rcv)
	if [ ! -n "$isFile" ]
	then
		continue	
	fi	
fi

if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then	
  line_SND=$(adb -s ${deviceID} shell cat /proc/uid_stat/${pkgUID}/tcp_snd | sed 's/\r//g')
else
  Zero_value=$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==0{printf $'$tx_bytes'}')
  One_value=$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==1{printf $'$tx_bytes'}')
  line_SND=`expr $Zero_value + $One_value`
fi
	if [ ! -n "$line_SND" ]
	then
		continue
	fi
	
if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
then	
	line_RCV=$(adb -s ${deviceID} shell cat /proc/uid_stat/${pkgUID}/tcp_rcv | sed 's/\r//g')
else
  Zero_value=$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==0{printf $'$rx_bytes'}')
  One_value=$(adb -s ${deviceID} shell cat /proc/net/xt_qtaguid/stats | awk '$'$uid_tag_int'=='$pkgUID' && $'$cnt_set'==1{printf $'$rx_bytes'}')
  line_RCV=`expr $Zero_value + $One_value`
fi
	if [ ! -n "$line_RCV" ]
	then
		continue
	fi
	
	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`
#root@herolteskt:/proc/uid_stat/10207 # ls
#tcp_rcv
#tcp_snd
#root@herolteskt:/proc/uid_stat/10207 # cat tcp_rcv
#9023810
#root@herolteskt:/proc/uid_stat/10207 # cat tcp_snd
#2985999

	result_rcv=$(($line_RCV-$INIT_RCV))
	if [ ${result_rcv} -lt 0 ]
	then
		INIT_RCV=0
		result_rcv=$(($line_RCV-$INIT_RCV))
	fi	
#	AVG_RCV=$((($AVG_RCV*($count-1)+$result_rcv)/$count))
	AVG_RCV=`echo "${AVG_RCV} $(($count-1)) ${result_rcv} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`
	
	if [ ${result_rcv} -gt ${MAX_RCV} ]
	then
		MAX_RCV=${result_rcv}
	fi

	if [ ${MIN_RCV} -gt ${result_rcv} ]
	then
		MIN_RCV=${result_rcv}
	fi	
	SUM_RCV=$(($SUM_RCV+$result_rcv))
	

	result_snd=$(($line_SND-$INIT_SND))
	if [ ${result_snd} -lt 0 ]
	then
		INIT_SND=0
		result_snd=$(($line_SND-$INIT_SND))
	fi	
#	AVG_SND=$((($AVG_SND*($count-1)+$result_snd)/$count))
	AVG_SND=`echo "${AVG_SND} $(($count-1)) ${result_snd} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`
	
	if [ ${result_snd} -gt ${MAX_SND} ]
	then
		MAX_SND=${result_snd}
	fi

	if [ ${MIN_SND} -gt ${result_snd} ]
	then
		MIN_SND=${result_snd}
	fi	
	SUM_SND=$(($SUM_SND+$result_snd))

    writeTrace

	echo "============================================="		
	echo "tcp_rcv:[${line_RCV}]"
	echo "filter>>${result_rcv}"
	echo "AVG_RCV is ${AVG_RCV}"
	echo "MAX_RCV is ${MAX_RCV}"
	echo "MIN_RCV is ${MIN_RCV}"		
	echo "SUM_RCV is ${SUM_RCV}"
	echo "---------------------------------------------"	
	echo "tcp_snd:[${line_SND}]"
	echo "filter>>${result_snd}"
	echo "AVG_SND is ${AVG_SND}"
	echo "MAX_SND is ${MAX_SND}"
	echo "MIN_SND is ${MIN_SND}"		
	echo "SUM_SND is ${SUM_SND}"

	sleep ${POLLING_DELAY}
	
	INIT_RCV=${line_RCV}
	INIT_SND=${line_SND}	
done

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${AVG_RCV}\t${MAX_RCV}\t${MIN_RCV}\t${SUM_RCV}\t${AVG_SND}\t${MAX_SND}\t${MIN_SND}\t${SUM_SND}" >> ./summary.txt

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

echo "AVG_RCV" "$AVG_RCV" >> ./${ID_FILENAME}_json.txt
echo "MAX_RCV" "$MAX_RCV" >> ./${ID_FILENAME}_json.txt
echo "MIN_RCV" "$MIN_RCV" >> ./${ID_FILENAME}_json.txt
echo "SUM_RCV" "$SUM_RCV" >> ./${ID_FILENAME}_json.txt
echo "AVG_SND" "$AVG_SND" >> ./${ID_FILENAME}_json.txt
echo "MAX_SND" "$MAX_SND" >> ./${ID_FILENAME}_json.txt
echo "MIN_SND" "$MIN_SND" >> ./${ID_FILENAME}_json.txt
echo "SUM_SND" "$SUM_SND" >> ./${ID_FILENAME}_json.txt

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