# 🔧 Tcl/Tk — 1988

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El lenguaje con el que se diseñan los chips.** Cada procesador moderno pasa por un flujo de
herramientas de diseño electrónico, y ese flujo se conduce con guiones Tcl. Synopsys, Cadence y
Xilinx exponen sus herramientas como comandos Tcl. Es un lenguaje casi invisible que está debajo del
silicio que estás usando ahora mismo.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: Tcl se ejecuta hoy en la cadena de herramientas EDA de toda la industria
> del semiconductor**, en equipamiento de red (Cisco IOS lleva Tcl incrustado), en automatización de
> pruebas con **Expect**, y detrás de `tkinter`, la biblioteca gráfica que viene con Python. El
> lenguaje publicó **Tcl 9.0** en 2024: sigue en desarrollo.
>
> Entra porque **lleva al extremo un concepto que el núcleo esconde**: en Tcl **no hay sintaxis, solo
> comandos**. `if`, `while`, `for` y `proc` no son palabras clave del lenguaje: son procedimientos
> normales que reciben cadenas y las evalúan. Eso significa que **puedes escribir tus propias
> estructuras de control** sin macros ni compilador, algo que en el núcleo entero solo se aproxima
> con las lambdas. Y su regla "todo es una cadena" (*EIAS*) es la versión más pura del tipado débil
> que existe: aclara de golpe qué significan realmente la coerción de JavaScript o el tipado de PHP.

| | |
|---|---|
| **Año** | 1988 (Tcl); **Tk** en 1991; versión vigente **Tcl 9.0** (2024) |
| **Autoría** | **John Ousterhout**, Universidad de California en Berkeley |
| **Familia** | Scripting dinámico / lenguajes de comandos incrustables |
| **Paradigma** | Imperativo y procedimental; OO desde 8.6 con **TclOO** |
| **Tipado** | **Dinámico y débil** — *Everything Is A String* |
| **Memoria** | Gestionada por conteo de referencias, con objetos con doble representación |
| **Ejecución** | Interpretado a bytecode; diseñado para **incrustarse** dentro de una aplicación C |
| **Estado** | 🟡 **Nicho industrial muy sólido** — EDA, redes, testing, GUI multiplataforma |

---

## 📜 Historia

A finales de los 80, **John Ousterhout** dirigía en Berkeley un grupo que construía herramientas de
diseño de circuitos integrados. Observó un patrón repetido: cada herramienta acababa necesitando un
lenguaje de comandos propio, cada uno se inventaba desde cero, y todos eran malos. Su propuesta fue
escribir **un solo lenguaje de comandos, pequeño y empotrable**, que cualquier aplicación en C
pudiera enlazar y extender con sus propios comandos.

Eso es **Tcl** (*Tool Command Language*, pronunciado "tickle"). Su diseño está subordinado por
completo a ese objetivo: sintaxis mínima (doce reglas caben en una página de manual), una única
representación de datos —la cadena—, y una API en C para registrar comandos nuevos que es tan simple
que se aprende en una tarde.

En 1991 llegó **Tk**, el kit de widgets gráficos. Fue el primer sistema que permitió construir una
interfaz gráfica multiplataforma con veinte líneas de guion, y su impacto fue enorme: **Python lo
adoptó como `tkinter`** (que sigue siendo la GUI de la biblioteca estándar) y Perl y Ruby hicieron lo
propio. Buena parte de la gente que ha usado Tk nunca ha escrito una línea de Tcl.

Un año antes, en 1990, **Don Libes** escribió **Expect** sobre Tcl para automatizar programas
interactivos: guiones que "esperan" un texto en la salida de otro programa y responden. Sigue siendo
la herramienta canónica para automatizar sesiones de consola, y es la razón de que Tcl viva en la
administración de equipos de red.

La industria EDA lo adoptó y ya no lo soltó: hoy los flujos de síntesis y de disposición física
(*place & route*) se describen en Tcl porque las herramientas de Synopsys, Cadence y AMD/Xilinx
exponen su funcionalidad como comandos Tcl.

## 🏭 Dónde sobrevive hoy

- **Diseño electrónico (EDA)**: Synopsys Design Compiler, Cadence Innovus y Genus, AMD Vivado. Los
  guiones de síntesis, restricciones temporales (**SDC**, que es un formato Tcl) y flujos de
  fabricación se escriben en Tcl.
- **Equipos de red**: Cisco IOS incorpora un intérprete Tcl para automatización en el propio equipo.
- **Automatización de pruebas y de sesiones interactivas**: **Expect**.
- **Interfaces gráficas**: **Tk** sigue siendo la GUI multiplataforma con menos fricción, y llega a
  millones de usuarios a través de `tkinter` de Python.
- **Software científico e industrial**: incrustado como capa de guion en aplicaciones grandes de C++.

## 🧠 Por qué no ha muerto

**1. Incrustarlo es trivial.** Enlazar el intérprete y registrar comandos propios desde C son unas
pocas llamadas. Para un fabricante de herramientas, eso significa exponer todo su producto como
lenguaje de guion con un esfuerzo mínimo. Ninguna alternativa —ni Python ni Lua— es más simple de
integrar a ese nivel.

**2. Los flujos de fabricación no se tocan.** Un guion de síntesis validado sobre un proceso de
fabricación concreto es un activo que se hereda de proyecto en proyecto. Cambiar el lenguaje del
flujo no aporta nada y arriesga mucho.

**3. La sintaxis mínima resiste el paso del tiempo.** Un guion Tcl de 1995 se ejecuta hoy. La
compatibilidad hacia atrás ha sido casi total durante treinta años.

**4. Estabilidad como característica, no como estancamiento.** Tcl 8.6 trajo corrutinas y OO; Tcl 9.0
trajo soporte completo de Unicode y ficheros grandes. Evoluciona despacio y a propósito.

## 🔄 Lo que se ha modernizado

- **Tcl 9.0 (2024)**, la primera versión mayor en veinte años: **Unicode completo** más allá del plano
  básico, ficheros y cadenas **de más de 2 GB**, enteros de 64 bits, y sistema de ficheros virtual con
  soporte de ZIP integrado (una aplicación puede llevar sus recursos dentro del propio ejecutable).
- **TclOO** (desde 8.6): un sistema de objetos **en el núcleo del lenguaje**, con metaclases y
  mixins, que unificó los tres o cuatro sistemas OO que competían en la comunidad.
- **Corrutinas** (8.6): concurrencia cooperativa sin hilos, y un manejo de excepciones estructurado
  con `try`/`trap`/`finally`.
- **Tk moderno**: los *widgets* temáticos `ttk` adoptan el aspecto nativo de Windows, macOS y Linux;
  la interfaz de 2026 no se parece a la de los 90. Y sigue llegando a millones de usuarios a través
  de `tkinter`.
- **Starkit/Starpack**: empaquetar aplicación e intérprete en **un solo fichero ejecutable** — la
  misma idea del binario autocontenido de Go, dos décadas antes.
- **Vigencia en EDA**: las herramientas de Synopsys, Cadence y AMD siguen exponiendo su
  funcionalidad como comandos Tcl en sus versiones actuales. Aquí no hay migración a la vista.

## ⚙️ Cómo se ejecuta hoy

```bash
sudo apt-get install -y tcl

tclsh total.tcl < entrada.txt
echo "15000 2 0.10" | tclsh total.tcl
# Total: 27000.00

# Con interfaz gráfica:
wish miapp.tcl
```

**Ecosistema:** **`tclsh`** (intérprete), **`wish`** (intérprete con Tk cargado), **Tcllib** y
**Tklib** (bibliotecas estándar de la comunidad), y **Starkit/Starpack**, un mecanismo para empaquetar
una aplicación entera —intérprete, código y recursos— en un **único fichero ejecutable**, mucho antes
de que eso fuera habitual.

## 🧪 El programa de la clase 041 en Tcl

```tcl
gets stdin linea
lassign [split [string trim $linea]] precio cantidad descuento
set total [expr {$precio * $cantidad * (1 - $descuento)}]
puts [format "Total: %.2f" $total]
```

**Recorrido, línea a línea.**

- `gets stdin linea` — `gets` **no** es una palabra clave: es un comando, y `stdin` y `linea` son sus
  dos argumentos. Con dos argumentos, guarda la línea leída en la variable indicada y devuelve su
  longitud. Toda la sintaxis de Tcl es esta: `comando arg1 arg2 ...`, separados por espacios.
- Los **corchetes** `[...]` son **sustitución de comando**: se ejecuta lo de dentro y su resultado se
  inserta en su lugar. Equivalen a la `$(...)` del shell. `[split [string trim $linea]]` primero
  recorta espacios y luego parte por espacios en blanco.
- `lassign lista a b c` reparte los elementos de una lista en varias variables. Y aquí aparece la
  idea nuclear: **la lista es una cadena** con los elementos separados por espacios. `split` no
  construye una estructura nueva; produce una cadena que Tcl sabe interpretar como lista.
- `set total [...]` asigna. No hay operador `=`: `set` es un comando.
- **`expr` con llaves es la línea importante.** Tcl no tiene operadores aritméticos; `expr` es un
  comando que recibe una expresión y la evalúa. Las **llaves** impiden que Tcl sustituya las
  variables *antes* de pasar el texto a `expr`, de modo que `expr` recibe la expresión con los
  nombres y la compila una sola vez. Sin llaves —`expr $a * $b`— funciona, pero es más lento y, si
  una variable contiene texto con espacios o corchetes, **se reinterpreta**, lo que es un agujero de
  inyección clásico. La regla de la comunidad es absoluta: **`expr` siempre con llaves**.
- `format "%.2f" $total` es el `printf` de Tcl; `puts` escribe la línea.

**Y ahora el motivo real de estudiarlo.** En Tcl, `if` es un comando corriente. Puedes escribir el
tuyo:

```tcl
proc repetir {n cuerpo} {
    for {set i 1} {$i <= $n} {incr i} {
        uplevel 1 $cuerpo
    }
}

set contador 0
repetir 3 { incr contador ; puts "vuelta $contador" }
```

`repetir` recibe el bloque `{ ... }` como una **cadena** y `uplevel 1` la evalúa **en el ámbito de
quien llamó**, de modo que `contador` es la variable del llamante y no una copia. Acabas de añadir
una estructura de control al lenguaje con un procedimiento de cuatro líneas, sin macros y sin tocar
el compilador. Su pareja, `upvar`, hace lo mismo con variables y es la forma de escribir un
procedimiento que modifica los argumentos de su llamante.

Esa capacidad —que las estructuras de control sean código de usuario— la comparten muy pocos
lenguajes: [Lisp](common-lisp.md) con macros, [Smalltalk](smalltalk.md) con bloques, y Tcl con la
evaluación explícita de cadenas.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En Tcl es… |
|---|---|
| `x = 5` | `set x 5` |
| `$(comando)` del shell | `[comando]` — sustitución de comando |
| `x = a * b` | `set x [expr {$a * $b}]` |
| `print(x)` | `puts $x` |
| `def f(a, b):` | `proc f {a b} { ... }` |
| `if cond:` | `if {$cond} { ... } else { ... }` — `if` es un comando |
| `for i in range(n)` | `for {set i 0} {$i < $n} {incr i} { ... }` |
| Lista / array | `list`, `lindex`, `lappend`, `lsort` — y todo es cadena |
| Diccionario | `dict get`, `dict set`, o los *arrays asociativos* `a(clave)` |
| `"%.2f" % x` | `format "%.2f" $x` |
| `import` | `package require nombre` |
| Paso por referencia | `upvar` |

## ⚠️ Errores comunes al leerlo

- **`expr` sin llaves.** Además de ser lento, permite inyección. Es el error que más aparece en
  revisiones de código Tcl.
- **Confundir `{}` con un bloque de código.** Las llaves son **comillas que no sustituyen nada**. Que
  `if {...} { ... }` parezca C es una coincidencia afortunada: el segundo grupo es simplemente una
  cadena que `if` decidirá evaluar.
- **Espacios obligatorios.** `set x[expr 1]` no funciona: los argumentos se separan por espacios,
  siempre. `if{$a}` tampoco, porque el comando se llamaría `if{$a}`.
- **Creer que hay tipos.** `"10"`, `10` y `10.0` son la misma cadena hasta que un comando decide cómo
  leerla. Internamente Tcl cachea una representación numérica por rendimiento, pero eso es invisible
  y no cambia la semántica.
- **Usar comillas dobles donde van llaves.** `"..."` **sí** sustituye variables y comandos; `{...}` no.
  Elegir mal cambia el momento en que se evalúa algo.
- **Ignorar `Tcl_Eval` en código C.** Si lees el fuente de una herramienta EDA, la mitad del lenguaje
  no está en Tcl: son comandos registrados desde C. La documentación del comando está en el manual de
  la herramienta, no en el de Tcl.

## 📚 Fuentes y bibliografía

- [tcl-lang.org](https://www.tcl-lang.org/) — sitio oficial, con el manual de referencia de cada
  comando.
- [Tcl/Tk 9.0 — novedades](https://www.tcl-lang.org/software/tcltk/9.0.html) — el estado actual del
  lenguaje.
- [The Tcler's Wiki](https://wiki.tcl-lang.org/) — la memoria colectiva de la comunidad; treinta años
  de recetas.
- **John Ousterhout, Ken Jones**, *Tcl and the Tk Toolkit*, 2.ª ed., Addison-Wesley — escrito por el
  autor del lenguaje; explica el porqué de cada decisión de diseño.
- **Brent Welch, Ken Jones**, *Practical Programming in Tcl and Tk*, 4.ª ed., Prentice Hall — el
  manual práctico de referencia.
- **Don Libes**, *Exploring Expect*, O'Reilly — automatización de programas interactivos, por el autor
  de Expect.
- **John Ousterhout**, *Scripting: Higher Level Programming for the 21st Century*, IEEE Computer, 1998
  — el artículo que argumentó por qué los lenguajes de guion complementan a los de sistemas en lugar
  de competir con ellos.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [Perl](perl.md) · [Common Lisp](common-lisp.md) · [AutoLISP](autolisp.md)
