import os
import sys

def get_asset_path(rel_path: str) -> str:
    """
    Resolve o caminho de assets para desenvolvimento e executável (PyInstaller).
    Garante que o caminho suba um nível se for chamado de dentro de 'src'.
    """
    if getattr(sys, "frozen", False):
        # O PyInstaller extrai tudo para esta pasta temporária
        base = sys._MEIPASS 
    else:
        # Em desenvolvimento, pegamos a pasta raiz do projeto (um nível acima de 'src')
        # Se este arquivo estiver na raiz, use apenas: os.path.dirname(__file__)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(current_dir) == "src":
            base = os.path.dirname(current_dir)
        else:
            base = current_dir

    return os.path.join(base, rel_path)
