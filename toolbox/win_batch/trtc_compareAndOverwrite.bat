@echo off
setlocal enabledelayedexpansion
set WORK_FOLDER=C:\_webRTC\trtc\webrtc
set TARG_FOLDER=Z:\trtc_ing\trtc\webrtc

IF "%time:~0,1%" == " " (
set STARTTIME=%date:~0,4%%date:~5,2%%date:~8,2%0%time:~1,1%%time:~3,2%%time:~6,2%
) ELSE (
set STARTTIME=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
)

cd %WORK_FOLDER%
rem FOR /F "delims=" %%A in ('dir /OD /B') DO (
FOR /F "delims=" %%A in ('dir /S /B') DO (
    rem echo "%%~fA"
    set AFILE="%%~fA"
    set BFILE=!AFILE:%WORK_FOLDER%=%TARG_FOLDER%!
    if exist !AFILE!\ (
      rem echo "!AFILE! is a folder."
    ) else (
    if exist !BFILE! (
rem    fc /B !AFILE! !BFILE!
    fc !AFILE! !BFILE! > nul
    IF !errorlevel! EQU 1 (
        rem echo "errorlevel:!errorlevel!"
        rem echo "!AFILE! is different to !BFILE!"
        xcopy /Y !AFILE! !BFILE!
        echo "!AFILE! is copied to !BFILE!"
    ) else (
      rem echo "!BFILE! is not exist."
    )
    )
    )
)

set WORK_FOLDER=C:\_webRTC\trtc\ide\framework\android\sample\trtc\src\main\java
set TARG_FOLDER=Z:\trtc_ing\trtc\ide\framework\android\sample\trtc\src\main\java

cd %WORK_FOLDER%
rem FOR /F "delims=" %%A in ('dir /OD /B') DO (
FOR /F "delims=" %%A in ('dir /S /B') DO (
    rem echo "%%~fA"
    set AFILE="%%~fA"
    set BFILE=!AFILE:%WORK_FOLDER%=%TARG_FOLDER%!
    if exist !AFILE!\ (
      rem echo "!AFILE! is a folder."
    ) else (
    if exist !BFILE! (
rem    fc /B !AFILE! !BFILE!
    fc !AFILE! !BFILE! > nul
    IF !errorlevel! EQU 1 (
        rem echo "errorlevel:!errorlevel!"
        rem echo "!AFILE! is different to !BFILE!"
        xcopy /Y !AFILE! !BFILE!
        echo "!AFILE! is copied to !BFILE!"
    ) else (
      rem echo "!BFILE! is not exist."
    )
    )
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

exit 0

set WORK_FOLDER=C:\_webRTC\trtc\third_party
set TARG_FOLDER=Z:\trtc_ing\trtc\third_party

cd %WORK_FOLDER%
rem FOR /F "delims=" %%A in ('dir /OD /B') DO (
FOR /F "delims=" %%A in ('dir /S /B') DO (
    rem echo "%%~fA"
    set AFILE="%%~fA"
    set BFILE=!AFILE:%WORK_FOLDER%=%TARG_FOLDER%!
    if exist !AFILE!\ (
      rem echo "!AFILE! is a folder."
    ) else (
    if exist !BFILE! (
rem    fc /B !AFILE! !BFILE!
    fc !AFILE! !BFILE! > nul
    IF !errorlevel! EQU 1 (
        rem echo "errorlevel:!errorlevel!"
        rem echo "!AFILE! is different to !BFILE!"
        xcopy /Y !AFILE! !BFILE!
        echo "!AFILE! is copied to !BFILE!"
    ) else (
      rem echo "!BFILE! is not exist."
    )
    )
    )
)
