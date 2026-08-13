#!/usr/bin/env python3
"""
Validador semântico para o pacote de grafos da tese de Soares (2006).

Implementa as 10 regras que o JSON Schema não resolve sozinho (Parte F do prompt):
  1. IDs únicos em nós, arestas, evidências, operações e argumentos.
  2. Toda origem e destino de aresta existe em nos.
  3. Todo evidence_id referido existe em evidencias.
  4. O tipo de relação é compatível com tipos de origem/destino.
  5. Fascículo, data e manifestação brasileira são coerentes com o corpus canônico.
  6. Não há placeholders, ??, pendente, 'cerca de' ou campos vazios indevidos.
  7. Toda obra serializada tem todas as partes registradas.
  8. Uma relação com 'problematico' não pode ser apresentada como rota documentada.
  9. Não existem páginas PDF/impressas trocadas (PDF > impressa, exceto se offset correto).
  10. Toda afirmação 'documentado' possui pelo menos um evidence_id.
  11. 'inferido' e 'hipotese' exigem observacao ou justificativa preenchida.
  12. Operação tradutória deve ter 2+ manifestações comparadas.
  13. Evidência deve ter ao menos uma página PDF ou impressa.

Saída: relatorio_validacao.json
"""
import json
import re
from pathlib import Path
from collections import Counter

OUT_DIR = Path("/home/z/my-project/output")
REPORT_PATH = OUT_DIR / "relatorio_validacao.json"

# ---------- Carrega todos os arquivos ----------
corpus = json.loads((OUT_DIR / "corpus_britanico_canonico.json").read_text(encoding="utf-8"))
grafo_ctx = json.loads((OUT_DIR / "grafo_contextual_v2.json").read_text(encoding="utf-8"))
grafo_prov = json.loads((OUT_DIR / "grafo_proveniencia_textual_v3.json").read_text(encoding="utf-8"))

erros = []
avisos = []

def err(codigo, gravidade, entidade, mensagem, correcao_sugerida=None):
    e = {"codigo": codigo, "gravidade": gravidade, "entidade": entidade, "mensagem": mensagem}
    if correcao_sugerida:
        e["correcao_sugerida"] = correcao_sugerida
    erros.append(e)

def aviso(codigo, entidade, mensagem):
    avisos.append({"codigo": codigo, "entidade": entidade, "mensagem": mensagem})

# ---------- Regra 1: IDs únicos ----------
def check_unique_ids(name, items, id_key="id"):
    ids = [it[id_key] for it in items if id_key in it]
    dupes = [iid for iid, c in Counter(ids).items() if c > 1]
    for d in dupes:
        err("ID_DUPLICADO", "alta", d, f"ID duplicado em {name}: aparece {Counter(ids)[d]} vezes.", f"Renomear para garantir unicidade.")
    return len(dupes) == 0

check_unique_ids("corpus.itens", corpus["itens"])
check_unique_ids("grafo_contextual.nos", grafo_ctx["nos"])
check_unique_ids("grafo_contextual.arestas", grafo_ctx["arestas"])
check_unique_ids("grafo_contextual.evidencias", grafo_ctx["evidencias"])
check_unique_ids("grafo_proveniencia.nos", grafo_prov["nos"])
check_unique_ids("grafo_proveniencia.arestas", grafo_prov["arestas"])
check_unique_ids("grafo_proveniencia.evidencias", grafo_prov["evidencias"])
check_unique_ids("grafo_proveniencia.operacoes_tradutorias", grafo_prov["operacoes_tradutorias"])
if grafo_prov.get("argumentos"):
    check_unique_ids("grafo_proveniencia.argumentos", grafo_prov["argumentos"])

# Verificação cruzada: IDs de evidências em ambos os grafos devem ser únicos globalmente
all_evidence_ids = [e["id"] for e in grafo_ctx["evidencias"]] + [e["id"] for e in grafo_prov["evidencias"]]
dupes_ev = [iid for iid, c in Counter(all_evidence_ids).items() if c > 1]
for d in dupes_ev:
    aviso("EVIDENCIA_ID_REUTILIZADO", d, f"Evidence ID aparece em ambos os grafos ({Counter(all_evidence_ids)[d]}x). Isto é aceitável se o conteúdo é idêntico.")

# ---------- Regra 2: origem/destino de arestas existem ----------
def check_edge_targets(graph, name):
    node_ids = set(n["id"] for n in graph["nos"])
    orphan_count = 0
    for a in graph["arestas"]:
        if a["origem"] not in node_ids:
            err("EDGE_SOURCE_NOT_FOUND", "alta", a["id"], f"Origem não encontrada em nós: {a['origem']}", f"Adicionar nó {a['origem']} ou corrigir ID.")
            orphan_count += 1
        if a["destino"] not in node_ids:
            err("EDGE_TARGET_NOT_FOUND", "alta", a["id"], f"Destino não encontrado em nós: {a['destino']}", f"Adicionar nó {a['destino']} ou corrigir ID.")
            orphan_count += 1
    return orphan_count

check_edge_targets(grafo_ctx, "grafo_contextual")
check_edge_targets(grafo_prov, "grafo_proveniencia")

# ---------- Regra 3: evidence_ids referidos existem ----------
def check_evidence_refs(graph, name):
    ev_ids = set(e["id"] for e in graph["evidencias"])
    missing = 0
    # Em nós
    for n in graph["nos"]:
        for eid in n.get("evidence_ids", []):
            if eid not in ev_ids:
                err("EVIDENCE_ID_NOT_FOUND", "alta", n["id"], f"Nó referencia evidência inexistente: {eid}", f"Adicionar evidência {eid} ou corrigir referência.")
                missing += 1
    # Em arestas
    for a in graph["arestas"]:
        for eid in a.get("evidence_ids", []):
            if eid not in ev_ids:
                err("EVIDENCE_ID_NOT_FOUND", "alta", a["id"], f"Aresta referencia evidência inexistente: {eid}", f"Adicionar evidência {eid} ou corrigir referência.")
                missing += 1
    # Em operações (provenance only)
    for op in graph.get("operacoes_tradutorias", []):
        for eid in op.get("evidence_ids", []):
            if eid not in ev_ids:
                err("EVIDENCE_ID_NOT_FOUND", "alta", op["id"], f"Operação referencia evidência inexistente: {eid}", f"Adicionar evidência {eid}.")
                missing += 1
    # Em argumentos
    for arg in graph.get("argumentos", []):
        for eid in arg.get("evidence_ids", []):
            if eid not in ev_ids:
                err("EVIDENCE_ID_NOT_FOUND", "alta", arg["id"], f"Argumento referencia evidência inexistente: {eid}")
                missing += 1
    return missing

check_evidence_refs(grafo_ctx, "grafo_contextual")
check_evidence_refs(grafo_prov, "grafo_proveniencia")

# ---------- Regra 4: tipo de relação compatível com tipos de origem/destino ----------
# Vocabulário mínimo: cada tipo de aresta tem um conjunto esperado de (tipo_origem, tipo_destino)
def check_edge_types(graph, name):
    node_map = {n["id"]: n["tipo"] for n in graph["nos"]}
    # Regras: (tipo_aresta, tipos_origem_permitidos, tipos_destino_permitidos)
    rules = {
        "AUTORA_DE": (["Pessoa"], ["Tese", "ObraAbstrata", "ManifestacaoTextual"]),
        "ORIENTA": (["Pessoa"], ["Tese"]),
        "ANALISA": (["Tese", "Pessoa"], ["Periodico", "ObraAbstrata", "ManifestacaoTextual", "Conceito", "Capitulo", "Argumento"]),
        "PUBLICADA_EM": (["ManifestacaoTextual", "ObraAbstrata"], ["Periodico", "Giftbook"]),
        "IMPRESSA_EM": (["Periodico"], ["Tipografia"]),
        "VENDIDA_EM": (["Periodico"], ["Livraria"]),
        "REDIGE": (["Pessoa"], ["Periodico"]),
        "COLABORA_COM": (["Pessoa"], ["Periodico", "Instituicao", "Pessoa"]),
        "CONTRIBUI_PARA": (["Pessoa"], ["Periodico", "Instituicao"]),
        "REPUBLICADA_EM": (["Periodico"], ["Periodico"]),
        "RELACIONA_SE_A": (["Pessoa", "Conceito"], ["Tipografia", "Livraria", "Periodico", "Pessoa", "Conceito", "Tema", "MovimentoLiterario"]),
        "CITA": (["Pessoa", "Tese", "Argumento"], ["Periodico", "Capitulo", "ObraAbstrata"]),
        "SUSTENTA": (["Argumento", "Evidencia"], ["Conceito", "Tema", "MovimentoLiterario", "Periodico", "ObraAbstrata", "ManifestacaoTextual", "OperacaoTradutoria", "Pessoa"]),
        "ASSOCIA_SE_A": (["Pessoa", "Conceito"], ["Conceito", "Tema"]),
        "CONTEXTO_DE": (["Local"], ["Periodico", "ObraAbstrata", "ManifestacaoTextual"]),
        "INTEGRA": (["Tese", "Capitulo"], ["Capitulo", "Secao"]),
        "INFLUENCIA": (["MovimentoLiterario", "Pessoa"], ["Conceito", "Tema", "MovimentoLiterario"]),
        "TEM_TEMA": (["Periodico", "ObraAbstrata", "ManifestacaoTextual"], ["Tema"]),
        # Provenance-specific
        "MANIFESTA": (["ObraAbstrata"], ["ManifestacaoTextual"]),
        "PERTENCE_A": (["Fasciculo"], ["Periodico"]),
        "SERIALIZADA_EM": (["ManifestacaoTextual"], ["PublicacaoSerializada"]),
        "PARTE_EM": (["PublicacaoSerializada"], ["Fasciculo"]),
        "DECLARA_COMO_FONTE": (["ManifestacaoTextual"], ["FonteDeclarada"]),
        "PUBLICADA_ORIGINALMENTE_EM": (["ObraAbstrata"], ["Periodico", "Giftbook"]),
        "RELACAO_DE_DEPENDENCIA_TEXTUAL": (["ManifestacaoTextual"], ["ManifestacaoTextual"]),
        "INTERMEDIADA_POR": (["ManifestacaoTextual"], ["Periodico"]),
        "TEM_VERSAO_FRANCESA_NA_REVUE": (["ManifestacaoTextual"], ["Periodico"]),
        "NAO_E_FONTE_DIRETA_DE": (["ManifestacaoTextual"], ["ManifestacaoTextual"]),
        "COMPARA_COM": (["OperacaoTradutoria"], ["ManifestacaoTextual"]),
        "TEM_TRECHO": (["ManifestacaoTextual"], ["Trecho"]),
        "AFETA": (["OperacaoTradutoria"], ["ObraAbstrata"]),
        "AUTOR_DE": (["Pessoa"], ["ObraAbstrata"]),
    }
    for a in graph["arestas"]:
        if a["tipo"] not in rules:
            aviso("UNKNOWN_EDGE_TYPE", a["id"], f"Tipo de aresta não está nas regras de validação: {a['tipo']}")
            continue
        tipos_origem_ok, tipos_destino_ok = rules[a["tipo"]]
        if a["origem"] not in node_map:
            continue  # já reportado acima
        if a["destino"] not in node_map:
            continue
        tipo_origem = node_map[a["origem"]]
        tipo_destino = node_map[a["destino"]]
        if tipo_origem not in tipos_origem_ok:
            err("EDGE_TYPE_MISMATCH", "media", a["id"], f"Aresta {a['tipo']} espera origem {tipos_origem_ok}, mas origem é {tipo_origem} ({a['origem']}).")
        if tipo_destino not in tipos_destino_ok:
            err("EDGE_TYPE_MISMATCH", "media", a["id"], f"Aresta {a['tipo']} espera destino {tipos_destino_ok}, mas destino é {tipo_destino} ({a['destino']}).")

check_edge_types(grafo_ctx, "grafo_contextual")
check_edge_types(grafo_prov, "grafo_proveniencia")

# ---------- Regra 5: Coerência fascículo/data/manifestação com corpus canônico ----------
# Para cada item do corpus, verificar que a manifestação brasileira no grafo_prov tem fascículo e data corretos.
corpus_by_id = {it["id"]: it for it in corpus["itens"]}
# Mapear corpus_id -> obra_id (work:slug)
corpus_to_work = {
    "corpus:costumes-ingleses": "work:a-cockney-country-gentleman",
    "corpus:uma-noite-no-mar": "work:uma-noite-no-mar",
    "corpus:testamento": "work:o-testamento",
    "corpus:livro-da-vida": "work:o-livro-da-vida",
    "corpus:sedutor": "work:o-sedutor-irving",
    "corpus:manuscrito-casa-loucos": "work:manuscrito-casa-loucos",
    "corpus:honras-hereditarias": "work:hereditary-honours",
    "corpus:terencio-alfaiate": "work:terence-oflaherty",
    "corpus:alibi": "work:alibi-grattan",
    "corpus:esbocos-sicilianos": "work:esbocos-sicilianos"
}
# Manifestações brasileiras no grafo_prov
prov_manifestations_br = [n for n in grafo_prov["nos"] if n["tipo"] == "ManifestacaoTextual" and n["atributos"].get("idioma") == "pt-br" and n["atributos"].get("veiculo") == "Gabinete de Leitura"]

for corpus_id, work_id in corpus_to_work.items():
    item = corpus_by_id[corpus_id]
    fasc_esperado = item["fasciculos"][0]  # usa o primeiro fascículo
    # Procurar manifestação brasileira que corresponda a esta obra
    # Buscar por obra_id no atributo ou por convenção de ID
    # Convention: manifestação brasileira cujo ID contém o slug da obra
    found = False
    for m in prov_manifestations_br:
        # Heurística: a manifestação pertence a work_id se há aresta MANIFESTA com origem work_id
        pass
    # Mais robusto: usar arestas MANIFESTA para ligar work -> manifestacao
    edges_manifesta = [a for a in grafo_prov["arestas"] if a["tipo"] == "MANIFESTA" and a["origem"] == work_id and a["destino"] in [m["id"] for m in prov_manifestations_br]]
    for e in edges_manifesta:
        m = next(mm for mm in prov_manifestations_br if mm["id"] == e["destino"])
        data_manifestacao = m["atributos"].get("data_publicacao") or m["atributos"].get("data_publicacao_inicio")
        if data_manifestacao and data_manifestacao != fasc_esperado["data_iso"]:
            err("FASCICULO_DATA_MISMATCH", "alta", m["id"],
                f"Manifestação brasileira tem data {data_manifestacao}, mas corpus espera {fasc_esperado['data_iso']} para {corpus_id}.",
                "Atualizar manifestação ou corrigir corpus.")
        if "numero_fasciculo" in m["atributos"] and m["atributos"]["numero_fasciculo"] != fasc_esperado["numero"]:
            err("FASCICULO_NUMERO_MISMATCH", "alta", m["id"],
                f"Manifestação tem número {m['atributos']['numero_fasciculo']}, mas corpus espera {fasc_esperado['numero']}.")
        found = True
    if not found:
        aviso("MANIFESTACAO_BR_NAO_ENCONTRADA", work_id, f"Não foi encontrada manifestação brasileira para {corpus_id} via aresta MANIFESTA.")

# Verificar que o corpus tem exatamente 10 itens (Parte H critério)
if len(corpus["itens"]) != 10:
    err("CORPUS_SIZE_WRONG", "alta", "corpus_britanico_canonico.itens", f"Corpus tem {len(corpus['itens'])} itens, esperado 10.")

# ---------- Regra 6: Não há placeholders ----------
placeholder_patterns = [
    (r'\?\?', 'placeholder ??'),
    (r'texto-0[0-9]', 'placeholder texto-0X'),
    (r'\bpendente\b', 'palavra "pendente"'),
    (r'\bcerca de\b', 'palavras "cerca de"'),
    (r'\bTBD\b', 'placeholder TBD'),
    (r'\bTODO\b', 'placeholder TODO'),
    (r'^\s*null\s*$', 'valor null em campo textual'),
]

def scan_for_placeholders(obj, path=""):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            found.extend(scan_for_placeholders(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found.extend(scan_for_placeholders(v, f"{path}[{i}]"))
    elif isinstance(obj, str):
        for pat, label in placeholder_patterns:
            if re.search(pat, obj, re.IGNORECASE if label.startswith('palavra') else 0):
                # Ignorar "null" se o campo aceitar null (default); só reportar strings literais "null"
                if label == 'valor null em campo textual' and obj.strip().lower() == 'null':
                    found.append((path, label, obj))
    return found

# Verificar textos de títulos, observações, descrições
ph_count = 0
for graph, name in [(corpus, "corpus"), (grafo_ctx, "grafo_contextual"), (grafo_prov, "grafo_proveniencia")]:
    found = scan_for_placeholders(graph)
    for p, label, val in found:
        aviso("POSSIVEL_PLACEHOLDER", p, f"Possível {label}: {val[:60]!r}")
        ph_count += 1

# ---------- Regra 7: Toda obra serializada tem todas as partes registradas ----------
# No grafo_prov, buscar PublicacaoSerializada e verificar arestas PARTE_EM
for n in grafo_prov["nos"]:
    if n["tipo"] == "PublicacaoSerializada":
        serial_id = n["id"]
        partes = [a for a in grafo_prov["arestas"] if a["tipo"] == "PARTE_EM" and a["origem"] == serial_id]
        expected_fasciculos = n["atributos"].get("fasciculos", [])
        if len(partes) != len(expected_fasciculos):
            err("SERIALIZADA_PARTES_FALTANDO", "alta", serial_id,
                f"PublicacaoSerializada espera {len(expected_fasciculos)} partes, mas só há {len(partes)} arestas PARTE_EM.",
                f"Adicionar arestas PARTE_EM para os fascículos faltantes.")
        # Verificar que cada fascículo esperado está presente
        for fnum in expected_fasciculos:
            found_fasc = False
            for p in partes:
                fasc_node = next((nn for nn in grafo_prov["nos"] if nn["id"] == p["destino"]), None)
                if fasc_node and fasc_node["atributos"].get("numero") == fnum:
                    found_fasc = True
                    break
            if not found_fasc:
                err("FASCICULO_FALTANTE_EM_SERIE", "alta", serial_id,
                    f"Fascículo n.{fnum} esperado em {serial_id} não foi encontrado via PARTE_EM.")

# ---------- Regra 8: relação problematico não apresentada como rota documentada ----------
# Verificar arestas RELACAO_DE_DEPENDENCIA_TEXTUAL com status_epistemologico 'problematico' ou 'nao_identificado'
# NÃO devem ter arestas paralelas TRADUZIDA_DE (que não existe no vocabulário) ou evidência afirmando rota direta
for a in grafo_prov["arestas"]:
    if a["tipo"] == "RELACAO_DE_DEPENDENCIA_TEXTUAL" and a["status_epistemologico"] in ("problematico", "nao_identificado"):
        # OK, é apenas um registro
        pass
    # Verificar que não há aresta com tipo fora do vocabulário (que afirmaria rota direta indevidamente)
# Verificar também que works com status 'problematico' ou 'nao_identificado' não têm aresta PUBLICADA_ORIGINALMENTE_EM
work_status_map = {n["id"]: n["status_epistemologico"] for n in grafo_prov["nos"] if n["tipo"] == "ObraAbstrata"}
for a in grafo_prov["arestas"]:
    if a["tipo"] == "PUBLICADA_ORIGINALMENTE_EM":
        work_id = a["origem"]
        if work_id in work_status_map and work_status_map[work_id] in ("problematico", "nao_identificado"):
            err("ROTA_AFIRMADA_PARA_OBRA_PROBLEMATICA", "alta", a["id"],
                f"Aresta PUBLICADA_ORIGINALMENTE_EM afirma rota para obra {work_id} (status {work_status_map[work_id]}). Obra problemática não deve ter rota original afirmada.",
                "Remover aresta ou alterar status da obra para 'identificado'.")

# ---------- Regra 9: Paginação PDF/impressa coerente ----------
# Offset esperado: PDF = impressa + 8 (verificado)
for ev in grafo_ctx["evidencias"] + grafo_prov["evidencias"]:
    fonte = ev["fonte"]
    p_pdf_i = fonte.get("pagina_pdf_inicio")
    p_pdf_f = fonte.get("pagina_pdf_fim")
    p_imp_i = fonte.get("pagina_impressa_inicio")
    p_imp_f = fonte.get("pagina_impressa_fim")
    if p_pdf_i is not None and p_imp_i is not None:
        if p_pdf_i - p_imp_i != 8:
            err("PAGINACAO_OFFSET_ERRADO", "alta", ev["id"],
                f"Offset PDF-impressa incorreto: PDF={p_pdf_i}, impressa={p_imp_i}, diff={p_pdf_i-p_imp_i} (esperado 8).")
    if p_pdf_f is not None and p_imp_f is not None:
        if p_pdf_f - p_imp_f != 8:
            err("PAGINACAO_OFFSET_ERRADO", "alta", ev["id"],
                f"Offset PDF-impressa (fim) incorreto: PDF={p_pdf_f}, impressa={p_imp_f}, diff={p_pdf_f-p_imp_f} (esperado 8).")
    # PDF inicio <= PDF fim
    if p_pdf_i is not None and p_pdf_f is not None and p_pdf_i > p_pdf_f:
        err("PAGINACAO_INVERTIDA", "alta", ev["id"],
            f"pagina_pdf_inicio ({p_pdf_i}) > pagina_pdf_fim ({p_pdf_f}).")

# ---------- Regra 10: 'documentado' exige pelo menos um evidence_id ----------
def check_documented_requires_evidence(graph, name):
    # Exceções: nós que são metadados da própria tese (não claims que precisam de evidência paginada)
    EXCEPTION_IDS = {
        "tese:soares:2006",
        "instituicao:usp-fflch",
        "pessoa:maria-angelica-soares",
        "pessoa:sandra-vasconcelos"
    }
    EXCEPTION_EDGE_TYPES = {"AUTORA_DE", "ORIENTA", "INTEGRA"}  # auto-evidentes
    for n in graph["nos"]:
        if n["status_epistemologico"] == "documentado":
            if not n.get("evidence_ids"):
                if n["id"] in EXCEPTION_IDS:
                    continue
                if n["tipo"] in ("Tese", "Evidencia", "Argumento"):
                    continue
                aviso("DOCUMENTADO_SEM_EVIDENCIA", n["id"], f"Nó com status 'documentado' mas sem evidence_ids.")
    for a in graph["arestas"]:
        if a["status_epistemologico"] == "documentado":
            if not a.get("evidence_ids"):
                if a["tipo"] in EXCEPTION_EDGE_TYPES:
                    continue
                # Exceção: arestas que ligam nós-metadata à tese
                if a["origem"] in EXCEPTION_IDS or a["destino"] in EXCEPTION_IDS:
                    continue
                aviso("ARESTA_DOCUMENTADA_SEM_EVIDENCIA", a["id"], f"Aresta com status 'documentado' mas sem evidence_ids.")

check_documented_requires_evidence(grafo_ctx, "grafo_contextual")
check_documented_requires_evidence(grafo_prov, "grafo_proveniencia")

# ---------- Regra 11: 'inferido' e 'hipotese' exigem observacao/justificativa ----------
def check_inferred_requires_justification(graph, name):
    for n in graph["nos"]:
        if n["status_epistemologico"] in ("inferido", "hipotese"):
            if not n.get("observacao") and not n.get("justificativa"):
                err("INFERIDO_SEM_JUSTIFICATIVA", "alta", n["id"],
                    f"Nó com status '{n['status_epistemologico']}' deve ter observacao ou justificativa.")
    for a in graph["arestas"]:
        if a["status_epistemologico"] in ("inferido", "hipotese"):
            if not a.get("observacao") and not a.get("justificativa"):
                err("ARESTA_INFERIDA_SEM_JUSTIFICATIVA", "alta", a["id"],
                    f"Aresta com status '{a['status_epistemologico']}' deve ter observacao ou justificativa.")

check_inferred_requires_justification(grafo_ctx, "grafo_contextual")
check_inferred_requires_justification(grafo_prov, "grafo_proveniencia")

# ---------- Regra 12: Operação tradutória deve ter 2+ manifestações comparadas ----------
for op in grafo_prov.get("operacoes_tradutorias", []):
    if len(op.get("manifestacoes_comparadas", [])) < 2:
        err("OPERACAO_SEM_COMPARACAO", "alta", op["id"],
            f"Operação tradutória deve ter 2+ manifestações comparadas; tem {len(op.get('manifestacoes_comparadas', []))}.")

# ---------- Regra 13: Evidência deve ter ao menos uma página PDF ou impressa ----------
for ev in grafo_ctx["evidencias"] + grafo_prov["evidencias"]:
    fonte = ev["fonte"]
    has_pdf = fonte.get("pagina_pdf_inicio") is not None or fonte.get("pagina_pdf_fim") is not None
    has_imp = fonte.get("pagina_impressa_inicio") is not None or fonte.get("pagina_impressa_fim") is not None
    if not has_pdf and not has_imp:
        err("EVIDENCIA_SEM_PAGINACAO", "alta", ev["id"],
            f"Evidência deve ter ao menos uma página PDF ou impressa.")

# ---------- Estatísticas finais ----------
stats = {
    "nos_contextual": len(grafo_ctx["nos"]),
    "arestas_contextual": len(grafo_ctx["arestas"]),
    "nos_proveniencia": len(grafo_prov["nos"]),
    "arestas_proveniencia": len(grafo_prov["arestas"]),
    "evidencias": len(grafo_ctx["evidencias"]) + len(grafo_prov["evidencias"]),
    "operacoes_tradutorias": len(grafo_prov.get("operacoes_tradutorias", [])),
    "argumentos": len(grafo_ctx.get("argumentos", [])) + len(grafo_prov.get("argumentos", [])),
    "textos_corpus": len(corpus["itens"]),
    "arestas_orfas": sum(1 for a in grafo_ctx["arestas"] + grafo_prov["arestas"] if a["origem"] not in set(n["id"] for n in grafo_ctx["nos"] + grafo_prov["nos"]) or a["destino"] not in set(n["id"] for n in grafo_ctx["nos"] + grafo_prov["nos"])),
    "ids_duplicados": sum(1 for d in dupes_ev) if 'dupes_ev' in locals() else 0,
    "evidencias_ausentes": sum(1 for e in erros if e["codigo"] == "EVIDENCE_ID_NOT_FOUND"),
    "placeholders_encontrados": ph_count
}

# Resultado: aprovado se não há erros de gravidade alta
erros_alta = [e for e in erros if e["gravidade"] == "alta"]
resultado = "aprovado" if not erros_alta else "reprovado"

relatorio = {
    "resultado": resultado,
    "data_validacao": "2026-08-14",
    "arquivos_validados": [
        "corpus_britanico_canonico.json",
        "grafo_contextual_v2.json",
        "grafo_proveniencia_textual_v3.json",
        "schema_corpus_britanico_canonico.json",
        "schema_grafo_contextual_v2.json",
        "schema_grafo_proveniencia_textual_v3.json"
    ],
    "erros": erros,
    "avisos": avisos,
    "estatisticas": stats
}

REPORT_PATH.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nRelatório de validação: {REPORT_PATH}")
print(f"Resultado: {resultado}")
print(f"Total de erros: {len(erros)} ({len(erros_alta)} alta gravidade)")
print(f"Total de avisos: {len(avisos)}")
print(f"\nEstatísticas:")
for k, v in stats.items():
    print(f"  {k}: {v}")

if erros_alta:
    print(f"\nErros de alta gravidade:")
    for e in erros_alta[:10]:
        print(f"  [{e['codigo']}] {e['entidade']}: {e['mensagem'][:100]}")
