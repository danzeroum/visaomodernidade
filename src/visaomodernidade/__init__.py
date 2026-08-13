"""visaomodernidade — Pacote de dados acadêmicos do Gabinete de Leitura (1837-1838).

Extraído e validado a partir da tese de Maria Angélica Lau Pereira Soares (2006),
"Visão da Modernidade — A presença britânica no Gabinete de Leitura (1837-1838)".

Módulos principais:
    config       — caminhos e constantes do projeto
    corpus       — construção do corpus canônico dos 10 textos britânicos
    contextual   — construção do grafo contextual (ambiente editorial/intelectual)
    provenance   — construção do grafo de proveniência textual
    evidence     — gerenciamento de evidências com paginação dupla
    validation   — validação sintática (schema) e semântica
    cli          — entry points `visaomodernidade-build` e `visaomodernidade-validate`
"""

__version__ = "0.4.0"
__all__ = ["config", "corpus", "contextual", "provenance", "evidence", "validation", "cli"]
