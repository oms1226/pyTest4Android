@echo on
:LOOP
adb -s ce0916097c6ab53502 shell input tap 400 1800
ping 127.0.0.1 -n 3 > nul
adb -s ce0916097c6ab53502 shell input tap 1050 1800
ping 127.0.0.1 -n 2 > nul
goto LOOP