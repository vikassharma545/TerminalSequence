@echo off
:: Check for admin permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:: Install dependencies
echo Installing Python dependencies...
pip install psutil screeninfo pygetwindow pywin32

:: Set script path
set "SCRIPT_PATH=C:\Program Files\TerminalPosition\window_sequence.py"
if not exist "%SCRIPT_PATH%" (
    echo Error: window_sequence.py not found in C:\Program Files\TerminalPosition
    pause
    exit /B
)

:: Find Python executable
set "PYTHON_EXEC="
for %%i in (python.exe) do set "PYTHON_EXEC=%%~$PATH:i"
if "%PYTHON_EXEC%"=="" (
    echo Error: Python not found in PATH. Please ensure Python is installed and added to PATH.
    pause
    exit /B
)

:: Add context menu entry
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\RunWindowSequence" /ve /d "Terminal Sequence" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\RunWindowSequence\command" /ve /d "\"%PYTHON_EXEC%\" \"%SCRIPT_PATH%\"" /f
if %errorlevel%==0 (
    echo Context menu added successfully.
) else (
    echo Error: Failed to add context menu entry.
)
pause