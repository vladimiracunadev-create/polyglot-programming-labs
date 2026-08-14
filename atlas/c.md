# 🔩 C — 1972

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**Está en esta lista, pero no es legacy — y esa distinción es el contenido de la ficha.** C tiene la
edad de COBOL menos trece años y una diferencia decisiva: no sobrevive por el coste de migrar, sino
porque **sigue siendo la mejor herramienta para lo que hace**. Es, además, el idioma en el que todos
los demás lenguajes se hablan entre sí.

> **🎯 Por qué está en este programa**
>
> **C es uno de los diez lenguajes del núcleo**: se implementa y se verifica en CI en las 136 clases
> de código. Esta ficha no repite eso — cuenta su historia y responde a la pregunta que motiva esta
> sección: *¿por qué un lenguaje de 1972 no es un lenguaje viejo?*
>
> La respuesta corta: porque **C no es solo un lenguaje, es una interfaz**. La ABI de C es el único
> terreno común donde Python llama a NumPy, Rust llama al sistema operativo, Java llama a una
> biblioteca nativa y Go llama a SQLite. Cuando en la
> [Parte 10](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md) se estudia
> la interoperabilidad, se estudia la ABI de C, porque **no hay otra**. Un lenguaje puede sustituir a
> C escribiendo código nuevo; no puede sustituir a C como punto de encuentro.

| | |
|---|---|
| **Año** | 1972; **K&R** en 1978; ANSI **C89**; **C99**, **C11**, **C17**, **C23** |
| **Autoría** | **Dennis Ritchie**, Bell Labs, a partir de **B** (Thompson) y **BCPL** (Richards) |
| **Familia** | C / llaves — la raíz sintáctica de C++, Java, C#, Go, Rust, JavaScript, PHP… |
| **Paradigma** | Imperativo y procedimental |
| **Tipado** | Estático y **débil**: las conversiones son fáciles y a menudo silenciosas |
| **Memoria** | **Manual**: `malloc` / `free`, sin red de seguridad |
| **Ejecución** | Compilado a nativo |
| **Estado** | 🟢 **Tecnología fundamental** — no debería llamarse legacy |

---

## 📜 Historia

A finales de los 60, Ken Thompson escribió **B** en los Laboratorios Bell —una simplificación de
**BCPL**, de Martin Richards— para el PDP-7. B no tenía tipos: todo era una palabra de máquina. Al
llegar el PDP-11, con bytes y palabras de distinto tamaño, esa carencia se volvió insostenible, y
**Dennis Ritchie** extendió B con un sistema de tipos. El resultado se llamó **C** por continuación
alfabética.

El movimiento que lo cambió todo llegó en **1973**: Thompson y Ritchie **reescribieron el núcleo de
Unix en C**. Hasta entonces, un sistema operativo era ensamblador por definición. Al escribirlo en un
lenguaje de alto nivel, Unix se volvió **portable**: llevarlo a una máquina nueva pasó de ser un
proyecto de años a ser un proyecto de meses. Unix se extendió, y C viajó con él a todas partes.

En **1978**, Brian Kernighan y Dennis Ritchie publicaron *The C Programming Language*: 228 páginas
que sirvieron a la vez de tutorial, de manual y de estándar de facto durante una década. Es
probablemente el libro de programación más influyente jamás escrito, y su ejemplo de apertura fijó
para siempre el ritual del `hello, world`.

La estandarización llegó con **ANSI C (C89/C90)**, y después **C99** (comentarios `//`, `bool`,
declaraciones en medio del bloque, arrays de longitud variable), **C11** (hilos, atómicos,
`_Generic`), **C17** (correcciones) y **C23** (`constexpr`, `nullptr`, `typeof`, `bool` de verdad,
literales binarios, atributos).

El diseño se resume en una frase de Kernighan y Ritchie que sigue siendo la mejor descripción del
lenguaje: **"C no es un lenguaje grande, y no está bien servido por un libro grande."** Confía en el
programador, no impide lo que parece peligroso, y a cambio no oculta nada.

## 🏭 Dónde vive hoy

- **Núcleos de sistemas operativos**: Linux (decenas de millones de líneas), el núcleo de Windows,
  los BSD, macOS/XNU.
- **Firmware y embebidos**: desde el microcontrolador de un termostato hasta el software de un
  automóvil, bajo normas como **MISRA C**. Es, con mucho, el mayor volumen de C que se escribe hoy.
- **Infraestructura de Internet**: OpenSSL, nginx, curl, OpenSSH, los servidores DNS.
- **Bases de datos**: SQLite, PostgreSQL, MySQL, Redis.
- **Los intérpretes de otros lenguajes**: **CPython**, **PHP**, **Ruby (MRI)**, **Perl**, **Lua**, el
  motor de **R**. Cuando escribes Python, ejecutas C.
- **Bibliotecas numéricas y multimedia**: FFmpeg, zlib, libpng, la capa nativa de NumPy.
- **Herramientas**: git, GCC, los coreutils, prácticamente cualquier utilidad de Unix.

## 🧠 Por qué no es legacy

**1. Es la ABI universal.** No hay una "ABI de Python" ni una "ABI de Rust" a la que otros lenguajes
puedan hablar. Hay la ABI de C. Todo mecanismo de interoperabilidad —`ctypes`, JNI, P/Invoke, cgo,
`extern "C"` de Rust, N-API de Node— consiste en **fingir ser C** durante un momento. Mientras exista
software escrito en más de un lenguaje, existirá esa necesidad.

**2. Es la superficie del sistema operativo.** Las llamadas al sistema de Linux, la API de Windows y
POSIX están definidas en C. Programar contra el sistema operativo es hablar C, aunque lo escribas con
otro nombre.

**3. Modelo mental transparente.** No hay recolector de basura que se despierte en un momento
inconveniente, ni destructores implícitos, ni asignaciones ocultas. En un manejador de interrupción o
en un sistema de tiempo real duro, esa previsibilidad no es una preferencia estética: es un requisito.

**4. Portabilidad extrema.** Hay compilador de C para arquitecturas que ningún otro lenguaje soporta.
Un microcontrolador de 8 bits con 2 KB de memoria tiene compilador de C.

**5. Cuarenta años de código probado en producción.** No como deuda: como activo. SQLite es
posiblemente el software más desplegado del mundo y su fiabilidad procede de una suite de pruebas
descomunal sobre una base de C estable.

> **Y la crítica honesta, que también forma parte de la ficha.** La gestión manual de memoria de C es
> el origen de una parte muy grande de las vulnerabilidades graves de la industria: desbordamientos de
> búfer, uso después de liberar, doble liberación. Los análisis públicos de bases de código grandes
> han situado repetidamente esa familia de fallos en torno a **dos tercios** de las vulnerabilidades
> críticas de memoria, y las agencias de ciberseguridad recomiendan hoy lenguajes seguros por diseño
> para código nuevo. Eso **no** convierte a C en obsoleto —Rust y Zig existen porque el problema es
> difícil, no porque esté resuelto—, pero sí significa que elegir C en 2026 debe ser una decisión
> argumentada, no una inercia. Esta es la tensión de fondo de todo el debate actual sobre lenguajes de
> sistemas, y merece la pena entenderla antes de tomar partido.

## 🔄 Lo que se ha modernizado

- **C23**, el estándar vigente: `constexpr`, `nullptr` (adiós a la ambigüedad de `NULL`), `typeof`,
  `bool`/`true`/`false` como palabras del lenguaje, literales binarios `0b`, atributos `[[...]]` y
  `#embed` para incrustar ficheros binarios en tiempo de compilación.
- **Herramientas de seguridad que cambian el juego**: los *sanitizers* (**ASan**, **UBSan**, **TSan**,
  **MSan**) detectan en ejecución los errores de memoria y el comportamiento indefinido; **fuzzing**
  continuo (libFuzzer, AFL++, OSS-Fuzz) encuentra fallos que ninguna revisión humana encontraría; y
  el análisis estático (clang-tidy, Coverity, el analizador de GCC) atrapa clases enteras de defectos.
  El C que se escribe hoy con este instrumental es mucho más seguro que el de hace quince años.
- **Sistemas de construcción y dependencias modernos**: CMake, Meson, Ninja, y gestores de paquetes
  como Conan o vcpkg que también sirven a proyectos C.
- **Normas de codificación para dominios críticos**: **MISRA C** en automoción e industria,
  **CERT C** en seguridad, con verificación automatizada.
- **Convivencia con Rust**: el núcleo de Linux admite desde 2022 controladores escritos en Rust
  llamando a las interfaces C existentes. El futuro más probable no es la sustitución, sino la
  frontera bien definida — que es, otra vez, la ABI de C.

## ⚙️ Cómo se ejecuta hoy

```bash
cc total.c -o total          # el comando de la clase 041
gcc -std=c23 -Wall -Wextra -O2 total.c -o total

# Con red de seguridad, que es como conviene desarrollar:
gcc -fsanitize=address,undefined -g total.c -o total
```

## 🧪 El programa de la clase 041 en C

Es el mismo que se ejecuta y se verifica en la
[clase 041](../classes/parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md);
aquí interesa por comparación con las demás fichas.

```c
#include <stdio.h>

int main(void) {
    double precio, cantidad, descuento;

    if (scanf("%lf %lf %lf", &precio, &cantidad, &descuento) != 3) {
        return 1;
    }

    double total = precio * cantidad * (1 - descuento);
    printf("Total: %.2f\n", total);
    return 0;
}
```

**Lo que hay que ver, comparando con las otras fichas de esta sección.**

- **`&precio` es la diferencia fundamental.** C solo pasa argumentos **por valor**, así que para que
  `scanf` pueda escribir en tus variables hay que darle su **dirección**. [Fortran](fortran.md) pasa
  por referencia y no lo necesita; [Pascal](pascal.md) tiene `var`; [COBOL](cobol.md) no tiene
  funciones con parámetros en el sentido moderno. Ese `&` es toda una filosofía: **el programador
  gestiona las direcciones explícitamente.**
- **Comprobar el retorno de `scanf` no es opcional.** Devuelve cuántos elementos convirtió. Si la
  entrada no encaja, las variables quedan **sin inicializar** y leerlas es comportamiento indefinido.
  Casi todo el código de ejemplo que circula omite esta comprobación, y ese hábito es exactamente el
  problema que discutimos arriba.
- **`%lf` en `scanf` y `%f` en `printf`** para el mismo `double`. La asimetría existe porque en una
  función variádica los `float` se promueven a `double`, así que `printf` no puede distinguirlos, pero
  `scanf` recibe punteros y sí debe saber el tamaño. Es un detalle histórico que sigue sorprendiendo.
- **`printf` no valida nada.** Si el formato no coincide con los argumentos, el programa lee la pila
  como si fuera lo que dijiste. Los compiladores modernos avisan con `-Wformat`, pero el lenguaje
  no lo impide.
- **Todo esto es una elección de diseño coherente.** C te deja hacer lo que quieras y no te vigila. Es
  la razón de que sea rápido, portable y universal, y también la razón de que haya que escribirlo con
  disciplina y herramientas.

## 📚 Fuentes y bibliografía

- [cppreference — sección C](https://en.cppreference.com/w/c) — la mejor referencia en línea del
  lenguaje y su biblioteca estándar.
- [Documentación de GCC](https://gcc.gnu.org/onlinedocs/) y [Clang](https://clang.llvm.org/docs/) —
  incluidos los *sanitizers*, que conviene conocer desde el primer día.
- [SEI CERT C Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c) — reglas concretas para
  escribir C seguro.
- **Brian Kernighan, Dennis Ritchie**, *The C Programming Language*, 2.ª ed., Prentice Hall — "el
  K&R". Anterior a C99, así que no lo uses como referencia de la versión actual, pero léelo: enseña a
  pensar en C como ningún otro.
- **Ben Klemens**, *21st Century C*, 2.ª ed., O'Reilly — cómo escribir C hoy, con las herramientas y
  las prácticas actuales. El complemento moderno al K&R.
- **Robert Seacord**, *Effective C*, 2.ª ed., No Starch Press — actualizado a C23 y escrito por uno de
  los autores de los estándares de seguridad del CERT.
- **Peter van der Linden**, *Expert C Programming: Deep C Secrets* — los rincones oscuros del lenguaje,
  explicados con humor y precisión.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [C++](cpp.md) · [Assembler](assembler.md) · [Fortran](fortran.md)
