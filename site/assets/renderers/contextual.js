/**
 * contextual.js — Grafo contextual em camadas focado em uma entidade.
 *
 * Não é um force graph aberto (que seria caótico). É uma rede em camadas
 * vertical, quase como uma genealogia editorial:
 *
 *   Pessoas → Obras → Veículos britânicos → Mediações → Gabinete → Fascículos
 *
 * Foco em uma entidade por vez. "Expandir contexto" revela camadas adicionais.
 * Estado na URL: #grafo?foco=costumes-ingleses&profundidade=2
 */

import {
  findNode, findEdges, findAuthor, findOriginalManifestation, findOriginalVenue,
  findBrazilianManifestation, findFrenchVersion, hasFrenchVersionInRevue,
  findOperationsByWork, workIdForCorpus, formatDate
} from '../data-loader.js';
import { createBadge } from './badges.js';

const FOCO_OPTIONS = [
  { id: 'costumes-ingleses', label: 'Costumes Ingleses', corpusId: 'corpus:costumes-ingleses' },
  { id: 'honras-hereditarias', label: 'As Honras Hereditárias', corpusId: 'corpus:honras-hereditarias' },
  { id: 'alibi', label: 'Álibi', corpusId: 'corpus:alibi' },
  { id: 'esbocos-sicilianos', label: 'Esboços Sicilianos', corpusId: 'corpus:esbocos-sicilianos' },
  { id: 'testamento', label: 'O Testamento', corpusId: 'corpus:testamento' },
  { id: 'livro-da-vida', label: 'O Livro da Vida', corpusId: 'corpus:livro-da-vida' },
  { id: 'sedutor', label: 'O Sedutor', corpusId: 'corpus:sedutor' },
  { id: 'manuscrito-casa-loucos', label: 'Manuscrito Achado em uma Casa de Loucos', corpusId: 'corpus:manuscrito-casa-loucos' },
  { id: 'terencio-alfaiate', label: 'Terêncio o Alfaiate', corpusId: 'corpus:terencio-alfaiate' },
  { id: 'uma-noite-no-mar', label: 'Uma Noite no Mar', corpusId: 'corpus:uma-noite-no-mar' }
];

let _foco = 'costumes-ingleses';
let _profundidade = 2; // 1 = básico, 2 = com mediações, 3 = com contexto editorial
let _onSelectText = null;

export function renderContextual(container, corpus, contextual, proveniencia, callbacks) {
  _onSelectText = callbacks.onSelectText || (() => {});

  container.innerHTML = '';

  // Introdução
  const intro = document.createElement('p');
  intro.className = 'section-intro';
  intro.innerHTML = `Rede em camadas focada em uma entidade por vez. Comece com um texto e expanda progressivamente ` +
    `para ver pessoas, veículos britânicos, mediações e o Gabinete de Leitura. ` +
    `<strong>Não é um grafo caótico</strong> — é uma genealogia editorial.`;
  container.appendChild(intro);

  // Seletor de foco
  const focoDiv = document.createElement('div');
  focoDiv.className = 'contextual-foco';
  focoDiv.innerHTML = '<label class="filters-label" for="contextual-foco-select">Foco:</label>';
  const select = document.createElement('select');
  select.id = 'contextual-foco-select';
  select.className = 'contextual-select';
  for (const opt of FOCO_OPTIONS) {
    const o = document.createElement('option');
    o.value = opt.id;
    o.textContent = opt.label;
    if (opt.id === _foco) o.selected = true;
    select.appendChild(o);
  }
  select.addEventListener('change', (e) => {
    _foco = e.target.value;
    updateURL();
    renderDiagram();
  });
  focoDiv.appendChild(select);

  // Seletor de profundidade
  const profLabel = document.createElement('label');
  profLabel.className = 'filters-label';
  profLabel.htmlFor = 'contextual-prof-select';
  profLabel.textContent = 'Profundidade:';
  focoDiv.appendChild(profLabel);
  const profSelect = document.createElement('select');
  profSelect.id = 'contextual-prof-select';
  profSelect.className = 'contextual-select';
  for (const [val, label] of [[1, '1 — Básico'], [2, '2 — Com mediações'], [3, '3 — Contexto editorial']]) {
    const o = document.createElement('option');
    o.value = val;
    o.textContent = label;
    if (val === _profundidade) o.selected = true;
    profSelect.appendChild(o);
  }
  profSelect.addEventListener('change', (e) => {
    _profundidade = parseInt(e.target.value, 10);
    updateURL();
    renderDiagram();
  });
  focoDiv.appendChild(profSelect);
  container.appendChild(focoDiv);

  // Legenda de semântica visual
  const legend = document.createElement('div');
  legend.className = 'contextual-legend';
  legend.innerHTML = `
    <div class="legend-item"><span class="legend-line legend-line--solid"></span> Documentado</div>
    <div class="legend-item"><span class="legend-line legend-line--dashed"></span> Inferido</div>
    <div class="legend-item"><span class="legend-line legend-line--blocked"></span> Lacuna / não identificado</div>
    <div class="legend-item"><span class="legend-node legend-node--person"></span> Pessoa</div>
    <div class="legend-item"><span class="legend-node legend-node--work"></span> Obra</div>
    <div class="legend-item"><span class="legend-node legend-node--periodical"></span> Periódico</div>
  `;
  container.appendChild(legend);

  // Container do diagrama
  const diagramDiv = document.createElement('div');
  diagramDiv.id = 'contextual-diagram';
  diagramDiv.className = 'contextual-diagram';
  container.appendChild(diagramDiv);

  // Carrega estado da URL
  loadFromURL();

  function renderDiagram() {
    const diagram = document.getElementById('contextual-diagram');
    diagram.innerHTML = '';

    const focoOpt = FOCO_OPTIONS.find(o => o.id === _foco);
    if (!focoOpt) return;

    const corpusItem = corpus.itens.find(i => i.id === focoOpt.corpusId);
    if (!corpusItem) return;

    const workId = workIdForCorpus(corpusItem.id);
    const author = workId ? findAuthor(proveniencia, workId) : null;
    const origManifest = workId ? findOriginalManifestation(proveniencia, workId) : null;
    const origVenue = workId ? findOriginalVenue(proveniencia, workId) : null;
    const frenchVersion = workId ? findFrenchVersion(proveniencia, workId) : null;
    const brManifest = workId ? findBrazilianManifestation(proveniencia, workId) : null;
    const ops = workId ? findOperationsByWork(proveniencia, workId) : [];

    // Camada 1: Pessoa (autor)
    if (author) {
      diagram.appendChild(createLayerNode({
        type: 'person',
        title: author.titulo,
        subtitle: author.atributos.nacionalidade || '',
        status: 'documentado',
        node: author
      }));
      diagram.appendChild(createArrow('AUTOR_DE', 'documentado'));
    } else if (corpusItem.autor_original) {
      diagram.appendChild(createLayerNode({
        type: 'person',
        title: corpusItem.autor_original,
        subtitle: 'Atribuição',
        status: corpusItem.autor_status
      }));
      diagram.appendChild(createArrow('AUTOR_DE', corpusItem.autor_status));
    }

    // Camada 2: Obra original
    if (origManifest) {
      diagram.appendChild(createLayerNode({
        type: 'work',
        title: origManifest.titulo,
        subtitle: origManifest.atributos.veiculo || '',
        status: 'identificado',
        node: origManifest
      }));
      diagram.appendChild(createArrow('PUBLICADA_ORIGINALMENTE_EM', 'identificado'));
    }

    // Camada 3: Veículo britânico
    if (origVenue) {
      diagram.appendChild(createLayerNode({
        type: 'periodical',
        title: origVenue.titulo,
        subtitle: origVenue.atributos.local || '',
        status: 'identificado'
      }));
      diagram.appendChild(createArrow('RELAÇÃO_DE_DEPENDENCIA_TEXTUAL', 'documentado'));
    } else if (corpusItem.fonte_original_identificada.veiculo) {
      diagram.appendChild(createLayerNode({
        type: 'periodical',
        title: corpusItem.fonte_original_identificada.veiculo,
        subtitle: corpusItem.fonte_original_identificada.data || '',
        status: corpusItem.fonte_original_identificada.status_epistemologico
      }));
      diagram.appendChild(createArrow('RELAÇÃO_DE_DEPENDENCIA_TEXTUAL', corpusItem.fonte_original_identificada.status_epistemologico));
    } else {
      // Lacuna: original não identificado
      diagram.appendChild(createLayerNode({
        type: 'periodical',
        title: 'Original não localizado',
        subtitle: 'Lacuna documental',
        status: 'nao_identificado'
      }));
      diagram.appendChild(createArrow('LACUNA', 'nao_identificado'));
    }

    // Camada 4: Mediação (profundidade >= 2)
    if (_profundidade >= 2) {
      if (frenchVersion) {
        diagram.appendChild(createLayerNode({
          type: 'periodical',
          title: frenchVersion.titulo,
          subtitle: 'Revue Britannique',
          status: 'documentado',
          note: corpusItem.id === 'corpus:costumes-ingleses'
            ? '⚠ Não é fonte direta da versão brasileira'
            : 'Inferida por exclusão — rota não demonstrada'
        }));
        const edgeStatus = corpusItem.id === 'corpus:costumes-ingleses' ? 'documentado' : 'inferido';
        diagram.appendChild(createArrow('TEM_VERSAO_FRANCESA_NA_REVUE', edgeStatus));
      } else if (corpusItem.mediacao_francesa.status === 'documentado') {
        // Exceção explícita
        diagram.appendChild(createLayerNode({
          type: 'periodical',
          title: 'Sem versão francesa',
          subtitle: 'Exceção explícita da tese',
          status: 'documentado'
        }));
        diagram.appendChild(createArrow('EXCECAO_REVUE_BRITANNIQUE', 'documentado'));
      }
    }

    // Camada 5: Gabinete (versão brasileira)
    if (brManifest) {
      diagram.appendChild(createLayerNode({
        type: 'periodical',
        title: brManifest.titulo,
        subtitle: `Gabinete de Leitura · ${formatDate(brManifest.atributos.data_publicacao)}`,
        status: 'documentado'
      }));
    }

    // Camada 6: Contexto editorial (profundidade >= 3) — derivado do grafo contextual JSON
    if (_profundidade >= 3) {
      diagram.appendChild(createArrow('CONTEXTO_EDITORIAL', 'documentado'));

      // Consulta nós reais do grafo contextual
      const ctxNodes = [
        { id: 'tipografia:commercial', label: 'Tipografia Commercial' },
        { id: 'livraria:h-e-laemmert', label: 'Livraria H. & E. Laemmert' },
        { id: 'periodico:o-chronista', label: 'O Chronista' },
        { id: 'periodico:revue-britannique', label: 'Revue Britannique' }
      ];

      for (const ctxRef of ctxNodes) {
        const node = findNode(contextual, ctxRef.id);
        if (node) {
          // Deriva subtítulo dos atributos do nó
          let subtitle = '';
          if (node.atributos) {
            if (node.atributos.proprietario) subtitle = node.atributos.proprietario;
            else if (node.atributos.proprietarios) subtitle = node.atributos.proprietarios.join(', ');
            else if (node.atributos.periodo_inicio) subtitle = `${node.atributos.periodo_inicio}–${node.atributos.periodo_fim || ''}`;
            else if (node.atributos.local) subtitle = node.atributos.local;
            else if (node.atributos.papel) subtitle = node.atributos.papel;
          }
          diagram.appendChild(createLayerNode({
            type: 'periodical',
            title: node.titulo,
            subtitle: subtitle,
            status: node.status_epistemologico,
            node: node
          }));
        } else {
          // Fallback: se o nó não existir no grafo, mostra como lacuna
          console.warn(`Nó contextual não encontrado no JSON: ${ctxRef.id}`);
          diagram.appendChild(createLayerNode({
            type: 'periodical',
            title: ctxRef.label,
            subtitle: 'Nó não encontrado no grafo contextual',
            status: 'nao_identificado'
          }));
        }
      }
    }

    // Camada 7: Operações tradutórias (se houver)
    if (ops.length > 0) {
      diagram.appendChild(createArrow('OPERACOES_TRADUTORIAS', 'documentado'));
      for (const op of ops) {
        diagram.appendChild(createLayerNode({
          type: 'work',
          title: op.titulo,
          subtitle: op.tipo_operacao,
          status: op.status_epistemologico,
          node: op
        }));
      }
    }
  }

  function updateURL() {
    const newHash = `#grafo?foco=${_foco}&profundidade=${_profundidade}`;
    if (window.location.hash !== newHash) {
      // pushState: mudança de foco/profundidade é ação explícita do usuário
      history.pushState(null, '', newHash);
    }
  }

  function loadFromURL() {
    const hash = window.location.hash;
    const match = hash.match(/#grafo\?foco=([\w-]+)&profundidade=(\d+)/);
    if (match) {
      _foco = match[1];
      _profundidade = parseInt(match[2], 10);
      // Atualiza selects
      const focoSelect = document.getElementById('contextual-foco-select');
      const profSelect = document.getElementById('contextual-prof-select');
      if (focoSelect) focoSelect.value = _foco;
      if (profSelect) profSelect.value = _profundidade;
    }
  }

  renderDiagram();
}

function createLayerNode({ type, title, subtitle, status, note, node }) {
  const div = document.createElement('div');
  div.className = `layer-node layer-node--${type}`;

  const icon = type === 'person' ? '👤' : type === 'work' ? '📖' : '📰';

  div.innerHTML = `
    <div class="layer-node-icon">${icon}</div>
    <div class="layer-node-content">
      <div class="layer-node-title">${title}</div>
      ${subtitle ? `<div class="layer-node-subtitle">${subtitle}</div>` : ''}
      ${note ? `<div class="layer-node-note">${note}</div>` : ''}
    </div>
  `;

  const badge = createBadge(status);
  badge.style.marginTop = '4px';
  div.appendChild(badge);

  if (node) {
    div.dataset.nodeId = node.id;
    // Torna o nó focalizável para acessibilidade
    div.setAttribute('tabindex', '0');
    div.setAttribute('role', 'button');
    div.setAttribute('aria-label', `Ver detalhes: ${node.titulo}`);
    div.addEventListener('click', () => {
      // Guarda referência ao elemento clicado para retorno de foco
      showNodeDetails(node, div);
    });
    div.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        showNodeDetails(node, div);
      }
    });
    div.style.cursor = 'pointer';
  }

  return div;
}

function createArrow(label, status) {
  const arrow = document.createElement('div');
  arrow.className = `layer-arrow layer-arrow--${status}`;
  arrow.innerHTML = `
    <div class="layer-arrow-line"></div>
    <div class="layer-arrow-label">${label}</div>
  `;
  return arrow;
}

function showNodeDetails(node, triggerEl) {
  // Remove modal existente
  const existing = document.getElementById('node-details-modal');
  if (existing) existing.remove();

  // Guarda o elemento que abriu o modal para retornar o foco depois
  // Prioriza o triggerEl passado explicitamente; fallback para activeElement
  const trigger = triggerEl || document.activeElement;

  const overlay = document.createElement('div');
  overlay.id = 'node-details-modal';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-labelledby', 'node-details-title');
  overlay.style.cssText = `
    position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:400;
    display:flex;align-items:center;justify-content:center;padding:1rem;
  `;

  const modal = document.createElement('div');
  modal.style.cssText = `
    background:var(--paper-light);border-radius:12px;max-width:500px;width:100%;
    max-height:70vh;overflow-y:auto;padding:1.5rem;box-shadow:0 8px 32px rgba(0,0,0,0.3);
  `;

  const closeBtn = document.createElement('button');
  closeBtn.id = 'node-details-close';
  closeBtn.setAttribute('aria-label', 'Fechar modal de detalhes do nó');
  closeBtn.style.cssText = `
    float:right;background:var(--sepia-dark);color:var(--paper);border:none;
    border-radius:50%;width:28px;height:28px;font-size:1rem;cursor:pointer;
  `;
  closeBtn.textContent = '✕';

  const title = document.createElement('h4');
  title.id = 'node-details-title';
  title.textContent = node.titulo;
  title.style.cssText = 'margin:0 0 0.5rem;color:var(--green-dark);';

  const idDiv = document.createElement('div');
  idDiv.style.cssText = 'font-family:var(--font-mono);font-size:0.8rem;color:var(--sepia);margin-bottom:0.5rem;';
  idDiv.textContent = `ID: ${node.id}`;

  modal.appendChild(closeBtn);
  modal.appendChild(title);
  modal.appendChild(idDiv);

  if (node.atributos) {
    const attrs = document.createElement('div');
    attrs.style.cssText = 'font-size:0.9rem;';
    for (const [k, v] of Object.entries(node.atributos)) {
      if (v !== null && v !== undefined) {
        const attr = document.createElement('div');
        attr.style.cssText = 'margin-bottom:0.25rem;';
        attr.innerHTML = `<strong>${k}:</strong> ${typeof v === 'object' ? JSON.stringify(v) : v}`;
        attrs.appendChild(attr);
      }
    }
    modal.appendChild(attrs);
  }

  overlay.appendChild(modal);

  // Função para fechar e retornar foco
  const closeModal = () => {
    overlay.remove();
    if (trigger && typeof trigger.focus === 'function') {
      trigger.focus();
    }
    document.removeEventListener('keydown', onKeyDown);
  };

  // Fechamento: clique fora
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeModal();
  });

  // Fechamento: botão
  closeBtn.addEventListener('click', closeModal);

  // Fechamento: Escape
  const onKeyDown = (e) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      closeModal();
    }
    // Trap de foco simples: se Tab no último elemento, volta para o primeiro
    if (e.key === 'Tab') {
      const focusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (focusable.length === 0) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  };
  document.addEventListener('keydown', onKeyDown);

  document.body.appendChild(overlay);

  // Foco automático no botão fechar
  setTimeout(() => closeBtn.focus(), 50);
}
