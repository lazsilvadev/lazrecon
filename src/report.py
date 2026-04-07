from fpdf import FPDF
import os
import re
from datetime import datetime

class LazReport(FPDF):
    def __init__(self, lang_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang_dict # Armazena as traduções aqui

    def header(self):
        if self.page_no() == 1:
            self.set_font("helvetica", "B", 15)
            # Usa a tradução do título
            self.cell(0, 10, self.lang.get("pdf_title", "Relatório de Reconhecimento"), border=False, align="C", ln=True)
            self.ln(5)
        else:
            self.set_font("helvetica", "I", 9)
            self.set_text_color(100, 100, 100)
            # Usa a tradução da continuação
            continuation = self.lang.get("pdf_continuation", "LazRecon - Continuação")
            self.cell(0, 10, continuation, border=False, align="R", ln=True)
            self.set_text_color(0, 0, 0)
            self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        # Tradução da palavra "Página"
        page_word = self.lang.get("pdf_page", "Página")
        self.cell(0, 10, f"{page_word} {self.page_no()}/{{nb}}", align="C")

def get_severity(status, url, lang):
    url = url.lower()
    critical_extensions = [".sql", ".env", ".db", ".zip", ".bak", ".conf", ".git", ".config"]
    if any(ext in url for ext in critical_extensions) and status == "200":
        return (lang.get("pdf_sev_crit", "CRÍTICO"), (255, 0, 0))
    
    medium_paths = ["admin", "login", "config", "panel", "setup", "api"]
    if any(p in url for p in medium_paths) or status == "403":
        return (lang.get("pdf_sev_med", "MÉDIO"), (255, 140, 0))
    
    return ("INFO", (0, 0, 255))

def sanitize_for_safety(text):
    clean = re.sub(r'<[^>]*>', '', str(text))
    clean = re.sub(r'[;`$]', '', clean)
    return clean.strip()

def get_safe_filename(target_url):
    name = re.sub(r'https?://', '', target_url)
    name = re.sub(r'[^a-zA-Z0-9.\-]', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    return f"{name}.txt"

# --- AGORA RECEBE O PARÂMETRO 'lang' ---
def save_pdf(groups: dict, out_dir: str, lang: dict, filename: str = "LazRecon_Report_target.pdf") -> str:
    pdf = LazReport(lang_dict=lang) # Passa o dicionário para a classe
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.alias_nb_pages()
    pdf.add_page()

    findings_dir = os.path.abspath("findings")
    os.makedirs(findings_dir, exist_ok=True)

    for alvo, items in groups.items():
        if pdf.get_y() > 250:
            pdf.add_page()

        pdf.set_font("helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        # Alvo e Escaneado em (Traduzidos)
        pdf.cell(110, 10, f" {lang.get('pdf_target', 'Alvo')}: {alvo}", fill=True)
        pdf.set_font("helvetica", "I", 9)
        scanned_at = lang.get('pdf_scanned_at', 'Escaneado em')
        pdf.cell(0, 10, f"{scanned_at}: {data_hora} ", ln=True, fill=True, align="R")
        pdf.ln(2)

        txt_filename = get_safe_filename(alvo)
        txt_path = os.path.join(findings_dir, txt_filename)
        
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(f"LAZRECON - LOG\nTARGET: {alvo}\nDATE: {data_hora}\n" + "-"*30 + "\n")

            with pdf.table(col_widths=(22, 18, 60), text_align=("CENTER", "CENTER", "LEFT"), line_height=7) as table:
                header_row = table.row()
                # Cabeçalhos da tabela traduzidos
                header_row.cell(lang.get("pdf_severity", "Severidade"))
                header_row.cell("Status")
                header_row.cell(lang.get("pdf_url_found", "URL Encontrada"))

                for item in items:
                    status = str(item.get("status", ""))
                    url = item.get("url", "")
                    severity_text, severity_color = get_severity(status, url, lang)
                    
                    row = table.row()
                    pdf.set_font("helvetica", "B", 10)
                    pdf.set_text_color(*severity_color)
                    row.cell(severity_text)
                    
                    pdf.set_font("helvetica", "", 10)
                    # Lógica de cores do status (mantida)
                    if status.startswith("2"): pdf.set_text_color(0, 128, 0)
                    else: pdf.set_text_color(0, 0, 0)
                    
                    row.cell(status)
                    pdf.set_text_color(0, 0, 0)
                    row.cell(url)
        
        pdf.ln(8)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    pdf.output(out_path)
    return out_path
