# 📓 Changelog

> [⬅️ Volver al programa](README.md) · [🗺️ Roadmap](ROADMAP.md) · [📥 Releases](https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases)

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/); versionado
según [SemVer](https://semver.org/lang/es/). Para un curso, la lectura de SemVer es esta:
**MAJOR** = cambia la estructura del currículo (numeración o partes); **MINOR** = contenido
o herramientas nuevas sin mover la numeración; **PATCH** = correcciones.

## [1.0.1] — 2026-08-14

### Corregido

- **Los enlaces del sitio a los archivos del repositorio daban 404.** Cada clase enlaza a
  su `casos.json` y a sus diez `implementaciones/<lenguaje>/main.*` —son parte del
  contenido: «este bloque es el archivo real»—, pero el portal no copia esos archivos, así
  que en GitHub Pages y **dentro de las apps** no llevaban a ninguna parte. Eran 1806
  enlaces. Ahora `scripts/generar_sitio.py` hace una pasada final: todo enlace cuyo destino
  no publique el sitio se reapunta a la URL del repositorio, donde el archivo sí existe
  (1969 reapuntados), y **el generador falla si queda alguno roto**, de modo que el
  problema no puede volver sin que CI se entere.
- El sitio publica también `CHANGELOG`, `CODE_OF_CONDUCT` y los README de las dos apps,
  que estaban enlazados desde la portada pero no se generaban.

> Los binarios de la v1.0.0 llevan dentro el sitio con esos enlaces rotos. Se sustituyen
> por los de esta versión; los `.pdf` no cambian (en papel los enlaces ya iban a texto).

## [1.0.0] — 2026-08-14

Primer release. El programa está completo y empaquetado: las 176 clases construidas, la
equivalencia verificada por máquina y el curso distribuido en cuatro formatos (web, APK,
ejecutable de Windows y PDF).

### Currículo

- **176 clases en 12 partes**, con numeración global y secuencial (001→176).
- **136 clases de código** (Partes 3–11) con **1360 implementaciones** del núcleo —
  Python, JavaScript, TypeScript, Java, C#, Go, Rust, C, SQL y PHP— con el código a la
  vista dentro de la clase y verificadas en CI contra su `casos.json`.
- **40 clases de método** (Partes 0–2): pensamiento computacional, genealogía de los
  lenguajes y toolchains.
- **2722 programas primos** en 20 lenguajes repartidos en los 136 anexos `primos.md`.
  Ruby, Perl y Lua se **ejecutan** en CI contra el mismo `casos.json` que el núcleo; los
  otros 17 son material de lectura y así se declara en cada página.
- **Atlas** de 39 cápsulas en 15 familias, **glosario** de 424 términos derivados de las
  clases y **90 preguntas** de autoevaluación (una batería por parte).

### Añadido en este release

- **README docente por parte.** Cada una de las 12 partes explica de qué trata, qué hay
  que traer, qué se sabrá hacer al terminar, **qué se aprende en cada una de sus clases**
  agrupadas en bloques temáticos, y los malentendidos que corrige. El contenido vive en
  [`scripts/guias.py`](scripts/guias.py) y lo renderiza `scripts/build.py`.
- **App Android** ([`apps/android`](apps/android/README.md)): el curso completo sin
  conexión, empaquetando el sitio con Capacitor.
- **App de escritorio** ([`apps/desktop`](apps/desktop/README.md)): ejecutable único que
  sirve el curso embebido en `127.0.0.1` y lo abre en el navegador.
- **Verificación anti-vacío de los artefactos.** Los workflows
  [`android.yml`](.github/workflows/android.yml) y [`desktop.yml`](.github/workflows/desktop.yml)
  abren el binario ya compilado y **cuentan** las páginas de clase que lleva dentro. Un
  APK sin curso compila igual y un `.exe` sin datos arranca igual: solo el recuento lo
  distingue.
- **PDF completo** (`MANUAL-COMPLETO.pdf`, ~2420 páginas): el manual **con** los 2722
  primos incluidos, como asset del release.
- **Rutas y autoevaluaciones reescritas**: cada perfil declara qué trae que se transfiere,
  qué le costará y con qué clase empezar; el banco de preguntas documenta qué evalúa y
  cómo leer el resultado.

### Verificación

| Superficie | Cómo se comprueba |
|---|---|
| Equivalencia entre lenguajes | `ci.yml` — un job por lenguaje, cada implementación contra `casos.json` |
| Primos ejecutables | `labs.yml` — Ruby, Perl y Lua contra el mismo contrato |
| Estructura y manifest | `scripts/validar_estructura.py` en CI |
| Markdown | `markdownlint-cli2` sobre los 754 ficheros del repositorio |
| Secretos y código de los scripts | `gitleaks` y `bandit` en `security.yml` |
| Contenido dentro del APK y del `.exe` | `android.yml` y `desktop.yml` (recuento dentro del binario) |

### Artefactos del release

| Artefacto | Qué es |
|---|---|
| `PolyglotProgrammingLabs-android.apk` | El curso en Android, sin conexión |
| `PolyglotProgrammingLabs-windows.exe` | El curso en Windows, ejecutable único |
| `MANUAL.pdf` | Las 176 clases con el código a la vista (~1306 páginas) |
| `MANUAL-COMPLETO.pdf` | Lo anterior **más** los 2722 primos (~2420 páginas) |
| `sitio-offline.zip` | El portal HTML completo, para servir donde quieras |
| `SHA256SUMS.txt` | Hashes de todo lo anterior |

[1.0.1]: https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/tag/v1.0.1
[1.0.0]: https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/tag/v1.0.0
