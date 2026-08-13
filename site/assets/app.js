/**
 * app.js — Orquestrador principal do site estático.
 *
 * Responsabilidades:
 *   1. Carregar os JSONs via data-loader.js
 *   2. Gerenciar estados (loading, ready, warning, error)
 *   3. Renderizar timeline, lista de textos, dossiê, laboratório
 *   4. Travar navegação se validação não estiver aprovada
 */

import { loadAll, ESTADO } from './data-loader.js';
import { renderTimeline } from './renderers/timeline.js';
import { openDossier, closeDossier } from './renderers/dossier.js';
import { renderTranslationLab } from './renderers/translation-lab.js';
import { createBadge, createBadgeLegend } from './renderers/badges.js';

// ---------- Estado da aplicação ----------
const state = {
  corpus: null,
  contextual: null,
  proveniencia: null,
  validacao: null,
  estado: ESTADO.LOADING,
  selectedCorpusId: null
};

// ---------- Inicialização ----------
document.addEventListener('DOMContentLoaded', init);

async function init() {
  showStateBanner(ESTADO.LOADING, 'Carregando dados acadêmicos…');

  // Carrega o sprite SVG inline (necessário para <use> funcionar em file://)
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
}

/**
 * Carrega o sprite SVG (assets/icons.svg) e injeta inline no DOM.
 * Necessário porque <use href="assets/icons.svg#..."> não funciona
 * de forma confiável em file:// e tem problemas de CORS em alguns ambientes.
 */
async function loadSvgSprite() {
  const container = document.getElementById('svg-sprite-container');
  if (!container) return;
  try {
    const res = await fetch('assets/icons.svg');
    if (!res.ok) {
      console.warn('Sprite SVG não pôde ser carregado:', res.status);
      return;
    }
    const text = await res.text();
    container.innerHTML = text;
  } catch (err) {
    console.warn('Erro ao carregar sprite SVG:', err);
  }
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
      <p style="margin-top:1rem;font-size:0.85rem;">
        Verifique se o site está sendo servido por HTTP (não file://) e se os JSONs
        em <code>data/</code> estão acessíveis.
      </p>
    </div>
  `;
}

function renderAll() {
  // Stats do hero
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

  // Legenda de badges
  const legendContainer = document.getElementById('badge-legend');
  if (legendContainer) {
    legendContainer.appendChild(createBadgeLegend());
  }

  // Footer meta
  renderFooterMeta();
}

function renderHeroStats() {
  // Anima os números
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

    // Badges
    const badgesDiv = card.querySelector('.text-card-badges');
    badgesDiv.appendChild(createBadge(item.autor_status, 'Autor'));

    if (item.original_identificado) {
      badgesDiv.appendChild(createBadge('identificado', 'Original'));
    } else if (item.fonte_original_identificada.status_epistemologico === 'problematico') {
      badgesDiv.appendChild(createBadge('problematico', 'Original'));
    } else {
      badgesDiv.appendChild(createBadge('nao_identificado', 'Original'));
    }

    if (item.rota_tradutoria.status === 'documentado') {
      badgesDiv.appendChild(createBadge('documentado', 'Rota'));
    } else {
      badgesDiv.appendChild(createBadge(item.rota_tradutoria.status, 'Rota'));
    }

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

  // Marca card selecionado
  document.querySelectorAll('.text-card').forEach(c => {
    c.classList.toggle('text-card--selected', c.dataset.corpusId === corpusId);
  });
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

// ---------- Fechar dossiê ----------
document.addEventListener('click', (e) => {
  if (e.target.id === 'dossier-overlay' ||
      e.target.closest('.dossier-close')) {
    const overlay = document.getElementById('dossier-overlay');
    const panel = document.getElementById('dossier-panel');
    closeDossier(overlay, panel);
    document.querySelectorAll('.text-card--selected').forEach(c => c.classList.remove('text-card--selected'));
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
