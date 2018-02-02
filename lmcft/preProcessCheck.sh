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

rootDir=$5
echo "rootDir is [${rootDir}]"

lintLinkRootUrl=$6
echo "lintLinkRootUrl is [${lintLinkRootUrl}]"

error_reason=""

apkCreateTime=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir} | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f6-7 -d " " | sed 's/ /_/g' )
echo "apkCreateTime is [${apkCreateTime}]"
apkFullName=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir} | grep ^- | grep .apk | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f8 -d " " )
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
	git_branchName=$(echo ${apkFullName} | cut -f2 -d "." )
	echo "git_branchName is [${git_branchName}]"
	git_revCount=$(echo ${apkFullName} | cut -f3 -d "." )
	echo "git_revCount is [${git_revCount}]"
	git_commitValue=$(echo ${apkFullName} | cut -f4 -d "." )
	echo "git_commitValue is [${git_commitValue}]"

	lintCreateTime=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir}/lint | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f6-7 -d " " | sed 's/ /_/g' )
	echo "lintCreateTime is [${lintCreateTime}]"
	lintFullName=$(ls --time-style="+%Y-%m-%d %H:%M:%S" -altr ${rootDir}/lint | grep ^- | tail -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f8 -d " " )
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

UUID=${UUID}[${git_branchName}]
UUID=${UUID}[${git_commitValue}]
UUID=${UUID}[${git_revCount}]
echo "UUID is ${UUID}"

if [ ! -n "${error_reason}" ]
then
	lintLinkUrl=${lintLinkRootUrl}/${lintFullName}
	echo "lintLinkUrl is [${lintLinkUrl}]"
	lineErrorCount=$(cat ${rootDir}/lint/${lintFullName} | grep found: | head -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f1 -d " " )
	echo "lineErrorCount is [${lineErrorCount}]"
	lineWarningCount=$(cat ${rootDir}/lint/${lintFullName} | grep found: | head -n 1 | sed 's/  */ /g' | sed 's/\r//g' | cut -f4 -d " " )
	echo "lineWarningCount is [${lineWarningCount}]"	
fi

if [ ! -n "${error_reason}" ]
then
	`cp -f ${rootDir}/${apkFullName} .`
	echo "adb -s ${deviceID} install -r ${rootDir}/${apkFullName}"
	installStatus=$(adb -s ${deviceID} install -r ${apkFullName} 2>&1 | sed 's/\r//g')
	echo "installStatus is [${installStatus}]"
	if [ ! -n "$(ls --time-style="+%Y-%m-%d %H:%M:%S" . | grep ${apkFullName})" ]
	then
		error_reason=${error_reason}."failCopyApk"
		echo ${error_reason}	
	else
		`rm -f ./${apkFullName}`
	fi
	if [ "${installStatus}" != "Success" ]
	then
		error_reason=${error_reason}."failInstallApk"
		echo ${error_reason}
	fi	
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
