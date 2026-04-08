@echo off
setlocal
title LazRecon v1.2.0 - Loader

:: Configuração de Cores (Fundo preto, texto verde)
color 0A

set "BASE_DIR=%~dp0"
set "SETUP_SCRIPT=%BASE_DIR%setup.ps1"
set "VENV_PATH=%BASE_DIR%.venv"

:: 1. Checagem de integridade do pacote
if not exist "%SETUP_SCRIPT%" (
    echo [!] ERRO CRITICO: Arquivo setup.ps1 nao encontrado.
    echo Certifique-se de extrair todos os arquivos do ZIP.
    pause
    exit /b
)

:: 2. Checagem do motor UV
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] AVISO: O gerenciador 'uv' nao foi detectado no seu sistema.
    echo Tentando prosseguir via instalador...
    timeout /t 3 >nul
)

:: 3. Fluxo de Inicialização Inteligente
if not exist "%VENV_PATH%" (
    echo ====================================================
    echo           CONFIGURACAO INICIAL DO LAZRECON
    echo ====================================================
    echo [*] Criando ambiente virtual e instalando dependencias...
    powershell -NoProfile -ExecutionPolicy Bypass -File "%SETUP_SCRIPT%"
) else (
    cls
    echo ====================================================
    echo           LAZRECON v1.2.0 - ASYNC ENGINE
    echo ====================================================
    echo [+] Ambiente: OK (.venv)
    echo [+] Motor: HTTPX / Asyncio
    echo [+] Workspace: Ativo
    echo ----------------------------------------------------
    echo [LOGS]:

    :: --- CORREÇÃO DE IDIOMA E ENCODE ---
    :: Limpa variáveis que podem forçar o PT-BR
    set LANG=en_US.UTF-8
    set LC_ALL=en_US.UTF-8
    set LANGUAGE=en_US.UTF-8
    
    :: Força o Python a ignorar a localidade do Windows e usar UTF-8
    set PYTHONIOENCODING=utf-8
    set PYTHONUTF8=1
    
    :: Execução direta via motor UV
    uv run main.py
)

:: 4. Captura de Erros Finais
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Ocorreu um problema ao rodar o LazRecon.
    echo [!] Codigo de erro: %ERRORLEVEL%
    pause
)

endlocal
