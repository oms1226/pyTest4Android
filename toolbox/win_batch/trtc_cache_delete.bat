@echo off
setlocal enabledelayedexpansion
set WORK_FOLDER=C:\Users\owner\.gradle\caches\transforms-1\files-1.1

if not "%1"=="" (
    set CMD_GET_STR_VAL=%1
    shift
    echo "CMD_GET_STR_VAL: !CMD_GET_STR_VAL!"
) else (
    set CMD_GET_STR_VAL=
)


cd %WORK_FOLDER%
FOR /F "delims=" %%A in ('dir /OD /B') DO (
    rem echo "%%~fA"
    set AFILE="%%~fA"
    set BFILE=!AFILE:trtc=del!
    rem echo !BFILE!
    if !AFILE! == !BFILE! (
      rem echo "!AFILE! is not related to trtc."
    ) else (
      rmdir /S /Q !AFILE!
      echo "rmdir /S /Q !AFILE!"
      if exist !AFILE! (
          del /Q /S !AFILE!
          echo "del /Q /S !AFILE!"
      )
    )
)

if "%CMD_GET_STR_VAL%"=="-np" (
    echo "not pause!"
) else (
    pause
)