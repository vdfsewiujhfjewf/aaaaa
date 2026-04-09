@echo off
setlocal

REM Move to this script's directory
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

if not exist "start_config.bat" (
  echo [Info] start_config.bat not found. Creating defaults...
  (
    echo @echo off
    echo REM Voice changer settings ^(edit freely^)
    echo set SEMITONES=4
    echo set BLOCKSIZE=512
    echo set CHANNELS=1
    echo set GAIN_DB=0
    echo set PRESET=male_to_female
    echo set HIGHPASS_HZ=70
    echo set INPUT_DEVICE=
    echo set OUTPUT_DEVICE=
    echo set EXTRA_ARGS=
  )>start_config.bat
)

call start_config.bat
if errorlevel 1 goto :error

set "CMD=python voice_changer.py --preset %PRESET% --semitones %SEMITONES% --highpass-hz %HIGHPASS_HZ% --blocksize %BLOCKSIZE% --channels %CHANNELS% --gain-db %GAIN_DB%"
if not "%INPUT_DEVICE%"=="" set "CMD=%CMD% --input-device %INPUT_DEVICE%"
if not "%OUTPUT_DEVICE%"=="" set "CMD=%CMD% --output-device %OUTPUT_DEVICE%"
if not "%EXTRA_ARGS%"=="" set "CMD=%CMD% %EXTRA_ARGS%"

echo.
echo [Run] %CMD%
echo.
%CMD%
goto :eof

:error
echo.
echo [Error] Setup or launch failed.
exit /b 1
