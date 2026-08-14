/**
 * app.js — Orquestrador principal do site estático (Sprint 3).
 *
 * Responsabilidades:
 *   1. Carregar os JSONs via data-loader.js
 *   2. Gerenciar estados (loading, ready, warning, error)
 *   3. Renderizar timeline, matriz, trilhas, dossiê, laboratório, grafo contextual
 *   4. Deep links (estado na URL: #texto=, #matriz?, #trilha=, #grafo?)
 *   5. Ficha de confiabilidade global
 */

import { loadAll, ESTADO } from './data-loader.js';
import { renderTimeline } from './renderers/timeline.js';
import { openDossier, closeDossier } from './renderers/dossier.js';
import { renderTranslationLab } from './renderers/translation-lab.js';
import { renderMatrix } from './renderers/matrix.js';
import { renderTrails } from './renderers/trails.js';
import { renderContextual } from './renderers/contextual.js';
import { createBadge, createBadgeLegend } from './renderers/badges.js';

const state = {
  corpus: null,
  contextual: null,
  proveniencia: null,
  validacao: null,
  estado: ESTADO.LOADING,
  selectedCorpusId: null
};

document.addEventListener('DOMContentLoaded', init);

async function init() {
  showStateBanner(ESTADO.LOADING, 'Carregando dados acadêmicos…');
  await loadSvgSprite();
  const result = await loadAll();
  state.corpus = result.corpus;
  state.contextual = result.contextual;
  state.proveniencia = result.proveniencia;
  state.validacao = result.validacao;
  state.estado = result.estado;

  if (state.estado === ESTADO.ERROR) {
    showStateBanner(ESTADO.ERROR, result.mensagem);
    showError(result.mensagem);
    return;
  }

  if (state.estado === ESTADO.WARNING) {
    showStateBanner(ESTADO.WARNING, result.mensagem);
  } else {
    hideStateBanner();
  }

  renderAll();
  handleDeepLinks();
}

function showStateBanner(estado, mensagem) {
  const banner = document.getElementById('state-banner');
  if (!banner) return;
  banner.className = `state-banner state-banner--${estado}`;
  banner.textContent = mensagem;
  banner.style.display = 'block';
}

function hideStateBanner() {
  const banner = document.getElementById('state-banner');
  if (!banner) return;
  banner.style.display = 'none';
}

function showError(mensagem) {
  const main = document.getElementById('site-main');
  if (!main) return;
  main.innerHTML = `
    <div class="loading-message">
      <div style="font-size:3rem;margin-bottom:1rem;">⚠</div>
      <h2 style="color:var(--st-problematico);">Não foi possível carregar os dados</h2>
      <p>${mensagem}</p>
    </div>
  `;
}

function renderAll() {
  renderHeroStats();

  // Timeline
  const timelineContainer = document.getElementById('timeline');
  if (timelineContainer) {
    renderTimeline(timelineContainer, state.corpus, (fascNum, corpusItem) => {
      openDossierForCorpusId(corpusItem.id);
    });
  }

  // Lista de textos
  const listContainer = document.getElementById('text-list');
  if (listContainer) {
    renderTextList(listContainer);
  }

  // Laboratório de tradução
  const labContainer = document.getElementById('translation-lab');
  if (labContainer) {
    renderTranslationLab(labContainer, state.proveniencia);
  }

  // Matriz
  const matrixContainer = document.getElementById('matrix-container');
  if (matrixContainer) {
    renderMatrix(matrixContainer, state.corpus, state.proveniencia, {
      onSelectText: (corpusId) => openDossierForCorpusId(corpusId),
      onFocusFasciculo: (fasciculos, scrollToTimeline) => {
        highlightFasciculos(fasciculos);
        if (scrollToTimeline) {
          document.getElementById('periodico').scrollIntoView({ behavior: 'smooth' });
        }
      },
      onOpenLab: (corpusId) => {
        const workId = workIdForCorpus(corpusId);
        if (workId) {
          // Scroll to lab and trigger the right option
          document.getElementById('laboratorio').scrollIntoView({ behavior: 'smooth' });
          // The lab has its own selector; we'd need to expose a setter
          // For now, just scroll
        }
      }
    });
  }

  // Trilhas
  const trailsContainer = document.getElementById('trails-container');
  if (trailsContainer) {
    renderTrails(trailsContainer, {
      onSelectText: (corpusId) => openDossierForCorpusId(corpusId)
    });
  }

  // Grafo contextual
  const contextualContainer = document.getElementById('contextual-container');
  if (contextualContainer) {
    renderContextual(contextualContainer, state.corpus, state.contextual, state.proveniencia, {
      onSelectText: (corpusId) => openDossierForCorpusId(corpusId)
    });
  }

  // Legenda de badges
  const legendContainer = document.getElementById('badge-legend');
  if (legendContainer) {
    legendContainer.appendChild(createBadgeLegend());
  }

  // Ficha de confiabilidade
  renderConfidenceCard();

  // Footer meta
  renderFooterMeta();
}

function renderHeroStats() {
  document.querySelectorAll('.stat-num').forEach(el => {
    const target = parseInt(el.textContent, 10);
    if (isNaN(target)) return;
    let current = 0;
    const step = Math.max(1, Math.floor(target / 30));
    const interval = setInterval(() => {
      current = Math.min(target, current + step);
      el.textContent = current;
      if (current >= target) clearInterval(interval);
    }, 30);
  });
}

function renderTextList(container) {
  container.innerHTML = '';
  for (const item of state.corpus.itens) {
    const card = document.createElement('div');
    card.className = 'text-card';
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    card.dataset.corpusId = item.id;

    const fasciculos = item.fasciculos.map(f => `n.${f.numero}`).join('–');
    const data = item.fasciculos[0].data_iso;

    card.innerHTML = `
      <div class="text-card-fasc">${fasciculos} · ${formatDateShort(data)}</div>
      <h3 class="text-card-title">${item.titulo_gabinete}</h3>
      ${item.autor_original
        ? `<div class="text-card-author">${item.autor_original}</div>`
        : `<div class="text-card-author" style="color:var(--sepia);">Autor não identificado</div>`
      }
      ${item.titulo_original
        ? `<div class="text-card-original">↳ <em>${item.titulo_original}</em></div>`
        : ''
      }
      <div class="text-card-badges"></div>
    `;

    const badgesDiv = card.querySelector('.text-card-badges');
    badgesDiv.appendChild(createBadge(item.autor_status, 'Autor'));

    if (item.original_identificado) {
      badgesDiv.appendChild(createBadge('identificado', 'Original'));
    } else if (item.fonte_original_identificada.status_epistemologico === 'problematico') {
      badgesDiv.appendChild(createBadge('problematico', 'Original'));
    } else {
      badgesDiv.appendChild(createBadge('nao_identificado', 'Original'));
    }

    badgesDiv.appendChild(createBadge(item.rota_tradutoria.status, 'Rota'));

    card.addEventListener('click', () => openDossierForCorpusId(item.id));
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openDossierForCorpusId(item.id);
      }
    });

    container.appendChild(card);
  }
}

function formatDateShort(iso) {
  if (!iso) return '';
  const [y, m, d] = iso.split('-');
  const months = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
  return `${parseInt(d)} ${months[parseInt(m) - 1]} ${y}`;
}

function openDossierForCorpusId(corpusId) {
  state.selectedCorpusId = corpusId;
  const item = state.corpus.itens.find(i => i.id === corpusId);
  if (!item) return;

  const overlay = document.getElementById('dossier-overlay');
  const panel = document.getElementById('dossier-panel');
  openDossier(overlay, panel, item, state.proveniencia);

  // Deep link
  updateDeepLink(`#texto=${corpusId.replace('corpus:', '')}`);

  // Marca card selecionado
  document.querySelectorAll('.text-card').forEach(c => {
    c.classList.toggle('text-card--selected', c.dataset.corpusId === corpusId);
  });
}

function highlightFasciculos(fasciculos) {
  // Remove highlights anteriores
  document.querySelectorAll('.timeline-dot--highlighted').forEach(el => {
    el.classList.remove('timeline-dot--highlighted');
  });
  // Adiciona highlight nos fascículos ativos
  for (const num of fasciculos) {
    const dots = document.querySelectorAll('.timeline-dot');
    for (const dot of dots) {
      const numEl = dot.querySelector('.timeline-dot-num');
      if (numEl && parseInt(numEl.textContent, 10) === num) {
        dot.classList.add('timeline-dot--highlighted');
        break;
      }
    }
  }
}

function renderConfidenceCard() {
  const card = document.getElementById('confidence-card');
  if (!card || !state.validacao || !state.corpus) return;

  const stats = state.validacao.estatisticas || {};
  const corpus = state.corpus;
  let documentados = 0, inferidos = 0, lacunas = 0, problematicos = 0;
  for (const item of corpus.itens) {
    if (item.fonte_declarada_no_gabinete.status_epistemologico === 'documentado') documentados++;
    if (item.mediacao_francesa.status === 'inferido') inferidos++;
    if (!item.original_identificado) lacunas++;
    if (item.fonte_declarada_no_gabinete.status_epistemologico === 'problematico') problematicos++;
  }

  card.innerHTML = `
    <div class="evidence-meta">
      <div class="evidence-meta-item">
        <span class="evidence-meta-label">Dados verificados</span>
        <span class="evidence-meta-value">${documentados}</span>
      </div>
      <div class="evidence-meta-item">
        <span class="evidence-meta-label">Inferências</span>
        <span class="evidence-meta-value">${inferidos}</span>
      </div>
      <div class="evidence-meta-item">
        <span class="evidence-meta-label">Lacunas</span>
        <span class="evidence-meta-value">${lacunas}</span>
      </div>
      <div class="evidence-meta-item">
        <span class="evidence-meta-label">Fontes problemáticas</span>
        <span class="evidence-meta-value">${problematicos}</span>
      </div>
      <div class="evidence-meta-item">
        <span class="evidence-meta-label">Última validação</span>
        <span class="evidence-meta-value">${state.validacao.data_validacao || '—'}</span>
      </div>
      <div class="evidence-meta-item">
        <span class="evidence-meta-label">Versão dos dados</span>
        <span class="evidence-meta-value">${corpus.versao}</span>
      </div>
    </div>
    <p style="margin-top:0.5rem;font-size:0.85rem;color:var(--sepia);">
      <strong>Validação semântica: <span style="color:var(--st-documentado);">${state.validacao.resultado}</span></strong>
      · ${state.validacao.erros?.length || 0} erros, ${state.validacao.avisos?.length || 0} avisos informativos
    </p>
  `;
}

function renderFooterMeta() {
  const el = document.getElementById('footer-meta');
  if (!el || !state.validacao) return;
  const stats = state.validacao.estatisticas || {};
  el.innerHTML = `
    ${stats.nos_contextual || 0} nós contextuais ·
    ${stats.nos_proveniencia || 0} nós de proveniência ·
    ${stats.evidencias || 0} evidências ·
    ${stats.operacoes_tradutorias || 0} operações tradutórias ·
    Validação: <strong style="color:var(--gold);">${state.validacao.resultado}</strong>
    ${state.validacao.data_validacao ? ` · ${state.validacao.data_validacao}` : ''}
  `;
}

// ---------- Deep links ----------
function handleDeepLinks() {
  const hash = window.location.hash;
  if (!hash) return;

  // #texto=costumes-ingleses
  const textoMatch = hash.match(/#texto=([\w-]+)/);
  if (textoMatch) {
    const slug = textoMatch[1];
    const corpusId = `corpus:${slug}`;
    // Aguarda dados carregarem (até 5s)
    const tryOpen = (attempts = 0) => {
      if (state.corpus && state.proveniencia) {
        openDossierForCorpusId(corpusId);
      } else if (attempts < 50) {
        setTimeout(() => tryOpen(attempts + 1), 100);
      }
    };
    tryOpen();
    return;
  }

  // #matriz?... (matrix.js handles its own state)
  if (hash.startsWith('#matriz')) {
    setTimeout(() => {
      document.getElementById('matriz')?.scrollIntoView({ behavior: 'smooth' });
    }, 800);
    return;
  }

  // #trilha=... (trails.js handles its own state)
  if (hash.startsWith('#trilha')) {
    setTimeout(() => {
      document.getElementById('trilhas')?.scrollIntoView({ behavior: 'smooth' });
    }, 800);
    return;
  }

  // #grafo?... (contextual.js handles its own state)
  if (hash.startsWith('#grafo')) {
    setTimeout(() => {
      document.getElementById('grafo')?.scrollIntoView({ behavior: 'smooth' });
    }, 800);
    return;
  }
}

function updateDeepLink(hash) {
  if (window.location.hash !== hash) {
    history.replaceState(null, '', hash);
  }
  // Show deep link bar
  const bar = document.getElementById('deep-link-bar');
  const urlSpan = document.getElementById('deep-link-url');
  if (bar && urlSpan) {
    const fullUrl = window.location.origin + window.location.pathname + hash;
    urlSpan.textContent = fullUrl;
    bar.classList.add('deep-link-bar--visible');
  }
}

// ---------- Load SVG sprite ----------
async function loadSvgSprite() {
  const container = document.getElementById('svg-sprite-container');
  if (!container) return;
  try {
    const res = await fetch('assets/icons.svg');
    if (!res.ok) return;
    const text = await res.text();
    container.innerHTML = text;
  } catch (err) {
    console.warn('Erro ao carregar sprite SVG:', err);
  }
}

// ---------- Close dossier ----------
document.addEventListener('click', (e) => {
  if (e.target.id === 'dossier-overlay' || e.target.closest('.dossier-close')) {
    const overlay = document.getElementById('dossier-overlay');
    const panel = document.getElementById('dossier-panel');
    closeDossier(overlay, panel);
    document.querySelectorAll('.text-card--selected').forEach(c => c.classList.remove('text-card--selected'));
    // Limpa deep link do dossiê
    if (window.location.hash.startsWith('#texto=')) {
      history.replaceState(null, '', window.location.pathname);
      document.getElementById('deep-link-bar')?.classList.remove('deep-link-bar--visible');
    }
  }
});

// Copy deep link button
document.addEventListener('click', (e) => {
  if (e.target.id === 'deep-link-copy-btn') {
    const url = document.getElementById('deep-link-url')?.textContent;
    if (url) {
      navigator.clipboard.writeText(url).then(() => {
        const btn = e.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copiado!';
        setTimeout(() => { btn.textContent = originalText; }, 2000);
      });
    }
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const overlay = document.getElementById('dossier-overlay');
    const panel = document.getElementById('dossier-panel');
    if (overlay && overlay.classList.contains('dossier-overlay--open')) {
      closeDossier(overlay, panel);
      document.querySelectorAll('.text-card--selected').forEach(c => c.classList.remove('text-card--selected'));
    }
  }
});
