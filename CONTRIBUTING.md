# 🤝 Contribuir

> [⬅️ Volver al programa](README.md) · [📚 Índice completo](classes/README.md) · [🔐 Seguridad](SECURITY.md)

Gracias por querer mejorar **Polyglot Programming Labs**. Este es un programa **conceptual**: se compara la programación entre lenguajes, no se enseña un lenguaje aislado. Por eso una contribución se juzga por lo que **explica**, no solo por el código que añade. No se acepta una nueva implementación que se limite a traducir tokens sin explicar sus diferencias semánticas o idiomáticas.

## Qué puedes aportar

- **Corrección de contenido** — una errata, una imprecisión técnica o algo poco claro en una clase. Usa la plantilla de [issue](.github/ISSUE_TEMPLATE/correccion-de-contenido.md).
- **Mejora de una clase** — una explicación más clara, un mejor ejemplo, una comparación más precisa, una referencia a un libro.
- **Implementaciones del núcleo** — arreglar o hacer más idiomática una de las 10 implementaciones de una clase de código.
- **Portal, documentación o scripts** — rutas, atlas, glosario, autoevaluaciones, el verificador.

## Lista de comprobación

- [ ] El concepto está definido **sin depender de un lenguaje**.
- [ ] Existe pseudocódigo o contrato equivalente y neutral.
- [ ] Los casos de prueba (`casos.json`) son **comunes** a todos los lenguajes.
- [ ] Cada implementación es **idiomática** en su lenguaje.
- [ ] Las diferencias están **clasificadas** (sintáctica · semántica · paradigmática).
- [ ] Los comandos para ejecutar son **reproducibles**.
- [ ] **No se afirma una equivalencia** que el lenguaje no ofrece.
- [ ] El contenido está en **español** y cita sus fuentes cuando corresponde.

## Antes de abrir el PR

```bash
# Si tocaste una implementación, verifica la equivalencia
python scripts/verificar_equivalencia.py <clase>

# Comprueba la estructura y los enlaces
python scripts/validar_estructura.py

# Lint de los .md que modificaste
npx markdownlint-cli2 "ruta/al/archivo.md"
```

Rellena la [plantilla de pull request](.github/PULL_REQUEST_TEMPLATE.md). La CI ejecutará la estructura, el markdown y el verificador de equivalencia por lenguaje; el workflow de seguridad escanea secretos con `gitleaks` y el tooling con `bandit`.
