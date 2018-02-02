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

rootDir=$5
echo "rootDir is [${rootDir}]"

lintLinkRootUrl=$6
echo "lintLinkRootUrl is [${lintLinkRootUrl}]"

lmcst_ratio=$7
echo "lmcst_ratio is ${lmcst_ratio}"

error_reason=""

if [[ "$(uname -s)" == *"Darwin"* ]]
then
    apkCreateTime=$(gls -l --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir} | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\n//g' | cut -f6-7 -d " " | sed 's/ /_/g' )
    apkFullName=$(gls -l --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir} | grep ^- | grep .apk | tail -n 1 | sed 's/  */ /g' | sed 's/\n//g' | cut -f8 -d " " )
else
    if [ ! -n "$(echo ${deviceID} | grep emulator)"  ] #"real device"
    then
        apkCreateTime=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir} | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f6-7 -d " " | sed 's/ /_/g' )
        apkFullName=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir} | grep ^- | grep .apk | grep armeabi | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f8 -d " " )
    else
        apkCreateTime=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir} | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f6-7 -d " " | sed 's/ /_/g' )
        apkFullName=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir} | grep ^- | grep .apk | grep x86 | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f8 -d " " )
    fi
fi

echo "apkCreateTime is [${apkCreateTime}]"
echo "apkFullName is [${apkFullName}]"
if [ ! -n "$(echo ${apkFullName} | grep .apk)" ]
then
	error_reason=${error_reason}."notFindApk"
	echo ${error_reason}
fi

if [ ! -n "${error_reason}" ]
then
	apkName=$(echo ${apkFullName} | cut -f1 -d "." )
	echo "apkName is [${apkName}]"
#	git_branchName=$(echo ${apkFullName} | cut -f2 -d "." )
#	echo "git_branchName is [${git_branchName}]"
#	git_revCount=$(echo ${apkFullName} | cut -f3 -d "." )
#	echo "git_revCount is [${git_revCount}]"
#	git_commitValue=$(echo ${apkFullName} | cut -f4 -d "." )
#	echo "git_commitValue is [${git_commitValue}]"
	
	git_branchName=master
	echo "git_branchName is [${git_branchName}]"
	git_revCount=$(echo ${apkName} | cut -f3 -d "_" )
	echo "git_revCount is [${git_revCount}]"
	git_commitValue=$(echo ${apkName} | cut -f4 -d "_" )
	echo "git_commitValue is [${git_commitValue}]"	

    if [ "${lintLinkRootUrl}" != "none" ]
    then
	if [[ "$(uname -s)" == *"Darwin"* ]]
	then
		lintCreateTime=$(gls -l --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir}/lint | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\n//g' | cut -f6-7 -d " " | sed 's/ /_/g' )
		lintFullName=$(gls -l --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir}/lint | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\n//g' | cut -f8 -d " " )
	else
		lintCreateTime=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir}/lint | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f6-7 -d " " | sed 's/ /_/g' )
		lintFullName=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir}/lint | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f8 -d " " )
	fi
    
	echo "lintCreateTime is [${lintCreateTime}]"
	echo "lintFullName is [${lintFullName}]"
	lintName=$(echo ${lintFullName} | cut -f1 -d "." )
	echo "lintName is [${lintName}]"
	
	if [ ! -n "${git_branchName}" ]
	then
		error_reason=${error_reason}."git_branchName_null"
		echo ${error_reason}	
	fi
	if [ ${git_branchName} != $(echo ${lintFullName} | cut -f2 -d "." ) ]
	then
		error_reason=${error_reason}."git_branchName_notMatch"
		echo ${error_reason}
	fi

	if [ ! -n "${git_revCount}" ]
	then
		error_reason=${error_reason}."git_revCount_null"
		echo ${error_reason}	
	fi	
	if [ ${git_revCount} != $(echo ${lintFullName} | cut -f3 -d "." ) ]
	then
		error_reason=${error_reason}."git_revCount_notMatch"
		echo ${error_reason}
	fi

	if [ ! -n "${git_commitValue}" ]
	then
		error_reason=${error_reason}."git_commitValue_null"
		echo ${error_reason}	
	fi	
	if [ ${git_commitValue} != $(echo ${lintFullName} | cut -f4 -d "." ) ]
	then
		error_reason=${error_reason}."git_commitValue_notMatch"
		echo ${error_reason}		
	fi
    fi
fi

UUID=${UUID}[${git_branchName}]
UUID=${UUID}[${git_commitValue}]
UUID=${UUID}[${git_revCount}]
echo "UUID is ${UUID}"

if [ ! -n "${error_reason}" ]
then
        if [ "${lintLinkRootUrl}" == "none" ]
	then
		lintLinkUrl="none"
		lineErrorCount=0
		lineWarningCount=0
	else
		lintLinkUrl=${lintLinkRootUrl}/${lintFullName}	
		echo "lintLinkUrl is [${lintLinkUrl}]"
		lineErrorCount=$(cat ${rootDir}/lint/${lintFullName} | grep found: | head -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f1 -d " " )
		echo "lineErrorCount is [${lineErrorCount}]"
		lineWarningCount=$(cat ${rootDir}/lint/${lintFullName} | grep found: | head -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f4 -d " " )
		echo "lineWarningCount is [${lineWarningCount}]"			
	fi
fi

if [ ! -n "${error_reason}" ]
then
	`cp -f ${rootDir}/${apkFullName} .`
	echo "adb -s ${deviceID} install -r ${rootDir}/${apkFullName}"
	installStatus=$(adb -s ${deviceID} install -r ${apkFullName} 2>&1 | sed 's/\r//g')
	echo "installStatus is [${installStatus}]"
    if [[ "$(uname)" == *"Darwin"* ]]
    then
        if [ ! -n "$(gls -l --time-style="+%Y-%m-%d %H:%M:%S" . | grep ${apkFullName})" ]
        then
            error_reason=${error_reason}."failCopyApk"
            echo ${error_reason}
        else
            `rm -f ./${apkFullName}`
        fi
    else
    	if [ ! -n "$(ls --time-style="+%Y-%m-%d %H:%M:%S" . | grep ${apkFullName})" ]
        then
            error_reason=${error_reason}."failCopyApk"
            echo ${error_reason}
        else
            `rm -f ./${apkFullName}`
        fi
    fi

	if [ "${installStatus}" != "Success" ]
	then
		error_reason=${error_reason}."failInstallApk"
		echo ${error_reason}
	fi	
fi

if [ ! -n "${error_reason}" ]
then
	rm -f ./rawinfo_${ID_FILENAME}.txt
    `adb -s ${deviceID} shell du -sk /data/app/${packageName}* > ./rawinfo_${ID_FILENAME}.txt`
	line_Result=$(cat ./rawinfo_${ID_FILENAME}.txt | sed 's/  */ /g' | sed 's/\r//g')
	if [ -n "$line_Result" ]
	then
		apkInstallSize=$(echo ${line_Result} | cut -f1 -d " ")
        echo "apkInstallSize" "$apkInstallSize"
		echo "apkInstallSize" "$apkInstallSize" >> ./${ID_FILENAME}_json.txt
	fi

	rm -f ./rawinfo_${ID_FILENAME}.txt
    `du -sk ${rootDir}/${apkFullName} > ./rawinfo_${ID_FILENAME}.txt`
	line_Result=$(cat ./rawinfo_${ID_FILENAME}.txt | sed 's/  */ /g' | sed 's/\r//g')
	if [ -n "$line_Result" ]
	then
		apkSize=$(echo ${line_Result} | cut -f1 -d " ")
		echo "apkSize" "$apkSize"
		echo "apkSize" "$apkSize" >> ./${ID_FILENAME}_json.txt
	fi
fi


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

if [ -n "$error_reason" ]
then
    echo "error_reason" "$error_reason" >> ./${ID_FILENAME}_json.txt
fi
echo "apkFullName" "$apkFullName" >> ./${ID_FILENAME}_json.txt
echo "lintLinkUrl" "$lintLinkUrl" >> ./${ID_FILENAME}_json.txt
echo "lineErrorCount" "$lineErrorCount" >> ./${ID_FILENAME}_json.txt
echo "lineWarningCount" "$lineWarningCount" >> ./${ID_FILENAME}_json.txt

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


if [ ! -n "${error_reason}" ]
then
	error_reason=none
    echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${error_reason}\t${apkFullName}\t${lintLinkUrl}\t${lineErrorCount}\t${lineWarningCount}" >> ./summary.txt
	exit 0
else
    echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${error_reason}\t${apkFullName}\t${lintLinkUrl}\t${lineErrorCount}\t${lineWarningCount}" >> ./summary.txt
	echo "error_reason is [${error_reason}]"
	exit 1
fi
