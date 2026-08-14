# 🤝 Contribuir

> [⬅️ Volver al programa](README.md) · [📚 Índice completo](classes/README.md) · [🔐 Seguridad](SECURITY.md)

Gracias por querer mejorar **Polyglot Programming Labs**. Este es un programa **conceptual**: se compara la programación entre lenguajes, no se enseña un lenguaje aislado. Por eso una contribución se juzga por lo que **explica**, no solo por el código que añade. No se acepta una nueva implementación que se limite a traducir tokens sin explicar sus diferencias semánticas o idiomáticas.

## Qué puedes aportar

- **Corrección de contenido** — una errata, una imprecisión técnica o algo poco claro en una clase. Usa la plantilla de [issue](.github/ISSUE_TEMPLATE/correccion-de-contenido.md).
- **Mejora de una clase** — una explicación más clara, un mejor ejemplo, una comparación más precisa, una referencia a un libro.
- **Implementaciones del núcleo** — arreglar o hacer más idiomática una de las 10 implementaciones de una clase de código.
- **Portal, documentación o scripts** — rutas, atlas, glosario, autoevaluaciones, el verificador.
- **Apps** — la de [Android](apps/android/README.md) y la de [escritorio](apps/desktop/README.md), que empaquetan el mismo sitio generado.

## Qué se edita a mano y qué se genera

Editar un archivo generado es trabajo perdido: la siguiente ejecución del generador lo
sobrescribe. Antes de tocar nada, mira en qué columna cae.

| Archivo | ¿Se edita a mano? |
|---|---|
| `classes/parte-N/NNN-*/README.md` y sus `concepto/comparacion/reto/primos/casos.json` | ✅ sí, es el contenido del curso |
| `classes/parte-N/README.md` (README de parte) | ❌ **no** — se genera; el texto vive en [`scripts/guias.py`](scripts/guias.py) |
| `classes/README.md` (índice) y `classes/_manifest.json` | ❌ no — los genera `scripts/build.py` |
| `glosario/README.md` | ❌ no — lo genera `scripts/generar_glosario.py` desde las clases |
| `site/`, `manual/MANUAL.pdf`, `material/` | ❌ no — artefactos generados |
| `atlas/`, `rutas/`, `autoevaluaciones/`, `labs/`, `docs/` | ✅ sí |

Para cambiar la narrativa de una parte o la descripción de una clase en su índice, edita
`scripts/guias.py` y ejecuta `python scripts/build.py`.

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

# Si tocaste scripts/guias.py o el currículo, regenera partes e índice
python scripts/build.py

# Lint de los .md que modificaste
npx markdownlint-cli2 "ruta/al/archivo.md"
```

Rellena la [plantilla de pull request](.github/PULL_REQUEST_TEMPLATE.md). La CI ejecutará la estructura, el markdown y el verificador de equivalencia por lenguaje; el workflow de seguridad escanea secretos con `gitleaks` y el tooling con `bandit`.
