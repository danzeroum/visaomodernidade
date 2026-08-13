#!/usr/bin/env python3
"""
Gera corpus_britanico_canonico.json — tabela canônica dos dez textos britânicos
presentes no Gabinete de Leitura segundo a tese de Maria Angélica Lau Pereira Soares (2006).

Fonte primária: TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf
Cada afirmação é referenciada com paginação dupla (PDF / impressa).
"""
import json
from pathlib import Path

OUT = Path("/home/z/my-project/output/corpus_britanico_canonico.json")

corpus = {
    "$schema": "./schema_corpus_britanico_canonico.json",
    "versao": "1.1.0",
    "data_geracao": "2026-08-14",
    "fonte_primaria": {
        "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf",
        "autora": "Maria Angélica Lau Pereira Soares",
        "titulo": "Visão da Modernidade — A presença britânica no Gabinete de Leitura (1837-1838)",
        "ano": 2006,
        "instituicao": "Universidade de São Paulo, FFLCH, Departamento de Letras Modernas",
        "orientadora": "Sandra Guardini Teixeira Vasconcelos"
    },
    "metadados": {
        "descricao": "Corpus canônico dos dez textos ficcionais britânicos identificados no Gabinete de Leitura (Cap. 6.2 da tese, p. impressa 82).",
        "principio_filiacao": "Tese é fonte de verdade primária; JSONs anteriores tratados como rascunhos.",
        "paginacao": {
            "regra_global": "Não há offset universal garantido para toda a dissertação; nas páginas pré-textuais a distância varia.",
            "mapeamento_verificado": [
                {
                    "secao": "Capítulo 6 (A nação britânica no Gabinete de Leitura)",
                    "pagina_impressa_inicio": 76,
                    "pagina_pdf_inicio": 84,
                    "offset": 8,
                    "metodo_verificacao": "Marcador 'Capítulo 6' encontrado no PDF p.84 = impressa p.76 (confirmado via pdftotext -layout)."
                },
                {
                    "secao": "Capítulos 1 a 6 (corpo do texto, pós-pré-textuais)",
                    "observacao": "Offset 8 verificado para o corpo da dissertação a partir do Capítulo 1; pré-textuais (capa, folha de rosto, resumo, sumário) seguem paginação romana ou própria e não devem ser derivados por esta regra."
                }
            ],
            "instrucao_consumidor": "Cada evidência deve armazenar explicitamente pagina_pdf_* e pagina_impressa_* quando disponíveis. Consumidores (HTML, scripts) nunca devem derivar uma a partir da outra em tempo de execução."
        },
        "convencoes_id": "IDs estáveis em kebab-case; slugs derivados do título no Gabinete."
    },
    "itens": [
        # 1. Costumes Ingleses
        {
            "id": "corpus:costumes-ingleses",
            "titulo_gabinete": "Costumes Ingleses — Um Amador da Vida Campestre",
            "titulo_original": "A Cockney Country-Gentleman",
            "autor_original": "John Poole",
            "autor_status": "identificado",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 30,
                    "data_iso": "1838-03-04",
                    "paginas_periodico": "233-236",
                    "papel": "publicacao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": "Colburn's Magazine",
                "status_epistemologico": "problematico",
                "observacao": "Não existiu na Grã-Bretanha publicação intitulada Colburn's Magazine. Provável confusão com Henry Colburn, proprietário da New Monthly Magazine na época."
            },
            "fonte_original_identificada": {
                "veiculo": "The New Monthly Magazine and Humorist",
                "data": "1837-06",
                "data_iso": "1837-06",
                "status_epistemologico": "identificado",
                "editor_epoca": "Theodore Hook"
            },
            "original_identificado": True,
            "rota_tradutoria": {
                "status": "nao_identificado",
                "descricao": "Original inglês identificado (A Cockney Country-Gentleman, jun/1837) e versão francesa descartada como fonte direta (Le Cockney Campagnard, fev/1838); a rota efetiva entre original e versão brasileira permanece não determinada. O que é problemático é a fonte declarada 'Colburn's Magazine', não a existência do original."
            },
            "mediacao_francesa": {
                "status": "documentado",
                "descricao": "Há versão francesa na Revue Britannique, 'Le Cockney Campagnard', publicada em fevereiro de 1838. A tese afirma expressamente que a versão brasileira NÃO é tradução desta versão francesa. A mediação francesa, portanto, não é rota confirmada — é candidata descartada pela tese para este texto específico."
            },
            "operacoes_tradutorias_ids": [
                "op:costumes:atenuacao-ironia-fieldlove",
                "op:costumes:modificacao-trabalho-rural",
                "op:costumes:alteracao-desfecho-positivo"
            ],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p103-111:costumes-comparacao",
                "evidence:soares:2006:pdf-p137-138:revue-britannique-le-cockney"
            ],
            "observacoes": "Assinatura 'P*' no original identificada como John Poole. Análise comparativa mais extensa do corpus (PDF 103-111 / impressa 95-103)."
        },
        # 2. Uma Noite no Mar
        {
            "id": "corpus:uma-noite-no-mar",
            "titulo_gabinete": "Uma Noite no Mar",
            "titulo_original": "Davy Jones and the Yankee Privateer",
            "autor_original": None,
            "autor_status": "nao_identificado",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 2,
                    "data_iso": "1837-08-20",
                    "paginas_periodico": "13-15",
                    "papel": "publicacao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": "Blackwood's Magazine",
                "status_epistemologico": "documentado",
                "observacao": "Fonte declarada confirmada pela tese: o texto integra série publicada em cinco partes na Blackwood's Magazine entre setembro de 1829 e outubro de 1830."
            },
            "fonte_original_identificada": {
                "veiculo": "Blackwood's Magazine",
                "data": "1830-07",
                "data_iso": "1830-07",
                "status_epistemologico": "identificado",
                "observacao": "Quarto episódio de uma série de cinco: 1) 'A Scene of Bermuda' (set/1829); 2) 'The Cruise of H. M. S. Torch' (nov/1829); 3) 'Heat and Thirst, A Scene in Jamaica' (jun/1830); 4) 'Davy Jones and the Yankee Privateer' (jul/1830); 5) 'The Quenching of the Torch' (out/1830). A versão brasileira compreende apenas o quarto episódio."
            },
            "original_identificado": True,
            "rota_tradutoria": {
                "status": "nao_identificado",
                "descricao": "Tese não discute rota tradutória específica para este texto; autoria permanece não identificada."
            },
            "mediacao_francesa": {
                "status": "inferido",
                "metodo": "inferencia_por_exclusao",
                "descricao": "A tese afirma (p. impressa 135-136 / PDF 143-144) que sete dos dez textos britânicos tiveram versões francesas na Revue Britannique, e nomeia explicitamente as três exceções (O Testamento, As Honras Hereditárias, Costumes Ingleses). 'Uma Noite no Mar' não figura entre as exceções — logo, por exclusão, teve versão francesa. Contudo, a tese não localiza nominalmente a versão francesa deste texto nem demonstra que ela foi a rota tradutória até o Brasil."
            },
            "operacoes_tradutorias_ids": [],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"
            ],
            "observacoes": "A tese não realiza análise comparativa detalhada deste texto com o original, apenas apresenta a narrativa e identifica o original."
        },
        # 3. O Testamento
        {
            "id": "corpus:testamento",
            "titulo_gabinete": "O Testamento",
            "titulo_original": None,
            "autor_original": "George Crabbe",
            "autor_status": "problematico",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 9,
                    "data_iso": "1837-10-08",
                    "paginas_periodico": "69-71",
                    "papel": "publicacao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": "Crabbe's Posthumous Works",
                "status_epistemologico": "problematico",
                "observacao": "A tese registra (Anexo 3, George Crabbe): 'Não houve publicação com o título indicado.' A fonte declarada no Gabinete é uma referência a uma obra inexistente sob esse nome."
            },
            "fonte_original_identificada": {
                "veiculo": None,
                "data": None,
                "status_epistemologico": "nao_identificado",
                "observacao": "Original não localizado pela tese. Crabbe é autor de prosa e poesia realista, mas a obra específica de onde o texto foi retirado não foi encontrada."
            },
            "original_identificado": False,
            "rota_tradutoria": {
                "status": "nao_identificado",
                "descricao": "Sem original localizado, a rota tradutória não pode ser estabelecida. A autoria atribuída pelo Gabinete a George Crabbe (1754-1832) não foi confirmada nem negada por evidência externa na tese; a própria fonte declarada é problemática."
            },
            "mediacao_francesa": {
                "status": "documentado",
                "descricao": "A tese enumera explicitamente 'O Testamento' entre as três exceções (junto com As Honras Hereditárias e Costumes Ingleses) que NÃO tiveram versão francesa na Revue Britannique. Portanto, não há mediação francesa para este texto."
            },
            "operacoes_tradutorias_ids": [],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p91-93:testamento-fonte-problematica",
                "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"
            ],
            "observacoes": "Status epistemológico global: problematico. Atribuição de autoria pelo Gabinete não confirmada pela pesquisa; fonte declarada inexistente; original não localizado."
        },
        # 4. O Livro da Vida
        {
            "id": "corpus:livro-da-vida",
            "titulo_gabinete": "O Livro da Vida",
            "titulo_original": None,
            "autor_original": None,
            "autor_status": "nao_identificado",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 6,
                    "data_iso": "1837-09-17",
                    "paginas_periodico": "43-46",
                    "papel": "publicacao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": "Retrospective Review",
                "status_epistemologico": "problematico",
                "observacao": "A tese registra: 'a Revue Retrospective [sic] também há problemas porque essa revista se dedicava a resenhas críticas e não publicava narrativas completas, apenas citações de determinados trechos das obras analisadas.'"
            },
            "fonte_original_identificada": {
                "veiculo": None,
                "data": None,
                "status_epistemologico": "nao_identificado",
                "observacao": "Original não localizado pela tese."
            },
            "original_identificado": False,
            "rota_tradutoria": {
                "status": "nao_identificado",
                "descricao": "Sem original localizado, a rota tradutória não pode ser estabelecida."
            },
            "mediacao_francesa": {
                "status": "inferido",
                "metodo": "inferencia_por_exclusao",
                "descricao": "A tese nomeia explicitamente três exceções (O Testamento, As Honras Hereditárias, Costumes Ingleses). 'O Livro da Vida' não figura entre elas — logo, por exclusão, teve versão francesa na Revue Britannique. A tese não localiza nominalmente a versão francesa deste texto nem demonstra que ela foi a rota tradutória até o Brasil."
            },
            "operacoes_tradutorias_ids": [],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p92-93:livro-da-vida-fonte-problematica",
                "evidence:soares:2006:pdf-p12-13:livro-da-vida-republicacao-chronista",
                "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"
            ],
            "observacoes": "Texto já havia sido publicado n'O Chronista (1836) antes do Gabinete de Leitura (1837). Anexo 2 da tese referencia 'n.16' para este texto, mas a data indicada (17/09/1837) corresponde ao n.6 segundo o Anexo 1 — divergência interna da tese registrada no relatório de divergências."
        },
        # 5. O Sedutor
        {
            "id": "corpus:sedutor",
            "titulo_gabinete": "O Sedutor",
            "titulo_original": None,
            "autor_original": "Washington Irving",
            "autor_status": "identificado",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 10,
                    "data_iso": "1837-10-15",
                    "paginas_periodico": "73-75",
                    "papel": "publicacao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": None,
                "status_epistemologico": "nao_identificado",
                "observacao": "O Gabinete de Leitura não indica fonte para 'O Sedutor'; apenas assina como Washington Irving."
            },
            "fonte_original_identificada": {
                "veiculo": None,
                "data": None,
                "status_epistemologico": "nao_identificado",
                "observacao": "A tese não identifica título, veículo ou data de publicação original do texto de Irving. Não inventar título."
            },
            "original_identificado": False,
            "rota_tradutoria": {
                "status": "nao_identificado",
                "descricao": "Tese não realiza análise comparativa de O Sedutor com um original inglês específico. A análise de Irving é comparativa com 'A Perjura' (brasileira) e 'O Vil Sedutor' (Semanario do Cincinnato), não com um original inglês. Irving é americano, não britânico — incluído no corpus britânico por afinidade linguística."
            },
            "mediacao_francesa": {
                "status": "inferido",
                "metodo": "inferencia_por_exclusao",
                "descricao": "A tese nomeia explicitamente três exceções (O Testamento, As Honras Hereditárias, Costumes Ingleses). Este texto não figura entre elas — logo, por exclusão, teve versão francesa na Revue Britannique. A tese não localiza nominalmente a versão francesa deste texto nem demonstra que ela foi a rota tradutória até o Brasil."
            },
            "operacoes_tradutorias_ids": [],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p55-58:sedutor-comparativo",
                "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"
            ],
            "observacoes": "Washington Irving (1783-1859) é escritor americano, não britânico. A tese o inclui no corpus por sua presença como autor de língua inglesa no Gabinete. A análise do texto é de caráter comparativo-pedagógico (moralização), não filológico-tradutório."
        },
        # 6. Manuscrito Achado em uma Casa de Loucos
        {
            "id": "corpus:manuscrito-casa-loucos",
            "titulo_gabinete": "Manuscrito Achado em uma Casa de Loucos",
            "titulo_original": "A Manuscript Found in a Madhouse",
            "autor_original": "Edward Bulwer-Lytton",
            "autor_status": "identificado",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 8,
                    "data_iso": "1837-10-01",
                    "paginas_periodico": "59-60",
                    "papel": "publicacao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": "Literary Souvenir",
                "status_epistemologico": "documentado",
                "observacao": "Fonte declarada confirmada: publicada no volume de 1829 do Literary Souvenir (1825-1835), um dos gift books mais famosos da Inglaterra."
            },
            "fonte_original_identificada": {
                "veiculo": "Literary Souvenir",
                "data": "1829",
                "data_iso": "1829",
                "status_epistemologico": "identificado",
                "observacao": "O original traz nota: 'by the author of Pelham', identificada como Edward Bulwer-Lytton. A autoria somente foi revelada pelo original."
            },
            "original_identificado": True,
            "rota_tradutoria": {
                "status": "nao_identificado",
                "descricao": "Tese não realiza análise comparativa detalhada deste texto com o original; apenas identifica e resume a narrativa."
            },
            "mediacao_francesa": {
                "status": "inferido",
                "metodo": "inferencia_por_exclusao",
                "descricao": "A tese nomeia explicitamente três exceções (O Testamento, As Honras Hereditárias, Costumes Ingleses). Este texto não figura entre elas — logo, por exclusão, teve versão francesa na Revue Britannique. A tese não localiza nominalmente a versão francesa deste texto nem demonstra que ela foi a rota tradutória até o Brasil."
            },
            "operacoes_tradutorias_ids": [],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p98-99:manuscrito-original",
                "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"
            ],
            "observacoes": "Texto discutido também no conjunto de histórias com mocinhas perseguidas (PDF 116-117 / impressa 108-109)."
        },
        # 7. As Honras Hereditárias
        {
            "id": "corpus:honras-hereditarias",
            "titulo_gabinete": "As Honras Hereditárias — História de Amor, de Mistério e de Filosofia",
            "titulo_original": "Hereditary Honours — A Tale of Love and Mystery",
            "autor_original": "Edward Bulwer-Lytton",
            "autor_status": "identificado",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 11,
                    "data_iso": "1837-10-22",
                    "paginas_periodico": "81-83",
                    "papel": "publicacao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": None,
                "status_epistemologico": "nao_identificado",
                "observacao": "O Gabinete assina como 'G. L. Bulwer' mas não indica veículo-fonte estrangeiro; traz apenas nota final explicando a hereditariedade do ofício de carrasco."
            },
            "fonte_original_identificada": {
                "veiculo": "The New Monthly and Literary Journal",
                "data": "1832",
                "data_iso": "1832",
                "status_epistemologico": "identificado",
                "editor_epoca": "Edward Bulwer-Lytton (editor entre 1831 e 1833)"
            },
            "original_identificado": True,
            "rota_tradutoria": {
                "status": "documentado",
                "descricao": "Tese realiza análise comparativa explícita, identificando duas operações tradutórias. Rota tradutória direta do inglês não é afirmada; a tese compara versões mas mantém a rota como RELACAO_DE_DEPENDENCIA_TEXTUAL (original identificado para comparação)."
            },
            "mediacao_francesa": {
                "status": "documentado",
                "descricao": "A tese enumera 'As Honras Hereditárias' explicitamente entre as três exceções (com O Testamento e Costumes Ingleses) que NÃO tiveram versão francesa na Revue Britannique."
            },
            "operacoes_tradutorias_ids": [
                "op:honras:supressao-gesto-caracterizador",
                "op:honras:especificacao-espaco-narrativo"
            ],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p100-103:honras-comparacao",
                "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"
            ],
            "observacoes": "Análise comparativa detalhada nas pp. impressas 92-95 (PDF 100-103)."
        },
        # 8. Terêncio o Alfaiate
        {
            "id": "corpus:terencio-alfaiate",
            "titulo_gabinete": "Terêncio o Alfaiate",
            "titulo_original": "Terence O'Flaherty",
            "autor_original": "Robert Macnish",
            "autor_status": "identificado",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 14,
                    "data_iso": "1837-11-12",
                    "paginas_periodico": "110-112",
                    "papel": "publicacao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": "Forget-me-not",
                "status_epistemologico": "documentado",
                "observacao": "Fonte declarada confirmada: publicado no volume do Forget-me-Not para o ano de 1829."
            },
            "fonte_original_identificada": {
                "veiculo": "Forget-me-Not (gift book, ed. R. Ackermann, dir. Frederic Shobel; publicado 1823-1847)",
                "data": "1829",
                "data_iso": "1829",
                "status_epistemologico": "identificado",
                "observacao": "Texto original assinado por 'A Modern Pythagorean' (em alguns pontos 'The Modern Pythagorean'), pseudônimo de Robert Macnish (1802-1837). Forget-me-Not; a Christmas and New Year's Present for 1823 foi o primeiro gift book inglês."
            },
            "original_identificado": True,
            "rota_tradutoria": {
                "status": "nao_identificado",
                "descricao": "Tese identifica o original e discute aspectos da narrativa mas não realiza análise comparativa tradutória detalhada deste texto."
            },
            "mediacao_francesa": {
                "status": "inferido",
                "metodo": "inferencia_por_exclusao",
                "descricao": "A tese nomeia explicitamente três exceções (O Testamento, As Honras Hereditárias, Costumes Ingleses). Este texto não figura entre elas — logo, por exclusão, teve versão francesa na Revue Britannique. A tese não localiza nominalmente a versão francesa deste texto nem demonstra que ela foi a rota tradutória até o Brasil."
            },
            "operacoes_tradutorias_ids": [],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p93-95:terencio-original",
                "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"
            ],
            "observacoes": "Macnish também é autor de The Anatomy of Drunkness — tese sobre o alcoolismo, relevante para o tema da narrativa. NOTA: a tese apresenta divergência interna sobre a data desta obra: o corpo do Cap. 6.2 (p. impressa 87 / PDF 95) registra '1824'; o Anexo 3, verbete Robert Macnish (p. impressa 171 / PDF 179), registra 'tese apresentada em 1825 e publicada em 1827'. A divergência foi preservada sem escolher uma das datas."
        },
        # 9. Álibi
        {
            "id": "corpus:alibi",
            "titulo_gabinete": "Álibi",
            "titulo_original": "The Alibi; an Assize Anedocte",
            "autor_original": "Thomas Colley Grattan",
            "autor_status": "identificado",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 12,
                    "data_iso": "1837-10-29",
                    "paginas_periodico": "89-91",
                    "papel": "publicacao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": "New Monthly Magazine",
                "status_epistemologico": "documentado",
                "observacao": "Fonte declarada confirmada; porém o Gabinete cita apenas a fonte, não a autoria — esta somente foi descoberta pelo original."
            },
            "fonte_original_identificada": {
                "veiculo": "New Monthly Magazine and Literary Journal",
                "data": "1836-02",
                "data_iso": "1836-02",
                "status_epistemologico": "identificado",
                "observacao": "Original traz nota: 'by the author of Highways and Byways', identificada como Thomas Colley Grattan (1792-1864). Grattan era irlandês, nascido em Dublin."
            },
            "original_identificado": True,
            "rota_tradutoria": {
                "status": "documentado",
                "descricao": "Tese realiza análise comparativa explícita, identificando a operação tradutória de supressão da crítica ao 'modo de ser dos irlandeses'. Rota tradutória direta do inglês permanece como RELACAO_DE_DEPENDENCIA_TEXTUAL (original identificado para comparação)."
            },
            "mediacao_francesa": {
                "status": "inferido",
                "metodo": "inferencia_por_exclusao",
                "descricao": "A tese nomeia explicitamente três exceções (O Testamento, As Honras Hereditárias, Costumes Ingleses). Este texto não figura entre elas — logo, por exclusão, teve versão francesa na Revue Britannique. A tese não localiza nominalmente a versão francesa deste texto nem demonstra que ela foi a rota tradutória até o Brasil."
            },
            "operacoes_tradutorias_ids": [
                "op:alibi:supressao-critica-irlandeses"
            ],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p95-97:alibi-apresentacao",
                "evidence:soares:2006:pdf-p132-134:alibi-comparacao",
                "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"
            ],
            "observacoes": "Gabinete inclui nota original esclarecendo o termo jurídico 'álibi': 'Ausência do indiciado do lugar onde foi cometido o crime de que é acusado, no tempo em que teve lugar.'"
        },
        # 10. Esboços Sicilianos
        {
            "id": "corpus:esbocos-sicilianos",
            "titulo_gabinete": "Esboços Sicilianos",
            "titulo_original": "Sicilian Facts",
            "autor_original": "Edward D. Baynes",
            "autor_status": "identificado",
            "origem_linguistica": "en",
            "fasciculos": [
                {
                    "numero": 31,
                    "data_iso": "1838-03-11",
                    "paginas_periodico": "246-247",
                    "papel": "publicacao"
                },
                {
                    "numero": 32,
                    "data_iso": "1838-03-18",
                    "paginas_periodico": "253-254",
                    "papel": "continua"
                },
                {
                    "numero": 33,
                    "data_iso": "1838-03-25",
                    "paginas_periodico": "260-261",
                    "papel": "continua"
                },
                {
                    "numero": 34,
                    "data_iso": "1838-04-01",
                    "paginas_periodico": "270-271",
                    "papel": "conclusao"
                }
            ],
            "fonte_declarada_no_gabinete": {
                "referencia": "The Metropolitan",
                "status_epistemologico": "documentado",
                "observacao": "Fonte declarada no Gabinete apenas no n.34 (última parte). Os três fascículos anteriores não trazem indicação de fonte, apenas a nota 'Continua' / 'Vide n. anterior'."
            },
            "fonte_original_identificada": {
                "veiculo": "The Metropolitan",
                "data": None,
                "data_iso": None,
                "status_epistemologico": "identificado",
                "observacao": "Tese identifica o veículo e o autor (Edward D. Baynes), mas não fornece data específica de publicação original. Sobre Baynes, a tese registra que não se encontrou informação biográfica além da indicação de outra obra sua, Ovid's Epistles (1818)."
            },
            "original_identificado": True,
            "rota_tradutoria": {
                "status": "documentado",
                "descricao": "Tese realiza análise comparativa do prólogo, identificando a operação tradutória de supressão da nota sobre punição moral e consciência culpada. Rota tradutória direta do inglês permanece como RELACAO_DE_DEPENDENCIA_TEXTUAL."
            },
            "mediacao_francesa": {
                "status": "inferido",
                "metodo": "inferencia_por_exclusao",
                "descricao": "A tese nomeia explicitamente três exceções (O Testamento, As Honras Hereditárias, Costumes Ingleses). Este texto não figura entre elas — logo, por exclusão, teve versão francesa na Revue Britannique. A tese não localiza nominalmente a versão francesa deste texto nem demonstra que ela foi a rota tradutória até o Brasil."
            },
            "operacoes_tradutorias_ids": [
                "op:esbocos:supressao-nota-punicao-moral"
            ],
            "evidencias_ids": [
                "evidence:soares:2006:pdf-p97-98:esbocos-apresentacao",
                "evidence:soares:2006:pdf-p98:esbocos-supressao-nota-punicao",
                "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"
            ],
            "observacoes": "Publicação serializada em quatro fascículos (n.31-34, de 11/03/1838 a 01/04/1838). O texto inglês é uma longa coletânea de pequenas narrativas independentes; o Gabinete publicou duas histórias (a primeira com prólogo+história, a segunda dividida em duas partes, e uma terceira em parte única — ver descrição da tese p. impressa 89)."
        }
    ]
}

OUT.write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Escrito: {OUT}")
print(f"Itens no corpus: {len(corpus['itens'])}")
for it in corpus["itens"]:
    print(f"  - {it['id']:40s} | fascículos: {[f['numero'] for f in it['fasciculos']]}")
