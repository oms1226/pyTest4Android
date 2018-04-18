@echo on

cd C:\_webRTC\trtc

xcopy /Y /S Z:\trtc_ing\trtc\ide\framework\android\sample\trtc\jni ide\framework\android\sample\trtc\jni && xcopy /Y /S Z:\trtc_ing\trtc\ide\framework\android\sample\trtc\libs ide\framework\android\sample\trtc\libs && xcopy /Y /S Z:\trtc_ing\trtc\ide\framework\android\sample\trtc\src\main\jniLibs ide\framework\android\sample\trtc\src\main\jniLibs && xcopy /Y /S Z:\trtc_ing\trtc\ide\framework\android\sample\trtc\src\main\res\raw ide\framework\android\sample\trtc\src\main\res\raw

echo %DATE%,%TIME%

pause