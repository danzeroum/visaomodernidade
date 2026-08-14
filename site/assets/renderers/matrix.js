/**
 * matrix.js — Matriz filtrável do corpus com busca por sintaxe.
 *
 * Funcionalidades:
 *   - Tabela dos 10 textos com colunas: Texto, Fascículo, Original, Rota, Alterações, Certeza
 *   - Busca textual simples (título, autor, fascículo, fonte)
 *   - Busca com sintaxe: status:problematico, autor:bulwer, fasciculo:30, fonte:revue, operacao:ironia
 *   - Filtros por pergunta narrativa (atalhos que aplicam filtros automáticos)
 *   - Colunas clicáveis: Texto→dossiê, Fascículo→timeline, Original→rota, Alterações→laboratório, Certeza→explicação
 *   - Navegação por teclado (j/k para baixo/cima, Enter para abrir)
 *   - Estado dos filtros refletido na URL (#matriz?status=problematico)
 */

import { workIdForCorpus, findAuthor, findOperationsByWork, findOriginalManifestation, findOriginalVenue } from '../data-loader.js';
import { createBadge } from './badges.js';

// ---------- Perguntas narrativas (filtros prontos) ----------
const PERGUNTAS = [
  {
    id: 'nao-sabemos',
    label: 'O que ainda não sabemos?',
    descricao: 'Textos com original não localizado, atribuição problemática ou rota indeterminada',
    filtro: (item) => !item.original_identificado || item.autor_status === 'problematico' || item.rota_tradutoria.status === 'nao_identificado'
  },
  {
    id: 'franca',
    label: 'Quais textos tiveram versão francesa identificada?',
    descricao: 'Textos com versão francesa na Revue Britannique (inclui os 7 inferidos por exclusão + Costumes Ingleses que tem versão mas não é fonte direta)',
    filtro: (item) => item.mediacao_francesa.tem_versao_francesa === true
  },
  {
    id: 'franca-inferida',
    label: 'Quais rotas via França são apenas inferidas?',
    descricao: 'Textos cuja versão francesa foi inferida por exclusão (rota não demonstrada caso a caso)',
    filtro: (item) => item.mediacao_francesa.status === 'inferido'
  },
  {
    id: 'mudou-sentido',
    label: 'Onde a tradução mudou o sentido?',
    descricao: 'Textos com operações tradutórias documentadas pela tese',
    filtro: (item, prov) => {
      const workId = workIdForCorpus(item.id);
      return workId && findOperationsByWork(prov, workId).length > 0;
    }
  },
  {
    id: 'critica-sociedade',
    label: 'Quais narrativas criticam a sociedade?',
    descricao: 'Textos cuja análise da tese versa sobre crítica social',
    filtro: (item) => ['corpus:costumes-ingleses', 'corpus:honras-hereditarias', 'corpus:alibi', 'corpus:esbocos-sicilianos'].includes(item.id)
  },
  {
    id: 'sem-original',
    label: 'Quais textos não têm original identificado?',
    descricao: 'Original não localizado pela tese',
    filtro: (item) => !item.original_identificado
  },
  {
    id: 'fonte-problematica',
    label: 'Quais textos têm fonte problemática?',
    descricao: 'Fonte declarada no Gabinete é inconsistente',
    filtro: (item) => item.fonte_declarada_no_gabinete.status_epistemologico === 'problematico'
  },
  {
    id: 'serializado',
    label: 'Quais textos foram serializados?',
    descricao: 'Publicação em mais de um fascículo',
    filtro: (item) => item.fasciculos.length > 1
  }
];

// ---------- Parser de sintaxe de busca ----------
function parseQuery(raw) {
  const result = {
    text: '',           // busca textual livre
    status: null,        // status:problematico
    autor: null,         // autor:bulwer
    fasciculo: null,     // fasciculo:30
    fonte: null,         // fonte:revue
    operacao: null       // operacao:ironia
  };
  if (!raw) return result;

  const tokens = raw.trim().split(/\s+/);
  const freeTextParts = [];

  for (const token of tokens) {
    const colonIdx = token.indexOf(':');
    if (colonIdx > 0) {
      const key = token.substring(0, colonIdx).toLowerCase();
      const value = token.substring(colonIdx + 1).toLowerCase();
      if (key in result) {
        result[key] = value;
      } else {
        freeTextParts.push(token);
      }
    } else {
      freeTextParts.push(token);
    }
  }
  result.text = freeTextParts.join(' ').toLowerCase();
  return result;
}

function matchesItem(item, query, proveniencia) {
  // Busca textual livre
  if (query.text) {
    const haystack = [
      item.titulo_gabinete,
      item.titulo_original || '',
      item.autor_original || '',
      item.fasciculos.map(f => `n.${f.numero}`).join(' '),
      item.fonte_declarada_no_gabinete.referencia || '',
      item.fonte_original_identificada.veiculo || ''
    ].join(' ').toLowerCase();
    if (!haystack.includes(query.text)) return false;
  }

  // status:problematico
  if (query.status) {
    const statusMap = {
      'problematico': item.fonte_declarada_no_gabinete.status_epistemologico === 'problematico' || item.autor_status === 'problematico',
      'documentado': item.rota_tradutoria.status === 'documentado',
      'inferido': item.mediacao_francesa.status === 'inferido',
      'identificado': item.autor_status === 'identificado',
      'nao_identificado': item.rota_tradutoria.status === 'nao_identificado' || !item.original_identificado
    };
    if (!statusMap[query.status]) return false;
  }

  // autor:bulwer
  if (query.autor) {
    if (!(item.autor_original || '').toLowerCase().includes(query.autor)) return false;
  }

  // fasciculo:30
  if (query.fasciculo) {
    const num = parseInt(query.fasciculo, 10);
    if (!item.fasciculos.some(f => f.numero === num)) return false;
  }

  // fonte:revue
  if (query.fonte) {
    const fonteStr = (item.fonte_declarada_no_gabinete.referencia || '') + ' ' +
                     (item.fonte_original_identificada.veiculo || '') + ' ' +
                     (item.mediacao_francesa.status === 'inferido' || item.mediacao_francesa.status === 'documentado' ? 'revue britannique' : '');
    if (!fonteStr.toLowerCase().includes(query.fonte)) return false;
  }

  // operacao:ironia
  if (query.operacao) {
    const workId = workIdForCorpus(item.id);
    if (!workId) return false;
    const ops = findOperationsByWork(proveniencia, workId);
    const hasOp = ops.some(op =>
      op.tipo_operacao.toLowerCase().includes(query.operacao) ||
      op.titulo.toLowerCase().includes(query.operacao)
    );
    if (!hasOp) return false;
  }

  return true;
}

// ---------- Renderização ----------
let _activePergunta = null;
let _currentQuery = '';
let _onSelectText = null;
let _onFocusFasciculo = null;
let _onOpenLab = null;

export function renderMatrix(container, corpus, proveniencia, callbacks) {
  _onSelectText = callbacks.onSelectText || (() => {});
  _onFocusFasciculo = callbacks.onFocusFasciculo || (() => {});
  _onOpenLab = callbacks.onOpenLab || (() => {});

  container.innerHTML = '';

  // Introdução
  const intro = document.createElement('p');
  intro.className = 'section-intro';
  intro.innerHTML = `Matriz dos <strong>10 textos britânicos</strong> com filtros por pergunta de pesquisa e busca com sintaxe. ` +
    `Clique nas colunas para navegar: <strong>Texto</strong> abre dossiê, <strong>Fascículo</strong> focaliza timeline, ` +
    `<strong>Alterações</strong> abre laboratório.`;
  container.appendChild(intro);

  // Busca
  const searchDiv = document.createElement('div');
  searchDiv.className = 'matrix-search';
  searchDiv.innerHTML = `
    <div class="search-wrapper">
      <input type="search" id="matrix-search-input" class="search-input"
             placeholder="Buscar por título, autor, fascículo, fonte… ou use status:problematico autor:bulwer"
             aria-label="Buscar textos"
             autocomplete="off">
      <kbd class="search-hint">Sintaxe: status:  autor:  fasciculo:  fonte:  operacao:</kbd>
    </div>
  `;
  container.appendChild(searchDiv);

  // Perguntas narrativas
  const perguntasDiv = document.createElement('div');
  perguntasDiv.className = 'perguntas-narrativas';
  perguntasDiv.innerHTML = '<div class="perguntas-label">Perguntas de pesquisa:</div>';

  const perguntasList = document.createElement('div');
  perguntasList.className = 'perguntas-list';

  // Botão "Todas" (limpa filtros)
  const todasBtn = document.createElement('button');
  todasBtn.className = 'pergunta-btn pergunta-btn--active';
  todasBtn.dataset.id = 'todas';
  todasBtn.textContent = 'Todos os textos';
  todasBtn.addEventListener('click', () => {
    _activePergunta = null;
    document.getElementById('matrix-search-input').value = '';
    _currentQuery = '';
    updatePerguntaButtons('todas');
    updateURL();
    renderTable();
  });
  perguntasList.appendChild(todasBtn);

  for (const p of PERGUNTAS) {
    const btn = document.createElement('button');
    btn.className = 'pergunta-btn';
    btn.dataset.id = p.id;
    btn.textContent = p.label;
    btn.title = p.descricao;
    btn.addEventListener('click', () => {
      _activePergunta = _activePergunta === p.id ? null : p.id;
      document.getElementById('matrix-search-input').value = '';
      _currentQuery = '';
      updatePerguntaButtons(_activePergunta || 'todas');
      updateURL();
      renderTable();
    });
    perguntasList.appendChild(btn);
  }
  perguntasDiv.appendChild(perguntasList);
  container.appendChild(perguntasDiv);

  // Tabela
  const tableWrap = document.createElement('div');
  tableWrap.className = 'matrix-table-wrap';
  tableWrap.innerHTML = `
    <table class="matrix-table" id="matrix-table">
      <thead>
        <tr>
          <th scope="col">Texto</th>
          <th scope="col">Fascículo</th>
          <th scope="col">Original</th>
          <th scope="col">Rota</th>
          <th scope="col" title="Número de operações tradutórias documentadas">Alterações</th>
          <th scope="col">Certeza</th>
        </tr>
      </thead>
      <tbody id="matrix-tbody"></tbody>
    </table>
  `;
  container.appendChild(tableWrap);

  // Contador de resultados
  const counter = document.createElement('div');
  counter.className = 'matrix-counter';
  counter.id = 'matrix-counter';
  container.appendChild(counter);

  // Listener de busca
  const input = document.getElementById('matrix-search-input');
  input.addEventListener('input', (e) => {
    _currentQuery = e.target.value;
    if (_currentQuery) {
      _activePergunta = null;
      updatePerguntaButtons('todas');
    }
    updateURL();
    renderTable();
  });

  // Navegação por teclado na tabela
  container.addEventListener('keydown', (e) => {
    const rows = container.querySelectorAll('.matrix-row');
    if (rows.length === 0) return;
    const current = document.activeElement.closest('.matrix-row');
    let idx = current ? Array.from(rows).indexOf(current) : -1;
    if (e.key === 'ArrowDown' || e.key === 'j') {
      e.preventDefault();
      idx = Math.min(rows.length - 1, idx + 1);
      rows[idx].focus();
    } else if (e.key === 'ArrowUp' || e.key === 'k') {
      e.preventDefault();
      idx = Math.max(0, idx - 1);
      rows[idx].focus();
    } else if (e.key === 'Enter' && current) {
      e.preventDefault();
      const corpusId = current.dataset.corpusId;
      _onSelectText(corpusId);
    }
  });

  // Carrega estado da URL
  loadFromURL();

  function renderTable() {
    const tbody = document.getElementById('matrix-tbody');
    tbody.innerHTML = '';

    let items = corpus.itens;

    // Aplica pergunta narrativa ativa
    if (_activePergunta) {
      const p = PERGUNTAS.find(p => p.id === _activePergunta);
      if (p) {
        items = items.filter(item => p.filtro(item, proveniencia));
      }
    }

    // Aplica busca
    if (_currentQuery) {
      const query = parseQuery(_currentQuery);
      items = items.filter(item => matchesItem(item, query, proveniencia));
    }

    // Renderiza linhas
    for (const item of items) {
      const row = createRow(item, proveniencia);
      tbody.appendChild(row);
    }

    // Contador
    const counter = document.getElementById('matrix-counter');
    if (items.length === 0) {
      counter.innerHTML = '<em>Nenhum texto encontrado com os filtros atuais.</em>';
    } else {
      counter.innerHTML = `<strong>${items.length}</strong> de ${corpus.itens.length} textos exibidos.`;
    }

    // Notifica timeline para destacar fascículos filtrados
    const fasciculosAtivos = items.flatMap(i => i.fasciculos.map(f => f.numero));
    _onFocusFasciculo(fasciculosAtivos);
  }

  function updatePerguntaButtons(activeId) {
    container.querySelectorAll('.pergunta-btn').forEach(b => {
      b.classList.toggle('pergunta-btn--active', b.dataset.id === activeId);
    });
  }

  function updateURL() {
    const params = new URLSearchParams();
    if (_activePergunta) {
      params.set('pergunta', _activePergunta);
    }
    if (_currentQuery) {
      params.set('q', _currentQuery);
    }
    const newHash = params.toString()
      ? `#matriz?${params.toString()}`
      : '#matriz';
    if (window.location.hash !== newHash) {
      history.replaceState(null, '', newHash);
    }
  }

  function loadFromURL() {
    const hash = window.location.hash;
    const matrixIdx = hash.indexOf('#matriz');
    if (matrixIdx === -1) return;
    const queryString = hash.substring(matrixIdx + 7).replace(/^\?/, '');
    const params = new URLSearchParams(queryString);
    const pergunta = params.get('pergunta');
    const q = params.get('q');
    if (pergunta && PERGUNTAS.some(p => p.id === pergunta)) {
      _activePergunta = pergunta;
      updatePerguntaButtons(pergunta);
    }
    if (q) {
      _currentQuery = q;
      document.getElementById('matrix-search-input').value = q;
    }
  }

  // Renderiza pela primeira vez
  renderTable();
}

function createRow(item, proveniencia) {
  const tr = document.createElement('tr');
  tr.className = 'matrix-row';
  tr.tabIndex = 0;
  tr.dataset.corpusId = item.id;

  const workId = workIdForCorpus(item.id);
  const opsCount = workId ? findOperationsByWork(proveniencia, workId).length : 0;
  const fascStr = item.fasciculos.map(f => `n.${f.numero}`).join('–');
  const dataStr = item.fasciculos[0].data_iso;

  // Coluna: Texto (clicável → dossiê)
  const tdTexto = document.createElement('td');
  tdTexto.className = 'col-texto';
  tdTexto.innerHTML = `
    <strong>${item.titulo_gabinete}</strong>
    ${item.autor_original ? `<br><small class="muted">${item.autor_original}</small>` : '<br><small class="muted">Autor não identificado</small>'}
  `;
  tdTexto.addEventListener('click', () => _onSelectText(item.id));
  tr.appendChild(tdTexto);

  // Coluna: Fascículo (clicável → timeline)
  const tdFasc = document.createElement('td');
  tdFasc.className = 'col-fasciculo';
  tdFasc.innerHTML = `<span class="fasc-link" title="Focalizar na timeline">${fascStr}</span><br><small class="muted">${formatDateShort(dataStr)}</small>`;
  tdFasc.addEventListener('click', () => {
    const firstFasc = item.fasciculos[0].numero;
    _onFocusFasciculo([firstFasc], true); // true = scroll to timeline
  });
  tr.appendChild(tdFasc);

  // Coluna: Original (clicável → rota no dossiê)
  const tdOriginal = document.createElement('td');
  tdOriginal.className = 'col-original';
  if (item.titulo_original) {
    tdOriginal.innerHTML = `<em>${item.titulo_original}</em>`;
  } else {
    tdOriginal.innerHTML = '<span class="muted">não localizado</span>';
  }
  const origBadge = createBadge(
    item.original_identificado ? 'identificado' :
    item.fonte_original_identificada.status_epistemologico === 'problematico' ? 'problematico' :
    'nao_identificado'
  );
  origBadge.style.marginTop = '4px';
  origBadge.style.display = 'inline-flex';
  tdOriginal.appendChild(document.createElement('br'));
  tdOriginal.appendChild(origBadge);
  tdOriginal.addEventListener('click', () => _onSelectText(item.id));
  tr.appendChild(tdOriginal);

  // Coluna: Rota
  const tdRota = document.createElement('td');
  tdRota.className = 'col-rota';
  const rotaLabel = {
    'documentado': 'Documentada',
    'identificado': 'Identificada',
    'inferido': 'Inferida',
    'hipotese': 'Hipotética',
    'problematico': 'Problemática',
    'nao_identificado': 'Indeterminada'
  }[item.rota_tradutoria.status] || item.rota_tradutoria.status;
  tdRota.innerHTML = `<span class="rota-label">${rotaLabel}</span>`;
  tdRota.appendChild(createBadge(item.rota_tradutoria.status));
  tr.appendChild(tdRota);

  // Coluna: Alterações (clicável → laboratório)
  const tdOps = document.createElement('td');
  tdOps.className = 'col-ops';
  if (opsCount > 0) {
    tdOps.innerHTML = `<span class="ops-link" title="Abrir no laboratório de tradução">${opsCount} operação${opsCount > 1 ? 'ões' : ''}</span>`;
    tdOps.addEventListener('click', () => _onOpenLab(item.id));
  } else {
    tdOps.innerHTML = '<span class="muted">—</span>';
  }
  tr.appendChild(tdOps);

  // Coluna: Certeza
  const tdCerteza = document.createElement('td');
  tdCerteza.className = 'col-certeza';
  const certezaStatus = item.fonte_declarada_no_gabinete.status_epistemologico === 'problematico'
    ? 'problematico'
    : (item.rota_tradutoria.status === 'documentado' ? 'documentado' :
       item.rota_tradutoria.status === 'nao_identificado' ? 'nao_identificado' : 'identificado');
  tdCerteza.appendChild(createBadge(certezaStatus));
  tr.appendChild(tdCerteza);

  return tr;
}

function formatDateShort(iso) {
  if (!iso) return '';
  const [y, m, d] = iso.split('-');
  const months = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
  return `${parseInt(d)} ${months[parseInt(m) - 1]} ${y}`;
}
