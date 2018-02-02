@echo off
echo execTime:%DATE%,%TIME%
echo ..60 sec waiting...
ping 127.0.0.1 -n 60 >  nul
start "filebeat" /SEPARATE cmd /c "cd filebeat\filebeat-5.6.3-windows-x86_64 && filebeat -e -c filebeat.yml"
echo ..60 sec waiting...
ping 127.0.0.1 -n 60 >  nul
rem start "CallRecordingTest" /SEPARATE cmd /c "cd CallRecordingTest && python pyCallRecordingTestMultiThread.py -a -h 12 -logcat "tag:E TPhone""
cmd /c "cd CallRecordingTest && python pyCallRecordingTestMultiThread.py -a -h 12 -logcat "tag:E TPhone""
echo endTime:%DATE%,%TIME%
pause