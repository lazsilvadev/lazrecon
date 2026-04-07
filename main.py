import pystray
import os
import sys
import threading
from PIL import Image
import flet as ft
from src.gui import build_ui
from src.translations import lang_en

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Referência global para a página
page_ptr = None

def tray_icon():
    global page_ptr
    icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
    
    try:
        img = Image.open(icon_path) if os.path.exists(icon_path) else Image.new('RGB', (64, 64), (33, 150, 243))
    except:
        img = Image.new('RGB', (64, 64), (255, 0, 0))

    def on_open(icon, item):
        if page_ptr:
            page_ptr.window.visible = True
            page_ptr.update()
            page_ptr.window.to_front()

    def on_exit(icon, item):
        icon.stop()
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem("Abrir LazRecon", on_open, default=True),
        pystray.MenuItem("Sair", on_exit)
    )
    
    icon = pystray.Icon("LazRecon", img, "LazRecon v1.2", menu)
    icon.run()

def main(page: ft.Page):
    global page_ptr
    page_ptr = page
    
    # 1. Configura o ícone da barra de título (o que aparece lá em cima)
    # Buscamos o ícone usando a função de path que criamos
    icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
    page.window.icon = icon_path
    
    # 2. Configurações de fechamento
    page.window.prevent_close = True
    
    def on_window_event(e):
        if e.data == "close":
            page.window.visible = False
            page.update()
    
    page.window.on_event = on_window_event

    # 3. Importante: Garanta que build_ui receba a página com os assets mapeados
    build_ui(page, lang_en)

if __name__ == "__main__":
    threading.Thread(target=tray_icon, daemon=True).start()
    
    # O assets_dir aqui deve ser o caminho absoluto extraído pelo PyInstaller
    assets_abs_path = get_resource_path("assets")
    ft.app(target=main, assets_dir=assets_abs_path)
