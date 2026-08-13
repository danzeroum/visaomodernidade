# Relatório de Divergências

Este relatório registra todas as divergências encontradas entre os JSONs de entrada (rascunhos) e a tese de Maria Angélica Lau Pereira Soares (2006), que é a fonte de verdade primária.

Convenção: para cada divergência, indica-se o dado no JSON anterior, o dado confirmado na tese, a decisão tomada e a evidência paginada.

---

## Divergência 1: Costumes Ingleses — número do fascículo

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): fascículo n.4, 04/03/1838.
- **Dado confirmado na tese**: fascículo n.30, 04/03/1838, p.233-236.
- **Decisão**: usar n.30, 04/03/1838, p.233-236.
- **Evidência**:
  - PDF p.95 (impressa 87): análise de Costumes Ingleses.
  - PDF p.95 (impressa 87): nota de rodapé 153: "Gabinete de Leitura, n.11 de 22 de outubro de 1837" — esta é referente a Honras Hereditárias, mas confirma o padrão de citação por número.
  - Anexo 1 (PDF p.165 / impressa 157): "N. 30 04/03/1838 / p.233-236 Costumes Ingleses – Um Amador da Vida Campestre [F] / Sem indicação do autor / Fonte: Colburn's Magazine".
  - Anexo 3 (PDF p.193 / impressa 185): "Costumes Ingleses. O Amador da Vida Campestre [04/03/1838, n. 30, p.233-236]".

---

## Divergência 2: Costumes Ingleses — ID de pessoa de John Poole

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): `person:richard-harris-poole`.
- **Dado confirmado na tese**: o autor é John Poole (não Richard Harris Poole).
- **Decisão**: usar `person:john-poole`.
- **Evidência**:
  - PDF p.95 (impressa 87): "'A Cockney Country-Gentleman' traz a assinatura P*, utilizada por John Poole, assíduo colaborador da revista."
  - Anexo 3, verbete JOHN POOLE (PDF p.182-183 / impressa 174-175): "John Poole (1786?- 1872) dramaturgo e escritor de contos e poemas."

---

## Divergência 3: Robert Macnish — ID de pessoa

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): `person:simon-macnish`.
- **Dado confirmado na tese**: o autor é Robert Macnish (não Simon Macnish).
- **Decisão**: usar `person:robert-macnish`.
- **Evidência**:
  - PDF p.85 (impressa 77): "O texto é assinado por 'A Modern Pythagorean', pseudônimo usado por Robert Macnish."
  - Anexo 3, verbete ROBERT MACNISH (PDF p.179-180 / impressa 171-172): "Robert Macnish (1802-1837) nasceu em Glasgow, na Escócia."

---

## Divergência 4: O Testamento — número do fascículo e data

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): fascículo n.16, 17/12/1837 (manifestação brasileira `manifestation:pt-br:gabinete:o-testamento:1837-12-17`).
- **Dado confirmado na tese**: fascículo n.9, 08/10/1837, p.69-71.
- **Decisão**: usar n.9, 08/10/1837, p.69-71.
- **Evidência**:
  - Anexo 1 (PDF p.154 / impressa 146): "N. 9 08/ 10/ 1837 / p.69- 71 O Testamento [F] / Fonte: Crabbe's POSTHUMOUS WORKS".
  - Anexo 3, verbete GEORGE CRABBE (PDF p.171 / impressa 163): "'O Testamento' [08/10/1837, n. 9, p. 69-71] (Crabbe's Posthumous Works)".

---

## Divergência 5: O Livro da Vida — número do fascículo e data

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): fascículo n.18, 31/12/1837 (manifestação brasileira `manifestation:pt-br:gabinete:o-livro-da-vida:1837-12-31`).
- **Dado confirmado na tese**: fascículo n.6, 17/09/1837, p.43-46.
- **Decisão**: usar n.6, 17/09/1837, p.43-46.
- **Evidência**:
  - Anexo 1 (PDF p.152 / impressa 144): "N.06 17 / 09/ 1837 / p.43- 46 O Livro da Vida [F] / Fonte: Retrospective Review".
  - Cap. 1, PDF p.12-13 (impressa 4-5): "Outra história do Gabinete de Leitura n. 16 (17 de setembro de 1837), 'O Livro da Vida'..." — **observação: a tese cita aqui "n.16", mas a data 17/09/1837 corresponde ao n.6 segundo o próprio Anexo 1 da tese. Esta é uma divergência interna da própria tese, registrada abaixo.**

---

## Divergência 6: O Livro da Vida — divergência INTERNA da própria tese (Anexo 2)

- **Dado no Anexo 2 da tese** (PDF p.170 / impressa 162): `"O Livro da Vida" [Ficção] [Gabinete de Leitura n.16 17/09/1837]`.
- **Dado no Anexo 1 da tese** (PDF p.152 / impressa 144): `N.06 17 / 09/ 1837 / p.43- 46 O Livro da Vida`.
- **Decisão**: usar n.6 (Anexo 1 é a fonte autoritativa para a numeração dos fascículos; a data 17/09/1837 confirmada em ambos; o "n.16" no Anexo 2 é um erro tipográfico da tese — existe um n.16 real em 26/11/1837).
- **Evidência**: PDF p.12 (impressa 4) e PDF p.170 (impressa 162) — ambas as menções da tese.
- **Ação**: registrar esta divergência interna da tese no grafo (`evidence:soares:2006:pdf-p12-13:livro-da-vida-republicacao-chronista` observa o problema).

---

## Divergência 7: O Sedutor — número do fascículo e data

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): fascículo n.23, 04/02/1838 (manifestação brasileira `manifestation:pt-br:gabinete:o-sedutor:1838-02-04`).
- **Dado confirmado na tese**: fascículo n.10, 15/10/1837, p.73-75.
- **Decisão**: usar n.10, 15/10/1837, p.73-75.
- **Evidência**:
  - Anexo 1 (PDF p.155 / impressa 147): "N. 10 15/ 10 / 1837 / p.73- 75 O Sedutor [F] / Autor: Washington Irving".
  - Anexo 3, verbete WASHINGTON IRVING (PDF p.186 / impressa 178): "'O Sedutor' [15/10/1837, n. 10, p. 73-75]".
  - Cap. 4 (PDF p.55 / impressa 47): nota de rodapé 104: "'O Sedutor' foi publicado no n. 10, de 15 outubro de 1837".

---

## Divergência 8: Terêncio o Alfaiate — número do fascículo e data

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): fascículo n.21, 21/01/1838 (manifestação brasileira `manifestation:pt-br:gabinete:terencio-o-alfaiate:1838-01-21`).
- **Dado confirmado na tese**: fascículo n.14, 12/11/1837, p.110-112.
- **Decisão**: usar n.14, 12/11/1837, p.110-112.
- **Evidência**:
  - Anexo 1 (PDF p.157 / impressa 149): "N. 14 12 / 11 / 1837 / p.110-112 Terêncio o Alfaiate [F] / Sem indicação do autor / Fonte: Forget-me-not".
  - Anexo 3, verbete ROBERT MACNISH (PDF p.179 / impressa 171): "'Terêncio o alfaiate' [12/11/1837, n.14, p. 110-112] (Forget me not)".

---

## Divergência 9: Álibi — número do fascículo e data

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): fascículo n.13, 12/11/1837 (manifestação brasileira `manifestation:pt-br:gabinete:alibi:1837-11-12`).
- **Dado confirmado na tese**: fascículo n.12, 29/10/1837, p.89-91.
- **Decisão**: usar n.12, 29/10/1837, p.89-91.
- **Evidência**:
  - Anexo 1 (PDF p.156 / impressa 148): "N. 12 29 / 10/ 1837 / p.89- 91 Álibi [F] / Fonte: New Monthly Magazine".
  - Anexo 3, verbete THOMAS COLLEY GRATTAN (PDF p.173 / impressa 165): "'Álibi' [29/10/1837, n. 12, p. 89-91] (New Monthly Magazine)".

---

## Divergência 10: Manuscrito Achado em uma Casa de Loucos — número do fascículo e data

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): fascículo n.8, 01/04/1838 (manifestação brasileira `manifestation:pt-br:gabinete:manuscrito-casa-loucos:1838-04-01`).
- **Dado confirmado na tese**: fascículo n.8, 01/10/1837, p.59-60.
- **Decisão**: usar n.8, 01/10/1837, p.59-60 (a numeração n.8 do JSON anterior está correta, mas a data estava trocada com a do n.34).
- **Evidência**:
  - Anexo 1 (PDF p.154 / impressa 146): "N. 8 01/ 10/ 1837 / p.59- 60 Manuscrito Achado em uma Casa de Loucos [F] / Fonte: Literary Souvenir".
  - Anexo 3, verbete BULWER-LYTTON (PDF p.166 / impressa 158): "'Manuscrito achado em uma casa de loucos' [01/10/1837, n. 8, p.59-60] (Literary Souvenir)".

---

## Divergência 11: Uma Noite no Mar — número do fascículo e data

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): fascículo n.5, 11/03/1838 (manifestação brasileira `manifestation:pt-br:gabinete:uma-noite-no-mar:1838-03-11`).
- **Dado confirmado na tese**: fascículo n.2, 20/08/1837, p.13-15.
- **Decisão**: usar n.2, 20/08/1837, p.13-15.
- **Evidência**:
  - Anexo 1 (PDF p.151 / impressa 143): "N. 02 20 / 08 / 1837 / p.13-15 Uma Noite no Mar [F] / Fonte: Blackwood's Magazine".

---

## Divergência 12: Esboços Sicilianos — número do fascículo e data

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): fascículo n.19, 07/01/1838 (manifestação brasileira `manifestation:pt-br:gabinete:esbocos-sicilianos:1838-01-07`).
- **Dado confirmado na tese**: publicação serializada nos fascículos n.31, 32, 33 e 34, de 11/03/1838 a 01/04/1838.
  - n.31 (11/03/1838), p.246-247
  - n.32 (18/03/1838), p.253-254
  - n.33 (25/03/1838), p.260-261
  - n.34 (01/04/1838), p.270-271
- **Decisão**: usar a serialização completa nos fascículos 31-34.
- **Evidência**:
  - Anexo 1 (PDF p.165-167 / impressa 157-159): entradas para n.31-34.
  - Cap. 6.2 (PDF p.89 / impressa 81): "'Esboços Sicilianos' foi publicada no Gabinete de Leitura em quatro episódios".

---

## Divergência 13: Manifestações inglesas com datas placeholder "c1830"

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): múltiplas manifestações inglesas com `c1830`, `c1835` como data (placeholders para "circa 1830/1835").
- **Dado confirmado na tese**: datas específicas para a maioria dos originais.
- **Decisão**: substituir placeholders por datas precisas quando a tese fornece; manter `null` quando a tese não fornece data específica (caso de Esboços Sicilianos / Sicilian Facts).
- **Mapeamento**:
  - `manifestation:en:nmm:cockney-country-gentleman:c1830` → `manifestation:en:new-monthly:cockney-country-gentleman:1837-06` (tese: "junho de 1837")
  - `manifestation:en:forget-me-not:terence-oflaherty:c1830` → `manifestation:en:forget-me-not:terence-oflaherty:1829` (tese: "volume do Forget-me-Not para o ano de 1829")
  - `manifestation:en:irving:sedutor:c1830` → removida; tese não identifica título ou veículo original de O Sedutor. Em vez disso, criou-se apenas a manifestação brasileira.
  - `manifestation:en:blackwoods:night-at-sea:c1835` → `manifestation:en:blackwoods:davy-jones:1830-07` (tese: "julho de 1830")
  - `manifestation:en:nmm:hereditary-honours:1832` → mantida como `manifestation:en:new-monthly:hereditary-honours:1832` (tese: "1832")
  - `manifestation:en:nmm:alibi:1836-02` → mantida como `manifestation:en:new-monthly:alibi:1836-02` (tese: "fevereiro de 1836")
  - `manifestation:en:metropolitan:sicilian-sketches:c1835` → `manifestation:en:metropolitan:sicilian-facts` (tese não fornece data específica — data permanece como `null`)
  - `manifestation:en:literary-souvenir:manuscript-madhouse:1829` → mantida (tese: "volume de 1829 do Literary Souvenir")
- **Evidência**: Cap. 6.2 da tese, pp. impressa 83-103.

---

## Divergência 14: O Sedutor — ausência de original inglês identificado

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): manifestação inglesa `manifestation:en:irving:sedutor:c1830` (criada com data placeholder).
- **Dado confirmado na tese**: a tese NÃO identifica título, veículo ou data de publicação original do texto de Washington Irving. A análise comparativa de "O Sedutor" é feita com "A Perjura" (brasileira) e "O Vil Sedutor" (Semanario do Cincinnato), não com um original inglês.
- **Decisão**: remover a manifestação inglesa fabricada. Manter apenas `manifestation:pt-br:gabinete:sedutor:1837-10-15`. Status da obra `work:o-sedutor-irving`: `nao_identificado` para original.
- **Evidência**: Cap. 4 da tese, PDF p.55-58 (impressa 47-50): análise comparativa de O Sedutor sem referência a um original inglês específico. Anexo 3, verbete WASHINGTON IRVING (PDF p.186 / impressa 178): apenas "1) 'O Sedutor' [15/10/1837, n. 10, p. 73-75]" sem citação de original inglês.

---

## Divergência 15: Tipo da aresta para Costumes Ingleses — TRADUZIDA_DE vs RELACAO_DE_DEPENDENCIA_TEXTUAL

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): tipo de aresta `TRADUZIDA_DE` (afirmação direta de rota tradutória).
- **Dado confirmado na tese**: a tese compara as versões mas NÃO demonstra a rota tradutória exata (pode ser direta do inglês, ou via versão francesa da Revue Britannique). A tese afirma expressamente que "a versão brasileira não é a tradução desta francesa" (referring to "Le Cockney Campagnard"), mas não afirma qual rota foi efetiva.
- **Decisão**: substituir `TRADUZIDA_DE` por `RELACAO_DE_DEPENDENCIA_TEXTUAL` com qualificador `original_identificado_para_comparacao` e status `documentado` (para os quatro textos com comparação explícita) ou `identificado` (para os três com original identificado mas sem comparação).
- **Evidência**: PDF p.95-103 (impressa 87-95): análise comparativa que não demonstra rota tradutória.

---

## Divergência 16: George Crabbe — atribuição não confirmada

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): `person:george-crabbe` não estava presente como nó (a atribuição era implícita).
- **Dado confirmado na tese**: a tese registra a atribuição do Gabinete a George Crabbe mas observa que "não houve publicação com o título indicado" (Crabbe's Posthumous Works é inexistente). A atribuição não é confirmada nem negada por evidência externa; o original não foi localizado.
- **Decisão**: incluir `person:george-crabbe` como nó, com aresta `AUTOR_DE` para `work:o-testamento` com status `problematico` e qualificador `atribuicao_nao_confirmada`.
- **Evidência**: Anexo 3, verbete GEORGE CRABBE (PDF p.171-172 / impressa 163-164): "OBSERVAÇÕES: Não houve publicação com o título indicado."

---

## Divergência 17: Edward D. Baynes — sem verbete próprio no Anexo 3

- **Observação (não é divergência com JSON anterior)**: a tese menciona Edward D. Baynes apenas no corpo do Cap. 6.2 (PDF p.89 / impressa 81), não havendo verbete próprio no Anexo 3.
- **Decisão**: criar nó `person:edward-d-baynes` com evidence_id apontando para a menção no Cap. 6.2. Status `documentado` para a existência do autor, mas os dados biográficos são mínimos: a tese registra apenas "sobre quem não se encontrou nenhuma informação biográfica a não ser a indicação de uma outra obra sua, Ovid's Epistles (1818)".
- **Evidência**: PDF p.89 (impressa 81) e PDF p.89-90 (impressa 81-82) — menção no corpo do capítulo.

---

## Divergência 18: Mediação da Revue Britannique — distinção entre existência e rota

- **Dado no JSON anterior** (`grafo_proveniencia_textual_v22.json`): ausência de modelagem explícita da distinção entre (a) existência de versão francesa e (b) rota tradutória via francês.
- **Dado confirmado na tese**: a tese afirma que "sete dos dez textos tiveram versões francesas na Revue Britannique" (existência documentada), mas NÃO demonstra que a versão brasileira derive diretamente dessas versões francesas (rota indeterminada). Para Costumes Ingleses especificamente, a tese afirma expressamente que a versão brasileira NÃO é tradução da versão francesa ("Le Cockney Campagnard", fev/1838).
- **Decisão**: modelar as três relações separadamente:
  1. `DECLARA_COMO_FONTE`: manifestação brasileira → fonte declarada no Gabinete.
  2. `RELACAO_DE_DEPENDENCIA_TEXTUAL`: manifestação brasileira → original identificado para comparação (status `documentado` ou `identificado`, conforme exista análise comparativa).
  3. `INTERMEDIADA_POR`: manifestação brasileira → Revue Britannique (status `documentado` para a existência da versão francesa; observação esclarece que a rota não está demonstrada).
  4. `NAO_E_FONTE_DIRETA_DE`: versão francesa de "Le Cockney Campagnard" → manifestação brasileira de Costumes Ingleses (status `documentado` — afirmação expressa da tese).
- **Evidência**: PDF p.135-136 (impressa 127-128) e PDF p.143-144 (impressa 135-136).

---

## Divergência 19 (v3 → v3.1): Offset de paginação não é universal

- **Dado no JSON anterior** (v3.0): `metadados.offset_paginacao: "pagina_pdf = pagina_impressa + 8 (verificado: Capítulo 6 começa no PDF p.84 = impressa p.76)"`.
- **Dado confirmado na tese e em verificação empírica**: o offset 8 funciona para o corpo da dissertação a partir do Capítulo 1, mas **não é universal** — nas páginas pré-textuais (capa, folha de rosto, resumo, abstract, sumário) a distância entre PDF e impressa varia.
- **Decisão**: remover a regra global; substituir por um `mapeamento_verificado` que registra explicitamente as seções onde o offset foi confirmado (Capítulo 6) e instrui consumidores a nunca derivar uma paginação a partir da outra em tempo de execução.
- **Evidência**: verificação via `pdftotext -layout` mostrou que a página impressa 82 aparece como PDF p.90 (offset 8 confirmado no Capítulo 6), mas páginas pré-textuais seguem paginação própria.

---

## Divergência 20 (v3 → v3.1): Mediação francesa individual — distinção entre existência e rota

- **Dado no JSON anterior** (v3.0): para os 7 textos não-excepcionais, aresta `INTERMEDIADA_POR` com status `documentado`.
- **Dado confirmado na tese**: a tese afirma que "sete dos dez textos tiveram versões francesas na Revue Britannique" e nomeia três exceções explícitas (O Testamento, As Honras Hereditárias, Costumes Ingleses). Para os 7 restantes, a existência individual decorre **por exclusão**, mas a tese não localiza nominalmente cada versão francesa nem demonstra que ela foi a rota tradutória.
- **Decisão**:
  1. Rebaixar `mediacao_francesa.status` de `documentado` para `inferido` com `metodo: "inferencia_por_exclusao"` nos 7 textos não-excepcionais do corpus.
  2. No grafo de proveniência, substituir as 7 arestas `INTERMEDIADA_POR` (que sugeriam rota) por arestas `TEM_VERSAO_FRANCESA_NA_REVUE` (que registram apenas a existência inferida) com status `inferido` e `justificativa` explícita.
  3. Adicionar `TEM_VERSAO_FRANCESA_NA_REVUE` ao vocabulário controlado do schema de proveniência.
- **Evidência**: PDF p.143-144 (impressa 135-136).

---

## Divergência 21 (v3 → v3.1): Rota tradutória de Costumes Ingleses — problematico vs nao_identificado

- **Dado no JSON anterior** (v3.0): `rota_tradutoria.status: "problematico"` para Costumes Ingleses.
- **Dado confirmado na tese**: a rota tradutória de Costumes Ingleses **não é problemática** — é **não determinada**. O que é problemático é a fonte declarada "Colburn's Magazine" (que não existiu), não a existência do original (que está identificado: *A Cockney Country-Gentleman*, New Monthly Magazine and Humorist, jun/1837). A tese demonstra comparação entre versões mas não afirma rota direta do inglês, nem via Revue Britannique (a versão "Le Cockney Campagnard" é expressamente descartada como fonte direta).
- **Decisão**: rebaixar `rota_tradutoria.status` de `problematico` para `nao_identificado`, com descrição esclarecendo que "o que é problemático é a fonte declarada, não a existência do original".
- **Evidência**: PDF p.103-111 (impressa 95-103) e PDF p.137-138 (impressa 129-130).

---

## Divergência 22 (v3 → v3.1): Data de *The Anatomy of Drunkness* — divergência INTERNA da tese

- **Dado no JSON anterior** (v3.0): `The Anatomy of Drunkness (1827)` (segundo o Anexo 3).
- **Dado na tese — divergência interna**:
  - Corpo do Cap. 6.2 (PDF p.95 / impressa 87): "em 1824, publicou sua tese The Anatomy of Drunkness".
  - Anexo 3, verbete Robert Macnish (PDF p.179 / impressa 171): "Sua primeira publicação foi Anatomy of Drunkness, tese apresentada em 1825 e publicada em 1827".
- **Decisão**: preservar a divergência interna da própria tese sem escolher uma das datas. Substituir a data única `(1827)` por uma nota explicativa nos três lugares onde a obra é mencionada (corpus, evidência biográfica, nó pessoa).
- **Evidência**: PDF p.95 (impressa 87) e PDF p.179 (impressa 171).

---

## Lacunas reais que permanecem abertas na tese

Estas não são divergências com JSONs anteriores, mas lacunas documentais que a tese identifica e que foram respeitadas no grafo final:

1. **O Testamento** — original não localizado; atribuição a George Crabbe não confirmada nem negada; fonte declarada (Crabbe's Posthumous Works) inexistente.
2. **O Livro da Vida** — original não localizado; fonte declarada (Retrospective Review) problemática.
3. **O Sedutor** — tese não identifica título, veículo ou data de publicação original do texto de Washington Irving.
4. **Sicilian Facts** (Esboços Sicilianos) — tese não fornece data específica de publicação original em The Metropolitan.
5. **Edward D. Baynes** — sem verbete no Anexo 3; apenas menção no corpo do texto.
6. **Redatores do Gabinete de Leitura** — a tese afirma expressamente: "Não se pode saber com certeza quem eram os redatores do Gabinete de Leitura". A modelagem usa `COLABORA_COM` com observação explicando que Josino, Justiniano e Firmino são prováveis (mas não confirmados) redatores.
7. **Rota tradutória exata para todos os textos** — a tese demonstra comparação mas não afirma rota direta do inglês ou via francês, exceto para o caso negativo de Costumes Ingleses (que NÃO é tradução da versão francesa).
8. **Tradutor(es)** — em nenhum dos dez textos o tradutor é identificado; todos os atributos `tradutor` são `null`.

---

## Resumo das decisões

| # | Item | Decisão |
|---|------|---------|
| 1-12 | Fascículos, datas e páginas | Corrigidos para o que consta no Anexo 1 da tese |
| 13 | Placeholders "c1830", "c1835" | Substituídos por datas precisas ou `null` quando a tese não fornece |
| 14 | Manifestação inglesa fabricada de O Sedutor | Removida |
| 15 | Aresta `TRADUZIDA_DE` | Substituída por `RELACAO_DE_DEPENDENCIA_TEXTUAL` com qualificador |
| 16 | Atribuição de Crabbe a O Testamento | Incluída com status `problematico` |
| 17 | Baynes sem verbete no Anexo 3 | Nó criado com evidência do Cap. 6.2 |
| 18 | Mediação da Revue Britannique (v2.2 → v3) | Três relações distintas modeladas (existência, comparação, negação) |
| 19 | Offset de paginação universal (v3 → v3.1) | Removida regra global; substituída por `mapeamento_verificado` |
| 20 | Mediação francesa individual (v3 → v3.1) | Rebaixada de `documentado` para `inferido` (método: exclusão); nova aresta `TEM_VERSAO_FRANCESA_NA_REVUE` distinta de `INTERMEDIADA_POR` |
| 21 | Rota tradutória de Costumes Ingleses (v3 → v3.1) | Rebaixada de `problematico` para `nao_identificado` (o problemático é a fonte declarada, não a rota) |
| 22 | Data de *The Anatomy of Drunkness* (v3 → v3.1) | Divergência interna da tese (1824 no corpo / 1827 no Anexo 3) preservada sem escolher uma das datas |
