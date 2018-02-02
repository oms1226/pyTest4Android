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

cpu_AVG=0
cpu_MAX=0
cpu_MIN=${INT_MAX}
cpu_SUM=0


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

	result=$(echo ${line_Top} | cut -f3 -d " " | sed 's/%//g')
	
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