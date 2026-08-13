#!/usr/bin/env python3
"""
Gera grafo_proveniencia_textual_v3.json — grafo de proveniência textual
dos dez textos britânicos do Gabinete de Leitura.

Estrutura:
- nos: Tese, Periodico, Giftbook, Fasciculo, PublicacaoSerializada,
       ObraAbstrata, ManifestacaoTextual, Pessoa, FonteDeclarada, OperacaoTradutoria,
       Evidencia, Argumento, Local
- arestas: vocabulário controlado da Parte D
- operacoes_tradutorias: lista separada, com 2+ manifestações comparadas
- argumentos: enunciações sustentadas pela tese
- evidencias: cada uma com paginação dupla PDF/impressa

Hierarquia de confiança:
- Tese é fonte primária.
- 'documentado' exige evidence_ids não-vazio.
- 'inferido' e 'hipotese' exigem justificativa.
- 'problematico' separa fonte declarada problemática de original identificado.
- Nenhuma rota tradutória direta é afirmada sem comparação explícita.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "grafo_proveniencia_textual_v3.json"

# ---------- Evidências (com paginação dupla) ----------
# Formato do ID: evidence:soares:2006:pdf-p{inicio}-{fim}:{slug}
# Todas com offset 8 entre PDF e impressa (PDF = impressa + 8)
EVIDENCIAS = [
    # Contextuais gerais
    {
        "id": "evidence:soares:2006:pdf-p9-12:redatores-gabinete",
        "tipo": "Evidencia",
        "titulo": "Identificação dos redatores do Gabinete de Leitura e da Tipografia Commercial",
        "fonte": {"obra": "Soares, Maria Angélica Lau Pereira. Visão da Modernidade...", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 9, "pagina_pdf_fim": 12, "pagina_impressa_inicio": 1, "pagina_impressa_fim": 4},
        "tipo_evidencia": "declaracao_autoral",
        "conteudo": "A tese afirma que o Gabinete de Leitura era publicado na Tipografia Commercial pertencente a Josino do Nascimento Silva, que também publicava O Chronista (cujos redatores eram o próprio Josino, Justiniano José da Rocha e Firmino Rodrigues da Silva). Ambos periódicos eram vendidos na livraria H. & E. Laemmert. Não se pode saber com certeza quem eram os redatores do Gabinete de Leitura.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p16-17:condicoes-producao",
        "tipo": "Evidencia",
        "titulo": "Condições de produção da imprensa da época (custos, assinaturas, impressora manual)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 16, "pagina_pdf_fim": 17, "pagina_impressa_inicio": 8, "pagina_impressa_fim": 9},
        "tipo_evidencia": "contexto_historico",
        "conteudo": "Josino do Nascimento Silva possuía sua própria tipografia, que trabalhava com impressora manual. O custo anual estimado de um periódico mensal de 32 páginas era da ordem de 610 mil réis, dos quais cerca de 80% eram gastos com papel. O valor da subscrição anual do Gabinete de Leitura era de 6 mil réis, exigindo um mínimo de 100 assinantes para cobrir as despesas.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique",
        "tipo": "Evidencia",
        "titulo": "As três exceções à mediação da Revue Britannique",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 143, "pagina_pdf_fim": 144, "pagina_impressa_inicio": 135, "pagina_impressa_fim": 136},
        "tipo_evidencia": "declaracao_autoral",
        "conteudo": "A tese afirma: 'dos dez textos ficcionais ingleses presentes no Gabinete de Leitura, sete tiveram versões francesas na Revue Britannique. A exceção ficou por conta de O Testamento, atribuída a George Crabbe, As honras hereditárias de Bulwer-Lytton, e Costumes Ingleses de John Poole. No caso da última, apesar de na Revue Britannique haver uma narrativa intitulada Le Cockney Campagnard, publicada em fevereiro de 1838, a versão brasileira não é a tradução desta francesa.'",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p91-92:prosa-britanica-apresentacao",
        "tipo": "Evidencia",
        "titulo": "Apresentação do conjunto de prosa de ficção britânica do Gabinete de Leitura",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 91, "pagina_pdf_fim": 92, "pagina_impressa_inicio": 83, "pagina_impressa_fim": 84},
        "tipo_evidencia": "declaracao_autoral",
        "conteudo": "A tese afirma: 'Dos noventa e dois textos ficcionais oferecidos aos leitores fluminenses pelo Gabinete de Leitura, dez registram como fonte publicações ou autores de língua inglesa.' Em nota de rodapé, a tese baseia-se no estudo de Maria Eulália Ramicelli sobre a intermediação da Revue Britannique.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    # 1. Costumes Ingleses
    {
        "id": "evidence:soares:2006:pdf-p103-111:costumes-comparacao",
        "tipo": "Evidencia",
        "titulo": "Análise comparativa entre Costumes Ingleses e A Cockney Country-Gentleman",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 103, "pagina_pdf_fim": 111, "pagina_impressa_inicio": 95, "pagina_impressa_fim": 103},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "A tese identifica o original inglês 'A Cockney Country-Gentleman' publicado em junho de 1837 na The New Monthly Magazine and Humorist (editor: Theodore Hook), assinado por 'P*' (John Poole). A indicação 'Colburn's Magazine' no Gabinete é incorreta. A tese realiza análise comparativa detalhada das omissões e modificações (atenuação da ironia sobre Fieldlove, modificação da representação do trabalho rural, alteração do desfecho).",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p137-138:revue-britannique-le-cockney",
        "tipo": "Evidencia",
        "titulo": "Menção à versão francesa 'Le Cockney Campagnard' na Revue Britannique (fev. 1838)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 137, "pagina_pdf_fim": 138, "pagina_impressa_inicio": 129, "pagina_impressa_fim": 130},
        "tipo_evidencia": "declaracao_autoral",
        "conteudo": "A tese afirma que, apesar de existir na Revue Britannique uma narrativa intitulada 'Le Cockney Campagnard' publicada em fevereiro de 1838, a versão brasileira de Costumes Ingleses NÃO é a tradução desta francesa. A tese também registra (segundo Ramicelli) que a versão brasileira difere da versão francesa, apresentando trechos que se encontram em inglês, mas não na versão francesa.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    # Operações tradutórias de Costumes Ingleses
    {
        "id": "evidence:soares:2006:pdf-p106-107:costumes-atenuacao-ironia",
        "tipo": "Evidencia",
        "titulo": "Atenuação da ironia sobre Fieldlove — supressão de 'monótono' e do comentário sobre limitação intelectual",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 106, "pagina_pdf_fim": 107, "pagina_impressa_inicio": 98, "pagina_impressa_fim": 99},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "No original inglês, à expressão 'trabalho infatigável' segue-se o adjetivo 'monótono' (no original: 'By dint of unremitting drudgery...'). O texto brasileiro omite o adjetivo 'monótono' e, sobretudo, omite o comentário irônico do narrador: 'That, indeed, was nearly all he could do; but, since nothing more was required of him, the satisfaction of the firm is not to be wondered at. The march of his intellect had certainly not kept pace with the progress of his hand; and, if it marched at all, it was, to say the most of it, to the tune of a very slow march.' A versão brasileira registra apenas os aspectos positivos alcançados por Fieldlove.",
        "citacao": "That, indeed, was nearly all he could do; but, since nothing more was required of him, the satisfaction of the 'firm' is not to be wondered at. The march of his intellect had certainly not kept pace with the progress of his hand",
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p108-109:costumes-modificacao-trabalho-rural",
        "tipo": "Evidencia",
        "titulo": "Modificação na representação do trabalho rural — substituição da fala do cura por 'elegância preguiçosa'",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 108, "pagina_pdf_fim": 109, "pagina_impressa_inicio": 100, "pagina_impressa_fim": 101},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "No original inglês, o cura descreve a vida ativa do proprietário rural Squire Woodleigh (gestão da propriedade, magistratura, sessões, etc.). Na versão brasileira, a resposta do cura é outra: 'Estes senhores estão habituados desde a infância a uma elegância preguiçosa, que, graças a Deus, vós não conhecestes. A caça e a pesca tinham encantos para vós porque vos divertiam de vossas ordinárias ocupações.' A versão brasileira confirma o discurso de Mr. Urby segundo o qual 'para gozar da vida do campo ou da cidade é mister ter sido educado para isso', diluindo o tom crítico.",
        "citacao": "Estes senhores estão habituados desde a infância a uma elegância preguiçosa, que, graças a Deus, vós não conhecestes.",
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p109-111:costumes-alteracao-desfecho",
        "tipo": "Evidencia",
        "titulo": "Alteração de desfecho irônico para encerramento mais positivo",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 109, "pagina_pdf_fim": 111, "pagina_impressa_inicio": 101, "pagina_impressa_fim": 103},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "No original inglês, Fieldlove retorna a Londres e repete ipisis litteris o discurso de Mr. Urby sobre o hábito, confirmando seus limitados horizontes e caráter acrítico (trecho omitido na versão brasileira). Na versão brasileira, o desfecho é positivo: 'Voltou para Londres, e continuou, não seus negócios, mas suas relações. Sua honra proporcionou-lhe consideração, e muita gente apreciando sua inteligência (...) deram-lhe seus sufrágios para importantes cargos da administração da cidade, e talvez que, se Deus lhe der vida, se realize a profecia de seu tio Urby: talvez seja Lord Maire.'",
        "citacao": "Voltou para Londres, e continuou, não seus negócios, mas suas relações. Sua honra proporcionou-lhe consideração, e muita gente apreciando sua inteligência quando lhe pediam conselhos, ou a grandeza de sua generosidade quando reclamavam seus serviços, deram-lhe seus sufrágios para importantes cargos da administração da cidade, e talvez que, se Deus lhe der vida, se realize a profecia de seu tio Urby: talvez seja Lord Maire.",
        "status_epistemologico": "documentado"
    },
    # 2. Uma Noite no Mar
    {
        "id": "evidence:soares:2006:pdf-p91:uma-noite-no-mar-original",
        "tipo": "Evidencia",
        "titulo": "Identificação do original de Uma Noite no Mar — Davy Jones and the Yankee Privateer (Blackwood's Magazine, jul/1830)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 91, "pagina_pdf_fim": 91, "pagina_impressa_inicio": 83, "pagina_impressa_fim": 83},
        "tipo_evidencia": "identificacao_original",
        "conteudo": "A tese identifica 'Uma Noite no Mar' como versão de 'Davy Jones and the Yankee Privateer', publicada em julho de 1830 na Blackwood's Magazine. O texto original integra uma série de cinco episódios publicados entre setembro de 1829 e outubro de 1830 (1: A Scene of Bermuda, set/1829; 2: The Cruise of H. M. S. Torch, nov/1829; 3: Heat and Thirst, A Scene in Jamaica, jun/1830; 4: Davy Jones and the Yankee Privateer, jul/1830; 5: The Quenching of the Torch, out/1830). A versão brasileira compreende apenas o quarto episódio.",
        "citacao": None,
        "status_epistemologico": "identificado"
    },
    # 3. O Testamento
    {
        "id": "evidence:soares:2006:pdf-p91-93:testamento-fonte-problematica",
        "tipo": "Evidencia",
        "titulo": "Fonte declarada de O Testamento problemática — Crabbe's Posthumous Works inexistente",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 91, "pagina_pdf_fim": 93, "pagina_impressa_inicio": 83, "pagina_impressa_fim": 85},
        "tipo_evidencia": "problema_proveniencia",
        "conteudo": "A tese afirma (Anexo 3, verbete George Crabbe): 'Não houve publicação com o título indicado.' No corpo do texto (Cap. 6.2): 'No caso de O Testamento não houve uma publicação com o título indicado como fonte.' Atribuição de autoria a George Crabbe não confirmada por evidência externa; original não localizado pela pesquisa.",
        "citacao": None,
        "status_epistemologico": "problematico"
    },
    # 4. O Livro da Vida
    {
        "id": "evidence:soares:2006:pdf-p92-93:livro-da-vida-fonte-problematica",
        "tipo": "Evidencia",
        "titulo": "Fonte declarada de O Livro da Vida problemática — Retrospective Review",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 92, "pagina_pdf_fim": 93, "pagina_impressa_inicio": 84, "pagina_impressa_fim": 85},
        "tipo_evidencia": "problema_proveniencia",
        "conteudo": "A tese afirma: 'O Livro da Vida, cuja fonte indicada é a Retrospective Review, também há problemas porque essa revista se dedicava a resenhas críticas e não publicava narrativas completas, apenas citações de determinados trechos das obras analisadas.'",
        "citacao": None,
        "status_epistemologico": "problematico"
    },
    {
        "id": "evidence:soares:2006:pdf-p12-13:livro-da-vida-republicacao-chronista",
        "tipo": "Evidencia",
        "titulo": "Republicação de O Livro da Vida n'O Chronista",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 12, "pagina_pdf_fim": 13, "pagina_impressa_inicio": 4, "pagina_impressa_fim": 5},
        "tipo_evidencia": "historia_publicacao",
        "conteudo": "A tese registra que O Livro da Vida já havia sido publicada na seção 'Variedades' d'O Chronista em 5, 15 e 19 de outubro de 1836, antes de sua republicação no Gabinete de Leitura n.6 de 17/09/1837. Anexo 2 da tese cita '[Gabinete de Leitura n.16 17/09/1837]' — divergência interna da tese (deveria ser n.6).",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    # 5. O Sedutor
    {
        "id": "evidence:soares:2006:pdf-p55-58:sedutor-comparativo",
        "tipo": "Evidencia",
        "titulo": "Análise comparativa de O Sedutor com A Perjura e O Vil Sedutor",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 55, "pagina_pdf_fim": 58, "pagina_impressa_inicio": 47, "pagina_impressa_fim": 50},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "A tese discute O Sedutor de Washington Irving como exemplo de prosa moralizante, comparando-o com A Perjura (brasileira, anônima) e O Vil Sedutor (Semanario do Cincinnato). A tese NÃO identifica título ou veículo original do texto de Irving, nem realiza análise comparativa tradutória com um original inglês. Irving é apresentado como americano, e o texto é analisado sob o aspecto pedagógico-moral, não filológico.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    # 6. Manuscrito Achado
    {
        "id": "evidence:soares:2006:pdf-p98-99:manuscrito-original",
        "tipo": "Evidencia",
        "titulo": "Identificação do original de Manuscrito Achado em uma Casa de Loucos — A Manuscript Found in a Madhouse (Literary Souvenir 1829, Bulwer-Lytton)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 98, "pagina_pdf_fim": 99, "pagina_impressa_inicio": 90, "pagina_impressa_fim": 91},
        "tipo_evidencia": "identificacao_original",
        "conteudo": "A tese identifica 'Manuscrito Achado em uma Casa de Loucos' como versão de 'A Manuscript Found in a Madhouse', originariamente publicada no volume de 1829 do Literary Souvenir (1825-1835), um dos gift books mais famosos da Inglaterra. A autoria somente foi revelada pelo original, que traz a nota: 'by the author of Pelham', identificado como Edward Bulwer-Lytton.",
        "citacao": None,
        "status_epistemologico": "identificado"
    },
    # 7. As Honras Hereditárias
    {
        "id": "evidence:soares:2006:pdf-p100-103:honras-comparacao",
        "tipo": "Evidencia",
        "titulo": "Análise comparativa entre As Honras Hereditárias e Hereditary Honours",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 100, "pagina_pdf_fim": 103, "pagina_impressa_inicio": 92, "pagina_impressa_fim": 95},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "A tese identifica 'As Honras Hereditárias' como versão de 'Hereditary Honours — A Tale of Love and Mystery', originalmente publicada na The New Monthly and Literary Journal em 1832 (editor da época: o próprio autor, Bulwer-Lytton). A tese discute o tom irônico do narrador e identifica duas operações tradutórias: (a) supressão do gesto caracterizador do protagonista (tentativa desajeitada de fazer um gesto de carinho, quase um soco no rosto da heroína); (b) especificação do espaço narrativo, com 'this country' traduzido como 'metrópole britânica', perdendo a ambiguidade do original.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p101-102:honras-supressao-gesto",
        "tipo": "Evidencia",
        "titulo": "Supressão do gesto caracterizador do protagonista em As Honras Hereditárias",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 101, "pagina_pdf_fim": 102, "pagina_impressa_inicio": 93, "pagina_impressa_fim": 94},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "Em nota de rodapé (n.154) na p. impressa 93, a tese registra: 'Cabe registrar que a versão do Gabinete de Leitura não traz a frase em que o narrador descreve a tentativa desajeitada do protagonista que, ao tentar fazer um gesto de carinho, quase acerta um soco no rosto da heroína. Ao somente registrar a reação de espanto da jovem (na seqüência: o rapaz a chama de \"celeste criatura\", e ela é acometida de terror), a versão brasileira acaba por comprometer a coerência dos eventos. Contudo, dadas as condições muitas vezes precárias em que os periódicos da época eram impressos, não se pode desconsiderar uma falha de impressão.'",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p102-103:honras-especificacao-espaco",
        "tipo": "Evidencia",
        "titulo": "Especificação do espaço narrativo em As Honras Hereditárias",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 102, "pagina_pdf_fim": 103, "pagina_impressa_inicio": 94, "pagina_impressa_fim": 95},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "Original inglês: 'There is a certain country, not very far distant from our own: in a certain small town, close to the metropolis of this country, there once lived a certain young lady, of the name of Laura.' Versão brasileira: 'Em uma cidade pequena vizinha da metrópole britânica, vivia uma moça que se chamava Laura.' A tese argumenta: a expressão 'this country' foi tomada pelo tradutor em sentido literal, mas sua estruturação no original cria uma deliberada ambiguidade (a certain country / this country) que acentua o tom irônico do narrador ao criticar a estrutura de classes da sociedade inglesa. Ao especificar 'britânica', a versão brasileira perde essa ambiguidade.",
        "citacao": "There is a certain country, not very far distant from our own: in a certain small town, close to the metropolis of this country, there once lived a certain young lady, of the name of Laura.",
        "status_epistemologico": "documentado"
    },
    # 8. Terêncio
    {
        "id": "evidence:soares:2006:pdf-p93-95:terencio-original",
        "tipo": "Evidencia",
        "titulo": "Identificação do original de Terêncio o Alfaiate — Terence O'Flaherty (Forget-me-Not 1829, Robert Macnish)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 93, "pagina_pdf_fim": 95, "pagina_impressa_inicio": 85, "pagina_impressa_fim": 87},
        "tipo_evidencia": "identificacao_original",
        "conteudo": "A tese identifica o original 'Terence O'Flaherty' publicado no Forget-me-Not para o ano de 1829. O texto é assinado por 'A Modern Pythagorean' (em algumas referências 'The Modern Pythagorean'), pseudônimo de Robert Macnish (1802-1837). Forget-me-Not; a Christmas and New Year's Present for 1823 foi o primeiro gift book inglês, editado por R. Ackermann e sob direção de Frederic Shobel, publicado de 1823 a 1847.",
        "citacao": None,
        "status_epistemologico": "identificado"
    },
    # 9. Álibi
    {
        "id": "evidence:soares:2006:pdf-p95-97:alibi-apresentacao",
        "tipo": "Evidencia",
        "titulo": "Apresentação e identificação do original de Álibi",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 95, "pagina_pdf_fim": 97, "pagina_impressa_inicio": 87, "pagina_impressa_fim": 89},
        "tipo_evidencia": "identificacao_original",
        "conteudo": "A tese identifica 'Álibi' como versão de 'The Alibi; an Assize Anedocte' [sic], de autoria do escritor irlandês Thomas Colley Grattan, publicada na New Monthly Magazine and Literary Journal de fevereiro de 1836. O Gabinete de Leitura cita apenas a fonte (New Monthly Magazine), não a autoria — esta foi descoberta pelo original, que traz a nota 'by the author of Highways and Byways', identificada como T. C. Grattan. Gabinete inclui nota esclarecendo o termo jurídico 'álibi'.",
        "citacao": None,
        "status_epistemologico": "identificado"
    },
    {
        "id": "evidence:soares:2006:pdf-p132-134:alibi-comparacao",
        "tipo": "Evidencia",
        "titulo": "Comparação entre Álibi e The Alibi — supressão da crítica ao modo de ser dos irlandeses",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 132, "pagina_pdf_fim": 134, "pagina_impressa_inicio": 124, "pagina_impressa_fim": 126},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "A tese cita trecho extenso do original inglês em que o narrador descreve o senhorio Mr. Mulligan e seus empregados (Tim Carney, Dinnis Murphy, etc.) reproduzindo o dialeto irlandês e tecendo crítica ao 'modo de ser dos irlandeses'. A versão brasileira resume drasticamente as imprecações e omite a crítica do narrador: 'Note-se também que a crítica formulada pelo narrador inglês desaparece do texto brasileiro.' A versão brasileira substitui por: 'O estalajadeiro das Armas de Flaherty era talvez neste momento o homem mais ocupado da cidade... foi o sinal dum chuveiro de injúrias irlandesas, com que messer Mulligan mimoseou todos os seus criados, machos e fêmeas, moços e velhos.'",
        "citacao": "Importante observar no original inglês a tentativa de se reproduzir o dialeto local na fala dos personagens, assim como a crítica do narrador em relação ao modo de ser dos irlandeses.",
        "status_epistemologico": "documentado"
    },
    # 10. Esboços Sicilianos
    {
        "id": "evidence:soares:2006:pdf-p97-98:esbocos-apresentacao",
        "tipo": "Evidencia",
        "titulo": "Apresentação e identificação do original de Esboços Sicilianos — Sicilian Facts (The Metropolitan, Edward D. Baynes)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 97, "pagina_pdf_fim": 98, "pagina_impressa_inicio": 89, "pagina_impressa_fim": 90},
        "tipo_evidencia": "identificacao_original",
        "conteudo": "A tese registra que 'Esboços Sicilianos' foi publicada no Gabinete de Leitura em quatro episódios. A versão inglesa, 'Sicilian Facts', foi publicada na revista londrina The Metropolitan. O autor é Edward D. Baynes, sobre quem não se encontrou informação biográfica a não ser a indicação de outra obra sua, Ovid's Epistles (1818). A tese não fornece data específica de publicação original.",
        "citacao": None,
        "status_epistemologico": "identificado"
    },
    {
        "id": "evidence:soares:2006:pdf-p98:esbocos-supressao-nota-punicao",
        "tipo": "Evidencia",
        "titulo": "Supressão da nota sobre punição moral e consciência culpada em Esboços Sicilianos",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 98, "pagina_pdf_fim": 98, "pagina_impressa_inicio": 90, "pagina_impressa_fim": 90},
        "tipo_evidencia": "comparacao_textual",
        "conteudo": "A tese transcreve nota do prólogo do original inglês: 'It will be observed, that in most of the events related, notwithstanding the power of the offenders, and their impunity from any earthly tribunal, a severe retribution has taken place, and moral justice been satisfied even in this state. In the instances where this is not perceptible, it is to be recollected that they have been left to the acute reproaches of a guilty conscience — perhaps the severest of punishments.' A tese afirma: 'na versão publicada no Gabinete de Leitura, o narrador não faz nenhuma referência quanto à possível punição moral dos criminosos, o que, de certa forma, intensifica a crítica a uma sociedade, na qual a Justiça somente pune os pequenos e humildes.'",
        "citacao": "It will be observed, that in most of the events related, notwithstanding the power of the offenders, and their impunity from any earthly tribunal, a severe retribution has taken place, and moral justice been satisfied even in this state.",
        "status_epistemologico": "documentado"
    },
    # Evidências contextuais adicionais (autores)
    {
        "id": "evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton",
        "tipo": "Evidencia",
        "titulo": "Dados biográficos de Edward Bulwer-Lytton (Anexo 3)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 166, "pagina_pdf_fim": 167, "pagina_impressa_inicio": 158, "pagina_impressa_fim": 159},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "Edward George Earle Bulwer-Lytton (1803-1873), primeiro Barão Lytton. Membro do parlamento inglês. Editor da New Monthly Magazine entre 1831 e 1833. Autor de Pelham (1828), Paul Clifford (1830), Eugene Aram (1833), The Last Days of Pompeii (1834), entre outros.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p171-172:autor-crabbe",
        "tipo": "Evidencia",
        "titulo": "Dados biográficos de George Crabbe (Anexo 3)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 171, "pagina_pdf_fim": 172, "pagina_impressa_inicio": 163, "pagina_impressa_fim": 164},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "George Crabbe (1754-1832), nasceu em Suffolk, Inglaterra. Publicou vários poemas, mas também escreveu algumas obras em prosa. Poesia de cunho realista sobre a vida rural. Obras: The Village (1783), The Borough (1810), Tales in Verse (1812), Tales of the Hall (1819). Observação da tese: 'Não houve publicação com o título indicado' (como fonte de O Testamento).",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p175-176:autor-irving",
        "tipo": "Evidencia",
        "titulo": "Dados biográficos de Washington Irving (Anexo 3)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 175, "pagina_pdf_fim": 176, "pagina_impressa_inicio": 167, "pagina_impressa_fim": 168},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "Washington Irving (1783-1859). Escritor americano, autor de contos e ensaios, poeta, biógrafo e colunista. Nascido em Nova York em 3 de abril de 1783. Residiu na Europa de 1817 a 1832. Primeiro escritor americano a alcançar renome internacional. Obras: The Sketch Book Of Geoffrey Crayon, Gent. (1819-20); Bracebridge Hall (1822); Alhambra (1832). Contos mais conhecidos: 'The Legend of Sleepy Hollow' e 'Rip Van Winkle'.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p179-180:autor-macnish",
        "tipo": "Evidencia",
        "titulo": "Dados biográficos de Robert Macnish (Anexo 3)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 179, "pagina_pdf_fim": 180, "pagina_impressa_inicio": 171, "pagina_impressa_fim": 172},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "Robert Macnish (1802-1837), nasceu em Glasgow, Escócia. Formou-se em medicina. Primeira publicação: Anatomy of Drunkness (a tese apresenta divergência interna: o corpo do Cap. 6.2 registra '1824'; o Anexo 3 registra 'tese apresentada em 1825 e publicada em 1827' — divergência preservada sem escolher uma das datas). Em 1830 publicou The Philosophy of Sleep. Sua ficção foi marcada pelo fantástico e grotesco. A partir de 'The Metempsychosis' (Blackwood's Magazine, 1826), seus escritos passaram a ser acolhidos por importantes revistas britânicas como Fraser's Magazine e The Metropolitan.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p173-174:autor-grattan",
        "tipo": "Evidencia",
        "titulo": "Dados biográficos de Thomas Colley Grattan (Anexo 3)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 173, "pagina_pdf_fim": 174, "pagina_impressa_inicio": 165, "pagina_impressa_fim": 166},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "Thomas Colley Grattan (1792-1864), nasceu em Dublin, Irlanda. Romancista, também escreveu relatos de viagens. Estudou direito mas dedicou-se à carreira literária. Amigo de Washington Irving, Lamartine e Thiers. Colaborador de vários periódicos britânicos como New Monthly Magazine, Edinburgh Review e Westminster Review. Exerceu o cargo de cônsul britânico em Massachusetts (EUA). Obras: Highways and Byways (1823); Traits of Travel (1829); The Heiress of Bruges (1831); Legends of the Rhine (1832).",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p182-183:autor-poole",
        "tipo": "Evidencia",
        "titulo": "Dados biográficos de John Poole (Anexo 3)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 182, "pagina_pdf_fim": 183, "pagina_impressa_inicio": 174, "pagina_impressa_fim": 175},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "John Poole (1786?-1872). Dramaturgo e escritor de contos e poemas. Ficou conhecido por suas farsas e comédias encenadas em Londres entre 1813 e 1829. Peça mais conhecida: Paul Pry (comédia em três atos, 1825). Colaborou assiduamente para a New Monthly Magazine. Participou com miscelâneas para Household Words (1850-1859), cujo editor era Charles Dickens. A tese registra (Anexo 3): 'Não existiu na Grã-Bretanha uma publicação intitulada Colburn's Magazine como indicado no Gabinete de Leitura.'",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    # Evidência para Baynes
    {
        "id": "evidence:soares:2006:pdf-p97-98:autor-baynes",
        "tipo": "Evidencia",
        "titulo": "Menção a Edward D. Baynes (Anexo 3 não tem verbete próprio)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 97, "pagina_pdf_fim": 98, "pagina_impressa_inicio": 89, "pagina_impressa_fim": 90},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "A tese menciona Edward D. Baynes apenas no corpo do Cap. 6.2: 'O autor de Sicilian Facts é Edward D. Baynes, sobre quem não se encontrou nenhuma informação biográfica a não ser a indicação de uma outra obra sua, Ovid's Epistles (1818).' Não há verbete próprio no Anexo 3.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    # Evidências sobre operações tradutórias (geral)
    {
        "id": "evidence:soares:2006:pdf-p129-130:liberdade-tradutora",
        "tipo": "Evidencia",
        "titulo": "Procedimentos tradutórios da época — liberdade do tradutor",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 129, "pagina_pdf_fim": 130, "pagina_impressa_inicio": 121, "pagina_impressa_fim": 122},
        "tipo_evidencia": "contexto_tradutorio",
        "conteudo": "A tese registra que os procedimentos tradutórios da época não se pautavam pela fidelidade ao texto original. Cita a tradutora brasileira de 'O Amor Materno': 'traduziremos, mas, com a liberdade de que usamos, iremos cortando ao original o que nos parecer inútil, desenvolvendo o que julgamos carecer de desenvolvimento, alterando o que achamos que para ser mais facilmente entendido deve ser alterado.' Cita também Justiniano José da Rocha (Jornal do Comércio, mar/1839): 'Será traduzida, será imitada, será original a novela que vos ofereço, leitor benévolo? Nem eu mesmo que a fiz vo-lo posso dizer.'",
        "citacao": None,
        "status_epistemologico": "documentado"
    }
]

# ---------- Nós ----------
nos = []

# Tese
nos.append({
    "id": "tese:soares:2006",
    "tipo": "Tese",
    "titulo": "Visão da Modernidade — A presença britânica no Gabinete de Leitura (1837-1838)",
    "aliases": ["Dissertação Maria Angélica Lau Pereira Soares"],
    "atributos": {
        "autora": "Maria Angélica Lau Pereira Soares",
        "ano": 2006,
        "instituicao": "USP / FFLCH / Departamento de Letras Modernas",
        "orientadora": "Sandra Guardini Teixeira Vasconcelos",
        "programa": "Pós-Graduação em Estudos Lingüísticos e Literários em Inglês"
    },
    "status_epistemologico": "documentado",
    "evidence_ids": [],
    "observacao": "Fonte primária deste grafo; seu conteúdo é a própria fonte de verdade. Por isso não possui evidence_ids (é a fonte)."
})

# Periodicos
nos.extend([
    {
        "id": "periodico:gabinete-de-leitura",
        "tipo": "Periodico",
        "titulo": "Gabinete de Leitura, Serões das Famílias Brasileiras, Jornal para todas as Classes, Sexos e Idades",
        "aliases": ["Gabinete de Leitura"],
        "atributos": {
            "local": "Rio de Janeiro",
            "periodo_inicio": "1837-08-13",
            "periodo_fim": "1838-04-08",
            "total_numeros": 35,
            "frequencia": "semanal (aos domingos)",
            "subscricao_anual_rs": 6000
        },
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"],
        "observacao": None
    },
    {
        "id": "periodico:o-chronista",
        "tipo": "Periodico",
        "titulo": "O Chronista",
        "aliases": ["O Chronista (1836-1839)"],
        "atributos": {
            "local": "Rio de Janeiro",
            "periodo_inicio": "1836",
            "periodo_fim": "1839",
            "frequencia": "bi-semanal em 1837 (qua/sáb); tri-semanal a partir de jan/1838 (ter/qui/sáb)"
        },
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete", "evidence:soares:2006:pdf-p12-13:livro-da-vida-republicacao-chronista"],
        "observacao": "Periódico irmão do Gabinete de Leitura, com o qual compartilha tipografia e redatores prováveis."
    },
    {
        "id": "periodico:new-monthly-magazine",
        "tipo": "Periodico",
        "titulo": "The New Monthly Magazine and Humorist",
        "aliases": ["The New Monthly and Literary Journal", "New Monthly Magazine"],
        "atributos": {
            "local": "Londres",
            "editores_relevantes": ["Edward Bulwer-Lytton (1831-1833)", "Theodore Hook (época de 1837)", "Henry Colburn (proprietário)"]
        },
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p103-111:costumes-comparacao", "evidence:soares:2006:pdf-p100-103:honras-comparacao", "evidence:soares:2006:pdf-p95-97:alibi-apresentacao"],
        "observacao": "Veículo original de Costumes Ingleses, As Honras Hereditárias e Álibi."
    },
    {
        "id": "periodico:blackwoods-magazine",
        "tipo": "Periodico",
        "titulo": "Blackwood's Magazine",
        "aliases": ["Blackwood Magazine"],
        "atributos": {"local": "Edimburgo / Londres"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"],
        "observacao": "Veículo original da série de cinco episódios incl. 'Davy Jones and the Yankee Privateer'."
    },
    {
        "id": "periodico:the-metropolitan",
        "tipo": "Periodico",
        "titulo": "The Metropolitan",
        "aliases": [],
        "atributos": {"local": "Londres"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"],
        "observacao": "Veículo original de 'Sicilian Facts'. Tese não fornece data específica de publicação."
    },
    {
        "id": "periodico:revue-britannique",
        "tipo": "Periodico",
        "titulo": "Revue Britannique",
        "aliases": [],
        "atributos": {"local": "Paris"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique", "evidence:soares:2006:pdf-p137-138:revue-britannique-le-cockney"],
        "observacao": "Intermediária documentada para sete dos dez textos do corpus; não figura como rota para O Testamento, As Honras Hereditárias e Costumes Ingleses (exceções explícitas da tese)."
    }
])

# Giftbooks
nos.extend([
    {
        "id": "giftbook:forget-me-not",
        "tipo": "Giftbook",
        "titulo": "Forget-me-Not; a Christmas and New Year's Present",
        "aliases": ["Forget-me-Not", "Forget me not"],
        "atributos": {
            "local": "Londres",
            "periodo": "1823-1847",
            "editor": "R. Ackermann",
            "diretor": "Frederic Shobel",
            "observacao_editorial": "Primeiro gift book inglês (1823); destinado principalmente ao público feminino; vendido próximo ao fim de ano como presente; principal atrativo eram as gravuras feitas por profissionais de renome."
        },
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p93-95:terencio-original"]
    },
    {
        "id": "giftbook:literary-souvenir",
        "tipo": "Giftbook",
        "titulo": "Literary Souvenir",
        "aliases": ["The Literary Souvenir"],
        "atributos": {
            "local": "Londres",
            "periodo": "1825-1835",
            "observacao_editorial": "Um dos annuals / gift books mais famosos da Inglaterra."
        },
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p98-99:manuscrito-original"]
    }
])

# Fascículos do Gabinete de Leitura (um por texto serializado no corpus)
# Apenas os fascículos do corpus são modelados; total no Gabinete: 35
fasciculos_data = [
    # (id_slug, numero, data_iso, papel, pertence_a_obra)
    ("gabinete:02:1837-08-20", 2, "1837-08-20", "publicacao", "work:uma-noite-no-mar"),
    ("gabinete:06:1837-09-17", 6, "1837-09-17", "publicacao", "work:o-livro-da-vida"),
    ("gabinete:08:1837-10-01", 8, "1837-10-01", "publicacao", "work:manuscrito-casa-loucos"),
    ("gabinete:09:1837-10-08", 9, "1837-10-08", "publicacao", "work:o-testamento"),
    ("gabinete:10:1837-10-15", 10, "1837-10-15", "publicacao", "work:o-sedutor-irving"),
    ("gabinete:11:1837-10-22", 11, "1837-10-22", "publicacao", "work:hereditary-honours"),
    ("gabinete:12:1837-10-29", 12, "1837-10-29", "publicacao", "work:alibi-grattan"),
    ("gabinete:14:1837-11-12", 14, "1837-11-12", "publicacao", "work:terence-oflaherty"),
    ("gabinete:30:1838-03-04", 30, "1838-03-04", "publicacao", "work:a-cockney-country-gentleman"),
    ("gabinete:31:1838-03-11", 31, "1838-03-11", "publicacao", "work:esbocos-sicilianos"),
    ("gabinete:32:1838-03-18", 32, "1838-03-18", "continua", "work:esbocos-sicilianos"),
    ("gabinete:33:1838-03-25", 33, "1838-03-25", "continua", "work:esbocos-sicilianos"),
    ("gabinete:34:1838-04-01", 34, "1838-04-01", "conclusao", "work:esbocos-sicilianos")
]
for slug, num, data, papel, obra_id in fasciculos_data:
    nos.append({
        "id": f"fasciculo:{slug}",
        "tipo": "Fasciculo",
        "titulo": f"Gabinete de Leitura n.{num} — {data}",
        "aliases": [],
        "atributos": {
            "numero": num,
            "data_iso": data,
            "veiculo": "Gabinete de Leitura",
            "papel": papel
        },
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p91-92:prosa-britanica-apresentacao"],
        "observacao": None
    })

# PublicacaoSerializada para Esboços Sicilianos
nos.append({
    "id": "serial:esbocos-sicilianos-no-gabinete",
    "tipo": "PublicacaoSerializada",
    "titulo": "Publicação serializada de Esboços Sicilianos no Gabinete de Leitura (n.31-34)",
    "aliases": [],
    "atributos": {
        "veiculo": "Gabinete de Leitura",
        "fasciculos": [31, 32, 33, 34],
        "periodo": "1838-03-11 a 1838-04-01"
    },
    "status_epistemologico": "documentado",
    "evidence_ids": ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"]
})

# Obras abstratas
obras_data = [
    {
        "id": "work:a-cockney-country-gentleman",
        "titulo": "A Cockney Country-Gentleman / Costumes Ingleses",
        "atributos": {
            "titulo_original": "A Cockney Country-Gentleman",
            "titulo_brasileiro": "Costumes Ingleses — Um Amador da Vida Campestre",
            "genero": "ficção / sátira social",
            "idioma_original": "en"
        },
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p103-111:costumes-comparacao"
    },
    {
        "id": "work:uma-noite-no-mar",
        "titulo": "Davy Jones and the Yankee Privateer / Uma Noite no Mar",
        "atributos": {
            "titulo_original": "Davy Jones and the Yankee Privateer",
            "titulo_brasileiro": "Uma Noite no Mar",
            "genero": "ficção / aventura marítima",
            "idioma_original": "en",
            "observacao": "Quarto episódio de uma série de cinco publicada na Blackwood's Magazine entre set/1829 e out/1830."
        },
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"
    },
    {
        "id": "work:o-testamento",
        "titulo": "O Testamento (obra abstrata)",
        "atributos": {
            "titulo_original": None,
            "titulo_brasileiro": "O Testamento",
            "genero": "ficção moral",
            "idioma_original": "en (presumido)",
            "observacao": "Original não localizado pela tese; atribuição a George Crabbe não confirmada por evidência externa; fonte declarada (Crabbe's Posthumous Works) inexistente."
        },
        "status": "problematico",
        "evidence_id": "evidence:soares:2006:pdf-p91-93:testamento-fonte-problematica"
    },
    {
        "id": "work:o-livro-da-vida",
        "titulo": "O Livro da Vida (obra abstrata)",
        "atributos": {
            "titulo_original": None,
            "titulo_brasileiro": "O Livro da Vida",
            "genero": "ficção fantástica / moral",
            "idioma_original": "en (presumido)",
            "observacao": "Original não localizado pela tese; fonte declarada (Retrospective Review) problemática; texto já havia sido publicado n'O Chronista em 1836."
        },
        "status": "problematico",
        "evidence_id": "evidence:soares:2006:pdf-p92-93:livro-da-vida-fonte-problematica"
    },
    {
        "id": "work:o-sedutor-irving",
        "titulo": "O Sedutor (Washington Irving) — obra abstrata",
        "atributos": {
            "titulo_original": None,
            "titulo_brasileiro": "O Sedutor",
            "genero": "ficção moralizante / viagem",
            "idioma_original": "en",
            "observacao": "Washington Irving é americano. A tese NÃO identifica título, veículo ou data de publicação original. Análise comparativa é feita com 'A Perjura' (brasileira) e 'O Vil Sedutor' (Semanario do Cincinnato), não com um original inglês."
        },
        "status": "nao_identificado",
        "evidence_id": "evidence:soares:2006:pdf-p55-58:sedutor-comparativo"
    },
    {
        "id": "work:manuscrito-casa-loucos",
        "titulo": "A Manuscript Found in a Madhouse / Manuscrito Achado em uma Casa de Loucos",
        "atributos": {
            "titulo_original": "A Manuscript Found in a Madhouse",
            "titulo_brasileiro": "Manuscrito Achado em uma Casa de Loucos",
            "genero": "ficção / grotesco",
            "idioma_original": "en"
        },
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p98-99:manuscrito-original"
    },
    {
        "id": "work:hereditary-honours",
        "titulo": "Hereditary Honours / As Honras Hereditárias",
        "atributos": {
            "titulo_original": "Hereditary Honours — A Tale of Love and Mystery",
            "titulo_brasileiro": "As Honras Hereditárias — História de Amor, de Mistério e de Filosofia",
            "genero": "ficção / sátira social / ironia",
            "idioma_original": "en"
        },
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p100-103:honras-comparacao"
    },
    {
        "id": "work:terence-oflaherty",
        "titulo": "Terence O'Flaherty / Terêncio o Alfaiate",
        "atributos": {
            "titulo_original": "Terence O'Flaherty",
            "titulo_brasileiro": "Terêncio o Alfaiate",
            "genero": "ficção humorística / ironia narrativa",
            "idioma_original": "en",
            "observacao": "Original assinado por 'A Modern Pythagorean', pseudônimo de Robert Macnish."
        },
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p93-95:terencio-original"
    },
    {
        "id": "work:alibi-grattan",
        "titulo": "The Alibi / Álibi",
        "atributos": {
            "titulo_original": "The Alibi; an Assize Anedocte",
            "titulo_brasileiro": "Álibi",
            "genero": "ficção / crítica social / ironia",
            "idioma_original": "en",
            "observacao": "Autor irlandês; crítica ao sistema judiciário irlandês e ao 'modo de ser dos irlandeses'."
        },
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p95-97:alibi-apresentacao"
    },
    {
        "id": "work:esbocos-sicilianos",
        "titulo": "Sicilian Facts / Esboços Sicilianos",
        "atributos": {
            "titulo_original": "Sicilian Facts",
            "titulo_brasileiro": "Esboços Sicilianos",
            "genero": "coletânea de narrativas / gótico / exotismo",
            "idioma_original": "en",
            "observacao": "Texto inglês é uma longa coletânea de pequenas narrativas independentes; o Gabinete publicou apenas duas histórias (a primeira com prólogo+história completa, a segunda dividida em duas partes, e uma terceira em parte única)."
        },
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"
    }
]
for o in obras_data:
    ev_id = o.pop("evidence_id")
    status = o.pop("status")
    nos.append({
        "id": o["id"],
        "tipo": "ObraAbstrata",
        "titulo": o["titulo"],
        "aliases": [],
        "atributos": o["atributos"],
        "status_epistemologico": status,
        "evidence_ids": [ev_id],
        "observacao": None
    })

# Manifestações (originais e brasileiras)
manifestacoes_data = [
    # Costumes Ingleses
    {
        "id": "manifestation:en:new-monthly:cockney-country-gentleman:1837-06",
        "titulo": "A Cockney Country-Gentleman (The New Monthly Magazine and Humorist, jun/1837)",
        "atributos": {"idioma": "en", "veiculo": "The New Monthly Magazine and Humorist", "data_publicacao": "1837-06", "editor_epoca": "Theodore Hook", "assinatura": "P*"},
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p103-111:costumes-comparacao"
    },
    {
        "id": "manifestation:fr:revue-britannique:le-cockney-campagnard:1838-02",
        "titulo": "Le Cockney Campagnard (Revue Britannique, fev/1838)",
        "atributos": {"idioma": "fr", "veiculo": "Revue Britannique", "data_publicacao": "1838-02"},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p137-138:revue-britannique-le-cockney",
        "observacao": "Versão francesa existe, mas a tese afirma expressamente que a versão brasileira NÃO é tradução desta versão francesa."
    },
    {
        "id": "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04",
        "titulo": "Costumes Ingleses — Um Amador da Vida Campestre (Gabinete de Leitura n.30, 04/03/1838)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao": "1838-03-04", "numero_fasciculo": 30, "paginas_periodico": "233-236", "tradutor": None},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p103-111:costumes-comparacao"
    },
    # Uma Noite no Mar
    {
        "id": "manifestation:en:blackwoods:davy-jones:1830-07",
        "titulo": "Davy Jones and the Yankee Privateer (Blackwood's Magazine, jul/1830)",
        "atributos": {"idioma": "en", "veiculo": "Blackwood's Magazine", "data_publicacao": "1830-07", "parte_serie": "4 de 5"},
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"
    },
    {
        "id": "manifestation:pt-br:gabinete:uma-noite-no-mar:1837-08-20",
        "titulo": "Uma Noite no Mar (Gabinete de Leitura n.2, 20/08/1837)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao": "1837-08-20", "numero_fasciculo": 2, "paginas_periodico": "13-15", "tradutor": None},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"
    },
    # O Testamento — só versão brasileira, original não identificado
    {
        "id": "manifestation:pt-br:gabinete:testamento:1837-10-08",
        "titulo": "O Testamento (Gabinete de Leitura n.9, 08/10/1837)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao": "1837-10-08", "numero_fasciculo": 9, "paginas_periodico": "69-71", "tradutor": None},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p91-93:testamento-fonte-problematica"
    },
    # O Livro da Vida — só versão brasileira, original não identificado; mas há republicação no Chronista
    {
        "id": "manifestation:pt-br:gabinete:livro-da-vida:1837-09-17",
        "titulo": "O Livro da Vida (Gabinete de Leitura n.6, 17/09/1837)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao": "1837-09-17", "numero_fasciculo": 6, "paginas_periodico": "43-46", "tradutor": None},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p92-93:livro-da-vida-fonte-problematica"
    },
    {
        "id": "manifestation:pt-br:chronista:livro-da-vida:1836-10",
        "titulo": "O Livro da Vida (O Chronista, out/1836)",
        "atributos": {"idioma": "pt-br", "veiculo": "O Chronista", "data_publicacao": "1836-10", "publicacoes": ["n.3 05/10/1836", "n.6 15/10/1836", "n.7 19/10/1836"], "secao": "Variedades"},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p12-13:livro-da-vida-republicacao-chronista",
        "observacao": "Primeira publicação do texto, antes da republicação no Gabinete."
    },
    # O Sedutor — só versão brasileira, original não identificado
    {
        "id": "manifestation:pt-br:gabinete:sedutor:1837-10-15",
        "titulo": "O Sedutor (Gabinete de Leitura n.10, 15/10/1837)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao": "1837-10-15", "numero_fasciculo": 10, "paginas_periodico": "73-75", "tradutor": None, "autor_assinado": "Washington Irving"},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p55-58:sedutor-comparativo"
    },
    # Manuscrito
    {
        "id": "manifestation:en:literary-souvenir:manuscript-madhouse:1829",
        "titulo": "A Manuscript Found in a Madhouse (Literary Souvenir 1829)",
        "atributos": {"idioma": "en", "veiculo": "Literary Souvenir", "data_publicacao": "1829", "nota_autoria": "by the author of Pelham (Edward Bulwer-Lytton)"},
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p98-99:manuscrito-original"
    },
    {
        "id": "manifestation:pt-br:gabinete:manuscrito-casa-loucos:1837-10-01",
        "titulo": "Manuscrito Achado em uma Casa de Loucos (Gabinete de Leitura n.8, 01/10/1837)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao": "1837-10-01", "numero_fasciculo": 8, "paginas_periodico": "59-60", "tradutor": None},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p98-99:manuscrito-original"
    },
    # Honras Hereditárias
    {
        "id": "manifestation:en:new-monthly:hereditary-honours:1832",
        "titulo": "Hereditary Honours — A Tale of Love and Mystery (The New Monthly and Literary Journal, 1832)",
        "atributos": {"idioma": "en", "veiculo": "The New Monthly and Literary Journal", "data_publicacao": "1832", "editor_epoca": "Edward Bulwer-Lytton (editor 1831-1833)"},
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p100-103:honras-comparacao"
    },
    {
        "id": "manifestation:pt-br:gabinete:as-honras-hereditarias:1837-10-22",
        "titulo": "As Honras Hereditárias (Gabinete de Leitura n.11, 22/10/1837)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao": "1837-10-22", "numero_fasciculo": 11, "paginas_periodico": "81-83", "tradutor": None, "autor_assinado": "G. L. Bulwer"},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p100-103:honras-comparacao"
    },
    # Terêncio
    {
        "id": "manifestation:en:forget-me-not:terence-oflaherty:1829",
        "titulo": "Terence O'Flaherty (Forget-me-Not para 1829)",
        "atributos": {"idioma": "en", "veiculo": "Forget-me-Not", "data_publicacao": "1829", "assinatura": "A Modern Pythagorean / The Modern Pythagorean (Robert Macnish)"},
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p93-95:terencio-original"
    },
    {
        "id": "manifestation:pt-br:gabinete:terencio-alfaiate:1837-11-12",
        "titulo": "Terêncio o Alfaiate (Gabinete de Leitura n.14, 12/11/1837)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao": "1837-11-12", "numero_fasciculo": 14, "paginas_periodico": "110-112", "tradutor": None},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p93-95:terencio-original"
    },
    # Álibi
    {
        "id": "manifestation:en:new-monthly:alibi:1836-02",
        "titulo": "The Alibi; an Assize Anedocte (New Monthly Magazine and Literary Journal, fev/1836)",
        "atributos": {"idioma": "en", "veiculo": "New Monthly Magazine and Literary Journal", "data_publicacao": "1836-02", "nota_autoria": "by the author of Highways and Byways (Thomas Colley Grattan)"},
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p95-97:alibi-apresentacao"
    },
    {
        "id": "manifestation:pt-br:gabinete:alibi:1837-10-29",
        "titulo": "Álibi (Gabinete de Leitura n.12, 29/10/1837)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao": "1837-10-29", "numero_fasciculo": 12, "paginas_periodico": "89-91", "tradutor": None, "nota_esclarecedora": "Ausência do indiciado do lugar onde foi cometido o crime de que é acusado, no tempo em que teve lugar."},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p95-97:alibi-apresentacao"
    },
    # Esboços Sicilianos
    {
        "id": "manifestation:en:metropolitan:sicilian-facts",
        "titulo": "Sicilian Facts (The Metropolitan)",
        "atributos": {"idioma": "en", "veiculo": "The Metropolitan", "data_publicacao": None, "autor": "Edward D. Baynes"},
        "status": "identificado",
        "evidence_id": "evidence:soares:2006:pdf-p97-98:esbocos-apresentacao",
        "observacao": "Tese não fornece data específica de publicação original."
    },
    {
        "id": "manifestation:pt-br:gabinete:esbocos-sicilianos:1838-03-11-a-04-01",
        "titulo": "Esboços Sicilianos (Gabinete de Leitura n.31-34, 11/03/1838 a 01/04/1838)",
        "atributos": {"idioma": "pt-br", "veiculo": "Gabinete de Leitura", "data_publicacao_inicio": "1838-03-11", "data_publicacao_fim": "1838-04-01", "fasciculos": [31, 32, 33, 34], "paginas_periodico": "246-247, 253-254, 260-261, 270-271", "tradutor": None},
        "status": "documentado",
        "evidence_id": "evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"
    }
]
for m in manifestacoes_data:
    ev_id = m.pop("evidence_id")
    status = m.pop("status")
    obs = m.pop("observacao", None)
    nos.append({
        "id": m["id"],
        "tipo": "ManifestacaoTextual",
        "titulo": m["titulo"],
        "aliases": [],
        "atributos": m["atributos"],
        "status_epistemologico": status,
        "evidence_ids": [ev_id],
        "observacao": obs
    })

# Pessoas (autores)
pessoas_data = [
    {
        "id": "person:john-poole",
        "titulo": "John Poole",
        "atributos": {"nascimento": "1786?", "falecimento": "1872", "nacionalidade": "britânica", "atividade": "Dramaturgo e escritor de contos e poemas", "obras_relevantes": ["Paul Pry (1825)", "Hamlet Travestie (1810)"], "colaboracao": "New Monthly Magazine; Household Words (1850-1859, editor: Charles Dickens)"},
        "evidence_id": "evidence:soares:2006:pdf-p182-183:autor-poole"
    },
    {
        "id": "person:edward-bulwer-lytton",
        "titulo": "Edward Bulwer-Lytton",
        "atributos": {"nascimento": "1803", "falecimento": "1873", "nacionalidade": "britânica", "atividade": "Membro do parlamento; romancista, dramaturgo, poeta, crítico literário", "editor_new_monthly": "1831-1833", "obras_relevantes": ["Pelham (1828)", "Paul Clifford (1830)", "Eugene Aram (1833)", "The Last Days of Pompeii (1834)", "The Caxtons (1849)"]},
        "evidence_id": "evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton"
    },
    {
        "id": "person:george-crabbe",
        "titulo": "George Crabbe",
        "atributos": {"nascimento": "1754", "falecimento": "1832", "nacionalidade": "britânica", "atividade": "Poeta realista; algum trabalho em prosa", "obras_relevantes": ["The Village (1783)", "The Borough (1810)", "Tales in Verse (1812)", "Tales of the Hall (1819)"], "observacao": "Atribuição de 'O Testamento' a Crabbe não confirmada por evidência externa; fonte declarada 'Crabbe's Posthumous Works' inexistente."},
        "evidence_id": "evidence:soares:2006:pdf-p171-172:autor-crabbe"
    },
    {
        "id": "person:washington-irving",
        "titulo": "Washington Irving",
        "atributos": {"nascimento": "1783-04-03", "falecimento": "1859", "nacionalidade": "americana", "atividade": "Escritor de contos, ensaios, poesia, biografia; colunista; livros de viagem", "obras_relevantes": ["The Sketch Book Of Geoffrey Crayon, Gent. (1819-20)", "Bracebridge Hall (1822)", "Columbus (1828)", "Alhambra (1832)", "The Legend of Sleepy Hollow", "Rip Van Winkle"], "observacao": "Primeiro escritor americano a alcançar renome internacional. Incluído no corpus britânico por sua presença como autor de língua inglesa no Gabinete."},
        "evidence_id": "evidence:soares:2006:pdf-p175-176:autor-irving"
    },
    {
        "id": "person:robert-macnish",
        "titulo": "Robert Macnish",
        "atributos": {"nascimento": "1802", "falecimento": "1837", "nacionalidade": "britânica (escocesa)", "atividade": "Médico e escritor de ficção fantástica/grotesca", "obras_relevantes": ["Anatomy of Drunkness (divergência interna da tese: 1824 no corpo / 1827 no Anexo 3)", "The Philosophy of Sleep (1830)", "The Metempsychosis (Blackwood's Magazine, 1826)"], "pseudonimo": "A Modern Pythagorean / The Modern Pythagorean"},
        "evidence_id": "evidence:soares:2006:pdf-p179-180:autor-macnish"
    },
    {
        "id": "person:thomas-colley-grattan",
        "titulo": "Thomas Colley Grattan",
        "atributos": {"nascimento": "1792", "falecimento": "1864", "nacionalidade": "irlandesa", "atividade": "Romancista, escritor de relatos de viagens, cônsul britânico em Massachusetts", "obras_relevantes": ["Highways and Byways (1823)", "Traits of Travel (1829)", "The Heiress of Bruges (1831)", "Legends of the Rhine (1832)"], "amizades": ["Washington Irving", "Lamartine", "Thiers"]},
        "evidence_id": "evidence:soares:2006:pdf-p173-174:autor-grattan"
    },
    {
        "id": "person:edward-d-baynes",
        "titulo": "Edward D. Baynes",
        "atributos": {"nascimento": None, "falecimento": None, "nacionalidade": "britânica (presumida)", "atividade": "Escritor", "obras_relevantes": ["Sicilian Facts", "Ovid's Epistles (1818)"], "observacao": "A tese registra: 'sobre quem não se encontrou nenhuma informação biográfica a não ser a indicação de uma outra obra sua, Ovid's Epistles (1818)'. Não há verbete próprio no Anexo 3."},
        "evidence_id": "evidence:soares:2006:pdf-p97-98:autor-baynes"
    }
]
for p in pessoas_data:
    ev_id = p.pop("evidence_id")
    nos.append({
        "id": p["id"],
        "tipo": "Pessoa",
        "titulo": p["titulo"],
        "aliases": [],
        "atributos": p["atributos"],
        "status_epistemologico": "documentado",
        "evidence_ids": [ev_id],
        "observacao": None
    })

# FonteDeclarada — apenas as problemáticas/diferenciadas
fontes_declaradas = [
    {
        "id": "fontedeclarada:colburns-magazine",
        "titulo": "Colburn's Magazine (referência declarada no Gabinete)",
        "atributos": {
            "referencia_original": "Colburn's Magazine",
            "veiculo_existente": False,
            "observacao": "A tese afirma: 'Não existiu na Grã-Bretanha uma publicação intitulada Colburn's Magazine como indicado no Gabinete de Leitura.' Provável confusão com Henry Colburn, proprietário da New Monthly Magazine na época.",
            "vinculo_real": "Henry Colburn (proprietário da New Monthly Magazine)"
        },
        "evidence_id": "evidence:soares:2006:pdf-p103-111:costumes-comparacao"
    },
    {
        "id": "fontedeclarada:crabbe-posthumous-works",
        "titulo": "Crabbe's Posthumous Works (referência declarada no Gabinete)",
        "atributos": {
            "referencia_original": "Crabbe's POSTHUMOUS WORKS",
            "veiculo_existente": False,
            "observacao": "A tese registra (Anexo 3, verbete George Crabbe): 'Não houve publicação com o título indicado.'"
        },
        "evidence_id": "evidence:soares:2006:pdf-p91-93:testamento-fonte-problematica"
    },
    {
        "id": "fontedeclarada:retrospective-review",
        "titulo": "Retrospective Review (referência declarada no Gabinete)",
        "atributos": {
            "referencia_original": "Retrospective Review",
            "veiculo_existente": True,
            "observacao": "A revista existia mas se dedicava a resenhas críticas e não publicava narrativas completas, apenas citações de trechos das obras analisadas. Portanto, não pode ter sido a fonte de uma narrativa completa."
        },
        "evidence_id": "evidence:soares:2006:pdf-p92-93:livro-da-vida-fonte-problematica"
    }
]
for fd in fontes_declaradas:
    ev_id = fd.pop("evidence_id")
    nos.append({
        "id": fd["id"],
        "tipo": "FonteDeclarada",
        "titulo": fd["titulo"],
        "aliases": [],
        "atributos": fd["atributos"],
        "status_epistemologico": "problematico",
        "evidence_ids": [ev_id],
        "observacao": None
    })

# Operações tradutórias — são nós E entradas separadas em operacoes_tradutorias
operacoes_data = [
    {
        "id": "op:costumes:atenuacao-ironia-fieldlove",
        "tipo": "OperacaoTradutoria",
        "titulo": "Atenuação da ironia sobre Fieldlove",
        "tipo_operacao": "ATENUACAO_DE_IRONIA",
        "obra_id": "work:a-cockney-country-gentleman",
        "manifestacoes_comparadas": ["manifestation:en:new-monthly:cockney-country-gentleman:1837-06", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04"],
        "trecho_original": "That, indeed, was nearly all he could do; but, since nothing more was required of him, the satisfaction of the 'firm' is not to be wondered at. The march of his intellect had certainly not kept pace with the progress of his hand; and, if it marched at all, it was, to say the most of it, to the tune of a very slow march.",
        "trecho_brasileiro": "Foi assim que Fieldlove chegou aos 21 anos. Os cinco anos de seu noviciado se haviam passado com grande satisfação dos snrs. Bags, Bales & Co. Graças a um trabalho infatigável, sua mão tinha-se consideravelmente melhorado; podia tirar uma conta com admirável celeridade, fazer uma fatura ou conhecimento digno (sic) dos elogios do caixeiro principal.",
        "efeito_textual": "Supressão do adjetivo 'monótono' (que qualificava o trabalho) e do comentário irônico do narrador sobre a limitação intelectual de Fieldlove. A versão brasileira registra apenas os aspectos positivos (não esmorecimento, progresso na escrita, conhecimento prático, satisfação dos empregadores) e omite os negativos (trabalho incessante e monótono, baixas expectativas, falta de progresso intelectual).",
        "efeito_interpretativo": "A versão brasileira reduz o caráter caricatural e crítico do personagem, transformando-o de homem comum e pouco inteligente em rapaz trabalhador que alcança mérito por esforço.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p106-107:costumes-atenuacao-ironia"],
        "observacao": None
    },
    {
        "id": "op:costumes:modificacao-trabalho-rural",
        "tipo": "OperacaoTradutoria",
        "titulo": "Modificação na representação do trabalho rural",
        "tipo_operacao": "MODIFICACAO_REPRESENTACAO_TRABALHO",
        "obra_id": "work:a-cockney-country-gentleman",
        "manifestacoes_comparadas": ["manifestation:en:new-monthly:cockney-country-gentleman:1837-06", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04"],
        "trecho_original": "He has plenty do to, replied the curate. He has a vast estate, upon which he was born, the management of which is in his own hands; he has a large tenantry, who, from his long residence among them, look up to him as their guardian and protector; then, he is a magistrate, and has to attend quarter-sessions, besides doing justice-business here; then he has a large circle of acquaintances about him...",
        "trecho_brasileiro": "Estes senhores estão habituados desde a infância a uma elegância preguiçosa, que, graças a Deus, vós não conhecestes. A caça e a pesca tinham encantos para vós porque vos divertiam de vossas ordinárias ocupações.",
        "efeito_textual": "Substituição da fala do cura, que no original descreve a vida ativa do proprietário rural (gestão da propriedade, magistratura, sessões, círculo de conhecidos), por uma fala que descreve a 'elegância preguiçosa' dos proprietários rurais.",
        "efeito_interpretativo": "Enquanto o original ironiza a percepção distorcida do urbano Fieldlove sobre o campo (lugar aprazível onde se caça e pesca longe da cidade), a versão brasileira confirma o discurso inicial de Mr. Urby ('para gozar da vida do campo ou da cidade é mister ter sido educado para isso'), diluindo o tom crítico sobre a adaptação do indivíduo ao meio.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p108-109:costumes-modificacao-trabalho-rural"],
        "observacao": None
    },
    {
        "id": "op:costumes:alteracao-desfecho-positivo",
        "tipo": "OperacaoTradutoria",
        "titulo": "Alteração de desfecho irônico para encerramento mais positivo",
        "tipo_operacao": "ALTERACAO_DE_DESECHO",
        "obra_id": "work:a-cockney-country-gentleman",
        "manifestacoes_comparadas": ["manifestation:en:new-monthly:cockney-country-gentleman:1837-06", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04"],
        "trecho_original": "Behold him, now, established in a comfortable house in Blooms-bury-square; visiting, or receiving the visits of, his old friends and acquaintances; indulging sometimes at the Opera, a concert, or a play; and passing his life agreeably, because in the manner for which habit had qualified him... And he has been heard to declare that, upon striking the balance, he is convinced that that is the only mode in which a confirmed Londoner can truly enjoy the life of — a COUNTRY GENTLEMAN.",
        "trecho_brasileiro": "Voltou para Londres, e continuou, não seus negócios, mas suas relações. Sua honra proporcionou-lhe consideração, e muita gente apreciando sua inteligência quando lhe pediam conselhos, ou a grandeza de sua generosidade quando reclamavam seus serviços, deram-lhe seus sufrágios para importantes cargos da administração da cidade, e talvez que, se Deus lhe der vida, se realize a profecia de seu tio Urby: talvez seja Lord Maire.",
        "efeito_textual": "No original inglês, o retorno de Fieldlove a Londres confirma seus limitados horizontes e caráter acrítico (repete o discurso do tio Urby sobre o hábito — trecho omitido na versão brasileira). Na versão brasileira, o desfecho é positivo: Fieldlove é honrado, inteligente e generoso, recebe votos para cargos públicos, e talvez se torne Lord Mayor.",
        "efeito_interpretativo": "A versão brasileira confere a Fieldlove 'certos contornos' que, sem dar-lhe profundidade psicológica, lhe conferem desenvolvimento, em contraste com o personagem completamente plano e caricatural do original. As alterações adequaram a narrativa à visão que os primeiros homens de letras brasileiros tinham da sociedade britânica como modelo a ser seguido.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p109-111:costumes-alteracao-desfecho"],
        "observacao": None
    },
    {
        "id": "op:honras:supressao-gesto-caracterizador",
        "tipo": "OperacaoTradutoria",
        "titulo": "Supressão do gesto caracterizador do protagonista",
        "tipo_operacao": "SUPRESSAO_GESTO_CARACTERIZADOR",
        "obra_id": "work:hereditary-honours",
        "manifestacoes_comparadas": ["manifestation:en:new-monthly:hereditary-honours:1832", "manifestation:pt-br:gabinete:as-honras-hereditarias:1837-10-22"],
        "trecho_original": "[O narrador descreve a tentativa desajeitada do protagonista de fazer um gesto de carinho, quase acertando um soco no rosto da heroína.]",
        "trecho_brasileiro": "[A versão do Gabinete de Leitura não traz a frase; registra apenas a reação de espanto da jovem, seguida do rapaz chamá-la de 'celeste criatura' e ela ser acometida de terror.]",
        "efeito_textual": "A versão brasileira omite a descrição do gesto desajeitado do protagonista (que quase acerta um soco no rosto da heroína ao tentar fazer um gesto cortês), registrando apenas a reação de espanto da jovem.",
        "efeito_interpretativo": "Ao suprimir o gesto, a versão brasileira compromete a coerência dos eventos: o leitor não entende a causa do espanto da heroína. A tese observa que não se pode descartar uma falha de impressão, dadas as condições precárias dos periódicos da época.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p101-102:honras-supressao-gesto"],
        "observacao": "A tese ressalva a possibilidade de falha de impressão, mas registra a divergência como operação."
    },
    {
        "id": "op:honras:especificacao-espaco-narrativo",
        "tipo": "OperacaoTradutoria",
        "titulo": "Especificação do espaço narrativo antes ambíguo",
        "tipo_operacao": "ESPECIFICACAO_ESPACO_NARRATIVO",
        "obra_id": "work:hereditary-honours",
        "manifestacoes_comparadas": ["manifestation:en:new-monthly:hereditary-honours:1832", "manifestation:pt-br:gabinete:as-honras-hereditarias:1837-10-22"],
        "trecho_original": "There is a certain country, not very far distant from our own: in a certain small town, close to the metropolis of this country, there once lived a certain young lady, of the name of Laura.",
        "trecho_brasileiro": "Em uma cidade pequena vizinha da metrópole britânica, vivia uma moça que se chamava Laura.",
        "efeito_textual": "A expressão 'this country' do original foi traduzida literalmente como 'metrópole britânica' na versão brasileira, eliminando a ambiguidade deliberada criada pela estruturação do original ('a certain country' / 'this country' / 'from our own').",
        "efeito_interpretativo": "A ambiguidade do original acentua o tom irônico do narrador ao criticar a estrutura de classes da sociedade inglesa. Ao especificar 'britânica', a versão brasileira perde essa ambiguidade e o caráter crítico se atenua.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p102-103:honras-especificacao-espaco"],
        "observacao": None
    },
    {
        "id": "op:alibi:supressao-critica-irlandeses",
        "tipo": "OperacaoTradutoria",
        "titulo": "Supressão da crítica ao 'modo de ser dos irlandeses'",
        "tipo_operacao": "SUPRESSAO_CRITICA_CULTURAL",
        "obra_id": "work:alibi-grattan",
        "manifestacoes_comparadas": ["manifestation:en:new-monthly:alibi:1836-02", "manifestation:pt-br:gabinete:alibi:1837-10-29"],
        "trecho_original": "[Trecho extenso com Mr. Mulligan, Tim Carney, Dinnis Murphy, etc., reproduzindo o dialeto irlandês e a crítica irônica do narrador ao 'modo de ser dos irlandeses', incluindo a passagem: 'But the division of idleness is a too well established principle of political economy in Ireland to run any risk of being violated, by any one individual doing any thing that isn’t his place.']",
        "trecho_brasileiro": "O estalajadeiro das Armas de Flaherty era talvez neste momento o homem mais ocupado da cidade. Sua casa estava cheia de estrangeiros, e ele se esforçava, com o vigilante olhar do dono, por manter uma aparência de ordem no meio da confusão que aí reinava. A sineta da porta exterior da estalagem soou-lhe aos ouvidos, uma e mais vezes, e foi o sinal dum chuveiro de injúrias irlandesas, com que messer Mulligan mimoseou todos os seus criados, machos e fêmeas, moços e velhos... Com todos os diabos! andem todos ao mesmo tempo, andem ... Ah ! que inferno aturar esta gente !",
        "efeito_textual": "A versão brasileira resume drasticamente as imprecações do senhorio e omite o longo diálogo com os empregados (no qual se reproduzia o dialeto irlandês). A crítica explícita do narrador ao 'modo de ser dos irlandeses' desaparece do texto brasileiro.",
        "efeito_interpretativo": "Há ao mesmo tempo um enxugamento do texto (que torna o enredo mais ágil) e uma alteração sensível da forma narrativa, com a supressão das intervenções críticas do narrador. A tese ressalta que esses procedimentos ocorrem em escala ainda mais acentuada em 'O Amador da Vida Campestre' (Costumes Ingleses).",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p132-134:alibi-comparacao"],
        "observacao": None
    },
    {
        "id": "op:esbocos:supressao-nota-punicao-moral",
        "tipo": "OperacaoTradutoria",
        "titulo": "Supressão da nota sobre punição moral e consciência culpada",
        "tipo_operacao": "SUPRESSAO_NOTA_MORAL",
        "obra_id": "work:esbocos-sicilianos",
        "manifestacoes_comparadas": ["manifestation:en:metropolitan:sicilian-facts", "manifestation:pt-br:gabinete:esbocos-sicilianos:1838-03-11-a-04-01"],
        "trecho_original": "It will be observed, that in most of the events related, notwithstanding the power of the offenders, and their impunity from any earthly tribunal, a severe retribution has taken place, and moral justice been satisfied even in this state. In the instances where this is not perceptible, it is to be recollected that they have been left to the acute reproaches of a guilty conscience — perhaps the severest of punishments.",
        "trecho_brasileiro": "[A versão brasileira não faz nenhuma referência à possível punição moral dos criminosos.]",
        "efeito_textual": "A versão brasileira omite a nota do prólogo do original inglês que assegura aos leitores vitorianos que os culpados receberam alguma forma de punição (seja terrena, seja pela 'consciência culposa').",
        "efeito_interpretativo": "A omissão intensifica a crítica a uma sociedade na qual a Justiça somente pune os pequenos e humildes — crítica que se torna mais aguda quando não há mais a garantia de punição moral para os poderosos.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p98:esbocos-supressao-nota-punicao"],
        "observacao": None
    }
]
# As operações também são nós do grafo (para permitir SUSTENTA/AFETA)
for op in operacoes_data:
    nos.append({
        "id": op["id"],
        "tipo": "OperacaoTradutoria",
        "titulo": op["titulo"],
        "aliases": [],
        "atributos": {
            "tipo_operacao": op["tipo_operacao"],
            "obra_id": op["obra_id"],
            "manifestacoes_comparadas": op["manifestacoes_comparadas"]
        },
        "status_epistemologico": op["status_epistemologico"],
        "evidence_ids": op["evidence_ids"],
        "observacao": op["observacao"]
    })

# Locais
nos.extend([
    {"id": "local:rio-de-janeiro", "tipo": "Local", "titulo": "Rio de Janeiro", "aliases": ["corte do Rio de Janeiro"], "atributos": {"pais": "Brasil", "papel": "local de publicação do Gabinete de Leitura e O Chronista"}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], "observacao": None},
    {"id": "local:londres", "tipo": "Local", "titulo": "Londres", "aliases": [], "atributos": {"pais": "Grã-Bretanha", "papel": "local de publicação de New Monthly Magazine, Forget-me-Not, Literary Souvenir, The Metropolitan"}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p103-111:costumes-comparacao"], "observacao": None},
    {"id": "local:paris", "tipo": "Local", "titulo": "Paris", "aliases": [], "atributos": {"pais": "França", "papel": "local de publicação da Revue Britannique"}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"], "observacao": None}
])

# ---------- Arestas ----------
arestas = []

def add_edge(edge_id, origem, destino, tipo, status, evidence_ids=None, qualificador=None, observacao=None, justificativa=None):
    arestas.append({
        "id": f"edge:{edge_id.replace(':', '-')}",
        "origem": origem,
        "destino": destino,
        "tipo": tipo,
        "status_epistemologico": status,
        "qualificador": qualificador,
        "evidence_ids": evidence_ids or [],
        "observacao": observacao,
        "justificativa": justificativa
    })

# AUTOR_DE — Pessoa -> ObraAbstrata
add_edge("poole-autor-cockney", "person:john-poole", "work:a-cockney-country-gentleman", "AUTOR_DE", "identificado", ["evidence:soares:2006:pdf-p103-111:costumes-comparacao"], observacao="Assinatura 'P*' identificada como John Poole.")
add_edge("bulwer-autor-manuscrito", "person:edward-bulwer-lytton", "work:manuscrito-casa-loucos", "AUTOR_DE", "identificado", ["evidence:soares:2006:pdf-p98-99:manuscrito-original"], observacao="Identificado pela nota 'by the author of Pelham'.")
add_edge("bulwer-autor-honras", "person:edward-bulwer-lytton", "work:hereditary-honours", "AUTOR_DE", "identificado", ["evidence:soares:2006:pdf-p100-103:honras-comparacao"])
add_edge("macnish-autor-terencio", "person:robert-macnish", "work:terence-oflaherty", "AUTOR_DE", "identificado", ["evidence:soares:2006:pdf-p93-95:terencio-original"], observacao="Pseudônimo 'A Modern Pythagorean'.")
add_edge("grattan-autor-alibi", "person:thomas-colley-grattan", "work:alibi-grattan", "AUTOR_DE", "identificado", ["evidence:soares:2006:pdf-p95-97:alibi-apresentacao"], observacao="Identificado pela nota 'by the author of Highways and Byways'.")
add_edge("baynes-autor-esbocos", "person:edward-d-baynes", "work:esbocos-sicilianos", "AUTOR_DE", "identificado", ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"])
add_edge("irving-autor-sedutor", "person:washington-irving", "work:o-sedutor-irving", "AUTOR_DE", "documentado", ["evidence:soares:2006:pdf-p55-58:sedutor-comparativo"])
# Crabbe: atribuição problemática — qualificador distinto
add_edge("crabbe-atribuicao-testamento", "person:george-crabbe", "work:o-testamento", "AUTOR_DE", "problematico", ["evidence:soares:2006:pdf-p91-93:testamento-fonte-problematica"], qualificador="atribuicao_nao_confirmada", observacao="Atribuição feita pelo Gabinete de Leitura; original não localizado pela tese; fonte declarada (Crabbe's Posthumous Works) inexistente.")
# O Livro da Vida: sem autor identificado

# MANIFESTA — Obra -> ManifestacaoTextual
add_edge("cockney-manifesta-en", "work:a-cockney-country-gentleman", "manifestation:en:new-monthly:cockney-country-gentleman:1837-06", "MANIFESTA", "identificado", ["evidence:soares:2006:pdf-p103-111:costumes-comparacao"])
add_edge("cockney-manifesta-fr", "work:a-cockney-country-gentleman", "manifestation:fr:revue-britannique:le-cockney-campagnard:1838-02", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p137-138:revue-britannique-le-cockney"])
add_edge("cockney-manifesta-pt", "work:a-cockney-country-gentleman", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p103-111:costumes-comparacao"])

add_edge("davy-manifesta-en", "work:uma-noite-no-mar", "manifestation:en:blackwoods:davy-jones:1830-07", "MANIFESTA", "identificado", ["evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"])
add_edge("davy-manifesta-pt", "work:uma-noite-no-mar", "manifestation:pt-br:gabinete:uma-noite-no-mar:1837-08-20", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"])

add_edge("testamento-manifesta-pt", "work:o-testamento", "manifestation:pt-br:gabinete:testamento:1837-10-08", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p91-93:testamento-fonte-problematica"])

add_edge("livro-manifesta-pt-gabinete", "work:o-livro-da-vida", "manifestation:pt-br:gabinete:livro-da-vida:1837-09-17", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p92-93:livro-da-vida-fonte-problematica"])
add_edge("livro-manifesta-pt-chronista", "work:o-livro-da-vida", "manifestation:pt-br:chronista:livro-da-vida:1836-10", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p12-13:livro-da-vida-republicacao-chronista"], observacao="Primeira publicação do texto; posteriormente republicado no Gabinete.")

add_edge("sedutor-manifesta-pt", "work:o-sedutor-irving", "manifestation:pt-br:gabinete:sedutor:1837-10-15", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p55-58:sedutor-comparativo"])

add_edge("manuscrito-manifesta-en", "work:manuscrito-casa-loucos", "manifestation:en:literary-souvenir:manuscript-madhouse:1829", "MANIFESTA", "identificado", ["evidence:soares:2006:pdf-p98-99:manuscrito-original"])
add_edge("manuscrito-manifesta-pt", "work:manuscrito-casa-loucos", "manifestation:pt-br:gabinete:manuscrito-casa-loucos:1837-10-01", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p98-99:manuscrito-original"])

add_edge("honras-manifesta-en", "work:hereditary-honours", "manifestation:en:new-monthly:hereditary-honours:1832", "MANIFESTA", "identificado", ["evidence:soares:2006:pdf-p100-103:honras-comparacao"])
add_edge("honras-manifesta-pt", "work:hereditary-honours", "manifestation:pt-br:gabinete:as-honras-hereditarias:1837-10-22", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p100-103:honras-comparacao"])

add_edge("terencio-manifesta-en", "work:terence-oflaherty", "manifestation:en:forget-me-not:terence-oflaherty:1829", "MANIFESTA", "identificado", ["evidence:soares:2006:pdf-p93-95:terencio-original"])
add_edge("terencio-manifesta-pt", "work:terence-oflaherty", "manifestation:pt-br:gabinete:terencio-alfaiate:1837-11-12", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p93-95:terencio-original"])

add_edge("alibi-manifesta-en", "work:alibi-grattan", "manifestation:en:new-monthly:alibi:1836-02", "MANIFESTA", "identificado", ["evidence:soares:2006:pdf-p95-97:alibi-apresentacao"])
add_edge("alibi-manifesta-pt", "work:alibi-grattan", "manifestation:pt-br:gabinete:alibi:1837-10-29", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p95-97:alibi-apresentacao"])

add_edge("esbocos-manifesta-en", "work:esbocos-sicilianos", "manifestation:en:metropolitan:sicilian-facts", "MANIFESTA", "identificado", ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"])
add_edge("esbocos-manifesta-pt", "work:esbocos-sicilianos", "manifestation:pt-br:gabinete:esbocos-sicilianos:1838-03-11-a-04-01", "MANIFESTA", "documentado", ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"])

# PUBLICADA_EM — Manifestacao -> Periodico/Giftbook
add_edge("cockney-publicada-en-nmm", "manifestation:en:new-monthly:cockney-country-gentleman:1837-06", "periodico:new-monthly-magazine", "PUBLICADA_EM", "identificado", ["evidence:soares:2006:pdf-p103-111:costumes-comparacao"])
add_edge("cockney-publicada-fr-rb", "manifestation:fr:revue-britannique:le-cockney-campagnard:1838-02", "periodico:revue-britannique", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p137-138:revue-britannique-le-cockney"])
add_edge("cockney-publicada-pt-gab", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p103-111:costumes-comparacao"])
add_edge("davy-publicada-en-bw", "manifestation:en:blackwoods:davy-jones:1830-07", "periodico:blackwoods-magazine", "PUBLICADA_EM", "identificado", ["evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"])
add_edge("davy-publicada-pt-gab", "manifestation:pt-br:gabinete:uma-noite-no-mar:1837-08-20", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"])
add_edge("testamento-publicada-pt-gab", "manifestation:pt-br:gabinete:testamento:1837-10-08", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p91-93:testamento-fonte-problematica"])
add_edge("livro-publicada-pt-gab", "manifestation:pt-br:gabinete:livro-da-vida:1837-09-17", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p92-93:livro-da-vida-fonte-problematica"])
add_edge("livro-publicada-pt-chr", "manifestation:pt-br:chronista:livro-da-vida:1836-10", "periodico:o-chronista", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p12-13:livro-da-vida-republicacao-chronista"])
add_edge("sedutor-publicada-pt-gab", "manifestation:pt-br:gabinete:sedutor:1837-10-15", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p55-58:sedutor-comparativo"])
add_edge("manuscrito-publicada-en-ls", "manifestation:en:literary-souvenir:manuscript-madhouse:1829", "giftbook:literary-souvenir", "PUBLICADA_EM", "identificado", ["evidence:soares:2006:pdf-p98-99:manuscrito-original"])
add_edge("manuscrito-publicada-pt-gab", "manifestation:pt-br:gabinete:manuscrito-casa-loucos:1837-10-01", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p98-99:manuscrito-original"])
add_edge("honras-publicada-en-nmm", "manifestation:en:new-monthly:hereditary-honours:1832", "periodico:new-monthly-magazine", "PUBLICADA_EM", "identificado", ["evidence:soares:2006:pdf-p100-103:honras-comparacao"])
add_edge("honras-publicada-pt-gab", "manifestation:pt-br:gabinete:as-honras-hereditarias:1837-10-22", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p100-103:honras-comparacao"])
add_edge("terencio-publicada-en-fmn", "manifestation:en:forget-me-not:terence-oflaherty:1829", "giftbook:forget-me-not", "PUBLICADA_EM", "identificado", ["evidence:soares:2006:pdf-p93-95:terencio-original"])
add_edge("terencio-publicada-pt-gab", "manifestation:pt-br:gabinete:terencio-alfaiate:1837-11-12", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p93-95:terencio-original"])
add_edge("alibi-publicada-en-nmm", "manifestation:en:new-monthly:alibi:1836-02", "periodico:new-monthly-magazine", "PUBLICADA_EM", "identificado", ["evidence:soares:2006:pdf-p95-97:alibi-apresentacao"])
add_edge("alibi-publicada-pt-gab", "manifestation:pt-br:gabinete:alibi:1837-10-29", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p95-97:alibi-apresentacao"])
add_edge("esbocos-publicada-en-met", "manifestation:en:metropolitan:sicilian-facts", "periodico:the-metropolitan", "PUBLICADA_EM", "identificado", ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"])
add_edge("esbocos-publicada-pt-gab", "manifestation:pt-br:gabinete:esbocos-sicilianos:1838-03-11-a-04-01", "periodico:gabinete-de-leitura", "PUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"])

# SERIALIZADA_EM — Manifestacao -> PublicacaoSerializada (apenas Esboços)
add_edge("esbocos-serializada-no-gabinete", "manifestation:pt-br:gabinete:esbocos-sicilianos:1838-03-11-a-04-01", "serial:esbocos-sicilianos-no-gabinete", "SERIALIZADA_EM", "documentado", ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"])

# PARTE_EM — PublicacaoSerializada -> Fasciculo (4 partes)
for slug in ["gabinete:31:1838-03-11", "gabinete:32:1838-03-18", "gabinete:33:1838-03-25", "gabinete:34:1838-04-01"]:
    add_edge(f"serial-{slug}-parte", "serial:esbocos-sicilianos-no-gabinete", f"fasciculo:{slug}", "PARTE_EM", "documentado", ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"])

# PERTENCE_A — Fasciculo -> Periodico
for slug in ["gabinete:02:1837-08-20", "gabinete:06:1837-09-17", "gabinete:08:1837-10-01", "gabinete:09:1837-10-08", "gabinete:10:1837-10-15", "gabinete:11:1837-10-22", "gabinete:12:1837-10-29", "gabinete:14:1837-11-12", "gabinete:30:1838-03-04", "gabinete:31:1838-03-11", "gabinete:32:1838-03-18", "gabinete:33:1838-03-25", "gabinete:34:1838-04-01"]:
    add_edge(f"fasc-{slug}-pertence-gab", f"fasciculo:{slug}", "periodico:gabinete-de-leitura", "PERTENCE_A", "documentado", ["evidence:soares:2006:pdf-p91-92:prosa-britanica-apresentacao"])

# DECLARA_COMO_FONTE — Manifestacao brasileira -> FonteDeclarada
add_edge("costumes-declara-colburns", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04", "fontedeclarada:colburns-magazine", "DECLARA_COMO_FONTE", "documentado", ["evidence:soares:2006:pdf-p103-111:costumes-comparacao"], observacao="Fonte declarada pelo Gabinete: 'Colburn's Magazine'. Referência problemática — não existiu.")
add_edge("testamento-declara-crabbe", "manifestation:pt-br:gabinete:testamento:1837-10-08", "fontedeclarada:crabbe-posthumous-works", "DECLARA_COMO_FONTE", "documentado", ["evidence:soares:2006:pdf-p91-93:testamento-fonte-problematica"], observacao="Fonte declarada pelo Gabinete: 'Crabbe's Posthumous Works'. Referência problemática — não houve publicação com esse título.")
add_edge("livro-declara-retrospective", "manifestation:pt-br:gabinete:livro-da-vida:1837-09-17", "fontedeclarada:retrospective-review", "DECLARA_COMO_FONTE", "documentado", ["evidence:soares:2006:pdf-p92-93:livro-da-vida-fonte-problematica"], observacao="Fonte declarada pelo Gabinete: 'Retrospective Review'. Revista existe mas não publicava narrativas completas.")

# PUBLICADA_ORIGINALMENTE_EM — Obra -> Periodico/Giftbook (veículo original identificado pela tese)
add_edge("cockney-publicada-originalmente-nmm", "work:a-cockney-country-gentleman", "periodico:new-monthly-magazine", "PUBLICADA_ORIGINALMENTE_EM", "identificado", ["evidence:soares:2006:pdf-p103-111:costumes-comparacao"])
add_edge("davy-publicada-originalmente-bw", "work:uma-noite-no-mar", "periodico:blackwoods-magazine", "PUBLICADA_ORIGINALMENTE_EM", "identificado", ["evidence:soares:2006:pdf-p91:uma-noite-no-mar-original"])
add_edge("manuscrito-publicada-originalmente-ls", "work:manuscrito-casa-loucos", "giftbook:literary-souvenir", "PUBLICADA_ORIGINALMENTE_EM", "identificado", ["evidence:soares:2006:pdf-p98-99:manuscrito-original"])
add_edge("honras-publicada-originalmente-nmm", "work:hereditary-honours", "periodico:new-monthly-magazine", "PUBLICADA_ORIGINALMENTE_EM", "identificado", ["evidence:soares:2006:pdf-p100-103:honras-comparacao"])
add_edge("terencio-publicada-originalmente-fmn", "work:terence-oflaherty", "giftbook:forget-me-not", "PUBLICADA_ORIGINALMENTE_EM", "identificado", ["evidence:soares:2006:pdf-p93-95:terencio-original"])
add_edge("alibi-publicada-originalmente-nmm", "work:alibi-grattan", "periodico:new-monthly-magazine", "PUBLICADA_ORIGINALMENTE_EM", "identificado", ["evidence:soares:2006:pdf-p95-97:alibi-apresentacao"])
add_edge("esbocos-publicada-originalmente-met", "work:esbocos-sicilianos", "periodico:the-metropolitan", "PUBLICADA_ORIGINALMENTE_EM", "identificado", ["evidence:soares:2006:pdf-p97-98:esbocos-apresentacao"])

# RELACAO_DE_DEPENDENCIA_TEXTUAL — Manifestacao brasileira -> Manifestacao original
# Usa-se quando há original identificado e comparação da tese, mas a rota tradutória exata não está demonstrada.
relacoes_dependencia = [
    ("costumes-dep-cockney", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04", "manifestation:en:new-monthly:cockney-country-gentleman:1837-06", "evidence:soares:2006:pdf-p103-111:costumes-comparacao", "A tese compara as versões, mas a rota tradutória exata permanece indeterminada (pode ser direta do inglês ou ter passado por outra via)."),
    ("honras-dep-hereditary", "manifestation:pt-br:gabinete:as-honras-hereditarias:1837-10-22", "manifestation:en:new-monthly:hereditary-honours:1832", "evidence:soares:2006:pdf-p100-103:honras-comparacao", "A tese compara as versões, mas a rota tradutória exata permanece indeterminada."),
    ("alibi-dep-the-alibi", "manifestation:pt-br:gabinete:alibi:1837-10-29", "manifestation:en:new-monthly:alibi:1836-02", "evidence:soares:2006:pdf-p132-134:alibi-comparacao", "A tese compara as versões, mas a rota tradutória exata permanece indeterminada."),
    ("esbocos-dep-sicilian", "manifestation:pt-br:gabinete:esbocos-sicilianos:1838-03-11-a-04-01", "manifestation:en:metropolitan:sicilian-facts", "evidence:soares:2006:pdf-p98:esbocos-supressao-nota-punicao", "A tese compara o prólogo e a nota sobre punição moral, mas a rota tradutória exata permanece indeterminada."),
    # Identificações sem comparação tradutória explícita: dependência registrada mas status 'identificado' (não 'documentado')
    ("davy-dep-davy", "manifestation:pt-br:gabinete:uma-noite-no-mar:1837-08-20", "manifestation:en:blackwoods:davy-jones:1830-07", "evidence:soares:2006:pdf-p91:uma-noite-no-mar-original", "Original identificado; tese não realiza análise comparativa tradutória detalhada."),
    ("manuscrito-dep-manuscript", "manifestation:pt-br:gabinete:manuscrito-casa-loucos:1837-10-01", "manifestation:en:literary-souvenir:manuscript-madhouse:1829", "evidence:soares:2006:pdf-p98-99:manuscrito-original", "Original identificado; tese não realiza análise comparativa tradutória detalhada."),
    ("terencio-dep-terence", "manifestation:pt-br:gabinete:terencio-alfaiate:1837-11-12", "manifestation:en:forget-me-not:terence-oflaherty:1829", "evidence:soares:2006:pdf-p93-95:terencio-original", "Original identificado; tese não realiza análise comparativa tradutória detalhada.")
]
for eid, br, en, ev, obs in relacoes_dependencia:
    # As quatro com comparação explícita = documentado; as três sem comparação = identificado
    status_dep = "documentado" if eid in ["costumes-dep-cockney", "honras-dep-hereditary", "alibi-dep-the-alibi", "esbocos-dep-sicilian"] else "identificado"
    add_edge(eid, br, en, "RELACAO_DE_DEPENDENCIA_TEXTUAL", status_dep, [ev], qualificador="original_identificado_para_comparacao", observacao=obs)

# NAO_E_FONTE_DIRETA_DE — Revue Britannique -> Manifestacao brasileira de Costumes Ingleses
add_edge("le-cockney-nao-e-fonte-costumes", "manifestation:fr:revue-britannique:le-cockney-campagnard:1838-02", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04", "NAO_E_FONTE_DIRETA_DE", "documentado", ["evidence:soares:2006:pdf-p137-138:revue-britannique-le-cockney"], observacao="A tese afirma expressamente: 'a versão brasileira não é a tradução desta francesa.'")

# TEM_VERSAO_FRANCESA_NA_REVUE — Manifestacao brasileira -> Periodico Revue Britannique
# Diferente de INTERMEDIADA_POR (que afirmaria rota), esta aresta registra apenas a EXISTÊNCIA
# de versão francesa, inferida por exclusão (a tese nomeia 3 exceções explícitas; os 7 restantes
# têm versão francesa, mas a tese não localiza nominalmente cada versão nem demonstra rota).
# Para Costumes Ingleses usamos NAO_E_FONTE_DIRETA_DE (afirmação expressa da tese — ver abaixo).
textos_com_versao_francesa = [
    ("manifestation:pt-br:gabinete:uma-noite-no-mar:1837-08-20", "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"),
    ("manifestation:pt-br:gabinete:livro-da-vida:1837-09-17", "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"),
    ("manifestation:pt-br:gabinete:sedutor:1837-10-15", "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"),
    ("manifestation:pt-br:gabinete:manuscrito-casa-loucos:1837-10-01", "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"),
    ("manifestation:pt-br:gabinete:terencio-alfaiate:1837-11-12", "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"),
    ("manifestation:pt-br:gabinete:alibi:1837-10-29", "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"),
    ("manifestation:pt-br:gabinete:esbocos-sicilianos:1838-03-11-a-04-01", "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique")
]
for br_id, ev in textos_com_versao_francesa:
    slug = br_id.split(":")[-1] if "pt-br:gabinete:" in br_id else br_id
    add_edge(f"{slug}-tem-versao-francesa-rb", br_id, "periodico:revue-britannique", "TEM_VERSAO_FRANCESA_NA_REVUE", "inferido", [ev], observacao="Existência inferida por exclusão: a tese nomeia 3 exceções (O Testamento, As Honras Hereditárias, Costumes Ingleses); este texto não figura entre elas. A tese não localiza nominalmente a versão francesa nem demonstra que ela foi a rota tradutória até o Brasil.", justificativa="Inferência por exclusão a partir da enumeração da tese (PDF p.143-144 / impressa 135-136) de 7 textos com versão francesa e 3 exceções.")

# COMPARA_COM — OperacaoTradutoria -> ManifestacaoTextual (par)
# Cada aresta COMPARA_COM herda as evidências da própria operação (a operação é a fonte da comparação)
comparacoes = [
    ("op-costumes-compara-en", "op:costumes:atenuacao-ironia-fieldlove", "manifestation:en:new-monthly:cockney-country-gentleman:1837-06"),
    ("op-costumes-compara-pt1", "op:costumes:atenuacao-ironia-fieldlove", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04"),
    ("op-costumes-trab-en", "op:costumes:modificacao-trabalho-rural", "manifestation:en:new-monthly:cockney-country-gentleman:1837-06"),
    ("op-costumes-trab-pt", "op:costumes:modificacao-trabalho-rural", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04"),
    ("op-costumes-desf-en", "op:costumes:alteracao-desfecho-positivo", "manifestation:en:new-monthly:cockney-country-gentleman:1837-06"),
    ("op-costumes-desf-pt", "op:costumes:alteracao-desfecho-positivo", "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04"),
    ("op-honras-gesto-en", "op:honras:supressao-gesto-caracterizador", "manifestation:en:new-monthly:hereditary-honours:1832"),
    ("op-honras-gesto-pt", "op:honras:supressao-gesto-caracterizador", "manifestation:pt-br:gabinete:as-honras-hereditarias:1837-10-22"),
    ("op-honras-espaco-en", "op:honras:especificacao-espaco-narrativo", "manifestation:en:new-monthly:hereditary-honours:1832"),
    ("op-honras-espaco-pt", "op:honras:especificacao-espaco-narrativo", "manifestation:pt-br:gabinete:as-honras-hereditarias:1837-10-22"),
    ("op-alibi-critica-en", "op:alibi:supressao-critica-irlandeses", "manifestation:en:new-monthly:alibi:1836-02"),
    ("op-alibi-critica-pt", "op:alibi:supressao-critica-irlandeses", "manifestation:pt-br:gabinete:alibi:1837-10-29"),
    ("op-esbocos-nota-en", "op:esbocos:supressao-nota-punicao-moral", "manifestation:en:metropolitan:sicilian-facts"),
    ("op-esbocos-nota-pt", "op:esbocos:supressao-nota-punicao-moral", "manifestation:pt-br:gabinete:esbocos-sicilianos:1838-03-11-a-04-01")
]
# Mapear operação -> seus evidence_ids (para propagar)
op_evidence_map = {op["id"]: op["evidence_ids"] for op in operacoes_data}
for eid, op_id, man_id in comparacoes:
    add_edge(eid, op_id, man_id, "COMPARA_COM", "documentado", op_evidence_map.get(op_id, []))

# SUSTENTA — Evidencia -> OperacaoTradutoria (cada operação sustentada por evidências)
sustenta_ops = [
    ("ev-sustenta-op-costumes-ironia", "evidence:soares:2006:pdf-p106-107:costumes-atenuacao-ironia", "op:costumes:atenuacao-ironia-fieldlove"),
    ("ev-sustenta-op-costumes-trab", "evidence:soares:2006:pdf-p108-109:costumes-modificacao-trabalho-rural", "op:costumes:modificacao-trabalho-rural"),
    ("ev-sustenta-op-costumes-desf", "evidence:soares:2006:pdf-p109-111:costumes-alteracao-desfecho", "op:costumes:alteracao-desfecho-positivo"),
    ("ev-sustenta-op-honras-gesto", "evidence:soares:2006:pdf-p101-102:honras-supressao-gesto", "op:honras:supressao-gesto-caracterizador"),
    ("ev-sustenta-op-honras-espaco", "evidence:soares:2006:pdf-p102-103:honras-especificacao-espaco", "op:honras:especificacao-espaco-narrativo"),
    ("ev-sustenta-op-alibi", "evidence:soares:2006:pdf-p132-134:alibi-comparacao", "op:alibi:supressao-critica-irlandeses"),
    ("ev-sustenta-op-esbocos", "evidence:soares:2006:pdf-p98:esbocos-supressao-nota-punicao", "op:esbocos:supressao-nota-punicao-moral")
]
for eid, ev_id, op_id in sustenta_ops:
    # As evidências também são nós do grafo
    # Vamos adicioná-las como nós abaixo
    pass

# AFETA — OperacaoTradutoria -> Obra
for op in operacoes_data:
    add_edge(f"op-{op['id'].split(':')[-1]}-afeta-obra", op["id"], op["obra_id"], "AFETA", "documentado", op["evidence_ids"])

# ANALISA — Tese -> Obra / Manifestacao
obras_ids = [o["id"] for o in obras_data]
for obra_id in obras_ids:
    add_edge(f"tese-analisa-{obra_id.split(':')[-1]}", "tese:soares:2006", obra_id, "ANALISA", "documentado", ["evidence:soares:2006:pdf-p91-92:prosa-britanica-apresentacao"])

# ---------- Evidências como nós ----------
# As evidências já são entidades separadas; também devem aparecer como nós do tipo Evidencia
for ev in EVIDENCIAS:
    nos.append({
        "id": ev["id"],
        "tipo": "Evidencia",
        "titulo": ev["titulo"],
        "aliases": [],
        "atributos": {
            "tipo_evidencia": ev["tipo_evidencia"],
            "fonte": ev["fonte"]
        },
        "status_epistemologico": ev["status_epistemologico"],
        "evidence_ids": [],
        "observacao": None
    })

# Agora sim as arestas SUSTENTA (Evidencia -> OperacaoTradutoria)
# A própria evidência é a fonte da aresta; o evidence_id é o ID do nó-origem.
for eid, ev_id, op_id in sustenta_ops:
    add_edge(eid, ev_id, op_id, "SUSTENTA", "documentado", [ev_id])

# SUSTENTA — Evidencia -> Arestas de dependência (também são sustentadas)
# Vamos adicionar argumentos genéricos

# ---------- Argumentos ----------
argumentos = [
    {
        "id": "argument:sete-textos-via-revue-britannique",
        "tipo": "Argumento",
        "titulo": "Sete dos dez textos britânicos do Gabinete tiveram versão francesa na Revue Britannique",
        "enunciado": "Apesar de os redatores do Gabinete de Leitura citarem apenas as fontes inglesas, apagando, assim, a provável intermediação da Revue Britannique, tudo indica que ela não foi pequena. Isso porque, dos dez textos ficcionais ingleses presentes no Gabinete de Leitura, sete tiveram versões francesas na Revue Britannique.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"],
        "sustenta_ids": ["periodico:revue-britannique"]
    },
    {
        "id": "argument:costumes-nao-traducao-do-frances",
        "tipo": "Argumento",
        "titulo": "A versão brasileira de Costumes Ingleses não é tradução da versão francesa de Le Cockney Campagnard",
        "enunciado": "Apesar de na Revue Britannique haver uma narrativa intitulada Le Cockney Campagnard, publicada em fevereiro de 1838, a versão brasileira não é a tradução desta francesa. Segundo Ramicelli, a versão brasileira também difere da versão francesa publicada nas páginas da Revue Britannique. Ela constatou que o texto brasileiro apresenta determinados trechos que se encontram em inglês, mas não na versão francesa.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p137-138:revue-britannique-le-cockney"],
        "sustenta_ids": ["manifestation:fr:revue-britannique:le-cockney-campagnard:1838-02"]
    },
    {
        "id": "argument:costumes-adequacao-visao-brasileira",
        "tipo": "Argumento",
        "titulo": "As alterações em Costumes Ingleses adequaram a narrativa à visão dos intelectuais brasileiros sobre a sociedade britânica",
        "enunciado": "O progresso material e intelectual adquirido por Fieldlove — que Torres Homem denominou de o 'duplo capital' ganho pelo trabalhador livre — correspondia às expectativas que esses jovens intelectuais tinham com relação a uma sociedade moderna, na qual as oportunidades de trabalho, e, consequentemente, de sucesso, estavam abertas ao cidadão comum.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p109-111:costumes-alteracao-desfecho"],
        "sustenta_ids": ["op:costumes:alteracao-desfecho-positivo"]
    },
    {
        "id": "argument:testamento-honras-costumes-excecoes-rb",
        "tipo": "Argumento",
        "titulo": "Três textos britânicos não tiveram versão na Revue Britannique (exceções explícitas)",
        "enunciado": "A exceção ficou por conta de 'O Testamento', atribuída a George Crabbe, 'As honras hereditárias' de Bulwer-Lytton, e 'Costumes Ingleses' de John Poole. No caso da última, apesar de na Revue Britannique haver uma narrativa intitulada 'Le Cockney Campagnard', a versão brasileira não é a tradução desta francesa.",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"],
        "sustenta_ids": ["work:o-testamento", "work:hereditary-honours", "work:a-cockney-country-gentleman"]
    },
    {
        "id": "argument:liberdade-tradutora-periodo",
        "tipo": "Argumento",
        "titulo": "Procedimentos tradutórios da época não se pautavam pela fidelidade ao texto original",
        "enunciado": "Os procedimentos tradutórios utilizados na época não se pautavam pela fidelidade ao texto original. Numa época em que a regulamentação dos direitos autorais era bastante precária, a livre apropriação de obras por quem as pirateava ou traduzia era bastante comum. A própria tradutora brasileira de 'O Amor Materno' indica: 'traduziremos, mas, com a liberdade de que usamos, iremos cortando ao original o que nos parecer inútil, desenvolvendo o que julgamos carecer de desenvolvimento, alterando o que achamos que para ser mais facilmente entendido deve ser alterado.'",
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p129-130:liberdade-tradutora"],
        "sustenta_ids": ["op:costumes:atenuacao-ironia-fieldlove", "op:costumes:modificacao-trabalho-rural", "op:costumes:alteracao-desfecho-positivo", "op:honras:supressao-gesto-caracterizador", "op:honras:especificacao-espaco-narrativo", "op:alibi:supressao-critica-irlandeses", "op:esbocos:supressao-nota-punicao-moral"]
    }
]
# Argumentos também como nós (para permitir referência por arestas)
for arg in argumentos:
    nos.append({
        "id": arg["id"],
        "tipo": "Argumento",
        "titulo": arg["titulo"],
        "aliases": [],
        "atributos": {"enunciado": arg["enunciado"]},
        "status_epistemologico": arg["status_epistemologico"],
        "evidence_ids": arg["evidence_ids"],
        "observacao": None
    })

# ---------- Montagem final ----------
grafo = {
    "versao": "3.0",
    "data_geracao": "2026-08-14",
    "metadados_projeto": {
        "tese_base": "SOARES, Maria Angélica Lau Pereira. Visão da Modernidade: A Presença Britânica no Gabinete de Leitura (1837-1838). 209f. Dissertação (Mestrado em Estudos Lingüísticos e Literários em Inglês) — Universidade de São Paulo, São Paulo, 2006.",
        "escopo": "Proveniência textual dos dez textos ficcionais britânicos identificados no Gabinete de Leitura (1837-1838) segundo a tese de Soares (2006).",
        "fonte_primaria": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf",
        "principio_filiacao": "Tese é fonte de verdade primária. JSONs anteriores (v2, v2.1, v2.2) são rascunhos e divergências foram registradas no relatorio_divergencias.md.",
        "paginacao": {
            "regra_global": "Não há offset universal garantido para toda a dissertação; nas páginas pré-textuais a distância varia.",
            "mapeamento_verificado": [
                {
                    "secao": "Capítulo 6 (A nação britânica no Gabinete de Leitura)",
                    "pagina_impressa_inicio": 76,
                    "pagina_pdf_inicio": 84,
                    "offset": 8,
                    "metodo_verificacao": "Marcador 'Capítulo 6' encontrado no PDF p.84 = impressa p.76 (confirmado via pdftotext -layout)."
                }
            ],
            "instrucao_consumidor": "Cada evidência armazena explicitamente pagina_pdf_* e pagina_impressa_* quando disponíveis. Consumidores nunca devem derivar uma a partir da outra em tempo de execução."
        }
    },
    "vocabulario_controlado": {
        "tipos_no": ["Tese", "Periodico", "Giftbook", "Fasciculo", "PublicacaoSerializada", "ObraAbstrata", "ManifestacaoTextual", "Pessoa", "FonteDeclarada", "Trecho", "OperacaoTradutoria", "Evidencia", "Argumento", "Local"],
        "tipos_aresta": ["AUTOR_DE", "MANIFESTA", "PUBLICADA_EM", "PERTENCE_A", "SERIALIZADA_EM", "PARTE_EM", "DECLARA_COMO_FONTE", "PUBLICADA_ORIGINALMENTE_EM", "RELACAO_DE_DEPENDENCIA_TEXTUAL", "INTERMEDIADA_POR", "TEM_VERSAO_FRANCESA_NA_REVUE", "NAO_E_FONTE_DIRETA_DE", "COMPARA_COM", "TEM_TRECHO", "AFETA", "SUSTENTA", "ANALISA"],
        "status_epistemologico": ["documentado", "identificado", "inferido", "hipotese", "problematico", "nao_identificado"]
    },
    "nos": nos,
    "arestas": arestas,
    "operacoes_tradutorias": operacoes_data,
    "argumentos": argumentos,
    "evidencias": EVIDENCIAS
}

OUT.write_text(json.dumps(grafo, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Escrito: {OUT}")
print(f"Nós: {len(nos)}")
print(f"Arestas: {len(arestas)}")
print(f"Operações tradutórias: {len(operacoes_data)}")
print(f"Argumentos: {len(argumentos)}")
print(f"Evidências: {len(EVIDENCIAS)}")

# Verificação rápida: IDs únicos
all_ids = [n["id"] for n in nos]
dup_ids = [x for x in all_ids if all_ids.count(x) > 1]
if dup_ids:
    print(f"AVISO: IDs duplicados: {set(dup_ids)}")
else:
    print("OK: IDs únicos")

# Verificação: origem/destino das arestas existem em nós
nos_set = set(all_ids)
arestas_orfas = [a for a in arestas if a["origem"] not in nos_set or a["destino"] not in nos_set]
if arestas_orfas:
    for a in arestas_orfas[:5]:
        print(f"  ORFÃ: {a['id']} — {a['origem']} -> {a['destino']}")
    print(f"Total de arestas órfãs: {len(arestas_orfas)}")
else:
    print("OK: Todas as arestas referenciam nós existentes")
