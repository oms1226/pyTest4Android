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

DalvikHeap_Size_AVG=0
DalvikHeap_Size_MAX=0
DalvikHeap_Size_MIN=${INT_MAX}

DalvikHeapAlloc_AVG=0
DalvikHeapAlloc_MAX=0
DalvikHeapAlloc_MIN=${INT_MAX}

DalvikHeap_Free_AVG=0
DalvikHeap_Free_MAX=0
DalvikHeap_Free_MIN=${INT_MAX}
	
NativeHeap_Size_AVG=0
NativeHeap_Size_MAX=0
NativeHeap_Size_MIN=${INT_MAX}

NativeHeapAlloc_AVG=0
NativeHeapAlloc_MAX=0
NativeHeapAlloc_MIN=${INT_MAX}

NativeHeap_Free_AVG=0
NativeHeap_Free_MAX=0
NativeHeap_Free_MIN=${INT_MAX}

previousPID=0

count=0
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
    echo "DalvikHeap_Size" "$DalvikHeap_Size" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "DalvikHeapAlloc" "$DalvikHeapAlloc" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "DalvikHeap_Free" "$DalvikHeap_Free" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "NativeHeap_Size" "$NativeHeap_Size" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "NativeHeapAlloc" "$NativeHeapAlloc" >> ./${ID_FILENAME}_json_snapshot.txt
    echo "NativeHeap_Free" "$NativeHeap_Free" >> ./${ID_FILENAME}_json_snapshot.txt

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
	
	pid=$(adb -s ${deviceID} shell ps | grep ${packageName} | sed 's/  */ /g' | sed 's/\r//g' | cut -f2 -d " ")

	echo "pid is [${pid}]" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
	echo "previousPID is [${previousPID}]" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
	
	if [ -n "$pid" -a  -n "$previousPID" -a ${previousPID} -ne ${pid} ]
	then
		echo "{\"process_mem_lastreport\":{\"pid\":${previousPID},\"DalvikHeap_Size\":${DalvikHeap_Size},\"DalvikHeap_Size_MAX\":${DalvikHeap_Size_MAX},\"DalvikHeapAlloc\":${DalvikHeapAlloc},\"DalvikHeapAlloc_MAX\":${DalvikHeapAlloc_MAX},\"DalvikHeap_Free\":${DalvikHeap_Free},\"DalvikHeap_Free_MAX\":${DalvikHeap_Free_MAX},\"NativeHeap_Size\":${NativeHeap_Size},\"NativeHeap_Size_MAX\":${NativeHeap_Size_MAX},\"NativeHeapAlloc\":${NativeHeapAlloc},\"NativeHeapAlloc_MAX\":${NativeHeapAlloc_MAX},\"NativeHeap_Free\":${NativeHeap_Free},\"NativeHeap_Free_MAX\":${NativeHeap_Free_MAX}}}" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_Logging.txt
		echo "{\"process_mem_lastreport\":{\"pid\":${previousPID},\"DalvikHeap_Size\":${DalvikHeap_Size},\"DalvikHeap_Size_MAX\":${DalvikHeap_Size_MAX},\"DalvikHeapAlloc\":${DalvikHeapAlloc},\"DalvikHeapAlloc_MAX\":${DalvikHeapAlloc_MAX},\"DalvikHeap_Free\":${DalvikHeap_Free},\"DalvikHeap_Free_MAX\":${DalvikHeap_Free_MAX},\"NativeHeap_Size\":${NativeHeap_Size},\"NativeHeap_Size_MAX\":${NativeHeap_Size_MAX},\"NativeHeapAlloc\":${NativeHeapAlloc},\"NativeHeapAlloc_MAX\":${NativeHeapAlloc_MAX},\"NativeHeap_Free\":${NativeHeap_Free},\"NativeHeap_Free_MAX\":${NativeHeap_Free_MAX}}}" >> ./rawinfo_${ID_FILENAME}_${START_TIME}_PIDREPORT.txt
		previousPID=${pid}
	fi	
	
	rm -f ./rawinfo_${ID_FILENAME}.txt
        `adb -s ${deviceID} shell dumpsys meminfo ${packageName} > rawinfo_${ID_FILENAME}.txt`
	sleep ${POLLING_DELAY}
	line_DalvikHeap=$(cat rawinfo_${ID_FILENAME}.txt | grep 'Dalvik Heap' | sed 's/  */ /g' | sed 's/ //' | sed 's/\r//g')
#	echo "line_DalvikHeap is [${line_DalvikHeap}]"
	if [ ! -n "$line_DalvikHeap" ]
	then
		continue
	fi	
	line_NativeHeap=$(cat rawinfo_${ID_FILENAME}.txt | grep 'Native Heap ' | sed 's/  */ /g' | sed 's/ //' | sed 's/\r//g')
#	echo "line_NativeHeap is [${line_NativeHeap}]"			
	if [ ! -n "$line_NativeHeap" ]
	then
		continue
	fi	


        result=$(echo ${line_DalvikHeap} | cut -f7 -d " ")
	if [ ! $(echo $result | egrep "[0-9]+") ]; then
		continue
	fi	
	DalvikHeap_Size=${result}
	
        result=$(echo ${line_DalvikHeap} | cut -f8 -d " ")
	if [ ! $(echo $result | egrep "[0-9]+") ]; then
		continue
	fi	
	DalvikHeapAlloc=${result}
	
        result=$(echo ${line_DalvikHeap} | cut -f9 -d " ")
	if [ ! $(echo $result | egrep "[0-9]+") ]; then
		continue
	fi
	DalvikHeap_Free=${result}
	
        result=$(echo ${line_NativeHeap} | cut -f7 -d " ")
	if [ ! $(echo $result | egrep "[0-9]+") ]; then
		continue
	fi	
	NativeHeap_Size=${result}
	
        result=$(echo ${line_NativeHeap} | cut -f8 -d " ")
	if [ ! $(echo $result | egrep "[0-9]+") ]; then
		continue
	fi	
	NativeHeapAlloc=${result}
	
        result=$(echo ${line_NativeHeap} | cut -f9 -d " ")
	if [ ! $(echo $result | egrep "[0-9]+") ]; then
		continue
	fi	
	NativeHeap_Free=${result}

	count=`expr $count + 1`
	execTiime=`eval date +%Y%m%d%H%M`
#** MEMINFO in pid 6673 [com.skt.prod.tmessage] **
#                   Pss  Private  Private  Swapped     Heap     Heap     Heap
#                 Total    Dirty    Clean    Dirty     Size    Alloc     Free
#                ------   ------   ------   ------   ------   ------   ------
#  Native Heap    24102    24020        8     3612    45184    29662    15521
#  Dalvik Heap    39414    39240        0     1700    54062    37820    16242
	
#	DalvikHeap_Size_AVG=$((($DalvikHeap_Size_AVG*($count-1)+$DalvikHeap_Size)/$count))
	DalvikHeap_Size_AVG=`echo "${DalvikHeap_Size_AVG} $(($count-1)) ${DalvikHeap_Size} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`	
#	DalvikHeapAlloc_AVG=$((($DalvikHeapAlloc_AVG*($count-1)+$DalvikHeapAlloc)/$count))
	DalvikHeapAlloc_AVG=`echo "${DalvikHeapAlloc_AVG} $(($count-1)) ${DalvikHeapAlloc} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`
#	DalvikHeap_Free_AVG=$((($DalvikHeap_Free_AVG*($count-1)+$DalvikHeap_Free)/$count))
	DalvikHeap_Free_AVG=`echo "${DalvikHeap_Free_AVG} $(($count-1)) ${DalvikHeap_Free} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`
#	NativeHeap_Size_AVG=$((($NativeHeap_Size_AVG*($count-1)+$NativeHeap_Size)/$count))
	NativeHeap_Size_AVG=`echo "${NativeHeap_Size_AVG} $(($count-1)) ${NativeHeap_Size} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`
#	NativeHeapAlloc_AVG=$((($NativeHeapAlloc_AVG*($count-1)+$NativeHeapAlloc)/$count))
	NativeHeapAlloc_AVG=`echo "${NativeHeapAlloc_AVG} $(($count-1)) ${NativeHeapAlloc} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`
#	NativeHeap_Free_AVG=$((($NativeHeap_Free_AVG*($count-1)+$NativeHeap_Free)/$count))
	NativeHeap_Free_AVG=`echo "${NativeHeap_Free_AVG} $(($count-1)) ${NativeHeap_Free} ${count}"|awk '{printf "%.5f", ($1 * $2 + $3) / $4}'`

	if [ ${DalvikHeap_Size} -gt ${DalvikHeap_Size_MAX} ]
	then
		DalvikHeap_Size_MAX=${DalvikHeap_Size}
	fi

	if [ ${DalvikHeap_Size_MIN} -gt ${DalvikHeap_Size} ]
	then
		DalvikHeap_Size_MIN=${DalvikHeap_Size}
	fi

	if [ ${DalvikHeapAlloc} -gt ${DalvikHeapAlloc_MAX} ]
	then
		DalvikHeapAlloc_MAX=${DalvikHeapAlloc}
	fi

	if [ ${DalvikHeapAlloc_MIN} -gt ${DalvikHeapAlloc} ]
	then
		DalvikHeapAlloc_MIN=${DalvikHeapAlloc}
	fi

	if [ ${DalvikHeap_Free} -gt ${DalvikHeap_Free_MAX} ]
	then
		DalvikHeap_Free_MAX=${DalvikHeap_Free}
	fi

	if [ ${DalvikHeap_Free_MIN} -gt ${DalvikHeap_Free} ]
	then
		DalvikHeap_Free_MIN=${DalvikHeap_Free}
	fi
	
	if [ ${NativeHeap_Size} -gt ${NativeHeap_Size_MAX} ]
	then
		NativeHeap_Size_MAX=${NativeHeap_Size}
	fi

	if [ ${NativeHeap_Size_MIN} -gt ${NativeHeap_Size} ]
	then
		NativeHeap_Size_MIN=${NativeHeap_Size}
	fi	

	if [ ${NativeHeapAlloc} -gt ${NativeHeapAlloc_MAX} ]
	then
		NativeHeapAlloc_MAX=${NativeHeapAlloc}
	fi

	if [ ${NativeHeapAlloc_MIN} -gt ${NativeHeapAlloc} ]
	then
		NativeHeapAlloc_MIN=${NativeHeapAlloc}
	fi	


	if [ ${NativeHeap_Free} -gt ${NativeHeap_Free_MAX} ]
	then
		NativeHeap_Free_MAX=${NativeHeap_Free}
	fi

	if [ ${NativeHeap_Free_MIN} -gt ${NativeHeap_Free} ]
	then
		NativeHeap_Free_MIN=${NativeHeap_Free}
	fi	

	writeTrace

	echo "============================================="		
        result=$(echo ${line_DalvikHeap} | sed 's/  */ /g' | sed 's/ //')
	echo "${result}"
	echo "filter>>${DalvikHeap_Size} ${DalvikHeapAlloc} ${DalvikHeap_Free}"
	echo "DalvikHeap_Size_AVG is ${DalvikHeap_Size_AVG}"
	echo "DalvikHeap_Size_MAX is ${DalvikHeap_Size_MAX}"
	echo "DalvikHeap_Size_MIN is ${DalvikHeap_Size_MIN}"		
	echo "---------------------------------------------"	
	echo "DalvikHeapAlloc_AVG is ${DalvikHeapAlloc_AVG}"	
	echo "DalvikHeapAlloc_MAX is ${DalvikHeapAlloc_MAX}"	
	echo "DalvikHeapAlloc_MIN is ${DalvikHeapAlloc_MIN}"			
	echo "---------------------------------------------"	
	echo "DalvikHeap_Free_AVG is ${DalvikHeap_Free_AVG}"
	echo "DalvikHeap_Free_MAX is ${DalvikHeap_Free_MAX}"
	echo "DalvikHeap_Free_MIN is ${DalvikHeap_Free_MIN}"		
	echo "============================================="	
        result=$(echo ${line_NativeHeap} | sed 's/  */ /g' | sed 's/ //')
	echo "${result}"
	echo "filter>>${NativeHeap_Size} ${NativeHeapAlloc} ${NativeHeap_Free}"	
	echo "NativeHeap_Size_AVG is ${NativeHeap_Size_AVG}"			
	echo "NativeHeap_Size_MAX is ${NativeHeap_Size_MAX}"			
	echo "NativeHeap_Size_MIN is ${NativeHeap_Size_MIN}"					
	echo "---------------------------------------------"	
	echo "NativeHeapAlloc_AVG is ${NativeHeapAlloc_AVG}"				
	echo "NativeHeapAlloc_MAX is ${NativeHeapAlloc_MAX}"				
	echo "NativeHeapAlloc_MIN is ${NativeHeapAlloc_MIN}"						
	echo "---------------------------------------------"	
	echo "NativeHeap_Free_AVG is ${NativeHeap_Free_AVG}"						
	echo "NativeHeap_Free_MAX is ${NativeHeap_Free_MAX}"				
	echo "NativeHeap_Free_MIN is ${NativeHeap_Free_MIN}"						

	sleep ${POLLING_DELAY}
done

echo -e "${UUID}\t${deviceID}\t${packageName}\t${git_branchName}\t${git_commitValue}\t${git_revCount}\t${ID_FILENAME}\t${START_TIME}\t${EXPECT_END_TIME}\t${duringHours}\t${throttle}\t${count}\t${DalvikHeap_Size_AVG}\t${DalvikHeap_Size_MAX}\t${DalvikHeap_Size_MIN}\t${DalvikHeapAlloc_AVG}\t${DalvikHeapAlloc_MAX}\t${DalvikHeapAlloc_MIN}\t${DalvikHeap_Free_AVG}\t${DalvikHeap_Free_MAX}\t${DalvikHeap_Free_MIN}\t${NativeHeap_Size_AVG}\t${NativeHeap_Size_MAX}\t${NativeHeap_Size_MIN}\t${NativeHeapAlloc_AVG}\t${NativeHeapAlloc_MAX}\t${NativeHeapAlloc_MIN}\t${NativeHeap_Free_AVG}\t${NativeHeap_Free_MAX}\t${NativeHeap_Free_MIN}" >> ./summary.txt

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

echo "DalvikHeap_Size_AVG" "$DalvikHeap_Size_AVG" >> ./${ID_FILENAME}_json.txt
echo "DalvikHeap_Size_MAX" "$DalvikHeap_Size_MAX" >> ./${ID_FILENAME}_json.txt
echo "DalvikHeap_Size_MIN" "$DalvikHeap_Size_MIN" >> ./${ID_FILENAME}_json.txt

echo "DalvikHeapAlloc_AVG" "$DalvikHeapAlloc_AVG" >> ./${ID_FILENAME}_json.txt
echo "DalvikHeapAlloc_MAX" "$DalvikHeapAlloc_MAX" >> ./${ID_FILENAME}_json.txt
echo "DalvikHeapAlloc_MIN" "$DalvikHeapAlloc_MIN" >> ./${ID_FILENAME}_json.txt

echo "DalvikHeap_Free_AVG" "$DalvikHeap_Free_AVG" >> ./${ID_FILENAME}_json.txt
echo "DalvikHeap_Free_MAX" "$DalvikHeap_Free_MAX" >> ./${ID_FILENAME}_json.txt
echo "DalvikHeap_Free_MIN" "$DalvikHeap_Free_MIN" >> ./${ID_FILENAME}_json.txt

echo "NativeHeap_Size_AVG" "$NativeHeap_Size_AVG" >> ./${ID_FILENAME}_json.txt
echo "NativeHeap_Size_MAX" "$NativeHeap_Size_MAX" >> ./${ID_FILENAME}_json.txt
echo "NativeHeap_Size_MIN" "$NativeHeap_Size_MIN" >> ./${ID_FILENAME}_json.txt

echo "NativeHeapAlloc_AVG" "$NativeHeapAlloc_AVG" >> ./${ID_FILENAME}_json.txt
echo "NativeHeapAlloc_MAX" "$NativeHeapAlloc_MAX" >> ./${ID_FILENAME}_json.txt
echo "NativeHeapAlloc_MIN" "$NativeHeapAlloc_MIN" >> ./${ID_FILENAME}_json.txt

echo "NativeHeap_Free_AVG" "$NativeHeap_Free_AVG" >> ./${ID_FILENAME}_json.txt
echo "NativeHeap_Free_MAX" "$NativeHeap_Free_MAX" >> ./${ID_FILENAME}_json.txt
echo "NativeHeap_Free_MIN" "$NativeHeap_Free_MIN" >> ./${ID_FILENAME}_json.txt

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
