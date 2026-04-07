# =================================================================
# LAZRECON v1.2 - TRANSLATIONS (i18n)
# =================================================================

languages = {
    "en": {
        "app_title": "LazRecon v1.2 - Web Path Reconnaissance Tool",
        "target_label": "Target URL",
        "target_hint": "example.com",
        "btn_start": "Start Scan",
        "btn_stop": "Stop",
        "method_label": "Method",
        "btn_report": "Generate Report",
        "waf_waiting": "Defense Status: Waiting for target",
        "waf_probing": "Probing target defenses...",
        "waf_none": "No obvious WAF detected.",
        "waf_detected": "WAF DETECTED: {name}\nAdjust Threads/Delay to avoid ban.",
        "status_ready": "Ready to start",
        "status_checking": "🔍 Checking connectivity...",
        "status_starting": "🚀 Target online! Starting...",
        "status_stopping": "Stopping...",
        "status_finished": "Finished!",
        "status_interrupted": "Stopped!",
        "error_no_target": "Please enter a target.",
        "error_invalid_url": "Invalid URL or Domain (ex: google.com)",
        "error_unreachable": "Target unreachable or DNS non-existent.",
        "error_no_response": "❌ Error: Host did not respond.",
        "wordlist_default": "Using default wordlist",
        "wordlist_loaded": "✅ Wordlist loaded: {count} items",
        "wordlist_error": "❌ Error reading file: {error}",
        "wordlist_restored": "🔁 Default wordlist restored: {count} items",
        "tooltip_load_wl": "Load Wordlist",
        "tooltip_reset_wl": "Restore Default Wordlist",
        "tooltip_clear_findings": "Clear findings",
        "tooltip_explore": "Explore findings",
        "options_title": "Bypass & Performance Options",
        "threads_label": "Threads:",
        "delay_label": "Delay (Throttling):",
        "bypass_label": "Preserve extra slashes (Bypass)",
        "bypass_tooltip": "With Bypass active, type extra slashes directly in the URL above.",
        "headers_label": "Custom Headers",
        "headers_hint": "Ex: Cookie: session=123\nReferer: https://google.com",
        "workspace_label": "Workspace:",
        "repo_button": "Official GitHub Repository",
        "speed_stealth": "Stealth (Silent)",
        "speed_balanced": "Balanced",
        "speed_turbo": "Turbo (Aggressive)",
        "speed_insane": "🔥 INSANE MODE",
        "btn_open": "Open",
        "snack_report": "Reports generated at: {path}",
    
        # --- PDF REPORT KEYS (EN) ---
        "pdf_title": "Reconnaissance Report - LazRecon",
        "pdf_continuation": "LazRecon - Report Continuation",
        "pdf_page": "Page",
        "pdf_target": "Target",
        "pdf_scanned_at": "Scanned at",
        "pdf_severity": "Severity",
        "pdf_url_found": "URL Found",
        "pdf_sev_crit": "CRITICAL",
        "pdf_sev_med": "MEDIUM"
    },
    "pt": {
        "app_title": "LazRecon v1.2 - Ferramenta de Reconhecimento Web Path",
        "target_label": "URL Alvo",
        "target_hint": "exemplo.com",
        "btn_start": "Iniciar Scan",
        "btn_stop": "Parar",
        "method_label": "Método",
        "btn_report": "Gerar Relatório",
        "waf_waiting": "Status de Defesa: Aguardando alvo",
        "waf_probing": "Sondando defesas do alvo...",
        "waf_none": "Nenhum WAF óbvio detectado.",
        "waf_detected": "WAF DETECTADO: {name}\nAjuste Threads/Delay para evitar banimento.",
        "status_ready": "Pronto para começar",
        "status_checking": "🔍 Verificando conectividade...",
        "status_starting": "🚀 Alvo online! Iniciando...",
        "status_stopping": "Parando...",
        "status_finished": "Finalizado!",
        "status_interrupted": "Interrompido!",
        "error_no_target": "Por favor, insira um alvo.",
        "error_invalid_url": "URL ou Domínio inválido (ex: google.com)",
        "error_unreachable": "Alvo inalcançável ou DNS inexistente.",
        "error_no_response": "❌ Erro: O host não respondeu.",
        "wordlist_default": "Usando wordlist padrão",
        "wordlist_loaded": "✅ Wordlist carregada: {count} itens",
        "wordlist_error": "❌ Erro ao ler arquivo: {error}",
        "wordlist_restored": "🔁 Wordlist padrão restaurada: {count} itens",
        "tooltip_load_wl": "Carregar Wordlist",
        "tooltip_reset_wl": "Restaurar Wordlist Padrão",
        "tooltip_clear_findings": "Limpar resultados",
        "tooltip_explore": "Explorar resultados",
        "options_title": "Opções de Bypass e Performance",
        "threads_label": "Threads:",
        "delay_label": "Delay (Atraso):",
        "bypass_label": "Preservar barra extra (Bypass)",
        "bypass_tooltip": "Com o Bypass ativo, digite as barras extras diretamente na URL acima.",
        "headers_label": "Headers Customizados",
        "headers_hint": "Ex: Cookie: sessão=123\nReferência: https://google.com",
        "workspace_label": "Área de Trabalho:",
        "repo_button": "Repositório Oficial no GitHub",
        "speed_stealth": "Furtivo (Silencioso)",
        "speed_balanced": "Equilibrado",
        "speed_turbo": "Turbo (Agressivo)",
        "speed_insane": "🔥 MODO INSANO",
        "btn_open": "Abrir",
        "snack_report": "Relatórios gerados em: {path}",

        # --- PDF REPORT KEYS (PT) ---
        "pdf_title": "Relatório de Reconhecimento - LazRecon",
        "pdf_continuation": "LazRecon - Continuação do Relatório",
        "pdf_page": "Página",
        "pdf_target": "Alvo",
        "pdf_scanned_at": "Escaneado em",
        "pdf_severity": "Severidade",
        "pdf_url_found": "URL Encontrada",
        "pdf_sev_crit": "CRÍTICO",
        "pdf_sev_med": "MÉDIO"
    }
}

# Define o idioma padrão
LANG = "en"

# Função para buscar chaves dinamicamente
def t(key):
    return languages[LANG].get(key, languages["en"].get(key, key))

# Variável para os imports diretos no main.py e gui.py
lang_en = languages["en"]
lang_pt = languages["pt"]