@echo off

echo Run settings environment...
set dir_bat=%cd%
set dir_env=%dir_bat%\env_gitlab

echo 1.5 Install environment
python -m venv %dir_env%
echo 2.5 Activate environment
call %dir_env%\Scripts\activate.bat
echo 3.5 Install dependencies
pip install -r %dir_bat%\requirements.txt
echo 4.5 Deactivate environment
call %dir_env%\Scripts\deactivate.bat
echo 5.5 Done!
pause
exit /B 1
