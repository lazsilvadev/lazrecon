from PIL import Image

def ultra_crop_icon(entrada_png, saida_ico):
    img = Image.open(entrada_png).convert("RGBA")
    
    # 1. Acha a "caixa delimitadora" do conteúdo não transparente
    bbox = img.getbbox()
    if not bbox:
        print("Erro: Imagem vazia!")
        return
    
    # 2. Corta a imagem apenas no conteúdo real
    img_cortada = img.crop(bbox)
    
    # 3. Transforma em um quadrado perfeito (proporção 1:1)
    largura, altura = img_cortada.size
    tamanho_max = max(largura, altura)
    nova_img = Image.new("RGBA", (tamanho_max, tamanho_max), (0, 0, 0, 0))
    
    # Centraliza o espião no novo quadrado
    offset = ((tamanho_max - largura) // 2, (tamanho_max - altura) // 2)
    nova_img.paste(img_cortada, offset)
    
    # 4. Salva como .ico com múltiplos tamanhos
    tamanhos = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    nova_img.save(saida_ico, format='ICO', sizes=tamanhos)
    print(f"✅ Ícone 'GIGANTE' gerado com sucesso em: {saida_ico}")

ultra_crop_icon("blue_spy_extreme_zoom.png", "icon.ico")