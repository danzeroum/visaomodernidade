/**
 * data-loader.js — Carrega os JSONs do diretório ./data/ e lê o relatório de validação.
 *
 * Ordem de carregamento:
 *   1. relatorio_validacao.json — se resultado != "aprovado", retorna estado "warning".
 *   2. corpus_britanico_canonico.json
 *   3. grafo_contextual_v2.json
 *   4. grafo_proveniencia_textual_v3.json
 *
 * Exporta:
 *   - DATA_BASE: caminho base para fetch()
 *   - loadAll(): retorna { corpus, contextual, proveniencia, validacao, estado }
 *   - estado: "loading" | "ready" | "warning" | "error"
 */

export const DATA_BASE = './data';

export const ESTADO = {
  LOADING: 'loading',
  READY: 'ready',
  WARNING: 'warning',
  ERROR: 'error'
};

async function fetchJSON(path) {
  const res = await fetch(path);
  if (!res.ok) {
    throw new Error(`Falha ao carregar ${path}: HTTP ${res.status}`);
  }
  return res.json();
}

/**
 * Carrega todos os JSONs e verifica o relatório de validação.
 * @returns {Promise<{corpus, contextual, proveniencia, validacao, estado, mensagem}>}
 */
export async function loadAll() {
  let validacao, corpus, contextual, proveniencia;

  try {
    validacao = await fetchJSON(`${DATA_BASE}/relatorio_validacao.json`);
  } catch (err) {
    return {
      estado: ESTADO.ERROR,
      mensagem: `Não foi possível carregar o relatório de validação: ${err.message}`,
      validacao: null,
      corpus: null,
      contextual: null,
      proveniencia: null
    };
  }

  // Se a validação não estiver aprovada, alerta o usuário mas continua carregando
  let estado = ESTADO.READY;
  let mensagem = null;
  if (validacao.resultado !== 'aprovado') {
    estado = ESTADO.WARNING;
    const errosAlta = (validacao.erros || []).filter(e => e.gravidade === 'alta');
    mensagem = `Atenção: o relatório de validação está "${validacao.resultado}". ` +
               `Há ${errosAlta.length} erro(s) de alta gravidade. Os dados podem estar comprometidos.`;
  } else if ((validacao.avisos || []).length > 0) {
    mensagem = `Dados validados com ${validacao.avisos.length} aviso(s) informativo(s).`;
  }

  try {
    [corpus, contextual, proveniencia] = await Promise.all([
      fetchJSON(`${DATA_BASE}/corpus_britanico_canonico.json`),
      fetchJSON(`${DATA_BASE}/grafo_contextual_v2.json`),
      fetchJSON(`${DATA_BASE}/grafo_proveniencia_textual_v3.json`)
    ]);
  } catch (err) {
    return {
      estado: ESTADO.ERROR,
      mensagem: `Erro ao carregar dados: ${err.message}`,
      validacao,
      corpus: null,
      contextual: null,
      proveniencia: null
    };
  }

  return { validacao, corpus, contextual, proveniencia, estado, mensagem };
}

// ---------- Helpers de consulta ao grafo de proveniência ----------

/**
 * Encontra um nó por ID no grafo de proveniência.
 */
export function findNode(proveniencia, id) {
  return proveniencia.nos.find(n => n.id === id) || null;
}

/**
 * Encontra arestas por origem, destino e/ou tipo.
 */
export function findEdges(proveniencia, { origem = null, destino = null, tipo = null } = {}) {
  return proveniencia.arestas.filter(a => {
    if (origem && a.origem !== origem) return false;
    if (destino && a.destino !== destino) return false;
    if (tipo && a.tipo !== tipo) return false;
    return true;
  });
}

/**
 * Encontra uma evidência por ID.
 */
export function findEvidence(proveniencia, id) {
  return proveniencia.evidencias.find(e => e.id === id) || null;
}

/**
 * Encontra operações tradutórias por obra_id.
 */
export function findOperationsByWork(proveniencia, obraId) {
  return proveniencia.operacoes_tradutorias.filter(op => op.obra_id === obraId);
}

/**
 * Mapeamento corpus_id -> work_id (conforme config.py)
 */
const CORPUS_TO_WORK = {
  'corpus:costumes-ingleses': 'work:a-cockney-country-gentleman',
  'corpus:uma-noite-no-mar': 'work:uma-noite-no-mar',
  'corpus:testamento': 'work:o-testamento',
  'corpus:livro-da-vida': 'work:o-livro-da-vida',
  'corpus:sedutor': 'work:o-sedutor-irving',
  'corpus:manuscrito-casa-loucos': 'work:manuscrito-casa-loucos',
  'corpus:honras-hereditarias': 'work:hereditary-honours',
  'corpus:terencio-alfaiate': 'work:terence-oflaherty',
  'corpus:alibi': 'work:alibi-grattan',
  'corpus:esbocos-sicilianos': 'work:esbocos-sicilianos'
};

export function workIdForCorpus(corpusId) {
  return CORPUS_TO_WORK[corpusId] || null;
}

/**
 * Encontra a manifestação brasileira de uma obra no Gabinete de Leitura.
 */
export function findBrazilianManifestation(proveniencia, obraId) {
  // work --MANIFESTA--> manifestation
  const manifestaEdges = findEdges(proveniencia, { origem: obraId, tipo: 'MANIFESTA' });
  for (const e of manifestaEdges) {
    const node = findNode(proveniencia, e.destino);
    if (node && node.tipo === 'ManifestacaoTextual' &&
        node.atributos.idioma === 'pt-br' &&
        node.atributos.veiculo === 'Gabinete de Leitura') {
      return node;
    }
  }
  return null;
}

/**
 * Encontra a manifestação original (em inglês) de uma obra.
 */
export function findOriginalManifestation(proveniencia, obraId) {
  const manifestaEdges = findEdges(proveniencia, { origem: obraId, tipo: 'MANIFESTA' });
  for (const e of manifestaEdges) {
    const node = findNode(proveniencia, e.destino);
    if (node && node.tipo === 'ManifestacaoTextual' &&
        node.atributos.idioma === 'en') {
      return node;
    }
  }
  return null;
}

/**
 * Encontra a fonte declarada de uma manifestação brasileira.
 */
export function findDeclaredFont(proveniencia, manifestacaoId) {
  const edges = findEdges(proveniencia, { origem: manifestacaoId, tipo: 'DECLARA_COMO_FONTE' });
  if (edges.length === 0) return null;
  return findNode(proveniencia, edges[0].destino);
}

/**
 * Encontra a versão francesa de uma obra (se existir).
 */
export function findFrenchVersion(proveniencia, obraId) {
  const manifestaEdges = findEdges(proveniencia, { origem: obraId, tipo: 'MANIFESTA' });
  for (const e of manifestaEdges) {
    const node = findNode(proveniencia, e.destino);
    if (node && node.tipo === 'ManifestacaoTextual' &&
        node.atributos.idioma === 'fr') {
      return node;
    }
  }
  return null;
}

/**
 * Verifica se a versão francesa NÃO é fonte direta da manifestação brasileira.
 */
export function isFrenchVersionNotDirectSource(proveniencia, frenchManifestationId, brazilianManifestationId) {
  const edges = findEdges(proveniencia, {
    origem: frenchManifestationId,
    destino: brazilianManifestationId,
    tipo: 'NAO_E_FONTE_DIRETA_DE'
  });
  return edges.length > 0;
}

/**
 * Verifica se há uma aresta TEM_VERSAO_FRANCESA_NA_REVUE para a manifestação brasileira.
 */
export function hasFrenchVersionInRevue(proveniencia, brazilianManifestationId) {
  const edges = findEdges(proveniencia, {
    origem: brazilianManifestationId,
    tipo: 'TEM_VERSAO_FRANCESA_NA_REVUE'
  });
  return edges.length > 0 ? edges[0] : null;
}

/**
 * Encontra o autor de uma obra.
 */
export function findAuthor(proveniencia, obraId) {
  const edges = findEdges(proveniencia, { destino: obraId, tipo: 'AUTOR_DE' });
  if (edges.length === 0) return null;
  return findNode(proveniencia, edges[0].origem);
}

/**
 * Encontra o veículo de publicação original de uma obra.
 */
export function findOriginalVenue(proveniencia, obraId) {
  const edges = findEdges(proveniencia, { origem: obraId, tipo: 'PUBLICADA_ORIGINALMENTE_EM' });
  if (edges.length === 0) return null;
  return findNode(proveniencia, edges[0].destino);
}

/**
 * Encontra todas as evidências referenciadas por um nó ou aresta.
 */
export function getEvidenceFor(proveniencia, item) {
  if (!item || !item.evidence_ids) return [];
  return item.evidence_ids.map(id => findEvidence(proveniencia, id)).filter(e => e !== null);
}

/**
 * Formata data ISO (YYYY-MM-DD) para exibição pt-BR.
 */
export function formatDate(iso) {
  if (!iso) return '—';
  const [y, m, d] = iso.split('-');
  const months = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
  const mi = parseInt(m, 10) - 1;
  if (mi < 0 || mi > 11) return iso;
  return `${parseInt(d)} ${months[mi]} ${y}`;
}

/**
 * Formata intervalo de páginas impressas.
 */
export function formatPages(fonte) {
  if (!fonte) return '—';
  const pi = fonte.pagina_impressa_inicio;
  const pf = fonte.pagina_impressa_fim;
  if (pi === null && pf === null) return '—';
  if (pi === pf) return `p. ${pi}`;
  return `pp. ${pi}–${pf}`;
}

/**
 * Formata intervalo de páginas PDF.
 */
export function formatPdfPages(fonte) {
  if (!fonte) return '—';
  const pi = fonte.pagina_pdf_inicio;
  const pf = fonte.pagina_pdf_fim;
  if (pi === null && pf === null) return '—';
  if (pi === pf) return `PDF p. ${pi}`;
  return `PDF pp. ${pi}–${pf}`;
}
