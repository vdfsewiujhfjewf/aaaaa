@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [Setup] Creating virtual environment...
  py -3 -m venv .venv
  if errorlevel 1 goto :error
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 goto :error

echo [Setup] Installing dependencies...
python -m pip install -U pip
if errorlevel 1 goto :error
python -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo [Run] Open http://127.0.0.1:5000 in your browser.
python web_voice_control.py
goto :eof

:error
echo [Error] Setup or launch failed.
exit /b 1
