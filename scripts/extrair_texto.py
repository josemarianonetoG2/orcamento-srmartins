#!/usr/bin/env python3
"""Imprime o texto de cada página da cotação da seguradora.

Uso:
    python extrair_texto.py cotacao.pdf [pasta_para_imagens]

Páginas sem texto selecionável (escaneadas ou "impressas" como desenho) são
salvas como PNG, para serem lidas visualmente. Por padrão vão para uma pasta
temporária; o caminho de cada uma aparece na saída.
"""
import sys
import tempfile
from pathlib import Path

import fitz  # PyMuPDF

if len(sys.argv) not in (2, 3):
    sys.exit(__doc__)

doc = fitz.open(sys.argv[1])
pasta_img = Path(sys.argv[2]) if len(sys.argv) == 3 else None
for i, page in enumerate(doc, start=1):
    print(f"===== Página {i} de {doc.page_count} =====")
    # sort=True lê em ordem visual, o que ajuda nas tabelas de duas colunas.
    texto = page.get_text(sort=True)
    if len(texto.strip()) < 50:
        pasta_img = pasta_img or Path(tempfile.mkdtemp(prefix="cotacao_"))
        pasta_img.mkdir(parents=True, exist_ok=True)
        png = pasta_img / f"pagina_{i}.png"
        # 200 dpi deixa os dígitos legíveis; amplie um recorte se ainda houver dúvida.
        page.get_pixmap(dpi=200).save(png)
        print(f"[PÁGINA SEM TEXTO] Leia a imagem: {png}")
    else:
        print(texto)
