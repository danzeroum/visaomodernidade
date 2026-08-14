/**
 * trails.js — Trilhas guiadas pela exposição.
 *
 * Três percursos curtos (4-5 passos cada) que guiam o visitante
 * por uma narrativa específica:
 *
 *   1. "Uma história em viagem" — como Costumes Ingleses chegou ao Brasil
 *   2. "O que a tradução apaga?" — comparações tradutórias
 *   3. "O que ainda não sabemos?" — lacunas documentais
 *
 * Cada passo abre o dossiê correspondente. Estado refletido na URL (#trilha=...).
 */

const TRILHAS = [
  {
    id: 'historia-em-viagem',
    titulo: 'Uma história em viagem',
    subtitulo: 'Como uma narrativa inglesa chegou ao Rio de Janeiro',
    duracao: '5 min',
    passos: [
      { corpusId: 'corpus:costumes-ingleses', titulo: 'Costumes Ingleses no Rio de Janeiro', descricao: 'Publicado no Gabinete n.30, 04/03/1838.' },
      { corpusId: 'corpus:costumes-ingleses', titulo: 'Original de John Poole', descricao: 'A Cockney Country-Gentleman, The New Monthly Magazine, jun/1837.' },
      { corpusId: 'corpus:costumes-ingleses', titulo: 'Fonte declarada problemática', descricao: 'O Gabinete indica "Colburn\'s Magazine" — publicação que não existiu.' },
      { corpusId: 'corpus:costumes-ingleses', titulo: 'Versão francesa descartada', descricao: 'Le Cockney Campagnard existe, mas a tese afirma que não foi a fonte direta.' },
      { corpusId: 'corpus:costumes-ingleses', titulo: 'Mudança de ironia e desfecho', descricao: 'Três operações tradutórias alteram a sátira social do original.' }
    ]
  },
  {
    id: 'traducao-apaga',
    titulo: 'O que a tradução apaga?',
    subtitulo: 'Comparações que revelam transformações no percurso',
    duracao: '6 min',
    passos: [
      { corpusId: 'corpus:costumes-ingleses', titulo: 'Costumes Ingleses', descricao: 'Atenuação da ironia sobre Fieldlove; alteração do desfecho.' },
      { corpusId: 'corpus:alibi', titulo: 'Álibi', descricao: 'Supressão da crítica ao "modo de ser dos irlandeses".' },
      { corpusId: 'corpus:esbocos-sicilianos', titulo: 'Esboços Sicilianos', descricao: 'Supressão da nota sobre punição moral e consciência culpada.' },
      { corpusId: 'corpus:honras-hereditarias', titulo: 'As Honras Hereditárias', descricao: 'Supressão do gesto caracterizador; especificação do espaço narrativo.' }
    ]
  },
  {
    id: 'o-que-nao-sabemos',
    titulo: 'O que ainda não sabemos?',
    subtitulo: 'Lacunas documentais que a pesquisa séria exibe',
    duracao: '4 min',
    passos: [
      { corpusId: 'corpus:testamento', titulo: 'O Testamento', descricao: 'Original não localizado; atribuição a Crabbe não confirmada; fonte declarada inexistente.' },
      { corpusId: 'corpus:livro-da-vida', titulo: 'O Livro da Vida', descricao: 'Original não localizado; fonte Retrospective Review problemática.' },
      { corpusId: 'corpus:sedutor', titulo: 'O Sedutor', descricao: 'Washington Irving é identificado, mas a tese não localiza título, veículo ou data do original.' },
      { corpusId: 'corpus:esbocos-sicilianos', titulo: 'Esboços Sicilianos', descricao: 'Autor identificado, mas data de publicação em The Metropolitan não especificada.' }
    ]
  }
];

let _activeTrail = null;
let _currentStep = 0;
let _onSelectText = null;

export function renderTrails(container, callbacks) {
  _onSelectText = callbacks.onSelectText || (() => {});

  container.innerHTML = '';

  // Introdução
  const intro = document.createElement('p');
  intro.className = 'section-intro';
  intro.innerHTML = `Percursos guiados pela exposição. Cada trilha conduz o visitante por uma narrativa específica, ` +
    `passo a passo, abrindo dossiês relevantes. <strong>Pesquisa séria também exibe lacunas</strong> — a terceira trilha é particularmente boa para isso.`;
  container.appendChild(intro);

  // Seletor de trilha
  const selector = document.createElement('div');
  selector.className = 'trail-selector';
  for (const trail of TRILHAS) {
    const btn = document.createElement('button');
    btn.className = 'trail-option';
    btn.dataset.id = trail.id;
    btn.innerHTML = `
      <div class="trail-option-title">${trail.titulo}</div>
      <div class="trail-option-meta">${trail.passos.length} passos · ${trail.duracao}</div>
    `;
    btn.addEventListener('click', () => selectTrail(trail.id));
    selector.appendChild(btn);
  }
  container.appendChild(selector);

  // Container da trilha ativa
  const trailContent = document.createElement('div');
  trailContent.id = 'trail-content';
  container.appendChild(trailContent);

  // Renderiza estado inicial (nenhuma trilha ativa)
  renderTrailContent();

  // Carrega trilha da URL (após render inicial)
  const hash = window.location.hash;
  const trailMatch = hash.match(/#trilha=([\w-]+)/);
  if (trailMatch) {
    selectTrail(trailMatch[1]);
  }

  function selectTrail(trailId) {
    const trail = TRILHAS.find(t => t.id === trailId);
    if (!trail) return;

    _activeTrail = trail;
    _currentStep = 0;

    // Atualiza botões
    container.querySelectorAll('.trail-option').forEach(b => {
      b.classList.toggle('trail-option--active', b.dataset.id === trailId);
    });

    // Atualiza URL — pushState porque é ação explícita do usuário (clique em trilha)
    history.pushState(null, '', `#trilha=${trailId}`);

    renderTrailContent();
  }

  function renderTrailContent() {
    const content = document.getElementById('trail-content');
    content.innerHTML = '';

    if (!_activeTrail) return;

    // Cabeçalho da trilha
    const header = document.createElement('div');
    header.className = 'trail-header';
    header.innerHTML = `
      <h3 class="trail-title">${_activeTrail.titulo}</h3>
      <p class="trail-subtitle">${_activeTrail.subtitulo}</p>
      <div class="trail-progress">
        Passo ${_currentStep + 1} de ${_activeTrail.passos.length}
      </div>
    `;
    content.appendChild(header);

    // Lista de passos
    const stepsList = document.createElement('ol');
    stepsList.className = 'trail-steps';

    _activeTrail.passos.forEach((passo, idx) => {
      const li = document.createElement('li');
      li.className = `trail-step ${idx === _currentStep ? 'trail-step--current' : ''} ${idx < _currentStep ? 'trail-step--done' : ''}`;
      li.innerHTML = `
        <div class="trail-step-num">${idx + 1}</div>
        <div class="trail-step-content">
          <div class="trail-step-title">${passo.titulo}</div>
          <div class="trail-step-desc">${passo.descricao}</div>
        </div>
      `;
      li.addEventListener('click', () => {
        _currentStep = idx;
        renderTrailContent();
        _onSelectText(passo.corpusId);
      });
      stepsList.appendChild(li);
    });

    content.appendChild(stepsList);

    // Botões de navegação
    const nav = document.createElement('div');
    nav.className = 'trail-nav';

    if (_currentStep > 0) {
      const prev = document.createElement('button');
      prev.className = 'filter-btn';
      prev.textContent = '← Passo anterior';
      prev.addEventListener('click', () => {
        _currentStep--;
        renderTrailContent();
      });
      nav.appendChild(prev);
    }

    const openBtn = document.createElement('button');
    openBtn.className = 'filter-btn filter-btn--active';
    openBtn.textContent = `Abrir dossiê: ${_activeTrail.passos[_currentStep].titulo}`;
    openBtn.addEventListener('click', () => {
      _onSelectText(_activeTrail.passos[_currentStep].corpusId);
    });
    nav.appendChild(openBtn);

    if (_currentStep < _activeTrail.passos.length - 1) {
      const next = document.createElement('button');
      next.className = 'filter-btn';
      next.textContent = 'Próximo passo →';
      next.addEventListener('click', () => {
        _currentStep++;
        renderTrailContent();
        // Abre automaticamente o dossiê do próximo passo
        _onSelectText(_activeTrail.passos[_currentStep].corpusId);
      });
      nav.appendChild(next);
    }

    content.appendChild(nav);
  }
}
