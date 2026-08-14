/**
 * translation-lab.js — Laboratório de comparação tradutória.
 *
 * Mostra os 4 casos prioritários com comparação textual:
 *   - Costumes Ingleses (3 operações)
 *   - As Honras Hereditárias (2 operações)
 *   - Álibi (1 operação)
 *   - Esboços Sicilianos (1 operação)
 *
 * Layout desktop: 3 colunas (Original | Gabinete | Leitura da tese)
 * Layout mobile: colunas verticais
 */

import { findOperationsByWork, getEvidenceFor, formatPages, formatPdfPages } from '../data-loader.js';
import { createBadge } from './badges.js';

let _activeWorkId = null;

/**
 * Seleciona uma obra específica no laboratório de tradução.
 * Permite que outros renderers (ex: matrix.js) abram o laboratório
 * já com o texto correto selecionado.
 * @param {string} workId — ID da obra (ex: "work:a-cockney-country-gentleman")
 */
export function selectTranslationWork(workId) {
  const t = TEXTOS_LAB.find(t => t.workId === workId);
  if (!t) {
    console.warn(`selectTranslationWork: workId não encontrado: ${workId}`);
    return;
  }
  // Atualiza botões
  const options = document.querySelectorAll('.translation-lab-option');
  options.forEach((opt, i) => {
    opt.classList.toggle('translation-lab-option--active', TEXTOS_LAB[i].workId === workId);
  });
  // Re-renderiza operações
  const opsContainer = document.querySelector('.translation-ops');
  if (opsContainer) {
    renderOperations(opsContainer, _proveniencia, workId);
  }
  _activeWorkId = workId;
}

let _proveniencia = null;

const TEXTOS_LAB = [
  { corpusId: 'corpus:costumes-ingleses', workId: 'work:a-cockney-country-gentleman', label: 'Costumes Ingleses' },
  { corpusId: 'corpus:honras-hereditarias', workId: 'work:hereditary-honours', label: 'As Honras Hereditárias' },
  { corpusId: 'corpus:alibi', workId: 'work:alibi-grattan', label: 'Álibi' },
  { corpusId: 'corpus:esbocos-sicilianos', workId: 'work:esbocos-sicilianos', label: 'Esboços Sicilianos' }
];

/**
 * Renderiza o laboratório de comparação.
 * @param {HTMLElement} container
 * @param {Object} proveniencia
 */
export function renderTranslationLab(container, proveniencia) {
  _proveniencia = proveniencia;
  container.innerHTML = '';

  const intro = document.createElement('p');
  intro.className = 'section-intro';
  intro.innerHTML = `Comparação textual entre o original inglês e a versão brasileira publicada no Gabinete de Leitura, ` +
    `baseada na análise de Soares (2006). Apenas os <strong>4 casos com comparação explícita</strong> na tese são exibidos.`;
  container.appendChild(intro);

  // Seletor de texto
  const selector = document.createElement('div');
  selector.className = 'translation-lab-selector';

  for (let i = 0; i < TEXTOS_LAB.length; i++) {
    const t = TEXTOS_LAB[i];
    const btn = document.createElement('button');
    btn.className = `translation-lab-option ${i === 0 ? 'translation-lab-option--active' : ''}`;
    btn.textContent = t.label;
    btn.dataset.index = i;
    btn.addEventListener('click', () => {
      selector.querySelectorAll('.translation-lab-option').forEach(b => b.classList.remove('translation-lab-option--active'));
      btn.classList.add('translation-lab-option--active');
      renderOperations(opsContainer, proveniencia, t.workId);
    });
    selector.appendChild(btn);
  }
  container.appendChild(selector);

  // Container de operações
  const opsContainer = document.createElement('div');
  opsContainer.className = 'translation-ops';
  container.appendChild(opsContainer);

  // Renderiza o primeiro por padrão
  renderOperations(opsContainer, proveniencia, TEXTOS_LAB[0].workId);
}

function renderOperations(container, proveniencia, workId) {
  container.innerHTML = '';
  const ops = findOperationsByWork(proveniencia, workId);

  if (ops.length === 0) {
    container.innerHTML = '<p style="color:var(--sepia);font-style:italic;">Nenhuma operação tradutória documentada para este texto.</p>';
    return;
  }

  for (const op of ops) {
    const opDiv = document.createElement('div');
    opDiv.className = 'translation-op';

    // Cabeçalho da operação
    const header = document.createElement('div');
    header.className = 'translation-op-header';
    header.innerHTML = `
      <div class="translation-op-title">${op.titulo}</div>
      <div class="translation-op-type">${op.tipo_operacao}</div>
    `;
    const badge = createBadge(op.status_epistemologico);
    badge.style.marginTop = '4px';
    header.appendChild(badge);
    opDiv.appendChild(header);

    // 3 colunas
    const cols = document.createElement('div');
    cols.className = 'translation-op-cols';

    // Coluna 1: Original inglês
    const col1 = document.createElement('div');
    col1.className = 'translation-op-col';
    col1.innerHTML = `
      <div class="translation-op-col-label">
        <span class="flag flag--uk"></span>
        Original inglês
      </div>
    `;
    const text1 = document.createElement('div');
    text1.className = `translation-op-text ${op.trecho_original ? '' : 'translation-op-text--muted'}`;
    text1.textContent = op.trecho_original || '(trecho não transcrito na tese)';
    col1.appendChild(text1);
    cols.appendChild(col1);

    // Coluna 2: Versão brasileira
    const col2 = document.createElement('div');
    col2.className = 'translation-op-col';
    col2.innerHTML = `
      <div class="translation-op-col-label">
        <span class="flag flag--br"></span>
        Versão brasileira (Gabinete)
      </div>
    `;
    const text2 = document.createElement('div');
    text2.className = `translation-op-text ${op.trecho_brasileiro ? '' : 'translation-op-text--muted'}`;
    text2.textContent = op.trecho_brasileiro || '(trecho não transcrito na tese)';
    col2.appendChild(text2);
    cols.appendChild(col2);

    // Coluna 3: Leitura da tese
    const col3 = document.createElement('div');
    col3.className = 'translation-op-col';
    col3.innerHTML = `
      <div class="translation-op-col-label">
        <span class="flag flag--thesis"></span>
        Leitura da tese
      </div>
    `;
    const effect = document.createElement('div');
    effect.className = 'translation-op-text';
    effect.innerHTML = `<strong>Efeito textual:</strong> ${op.efeito_textual || '—'}`;
    col3.appendChild(effect);

    if (op.efeito_interpretativo) {
      const interp = document.createElement('div');
      interp.className = 'translation-op-interpretation';
      interp.innerHTML = `<strong>Interpretação:</strong> ${op.efeito_interpretativo}`;
      col3.appendChild(interp);
    }

    // Evidências paginadas
    const evs = getEvidenceFor(proveniencia, op);
    if (evs.length > 0) {
      const evSection = document.createElement('div');
      evSection.style.cssText = 'margin-top:0.75rem;padding-top:0.5rem;border-top:1px solid var(--sepia-light);';
      evSection.innerHTML = '<div style="font-family:var(--font-sans);font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--gold-dark);margin-bottom:4px;">Evidência</div>';
      for (const ev of evs) {
        const evDiv = document.createElement('div');
        evDiv.style.cssText = 'font-size:0.8rem;color:var(--sepia-dark);margin-bottom:4px;';
        evDiv.innerHTML = `
          ${ev.titulo}<br>
          <span style="color:var(--sepia);">${formatPages(ev.fonte)} · ${formatPdfPages(ev.fonte)}</span>
        `;
        evSection.appendChild(evDiv);
      }
      col3.appendChild(evSection);
    }

    cols.appendChild(col3);
    opDiv.appendChild(cols);
    container.appendChild(opDiv);
  }
}
