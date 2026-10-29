# Orçamento de Seguro – S.R. Martins

Skill para o Claude que transforma a cotação da seguradora (Allianz, Tokio Marine, Yelum, HDI e outras, de 1 a 6 páginas, inclusive escaneada) no **orçamento de 1 página da S.R. Martins**, com logo, cabeçalho e nota padrão, pronto para enviar ao cliente.

## Como usar

Anexe o PDF da cotação e escreva:

```
/orcamento
```

O Claude lê a cotação, gera o PDF com o nome do segurado (ex.: `MARIA APARECIDA DOS SANTOS.pdf`) na mesma pasta da cotação e mostra um resumo dos valores para você conferir antes de enviar. Ele avisa se a cotação está vencida e pergunta só o que faltar (por exemplo, a placa nas cotações da HDI).

## Instalação

### No Claude (app ou claude.ai)

1. Baixe o arquivo **`orcamento.skill`** na [página de downloads](https://github.com/josemarianonetoG2/orcamento-srmartins/releases/latest).
2. No Claude, vá em **Configurações → Capacidades → Skills** e clique em **Carregar skill**.
3. Escolha o arquivo `orcamento.skill`.

### No Claude Code (Mac)

Abra o Terminal e rode:

```bash
git clone https://github.com/josemarianonetoG2/orcamento-srmartins.git ~/.claude/skills/orcamento && python3 -m venv ~/.claude/skills/orcamento/.venv && ~/.claude/skills/orcamento/.venv/bin/pip install pymupdf
```

Depois abra uma sessão nova do Claude Code e use `/orcamento`.

Para atualizar depois:

```bash
git -C ~/.claude/skills/orcamento pull
```

## O que tem aqui

| Arquivo | Para que serve |
|---|---|
| `SKILL.md` | Instruções que o Claude segue. |
| `references/campos.md` | De onde sai cada campo em cada seguradora e as regras de pagamento e franquias. |
| `scripts/extrair_texto.py` | Lê o texto da cotação (e transforma páginas escaneadas em imagem). |
| `scripts/gerar_orcamento.py` | Desenha o PDF de 1 página em cima do modelo. |
| `assets/modelo_base.pdf` | Modelo oficial da S.R. Martins (logo, cabeçalho, rodapé). |
| `assets/fonts/` | Fonte Carlito, compatível com a Calibri do modelo (licença OFL). |
