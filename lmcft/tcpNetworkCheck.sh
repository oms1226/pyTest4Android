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

pkgUID=$(adb -s ${deviceID} shell dumpsys package ${packageName} | grep 'userId' | sed 's/ //g' | sed 's/userId=//g' | sed 's/\r//g')

while [ ! -n "$(adb -s ${deviceID} shell ls /proc/uid_stat | grep ${pkgUID})" ]
do
	echo "$(adb -s ${deviceID} shell ls /proc/uid_stat | grep ${pkgUID})"
	sleep 1
done
AVG_RCV=0
MAX_RCV=0
MIN_RCV=${INT_MAX}
SUM_RCV=0
while [ ! -n "$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_rcv)" ]
do
	echo "$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_rcv)"
	sleep 1
done
INIT_RCV=$(adb -s ${deviceID} shell cat /proc/uid_stat/${pkgUID}/tcp_rcv | sed 's/\r//g')

AVG_SND=0
MAX_SND=0
MIN_SND=${INT_MAX}
SUM_SND=0
while [ ! -n "$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_snd)" ]
do
	echo "$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_snd)"
	sleep 1
done
INIT_SND=$(adb -s ${deviceID} shell cat /proc/uid_stat/${pkgUID}/tcp_snd | sed 's/\r//g')



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

	isFile=$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_snd)
	if [ ! -n "$isFile" ]
	then
		continue	
	fi
	
	isFile=$(adb -s ${deviceID} shell ls /proc/uid_stat/${pkgUID} | grep tcp_rcv)
	if [ ! -n "$isFile" ]
	then
		continue	
	fi	

	line_SND=$(adb -s ${deviceID} shell cat /proc/uid_stat/${pkgUID}/tcp_snd | sed 's/\r//g')
	if [ ! -n "$line_SND" ]
	then
		continue
	fi
	
	line_RCV=$(adb -s ${deviceID} shell cat /proc/uid_stat/${pkgUID}/tcp_rcv | sed 's/\r//g')
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