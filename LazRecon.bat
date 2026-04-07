@echo off
title LazRecon v1.2.0 - Loader

:: %~dp0 garante que o Windows sempre olhe para a pasta onde o .bat está guardado
set SCRIPT_PATH=%~dp0setup.ps1

:: Verifica se o setup.ps1 realmente existe lá antes de tentar rodar
if exist "%SCRIPT_PATH%" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_PATH%"
) else (
    echo [!] Erro: Nao foi possivel encontrar o arquivo setup.ps1 em:
    echo %~dp0
    echo Certifique-se de que o .bat esteja na mesma pasta do projeto.
    pause
)