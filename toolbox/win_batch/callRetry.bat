@echo on
:LOOP
adb -s ce1115fbd5ad960201 shell input tap 500 1800
ping 127.0.0.1 -n 3 > nul
adb -s ce1115fbd5ad960201 shell input tap 150 1800
ping 127.0.0.1 -n 20 > nul
adb -s ce1115fbd5ad960201 shell input tap 960 1730
ping 127.0.0.1 -n 10 > nul
goto LOOP