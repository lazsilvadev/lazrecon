# =================================================================
# LAZRECON v1.2 - INTERFACE WORKER (GUI) - TRANSLATED VERSION
# =================================================================
# Este arquivo é o "Worker" de interface do projeto.
# 1. Este script gerencia APENAS a renderização da UI e o Fuzzer.
# 2. Agora configurado para utilizar o dicionário de tradução (translations.py).

import flet as ft
import sys
import ctypes
from src.ui import build_ui
# Importamos o dicionário de inglês
from translations import lang_en

# --- ID do Windows (Garante o agrupamento na barra de tarefas) ---
if sys.platform == "win32":
    my_app_id = "laz.recon.fuzzer.v1"  
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
    except Exception: 
        pass

def main(page: ft.Page):
    # Definimos o título da janela usando o arquivo de tradução
    # Certifique-se de que a chave "title" existe no seu lang_en
    page.title = lang_en.get("app_title", "LazRecon v1.2")
    
    # IMPORTANTE: 
    # Agora passamos o lang_en para dentro do build_ui.
    # Você precisará ajustar o arquivo 'src/ui.py' para receber esse argumento!
    build_ui(page, lang_en) 
    
    # Gerenciamento do fechamento da janela
    def handle_window_event(e):
        if e.data == "close":
            # Destrói a janela para encerrar o processo gui.py
            page.window.destroy()
            
    page.on_window_event = handle_window_event
    page.update()

if __name__ == "__main__":
    # Inicia a interface como um processo isolado
    ft.app(target=main, assets_dir="assets")
