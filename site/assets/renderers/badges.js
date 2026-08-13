/**
 * badges.js — Renderiza selos epistêmicos com ícone + texto + cor.
 *
 * Nunca usa apenas cor — sempre inclui ícone SVG e texto.
 * Os ícones são carregados inline no início do app (ver app.js → loadSvgSprite).
 */

const STATUS_CONFIG = {
  documentado: {
    icon: 'icon-check',
    label: 'Documentado',
    title: 'Declaração explícita ou dado verificável na tese'
  },
  identificado: {
    icon: 'icon-star',
    label: 'Identificado',
    title: 'Original ou atribuição localizado e confirmado pela tese'
  },
  inferido: {
    icon: 'icon-approx',
    label: 'Inferido',
    title: 'Conclusão derivada de evidências indiretas'
  },
  hipotese: {
    icon: 'icon-hypothesis',
    label: 'Hipótese',
    title: 'Possibilidade plausível, sem confirmação documental'
  },
  problematico: {
    icon: 'icon-warning',
    label: 'Problemático',
    title: 'Fonte inconsistente, original não localizado ou conflito documental'
  },
  'nao_identificado': {
    icon: 'icon-unknown',
    label: 'Não identificado',
    title: 'Informação ausente ou ainda não localizada'
  }
};

/**
 * Cria um elemento de ícone SVG via <use> no sprite inline.
 * @param {string} iconId
 * @returns {SVGSVGElement}
 */
function createIcon(iconId) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('width', '14');
  svg.setAttribute('height', '14');
  const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
  use.setAttribute('href', `#${iconId}`);
  svg.appendChild(use);
  return svg;
}

/**
 * Cria um elemento de badge epistêmico.
 * @param {string} status — um dos: documentado, identificado, inferido, hipotese, problematico, nao_identificado
 * @param {string} [customLabel] — texto alternativo (opcional)
 * @returns {HTMLElement}
 */
export function createBadge(status, customLabel) {
  const cfg = STATUS_CONFIG[status] || STATUS_CONFIG['nao_identificado'];
  const badge = document.createElement('span');
  badge.className = `badge badge--${status === 'nao_identificado' ? 'nao-identificado' : status}`;
  badge.title = cfg.title;
  badge.setAttribute('role', 'img');
  badge.setAttribute('aria-label', `${cfg.label}: ${cfg.title}`);

  // Ícone SVG via <use> no sprite inline
  badge.appendChild(createIcon(cfg.icon));

  // Texto
  const text = document.createElement('span');
  text.textContent = customLabel || cfg.label;
  badge.appendChild(text);

  return badge;
}

/**
 * Cria um badge compacto (apenas ícone, com tooltip).
 * @param {string} status
 * @returns {HTMLElement}
 */
export function createCompactBadge(status) {
  const cfg = STATUS_CONFIG[status] || STATUS_CONFIG['nao_identificado'];
  const badge = document.createElement('span');
  badge.className = `badge badge--${status === 'nao_identificado' ? 'nao-identificado' : status}`;
  badge.title = `${cfg.label}: ${cfg.title}`;
  badge.setAttribute('role', 'img');
  badge.setAttribute('aria-label', cfg.label);

  badge.appendChild(createIcon(cfg.icon));

  return badge;
}

/**
 * Cria uma legenda explicando os badges.
 * @returns {HTMLElement}
 */
export function createBadgeLegend() {
  const legend = document.createElement('div');
  legend.className = 'badge-legend';
  legend.style.cssText = 'display:flex;flex-wrap:wrap;gap:0.5rem;margin-top:1rem;font-size:0.8rem;color:var(--sepia);';

  const items = [
    { status: 'documentado', text: 'Confirmado pela tese' },
    { status: 'identificado', text: 'Original localizado' },
    { status: 'inferido', text: 'Inferido por exclusão' },
    { status: 'problematico', text: 'Fonte problemática' },
    { status: 'nao_identificado', text: 'Ainda não identificado' }
  ];

  for (const item of items) {
    const span = document.createElement('span');
    span.style.cssText = 'display:inline-flex;align-items:center;gap:4px;';
    const badge = createCompactBadge(item.status);
    badge.style.padding = '2px 4px';
    span.appendChild(badge);
    const label = document.createElement('span');
    label.textContent = item.text;
    span.appendChild(label);
    legend.appendChild(span);
  }

  return legend;
}
