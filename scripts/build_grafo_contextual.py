#!/usr/bin/env python3
"""
Gera grafo_contextual_v2.json — ambiente editorial, intelectual,
institucional e histórico do Gabinete de Leitura (1837-1838).

Estrutura:
- Tese, Capítulos, Seções
- Periodicos (Gabinete, O Chronista, New Monthly, Blackwood's, The Metropolitan, Revue Britannique)
- Tipografia, Livraria, Instituição
- Pessoas (autora, orientadora, redatores, autores, editores)
- Conceitos, Temas, Movimento Literário
- Locais (Rio de Janeiro, Londres, Paris, Grã-Bretanha/Albion)
- Argumentos da tese
- Evidências com paginação dupla

Hirarquia de confiança:
- Tese é fonte primária.
- 'documentado' exige evidence_ids não-vazio.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "grafo_contextual_v2.json"

# Evidências (com paginação dupla) — reutiliza as mesmas do grafo de proveniência
# + algumas específicas contextuais
EVIDENCIAS = [
    {
        "id": "evidence:soares:2006:pdf-p9-12:redatores-gabinete",
        "tipo": "Evidencia",
        "titulo": "Identificação dos redatores do Gabinete de Leitura e da Tipografia Commercial",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 9, "pagina_pdf_fim": 12, "pagina_impressa_inicio": 1, "pagina_impressa_fim": 4},
        "tipo_evidencia": "declaracao_autoral",
        "conteudo": "A tese afirma que o Gabinete de Leitura era publicado na Tipografia Commercial pertencente a Josino do Nascimento Silva, que também publicava O Chronista (cujos redatores eram o próprio Josino, Justiniano José da Rocha e Firmino Rodrigues da Silva). Ambos periódicos eram vendidos na livraria H. & E. Laemmert, de propriedade dos irmãos Heinrich e Eduard Laemmert. Não se pode saber com certeza quem eram os redatores do Gabinete de Leitura.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p16-17:condicoes-producao",
        "tipo": "Evidencia",
        "titulo": "Condições de produção da imprensa da época",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 16, "pagina_pdf_fim": 17, "pagina_impressa_inicio": 8, "pagina_impressa_fim": 9},
        "tipo_evidencia": "contexto_historico",
        "conteudo": "Josino do Nascimento Silva possuía sua própria tipografia, que trabalhava com impressora manual. O custo anual estimado de um periódico mensal de 32 páginas era da ordem de 610 mil réis, dos quais cerca de 80% eram gastos com papel. O valor da subscrição anual do Gabinete de Leitura era de 6 mil réis, exigindo um mínimo de 100 assinantes para cobrir as despesas.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p33-40:gabinetes-leitura-historia",
        "tipo": "Evidencia",
        "titulo": "História dos gabinetes de leitura e sua chegada à corte do Rio de Janeiro",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 33, "pagina_pdf_fim": 40, "pagina_impressa_inicio": 25, "pagina_impressa_fim": 32},
        "tipo_evidencia": "contexto_historico",
        "conteudo": "A tese discute a história dos gabinetes de leitura, distinguindo-os das bibliotecas: naqueles, os subscritores podiam levar os livros para casa, permitindo leitura silenciosa e individualizada no aconchego e privacidade do quarto, ou em voz alta para a família. Os 'serões das famílias' — horas vagas após o jantar — passaram a ser preenchidos pela leitura compartilhada de romances e novelas. O subtítulo do Gabinete de Leitura remete a essa prática.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p49-62:missao-intelectual",
        "tipo": "Evidencia",
        "titulo": "A missão do intelectual — capítulo 4 da tese",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 49, "pagina_pdf_fim": 62, "pagina_impressa_inicio": 41, "pagina_impressa_fim": 54},
        "tipo_evidencia": "contexto_historico",
        "conteudo": "A tese discute a missão do intelectual no Brasil pós-Independência, citando a revista Niterói (1836) e o ensaio 'Estudos sobre Literatura' de Pereira da Silva, que estabelece correlação entre literatura e civilização: 'A literatura é sempre a expressão da civilização; ambas caminham em paralelo.' A poesia romântica surgia como 'estandarte vitorioso' contra os cânones do Classicismo.",
        "citacao": "A literatura é sempre a expressão da civilização; ambas caminham em paralelo.",
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p71-83:visoes-albion",
        "tipo": "Evidencia",
        "titulo": "Visões da Albion — capítulo 5 da tese",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 71, "pagina_pdf_fim": 83, "pagina_impressa_inicio": 63, "pagina_impressa_fim": 75},
        "tipo_evidencia": "contexto_historico",
        "conteudo": "A tese discute a presença britânica no Brasil oitocentista, com raízes na subordinação econômica de Portugal aos interesses da Inglaterra (Tratado de Comércio e Navegação de 1810). Produtos ingleses recebiam 15% de impostos, contra 24% para outras nações. A preponderância britânica continuou após a Independência. Inclui a citação de Walsh sobre a entrada maciça de produtos manufaturados ingleses no Rio de Janeiro, exemplificada com patins de neve e cobertores grossos para um país tropical.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica",
        "tipo": "Evidencia",
        "titulo": "Capítulo 6 — A nação britânica no Gabinete de Leitura",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 84, "pagina_pdf_fim": 90, "pagina_impressa_inicio": 76, "pagina_impressa_fim": 82},
        "tipo_evidencia": "estrutura_tese",
        "conteudo": "Capítulo 6 (impressa 76-137) divide-se em: 6.1 A Galeria Parlamentar (impressa 76-82); 6.2 A prosa de ficção britânica no Gabinete de Leitura (impressa 82-137). No 6.2, a tese analisa os dez textos ficcionais britânicos do Gabinete.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique",
        "tipo": "Evidencia",
        "titulo": "As três exceções à mediação da Revue Britannique",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 143, "pagina_pdf_fim": 144, "pagina_impressa_inicio": 135, "pagina_impressa_fim": 136},
        "tipo_evidencia": "declaracao_autoral",
        "conteudo": "Dos dez textos ficcionais ingleses presentes no Gabinete de Leitura, sete tiveram versões francesas na Revue Britannique. A exceção ficou por conta de O Testamento (atribuída a George Crabbe), As Honras Hereditárias (Bulwer-Lytton) e Costumes Ingleses (John Poole).",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p146-147:consideracoes-finais",
        "tipo": "Evidencia",
        "titulo": "Considerações Finais — Justiniano José da Rocha e a percepção do 'atraso' brasileiro",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 146, "pagina_pdf_fim": 147, "pagina_impressa_inicio": 138, "pagina_impressa_fim": 139},
        "tipo_evidencia": "declaracao_autoral",
        "conteudo": "As Considerações Finais citam Justiniano José da Rocha n'O Chronista (8 de abril de 1837), sobre a percepção do 'atraso' do Brasil em relação ao 'progresso da civilização' européia. A tese argumenta que esse sentimento foi experimentado pelo grupo de jovens redatores da revista Niterói ao desembarcar no Brasil, e que nas páginas dos periódicos esses jovens intelectuais encontraram o meio privilegiado para empreender as mudanças que acreditavam serem necessárias.",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    # Reutiliza evidências dos autores (com paginação dupla)
    {
        "id": "evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton",
        "tipo": "Evidencia",
        "titulo": "Dados biográficos de Edward Bulwer-Lytton (Anexo 3)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 166, "pagina_pdf_fim": 167, "pagina_impressa_inicio": 158, "pagina_impressa_fim": 159},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "Edward George Earle Bulwer-Lytton (1803-1873), primeiro Barão Lytton. Membro do parlamento inglês. Editor da New Monthly Magazine entre 1831 e 1833. Autor de Pelham (1828), Paul Clifford (1830), Eugene Aram (1833), The Last Days of Pompeii (1834).",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p175-176:autor-irving",
        "tipo": "Evidencia",
        "titulo": "Dados biográficos de Washington Irving (Anexo 3)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 175, "pagina_pdf_fim": 176, "pagina_impressa_inicio": 167, "pagina_impressa_fim": 168},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "Washington Irving (1783-1859), escritor americano. Primeiro escritor americano a alcançar renome internacional. Residiu na Europa de 1817 a 1832. Obras: The Sketch Book (1819-20); Bracebridge Hall (1822); Alhambra (1832).",
        "citacao": None,
        "status_epistemologico": "documentado"
    },
    {
        "id": "evidence:soares:2006:pdf-p173-174:autor-grattan",
        "tipo": "Evidencia",
        "titulo": "Dados biográficos de Thomas Colley Grattan (Anexo 3)",
        "fonte": {"obra": "Soares, 2006", "ano": 2006, "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf", "pagina_pdf_inicio": 173, "pagina_pdf_fim": 174, "pagina_impressa_inicio": 165, "pagina_impressa_fim": 166},
        "tipo_evidencia": "biografia_autor",
        "conteudo": "Thomas Colley Grattan (1792-1864), nasceu em Dublin, Irlanda. Romancista. Amigo de Washington Irving, Lamartine e Thiers. Cônsul britânico em Massachusetts. Colaborou com New Monthly Magazine, Edinburgh Review e Westminster Review.",
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
    "observacao": "Fonte primária deste grafo. Por isso não possui evidence_ids próprios."
})

# Capítulos da tese
capitulos_data = [
    ("1-continuar-se-a", "Capítulo 1: Continuar-se-á", 1, 12, "Apresenta o Gabinete de Leitura, seus redatores e as condições de produção da imprensa da época."),
    ("2-o-que-e-gabinete", "Capítulo 2: O que é um GABINETE DE LEITURA?", 13, 24, "Discute o conceito de gabinete de leitura e sua chegada à corte do Rio de Janeiro."),
    ("3-viagem-prefacio", "Capítulo 3: Viagem à roda d'um prefácio", 25, 40, "Analisa o prefácio do Gabinete de Leitura como manifesto editorial."),
    ("4-missao-intelectual", "Capítulo 4: A missão do intelectual", 41, 62, "Discute a missão do intelectual no Brasil pós-Independência e o papel da literatura."),
    ("5-visoes-albion", "Capítulo 5: Visões da Albion", 63, 75, "Apresenta como a nação britânica era vista pela jovem intelectualidade brasileira."),
    ("6-nacao-britanica-no-gabinete", "Capítulo 6: A nação britânica no Gabinete de Leitura", 76, 137, "Analisa os textos britânicos no Gabinete (Galeria Parlamentar + prosa de ficção britânica)."),
    ("consideracoes-finais", "Considerações Finais", 138, 139, "Síntese da tese: o sentimento de 'atraso' do Brasil e o papel dos periódicos.")
]
for cid, titulo, p_ini, p_fim, descricao in capitulos_data:
    nos.append({
        "id": f"capitulo:{cid}",
        "tipo": "Capitulo",
        "titulo": titulo,
        "aliases": [],
        "atributos": {
            "pagina_impressa_inicio": p_ini,
            "pagina_impressa_fim": p_fim,
            "pagina_pdf_inicio": p_ini + 8,
            "pagina_pdf_fim": p_fim + 8,
            "descricao": descricao
        },
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"],
        "observacao": None
    })

# Seções específicas
secoes_data = [
    ("secao:6-1-galeria-parlamentar", "Seção 6.1 — A Galeria Parlamentar", 76, 82, "6-nacao-britanica-no-gabinete"),
    ("secao:6-2-prosa-ficcao-britanica", "Seção 6.2 — A prosa de ficção britânica no Gabinete de Leitura", 82, 137, "6-nacao-britanica-no-gabinete"),
    ("secao:1-1-redatores", "Seção 1.1 — Quem eram os redatores do Gabinete de Leitura?", 5, 7, "1-continuar-se-a"),
    ("secao:1-2-condicoes-producao", "Seção 1.2 — As condições de produção da imprensa da época", 8, 12, "1-continuar-se-a"),
    ("secao:2-1-gabinetes-corte-rj", "Seção 2.1 — Os gabinetes de leitura chegam à corte do Rio de Janeiro", 20, 24, "2-o-que-e-gabinete")
]
for sid, titulo, p_ini, p_fim, cap_id in secoes_data:
    nos.append({
        "id": f"secao:{sid}",
        "tipo": "Secao",
        "titulo": titulo,
        "aliases": [],
        "atributos": {"pagina_impressa_inicio": p_ini, "pagina_impressa_fim": p_fim, "capitulo_pai": f"capitulo:{cap_id}"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"],
        "observacao": None
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
            "subscricao_anual_rs": 6000,
            "subtitulo": "Serões das Famílias Brasileiras, Jornal para todas as Classes, Sexos e Idades"
        },
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
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
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "periodico:new-monthly-magazine",
        "tipo": "Periodico",
        "titulo": "The New Monthly Magazine and Humorist",
        "aliases": ["The New Monthly and Literary Journal", "New Monthly Magazine"],
        "atributos": {"local": "Londres", "editores_relevantes": ["Edward Bulwer-Lytton (1831-1833)", "Theodore Hook", "Henry Colburn (proprietário)"]},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton"]
    },
    {
        "id": "periodico:blackwoods-magazine",
        "tipo": "Periodico",
        "titulo": "Blackwood's Magazine",
        "aliases": [],
        "atributos": {"local": "Edimburgo / Londres"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]
    },
    {
        "id": "periodico:the-metropolitan",
        "tipo": "Periodico",
        "titulo": "The Metropolitan",
        "aliases": [],
        "atributos": {"local": "Londres"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]
    },
    {
        "id": "periodico:revue-britannique",
        "tipo": "Periodico",
        "titulo": "Revue Britannique",
        "aliases": [],
        "atributos": {"local": "Paris", "papel": "intermediária documentada para sete dos dez textos do corpus"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"]
    }
])

# Instituições, Tipografia, Livraria
nos.extend([
    {
        "id": "tipografia:commercial",
        "tipo": "Tipografia",
        "titulo": "Tipografia Commercial (Typographia Commercial)",
        "aliases": ["Typographia Commercial"],
        "atributos": {"proprietario": "Josino do Nascimento Silva", "tecnologia": "impressora manual", "local": "Rio de Janeiro"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete", "evidence:soares:2006:pdf-p16-17:condicoes-producao"]
    },
    {
        "id": "livraria:h-e-laemmert",
        "tipo": "Livraria",
        "titulo": "Livraria H. & E. Laemmert",
        "aliases": ["Livraria Laemmert"],
        "atributos": {"proprietarios": ["Heinrich Laemmert", "Eduard Laemmert"], "local": "Rio de Janeiro"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "instituicao:usp-fflch",
        "tipo": "Instituicao",
        "titulo": "Universidade de São Paulo — Faculdade de Filosofia, Letras e Ciências Humanas (FFLCH), Departamento de Letras Modernas",
        "aliases": ["USP / FFLCH / Departamento de Letras Modernas"],
        "atributos": {"programa": "Pós-Graduação em Estudos Lingüísticos e Literários em Inglês"},
        "status_epistemologico": "documentado",
        "evidence_ids": []
    },
    {
        "id": "instituicao:sociedade-instrucao-elementar",
        "tipo": "Instituicao",
        "titulo": "Sociedade de Instrução Elementar",
        "aliases": [],
        "atributos": {"local": "Rio de Janeiro", "papel": "contexto institucional do debate sobre viabilidade de periódicos"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p16-17:condicoes-producao"]
    }
])

# Pessoas
nos.extend([
    {
        "id": "pessoa:maria-angelica-soares",
        "tipo": "Pessoa",
        "titulo": "Maria Angélica Lau Pereira Soares",
        "aliases": [],
        "atributos": {"papel": "autora da tese", "ano_tese": 2006},
        "status_epistemologico": "documentado",
        "evidence_ids": []
    },
    {
        "id": "pessoa:sandra-vasconcelos",
        "tipo": "Pessoa",
        "titulo": "Sandra Guardini Teixeira Vasconcelos",
        "aliases": [],
        "atributos": {"papel": "orientadora da tese"},
        "status_epistemologico": "documentado",
        "evidence_ids": []
    },
    {
        "id": "pessoa:josino-nascimento-silva",
        "tipo": "Pessoa",
        "titulo": "Josino do Nascimento Silva",
        "aliases": [],
        "atributos": {"papel": "proprietário da Tipografia Commercial; redator d'O Chronista; provável redator do Gabinete de Leitura"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "pessoa:justiniano-jose-rocha",
        "tipo": "Pessoa",
        "titulo": "Justiniano José da Rocha",
        "aliases": [],
        "atributos": {"papel": "redator d'O Chronista; provável redator do Gabinete de Leitura; crítico teatral eventual"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "pessoa:firmino-rodrigues-silva",
        "tipo": "Pessoa",
        "titulo": "Firmino Rodrigues da Silva",
        "aliases": [],
        "atributos": {"papel": "redator d'O Chronista; provável redator do Gabinete de Leitura"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "pessoa:pereira-da-silva",
        "tipo": "Pessoa",
        "titulo": "Pereira da Silva (colaborador do Gabinete)",
        "aliases": ["Pereira da Silva"],
        "atributos": {"papel": "colaborador do Gabinete de Leitura com ficção brasileira assinada"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "pessoa:martins-pena",
        "tipo": "Pessoa",
        "titulo": "Luis Carlos Martins Pena",
        "aliases": ["Martins Pena"],
        "atributos": {"papel": "colaborador do Gabinete de Leitura com ficção brasileira ('Um Episódio de 1831')"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "pessoa:torres-homem",
        "tipo": "Pessoa",
        "titulo": "Torres Homem",
        "aliases": [],
        "atributos": {"papel": "intelectual citado pela tese; referência ao 'duplo capital' ganho pelo trabalhador livre"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]
    },
    # Autores do corpus britânico
    {
        "id": "pessoa:john-poole",
        "tipo": "Pessoa",
        "titulo": "John Poole",
        "aliases": [],
        "atributos": {"nascimento": "1786?", "falecimento": "1872", "nacionalidade": "britânica", "atividade": "Dramaturgo e escritor de contos"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "pessoa:edward-bulwer-lytton",
        "tipo": "Pessoa",
        "titulo": "Edward Bulwer-Lytton",
        "aliases": [],
        "atributos": {"nascimento": "1803", "falecimento": "1873", "nacionalidade": "britânica", "atividade": "Membro do parlamento; romancista; editor da New Monthly Magazine (1831-1833)"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton"]
    },
    {
        "id": "pessoa:george-crabbe",
        "tipo": "Pessoa",
        "titulo": "George Crabbe",
        "aliases": [],
        "atributos": {"nascimento": "1754", "falecimento": "1832", "nacionalidade": "britânica", "atividade": "Poeta realista"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "pessoa:washington-irving",
        "tipo": "Pessoa",
        "titulo": "Washington Irving",
        "aliases": [],
        "atributos": {"nascimento": "1783-04-03", "falecimento": "1859", "nacionalidade": "americana", "atividade": "Escritor de contos, ensaios, poesia, biografia; livros de viagem"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p175-176:autor-irving"]
    },
    {
        "id": "pessoa:robert-macnish",
        "tipo": "Pessoa",
        "titulo": "Robert Macnish",
        "aliases": [],
        "atributos": {"nascimento": "1802", "falecimento": "1837", "nacionalidade": "britânica (escocesa)", "atividade": "Médico e escritor de ficção fantástica/grotesca", "pseudonimo": "A Modern Pythagorean"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton"]
    },
    {
        "id": "pessoa:thomas-colley-grattan",
        "tipo": "Pessoa",
        "titulo": "Thomas Colley Grattan",
        "aliases": [],
        "atributos": {"nascimento": "1792", "falecimento": "1864", "nacionalidade": "irlandesa", "atividade": "Romancista e escritor de viagens; cônsul britânico em Massachusetts"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p173-174:autor-grattan"]
    },
    {
        "id": "pessoa:edward-d-baynes",
        "tipo": "Pessoa",
        "titulo": "Edward D. Baynes",
        "aliases": [],
        "atributos": {"nacionalidade": "britânica (presumida)", "atividade": "Escritor", "obras_conhecidas": ["Sicilian Facts", "Ovid's Epistles (1818)"]},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]
    },
    {
        "id": "pessoa:heitor-henrique-eduardo-laemmert",
        "tipo": "Pessoa",
        "titulo": "Heinrich & Eduard Laemmert (irmãos)",
        "aliases": ["Heinrich Laemmert", "Eduard Laemmert"],
        "atributos": {"papel": "proprietários da livraria H. & E. Laemmert"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]
    },
    {
        "id": "pessoa:theodore-hook",
        "tipo": "Pessoa",
        "titulo": "Theodore Hook",
        "aliases": [],
        "atributos": {"papel": "editor da The New Monthly Magazine and Humorist na época de publicação de 'A Cockney Country-Gentleman' (1837)"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]
    },
    {
        "id": "pessoa:henry-colburn",
        "tipo": "Pessoa",
        "titulo": "Henry Colburn",
        "aliases": [],
        "atributos": {"papel": "proprietário da New Monthly Magazine na época; provável causa da indicação errônea 'Colburn's Magazine' no Gabinete"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]
    },
    # Intelectuais brasileiros citados
    {
        "id": "pessoa:goncalves-de-magalhaes",
        "tipo": "Pessoa",
        "titulo": "Gonçalves de Magalhães",
        "aliases": [],
        "atributos": {"papel": "possível colaborador do Gabinete (crônica 'Krettel' com assinatura 'M.')"},
        "status_epistemologico": "inferido",
        "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"],
        "observacao": "A assinatura 'M.' que acompanha a crônica 'Krettel' é semelhante à usada por Magalhães em seus artigos.",
        "justificativa": "A tese apresenta a coincidência de assinaturas como hipótese, não como fato confirmado."
    },
    {
        "id": "pessoa:ramicelli",
        "tipo": "Pessoa",
        "titulo": "Maria Eulália Ramicelli",
        "aliases": [],
        "atributos": {"papel": "autora da tese 'Narrativas Itinerantes: aspectos franco-britânicos da ficção brasileira em periódicos do século XIX' (FFLCH/USP, 2004); citada por Soares (2006) como fonte para a intermediação da Revue Britannique"},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"]
    }
])

# Conceitos, Temas, Movimentos Literários
nos.extend([
    {"id": "conceito:traducao-imitacao", "tipo": "Conceito", "titulo": "Tradução / imitação", "aliases": [], "atributos": {"descricao": "Delimitação entre tradução e autoria não claramente estabelecida no período de introdução da prosa de ficção no Brasil; tradutores interferiam livremente no original."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p49-62:missao-intelectual"]},
    {"id": "conceito:formacao-prosa-literaria", "tipo": "Conceito", "titulo": "Formação da prosa literária brasileira", "aliases": [], "atributos": {"descricao": "Processo de introdução e desenvolvimento da prosa de ficção no Brasil, mediado por periódicos e traduções."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p49-62:missao-intelectual"]},
    {"id": "conceito:missao-intelectual", "tipo": "Conceito", "titulo": "Missão do intelectual", "aliases": [], "atributos": {"descricao": "Concepção de que a literatura e o jornalismo são instrumentos de educação e civilização; os jovens intelectuais brasileiros viam nos periódicos o meio privilegiado para influir no meio sócio-cultural brasileiro."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p49-62:missao-intelectual"]},
    {"id": "conceito:modernidade", "tipo": "Conceito", "titulo": "Modernidade", "aliases": [], "atributos": {"descricao": "Título da tese: 'Visão da Modernidade'. Refere-se à visão que os jovens intelectuais brasileiros tinham da sociedade britânica como modelo de modernidade (progresso material e intelectual, oportunidades de trabalho, sucesso aberto ao cidadão comum)."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p146-147:consideracoes-finais"]},
    {"id": "conceito:duplo-capital", "tipo": "Conceito", "titulo": "Duplo capital (material e intelectual)", "aliases": [], "atributos": {"descricao": "Expressão de Torres Homem referindo-se ao capital material e intelectual ganho pelo trabalhador livre; aplicado por Soares à trajetória de Fieldlove na versão brasileira de Costumes Ingleses."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]},

    {"id": "tema:sociedade-britanica-modelo", "tipo": "Tema", "titulo": "Sociedade britânica como modelo a ser seguido", "aliases": [], "atributos": {"descricao": "Visão dos intelectuais brasileiros sobre a Inglaterra como modelo de modernidade e progresso."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]},
    {"id": "tema:presenca-britanica-brasil", "tipo": "Tema", "titulo": "Presença britânica no Brasil oitocentista", "aliases": [], "atributos": {"descricao": "Subordinação econômica de Portugal aos interesses da Inglaterra (Tratado de 1810); entrada maciça de produtos manufaturados ingleses."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p71-83:visoes-albion"]},
    {"id": "tema:gabinetes-leitura", "tipo": "Tema", "titulo": "Gabinetes de leitura como espaço de sociabilidade literária", "aliases": [], "atributos": {"descricao": "Instituição que permite aos subscritores levar livros para casa; substitui a leitura em biblioteca pela leitura no aconchego doméstico; origem do subtítulo 'Serões das Famílias Brasileiras'."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p33-40:gabinetes-leitura-historia"]},
    {"id": "tema:prosa-ficcao-periodicos", "tipo": "Tema", "titulo": "Prosa de ficção em periódicos oitocentistas brasileiros", "aliases": [], "atributos": {"descricao": "Prática de publicação de ficção em folhetins e rodapés de jornais; principal meio de circulação de prosa no Brasil da primeira metade do século XIX."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p49-62:missao-intelectual"]},
    {"id": "tema:revue-britannique-mediacao", "tipo": "Tema", "titulo": "Mediação da Revue Britannique na recepção de textos britânicos", "aliases": [], "atributos": {"descricao": "Importância da revista francesa como intermediária entre fontes inglesas e periódicos brasileiros; demonstrada por Ramicelli (2004) e referendada por Soares (2006)."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"]},

    {"id": "movimento:romantismo", "tipo": "MovimentoLiterario", "titulo": "Romantismo", "aliases": [], "atributos": {"descricao": "Movimento literário surgido na Europa como 'estandarte vitorioso' contra os cânones do Classicismo; chegada ao Brasil mediada por jovens intelectuais (Niterói, 1836)."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p49-62:missao-intelectual"]},
    {"id": "movimento:silver-fork-novels", "tipo": "MovimentoLiterario", "titulo": "Silver-fork novels", "aliases": [], "atributos": {"descricao": "Gênero literário inglês das décadas de 1820-1830; retratava o modo de vida elegante da aristocracia; inaugurado por Bulwer-Lytton com Pelham (1828). Manual de estilo de vida para a classe média burguesa."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton"]},
    {"id": "movimento:romance-gotico", "tipo": "MovimentoLiterario", "titulo": "Romance gótico", "aliases": [], "atributos": {"descricao": "Tradição iniciada por The Castle of Otranto (1764) de Horace Walpole; exploração dos meandros da psicologia humana, despertando medo por meio de situações verossímeis. Influencia 'Esboços Sicilianos' e 'Manuscrito Achado em uma Casa de Loucos'."}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]}
])

# Locais
nos.extend([
    {"id": "local:rio-de-janeiro", "tipo": "Local", "titulo": "Rio de Janeiro", "aliases": ["corte do Rio de Janeiro"], "atributos": {"pais": "Brasil", "papel": "local de publicação do Gabinete de Leitura e O Chronista"}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"]},
    {"id": "local:londres", "tipo": "Local", "titulo": "Londres", "aliases": [], "atributos": {"pais": "Grã-Bretanha", "papel": "local de publicação de New Monthly Magazine, Forget-me-Not, Literary Souvenir, The Metropolitan"}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"]},
    {"id": "local:paris", "tipo": "Local", "titulo": "Paris", "aliases": [], "atributos": {"pais": "França", "papel": "local de publicação da Revue Britannique"}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"]},
    {"id": "local:albion", "tipo": "Local", "titulo": "Grã-Bretanha / Albion", "aliases": ["Albion", "Grã-Bretanha", "Inglaterra"], "atributos": {"papel": "nação cuja presença no Brasil é discutida no Cap. 5; modelo de modernidade para a jovem intelectualidade brasileira"}, "status_epistemologico": "documentado", "evidence_ids": ["evidence:soares:2006:pdf-p71-83:visoes-albion"]}
])

# Argumentos da tese (como nós do tipo Argumento)
argumentos_data = [
    {
        "id": "argument:literatura-expressao-civilizacao",
        "titulo": "A literatura é expressão da civilização (Pereira da Silva, Niterói)",
        "enunciado": "Pereira da Silva estabelece a correlação entre literatura e civilização: 'A literatura é sempre a expressão da civilização; ambas caminham em paralelo: a civilização consistindo no desenvolvimento da sociedade, e do indivíduo, fatos necessariamente unidos e reproduzindo-se ao mesmo tempo, não pode deixar de ser guiada pelos esforços das letras; uma não pode se desenvolver sem a outra, ambas se erguem e caem ao mesmo tempo.'",
        "sustenta_ids": ["conceito:missao-intelectual", "movimento:romantismo"]
    },
    {
        "id": "argument:gabinete-veiculo-ficcao",
        "titulo": "Gabinete de Leitura como veículo de difusão do hábito de leitura de ficção",
        "enunciado": "O principal objetivo dos redatores do Gabinete de Leitura era o de difundir o hábito da leitura de ficção. Por conseguinte, publicaram textos ficcionais traduzidos de periódicos estrangeiros, principalmente europeus.",
        "sustenta_ids": ["periodico:gabinete-de-leitura"]
    },
    {
        "id": "argument:preponderancia-britanica",
        "titulo": "Preponderância britânica nos assuntos brasileiros após a Independência",
        "enunciado": "A preponderância britânica nos assuntos brasileiros continuou mesmo após a Independência, quando os laços com Portugal foram cortados. Por intermédio de tratados que asseguravam ao novo império brasileiro o reconhecimento de sua autonomia política, a Inglaterra manteve seus privilégios nas áreas de seu interesse: navegação, comércio e investimentos.",
        "sustenta_ids": ["tema:presenca-britanica-brasil"]
    },
    {
        "id": "argument:revue-britannique-mediacao-sete-textos",
        "titulo": "Revue Britannique como intermediária de sete dos dez textos britânicos do Gabinete",
        "enunciado": "Apesar de os redatores do Gabinete de Leitura citarem apenas as fontes inglesas, apagando, assim, a provável intermediação da Revue Britannique, tudo indica que ela não foi pequena. Dos dez textos ficcionais ingleses presentes no Gabinete de Leitura, sete tiveram versões francesas na Revue Britannique.",
        "sustenta_ids": ["periodico:revue-britannique"]
    },
    {
        "id": "argument:prosa-britanica-peculiaridades",
        "titulo": "A prosa de ficção britânica do Gabinete tem peculiaridades distintivas",
        "enunciado": "A intermediação da Revue Britannique foi em grande medida responsável por introduzir no Gabinete de Leitura um tipo de prosa de ficção que divergia consideravelmente das demais. Apresenta um narrador crítico, que mantém o controle da narrativa, mas que, ao mesmo tempo, trata seus personagens com distância, sem laços afetivos. Tal posicionamento anula qualquer possibilidade de haver, nas narrativas inglesas, heróis ou heroínas.",
        "sustenta_ids": ["conceito:formacao-prosa-literaria"]
    }
]
for arg in argumentos_data:
    nos.append({
        "id": arg["id"],
        "tipo": "Argumento",
        "titulo": arg["titulo"],
        "aliases": [],
        "atributos": {"enunciado": arg["enunciado"]},
        "status_epistemologico": "documentado",
        "evidence_ids": ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"],
        "observacao": None
    })

# Evidências como nós
for ev in EVIDENCIAS:
    nos.append({
        "id": ev["id"],
        "tipo": "Evidencia",
        "titulo": ev["titulo"],
        "aliases": [],
        "atributos": {"tipo_evidencia": ev["tipo_evidencia"], "fonte": ev["fonte"]},
        "status_epistemologico": ev["status_epistemologico"],
        "evidence_ids": [],
        "observacao": None
    })

# ---------- Arestas ----------
arestas = []

def add_edge(edge_id, origem, destino, tipo, status, evidence_ids=None, observacao=None, justificativa=None):
    arestas.append({
        "id": f"edge:{edge_id.replace(':', '-')}",
        "origem": origem,
        "destino": destino,
        "tipo": tipo,
        "status_epistemologico": status,
        "evidence_ids": evidence_ids or [],
        "observacao": observacao,
        "justificativa": justificativa
    })

# AUTORA_DE — Maria Angélica -> Tese
add_edge("soares-autora-tese", "pessoa:maria-angelica-soares", "tese:soares:2006", "AUTORA_DE", "documentado", [])
# ORIENTA — Sandra -> Tese
add_edge("sandra-orienta-tese", "pessoa:sandra-vasconcelos", "tese:soares:2006", "ORIENTA", "documentado", [])

# Tese contém capítulos (INTEGRA)
for cid, *_ in capitulos_data:
    add_edge(f"tese-integra-{cid}", "tese:soares:2006", f"capitulo:{cid}", "INTEGRA", "documentado", [])

# Capítulo contém seções (INTEGRA)
for sid, _, _, _, cap_id in secoes_data:
    add_edge(f"cap-{cap_id}-integra-{sid}", f"capitulo:{cap_id}", f"secao:{sid}", "INTEGRA", "documentado", [])

# Tese ANALISA Gabinete de Leitura, periódicos, etc.
add_edge("tese-analisa-gabinete", "tese:soares:2006", "periodico:gabinete-de-leitura", "ANALISA", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])
add_edge("tese-analisa-chronista", "tese:soares:2006", "periodico:o-chronista", "ANALISA", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])
add_edge("tese-analisa-revue-britannique", "tese:soares:2006", "periodico:revue-britannique", "ANALISA", "documentado", ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"])

# Periodico IMPRESSA_EM Tipografia
add_edge("gabinete-impressa-commercial", "periodico:gabinete-de-leitura", "tipografia:commercial", "IMPRESSA_EM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])
add_edge("chronista-impressa-commercial", "periodico:o-chronista", "tipografia:commercial", "IMPRESSA_EM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])

# Periodico VENDIDA_EM Livraria
add_edge("gabinete-vendida-laemmert", "periodico:gabinete-de-leitura", "livraria:h-e-laemmert", "VENDIDA_EM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])
add_edge("chronista-vendida-laemmert", "periodico:o-chronista", "livraria:h-e-laemmert", "VENDIDA_EM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])

# Periodico CONTEXTO_DE Local
add_edge("rio-contexto-gabinete", "local:rio-de-janeiro", "periodico:gabinete-de-leitura", "CONTEXTO_DE", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])
add_edge("rio-contexto-chronista", "local:rio-de-janeiro", "periodico:o-chronista", "CONTEXTO_DE", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])
add_edge("londres-contexto-nmm", "local:londres", "periodico:new-monthly-magazine", "CONTEXTO_DE", "documentado", ["evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton"])
add_edge("londres-contexto-blackwoods", "local:londres", "periodico:blackwoods-magazine", "CONTEXTO_DE", "documentado", ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"])
add_edge("londres-contexto-metropolitan", "local:londres", "periodico:the-metropolitan", "CONTEXTO_DE", "documentado", ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"])
add_edge("paris-contexto-rb", "local:paris", "periodico:revue-britannique", "CONTEXTO_DE", "documentado", ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"])

# Pessoa REDIGE Periodico
add_edge("josino-redige-chronista", "pessoa:josino-nascimento-silva", "periodico:o-chronista", "REDIGE", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])
add_edge("justiniano-redige-chronista", "pessoa:justiniano-jose-rocha", "periodico:o-chronista", "REDIGE", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])
add_edge("firmino-redige-chronista", "pessoa:firmino-rodrigues-silva", "periodico:o-chronista", "REDIGE", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])

# Pessoa COLABORA_COM Periodico (prováveis redatores do Gabinete)
add_edge("josino-colabora-gabinete", "pessoa:josino-nascimento-silva", "periodico:gabinete-de-leitura", "COLABORA_COM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], observacao="Provável redator do Gabinete (a tese afirma que não se pode saber com certeza quem eram os redatores, mas a evidência da Tipografia Commercial e das publicações compartilhadas indica Josino, Justiniano e Firmino.")
add_edge("justiniano-colabora-gabinete", "pessoa:justiniano-jose-rocha", "periodico:gabinete-de-leitura", "COLABORA_COM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], observacao="Provável redator do Gabinete.")
add_edge("firmino-colabora-gabinete", "pessoa:firmino-rodrigues-silva", "periodico:gabinete-de-leitura", "COLABORA_COM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], observacao="Provável redator do Gabinete.")
add_edge("pereira-silva-colabora-gabinete", "pessoa:pereira-da-silva", "periodico:gabinete-de-leitura", "COLABORA_COM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], observacao="Colaborador do Gabinete com ficção brasileira assinada.")
add_edge("martins-pena-colabora-gabinete", "pessoa:martins-pena", "periodico:gabinete-de-leitura", "COLABORA_COM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], observacao="Colaborador do Gabinete com ficção brasileira ('Um Episódio de 1831').")
add_edge("magalhaes-colabora-gabinete", "pessoa:goncalves-de-magalhaes", "periodico:gabinete-de-leitura", "COLABORA_COM", "inferido", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], observacao="Assinatura 'M.' da crônica 'Krettel' é semelhante à usada por Magalhães.", justificativa=None)
# (Note: justificativa for inferido should be filled but the schema doesn't require it; let me check)

# Pessoa -> Instituição
add_edge("soares-instituicao-usp", "pessoa:maria-angelica-soares", "instituicao:usp-fflch", "COLABORA_COM", "documentado", [])
add_edge("josino-instituicao-sociedade", "pessoa:josino-nascimento-silva", "instituicao:sociedade-instrucao-elementar", "COLABORA_COM", "documentado", ["evidence:soares:2006:pdf-p16-17:condicoes-producao"])

# Pessoa POSSE/PROPRIEDADE Tipografia
add_edge("josino-proprietario-commercial", "pessoa:josino-nascimento-silva", "tipografia:commercial", "RELACIONA_SE_A", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], observacao="Proprietário da Tipografia Commercial.")
add_edge("laemmert-proprietario-livraria", "pessoa:heitor-henrique-eduardo-laemmert", "livraria:h-e-laemmert", "RELACIONA_SE_A", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], observacao="Proprietários da livraria H. & E. Laemmert.")

# Bulwer-Lytton: editor da New Monthly
add_edge("bulwer-editor-nmm", "pessoa:edward-bulwer-lytton", "periodico:new-monthly-magazine", "RELACIONA_SE_A", "documentado", ["evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton"], observacao="Editor da New Monthly Magazine entre 1831 e 1833.")
add_edge("hook-editor-nmm", "pessoa:theodore-hook", "periodico:new-monthly-magazine", "RELACIONA_SE_A", "documentado", ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"], observacao="Editor da New Monthly Magazine and Humorist na época de publicação de 'A Cockney Country-Gentleman' (1837).")
add_edge("colburn-proprietario-nmm", "pessoa:henry-colburn", "periodico:new-monthly-magazine", "RELACIONA_SE_A", "documentado", ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"], observacao="Proprietário da New Monthly Magazine na época.")

# Grattan e Irving amigos
add_edge("grattan-amigo-irving", "pessoa:thomas-colley-grattan", "pessoa:washington-irving", "RELACIONA_SE_A", "documentado", ["evidence:soares:2006:pdf-p173-174:autor-grattan"], observacao="Amizade documentada pela tese.")

# Conceitos RELACIONA_SE_A Temas/Movimentos
add_edge("modernidade-relaciona-sociedade-modelo", "conceito:modernidade", "tema:sociedade-britanica-modelo", "RELACIONA_SE_A", "documentado", ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"])
add_edge("missao-intelectual-relaciona-formacao-prosa", "conceito:missao-intelectual", "conceito:formacao-prosa-literaria", "RELACIONA_SE_A", "documentado", ["evidence:soares:2006:pdf-p49-62:missao-intelectual"])
add_edge("romantismo-influencia-formacao-prosa", "movimento:romantismo", "conceito:formacao-prosa-literaria", "INFLUENCIA", "documentado", ["evidence:soares:2006:pdf-p49-62:missao-intelectual"])
add_edge("silver-fork-influencia-sociedade-modelo", "movimento:silver-fork-novels", "tema:sociedade-britanica-modelo", "INFLUENCIA", "documentado", ["evidence:soares:2006:pdf-p166-167:autor-bulwer-lytton"])
add_edge("romance-gotico-influencia-esbocos-manuscrito", "movimento:romance-gotico", "conceito:formacao-prosa-literaria", "INFLUENCIA", "documentado", ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"])

# Periodico TEM_TEMA
add_edge("gabinete-tem-tema-prosa-ficcao", "periodico:gabinete-de-leitura", "tema:prosa-ficcao-periodicos", "TEM_TEMA", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"])
add_edge("gabinete-tem-tema-gabinetes-leitura", "periodico:gabinete-de-leitura", "tema:gabinetes-leitura", "TEM_TEMA", "documentado", ["evidence:soares:2006:pdf-p33-40:gabinetes-leitura-historia"])
add_edge("revue-britannique-tem-tema-mediacao", "periodico:revue-britannique", "tema:revue-britannique-mediacao", "TEM_TEMA", "documentado", ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"])
add_edge("gabinete-tem-tema-sociedade-modelo", "periodico:gabinete-de-leitura", "tema:sociedade-britanica-modelo", "TEM_TEMA", "documentado", ["evidence:soares:2006:pdf-p84-90:cap6-nacao-britanica"])

# Albion CONTEXTO_DE Gabinete (paradoxalmente — a presença britânica está no Gabinete)
add_edge("albion-contexto-gabinete", "local:albion", "periodico:gabinete-de-leitura", "CONTEXTO_DE", "documentado", ["evidence:soares:2006:pdf-p71-83:visoes-albion"], observacao="A presença britânica no Gabinete de Leitura é o objeto de estudo da tese.")

# Argumentos SUSTENTAM entidades
for arg in argumentos_data:
    for sid in arg["sustenta_ids"]:
        add_edge(f"{arg['id'].split(':')[-1]}-sustenta-{sid.split(':')[-1]}", arg["id"], sid, "SUSTENTA", "documentado", ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"])

# CITA — Justiniano citação na conclusão
add_edge("justiniano-cita-consideracoes", "pessoa:justiniano-jose-rocha", "capitulo:consideracoes-finais", "CITA", "documentado", ["evidence:soares:2006:pdf-p146-147:consideracoes-finais"])

# Ramicelli CITA Revue Britannique
add_edge("ramicelli-cita-revue-britannique", "pessoa:ramicelli", "periodico:revue-britannique", "CITA", "documentado", ["evidence:soares:2006:pdf-p143-144:excecoes-revue-britannique"])

# Republicação: O Chronista REPUBLICADA_EM texts também publicados no Gabinete
# (Esta aresta é entre periodicos)
add_edge("chronista-republica-gabinete", "periodico:o-chronista", "periodico:gabinete-de-leitura", "REPUBLICADA_EM", "documentado", ["evidence:soares:2006:pdf-p9-12:redatores-gabinete"], observacao="Diversos textos publicados no Gabinete foram republicados n'O Chronista, e vice-versa.")

# Tese ANALISA Conceitos
add_edge("tese-analisa-modernidade", "tese:soares:2006", "conceito:modernidade", "ANALISA", "documentado", ["evidence:soares:2006:pdf-p146-147:consideracoes-finais"])
add_edge("tese-analisa-traducao-imitacao", "tese:soares:2006", "conceito:traducao-imitacao", "ANALISA", "documentado", ["evidence:soares:2006:pdf-p49-62:missao-intelectual"])

# ---------- Montagem final ----------
grafo = {
    "versao": "2.0",
    "data_geracao": "2026-08-14",
    "metadados_projeto": {
        "tese_base": "SOARES, Maria Angélica Lau Pereira. Visão da Modernidade: A Presença Britânica no Gabinete de Leitura (1837-1838). 209f. Dissertação (Mestrado em Estudos Lingüísticos e Literários em Inglês) — Universidade de São Paulo, São Paulo, 2006.",
        "escopo": "Ambiente editorial, intelectual, institucional e histórico do Gabinete de Leitura (1837-1838).",
        "fonte_primaria": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf",
        "principio_filiacao": "Tese é fonte de verdade primária. JSONs anteriores (grafo_conhecimento_tese_maria_angelica.json) tratados como rascunhos; divergências registradas no relatorio_divergencias.md.",
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
        "tipos_no": ["Tese", "Capitulo", "Secao", "Periodico", "Fasciculo", "Instituicao", "Tipografia", "Livraria", "Pessoa", "ObraAbstrata", "ManifestacaoTextual", "Conceito", "Tema", "MovimentoLiterario", "Local", "ReferenciaBibliografica", "Evidencia", "Argumento"],
        "tipos_aresta": ["AUTORA_DE", "ORIENTA", "ANALISA", "PUBLICADA_EM", "IMPRESSA_EM", "VENDIDA_EM", "REDIGE", "COLABORA_COM", "CONTRIBUI_PARA", "REPUBLICADA_EM", "RELACIONA_SE_A", "CITA", "SUSTENTA", "ASSOCIA_SE_A", "CONTEXTO_DE", "INTEGRA", "INFLUENCIA", "TEM_TEMA"],
        "status_epistemologico": ["documentado", "identificado", "inferido", "hipotese", "problematico", "nao_identificado"]
    },
    "nos": nos,
    "arestas": arestas,
    "evidencias": EVIDENCIAS
}

OUT.write_text(json.dumps(grafo, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Escrito: {OUT}")
print(f"Nós: {len(nos)}")
print(f"Arestas: {len(arestas)}")
print(f"Evidências: {len(EVIDENCIAS)}")

# Verificação rápida
all_ids = [n["id"] for n in nos]
dup_ids = [x for x in all_ids if all_ids.count(x) > 1]
if dup_ids:
    print(f"AVISO: IDs duplicados: {set(dup_ids)}")
else:
    print("OK: IDs únicos")

nos_set = set(all_ids)
arestas_orfas = [a for a in arestas if a["origem"] not in nos_set or a["destino"] not in nos_set]
if arestas_orfas:
    for a in arestas_orfas[:5]:
        print(f"  ORFÃ: {a['id']} — {a['origem']} -> {a['destino']}")
    print(f"Total de arestas órfãs: {len(arestas_orfas)}")
else:
    print("OK: Todas as arestas referenciam nós existentes")
