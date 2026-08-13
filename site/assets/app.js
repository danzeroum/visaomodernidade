// visaomodernidade — app.js (placeholder)
// Será expandido na próxima iteração para consumir os JSONs de data/.

'use strict';

// Status epistemológico -> classes CSS para estilo visual
const STATUS_CLASSES = {
  documentado: 'status-documentado',
  identificado: 'status-identificado',
  inferido: 'status-inferido',
  hipotese: 'status-hipotese',
  problematico: 'status-problematico',
  nao_identificado: 'status-nao-identificado'
};

// Carrega dados estáticos (a ser implementado na próxima iteração)
async function loadCorpus() {
  const res = await fetch('./data/corpus_britanico_canonico.json');
  return res.json();
}

async function loadGrafoProveniencia() {
  const res = await fetch('./data/grafo_proveniencia_textual_v3.json');
  return res.json();
}

async function loadRelatorioValidacao() {
  const res = await fetch('./data/relatorio_validacao.json');
  return res.json();
}

// Animação dos números estatísticos
document.addEventListener('DOMContentLoaded', () => {
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
});
