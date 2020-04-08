
@echo off
SET SYSTEMSETTINGSPATH="C:\Users\06268818\Documents\My Games\Rocket League\TAGame\Config\"

if %1==RLBOT ( echo "SETTING RLBOT CONFIG.." 
del %SYSTEMSETTINGSPATH%"TASystemSettings.ini" 
copy %SYSTEMSETTINGSPATH%"SystemSettings\RLBOT_TASystemSettings.ini" %SYSTEMSETTINGSPATH%"TASystemSettings.ini")
if %1==DEFAULT ( echo "SETTING DEFAULT CONFIG.." 
del %SYSTEMSETTINGSPATH%"TASystemSettings.ini" 
copy %SYSTEMSETTINGSPATH%"SystemSettings\DEFAULT_TASystemSettings.ini" %SYSTEMSETTINGSPATH%"TASystemSettings.ini")

