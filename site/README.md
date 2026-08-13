# site/ — Exposição digital estática (MVP)

Exposição digital orientada por evidências sobre a presença britânica no *Gabinete de Leitura* (1837-1838), consumindo os JSONs canônicos do pacote `visaomodernidade`.

## Estrutura

```
site/
├── index.html                  # App shell com 5 seções
├── assets/
│   ├── styles.css              # Design system completo (sepia + papel)
│   ├── app.js                  # Orquestrador (carrega dados, gerencia estados)
│   ├── data-loader.js          # Carrega JSONs + helpers de consulta ao grafo
│   ├── icons.svg               # SVG sprite com ícones epistêmicos
│   └── renderers/
│       ├── badges.js           # Selos epistêmicos (ícone + texto + cor)
│       ├── timeline.js         # Linha do tempo dos 35 fascículos
│       ├── dossier.js          # Painel lateral de dossiê por texto
│       ├── evidence.js         # Painel de evidência com paginação dupla
│       └── translation-lab.js  # Comparador textual (3 colunas)
└── README.md                   # Este arquivo
```

## Como executar localmente

```bash
# Na raiz do repositório:
make site   # serve site/ em http://localhost:8000

# Ou manualmente:
cd site
python3 -m http.server 8000
```

Abra `http://localhost:8000` no navegador.

> ⚠️ **Não abra via `file://`** — o `fetch()` dos JSONs será bloqueado por CORS. Use sempre um servidor HTTP local.

## Fontes de dados

O site consome 4 JSONs do diretório `../data/`:

| Arquivo | Uso |
|---------|-----|
| `corpus_britanico_canonico.json` | Tabela canônica dos 10 textos, fascículos, datas, status |
| `grafo_contextual_v2.json` | Ambiente editorial, intelectual, institucional (não usado no MVP) |
| `grafo_proveniencia_textual_v3.json` | Manifestações, rotas, operações tradutórias, evidências |
| `relatorio_validacao.json` | Selo de qualidade — lido primeiro; se `resultado != "aprovado"`, mostra aviso |

Em produção (GitHub Pages), o workflow `deploy-pages.yml` copia esses JSONs para `site/data/` antes do deploy, permitindo `fetch('./data/*.json')`.

## Estados da aplicação

| Estado | Quando | Comportamento |
|--------|--------|---------------|
| `loading` | Início do carregamento | Banner azul no topo, spinners nos containers |
| `ready` | Todos os JSONs carregados, validação aprovada | Interface completa, sem banner |
| `warning` | JSONs carregados, validação com avisos | Banner amarelo, interface disponível |
| `error` | Falha ao carregar JSON ou validação reprovada | Tela de erro, dados não exibidos como validados |

## Selos epistêmicos

Nunca usam apenas cor — sempre ícone SVG + texto:

| Status | Ícone | Cor | Significado |
|--------|-------|-----|-------------|
| `documentado` | ✓ | verde | Declaração explícita ou dado verificável na tese |
| `identificado` | ★ | verde tracejado | Original localizado e confirmado |
| `inferido` | ≈ | amarelo tracejado | Conclusão por evidências indiretas |
| `hipotese` | ? | laranja tracejado | Possibilidade plausível sem confirmação |
| `problematico` | ⚠ | vermelho | Fonte inconsistente ou conflito documental |
| `nao_identificado` | — | cinza | Informação ausente |

## Acessibilidade

- Navegação por teclado (tabindex, Enter/Space nos cards)
- `role="dialog"` e `aria-modal` no painel de dossiê
- `aria-live="polite"` no banner de estado
- `aria-label` descritivo em todos os elementos interativos
- Foco visível com `outline: 2px solid var(--gold)`
- `prefers-reduced-motion` respeitado
- Contraste validado (WCAG AA)

## Próximos passos (P2/P3)

- [ ] Grafo progressivo por entidade (P3)
- [ ] Matriz filtrável do corpus completo (P2)
- [ ] Exportação CSV/JSON de consultas (P3)
- [ ] Modo "pesquisa" vs "explorar" (P3)
- [ ] Busca por texto livre (P3)
