import flet as ft
import threading
import webbrowser
import os
import datetime
import re
import time 
from src import core
from src import report
from src import resources
from src import wordlist
from src import utils 
from src import translations 

# Imports específicos para wordlist
from src.wordlist import DEFAULT_WORDLIST, load_wordlist

def build_ui(page: ft.Page, lang):
    page.controls.clear()
    
    # --- Configurações da Janela ---
    page.title = lang.get("app_title", "LazRecon v1.2")
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 720 
    page.window.height = 920 
    page.window.resizable = False
    page.window.maximizable = False

    # --- Estado da Aplicação ---
    current_wordlist = DEFAULT_WORDLIST.copy()
    found_results = []
    collected_results = {}
    stop_event = threading.Event()
    header_image_src = "/lazrecon.png"

    # Função auxiliar para pegar o idioma atual dinamicamente
    def get_current_lang():
        selected = page.client_storage.get("user_lang")
        if not selected:
            return lang
        from src.translations import languages
        return languages.get(selected, lang)

    # =================================================================
    # 1. DEFINIÇÃO DE VARIÁVEIS
    # =================================================================
    options_title_text = ft.Text(lang["options_title"], size=14, color=ft.Colors.GREY_200)
    threads_label_text = ft.Text(lang["threads_label"], size=11)
    delay_title_text = ft.Text(lang["delay_label"], size=11)
    workspace_label_text = ft.Text(lang["workspace_label"], size=10, color=ft.Colors.GREY_500, weight="bold")
    repo_button_text = ft.Text(lang["repo_button"], size=11)
    status_text = ft.Text(lang["status_ready"], color=ft.Colors.GREY_400)
    wordlist_status = ft.Text(lang["wordlist_default"], color=ft.Colors.GREY_500, size=12)
    counter_text = ft.Text("0/0", color=ft.Colors.BLUE_200, weight=ft.FontWeight.BOLD)
    speed_label = ft.Text(lang["speed_balanced"], color=ft.Colors.BLUE_200, size=11, weight="bold")
    delay_label = ft.Text("0ms", color=ft.Colors.WHITE, size=11, weight="bold")
    
    bypass_info_icon = ft.Icon(name=ft.Icons.INFO_OUTLINE, color=ft.Colors.BLUE_200, size=18, tooltip=lang["bypass_tooltip"])
    waf_status_icon = ft.Icon(name=ft.Icons.VPN_KEY_OUTLINED, color=ft.Colors.GREY_500, size=18, tooltip=lang["waf_waiting"])
    
    btn_clear_findings = ft.IconButton(
        icon=ft.Icons.DELETE_SWEEP_ROUNDED, icon_size=18, icon_color=ft.Colors.GREY_500,
        tooltip=lang["tooltip_clear_findings"], scale=1.0, animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT)
    )
    
    btn_explore = ft.IconButton(icon=ft.Icons.FOLDER_OPEN_ROUNDED, icon_size=16, icon_color=ft.Colors.GREY_500, tooltip=lang["tooltip_explore"])
    btn_file = ft.IconButton(icon=ft.Icons.FILE_OPEN, tooltip=lang["tooltip_load_wl"])
    btn_reset_wordlist = ft.IconButton(icon=ft.Icons.REFRESH, tooltip=lang["tooltip_reset_wl"])

    progress_refresh = ft.ProgressRing(visible=False, width=20, height=20)
    results_list = ft.ListView(expand=True, spacing=10, padding=10)
    progress_bar = ft.ProgressBar(width=None, color=ft.Colors.BLUE, visible=False)

    custom_headers_input = ft.TextField(
        label=lang["headers_label"], hint_text=lang["headers_hint"], multiline=True,
        min_lines=2, max_lines=4, text_size=12, border_color=ft.Colors.TRANSPARENT, 
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY_500), focused_border_color=ft.Colors.BLUE_200,
        focused_border_width=2, label_style=ft.TextStyle(color=ft.Colors.GREY_500), prefix_icon=ft.Icons.SECURITY_ROUNDED
    )
    
    url_input = ft.TextField(label=lang["target_label"], hint_text=lang["target_hint"], expand=True, focused_border_color=ft.Colors.BLUE_200)
    
    method_dropdown = ft.Dropdown(
        label=lang["method_label"], value="GET", width=160, border_color=ft.Colors.BLUE_200,
        options=[ft.dropdown.Option("GET"), ft.dropdown.Option("POST"), ft.dropdown.Option("HEAD"), ft.dropdown.Option("OPTIONS"), ft.dropdown.Option("PUT")]
    )
    
    bypass_slashes_check = ft.Checkbox(label=lang["bypass_label"], value=False, label_style=ft.TextStyle(size=12, color=ft.Colors.GREY_400))
    
    btn_scan = ft.ElevatedButton(lang["btn_start"], icon=ft.Icons.SEARCH)
    btn_stop = ft.ElevatedButton(lang["btn_stop"], icon=ft.Icons.STOP, disabled=True)
    btn_pdf = ft.ElevatedButton(lang["btn_report"], icon=ft.Icons.PICTURE_AS_PDF, visible=False)
    
    speed_slider = ft.Slider(min=1, max=500, divisions=50, value=15, label="{value}")
    delay_slider = ft.Slider(min=0, max=1000, divisions=20, value=0, label="{value}ms")

    # =================================================================
    # 2. LÓGICA DE INTERNACIONALIZAÇÃO
    # =================================================================
    def change_language(e):
        selected_lang = e.control.data 
        page.client_storage.set("user_lang", selected_lang)
        
        from src.translations import languages
        new_lang = languages[selected_lang]
        
        try:
            translations.LANG = selected_lang
        except: pass

        # Atualização dos textos estáticos
        page.title = new_lang.get("app_title", "LazRecon")
        options_title_text.value = new_lang["options_title"]
        threads_label_text.value = new_lang["threads_label"]
        delay_title_text.value = new_lang["delay_label"]
        workspace_label_text.value = new_lang["workspace_label"]
        repo_button_text.value = new_lang["repo_button"]
        
        # --- ATUALIZAÇÃO DO STATUS ---
        status_ready_options = [l.get("status_ready") for l in languages.values()]
        status_finished_options = [l.get("status_finished") for l in languages.values()]
        status_stopping_options = [l.get("status_stopping") for l in languages.values()]

        if status_text.value in status_ready_options:
            status_text.value = new_lang["status_ready"]
        elif status_text.value in status_finished_options:
            status_text.value = new_lang["status_finished"]
        elif status_text.value in status_stopping_options:
            status_text.value = new_lang["status_stopping"]

        # --- ATUALIZAÇÃO DOS RESULTADOS JÁ NA TELA ---
        open_options = [l.get("btn_open", "Open") for l in languages.values()]
        for control in results_list.controls:
            if isinstance(control, ft.ListTile) and control.subtitle:
                subtitle_row = control.subtitle
                if len(subtitle_row.controls) > 1:
                    btn_open = subtitle_row.controls[1]
                    if isinstance(btn_open, ft.TextButton) and btn_open.text in open_options:
                        btn_open.text = new_lang.get("btn_open", "Open")

        # --- ATUALIZAÇÃO DO WAF ---
        waf_waiting_options = [l.get("waf_waiting") for l in languages.values()]
        waf_none_options = [l.get("waf_none") for l in languages.values()]

        if waf_status_icon.tooltip in waf_waiting_options:
            waf_status_icon.tooltip = new_lang["waf_waiting"]
        elif waf_status_icon.tooltip in waf_none_options:
            waf_status_icon.tooltip = new_lang["waf_none"]

        if len(current_wordlist) == len(DEFAULT_WORDLIST):
            wordlist_status.value = new_lang["wordlist_default"]
        else:
            wordlist_status.value = new_lang["wordlist_loaded"].format(count=len(current_wordlist))
            
        url_input.label = new_lang["target_label"]
        url_input.hint_text = new_lang["target_hint"]
        custom_headers_input.label = new_lang["headers_label"]
        custom_headers_input.hint_text = new_lang["headers_hint"]
        method_dropdown.label = new_lang["method_label"]
        bypass_slashes_check.label = new_lang["bypass_label"]
        bypass_info_icon.tooltip = new_lang["bypass_tooltip"]
        
        btn_scan.text = new_lang["btn_start"]
        btn_stop.text = new_lang["btn_stop"]
        btn_pdf.text = new_lang["btn_report"]
        
        btn_file.tooltip = new_lang["tooltip_load_wl"]
        btn_reset_wordlist.tooltip = new_lang["tooltip_reset_wl"]
        btn_explore.tooltip = new_lang["tooltip_explore"]
        btn_clear_findings.tooltip = new_lang["tooltip_clear_findings"]
        
        on_speed_change(ft.ControlEvent(target="", name="", data=str(speed_slider.value), control=speed_slider, page=page))

        for item in btn_change_lang.items:
            item.checked = (item.data == selected_lang)

        page.update()

    btn_change_lang = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="English", data="en", on_click=change_language),
            ft.PopupMenuItem(text="Português (BR)", data="pt", on_click=change_language),
        ],
        icon=ft.Icons.LANGUAGE_ROUNDED, icon_size=20, icon_color=ft.Colors.GREY_500, tooltip="Language"
    )

    # =================================================================
    # 3. HANDLERS E FUNÇÕES
    # =================================================================
    def on_headers_focus(e):
        e.control.label_style = ft.TextStyle(color=ft.Colors.BLUE_200)
        e.control.update()

    def on_headers_blur(e):
        e.control.label_style = ft.TextStyle(color=ft.Colors.GREY_700)
        e.control.update()

    def handle_clear_findings(e):
        findings_dir = "findings"
        def run_animation(success=True):
            if success:
                btn_clear_findings.icon = ft.Icons.DELETE_OUTLINE
                btn_clear_findings.icon_color = ft.Colors.RED_400
                btn_clear_findings.scale = 1.6
                btn_clear_findings.update()
                time.sleep(0.5) 
                btn_clear_findings.icon = ft.Icons.CLEANING_SERVICES_ROUNDED
                btn_clear_findings.icon_color = ft.Colors.GREEN_400
                btn_clear_findings.scale = 1.0
                btn_clear_findings.update()
            else:
                btn_clear_findings.icon_color = ft.Colors.AMBER_400
                btn_clear_findings.update()
                time.sleep(0.3)
                btn_clear_findings.icon_color = ft.Colors.GREY_500
                btn_clear_findings.update()
            time.sleep(0.8)
            btn_clear_findings.icon = ft.Icons.DELETE_SWEEP_ROUNDED
            btn_clear_findings.icon_color = ft.Colors.GREY_500
            btn_clear_findings.update()

        if os.path.exists(findings_dir) and any(os.scandir(findings_dir)):
            utils.clear_findings() 
            threading.Thread(target=lambda: run_animation(True), daemon=True).start()
        else:
            threading.Thread(target=lambda: run_animation(False), daemon=True).start()

    def on_speed_change(e):
        val = int(e.control.value)
        cur_lang = get_current_lang()
        if val <= 30:
            speed_label.value = cur_lang["speed_stealth"]; speed_label.color = ft.Colors.GREEN_400
        elif val <= 100:
            speed_label.value = cur_lang["speed_balanced"]; speed_label.color = ft.Colors.BLUE_200
        elif val <= 350:
            speed_label.value = cur_lang["speed_turbo"]; speed_label.color = ft.Colors.ORANGE_500
        else:
            speed_label.value = cur_lang["speed_insane"]; speed_label.color = ft.Colors.RED_ACCENT_400
        page.update()

    def on_delay_change(e):
        delay_label.value = f"{int(e.control.value)}ms"
        page.update()

    def toggle_headers_size(e):
        custom_headers_input.max_lines = 15 if custom_headers_input.max_lines == 4 else 4
        e.control.icon = ft.Icons.COMPRESS if custom_headers_input.max_lines == 15 else ft.Icons.EXPAND
        page.update()

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            cur_lang = get_current_lang()
            try:
                new_list = load_wordlist(file_path)
                current_wordlist.clear()
                current_wordlist.extend(new_list)
                wordlist_status.value = cur_lang["wordlist_loaded"].format(count=len(current_wordlist))
                wordlist_status.color = ft.Colors.GREEN_400
            except Exception as ex:
                wordlist_status.value = cur_lang["wordlist_error"].format(error=ex)
                wordlist_status.color = ft.Colors.RED_400
            page.update()

    def generate_pdf_report(e):
        try:
            cur_lang = get_current_lang() 
            current_url = url_input.value.strip()
            
            # Limpeza do alvo e Timestamp para o nome do arquivo
            clean_target = re.sub(r'https?://', '', current_url).replace('/', '_').replace(':', '')
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"LazRecon_Report_{clean_target}_{timestamp}.pdf"
            
            groups = collected_results if len(collected_results) > 0 else {current_url: found_results}
            exports_dir = os.path.abspath("exports")
            os.makedirs(exports_dir, exist_ok=True)
            
            # Caminho final do arquivo
            out_path = os.path.join(exports_dir, filename)
            
            # Gera o PDF
            report.save_pdf(groups, out_path, cur_lang) 
            
            try:
                os.startfile(out_path)
            except Exception:
                webbrowser.open("file://" + out_path)
                
            page.snack_bar = ft.SnackBar(ft.Text(cur_lang["snack_report"].format(path=filename)))
            page.snack_bar.open = True
            page.update()
        except Exception as ex: 
            print(f"Error Report: {ex}")

    def restore_default_wordlist(e):
        progress_refresh.visible = True
        btn_reset_wordlist.disabled = True
        page.update()
        def do_restore():
            time.sleep(0.6)
            cur_lang = get_current_lang()
            current_wordlist.clear()
            current_wordlist.extend(DEFAULT_WORDLIST)
            wordlist_status.value = cur_lang["wordlist_restored"].format(count=len(current_wordlist))
            wordlist_status.color = ft.Colors.GREY_500
            progress_refresh.visible = False
            btn_reset_wordlist.disabled = False
            page.update()
        threading.Thread(target=do_restore, daemon=True).start()

    def stop_scan(e):
        stop_event.set()
        status_text.value = get_current_lang()["status_stopping"]
        page.update()

    def start_scan(e):
        cur_lang = get_current_lang()
        raw_input = url_input.value.strip()
        if not bypass_slashes_check.value:
            raw_input = re.sub(r'(?<!:)/+', '/', raw_input)
        if not raw_input:
            url_input.error_text = cur_lang["error_no_target"]; page.update(); return
        
        target_for_check = raw_input if raw_input.startswith("http") else "http://" + raw_input
        status_text.value = cur_lang["status_checking"]; status_text.color = ft.Colors.BLUE_400
        url_input.error_text = None; page.update()

        if not utils.is_host_alive(target_for_check):
            url_input.error_text = cur_lang["error_unreachable"]
            status_text.value = cur_lang["error_no_response"]; status_text.color = ft.Colors.RED_ACCENT
            page.update(); return 

        waf_status_icon.color = ft.Colors.AMBER_500
        waf_status_icon.tooltip = cur_lang["waf_probing"]; page.update()
        detected_waf = utils.detect_waf(target_for_check)
        if detected_waf:
            waf_status_icon.name = ft.Icons.VPN_KEY_ROUNDED
            waf_status_icon.color = ft.Colors.CYAN_400 if "Cloudflare" in detected_waf else ft.Colors.RED_500
            waf_status_icon.tooltip = cur_lang["waf_detected"].format(name=detected_waf)
        else:
            waf_status_icon.name = ft.Icons.VPN_KEY_OUTLINED; waf_status_icon.color = ft.Colors.GREY_600; waf_status_icon.tooltip = cur_lang["waf_none"]
        
        user_headers = {}
        if custom_headers_input.value:
            for line in custom_headers_input.value.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    user_headers[key.strip()] = value.strip()
        
        ui_refresh_counter = 0
        def _on_progress(i, total):
            nonlocal ui_refresh_counter
            counter_text.value = f"{i}/{total}"
            ui_refresh_counter += 1
            if ui_refresh_counter % 10 == 0 or i == total: page.update()

        def _on_found(status, full_url, res_text):
            f_lang = get_current_lang()
            btn_open_text = f_lang.get("btn_open", "Open")
            
            match = re.search(r'https?://[^/]+(/.*)', full_url)
            display_path = (match.group(1) if match else full_url) if bypass_slashes_check.value else "/" + (match.group(1) if match else full_url).lstrip("/").replace("//", "/")
            icon, color = (ft.Icons.CHECK_CIRCLE, ft.Colors.GREEN) if status == 200 else (ft.Icons.REDO_ROUNDED, ft.Colors.BLUE_300) if 300 <= status < 400 else (ft.Icons.LOCK, ft.Colors.ORANGE_700)
            
            results_list.controls.insert(0, ft.ListTile(
                leading=ft.Icon(icon, color=color), 
                title=ft.Text(display_path, weight="bold", selectable=True), 
                subtitle=ft.Row([
                    ft.Text(f"Status {status} [{method_dropdown.value}]", color=ft.Colors.with_opacity(0.8, color)), 
                    ft.TextButton(btn_open_text, on_click=lambda e, u=full_url: webbrowser.open(u))
                ], spacing=12), 
                bgcolor=ft.Colors.with_opacity(0.05, color)
            ))
            found_results.append({"status": status, "url": full_url}); page.update()

        def _on_finished(interrupted):
            f_lang = get_current_lang()
            status_text.value = f_lang["status_interrupted"] if interrupted else f_lang["status_finished"]
            if found_results:
                collected_results.setdefault(target_for_check, [])
                for r in found_results:
                    if not any(x.get("url") == r.get("url") for x in collected_results[target_for_check]): 
                        collected_results[target_for_check].append(r)
            btn_pdf.visible = len(found_results) > 0 or len(collected_results) > 0
            progress_bar.visible = False; btn_scan.disabled = False; btn_stop.disabled = True; page.update()

        target_folder = os.path.abspath(os.path.join("findings", f"{utils.get_safe_folder_name(raw_input)}_{datetime.datetime.now().strftime('%H%M%S')}"))
        os.makedirs(target_folder, exist_ok=True)
        found_results.clear(); results_list.controls.clear(); progress_bar.visible = True; stop_event.clear(); btn_scan.disabled = True; btn_stop.disabled = False; page.update()

        threading.Thread(target=lambda: core.start_scan_engine(target_for_check, current_wordlist, user_headers, stop_event, _on_found, _on_progress, _on_finished, save_html_dir=target_folder, 
        concurrency=int(speed_slider.value), http_method=method_dropdown.value, delay=int(delay_slider.value)), daemon=True).start()

    # =================================================================
    # 4. BINDINGS
    # =================================================================
    custom_headers_input.on_focus = on_headers_focus
    custom_headers_input.on_blur = on_headers_blur
    custom_headers_input.suffix = ft.IconButton(icon=ft.Icons.EXPAND, icon_color=ft.Colors.BLUE_200, icon_size=18, on_click=toggle_headers_size)

    btn_clear_findings.on_click = handle_clear_findings
    speed_slider.on_change = on_speed_change
    delay_slider.on_change = on_delay_change
    
    file_picker = ft.FilePicker(on_result=on_file_result)
    page.overlay.append(file_picker)
    
    btn_file.on_click = lambda _: file_picker.pick_files(allowed_extensions=["txt"])
    btn_reset_wordlist.on_click = restore_default_wordlist
    btn_pdf.on_click = generate_pdf_report
    btn_stop.on_click = stop_scan
    btn_scan.on_click = start_scan
    url_input.on_submit = lambda _: start_scan(None)
    btn_explore.on_click = lambda _: utils.open_findings_folder()

    # =================================================================
    # 5. MONTAGEM DO LAYOUT
    # =================================================================
    page.add(
        ft.Row([
            ft.Container(expand=1),
            ft.Row([
                ft.Image(src=header_image_src, width=32), 
                ft.Text("LazRecon", size=25, weight="bold")
            ], expand=2, alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(btn_change_lang, expand=1, alignment=ft.alignment.center_right),
        ]),
        
        ft.Divider(),
        
        ft.Container(content=ft.Row([url_input, btn_file, btn_reset_wordlist, progress_refresh, waf_status_icon, btn_scan, btn_stop], spacing=10), padding=ft.padding.only(left=20, right=20)),
        
        ft.ExpansionTile(
            title=options_title_text,
            controls=[
                ft.Container(padding=ft.padding.only(top=15, bottom=15, left=20, right=20), content=ft.Column([
                    ft.Row([
                        method_dropdown, 
                        ft.Container(content=ft.Column([
                            ft.Row([threads_label_text, speed_label], spacing=5), 
                            speed_slider, 
                            ft.Row([delay_title_text, delay_label], spacing=5), 
                            delay_slider
                        ], spacing=0), padding=ft.padding.only(left=20), expand=True)
                    ]), 
                    ft.Container(height=10), 
                    ft.Row([bypass_slashes_check, bypass_info_icon], spacing=5), 
                    ft.Container(height=15), 
                    custom_headers_input
                ]))
            ]
        ),
        
        ft.Container(content=ft.Column([wordlist_status, progress_bar, ft.Row([status_text, counter_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)]), padding=ft.padding.only(left=20, right=20)),
        
        ft.Container(content=results_list, expand=True, border=ft.border.all(1, ft.Colors.GREY_700), border_radius=10, margin=ft.margin.only(left=20, right=20, bottom=10)),
        
        ft.Row([btn_pdf], alignment=ft.MainAxisAlignment.CENTER),
        
        ft.Container(
            padding=ft.padding.only(left=20, right=20, bottom=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row([
                        workspace_label_text,
                        btn_explore,
                        ft.VerticalDivider(width=5, color=ft.Colors.GREY_800),
                        btn_clear_findings,
                    ], spacing=0),
                    ft.Row([
                        ft.Text("LazRecon © 2026", size=10, color=ft.Colors.BLUE_200, weight="bold"), 
                        ft.Text("|", size=11, color=ft.Colors.GREY_700), 
                        ft.TextButton(content=repo_button_text, on_click=lambda _: page.launch_url("https://github.com/lazsilvadev/lazrecon"))
                    ], spacing=10)
                ]
            )
        )
    )
