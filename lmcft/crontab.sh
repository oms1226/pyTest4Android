#!/bin/sh

echo "this is ${0}"
start=`expr index "$0" /`
end=`expr index "$0" .sh`
ID_FILENAME=${0:$start:$(($end-$start-2))}
echo "ID_FILENAME is ${ID_FILENAME}"

deviceID=ce1115fbd5ad960201
#phoneNum=01021462805
#deviceID=ce1015faf3f91e0a01
#phoneNum=01021289015

#./fuzztest.sh -deviceID ce1115fbd5ad960201 -phoneNum 01021462805 -uploadRootDir /cygdrive/z 3000 10 yes
#CMD="./fuzztest.sh -deviceID '${deviceID}' -phoneNum '${phoneNum}' -uploadRootDir /cygdrive/z 3000 10 yes"
CMD="./fuzztest.sh -deviceID '${deviceID}' -uploadRootDir /cygdrive/z 3000 10 yes"

count=0
START_BATTERY=0
END___BATTERY=0
while [ 1 ]
do
	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`
	if [ ! -n "$(adb devices | grep ${deviceID})" ]
	then
		echo "deviceID[${deviceID}] probably turn off!"
		error_reason=${error_reason}."error_occur_turnoff"		
		continue
	fi
	
	if [ "$(date +%H)" == "00" -o "$(date +%H)" == "12" ]
	then
		if [ $(date +%M) -ge 10 -a $(date +%M) -le 15 ]
		then
			isMonkey=$(adb -s ${deviceID} shell ps | grep monkey)
			if [ -n "$isMonkey" ]
			then
				continue
			fi
			START_BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")		
			eval ${CMD}
			END___BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")
		fi
	fi
	
	#SM-G930S NOS
	phoneNumLineNum_Index=15
	phoneNum=$(adb -s ${deviceID} shell service call iphonesubinfo ${phoneNumLineNum_Index} | grep 0x00000000 | sed 's/  */ /g' | sed 's/\.//g' | sed "s/'//g" | sed 's/)//g' | sed 's/\r//g' | cut -f7 -d " ")
	phoneNum=${phoneNum}$(adb -s ${deviceID} shell service call iphonesubinfo ${phoneNumLineNum_Index} | grep 0x00000010 | sed 's/  */ /g' | sed 's/\.//g' | sed "s/'//g" | sed 's/)//g' | sed 's/\r//g' | cut -f7 -d " ")
	echo "phoneNum is [${phoneNum}]"
	echo "count is [${count}]"
	echo "execTiime is [${execTiime}]"	
	echo "LASTCMD_START_BATTERY is [${START_BATTERY}]"
	echo "LASTCMD_END___BATTERY is [${END___BATTERY}]"
	sleep 60
done

