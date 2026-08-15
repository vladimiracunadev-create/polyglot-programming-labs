# 🐚 Bash — 1989

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Bash es, con casi total seguridad, **el lenguaje que más veces se ejecuta al día en el mundo**: cada
arranque de un contenedor, cada canalización de integración continua y cada tarea programada de
cualquier servidor Linux pasa por él. Y es también **el que menos gente reconoce como un lenguaje de
programación** — hasta que un guion de cuatrocientas líneas falla en producción.

> **🎯 Por qué está en este programa**
>
> Bash es un **primo de la familia históricos / shell** ([Atlas](README.md#historicos-shell)).
>
> Aporta al programa **la composición de procesos por tuberías**
> ([clase 161](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/161-procesos-y-comunicacion-stdin-stdout-sockets-colas/README.md))
> —la idea de McIlroy de 1964 que sostiene el contrato de las 136 clases de este curso— y el
> **componente de automatización** de la clase 171 en su forma más extendida. Y aporta un caso serio de
> la clase 153: **la inyección de comandos y por qué la citación importa**.

| | |
|---|---|
| **Año** | 1989; **Bourne shell** de 1979; **Bash 5.x** actual |
| **Autoría** | **Brian Fox** para GNU; después **Chet Ramey**, que lo mantiene desde 1993 |
| **Familia** | Históricos / shell; sucesor del **Bourne shell** de Stephen Bourne |
| **Paradigma** | Imperativo, **orientado a la composición de procesos** |
| **Tipado** | **Todo es texto**; con arreglos y enteros como añadidos |
| **Memoria** | No aplica: el intérprete la gestiona |
| **Ejecución** | Interpretado, línea a línea |
| **Estado** | 🟢 **Omnipresente** en Unix, Linux, macOS, contenedores y CI |

---

## 📜 Historia

**Stephen Bourne** escribió el **Bourne shell (`sh`)** en los Laboratorios Bell en 1979, sustituyendo
al shell de Thompson. Y aportó lo que hoy es el lenguaje: **estructuras de control, funciones,
variables, sustitución de comandos y redirección**.

Su predecesor, el shell de Thompson (1971), había implementado **las tuberías** que
**Doug McIlroy** había propuesto en un memorando de 1964 con una imagen que se ha citado mil veces:

> Deberíamos tener alguna forma de acoplar programas como **mangueras de jardín**.

Y de ahí salió **la filosofía de Unix** (clase 161): programas pequeños que hacen una cosa, que leen
de la entrada estándar y escriben en la salida estándar, y que se componen.

**Bash** —*Bourne Again SHell*, un juego de palabras— lo escribió **Brian Fox** en **1989** para el
proyecto GNU, como reemplazo libre del `sh` de AT&T, añadiendo lo bueno del **C shell** y del **Korn
shell**: historial, edición de línea, `[[ ]]`, arreglos.

Se convirtió en el shell por defecto de **Linux**, y con Linux llegó a todas partes. **macOS lo usó
hasta 2019**, cuando cambió a **zsh** por la licencia GPLv3 de las versiones nuevas de Bash — un
detalle de licencias con consecuencias reales.

Y en **2014** tuvo su momento más incómodo: **Shellshock**, una vulnerabilidad en el manejo de
funciones exportadas por variables de entorno que estuvo presente **veinticinco años** y afectó a
millones de servidores.

## 🏭 Dónde vive hoy

- **Todo servidor Linux**: guiones de arranque, tareas de `cron`, mantenimiento (clase 171).
- **Contenedores**: cada `RUN` de un `Dockerfile` es un comando de shell (clase 174).
- **Integración continua**: los pasos de GitHub Actions, GitLab CI y Jenkins son, casi siempre, shell
  (clase 147).
- **Herramientas de desarrollo**: `./configure`, los guiones de instalación, los ganchos de git
  (clase 145).
- **Y como pegamento** entre cualquier par de programas que hablen texto.

## 🧠 Lo que enseña: componer procesos, y las trampas de la citación

**Uno, la tubería**, que es el contenido de la clase 161:

```bash
grep ERROR registro.log | awk '{print $4}' | sort | uniq -c | sort -rn | head
```

**Cinco programas, ninguno de los cuales sabe de los otros**, encadenados por texto. Cada uno se
escribió por separado, en años distintos, y componen porque **todos respetan el contrato: entrada
estándar, salida estándar** — que es exactamente el contrato de este curso (clase 040).

**Dos, y es la parte que hay que aprender bien: la citación** (clase 153).

```bash
# ✗ TODOS estos están mal
rm $fichero                  # si el nombre tiene espacios, borra varias cosas
if [ $var = "x" ]             # si $var está vacío, error de sintaxis
for f in $(ls *.txt)           # se rompe con espacios y con saltos de línea
eval "comando $entrada"         # inyección de comandos

# ✓ Y así se escriben
rm -- "$fichero"
if [[ "$var" == "x" ]]
for f in *.txt
```

**La regla es simple y casi nadie la sigue: entrecomillar SIEMPRE las variables.** Sin comillas, Bash
**divide por espacios y expande comodines** sobre el valor — que es la causa de la mayoría de los
guiones que fallan con un nombre de fichero raro, y de bastantes incidentes de seguridad.

**Y tres, las tres líneas que deberían encabezar todo guion serio:**

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

- **`-e`**: parar al primer comando que falle. **Sin esto, un guion sigue adelante tras un error** —el
  problema que `MONMSG` resuelve en [CL](rpg.md) (clase 171)—.
- **`-u`**: fallar al usar una variable no definida. **Es el `implicit none` de Bash** (clase 137), y
  evita el desastre clásico de `rm -rf "$DIR/"` con `$DIR` vacío.
- **`-o pipefail`**: que una tubería falle si falla **cualquiera** de sus partes, no solo la última.

> **Y la advertencia de la clase 171 aplica aquí más que en ningún sitio**: **el guion de shell es
> código de producción**. Despliega, borra y mueve datos. **Merece control de versiones, revisión
> (clase 146) y `shellcheck`** — que es un analizador estático excelente y gratuito, y que detecta la
> mayoría de los errores de esta sección.

## 🔄 Lo que se ha modernizado

- **Bash 5**: arreglos asociativos maduros, `${var@Q}` para citar de forma segura, mejoras de
  rendimiento.
- **ShellCheck**: análisis estático que **debería estar en la integración continua de cualquier
  repositorio con guiones** (clases 146 y 147).
- **`shfmt`**: formateador, como `gofmt` (clase 146).
- **`bats`**: marco de pruebas para guiones de shell — sí, se pueden probar (clase 139).
- **Y la competencia sana**: **zsh** (por defecto en macOS), **fish** (interactivo y amable) y
  **nushell** (con datos estructurados en lugar de texto plano), que replantea la premisa de McIlroy.

## ⚙️ Cómo se ejecuta hoy

```bash
bash main.sh < entrada.txt          # ejecutar
./main.sh                            # con el shebang y permiso de ejecución

shellcheck main.sh                    # ← análisis estático (clase 146)
shfmt -d main.sh                       # formato
bats pruebas/                           # pruebas (clase 139)
```

## 🧪 El programa de la clase 041 en Bash

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```bash
#!/usr/bin/env bash
set -euo pipefail

read -r precio cantidad descuento

# Bash NO tiene aritmética de coma flotante: hay que delegar en bc o en awk.
total=$(awk -v p="$precio" -v c="$cantidad" -v d="$descuento" \
            'BEGIN { printf "%.2f", p * c * (1 - d) }')

printf 'Total: %s\n' "$total"
```

**Lo que hay que ver, y es lo más honesto que puede decir esta ficha.**

- **Bash no sabe multiplicar números con decimales.** `$(( ))` es **solo aritmética entera**, así que
  **hay que llamar a otro programa** —`awk`, `bc` o `python3`—. **Y esa limitación es la ficha
  entera**: Bash no es un lenguaje de cálculo, **es un lenguaje para componer programas que sí
  calculan** (clase 155).
- **`read -r`** con `-r` es obligatorio: sin él, la barra invertida se interpreta como escape.
- **Cada variable va entrecomillada**, incluidas las de `awk -v`.
- **`printf` en lugar de `echo`**: `echo` **interpreta las barras invertidas de forma distinta según
  el shell y las opciones**, y no es portable. `printf` sí lo es, y es la recomendación universal.
- **Y `set -euo pipefail` en la segunda línea**, que es lo que convierte un guion frágil en uno que
  falla cuando debe.

## 📚 Fuentes y bibliografía

- [Manual de Bash (GNU)](https://www.gnu.org/software/bash/manual/) — la referencia; densa y completa.
- [BashFAQ y BashPitfalls](https://mywiki.wooledge.org/BashPitfalls) — **la lectura más útil de esta
  ficha**: una lista de errores comunes con la explicación de por qué fallan. Cambia cómo se escriben
  los guiones.
- [ShellCheck](https://www.shellcheck.net/) — pegar un guion y ver qué está mal, en el navegador.
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) — incluida la
  recomendación de **cuándo NO usar shell** (a partir de unas cien líneas o cuando hay estructuras de
  datos).
- **Doug McIlroy**, el memorando de 1964 y la filosofía de Unix — contexto de la clase 161.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Perl](perl.md) · [Tcl](tcl.md) · [PowerShell](powershell.md) · [JCL](jcl.md) ·
[Python](python.md)
