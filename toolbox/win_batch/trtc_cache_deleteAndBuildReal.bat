@echo off
setlocal enabledelayedexpansion

IF "%time:~0,1%" == " " (
set STARTTIME=%date:~0,4%%date:~5,2%%date:~8,2%0%time:~1,1%%time:~3,2%%time:~6,2%
) ELSE (
set STARTTIME=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
)

call trtc_cache_delete.bat -np

set ERROR_DETECT=false

cd C:\_android\workspace\tphone_android\trtcLib
FOR /F "delims=" %%A in ('dir /S /B *.aar') DO (
    set TARGETFILE="%%~fA"
)

echo "TARGETFILE:%TARGETFILE%"

set SOURCEFILE=Z:\trtc_ing\trtc\ide\framework\android\trtc\trtc.aar
echo "SOURCEFILE:%SOURCEFILE%"
if exist %SOURCEFILE% (
    xcopy /Y /S %SOURCEFILE% %TARGETFILE%
) else (
    echo "not Found: %SOURCEFILE%"
    set ERROR_DETECT=true
)

if %ERROR_DETECT% == false (
cd C:\_android\workspace\tphone_android
gradlew clean dialer:devReleaseSigningTaskRealDebug_dialer

if exist C:\_android\workspace\tphone_android\dialer\build\outputs\apk\real\debug\dialer-real-debug-unsigned-signed.apk (
    call adb -d install -r -d C:\_android\workspace\tphone_android\dialer\build\outputs\apk\real\debug\dialer-real-debug-unsigned-signed.apk
) else (
    echo "build failed!"
)
)

IF "%time:~0,1%" == " " (
set END__TIME=%date:~0,4%%date:~5,2%%date:~8,2%0%time:~1,1%%time:~3,2%%time:~6,2%
) ELSE (
set END__TIME=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
)

echo "STARTTIME:%STARTTIME%"
echo "END__TIME:%END__TIME%"

pause