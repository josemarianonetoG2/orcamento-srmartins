#!/usr/bin/env python3
"""Gera o orçamento de 1 página da S.R. Martins a partir de um JSON de dados.

Uso:
    python gerar_orcamento.py dados.json saida.pdf

O cabeçalho (logo, endereço), os títulos, o cabeçalho da tabela de coberturas
e a nota de rodapé vêm prontos de assets/modelo_base.pdf. Este script só
escreve os campos variáveis por cima, nas mesmas posições do modelo em Word.
Veja o formato do JSON em references/campos.md.
"""
import json
import sys
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "assets" / "modelo_base.pdf"
FONTS = ROOT / "assets" / "fonts"

# Carlito tem as mesmas medidas da Calibri usada no modelo original.
FONT_FILES = {
    "reg": "Carlito-Regular.ttf",
    "bold": "Carlito-Bold.ttf",
    "ital": "Carlito-Italic.ttf",
    "boldital": "Carlito-BoldItalic.ttf",
}

LEFT = 49.7
RIGHT = 565.0
LABEL_X = 46.2
VALUE_X = 182.7

# Colunas da tabela de coberturas (x inicial de cada valor) no modelo.
COLUNAS = [
    ("veiculo", 48.7, 99.0),
    ("danos_materiais", 104.7, 177.0),
    ("danos_corporais", 182.7, 255.0),
    ("danos_morais", 260.7, 326.0),
    ("app", 331.5, 396.5),
    ("vidros", 407.0, 446.5),
    ("assistencia", 452.0, 510.0),
    ("carro_reserva", 515.9, 574.0),
]

# Títulos das colunas, para redesenhar o cabeçalho quando alguma coluna sai.
TITULOS = {
    "veiculo": ["Veículo"],
    "danos_materiais": ["Danos", "Materiais"],
    "danos_corporais": ["Danos", "Corporais"],
    "danos_morais": ["Danos", "Morais"],
    "app": ["APP – Morte", "Invalidez"],
    "vidros": ["Vidros"],
    "assistencia": ["Assistência"],
    "carro_reserva": ["Carro", "Reserva"],
}
TABELA_X0, TABELA_X1 = 48.7, 574.0
CABECALHO = fitz.Rect(41.0, 299.5, 575.0, 325.6)  # entre as duas linhas azuis


def ausente(valor):
    return not valor or str(valor).strip().lower() in ("não", "nao", "-")


class Pagina:
    def __init__(self, page):
        self.page = page
        self.fonts = {}
        for key, name in FONT_FILES.items():
            path = str(FONTS / name)
            page.insert_font(fontname=key, fontfile=path)
            self.fonts[key] = fitz.Font(fontfile=path)

    def largura(self, texto, fonte, tamanho):
        return self.fonts[fonte].text_length(texto, fontsize=tamanho)

    def texto(self, x, y, texto, fonte="reg", tamanho=11, max_x=None, alinhar="esq"):
        """Escreve uma linha com baseline em y. Reduz a fonte se passar de max_x."""
        if max_x is not None:
            while tamanho > 7 and self.largura(texto, fonte, tamanho) > max_x - x:
                tamanho -= 0.5
        if alinhar == "dir":
            x = x - self.largura(texto, fonte, tamanho)
        self.page.insert_text((x, y), texto, fontname=fonte, fontsize=tamanho)

    def paragrafo(self, x, y, partes, tamanho=10, entrelinha=12.2, max_x=RIGHT):
        """Escreve texto corrido com quebra de linha. partes = [(texto, fonte), ...]."""
        cx = x
        espaco = {}
        for texto, fonte in partes:
            espaco[fonte] = self.largura(" ", fonte, tamanho)
            for palavra in texto.split():
                w = self.largura(palavra, fonte, tamanho)
                if cx > x and cx + w > max_x:
                    cx = x
                    y += entrelinha
                self.page.insert_text((cx, y), palavra, fontname=fonte, fontsize=tamanho)
                cx += w + espaco[fonte]
        return y


def gerar(dados, saida):
    doc = fitz.open(BASE)
    cob = dados["coberturas"]
    # A corretora mostra só o que o cliente tem: cobertura "Não" sai da tabela.
    colunas = [c for c in COLUNAS if not ausente(cob.get(c[0]))]
    if len(colunas) < len(COLUNAS):
        # Apaga só o texto do cabeçalho do modelo; as linhas azuis ficam.
        doc[0].add_redact_annot(CABECALHO)
        doc[0].apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                                graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    p = Pagina(doc[0])

    # --- Segurado / veículo / CEP ------------------------------------------
    segurado = dados["segurado"].strip().upper()
    condutor = (dados.get("condutor") or "").strip().upper()
    veiculo = dados["veiculo"].strip()
    if dados.get("placa"):
        veiculo = f"{veiculo} - {dados['placa'].strip().upper()}"

    linhas = []
    if dados.get("pessoa_juridica") and (not condutor or condutor == segurado):
        # Empresa sem condutor informado: só o nome da empresa.
        linhas.append(("SEGURADO:", segurado))
    elif not condutor or condutor == segurado:
        linhas.append(("SEGURADO E CONDUTOR:", segurado))
    else:
        linhas.append(("SEGURADO:", segurado))
        linhas.append(("CONDUTOR:", condutor))
    linhas.append(("VEÍCULO:", veiculo))
    linhas.append(("CEP DE PERNOITE:", dados["cep_pernoite"].strip()))

    # No modelo as linhas ficam a ~19,6 pt uma da outra a partir de y=204,4.
    passo = 19.6 if len(linhas) <= 3 else 14.5
    y = 204.4
    for rotulo, valor in linhas:
        p.texto(LABEL_X, y, rotulo, "bold", 11)
        p.texto(VALUE_X, y, valor, "bold", 11, max_x=RIGHT)
        y += passo

    # --- Tabela de coberturas ----------------------------------------------
    if len(colunas) < len(COLUNAS):
        # Redistribui as colunas que ficaram pela largura toda da tabela.
        largura = (TABELA_X1 - TABELA_X0) / len(colunas)
        colunas = [(chave, TABELA_X0 + i * largura, TABELA_X0 + (i + 1) * largura - 4)
                   for i, (chave, _, _) in enumerate(colunas)]
        for chave, x, max_x in colunas:
            titulo = TITULOS[chave]
            ys = [316.0] if len(titulo) == 1 else [309.3, 322.7]
            for linha, y in zip(titulo, ys):
                p.texto(x, y, linha, "bold", 11.04, max_x=max_x)
    for chave, x, max_x in colunas:
        p.texto(x, 340.5, str(cob[chave]), "reg", 10, max_x=max_x - 2)

    # --- Opções de pagamento -----------------------------------------------
    y = 420.2
    for op in dados["pagamento"]:
        p.texto(82.0, y, op["parcelas"], "reg", 11, alinhar="dir")
        p.texto(93.0, y, "R$", "reg", 11)
        p.texto(179.5, y, op["valor"], "reg", 11, alinhar="dir")
        if op.get("descricao"):
            p.texto(196.9, y, op["descricao"], "reg", 11, max_x=RIGHT)
        y += 13.45
    ultima_parcela = y - 13.45

    # --- Franquias ---------------------------------------------------------
    # O bloco acompanha o fim das parcelas, como no Word.
    if dados.get("isencao_primeira_franquia"):
        y = ultima_parcela + 48.0
        p.texto(LEFT, y, "COM ISENÇÃO DA 1ª FRANQUIA", "bold", 11)
        y += 32.7
    else:
        y = ultima_parcela + 64.3

    if dados.get("franquia_casco"):
        p.texto(LEFT, y, f"CASCO: {dados['franquia_casco']}", "bold", 11)
        y += 15.4

    franquias = (dados.get("franquias_texto") or "").strip()
    if franquias:
        y = p.paragrafo(LEFT, y, [("Franquias:", "boldital"), (franquias, "ital")])
        y += 15.2

    extras = (dados.get("franquias_extras_texto") or "").strip()
    if extras:
        p.paragrafo(LEFT, y, [(extras, "boldital")])

    doc.subset_fonts()
    doc.set_metadata({
        "title": f"Orçamento de Seguro - {segurado}",
        "author": "S.R. Martins Corretora de Seguros",
    })
    doc.save(saida, garbage=4, deflate=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--sobrescrever"]
    if len(args) != 2:
        sys.exit(__doc__)
    # O orçamento feito à mão costuma ter o mesmo nome; nunca apague sem querer.
    if Path(args[1]).exists() and "--sobrescrever" not in sys.argv:
        sys.exit(f"Já existe um arquivo em {args[1]}. Escolha outro nome "
                 "ou rode de novo com --sobrescrever se o usuário confirmar.")
    with open(args[0], encoding="utf-8") as f:
        gerar(json.load(f), args[1])
    print(f"Orçamento gerado: {args[1]}")
