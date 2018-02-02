#!/bin/sh
#./crontab.sh -deviceID ce1115fbd5ad960201
echo "this is ${0}"
start=`expr index "$0" /`
end=`expr index "$0" .sh`
ID_FILENAME=${0:$start:$(($end-$start-2))}
echo "ID_FILENAME is ${ID_FILENAME}"

if [ "$1" == "-deviceID" ]
then
	shift
	deviceID=${1}
	shift
else
	deviceID=emulator-5554
fi
#phoneNum=01021462805
#phoneNum=01021289015
RATIO=0

#cd /cygdrive/c/_python/workspace/PycharmProjects/lmcst/lmcst_v1.0
#./fuzztest.sh -deviceID ce1115fbd5ad960201 -uploadRootDir /cygdrive/z 3000 10 yes
#./fuzzTest.sh -deviceID HT6CN0201431 -uploadRootDir /cygdrive/z 3000 1 yes 50 confirm_lbp_neg_900.xml
#CMD="./fuzztest.sh -deviceID '${deviceID}' -phoneNum '${phoneNum}' -uploadRootDir /cygdrive/z 3000 10 yes"
if [[ "$(uname -s)" == *"Darwin"* ]]
then
	CMD="./fuzztest.sh -deviceID '${deviceID}' -uploadRootDir /Volumes/build 1000 10 yes '${RATIO}' confirm_lbp_neg_900.xml"
else
	CMD="./fuzztest.sh -deviceID '${deviceID}' -uploadRootDir /cygdrive/z 1000 10 yes '${RATIO}' confirm_lbp_neg_900.xml"
fi
if [ -n "$(echo ${deviceID} | grep emulator)"  ] #"emulator"
then
    phoneNum=01049611657
	CMD="./fuzztest.sh -deviceID '${deviceID}' -phoneNum 01049611657 -uploadRootDir /cygdrive/z 1000 10 yes"
	#cd /cygdrive/d/Android/projects/lmcst/lmcft/	
fi

count=0
START_BATTERY=0
END___BATTERY=0
while [ $count -lt 1 ]
do
	count=`expr $count + 1`	
	execTiime=`eval date +%Y%m%d%H%M`
	if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
    then
        if [ ! -n "$(adb devices | grep ${deviceID})" ]
        then
            echo "deviceID[${deviceID}] probably turn off!"
            error_reason=${error_reason}."error_occur_turnoff"
    	    echo "For waiting, sleep 3600 due to no connection!"
			sleep 3600
            continue
        fi

    fi

#	if [ "$(date +%H)" == "00" -o "$(date +%H)" == "06" -o "$(date +%H)" == "12" -o "$(date +%H)" == "18" ]

#	if [ "$(date +%H)" == "14" -o "$(date +%H)" == "02" ]
#	then
#		if [ $(date +%M) -ge 0 -a $(date +%M) -le 5 ]
#		then
############################################################################################################################3
            eval "adb -s '${deviceID}' root"
			isMonkey=$(adb -s ${deviceID} shell ps | grep monkey)
			if [ -n "$isMonkey" ]
			then
				echo "isMonkey is ${isMonkey}"
				continue
			fi
if [ -n "$(echo ${deviceID} | grep emulator)"  ] #"emulator"
then
			echo "taskkill /F /IM qemu-system-x86_64.exe"			
			eval "taskkill /F /IM qemu-system-x86_64.exe"
			echo "/cygdrive/d/Android/sdkFromAnotherPC/tools/emulator.exe -ports 1657,5555  -avd Pixel_XL_API_24.x86_64 -gpu host &"
			eval "/cygdrive/d/Android/sdkFromAnotherPC/tools/emulator.exe -ports 1657,5555  -avd Pixel_XL_API_24.x86_64 -gpu host &"
			echo "sleep 300"
			sleep 300
            eval "adb -s '${deviceID}' root"
else
            echo "adb -s '${deviceID}' reboot"
            eval "adb -s '${deviceID}' reboot"
			echo "sleep 300"
			sleep 300
            eval "adb -s '${deviceID}' root"
fi
			START_BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")
			echo "START_BATTERY is [${START_BATTERY}]"
			if [ -d /cygdrive/z  ]
			then			
				echo ${CMD}
                if [ ! -d /cygdrive/d/lmcft_log ] ; then
                    mkdir -p /cygdrive/d/lmcft_log
                fi
				eval ${CMD} > /cygdrive/d/lmcft_log/fuzztest.log
			else
				echo "/cygdrive/z is not found!"
			fi
			END___BATTERY=$(adb -s ${deviceID} shell dumpsys battery | grep level | sed 's/  */ /g' | sed 's/\r//g' | cut -f3 -d " ")
	        echo "END___BATTERY is [${END___BATTERY}]"
#			RATIO=`expr $RATIO + 10`
#			if [ ${RATIO} -gt 100 ]
#            		then
#                		RATIO=0
#			fi
############################################################################################################################3
#		fi
#	fi

	if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
    then
        #SM-G930S NOS
        phoneNumLineNum_Index=15
        phoneNum=$(adb -s ${deviceID} shell service call iphonesubinfo ${phoneNumLineNum_Index} | grep 0x00000000 | sed 's/  */ /g' | sed 's/\.//g' | sed "s/'//g" | sed 's/)//g' | sed 's/\r//g' | cut -f7 -d " ")
        phoneNum=${phoneNum}$(adb -s ${deviceID} shell service call iphonesubinfo ${phoneNumLineNum_Index} | grep 0x00000010 | sed 's/  */ /g' | sed 's/\.//g' | sed "s/'//g" | sed 's/)//g' | sed 's/\r//g' | cut -f7 -d " ")
    	echo "After test, sleep 3600"
		sleep 3600
    fi
	echo "phoneNum is [${phoneNum}]"
	echo "count is [${count}]"
	echo "execTiime is [${execTiime}]"	
	echo "LASTCMD_START_BATTERY is [${START_BATTERY}]"
	echo "LASTCMD_END___BATTERY is [${END___BATTERY}]"
    echo "After test, sleep 60"
	sleep 60
done

