import re
import os
import platform
import subprocess
import shutil
import httpx  # Unificado com o resto do projeto

# --- FUNÇÕES DE SEGURANÇA E HIGIENE ---

def sanitize_html(html_raw: str) -> str:
    """Limpa conteúdo HTML para visualização segura no navegador."""
    if not html_raw:
        return "[CONTEÚDO VAZIO]"
    
    # Remove Scripts
    clean = re.sub(r"<script_?.*?>.*?</script.*?>", "", html_raw, flags=re.DOTALL | re.IGNORECASE)
    
    # Bloqueia eventos JS (onclick, onerror, etc)
    clean = re.sub(r"\son\w+\s*=", " [EVENTO_BLOQUEADO]=", clean, flags=re.IGNORECASE)
    
    # Remove Iframes e Objetos perigosos
    clean = re.sub(r"<(iframe|object|embed|applet).*?>", "", clean, flags=re.IGNORECASE)
    
    # Higieniza links para evitar cliques acidentais em arquivos salvos (Anti-Phishing)
    clean = re.sub(r'href=["\'](.*?)["\']', r'href="#" data-original-link="\1"', clean, flags=re.IGNORECASE)
    
    return clean

def apply_csp_header(html_content: str) -> str:
    """Aplica uma Content Security Policy restrita para visualização segura."""
    csp_tag = (
        '<meta http-equiv="Content-Security-Policy" content="'
        "default-src 'none'; script-src 'none'; style-src 'unsafe-inline'; "
        "img-src 'self' data:; form-action 'none';\">\n"
    )
    return f"{csp_tag}\n{html_content}"

def save_protected_finding(folder_path, filename, content):
    """Salva achados higienizados em formato .txt para evitar execução acidental."""
    clean_data = sanitize_html(content)
    final_output = apply_csp_header(clean_data)
    
    file_path = os.path.join(folder_path, f"{filename}.txt")
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_output)

def get_safe_folder_name(raw_input: str) -> str:
    """Transforma URL em um nome de pasta válido e limpo."""
    name = raw_input.replace("https://", "").replace("http://", "").replace("www.", "")
    name = name.split('/')[0].split(':')[0]
    return re.sub(r"[^a-zA-Z0-9-]", "_", name)

# --- FUNÇÕES DE MANUTENÇÃO ---

def open_findings_folder():
    """Abre a pasta de resultados no explorador de arquivos nativo (Windows/Linux/macOS)."""
    path = os.path.abspath("findings")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path)
        else:
            cmd = "open" if system == "Darwin" else "xdg-open"
            subprocess.Popen([cmd, path])
    except Exception as e:
        print(f"Erro ao abrir a pasta: {e}")

def clear_findings():
    """Remove todos os arquivos e pastas de resultados anteriores."""
    path = "findings"
    if not os.path.exists(path):
        return
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Erro ao limpar item {item_path}: {e}")

# --- INTELIGÊNCIA DE RECON E VALIDAÇÃO ---

def is_host_alive(url: str) -> bool:
    """
    Verifica se o alvo responde antes de iniciar o scan (Pre-flight Check).
    Evita scans em domínios inexistentes ou offline.
    """
    try:
        with httpx.Client(verify=False, timeout=5.0, follow_redirects=True) as client:
            # HEAD é mais rápido que GET pois não baixa o corpo da página
            response = client.head(url)
            # Se o servidor responder qualquer coisa abaixo de 500 (mesmo erro 404), o host existe
            return response.status_code < 500
    except Exception:
        return False

def detect_waf(url: str) -> str | None:
    """
    Realiza o fingerprinting de WAFs usando headers e cookies via HTTPX.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,xml;q=0.9,*/*;q=0.8',
            'Cache-Control': 'no-cache'
        }
        
        with httpx.Client(verify=False, timeout=5.0, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            
            h = {k.lower(): v.lower() for k, v in response.headers.items()}
            c = {k.lower(): v.lower() for k, v in response.cookies.items()}
            server = h.get("server", "")

            # Detecção de assinaturas comuns
            if any(x in server for x in ["cloudflare", "cf-ray"]) or "cf-ray" in h or "__cf_bm" in c:
                return "Cloudflare"

            if "litespeed" in server:
                return "LiteSpeed (HostGator/Common Hosting)"
            
            if any(x in server for x in ["mod_security", "mod_pagespeed"]) or "x-mod-pagespeed" in h:
                return "ModSecurity"

            if "locaweb" in server or "x-lwaas" in h:
                return "Locaweb Firewall"

            if "x-sucuri-id" in h or "sucuri" in server:
                return "Sucuri WAF"

            if any(x in h for x in ["x-ms-edge", "x-azure-ref"]):
                return "Azure Front Door / WAF"

            if any(x in h for x in ["x-amz-cf-id", "x-amz-cf-pop"]) or "awswaf" in h:
                return "AWS WAF / CloudFront"

            if "akamai" in h or "x-akamai" in h or "edgeserver" in server:
                return "Akamai WAF"

            if "fortiwaf" in c or "f5-traffic-shield" in h or "x-f5-origin" in h:
                return "Fortinet/F5 Big-IP"

            return None
    except Exception:
        return None