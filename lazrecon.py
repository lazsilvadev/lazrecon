import flet as ft
import requests
import threading
import webbrowser
import os
import sys
import datetime
import re
from urllib.parse import urlparse
from fpdf import FPDF
import ctypes

# Esse trecho é para garantir o ícone da ferramenta fique agrupado corretamente na barra de tarefas do Windows.
if sys.platform == "win32":
    my_app_id = "laz.recon.fuzzer.v1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

def main(page: ft.Page):
    page.title = "LazRecon v1.1 - Web Path Reconnaissance Tool"
    page.theme_mode = ft.ThemeMode.DARK

    # Definir tamanho inicial e travar tamanho (não redimensionável)
    page.window.width = 700  # Largura fixa
    page.window.height = 880  # Altura fixa
    page.window.resizable = False  # Trava o tamanho (impede esticar)
    page.window.maximizable = False  # Desativa o botão de maximizar

    # 3. Centraliza a janela ao abrir
    # Nem todas as versões/ambientes do Flet expõem `window_center` 
    # use hasattr para evitar AttributeError em runtime.
    if hasattr(page, "window_center"):
        try:
            page.window_center()
        except Exception:
            pass

    # Código da interface
    page.add(ft.Text(""))
    # Impedir que o usuário redimensione ou maximize a janela
    page.window_resizable = False
    try:
        page.window_maximizable = False
    except Exception:
        pass

    page.window_icon = "lazrecon.png"  # Tentativa de definir ícone via atributo específico (pode ser ignorado em alguns sistemas)
    header_image_src = "/lazrecon.png"

    # Helper para resolver caminhos de assets em dev e quando empacotado (PyInstaller/_MEIPASS)
    def get_asset_path(rel_path: str) -> str:
        if getattr(sys, "frozen", False):
            base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
        else:
            base = os.path.dirname(__file__)
        return os.path.join(base, rel_path)

    # Definir ícone da janela / barra de tarefas (usa assets_dir do ft.app)
    icon_path = get_asset_path("icon.ico")
    for _attr in ("window_icon", "app_icon", "icon"):
        try:
            if hasattr(page, _attr):
                setattr(page, _attr, icon_path)
        except Exception:
            # Silencioso: continua se atributo não suportado
            pass

    # Wordlist padrão (fallback)
    default_wordlist = [
        # Portais e Acesso
        "admin",
        "administrator",
        "login",
        "logon",
        "wp-admin",
        "panel",
        "painel",
        # Configurações e Backups (Onde moram as senhas)
        "config",
        "conf",
        "backup",
        "bak",
        "old",
        "db",
        "database",
        "sql",
        "setup",
        # Desenvolvimento e Versão
        "dev",
        "development",
        "v1",
        "v2",
        "api",
        "test",
        "testing",
        "src",
        "git",
        # Arquivos de Sistema e Servidor
        "phpmyadmin",
        "server-status",
        "dashboard",
        "console",
        "shell",
        # Pastas de Conteúdo e Uploads
        "uploads",
        "files",
        "images",
        "img",
        "assets",
        "css",
        "js",
        "javascript",
        # Arquivos Específicos (Tente acessar diretamente)
        "robots.txt",
        "info.php",
        "phpinfo.php",
        ".htaccess",
        ".env",
        "config.php",
        "README.md",
        "license.txt",
        "index.php.bak",
        "user.txt",
        "root.txt",
        # Pastas de Servidor (Geralmente dão 403 se o "Indexes" estiver off)
        ".htaccess",
        ".htpasswd",
        ".git",
        ".svn",
        ".env",
        ".ssh",
        "cgi-bin",
        "server-status",
        "server-info",
        "logs",
        "error_log",
        # Pastas de Configuração de Frameworks
        "includes",
        "inc",
        "src",
        "lib",
        "library",
        "vendor",
        "node_modules",
        "system",
        "core",
        "bin",
        "etc",
        "var",
        "tmp",
        # Pastas de Admin e Auth (Onde o 403 é comum)
        "admin/auth",
        "admin/config",
        "admin/db",
        "private",
        "secret",
        "secure",
        "restricted",
        "auth",
        "users",
        "accounts",
        # Arquivos de Setup e DB
        "setup.php",
        "install.php",
        "phpinfo.php",
        "info.php",
        "status.php",
        "mysql",
        "sql",
        "db_backup",
        "dump.sql",
        "database.sql",
    ]
    current_wordlist = default_wordlist.copy()
    found_results = []
    collected_results = {}
    stop_event = threading.Event()

    # --- FUNÇÕES DE LÓGICA ---

    # Configuração de spoofing de headers para parecer um navegador real (evitar bloqueios básicos)
    browser_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
    }

    def open_link(e, link_url):
        webbrowser.open(link_url)

    # Função que lê o arquivo selecionado
    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            try:
                with open(file_path, "r") as f:
                    # Lê linhas, remove espaços e ignora linhas vazias
                    new_list = [line.strip() for line in f.readlines() if line.strip()]
                    current_wordlist.clear()
                    current_wordlist.extend(new_list)

                wordlist_status.value = (
                    f"✅ Wordlist carregada: {len(current_wordlist)} itens"
                )
                wordlist_status.color = ft.Colors.GREEN_400
            except Exception as ex:
                wordlist_status.value = f"❌ Erro ao ler arquivo: {ex}"
                wordlist_status.color = ft.Colors.RED_400
            page.update()

    def generate_pdf_report(e):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(
                200,
                10,
                "Relatório de Reconhecimento Web - LazRecon",
                ln=True,
                align="C",
            )
            pdf.ln(8)
            # Agrupar por alvo. Use collected_results se houver, senão use found_results atual
            groups = (
                collected_results
                if len(collected_results) > 0
                else {url_input.value: found_results}
            )

            for alvo, items in groups.items():
                # Alvo
                pdf.set_font("Arial", "B", 12)
                pdf.cell(25, 8, "Alvo:", ln=0)
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 8, f"{alvo}", ln=1)
                pdf.ln(3)

                # Itens do alvo
                for item in items:
                    status = item.get("status", "")
                    url = item.get("url", "")

                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(22, 7, "Status:", ln=0)

                    if status == 200 or str(status) == "200":
                        pdf.set_text_color(0, 100, 0)
                    elif status == 403 or str(status) == "403":
                        pdf.set_text_color(200, 0, 0)
                    else:
                        pdf.set_text_color(0, 0, 0)

                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(18, 7, str(status), ln=0)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Arial", "", 12)
                    pdf.cell(0, 7, f"  - {url}", ln=1)

                pdf.ln(4)

            # Garantir que a pasta exports exista e salvar o PDF lá
            exports_dir = os.path.abspath("exports")
            os.makedirs(exports_dir, exist_ok=True)
            out_path = os.path.join(exports_dir, "relatorio_fuzzer.pdf")
            pdf.output(out_path)
            try:
                # Tenta abrir automaticamente no Windows
                os.startfile(out_path)
            except Exception:
                # Fallback: abrir via browser
                webbrowser.open("file://" + out_path)
            page.snack_bar = ft.SnackBar(ft.Text(f"PDF gerado: {out_path}"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            print(f"Erro ao gerar PDF: {ex}")

    def restore_default_wordlist(e):
        progress_refresh.visible = True
        btn_reset_wordlist.disabled = True
        page.update()

        def do_restore():
            import time

            time.sleep(0.6)
            current_wordlist.clear()
            current_wordlist.extend(default_wordlist)
            wordlist_status.value = (
                f"🔁 Wordlist padrão restaurada: {len(current_wordlist)} itens"
            )
            wordlist_status.color = ft.Colors.GREY_500
            progress_refresh.visible = False
            btn_reset_wordlist.disabled = False
            page.update()

        threading.Thread(target=do_restore, daemon=True).start()

    # Instância do seletor de arquivos
    file_picker = ft.FilePicker(on_result=on_file_result)
    page.overlay.append(file_picker)  # Essencial para funcionar no Flet

    # --- COMPONENTES DA INTERFACE ---

    url_input = ft.TextField(
        label="URL Alvo",
        hint_text="http://exemplo.com/",
        expand=True,
        on_submit=lambda _: start_scan(None),
    )

    wordlist_status = ft.Text(
        "Usando wordlist padrão", color=ft.Colors.GREY_500, size=12
    )

    btn_file = ft.IconButton(
        icon=ft.Icons.FILE_OPEN,
        tooltip="Carregar Wordlist (.txt)",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False, allowed_extensions=["txt"]
        ),
    )

    btn_reset_wordlist = ft.IconButton(
        icon=ft.Icons.REFRESH,
        tooltip="Restaurar wordlist padrão",
        on_click=restore_default_wordlist,
    )

    progress_refresh = ft.ProgressRing(visible=False, width=20, height=20)

    results_list = ft.ListView(expand=True, spacing=10, padding=10)
    progress_bar = ft.ProgressBar(width=None, color=ft.Colors.BLUE, visible=False)
    status_text = ft.Text("Pronto para iniciar", color=ft.Colors.GREY_400)
    counter_text = ft.Text("0/0", color=ft.Colors.BLUE_200, weight=ft.FontWeight.BOLD)

    def stop_scan(e):
        stop_event.set()
        status_text.value = "Parando..."
        page.update()

    def start_scan(e):
        target = url_input.value.strip().rstrip("/")
        # limpar erro anterior ao validar
        url_input.error_text = None
        if not target or not target.startswith("http"):
            url_input.error_text = "Insira uma URL válida."
            page.update()
            return
        # Remover duplicatas na wordlist, preservando ordem
        current_wordlist[:] = list(dict.fromkeys(current_wordlist))

        # Limpar resultados anteriores para não misturar alvos
        found_results.clear()

        # Criar pasta de achados para este alvo (findigns/<host>_YYYYMMDD_HHMMSS/html)
        # Extrair hostname sem porta (ex: 44.227.89.148 ao invés de 44.227.89.148:8220)
        parsed = urlparse(target)
        if parsed.hostname:
            target_host = parsed.hostname
        else:
            # fallback robusto caso parsing falhe
            target_host = target.split("://")[-1].split("/")[0].split(":")[0]
        # sanitizar nome do host para ser um nome de pasta válido no Windows
        target_host = re.sub(r"[^0-9A-Za-z._-]", "_", target_host)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        target_folder = os.path.join("findigns", f"{target_host}_{ts}", "html")
        os.makedirs(target_folder, exist_ok=True)

        results_list.controls.clear()
        progress_bar.visible = True
        stop_event.clear()
        status_text.value = "Buscando..."
        counter_text.value = f"0/{len(current_wordlist)}"
        btn_scan.disabled = True
        btn_stop.disabled = False
        page.update()

        def scan_logic():
            total = len(current_wordlist)
            seen_urls = set()
            for i, path in enumerate(current_wordlist, 1):
                full_url = f"{target}/{path}"
                counter_text.value = f"{i}/{total}"
                if stop_event.is_set():
                    break
                try:
                    res = requests.get(
                        full_url,
                        timeout=3,
                        allow_redirects=False,
                        headers=browser_headers,
                    )

                    if res.status_code == 200:
                        if full_url not in seen_urls:
                            results_list.controls.insert(
                                0,
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN
                                    ),
                                    title=ft.Text(
                                        f"/{path}", weight=ft.FontWeight.BOLD
                                    ),
                                    subtitle=ft.Row(
                                        [
                                            ft.Text(
                                                "Status 200", color=ft.Colors.GREEN_100
                                            ),
                                            ft.TextButton(
                                                content=ft.Text("Abrir"),
                                                on_click=lambda e, url=full_url: (
                                                    open_link(e, url)
                                                ),
                                            ),
                                        ],
                                        spacing=12,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(
                                        0.05, ft.Colors.GREEN
                                    ),
                                ),
                            )
                            found_results.append(
                                {"status": res.status_code, "url": full_url}
                            )
                            # salvar resposta HTML para este alvo
                            try:
                                safe_name = path.strip("/").replace("/", "_") or "root"
                                fname = f"{res.status_code}_{safe_name}_{datetime.datetime.now().strftime('%H%M%S')}.html"
                                with open(
                                    os.path.join(target_folder, fname),
                                    "w",
                                    encoding="utf-8",
                                ) as fh:
                                    fh.write(res.text)
                            except Exception:
                                pass
                            seen_urls.add(full_url)

                    elif res.status_code == 403:
                        if full_url not in seen_urls:
                            results_list.controls.insert(
                                0,
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.SECURITY, color=ft.Colors.ORANGE
                                    ),
                                    title=ft.Text(
                                        f"PROTEGIDO: /{path}", weight=ft.FontWeight.BOLD
                                    ),
                                    subtitle=ft.Row(
                                        [
                                            ft.Text(
                                                "Status 403", color=ft.Colors.ORANGE_100
                                            ),
                                            ft.TextButton(
                                                content=ft.Text("Abrir"),
                                                on_click=lambda e, url=full_url: (
                                                    open_link(e, url)
                                                ),
                                            ),
                                        ],
                                        spacing=12,
                                    ),
                                ),
                            )
                            found_results.append(
                                {"status": res.status_code, "url": full_url}
                            )
                            # salvar resposta HTML para este alvo
                            try:
                                safe_name = path.strip("/").replace("/", "_") or "root"
                                fname = f"{res.status_code}_{safe_name}_{datetime.datetime.now().strftime('%H%M%S')}.html"
                                with open(
                                    os.path.join(target_folder, fname),
                                    "w",
                                    encoding="utf-8",
                                ) as fh:
                                    fh.write(res.text)
                            except Exception:
                                pass
                            seen_urls.add(full_url)

                    page.update()
                except Exception:
                    continue

            if stop_event.is_set():
                status_text.value = "Busca interrompida pelo usuário"
            else:
                if len(results_list.controls) == 0:
                    # Mostrar mensagem dentro da área de resultados
                    results_list.controls.append(
                        ft.ListTile(
                            title=ft.Text("Nada encontrado", color=ft.Colors.GREY_500)
                        )
                    )
                    status_text.value = "Busca finalizada!"
                else:
                    status_text.value = "Busca finalizada!"
            # Armazenar achados deste scan por alvo, evitando duplicatas
            if len(found_results) > 0:
                collected_results.setdefault(target, [])
                for r in found_results:
                    if not any(
                        x.get("url") == r.get("url") for x in collected_results[target]
                    ):
                        collected_results[target].append(r)
            # Mostrar botão de PDF apenas se houver resultados (no scan atual ou coletados previamente)
            any_collected = (
                any(len(v) > 0 for v in collected_results.values())
                if len(collected_results) > 0
                else False
            )
            btn_pdf.visible = (len(found_results) > 0) or any_collected
            progress_bar.visible = False
            btn_scan.disabled = False
            btn_stop.disabled = True
            page.update()

        threading.Thread(target=scan_logic, daemon=True).start()

    btn_scan = ft.ElevatedButton(
        "Iniciar Scan", icon=ft.Icons.SEARCH, on_click=start_scan
    )

    btn_stop = ft.ElevatedButton(
        "Parar", icon=ft.Icons.STOP, on_click=stop_scan, disabled=True
    )

    btn_pdf = ft.ElevatedButton(
        "Gerar Relatório",
        icon=ft.Icons.PICTURE_AS_PDF,
        on_click=generate_pdf_report,
        visible=False,
    )

    # --- LAYOUT ---
    page.add(
        ft.Row(
            [
                ft.Image(
                    src=header_image_src, width=36, height=36, fit=ft.ImageFit.CONTAIN
                ),
                ft.Text("LazRecon", size=25, weight="bold"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Divider(),
        ft.Row(
            [
                url_input,
                btn_file,
                btn_reset_wordlist,
                progress_refresh,
                btn_scan,
                btn_stop,
            ]
        ),
        ft.Row([wordlist_status], alignment=ft.MainAxisAlignment.START),
        progress_bar,
        ft.Row(
            [status_text, counter_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        ft.Container(
            content=results_list,
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_700),
            border_radius=10,
            bgcolor=ft.Colors.BLACK12,
        ),
        ft.Row([btn_pdf], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            [
                ft.Row(
                    controls=[
                        ft.Text(
                            "⚠️ Use com responsabilidade em sistemas autorizados.",  # Aviso de uso responsável
                            size=11,
                            color=ft.Colors.BLUE_GREY_200,
                        ),
                        ft.TextButton(
                            content=ft.Text(
                                "Saiba Mais © 2026",
                                size=11,
                                color=ft.Colors.BLUE_GREY_200,
                            ),
                            on_click=lambda _: page.launch_url(
                                "https://github.com/lazsilvadev/lazrecon"
                            ),  # Link para o repositório do projeto
                            style=ft.ButtonStyle(
                                padding=0
                            ),  # Remove o espaço extra do botão
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
