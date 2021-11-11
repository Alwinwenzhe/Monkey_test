:loop
set /a num+=1
if "%num%"=="2" goto end
adb -s NAB0220714016446 shell monkey -p com.jmbon.android --pct-syskeys 0 --pct-motion 0 --throttle 300 -s %random% -v 10000 > D:\python_script\monkey\monkey_test\monkey_test\bugreport_out\com.jmbon.android\com.jmbon.android-ANA-AN00\monkey_%Date:~0,4%%Date:~5,2%%Date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%.txt
@echo 测试成功完成，请查看日志文件~
adb -s NAB0220714016446 shell am force-stop com.jmbon.android
@ping -n 15 127.0.0.1 >nul
goto loop
:end