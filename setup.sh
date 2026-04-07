#!/bin/bash

# Cores para o terminal
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}--- [ LazRecon v1.2.0 | UV Loader (Linux/macOS) ] ---${NC}"

# 1. Garante que o UV está instalado
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}[setup] UV não encontrado. Instalando motor UV...${NC}"
    # Instalação oficial do UV via script shell
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Tenta carregar o env do UV para a sessão atual
    if [ -f "$HOME/.cargo/env" ]; then
        source "$HOME/.cargo/env"
    fi
    # Adiciona o caminho padrão do UV ao PATH temporário caso o source falhe
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# 2. Sincroniza as dependências forçando o Python 3.12
echo -e "${CYAN}[setup] Sincronizando bibliotecas (Flet, Pystray...)${NC}"
echo -e "${CYAN}[setup] Garantindo isolamento com Python 3.12...${NC}"

# O comando '--python 3.12' faz o UV buscar essa versão específica no sistema
# Se não encontrar, o UV é inteligente o suficiente para sugerir a instalação.
uv sync --python 3.12 --no-install-project

# 3. Execução via UV Run
MAIN_SCRIPT="./main.py"

if [ -f "$MAIN_SCRIPT" ]; then
    echo -e "${GREEN}[setup] Iniciando LazRecon...${NC}"
    # O 'uv run' utilizará automaticamente o venv criado com a 3.12
    uv run main.py
else
    echo -e "${RED}[!] Erro fatal: main.py não encontrado no diretório atual.${NC}"
    echo -e "${RED}Certifique-se de executar o script na raiz do projeto.${NC}"
    exit 1
fi