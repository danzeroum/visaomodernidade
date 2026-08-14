/**
 * research-mode.js — Modo Explorar / Modo Pesquisar + Exportação.
 *
 * Funcionalidades:
 *   - Toggle entre modo "Explorar" (didático, sem metadados técnicos) e "Pesquisar" (denso, com IDs, status, páginas)
 *   - Persistência da preferência em localStorage
 *   - Exportação CSV da matriz filtrada
 *   - Exportação JSON do dossiê atual
 *   - Copiar citação acadêmica
 *   - Deep link de evidência (#evidencia=ID)
 *   - Painel de consulta técnica
 */

const STORAGE_KEY = 'visaomodernidade-mode';

function buildCitation() {
  const consultationDate = new Date().toLocaleDateString('pt-BR');
  return `SOARES, Maria Angélica Lau Pereira. Visão da Modernidade: `
    + `A Presença Britânica no Gabinete de Leitura (1837-1838). `
    + `São Paulo: USP, 2006. Evidência consultada no projeto `
    + `visaomodernidade, versão 0.8.0, em ${consultationDate}.`;
}

let _currentMode = 'explorar'; // 'explorar' | 'pesquisar'
let _corpus = null;
let _proveniencia = null;
let _contextual = null;
let _getFilteredItems = null; // callback que retorna itens filtrados da matriz
let _getCurrentDossierItem = null; // callback que retorna item do dossiê aberto

export function initResearchMode(corpus, proveniencia, contextual, callbacks) {
  _corpus = corpus;
  _proveniencia = proveniencia;
  _contextual = contextual;
  _getFilteredItems = callbacks.getFilteredItems || (() => corpus.itens);
  _getCurrentDossierItem = callbacks.getCurrentDossierItem || (() => null);

  // Carrega preferência salva
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved === 'pesquisar' || saved === 'explorar') {
    _currentMode = saved;
  }

  // Cria o toggle no header
  createModeToggle();

  // Aplica modo inicial
  applyMode(_currentMode);

  // Cria barra de exportação na seção de pesquisa
  createExportBar();

  // Cria painel de consulta técnica
  createTechnicalPanel();

  // Listener para evento de dossiê aberto (adiciona metadados técnicos se em modo pesquisar)
  document.addEventListener('dossier-opened', () => {
    if (_currentMode === 'pesquisar') {
      addTechnicalInfoToDossier();
    }
  });
}

function createModeToggle() {
  // Verifica se já existe
  if (document.getElementById('mode-toggle')) return;

  const nav = document.querySelector('.site-nav');
  if (!nav) return;

  const toggle = document.createElement('div');
  toggle.id = 'mode-toggle';
  toggle.className = 'mode-toggle';
  toggle.innerHTML = `
    <button class="mode-btn ${_currentMode === 'explorar' ? 'mode-btn--active' : ''}" data-mode="explorar" aria-pressed="${_currentMode === 'explorar'}">
      Explorar
    </button>
    <button class="mode-btn ${_currentMode === 'pesquisar' ? 'mode-btn--active' : ''}" data-mode="pesquisar" aria-pressed="${_currentMode === 'pesquisar'}">
      Pesquisar
    </button>
  `;

  toggle.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const mode = btn.dataset.mode;
      setMode(mode);
    });
  });

  nav.appendChild(toggle);
}

function setMode(mode) {
  _currentMode = mode;
  localStorage.setItem(STORAGE_KEY, mode);

  // Atualiza botões
  document.querySelectorAll('.mode-btn').forEach(btn => {
    const isActive = btn.dataset.mode === mode;
    btn.classList.toggle('mode-btn--active', isActive);
    btn.setAttribute('aria-pressed', isActive);
  });

  applyMode(mode);
}

function applyMode(mode) {
  const body = document.body;
  body.classList.remove('mode-explorar', 'mode-pesquisar');
  body.classList.add(`mode-${mode}`);

  // Mostra/esconde elementos técnicos
  const techElements = document.querySelectorAll('.technical-only');
  techElements.forEach(el => {
    el.style.display = mode === 'pesquisar' ? '' : 'none';
  });

  // Atualiza densidade da matriz
  const matrixTable = document.getElementById('matrix-table');
  if (matrixTable) {
    matrixTable.classList.toggle('matrix-table--dense', mode === 'pesquisar');
  }

  // Atualiza dossiê se aberto
  if (mode === 'pesquisar') {
    addTechnicalInfoToDossier();
  }
}

// ---------- Exportação CSV ----------

export function exportMatrixCSV() {
  const items = _getFilteredItems();
  if (!items || items.length === 0) {
    alert('Nenhum texto para exportar com os filtros atuais.');
    return;
  }

  const headers = ['texto', 'fasciculo', 'data', 'autor', 'original', 'status_original', 'rota', 'operacoes', 'tem_versao_francesa', 'rota_francesa_demonstrada'];
  const rows = [headers.join(',')];

  for (const item of items) {
    const fasc = item.fasciculos.map(f => f.numero).join(';');
    const data = item.fasciculos[0].data_iso;
    const texto = escapeCSV(item.titulo_gabinete);
    const autor = escapeCSV(item.autor_original || '');
    const original = escapeCSV(item.titulo_original || '');
    const statusOrig = item.original_identificado ? 'identificado' : (item.fonte_original_identificada.status_epistemologico === 'problematico' ? 'problematico' : 'nao_identificado');
    const rota = item.rota_tradutoria.status;
    const ops = item.operacoes_tradutorias_ids?.length || 0;
    const temFr = item.mediacao_francesa.tem_versao_francesa !== undefined ? item.mediacao_francesa.tem_versao_francesa : '';
    const rotaFr = item.mediacao_francesa.rota_para_brasil_demonstrada !== undefined ? item.mediacao_francesa.rota_para_brasil_demonstrada : '';

    rows.push([texto, fasc, data, autor, original, statusOrig, rota, ops, temFr, rotaFr].join(','));
  }

  const csv = rows.join('\n');
  downloadFile(csv, 'visaomodernidade-matriz.csv', 'text/csv;charset=utf-8');
}

function escapeCSV(value) {
  if (value === null || value === undefined) return '';
  let str = String(value);
  // Proteção contra injeção de fórmula em Excel/LibreOffice
  if (/^[=+\-@]/.test(str)) {
    str = `'${str}`;
  }
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

// ---------- Exportação JSON do dossiê ----------

export function exportDossierJSON() {
  const item = _getCurrentDossierItem();
  if (!item) {
    alert('Nenhum dossiê aberto para exportar.');
    return;
  }

  const workId = getWorkIdForCorpus(item.id);
  const brManifest = workId ? findBrazilianManifestation(workId) : null;
  const origManifest = workId ? findOriginalManifestation(workId) : null;
  const ops = workId ? findOperationsByWork(workId) : [];

  // União de evidências: do item + das operações tradutórias
  const evidenceIds = new Set([
    ...(item.evidencias_ids || []),
    ...ops.flatMap(op => op.evidence_ids || [])
  ]);
  const evidences = [...evidenceIds]
    .map(id => _proveniencia.evidencias.find(e => e.id === id))
    .filter(Boolean);

  const exportData = {
    versao_pacote: '0.8.0',
    data_exportacao: new Date().toISOString(),
    fonte_primaria: {
      obra: 'SOARES, Maria Angélica Lau Pereira. Visão da Modernidade: A Presença Britânica no Gabinete de Leitura (1837-1838). São Paulo: USP, 2006.',
      arquivo: 'TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf'
    },
    corpus_item: item,
    manifestacao_brasileira: brManifest,
    manifestacao_original: origManifest,
    operacoes_tradutorias: ops,
    evidencias: evidences
  };

  const json = JSON.stringify(exportData, null, 2);
  const slug = item.id.replace('corpus:', '');
  downloadFile(json, `visaomodernidade-dossie-${slug}.json`, 'application/json');
}

function getWorkIdForCorpus(corpusId) {
  const MAP = {
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
  return MAP[corpusId] || null;
}

function findBrazilianManifestation(workId) {
  const edges = _proveniencia.arestas.filter(a => a.origem === workId && a.tipo === 'MANIFESTA');
  for (const e of edges) {
    const node = _proveniencia.nos.find(n => n.id === e.destino);
    if (node && node.atributos.idioma === 'pt-br' && node.atributos.veiculo === 'Gabinete de Leitura') {
      return node;
    }
  }
  return null;
}

function findOriginalManifestation(workId) {
  const edges = _proveniencia.arestas.filter(a => a.origem === workId && a.tipo === 'MANIFESTA');
  for (const e of edges) {
    const node = _proveniencia.nos.find(n => n.id === e.destino);
    if (node && node.atributos.idioma === 'en') {
      return node;
    }
  }
  return null;
}

function findOperationsByWork(workId) {
  return _proveniencia.operacoes_tradutorias.filter(op => op.obra_id === workId);
}

// ---------- Copiar citação acadêmica ----------

export function copyCitation() {
  navigator.clipboard.writeText(buildCitation()).then(() => {
    const btn = document.getElementById('copy-citation-btn');
    if (btn) {
      const original = btn.textContent;
      btn.textContent = '✓ Citação copiada!';
      setTimeout(() => { btn.textContent = original; }, 2000);
    }
  }).catch(err => {
    alert('Erro ao copiar: ' + err.message);
  });
}

// ---------- Deep link de evidência ----------

export function getEvidenceDeepLink(evidenceId) {
  const baseUrl = window.location.origin + window.location.pathname;
  return `${baseUrl}#evidencia=${evidenceId}`;
}

export function copyEvidenceLink(evidenceId) {
  const url = getEvidenceDeepLink(evidenceId);
  navigator.clipboard.writeText(url).then(() => {
    // Feedback visual
  });
}

// ---------- Painel de consulta técnica ----------

function createTechnicalPanel() {
  const researchSection = document.getElementById('pesquisa');
  if (!researchSection) return;

  // Verifica se já existe
  if (document.getElementById('technical-panel')) return;

  const panel = document.createElement('div');
  panel.id = 'technical-panel';
  panel.className = 'technical-panel technical-only';
  panel.style.display = _currentMode === 'pesquisar' ? '' : 'none';
  panel.innerHTML = `
    <h3 class="section-title">Painel de Consulta Técnica</h3>
    <p class="section-intro">Disponível apenas no Modo Pesquisar. Mostra IDs, status epistêmico, método de inferência, paginação dupla e evidências relacionadas.</p>
    <div id="technical-query-result" class="technical-query-result">
      <p style="color:var(--sepia);font-style:italic;">Selecione um texto na matriz ou abra um dossiê para ver os metadados técnicos.</p>
    </div>
  `;
  researchSection.appendChild(panel);
}

export function updateTechnicalPanel(corpusId) {
  const result = document.getElementById('technical-query-result');
  if (!result || !corpusId) return;

  const item = _corpus.itens.find(i => i.id === corpusId);
  if (!item) return;

  const workId = getWorkIdForCorpus(corpusId);
  const ops = workId ? findOperationsByWork(workId) : [];
  const evidences = (item.evidencias_ids || []).map(id => _proveniencia.evidencias.find(e => e.id === id)).filter(e => e);

  let html = `
    <table class="technical-table">
      <tr><th>Corpus ID</th><td><code>${item.id}</code></td></tr>
      <tr><th>Work ID</th><td><code>${workId || '—'}</code></td></tr>
      <tr><th>Fascículo(s)</th><td>${item.fasciculos.map(f => `n.${f.numero} (${f.data_iso})`).join(', ')}</td></tr>
      <tr><th>Autor</th><td>${item.autor_original || '—'} <span class="badge badge--${item.autor_status}" style="display:inline-flex;">${item.autor_status}</span></td></tr>
      <tr><th>Original</th><td>${item.titulo_original || 'não localizado'} <span class="badge badge--${item.original_identificado ? 'identificado' : 'nao_identificado'}" style="display:inline-flex;">${item.original_identificado ? 'identificado' : 'não identificado'}</span></td></tr>
      <tr><th>Fonte declarada</th><td>${item.fonte_declarada_no_gabinete.referencia || '—'} <span class="badge badge--${item.fonte_declarada_no_gabinete.status_epistemologico}" style="display:inline-flex;">${item.fonte_declarada_no_gabinete.status_epistemologico}</span></td></tr>
      <tr><th>Rota tradutória</th><td><span class="badge badge--${item.rota_tradutoria.status}" style="display:inline-flex;">${item.rota_tradutoria.status}</span></td></tr>
      <tr><th>Mediação francesa</th>
        <td>
          tem_versao_francesa: <strong>${item.mediacao_francesa.tem_versao_francesa !== undefined ? item.mediacao_francesa.tem_versao_francesa : '—'}</strong><br>
          rota_para_brasil_demonstrada: <strong>${item.mediacao_francesa.rota_para_brasil_demonstrada !== undefined ? item.mediacao_francesa.rota_para_brasil_demonstrada : '—'}</strong><br>
          <span class="badge badge--${item.mediacao_francesa.status}" style="display:inline-flex;">${item.mediacao_francesa.status}</span>
          ${item.mediacao_francesa.metodo ? ` <span style="font-size:0.8rem;color:var(--sepia);">método: ${item.mediacao_francesa.metodo}</span>` : ''}
        </td>
      </tr>
      <tr><th>Operações tradutórias</th><td>${ops.length} operação(ões) documentada(s)</td></tr>
  `;

  if (evidences.length > 0) {
    html += `<tr><th>Evidências relacionadas</th><td>`;
    for (const ev of evidences) {
      html += `
        <div style="margin-bottom:0.5rem;">
          <code>${ev.id}</code><br>
          <small>${ev.titulo}</small><br>
          <small style="color:var(--sepia);">${ev.fonte.pagina_impressa_inicio ? `pp. ${ev.fonte.pagina_impressa_inicio}–${ev.fonte.pagina_impressa_fim}` : ''} (PDF ${ev.fonte.pagina_pdf_inicio ? `pp. ${ev.fonte.pagina_pdf_inicio}–${ev.fonte.pagina_pdf_fim}` : ''})</small>
          <button class="filter-btn" style="font-size:0.7rem;padding:2px 8px;margin-left:4px;" onclick="navigator.clipboard.writeText('${getEvidenceDeepLink(ev.id)}')">Copiar link</button>
        </div>
      `;
    }
    html += `</td></tr>`;
  }

  html += `</table>`;
  result.innerHTML = html;
}

// ---------- Utilitários ----------

function downloadFile(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function addTechnicalInfoToDossier() {
  // Adiciona IDs técnicos ao dossiê quando em modo pesquisar
  const dossierBody = document.querySelector('.dossier-body');
  if (!dossierBody) return;

  // Verifica se já foi adicionado
  if (dossierBody.querySelector('.dossier-technical')) return;

  const item = _getCurrentDossierItem();
  if (!item) return;

  const workId = getWorkIdForCorpus(item.id);
  const techDiv = document.createElement('div');
  techDiv.className = 'dossier-section dossier-technical technical-only';
  techDiv.style.display = _currentMode === 'pesquisar' ? '' : 'none';
  techDiv.innerHTML = `
    <h4>Metadados técnicos</h4>
    <div class="dossier-field">
      <div class="dossier-field-label">Corpus ID</div>
      <div class="dossier-field-value"><code>${item.id}</code></div>
    </div>
    <div class="dossier-field">
      <div class="dossier-field-label">Work ID</div>
      <div class="dossier-field-value"><code>${workId || '—'}</code></div>
    </div>
    <div class="dossier-field">
      <div class="dossier-field-label">Versão do pacote</div>
      <div class="dossier-field-value">0.8.0</div>
    </div>
    <div class="dossier-field">
      <div class="dossier-field-label">Exportar</div>
      <div class="dossier-field-value">
        <button class="filter-btn" style="font-size:0.8rem;" onclick="window.__visaomodernidade.exportDossierJSON()">Baixar dossiê em JSON</button>
        <button class="filter-btn" style="font-size:0.8rem;margin-left:4px;" onclick="window.__visaomodernidade.copyCitation()">Copiar citação</button>
      </div>
    </div>
  `;
  dossierBody.appendChild(techDiv);
}

function createExportBar() {
  // Adiciona barra de exportação na seção de matriz
  const matrixSection = document.getElementById('matriz');
  if (!matrixSection) return;

  // Verifica se já existe
  if (document.getElementById('export-bar')) return;

  const bar = document.createElement('div');
  bar.id = 'export-bar';
  bar.className = 'export-bar';
  bar.innerHTML = `
    <button class="filter-btn filter-btn--active" id="export-csv-btn">📄 Exportar resultados em CSV</button>
    <button class="filter-btn" id="copy-citation-btn">📋 Copiar citação acadêmica</button>
  `;
  matrixSection.appendChild(bar);

  document.getElementById('export-csv-btn').addEventListener('click', exportMatrixCSV);
  document.getElementById('copy-citation-btn').addEventListener('click', copyCitation);
}

// Expõe funções globalmente para uso nos botões do dossiê
window.__visaomodernidade = {
  exportDossierJSON,
  copyCitation,
  exportMatrixCSV
};
