#!/bin/sh
echo "this is ${0}"
start=`expr index "$0" /`
end=`expr index "$0" .sh`
ID_FILENAME=${0:$start:$(($end-$start-2))}
echo "ID_FILENAME is ${ID_FILENAME}"
INT_MAX=2147483647
##################################################################
#./tmessageCheck.sh '[samsung][SM-G930S][6.0.1][G930SKSE1APL1][01021462805]' 'ce1115fbd5ad960201' 'com.skt.prod.tmessage' '[201703311050][201703311055][1][1500]' '2'
THREAD_SEND_LIMIT=50
MSG_SEND_MAX=500
PYTHONEXEC=/cygdrive/c/Python27/python.exe
###################################################################
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
isPreProcess=$6

lmcst_ratio=$7
echo "lmcst_ratio is ${lmcst_ratio}"

intentAction=com.skt.prod.RESPOND_VIA_MESSAGE
echo "intentAction is ${intentAction}"

count=0
sendmsgCount=0
revmsgCount=0
threadCount=0
filtedMsgCount=0
t114_Numbers=(15666000 16444000 15881600 0269426478 0237041004 15778000 15447200 15447000 15881900 15888900 15888710 15888700 0220008100 16449999 15881788 15881688 15881515 15889955 15885000 0269589000 15998800 15888100 18001111 15991155 15991111 15889500 15886700 15661000 15884500 15884000 029508510 15776200 15776000)
t114_Words=("[택배]" "[인증]" "[삼성카드]" "[하나카드]" "[우리카드]" "[신한카드]" "[하나카드]" "(광고)" "[외환카드]" "[신한체크]" "[삼성체크]" "[하나체크]" "[우리체크]" "[외화체크]" "[NH농협카드]" "[우체국]" "[KB국민카드]" "[수협은행]" "[롯데카드]" "[씨티카드]" "[BC카드]" "[현대카드]")

if [ "$isPreProcess" == "yes" ]
then
	##init##
	eval "adb -s '${deviceID}' shell pm clear com.android.providers.telephony"
	sleep ${POLLING_DELAY}
#	eval "adb -s '${deviceID}' shell rm -rf /data/data/${packageName}/databases"
#	sleep ${POLLING_DELAY}
	pid=$(adb -s ${deviceID} shell ps | grep 'com.android.phone' | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")
	echo "pid is [${pid}]"
	KILL_STATUS=`adb shell kill -9 ${pid}` 
	echo "KILL_STATUS is [${KILL_STATUS}]"
	sleep ${POLLING_DELAY}
	eval "adb -s '${deviceID}' shell \"am force-stop '${packageName}'\""	
	sleep ${POLLING_DELAY}
fi

echo "EXPECT_END_TIME is [${EXPECT_END_TIME}]"

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

	count=`expr $count + 1`
	execTiime=`eval date +%Y%m%d%H%M`
	
	ACION_LIST=""
	rand=$(( $RANDOM % 1000 ))
	if [ ${THREAD_SEND_LIMIT} -gt ${threadCount} -o ${rand} -lt 50 ]
	then	
		echo "${ID_FILENAME}_1_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
		revmsgCount=`expr $revmsgCount + 1`
		threadCount=`expr $threadCount + 1`
		senderPhoneNum=0101004$((${threadCount}+1000))
		if [ ${THREAD_SEND_LIMIT} -le ${threadCount} ]
		then
			randNum=$(( $RANDOM % 9000 ))
			senderPhoneNum=0101004$(($randNum+1000))
		fi
		text=none
		text=$(echo ${t114_Words[$(( $RANDOM % ${#t114_Words[*]} ))]}람멈밤삼암잠0123456789abcdefghijklmnopqrstuvwxyz | ./radamsa.exe | sed 's/\r//g' | sed 's/\n//g' | sed "s/'//g" | sed 's/`//g' | sed 's/\"//g')
		text="[msg_${revmsgCount}_${execTiime}]${text}"
	    rand=$(( $RANDOM % 100 ))
	    if [ ${rand} -lt 50 ]
	    then
		echo "${ID_FILENAME}_2_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
            MSG=$(${PYTHONEXEC} excelReadAndPrint.py | grep "ADDRESS:")
            senderPhoneNum=$(echo ${MSG} | cut -f1 -d "_" | sed 's/ADDRESS://g' | sed 's/\r//g' | sed 's/\n//g')
            text=$(echo ${MSG} | cut -f2 -d "_" | sed 's/MESSAGE://g' | sed 's/\r//g' | sed 's/\n//g')
		    text=$(echo ${text} | ./radamsa.exe | sed 's/\r//g' | sed 's/\n//g' | sed "s/'//g" | sed 's/`//g' | sed 's/\"//g')
        fi

		echo "text is [${text}]"
        echo "wget -O /dev/null 'http://beta.teafone.com/msggw/sendMsg?sender=${senderPhoneNum}&receiver=${phoneNum}&subject=${ID_FILENAME}&message=${text}'"
		eval "wget -O /dev/null 'http://beta.teafone.com/msggw/sendMsg?sender=${senderPhoneNum}&receiver=${phoneNum}&subject=${ID_FILENAME}&message=${text}'"

		ACION_LIST="${ACION_LIST}.recvMsg"
	fi	
	
	rand=$(( $RANDOM % 1000 ))
	if [ ${rand} -lt 50 ]
	then	
		echo "${ID_FILENAME}_3_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
		if [ ${sendmsgCount} -ge $(( ${MSG_SEND_MAX}/2 )) ]
		then
			ACION_LIST="${ACION_LIST}.limited_${sendmsgCount}"		
		else
			sendmsgCount=`expr $sendmsgCount + 1`
			text=none
			text=$(echo 감남담람멈밤삼암잠참캄탐팜함abcdefghijklmnopqrstuvwxyz | ./radamsa.exe | sed 's/\r//g' | sed 's/\n//g' | sed "s/'//g" | sed 's/`//g' | sed 's/\"//g' | sed 's/\\//g')
			#sleep ${POLLING_DELAY}
		    rand=$(( $RANDOM % 100 ))
            if [ ${rand} -lt 50 ]
            then
		echo "${ID_FILENAME}_4_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
                MSG=$(${PYTHONEXEC} excelReadAndPrint.py | grep "ADDRESS:")
                senderPhoneNum=$(echo ${MSG} | cut -f1 -d "_" | sed 's/ADDRESS://g' | sed 's/\r//g' | sed 's/\n//g')
                text=$(echo ${MSG} | cut -f2 -d "_" | sed 's/MESSAGE://g' | sed 's/\r//g' | sed 's/\n//g')
                text=$(echo ${text} | ./radamsa.exe | sed 's/\r//g' | sed 's/\n//g' | sed "s/'//g" | sed 's/`//g' | sed 's/\"//g')
            fi
    		echo "${ID_FILENAME}_31_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
		echo "${text}" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
	        eval "adb -s '${deviceID}' shell \"am startservice -a '${intentAction}' -d smsto:'${phoneNum}' --es android.intent.extra.TEXT '[msg_${sendmsgCount} send by yorum_fuzzTest.sh ${execTiime}] ${text}'\""
    		echo "${ID_FILENAME}_32_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
	        echo "adb -s '${deviceID}' shell \"am startservice -a '${intentAction}' -d smsto:'${phoneNum}' --es android.intent.extra.TEXT '[msg_${sendmsgCount} send by yorum_fuzzTest.sh ${execTiime}] ${text}'\""
		ACION_LIST="${ACION_LIST}.sendMsg"
    		echo "${ID_FILENAME}_33_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt			
		fi
	fi
	
	rand=$(( $RANDOM % 1000 ))
	if [ ${rand} -lt 50 ]
	then	
		echo "${ID_FILENAME}_5_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
		filtedMsgCount=`expr $filtedMsgCount + 1`
#		randNum=$(( $RANDOM % ${#t114_Numbers[*]} ))
#		senderPhoneNum=${t114_Numbers[${randNum}]}
		text=none
##		text="${t114_Words[$(( $RANDOM % ${#t114_Words[*]} ))]}[msg_${revmsgCount}_${execTiime}]${text}"
#		echo ${t114_Words[$(( $RANDOM % ${#t114_Words[*]} ))]}
#		cardOnlyName=$(echo ${t114_Words[$(( $RANDOM % ${#t114_Words[*]} ))]} | sed 's/\[//g' | sed 's/\]//g')
#		text="${cardOnlyName}승인1025오*섭 $(date +%m/%d) $(date +%H):$(date +%M) 인터파크INT_티켓 $(( $RANDOM % 1000 )),$(( $RANDOM % 1000 ))원 일시불"
##		echo "text is [${text}]"--> warning! not declare
#		text=$(echo ${text} | ./radamsa.exe | sed 's/\r//g' | sed 's/\n//g' | sed "s/'//g" | sed 's/`//g' | sed 's/\"//g')

        MSG=$(${PYTHONEXEC} excelReadAndPrint.py | grep "ADDRESS:")
	echo "${ID_FILENAME}_51_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt	
        senderPhoneNum=$(echo ${MSG} | cut -f1 -d "_" | sed 's/ADDRESS://g' | sed 's/\r//g' | sed 's/\n//g' | sed "s/'//g" | sed 's/`//g' | sed 's/\"//g')
	echo "${ID_FILENAME}_52_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt		
        text=$(echo ${MSG} | cut -f2 -d "_" | sed 's/MESSAGE://g' | sed 's/\r//g' | sed 's/\n//g' | sed "s/'//g" | sed 's/`//g' | sed 's/\"//g')
	echo "${ID_FILENAME}_53_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt		
		echo "text is [${text}]"
	echo "${ID_FILENAME}_54_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
		sleep ${POLLING_DELAY}
		#eval "wget -O /dev/null 'http://beta.teafone.com/msggw/sendMsg?sender=${senderPhoneNum}&receiver=${phoneNum}&subject=${ID_FILENAME}&message=${text}'"
        #echo "wget -O /dev/null 'http://beta.teafone.com/msggw/sendMsg?sender=${senderPhoneNum}&receiver=${phoneNum}&subject=${ID_FILENAME}&message=${text}'"
		eval "wget -O /dev/null 'http://beta.teafone.com/msggw/sendMsg?sender=${senderPhoneNum}&receiver=${phoneNum}&message=${text}'"
	echo "${ID_FILENAME}_55_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
        echo "wget -O /dev/null 'http://beta.teafone.com/msggw/sendMsg?sender=${senderPhoneNum}&receiver=${phoneNum}&message=${text}'"
	echo "${ID_FILENAME}_56_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
		ACION_LIST="${ACION_LIST}.recvFilterMsg"
	fi	
	
	echo "---------------------------------------------"
	echo "${ID_FILENAME}_ACION_LIST>>${ACION_LIST}"
	echo "${ID_FILENAME}_ACION_LIST>>${ACION_LIST}_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
	sleep ${POLLING_DELAY}
done

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${sendmsgCount}\t${revmsgCount}\t${filtedMsgCount}"
echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${sendmsgCount}\t${revmsgCount}\t${filtedMsgCount}" >> ./summary.txt
echo "${ID_FILENAME} complete!"
echo "${ID_FILENAME}_complete_$(date +%Y%m%d%H%M)" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt

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
echo "count" "$count" >> ./${ID_FILENAME}_json.txt

echo "sendmsgCount" "$sendmsgCount" >> ./${ID_FILENAME}_json.txt
echo "revmsgCount" "$revmsgCount" >> ./${ID_FILENAME}_json.txt
echo "filtedMsgCount" "$filtedMsgCount" >> ./${ID_FILENAME}_json.txt

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

