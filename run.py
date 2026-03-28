from pathlib import Path
import sys

# Garantir que o diretório src esteja no PATH para imports locais
sys.path.insert(0, str(Path(__file__).parent.joinpath("src")))

from lazrecon import main
import flet as ft


def find_assets_dir() -> str:
    root = Path(__file__).parent
    candidate = root.joinpath("src", "lazrecon", "assets")
    if candidate.exists():
        return str(candidate)
    fallback = root.joinpath("assets")
    return str(fallback) if fallback.exists() else str(root)


if __name__ == "__main__":
    print("[*] Iniciando LazRecon Fuzzer...")
    assets_dir = find_assets_dir()
    print(f"[+] Assets carregados de: {assets_dir}")
    ft.app(target=main, assets_dir=assets_dir)
