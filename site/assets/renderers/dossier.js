/**
 * dossier.js — Renderiza o dossiê lateral de um texto do corpus.
 *
 * Mostra:
 *   - Identidade (título brasileiro, fascículo, data, páginas)
 *   - Rota visual (original identificado, fonte declarada, versão francesa, rota efetiva)
 *   - Operações tradutórias (se houver)
 *   - Evidências (com painel expansível)
 *   - Status epistêmico global
 */

import {
  workIdForCorpus,
  findNode,
  findBrazilianManifestation,
  findOriginalManifestation,
  findDeclaredFont,
  findFrenchVersion,
  isFrenchVersionNotDirectSource,
  hasFrenchVersionInRevue,
  findAuthor,
  findOriginalVenue,
  findOperationsByWork,
  getEvidenceFor,
  formatDate,
  formatPages
} from '../data-loader.js';
import { createBadge } from './badges.js';
import { renderEvidencePanel } from './evidence.js';

/**
 * Abre o painel de dossiê para um item do corpus.
 * @param {HTMLElement} overlay — elemento .dossier-overlay
 * @param {HTMLElement} panel — elemento .dossier-panel
 * @param {Object} corpusItem — item do corpus
 * @param {Object} proveniencia — grafo de proveniência
 */
export function openDossier(overlay, panel, corpusItem, proveniencia) {
  const workId = workIdForCorpus(corpusItem.id);
  const brManifest = workId ? findBrazilianManifestation(proveniencia, workId) : null;
  const origManifest = workId ? findOriginalManifestation(proveniencia, workId) : null;
  const declaredFont = brManifest ? findDeclaredFont(proveniencia, brManifest.id) : null;
  const frenchVersion = workId ? findFrenchVersion(proveniencia, workId) : null;
  const author = workId ? findAuthor(proveniencia, workId) : null;
  const originalVenue = workId ? findOriginalVenue(proveniencia, workId) : null;
  const operations = workId ? findOperationsByWork(proveniencia, workId) : [];

  // Constrói o conteúdo
  const body = panel.querySelector('.dossier-body');
  body.innerHTML = '';

  // ---------- Cabeçalho ----------
  const header = panel.querySelector('.dossier-header h3');
  header.textContent = corpusItem.titulo_gabinete;

  // ---------- Seção: Identidade ----------
  const identitySection = document.createElement('div');
  identitySection.className = 'dossier-section';
  identitySection.innerHTML = '<h4>Identidade</h4>';

  const fasc = corpusItem.fasciculos[0];
  const fasciculosStr = corpusItem.fasciculos.map(f => `n.${f.numero}`).join('–');
  const dataStr = formatDate(fasc.data_iso);
  const paginasStr = fasc.paginas_periodico || '—';

  identitySection.innerHTML += `
    <div class="dossier-field">
      <div class="dossier-field-label">Publicação brasileira</div>
      <div class="dossier-field-value">
        <strong>Gabinete de Leitura</strong><br>
        ${fasciculosStr} · ${dataStr} · pp. ${paginasStr}
      </div>
    </div>
  `;

  if (corpusItem.titulo_original) {
    identitySection.innerHTML += `
      <div class="dossier-field">
        <div class="dossier-field-label">Título original</div>
        <div class="dossier-field-value">${corpusItem.titulo_original}</div>
      </div>
    `;
  }

  if (corpusItem.autor_original) {
    const field = document.createElement('div');
    field.className = 'dossier-field';
    field.innerHTML = `
      <div class="dossier-field-label">Autor original</div>
      <div class="dossier-field-value">${corpusItem.autor_original}</div>
    `;
    field.appendChild(createBadge(corpusItem.autor_status, 'Status da atribuição'));
    identitySection.appendChild(field);
  }

  body.appendChild(identitySection);

  // ---------- Seção: Rota visual ----------
  const routeSection = document.createElement('div');
  routeSection.className = 'dossier-section';
  routeSection.innerHTML = '<h4>Rota textual</h4>';
  routeSection.appendChild(renderRouteDiagram({
    corpusItem, brManifest, origManifest, declaredFont, frenchVersion, author, originalVenue, proveniencia
  }));
  body.appendChild(routeSection);

  // ---------- Seção: Operações tradutórias ----------
  if (operations.length > 0) {
    const opsSection = document.createElement('div');
    opsSection.className = 'dossier-section';
    opsSection.innerHTML = '<h4>Operações tradutórias documentadas</h4>';

    const intro = document.createElement('p');
    intro.style.cssText = 'font-size:0.9rem;color:var(--sepia);margin-bottom:1rem;';
    intro.textContent = `A tese identifica ${operations.length} operação(ões) tradutória(s) neste texto:`;
    opsSection.appendChild(intro);

    for (const op of operations) {
      const opDiv = document.createElement('div');
      opDiv.style.cssText = 'padding:0.75rem;background:var(--paper-dark);border-radius:6px;margin-bottom:0.5rem;';
      opDiv.innerHTML = `
        <div style="font-weight:600;color:var(--green-dark);">${op.titulo}</div>
        <div style="font-family:var(--font-sans);font-size:0.75rem;color:var(--gold-dark);text-transform:uppercase;letter-spacing:0.04em;">${op.tipo_operacao}</div>
      `;
      const badge = createBadge(op.status_epistemologico);
      badge.style.marginTop = '4px';
      opDiv.appendChild(badge);
      opsSection.appendChild(opDiv);
    }

    body.appendChild(opsSection);
  }

  // ---------- Seção: Evidências ----------
  const evidenceSection = document.createElement('div');
  evidenceSection.className = 'dossier-section';
  evidenceSection.innerHTML = '<h4>Evidências</h4>';

  // Coleta evidências do corpus item
  const corpusEvs = (corpusItem.evidencias_ids || [])
    .map(id => proveniencia.evidencias.find(e => e.id === id))
    .filter(e => e);

  if (corpusEvs.length === 0) {
    evidenceSection.innerHTML += '<p style="color:var(--sepia);font-style:italic;font-size:0.9rem;">Nenhuma evidência específica registrada para este texto no corpus.</p>';
  } else {
    for (const ev of corpusEvs) {
      evidenceSection.appendChild(renderEvidencePanel(ev));
    }
  }

  body.appendChild(evidenceSection);

  // ---------- Abrir painel ----------
  overlay.classList.add('dossier-overlay--open');
  panel.classList.add('dossier-panel--open');
  panel.focus();

  // Foco trap simples
  panel.setAttribute('tabindex', '-1');
  panel.focus();
}

/**
 * Fecha o painel de dossiê.
 */
export function closeDossier(overlay, panel) {
  overlay.classList.remove('dossier-overlay--open');
  panel.classList.remove('dossier-panel--open');
}

/**
 * Renderiza o diagrama visual da rota textual.
 */
function renderRouteDiagram({ corpusItem, brManifest, origManifest, declaredFont, frenchVersion, author, originalVenue, proveniencia }) {
  const diagram = document.createElement('div');
  diagram.className = 'route-diagram';

  // Nó: Original
  if (origManifest) {
    const node = document.createElement('div');
    node.className = 'route-node';
    node.innerHTML = `
      <div class="route-node-icon">1</div>
      <div class="route-node-content">
        <strong>Original inglês</strong>
        <small>${origManifest.titulo}</small>
        ${author ? `<small>por ${author.titulo}</small>` : ''}
        ${originalVenue ? `<small>em ${originalVenue.titulo}</small>` : ''}
      </div>
    `;
    node.appendChild(createBadge('identificado'));
    diagram.appendChild(node);
    diagram.appendChild(createArrow('dashed'));
  } else if (corpusItem.original_identificado === false) {
    const node = document.createElement('div');
    node.className = 'route-node';
    node.innerHTML = `
      <div class="route-node-icon" style="background:var(--st-nao-identificado);">?</div>
      <div class="route-node-content">
        <strong>Original não localizado</strong>
        <small>A tese não identificou o original</small>
      </div>
    `;
    node.appendChild(createBadge(corpusItem.autor_status === 'problematico' ? 'problematico' : 'nao_identificado'));
    diagram.appendChild(node);
    diagram.appendChild(createArrow('dashed'));
  }

  // Nó: Fonte declarada no Gabinete
  if (declaredFont) {
    const node = document.createElement('div');
    node.className = 'route-node';
    node.innerHTML = `
      <div class="route-node-icon" style="background:var(--gold-dark);">2</div>
      <div class="route-node-content">
        <strong>Fonte declarada no Gabinete</strong>
        <small>${declaredFont.atributos.referencia_original || declaredFont.titulo}</small>
      </div>
    `;
    node.appendChild(createBadge(declaredFont.status_epistemologico));
    diagram.appendChild(node);
    diagram.appendChild(createArrow('dashed'));
  }

  // Nó: Versão francesa (se houver)
  if (frenchVersion) {
    const brId = brManifest ? brManifest.id : null;
    const notDirect = brId ? isFrenchVersionNotDirectSource(proveniencia, frenchVersion.id, brId) : false;
    const node = document.createElement('div');
    node.className = 'route-node';
    node.innerHTML = `
      <div class="route-node-icon" style="background:var(--orange-fra);">3</div>
      <div class="route-node-content">
        <strong>Versão francesa</strong>
        <small>${frenchVersion.titulo}</small>
        ${notDirect
          ? '<small style="color:var(--st-problematico);">⚠ Não é fonte direta da versão brasileira</small>'
          : '<small>Existência inferida por exclusão — rota não demonstrada</small>'
        }
      </div>
    `;
    node.appendChild(createBadge(notDirect ? 'documentado' : 'inferido'));
    diagram.appendChild(node);
    diagram.appendChild(createArrow(notDirect ? 'blocked' : 'dashed'));
  } else if (corpusItem.mediacao_francesa.status === 'documentado' &&
             corpusItem.id !== 'corpus:costumes-ingleses' &&
             corpusItem.id !== 'corpus:testamento' &&
             corpusItem.id !== 'corpus:honras-hereditarias') {
    // Exceção explícita: sem versão francesa
    const node = document.createElement('div');
    node.className = 'route-node';
    node.innerHTML = `
      <div class="route-node-icon" style="background:var(--sepia);">3</div>
      <div class="route-node-content">
        <strong>Sem versão francesa</strong>
        <small>Exceção explícita da tese</small>
      </div>
    `;
    node.appendChild(createBadge('documentado'));
    diagram.appendChild(node);
    diagram.appendChild(createArrow('dashed'));
  }

  // Nó: Versão brasileira
  const brNode = document.createElement('div');
  brNode.className = 'route-node';
  brNode.innerHTML = `
    <div class="route-node-icon" style="background:var(--green-bra);">4</div>
    <div class="route-node-content">
      <strong>Versão brasileira no Gabinete</strong>
      <small>${corpusItem.titulo_gabinete}</small>
    </div>
  `;
  brNode.appendChild(createBadge('documentado'));
  diagram.appendChild(brNode);

  // Nó: Rota efetiva
  const routeNode = document.createElement('div');
  routeNode.className = 'route-node';
  routeNode.style.marginTop = '0.5rem';
  routeNode.style.paddingTop = '0.5rem';
  routeNode.style.borderTop = '1px solid var(--sepia-light)';
  routeNode.innerHTML = `
    <div class="route-node-icon" style="background:var(--st-nao-identificado);">?</div>
    <div class="route-node-content">
      <strong>Rota tradutória efetiva</strong>
      <small>${corpusItem.rota_tradutoria.descricao || 'Não determinada'}</small>
    </div>
  `;
  routeNode.appendChild(createBadge(corpusItem.rota_tradutoria.status));
  diagram.appendChild(routeNode);

  return diagram;
}

function createArrow(type = 'dashed') {
  const arrow = document.createElement('div');
  arrow.className = `route-arrow route-arrow--${type}`;
  return arrow;
}
