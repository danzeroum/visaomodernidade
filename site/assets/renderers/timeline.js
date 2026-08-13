/**
 * timeline.js — Renderiza a linha do tempo dos 35 fascículos do Gabinete de Leitura.
 *
 * O Gabinete era semanal, publicado aos domingos de 13/08/1837 a 08/04/1838.
 * Os 10 textos do corpus britânico são destacados nos fascículos correspondentes.
 */

import { formatDate } from '../data-loader.js';
import { createCompactBadge } from './badges.js';

// Data do primeiro fascículo
const FIRST_DATE = new Date('1837-08-13T00:00:00');
const TOTAL_FASCICULOS = 35;

/**
 * Calcula a data ISO de um fascículo pelo número.
 * O Gabinete era semanal (todo domingo), começando em 13/08/1837.
 * @param {number} num — número do fascículo (1-35)
 * @returns {string} data ISO YYYY-MM-DD
 */
function fasciculoDate(num) {
  const d = new Date(FIRST_DATE);
  d.setDate(d.getDate() + (num - 1) * 7);
  return d.toISOString().slice(0, 10);
}

/**
 * Mapeia fascículo -> texto do corpus (se houver).
 * Alguns fascículos têm mais de um item (Esboços Sicilianos: 31-34).
 */
function buildFasciculoToTextMap(corpus) {
  const map = new Map();
  for (const item of corpus.itens) {
    for (const f of item.fasciculos) {
      if (!map.has(f.numero)) {
        map.set(f.numero, []);
      }
      map.get(f.numero).push({ item, fasc: f });
    }
  }
  return map;
}

/**
 * Renderiza a timeline completa dos 35 fascículos.
 * @param {HTMLElement} container — elemento onde a timeline será inserida
 * @param {Object} corpus — corpus_britanico_canonico.json
 * @param {Function} onSelect — callback(fasciculoNum, item|null)
 */
export function renderTimeline(container, corpus, onSelect) {
  container.innerHTML = '';

  const fascMap = buildFasciculoToTextMap(corpus);

  // Introdução
  const intro = document.createElement('p');
  intro.className = 'section-intro';
  intro.innerHTML = `O <em>Gabinete de Leitura</em> foi publicado semanalmente no Rio de Janeiro ` +
    `entre <strong>13 de agosto de 1837</strong> e <strong>8 de abril de 1838</strong>, ` +
    `totalizando <strong>35 fascículos</strong>. Os <strong>10 textos britânicos</strong> ` +
    `do corpus canônico estão destacados abaixo.`;
  container.appendChild(intro);

  // Track
  const track = document.createElement('div');
  track.className = 'timeline-track';
  track.setAttribute('role', 'list');
  track.setAttribute('aria-label', 'Linha do tempo dos 35 fascículos');

  for (let num = 1; num <= TOTAL_FASCICULOS; num++) {
    const date = fasciculoDate(num);
    const texts = fascMap.get(num) || [];
    const hasText = texts.length > 0;

    const dot = document.createElement('button');
    dot.className = `timeline-dot ${hasText ? 'timeline-dot--has-text' : ''}`;
    dot.setAttribute('role', 'listitem');
    dot.setAttribute('aria-label',
      `Fascículo n.${num}, ${formatDate(date)}${hasText ? ` — contém ${texts.map(t => t.item.titulo_gabinete).join(', ')}` : ''}`
    );
    dot.style.border = 'none';
    dot.style.background = 'transparent';

    const numEl = document.createElement('span');
    numEl.className = 'timeline-dot-num';
    numEl.textContent = num;
    dot.appendChild(numEl);

    const marker = document.createElement('span');
    marker.className = 'timeline-dot-marker';
    dot.appendChild(marker);

    const dateEl = document.createElement('span');
    dateEl.className = 'timeline-dot-date';
    dateEl.textContent = formatDate(date).split(' ').slice(0, 2).join(' ');
    dot.appendChild(dateEl);

    if (hasText) {
      dot.addEventListener('click', () => {
        // Remove selected de todos
        track.querySelectorAll('.timeline-dot--selected').forEach(el => el.classList.remove('timeline-dot--selected'));
        dot.classList.add('timeline-dot--selected');
        onSelect(num, texts[0].item);
      });
    }

    track.appendChild(dot);
  }

  container.appendChild(track);

  // Legenda
  const legend = document.createElement('div');
  legend.className = 'timeline-legend';
  legend.innerHTML = `
    <div class="legend-item">
      <span class="legend-marker" style="background:var(--green-dark);width:18px;height:18px;border-radius:50%;"></span>
      Fascículo com texto britânico do corpus
    </div>
    <div class="legend-item">
      <span class="legend-marker" style="background:var(--sepia-light);"></span>
      Fascículo sem texto britânico identificado
    </div>
  `;
  container.appendChild(legend);
}
