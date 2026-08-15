# 📓 Changelog

> [⬅️ Volver al programa](README.md) · [🗺️ Roadmap](ROADMAP.md) · [📥 Releases](https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases)

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/); versionado
según [SemVer](https://semver.org/lang/es/). Para un curso, la lectura de SemVer es esta:
**MAJOR** = cambia la estructura del currículo (numeración o partes); **MINOR** = contenido
o herramientas nuevas sin mover la numeración; **PATCH** = correcciones.

## [1.1.0] — 2026-08-15

La capa de **lenguajes vivos** deja de ser un anexo del Atlas y pasa a estar en cada clase,
y **todos los lenguajes del repositorio tienen ficha propia**. No cambia ni una numeración:
el currículo sigue siendo el mismo 001→176.

### Añadido

- **1632 programas en los lenguajes que siguen vivos.** Las 136 clases de código traen ahora
  un anexo `vivos.md` con el problema de la clase resuelto en **COBOL, Fortran, Ada, Pascal,
  Common Lisp, Tcl, Perl, C++, RPG, PL/I, MUMPS y Smalltalk** —y en JCL, VBA, AutoLISP o
  ensamblador cuando el tema lo justifica—, cada uno con su explicación de qué enseña ese
  lenguaje que ningún otro del curso enseña igual.
- **Tres niveles de rigor, declarados en la propia página.** 🟢 COBOL, Fortran, Ada, Pascal,
  Lisp, Tcl, Perl y C++ **se compilan y se ejecutan en CI** contra el mismo `casos.json` que
  el núcleo (nuevo *job* `vivos` en [`labs.yml`](.github/workflows/labs.yml)); 🟡 RPG, JCL,
  VBA y AutoLISP **declaran su adaptación** del contrato `stdin→stdout` en lugar de fingir un
  programa que ese lenguaje no puede escribir; ⚪ PL/I, MUMPS, Smalltalk y ensamblador van
  **sin sello de máquina**, y se dice.
- **60 fichas de lenguaje** en [`atlas/lenguajes.md`](atlas/lenguajes.md) — una por cada
  lenguaje del repositorio. Antes solo tenían ficha los 18 vivos; los diez del núcleo no
  tenían ninguna. Cada una sigue la misma anatomía de nueve secciones: historia, dónde vive
  hoy, **lo que enseña**, lo que se ha modernizado, cómo se ejecuta con órdenes reales, **el
  programa de la clase 041 explicado línea a línea** y bibliografía. El código de esa clase
  es literal del repositorio; donde no existía, el programa nuevo se marca como no
  verificado en CI.
- **`manual/ATLAS.pdf`** (238 páginas): las 60 fichas con sus dos índices, en un volumen
  aparte. `generar_manual.py` aprende `--atlas` y `--con-vivos`.

### Cambiado

- El **manual completo** pasa de ~2420 a **4094 páginas**: incluye los anexos de lenguajes
  vivos además de los primos. Se sigue publicando como asset del release, no en el repo.
- El **portal** muestra la tercera capa en la portada y publica las 60 fichas y los 136
  anexos de vivos (542 páginas HTML, frente a 406).
- Las **apps se verifican por dentro con más detalle**: además de las 176 páginas de clase,
  [`android.yml`](.github/workflows/android.yml) y
  [`verificar_exe.py`](apps/desktop/verificar_exe.py) cuentan los 136 anexos de primos, los
  136 de vivos y las 60 fichas antes de publicar nada.

### Corregido

- Referencias cruzadas erróneas en las fichas: la aritmética decimal es la **clase 045** (no
  la 072) y la metaprogramación la **123** (no la 122); 26 enlaces a clases apuntaban a
  directorios que no existían. **12 223 enlaces relativos comprobados, 0 rotos.**
- Trampas de compilación reales encontradas al ejecutar los programas en CI —la lectura
  posicionada de Fortran, `'Image` en Ada, `SplitString` en Pascal, los programas anidados
  de COBOL— **corregidas y escritas dentro de la clase como contenido**, no parcheadas en
  silencio.

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

[1.1.0]: https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/tag/v1.1.0
[1.0.1]: https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/tag/v1.0.1
[1.0.0]: https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/tag/v1.0.0
