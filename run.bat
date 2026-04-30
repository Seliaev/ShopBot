@echo off
REM Скрипт запуска ShopBot (изолированное окружение)

set BOTDIR=%~dp0
set VENV=%BOTDIR%venv\Scripts\python.exe

if not exist "%VENV%" (
    echo [ShopBot] Создание окружения...
    py -3.12 -m venv "%BOTDIR%venv"
    "%BOTDIR%venv\Scripts\pip.exe" install aiogram==3.15.0 -q
)

echo [ShopBot] Запуск...
"%VENV%" "%BOTDIR%bot.py"

pause
