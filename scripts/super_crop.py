from PIL import Image
import os

def eliminar_area_transparente(entrada_path, saida_path):
    if not os.path.exists(entrada_path):
        print(f"❌ Erro: Arquivo {entrada_path} não encontrado.")
        return

    # Abre a imagem e garante que ela esteja no modo RGBA (com canal alfa)
    img = Image.open(entrada_path).convert("RGBA")
    
    # 1. Encontra a "caixa delimitadora" (bounding box) do conteúdo não transparente
    # getbbox() retorna as coordenadas (esquerda, cima, direita, baixo)
    bbox = img.getbbox()
    
    if bbox:
        print(f"✅ Conteúdo detectado. Coordenadas do corte: {bbox}")
        # 2. Corta a imagem exatamente nas bordas detectadas
        img_cortada = img.crop(bbox)
        
        # 3. Salva a nova imagem com o fundo transparente original
        img_cortada.save(saida_path)
        print(f"🚀 Sucesso! Imagem salva em: {saida_path}")
    else:
        print("❌ Erro: A imagem parece estar completamente transparente.")

# --- CONFIGURAÇÃO ---
# Coloque o nome do seu arquivo de entrada (o PNG transparente original)
ARQUIVO_ENTRADA = "lazrecon1.png" 
# Nome do arquivo de saída
ARQUIVO_SAIDA = "lazrecon1_sem_padding.png"

# Executa a função
eliminar_area_transparente(ARQUIVO_ENTRADA, ARQUIVO_SAIDA)