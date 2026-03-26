#!/usr/bin/env bash
# Setup do ambiente (POSIX shell)
# Executar na raiz do projeto: ./scripts/setup_poetry.sh
set -euo pipefail

echo "1) Verificando Python..."
if ! command -v python >/dev/null 2>&1; then
  echo "Python não encontrado no PATH. Instale Python 3.13+ e tente novamente." >&2
  exit 1
fi

echo "2) Atualizando pip..."
python -m pip install --upgrade pip

echo "3) Instalando/atualizando Poetry..."
python -m pip install --user --upgrade poetry

echo "4) Configurando poetry para criar venvs in-project e instalando dependências..."
poetry config virtualenvs.in-project true --local
poetry install

echo "Concluído. Ative o venv com: source .venv/bin/activate e rode a aplicação."