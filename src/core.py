import httpx
import asyncio
import random
import re
import os
import time
from src import utils 

# Lista de User-Agents para Evasão
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

async def run_scan(
    target: str,
    wordlist: list,
    browser_headers: dict, 
    stop_event,
    on_found,
    on_progress,
    on_finished,
    save_html_dir: str | None = None,
    concurrency: int = 15,
    http_method: str = "GET",
    delay: int = 0 
):
    total = len(wordlist)
    seen_urls = set()
    consecutive_blocks = 0
    MAX_BLOCKS_THRESHOLD = 20 
    response_lengths = {} 
    semaphore = asyncio.Semaphore(concurrency)
    processed_count = 0

    async def fetch(path, client):
        nonlocal consecutive_blocks, processed_count
        
        # --- CHECK 1: ANTES DE ENTRAR NA FILA ---
        if stop_event.is_set() or consecutive_blocks >= MAX_BLOCKS_THRESHOLD:
            processed_count += 1
            return

        try:
            async with semaphore:
                # --- LÓGICA DE DELAY (THROTTLING) ---
                if delay > 0:
                    await asyncio.sleep(delay / 1000.0) 

                # --- CHECK 2: APÓS SAIR DA FILA ---
                if stop_event.is_set() or consecutive_blocks >= MAX_BLOCKS_THRESHOLD:
                    return

                full_url = f"{target.rstrip('/')}/{path.lstrip('/')}"
                
                # --- LÓGICA DE ADVANCED HEADERS & EVASION ---
                current_headers = browser_headers.copy()

                if "User-Agent" not in current_headers:
                    current_headers["User-Agent"] = random.choice(USER_AGENTS)
                
                if "X-Forwarded-For" not in current_headers:
                    random_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    current_headers["X-Forwarded-For"] = random_ip

                if http_method in ["POST", "PUT"]:
                    if "Content-Type" not in current_headers:
                        current_headers["Content-Type"] = "application/x-www-form-urlencoded"
                    if "Content-Length" not in current_headers:
                        current_headers["Content-Length"] = "0"

                # Realiza a requisição
                res = await client.request(
                    method=http_method, 
                    url=full_url, 
                    headers=current_headers, 
                    follow_redirects=True,
                    timeout=httpx.Timeout(5.0, connect=2.0) 
                )
                
                # Detecção de bloqueio
                if res.status_code in (403, 429):
                    consecutive_blocks += 1
                else:
                    consecutive_blocks = 0

                # Processamento de resultados
                if res.status_code != 404:
                    content_len = len(res.text)
                    response_lengths[content_len] = response_lengths.get(content_len, 0) + 1
                    
                    if response_lengths[content_len] < 8: 
                        if full_url not in seen_urls:
                            if save_html_dir:
                                try:
                                    safe_path_label = utils.get_safe_folder_name(path.lstrip("/")) or "index"
                                    filename = f"{res.status_code}_{http_method}_{safe_path_label}"
                                    utils.save_protected_finding(save_html_dir, filename, res.text)
                                except Exception:
                                    pass
                            
                            on_found(res.status_code, full_url, res.text)
                            seen_urls.add(full_url)
        except (httpx.RequestError, asyncio.CancelledError):
            pass
        finally:
            processed_count += 1
            on_progress(processed_count, total)

    limits = httpx.Limits(max_keepalive_connections=concurrency, max_connections=concurrency * 2)
    
    async with httpx.AsyncClient(verify=False, limits=limits) as client:
        tasks = [asyncio.create_task(fetch(p, client)) for p in wordlist]
        
        while True:
            if stop_event.is_set() or consecutive_blocks >= MAX_BLOCKS_THRESHOLD:
                for t in tasks:
                    if not t.done():
                        t.cancel()
                break
            
            if all(t.done() for t in tasks):
                break
                
            await asyncio.wait(tasks, timeout=0.1, return_when=asyncio.FIRST_COMPLETED)
            
        await asyncio.gather(*tasks, return_exceptions=True)

    on_finished(consecutive_blocks >= MAX_BLOCKS_THRESHOLD or stop_event.is_set())

# --- FUNÇÃO DISPARADORA (FACHADA) ---

def start_scan_engine(*args, **kwargs):
    """
    Ponto de entrada síncrono para o motor assíncrono.
    Chamada pela UI dentro de uma Thread.
    """
    return asyncio.run(run_scan(*args, **kwargs))
