# Campos do orçamento

Regras tiradas de orçamentos reais da corretora para Allianz, Tokio Marine, Yelum e HDI. Em outras seguradoras os nomes mudam, mas a informação é a mesma: procure o equivalente. A seção "Por seguradora", no fim, mostra onde cada coisa fica em cada uma.

## Formato do JSON

```json
{
  "seguradora": "Allianz",
  "segurado": "MARIA APARECIDA DOS SANTOS",
  "condutor": "MARIA APARECIDA DOS SANTOS",
  "veiculo": "HYUNDAI HB20 COMFORT 1.0 12v(Flex) 4p",
  "placa": "ABC1D23",
  "cep_pernoite": "16900-000",
  "coberturas": {
    "veiculo": "100% FIPE",
    "danos_materiais": "R$ 1.000.000,00",
    "danos_corporais": "R$ 1.000.000,00",
    "danos_morais": "R$ 150.000,00",
    "app": "R$ 30.000,00",
    "vidros": "Sim",
    "assistencia": "Km Ilimitado",
    "carro_reserva": "30 Dias"
  },
  "pagamento": [
    {"parcelas": "À vista", "valor": "2.210,42", "descricao": ""},
    {"parcelas": "06x", "valor": "368,40", "descricao": "Cartão de Crédito / Débito"},
    {"parcelas": "10x", "valor": "221,04", "descricao": "Cartão de Crédito"}
  ],
  "isencao_primeira_franquia": true,
  "franquia_casco": "3.341,22",
  "franquias_texto": "Parabrisa 281,00 Lanterna Convencional 153,00 Vidros Laterais 118,00 ...",
  "franquias_extras_texto": "PEQUENOS REPAROS 160,00 - PROTEÇÃO PNEU E RODA 130,00"
}
```

Use os valores como texto, no formato brasileiro (`1.000.000,00`), exatamente como aparecem na cotação. Não converta para número: assim nenhum centavo se perde no arredondamento.

## Segurado, veículo e CEP

| Campo | Regra |
|---|---|
| `segurado` | Nome do segurado/proponente, em maiúsculas. |
| `condutor` | Nome do principal condutor. Se for o próprio segurado (inclusive quando a cotação só diz "Próprio segurado"), repita o nome. O PDF mostra "SEGURADO E CONDUTOR". Se for outra pessoa, mostra as duas linhas. |
| `veiculo` | Copie o campo do veículo como a seguradora escreve, tirando só códigos internos e código FIPE. Não acrescente fabricante nem ano que não estejam nesse campo. Ex.: Tokio traz "FIAT" num campo à parte e "TORO FREEDOM..." no campo Veículo, e o orçamento usa só `TORO FREEDOM 2.0 16V 4X4 DIESEL AUT`. |
| `placa` | Como está na cotação, com ou sem hífen (`ABC-1D23`, `XYZ9A88`). **Algumas cotações não trazem a placa (a HDI, por exemplo). Nesse caso pergunte ao usuário. Não invente nem deixe em branco sem avisar.** |
| `cep_pernoite` | Formato `00000-000`. Se a cotação trouxer só 5 dígitos (Yelum: `16900`), complete com `-000` (`16900-000`). |

## Coberturas

| Campo | Regra |
|---|---|
| `veiculo` | Casco/compreensiva/básica: `100% FIPE` (VMR 100% também é `100% FIPE`). Se não houver casco, `Não`. |
| `danos_materiais` / `danos_corporais` / `danos_morais` | Limite máximo de indenização (LMI) do RCF, com `R$ `. Danos morais pode vir como "Danos Morais e Estéticos". |
| `app` | O LMI de APP Morte por passageiro. Se Morte e Invalidez forem diferentes, use `R$ X / R$ Y`. |
| `vidros` | `Sim` se houver qualquer cobertura ou plano de vidros ("Plano 3", "Completo", "Superior"), senão `Não`. |
| `assistencia` | Guincho/reboque sem limite ("Km Livre", "Ilimitado", "Sem limite de Km") é `Km Ilimitado`. Com limite, `500 Km`, por exemplo. Se a cotação só der o nome do plano, sem quilometragem (Yelum "ASSISTÊNCIA - SUPERIOR"), use `Km Ilimitado` e avise o usuário que foi deduzido do plano. |
| `carro_reserva` | Número de dias: `15 Dias`, `30 Dias`, `35 Dias`. Sem carro reserva, `Não`. Se houver dois prazos (HDI: "7 dias quando terceiro, 30 dias com ar"), use o do próprio sinistro (o maior, que aparece no nome da cobertura). |

Ignore o prêmio de cada cobertura: ele não vai para o cliente. Cobertura sem coluna no modelo (ex.: "Gastos com Defesa", "Despesas Extras") fica de fora, mas cite no resumo ao usuário.

## Opções de pagamento

**Linha 1 – À vista:** o preço total em 1x, normal. Não use o "à vista antecipado" com desconto que algumas seguradoras oferecem (Tokio: "1 – 2.577,27 – Antecipado"). Se esse desconto ainda estiver valendo, mencione ao usuário. Quando o resumo e a tabela de parcelas diferirem em centavos, use a tabela (Allianz: 2.210,41 no resumo, 2.210,42 na tabela; o orçamento usa 2.210,42).

**Demais linhas – parcelas sem juros:** para cada forma de pagamento (cartão de crédito, débito em conta, carnê/boleto/ficha), ache **o maior número de parcelas ainda sem juros**. Depois monte uma linha para cada um desses máximos, do menor para o maior. A descrição lista todas as formas que aceitam aquele número sem juros:

- Tokio: carnê até 4x, débito até 5x, cartão até 12x →
  `04x 681,55 Cartão de Crédito / Débito / Carnê`, `05x 545,22 Cartão de Crédito / Débito`, `12x 227,07 Cartão de Crédito`
- Allianz: boleto só 1x (já é o à vista, não gera linha), débito até 6x, cartão até 10x →
  `06x 368,40 Cartão de Crédito / Débito`, `10x 221,04 Cartão de Crédito`

Detalhes:
- Ordem dos nomes na descrição: `Cartão de Crédito / Débito / Carnê`. "Boleto", "Ficha" e "Carnê" entram como `Carnê`; "Débito em conta" e "Débito/Pix" entram como `Débito`.
- Se a seguradora não indicar juros na tabela (Yelum, HDI), considere **sem juros** a parcela em que *número de parcelas × valor ≈ preço à vista* (diferença de poucos centavos). Ex.: HDI débito 6x 455,40 × 6 = 2.732,40 ≈ 2.732,42, sem juros; 7x 431,76 × 7 = 3.022,32, com juros.
- Yelum escreve "1 + N": o total é N+1 parcelas (`1 + 5` = `06x`, `1 + 11` = `12x`).
- Número de parcelas sempre com dois dígitos e "x" (`04x`, `12x`).
- Uma forma cujo máximo sem juros é 1x não gera linha.

## Franquias

| Campo | Regra |
|---|---|
| `isencao_primeira_franquia` | `true` só quando a cotação disser que a 1ª franquia é isenta (Allianz: "Isenção de franquia"). Tokio "Isenção de 1ª Franquia Parcial: Não" é `false`. O PDF mostra "COM ISENÇÃO DA 1ª FRANQUIA". |
| `franquia_casco` | Valor da franquia do casco/básica, sem `R$` (`2.641,00`). |
| `franquias_texto` | Lista de franquias de vidros, faróis, lanternas e retrovisores, **no texto da própria seguradora**: mantenha a grafia, o `R$` (com ou sem espaço), as barras ou os pontos como ela escreve. Não inclua o rótulo "Franquias:", que o script já põe. |
| `franquias_extras_texto` | Serviços de reparo à parte (pequenos reparos, martelinho, para-choque, lataria e pintura, pneu e roda, "reparo abaixo da franquia"). Sai em negrito itálico, exatamente como você escrever. Em geral vai em maiúsculas, mas siga o exemplo de cada seguradora abaixo (na Yelum, "Franquia" fica com minúsculas). Se não houver, `""`. |

## Por seguradora

**Allianz** (cotação de ~6 páginas)
- Veículo: campo "Veículo" (inclui o fabricante). CEP: "CEP Pernoite".
- Pagamento: seção "Outras formas de pagamento" (Boleto, Débito em Conta, Cartão), com juros indicados.
- Franquias: tabela de duas colunas "Assistência a vidros…". Leia **linha a linha** (esquerda, depois direita), formato `Nome valor` sem `R$`, separados por espaço. Pequenos Reparos e Proteção Pneu e Roda vão para os extras, separados por ` - `:
  `franquias_texto`: `Parabrisa 281,00 Lanterna Convencional 153,00 Vidros Laterais 118,00 Farol Auxiliar/Milha 270,00 ...`
  `franquias_extras_texto`: `PEQUENOS REPAROS 160,00 - PROTEÇÃO PNEU E RODA 130,00`

**Tokio Marine** (~4 páginas)
- Veículo: campo "Veículo" (sem o "Fabricante"). Placa com hífen.
- Pagamento: tabelas "Débito/Pix Aut.", "Ficha" (= Carnê) e "Cartão", com "Sem Juros" indicado.
- Franquias: tabela de três colunas. Leia **coluna por coluna** (de cima para baixo), formato `Nome R$ valor`. Os itens de vidros, faróis, lanternas, retrovisores, teto solar e máquina de vidro vão em `franquias_texto`. Martelinho, para-choque e lataria vão em `franquias_extras_texto`, separados por espaço:
  `franquias_texto`: `Parabrisa R$ 360,00 Vigia/Traseiro R$ 300,00 Lateral R$ 150,00 ... Teto Solar R$ 1.990,00 Máquina de Vidro R$ 345,00`
  `franquias_extras_texto`: `MARTELINHO (TETO) R$ 300,00 MARTELINHO (DEMAIS PEÇAS) R$ 80,00 PARA-CHOQUE (TROCA) R$ 830,00 PARA-CHOQUE (REPARO) R$ 230,00 LATARIA E PINTURA R$ 155,00`

**Yelum** (~2 páginas)
- Veículo: campo "Marca/Tipo do Veículo". CEP só com 5 dígitos (completar `-000`).
- Pagamento: tabela "1 + N" com colunas Carnê, Débito C/C, Cartão e PIX, sem indicar juros (use a conta parcelas × valor).
- Franquias: em "Informações complementares". `franquias_texto` = o texto depois de "VIDROS SUPERIOR (Rede Referenciada) - Franquia" até o último valor, sem a observação final ("- Cobertura LED e Xenon somente quando..."). `franquias_extras_texto` = a linha de pequenos reparos sem o telefone: `PROTECAO PEQUENOS REPAROS - Franquia R$190,00`.

**HDI** (~2 páginas, às vezes **escaneada**, só imagem)
- Veículo: campo "Veículo" sem o código inicial e sem o "(FIPE ...)": `CHEVROLET - ONIX - SEDAN PLUS LT 1.0 12V TB FLEX MEC.`
- **Não traz a placa**: pergunte ao usuário.
- CEP Pernoite vem sem hífen (`16900123` → `16900-123`).
- Pagamento: tabela "Parcelamento" com Cartão de Crédito, Débito em Conta e Carnê, sem indicar juros (use a conta parcelas × valor).
- Franquias: nos "Textos explicativos". `franquias_texto` = o texto de (*1) (vidros) seguido do de (*2) (faróis, lanternas, retrovisores), juntos. `franquias_extras_texto` = o texto de (*4): `REPARO ABAIXO DA FRANQUIA COM FRANQUIA DE R$ 190,00.`
