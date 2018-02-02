rem C:\Android\sdk-tools-windows-3859397\emulator\emulator.exe -ports 9898,5555 -avd pixel -gpu host
rem C:\Users\owner\AppData\Local\Android\sdk\emulator\emulator.exe -ports 681,5555 -avd Pixel_XL_API_24 -gpu host

set ANDROID_AVD_HOME="C:\Users\owner\.android\avd"
set ANDROID_SDK_ROOT="C:\Users\owner\AppData\Local\Android\sdk"
if exist C:\Users\owner\AppData\Local\Android\sdk\emulator\emulator.exe (
C:\Users\owner\AppData\Local\Android\sdk\emulator\emulator.exe -ports 681,5555 -avd Pixel_XL_API_25_x64 -gpu host
) else if exist B:\Android\sdk\emulator\emulator.exe (
B:\Android\sdk\emulator\emulator.exe -ports 681,5555 -avd Pixel_XL_API_25_x64 -gpu host
)