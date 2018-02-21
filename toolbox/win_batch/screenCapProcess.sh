#!/bin/bash
CAPTURE_PATH=/sdcard/hd_ar_capture
REQUEST_PATH=${CAPTURE_PATH}/requests
if [ -d ${REQUEST_PATH} ] ;then
  rm -rf ${REQUEST_PATH}
fi

while [ 1 ]
do
    echo -n "."
	if [ -d ${REQUEST_PATH} ] ;then
		if [ -f /system/bin/screencap ] ;then
		        REQUEST_FILE=$(ls -1 ${REQUEST_PATH}/)
                rm -rf ${REQUEST_PATH}
				screencap -p ${CAPTURE_PATH}/${REQUEST_FILE}
		        echo "screencap -p ${CAPTURE_PATH}/${REQUEST_FILE}"
    	else
				echo "not found screencap"
				exit 0
		fi
	fi
	sleep 1
done
