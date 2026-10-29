---
name: orcamento
description: Gera o orçamento de seguro de 1 página da S.R. Martins Corretora de Seguros (com logo, cabeçalho e nota padrão) a partir da cotação completa da seguradora (PDF da Allianz, Tokio Marine, Yelum, HDI, Porto, Bradesco, Mapfre, Suhai etc., de 1 a 6 páginas, inclusive escaneado). Use sempre que o usuário enviar ou mencionar uma cotação/proposta de seguro auto e pedir o orçamento, resumo, "PDF de 1 página", "orçamento pro cliente", "versão da SR Martins" ou "o PDF que a gente manda pro cliente", mesmo que não fale "skill" nem "S.R. Martins". Também é chamada pelos comandos /orcamento e /orçamento junto com o PDF da cotação.
---

# Orçamento de seguro – S.R. Martins

A corretora recebe da seguradora uma cotação longa (~6 páginas). Para o cliente ela manda só **1 página** com o essencial: quem é o segurado, o veículo, as coberturas, as opções de pagamento e as franquias. Esta skill transforma a cotação nessa página, no layout oficial da corretora.

O trabalho se divide em duas partes:
- **Você (Claude)** lê a cotação e decide o valor de cada campo. Cada seguradora escreve de um jeito, então é aqui que entra o julgamento.
- **O script** desenha o PDF. O layout fica sempre igual ao modelo, sem você precisar posicionar nada.

Quando o usuário mandar só o comando (/orcamento ou /orçamento) e o PDF, não pergunte nada antes: faça o passo a passo e devolva o orçamento pronto. Pergunte só o que faltar de verdade (a placa, por exemplo).

## Passo a passo

Para rodar os scripts, use `<skill>/.venv/bin/python` se essa pasta existir (é a instalação local, já com PyMuPDF). Se não existir, use `python`.

1. **Ler a cotação.** Extraia o texto do PDF:
   ```bash
   python <skill>/scripts/extrair_texto.py "<cotacao.pdf>"
   ```
   Se der `No module named 'fitz'`, instale com `pip install pymupdf` (se o ambiente permitir) e tente de novo.
   Cotações escaneadas (a HDI às vezes vem assim) não têm texto. O script salva essas páginas como imagem e mostra o caminho. Abra as imagens e leia os valores com atenção redobrada, porque um dígito trocado vira preço errado.

2. **Montar o JSON de dados.** Siga `references/campos.md`, que diz de onde sai cada campo, como formatar, as regras de pagamento e as particularidades de cada seguradora. Leia esse arquivo toda vez: as regras de pagamento e de franquias pegam detalhes fáceis de errar. Se faltar algo que só o usuário sabe (a placa, na HDI, por exemplo), pergunte antes de gerar.

3. **Gerar o PDF:**
   ```bash
   python <skill>/scripts/gerar_orcamento.py dados.json "<NOME DO SEGURADO>.pdf"
   ```
   Dê ao arquivo o nome completo do segurado em maiúsculas (ex.: `MARIA APARECIDA DOS SANTOS.pdf`), que é o padrão da corretora. Salve na mesma pasta da cotação, a menos que o usuário peça outra. Se já existir um arquivo com esse nome (muitas vezes é o orçamento que a corretora fez à mão), o script se recusa a gravar. Pergunte ao usuário se pode substituir (`--sobrescrever`) ou use outro nome, como `NOME (gerado).pdf`.

4. **Conferir antes de entregar.** Renderize a página e olhe se nada estourou a largura ou ficou vazio:
   ```bash
   python -c "import fitz,sys; fitz.open(sys.argv[1])[0].get_pixmap(dpi=90).save(sys.argv[2])" saida.pdf previa.png
   ```

5. **Responder ao usuário** com o caminho do PDF e um resumo curto do que foi preenchido: segurado, veículo, à vista e as parcelas. Assim ele confere antes de enviar ao cliente. Avise sobre qualquer campo que você teve de supor ou que não estava na cotação. O cliente vai decidir com base nesses números, e um valor errado custa caro para a corretora.

## O que não muda

Cabeçalho, logo, endereço, CNPJ, o título "ORÇAMENTO DE SEGURO AUTOMOVEL", o cabeçalho da tabela de coberturas e a nota do rodapé já estão em `assets/modelo_base.pdf`. Não recrie nada disso. Se a corretora mudar o modelo (outro endereço, outra logo), o certo é gerar um novo `modelo_base.pdf` a partir do Word atualizado, e não desenhar por cima.

## Quando a cotação foge do padrão

- **Mais de uma oferta na cotação** (ex.: "Exclusivo" e "Compacto"): pergunte qual oferta vai para o cliente, a menos que o usuário já tenha dito.
- **Cobertura ausente** (sem carro reserva, sem vidros): use `"Não"` na coluna. Não deixe em branco.
- **Cotação vencida ou quase**: compare a validade da cotação ("Garantimos as condições até…", "Validade cotação", "Cotação válida até") com a data de hoje. Se já venceu ou vence em até 2 dias, gere o orçamento mesmo assim, mas avise o usuário com destaque: o preço pode não valer mais. Se só o início da vigência já passou (comum em renovação), mencione numa linha, sem alarme.
- **Cobertura sem coluna no modelo** (ex.: "RCF – Gastos com Defesa"): fica fora da página. Cite no resumo para o usuário decidir se avisa o cliente.
- **Moto**: o modelo serve, mas o título continua "ORÇAMENTO DE SEGURO AUTOMOVEL", e moto costuma vir sem APP, sem vidros e sem carro reserva (`Não` nessas colunas). Avise o usuário dessas diferenças.
- **Seguro que não é de veículo** (residencial, vida): este modelo é só de automóvel. Diga isso ao usuário em vez de forçar os campos.
