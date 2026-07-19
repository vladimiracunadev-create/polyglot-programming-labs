# Clase 028 — Lenguajes históricos y de nicho: COBOL, Fortran, Pascal, BASIC, Bash

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Cerrar el Atlas con lenguajes que marcaron época o dominan un nicho. COBOL aún mueve bancos; Fortran, la ciencia; Pascal enseñó a generaciones; BASIC democratizó programar; y Bash sigue siendo el pegamento de la administración de sistemas. Conocerlos da perspectiva histórica y práctica.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Situar cada lenguaje en su época y su nicho actual.
2. Explicar por qué algunos 'viejos' siguen en producción crítica.
3. Reconocer Bash como habilidad transferible imprescindible hoy.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | COBOL: la banca | Miles de millones de líneas aún en producción |
| 2 | Pascal y BASIC | Enseñaron a programar a generaciones enteras |
| 3 | Fortran: la ciencia | El pionero que no se jubila |
| 4 | Bash: el pegamento vivo | Automatización y orquestación en Unix |

## 📖 Definiciones y características

- **COBOL** — 1959 (comité CODASYL, Grace Hopper influyente), para negocios. Clave: aún sostiene núcleos bancarios y de seguros.
- **Pascal** — 1970 (Niklaus Wirth), diseñado para enseñar programación estructurada. Clave: claridad; padre de Delphi.
- **BASIC** — 1964 (Kemeny y Kurtz), pensado para principiantes. Clave: llevó la programación a los ordenadores personales.
- **Bash** — 1989 (Brian Fox, GNU), shell de Unix. Clave: automatización viva; su modelo de tuberías y procesos es muy transferible.

## 🧩 Situación

Un banco descubre que su sistema central corre en COBOL y quedan pocos que lo mantengan. No es una curiosidad: entender por qué el software 'viejo' persiste es entender la realidad de la industria.

## 🔎 Ejemplo

Bash es el más vigente de este grupo: su modelo de tuberías es puro y transferible.

```text
# Contar cuántos archivos .md hay, en una línea:
ls *.md | wc -l

# Tubería: la salida de un comando es la entrada del siguiente
cat notas.txt | grep "TODO" | sort | uniq
```

## ✍️ Práctica

Escribe una tubería de Bash que, dado un archivo de texto, cuente cuántas líneas contienen la palabra 'error'. (Pista: `grep` y `wc`.)

## ⚠️ Errores comunes

- **Despreciar los lenguajes 'viejos'** → causa: creer que lo antiguo es inútil → solución: reconocer que COBOL y Fortran mueven infraestructura crítica hoy
- **Subestimar Bash** → causa: verlo como comandos sueltos → solución: aprender su modelo de tuberías/procesos: es habilidad diaria del desarrollador

## ❓ Preguntas frecuentes

- **¿Vale la pena aprender COBOL?** Como nicho bien pagado por la escasez de expertos, puede tener sentido; como base, no.
- **¿Bash cuenta como lenguaje?** Sí: tiene variables, control de flujo y funciones; y su modelo de procesos es muy transferible.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 027](../../parte-1-atlas-y-genealogia-de-los-lenguajes/027-familia-array-y-cientifica-apl-r-julia-fortran-matlab/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 029 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/029-que-es-un-toolchain-del-codigo-fuente-al-programa-que-corre/README.md)
