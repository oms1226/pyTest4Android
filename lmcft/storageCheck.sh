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

AVG=0
MAX=0
MIN=${INT_MAX}
INIT=0

AVG_CACHE=0
MAX_CACHE=0
MIN_CACHE=${INT_MAX}
INIT_CACHE=0

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