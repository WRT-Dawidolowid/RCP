@echo off
cd %~dp0%
echo Starting RCP...
:exist
pip install -r requirements.txt >nul
echo Software in USE!
start /wait python3 server.py >nul 2>&1
echo ######################################
echo #        Software Terminated!        #
echo #    Leave a star for us on GitHub   #
echo ######################################
echo.
pause
exit