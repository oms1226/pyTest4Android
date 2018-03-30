#!/bin/bash

programeName=ShareMouse
ppid=`ps -Af | grep ${programeName} | head -n 1 | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'| sed 's/  //g' |cut -f3 -d " "`
echo "${programeName}->ppid:${ppid}"
if ((${ppid} == 1))
then
    pid=`ps -Af | grep ${programeName} | head -n 1 | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'| sed 's/  //g' |cut -f2 -d " "`
    echo "${programeName}->pid:${pid}"
#    kill ${pid}
#    echo "kill ${pid}"
else
    echo "not found ${programeName}"
    open -a ${programeName}
    echo "open -a ${programeName}"    
fi
