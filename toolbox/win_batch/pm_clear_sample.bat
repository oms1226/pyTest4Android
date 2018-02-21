@echo off

FOR /F %%A in ('adb devices') DO (
    echo adb -s %%A shell pm clear com.skt.trtc.sample
    adb -s %%A shell pm clear com.skt.trtc.sample

)