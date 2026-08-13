/**
 * evidence.js — Renderiza o painel de evidência com paginação dupla e status epistêmico.
 *
 * Cada painel mostra:
 *   - Afirmação / título
 *   - Status epistêmico (badge)
 *   - Tipo de evidência
 *   - Página impressa
 *   - Página PDF
 *   - Resumo fiel da tese
 *   - Citação literal (se houver)
 */

import { createBadge } from './badges.js';
import { formatPages, formatPdfPages } from '../data-loader.js';

/**
 * Renderiza um painel de evidência.
 * @param {Object} evidence — objeto de evidência do grafo
 * @returns {HTMLElement}
 */
export function renderEvidencePanel(evidence) {
  const panel = document.createElement('div');
  panel.className = 'evidence-panel';

  const fonte = evidence.fonte || {};

  // Cabeçalho
  const header = document.createElement('h5');
  header.textContent = evidence.titulo;
  panel.appendChild(header);

  // Badge de status
  const badgeRow = document.createElement('div');
  badgeRow.style.cssText = 'display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:0.5rem;';
  badgeRow.appendChild(createBadge(evidence.status_epistemologico));
  if (evidence.tipo_evidencia) {
    const typeBadge = document.createElement('span');
    typeBadge.className = 'badge';
    typeBadge.style.cssText = 'background:var(--paper-dark);color:var(--sepia-dark);border:1px solid var(--sepia-light);';
    typeBadge.textContent = evidence.tipo_evidencia;
    badgeRow.appendChild(typeBadge);
  }
  panel.appendChild(badgeRow);

  // Metadados (paginação dupla)
  const meta = document.createElement('div');
  meta.className = 'evidence-meta';
  meta.innerHTML = `
    <div class="evidence-meta-item">
      <span class="evidence-meta-label">Fonte</span>
      <span class="evidence-meta-value">${fonte.autora || fonte.obra?.split(',')[0] || '—'}, ${fonte.ano || '—'}</span>
    </div>
    <div class="evidence-meta-item">
      <span class="evidence-meta-label">Página impressa</span>
      <span class="evidence-meta-value">${formatPages(fonte)}</span>
    </div>
    <div class="evidence-meta-item">
      <span class="evidence-meta-label">Página PDF</span>
      <span class="evidence-meta-value">${formatPdfPages(fonte)}</span>
    </div>
  `;
  panel.appendChild(meta);

  // Conteúdo
  if (evidence.conteudo) {
    const content = document.createElement('div');
    content.className = 'evidence-content';
    content.textContent = evidence.conteudo;
    panel.appendChild(content);
  }

  // Citação literal (se houver)
  if (evidence.citacao) {
    const quote = document.createElement('blockquote');
    quote.className = 'evidence-quote';
    quote.textContent = evidence.citacao;
    panel.appendChild(quote);
  }

  return panel;
}

/**
 * Cria um botão "Ver evidência" que abre um modal com o painel completo.
 * @param {Object} evidence
 * @returns {HTMLElement}
 */
export function createEvidenceButton(evidence) {
  const btn = document.createElement('button');
  btn.className = 'filter-btn';
  btn.style.cssText = 'font-size:0.8rem;padding:4px 12px;';
  btn.innerHTML = '📄 Ver evidência';
  btn.title = evidence.titulo;

  btn.addEventListener('click', () => {
    showEvidenceModal(evidence);
  });

  return btn;
}

/**
 * Mostra a evidência em um modal centralizado.
 */
function showEvidenceModal(evidence) {
  // Remove modal existente
  const existing = document.getElementById('evidence-modal');
  if (existing) existing.remove();

  const overlay = document.createElement('div');
  overlay.id = 'evidence-modal';
  overlay.style.cssText = `
    position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:400;
    display:flex;align-items:center;justify-content:center;padding:1rem;
  `;

  const modal = document.createElement('div');
  modal.style.cssText = `
    background:var(--paper-light);border-radius:12px;max-width:640px;width:100%;
    max-height:85vh;overflow-y:auto;padding:0;box-shadow:0 8px 32px rgba(0,0,0,0.3);
  `;

  const closeBtn = document.createElement('button');
  closeBtn.style.cssText = `
    position:sticky;top:0;float:right;margin:8px;
    background:var(--sepia-dark);color:var(--paper);border:none;border-radius:50%;
    width:32px;height:32px;font-size:1.2rem;cursor:pointer;z-index:1;
  `;
  closeBtn.textContent = '✕';
  closeBtn.setAttribute('aria-label', 'Fechar');
  closeBtn.addEventListener('click', () => overlay.remove());
  modal.appendChild(closeBtn);

  const content = document.createElement('div');
  content.style.padding = '1rem';
  content.appendChild(renderEvidencePanel(evidence));
  modal.appendChild(content);

  overlay.appendChild(modal);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.remove();
  });
  document.addEventListener('keydown', function esc(e) {
    if (e.key === 'Escape') {
      overlay.remove();
      document.removeEventListener('keydown', esc);
    }
  });

  document.body.appendChild(overlay);
}
