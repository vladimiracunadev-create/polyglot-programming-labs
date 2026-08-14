# 🧠 Lisp / Common Lisp — 1958

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El segundo lenguaje de alto nivel de la historia, y el que se adelantó a todos.** Recolección de
basura, funciones de primera clase, tipado dinámico, REPL, código que se manipula a sí mismo: Lisp
tenía todo eso cuando el resto del mundo programaba con tarjetas perforadas. Los demás lenguajes
llevan sesenta años alcanzándolo.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: Common Lisp se ejecuta hoy.** SBCL publica una versión al mes,
> Quicklisp distribuye miles de bibliotecas, y hay implementaciones comerciales con soporte
> (LispWorks, Allegro CL) vendiéndose a industria. Su variante **[AutoLISP](autolisp.md)** viene
> incluida en AutoCAD, uno de los programas de ingeniería más usados del planeta. Y **Emacs Lisp**
> configura el editor de una parte considerable de los programadores del mundo.
>
> Entra porque **muestra dos conceptos que el núcleo entero no tiene**. El primero es la
> **homoiconicidad**: en Lisp el código y los datos tienen la misma forma —listas—, así que un
> programa puede construir y transformar programas con las mismas herramientas con que manipula una
> lista. De ahí salen las **macros**, que no son plantillas de texto como en C sino transformaciones
> reales del árbol sintáctico: en Lisp puedes **añadir sintaxis al lenguaje**. El segundo es el
> **sistema de condiciones y reinicios**, un manejo de errores estrictamente más potente que el
> `try/catch` que casi todos heredamos. Ver Lisp es entender qué le falta a los demás.

| | |
|---|---|
| **Año** | 1958 (McCarthy); **Common Lisp** estandarizado en ANSI X3.226 en 1994 |
| **Autoría** | **John McCarthy** (MIT); Common Lisp por un comité de la comunidad |
| **Familia** | **Lisp** — la raíz de Scheme, Racket, Clojure, Emacs Lisp y AutoLISP |
| **Paradigma** | Multiparadigma: funcional, imperativo y OO (CLOS, con **despacho múltiple**) |
| **Tipado** | **Dinámico y fuerte**, con declaraciones de tipo opcionales para optimizar |
| **Memoria** | Recolector de basura — Lisp fue donde se inventó |
| **Ejecución** | Compilado a nativo en tiempo de ejecución; REPL siempre disponible |
| **Estado** | 🟡 **Nicho vivo** — IA simbólica, CAD, sistemas con mucho DSL, investigación |

---

## 📜 Historia

En 1958 **John McCarthy** trabajaba en el MIT sobre problemas de inteligencia artificial y necesitaba
manipular **expresiones simbólicas**, no números. Su artículo de 1960, *Recursive Functions of
Symbolic Expressions and Their Computation by Machine*, define un lenguaje matemático basado en el
cálculo lambda y en una sola estructura de datos: la **lista**.

McCarthy había definido, como ejercicio teórico, una función `eval` que interpretaba expresiones del
propio lenguaje. Su estudiante **Steve Russell** se dio cuenta de algo que McCarthy no había
previsto: esa `eval` se podía **implementar en código máquina**, y entonces habría un intérprete de
Lisp de verdad. Lo hizo, y así nació el primer Lisp ejecutable — junto con la idea del REPL y de la
programación interactiva.

Lisp introdujo o popularizó, décadas antes que nadie:

- La **recolección de basura automática**.
- Las **funciones como valores de primera clase** y las de orden superior.
- La **recursión** como herramienta central.
- El **tipado dinámico** con comprobación en tiempo de ejecución.
- El **REPL** y el desarrollo interactivo.
- Las **macros** y la metaprogramación sintáctica.
- La **condicional** `cond` — sí, el `if/else if` viene de aquí.

Durante los 70 y 80 proliferaron dialectos: MacLisp, InterLisp, ZetaLisp, Scheme (1975, minimalista y
académico). Se llegó a construir hardware específico —las **máquinas Lisp** de Symbolics y LMI— con el
lenguaje como sistema operativo. Cuando la financiación de la IA se desplomó a finales de los 80 (el
llamado "invierno de la IA"), aquella industria se hundió con ella.

Para frenar la fragmentación, un comité produjo en 1984 *Common Lisp the Language* y en **1994** el
estándar **ANSI Common Lisp**: un lenguaje grande, deliberadamente pragmático, que unificó los
dialectos e incorporó **CLOS** (*Common Lisp Object System*), probablemente el sistema de objetos más
potente jamás estandarizado.

## 🏭 Dónde sobrevive hoy

- **CAD e ingeniería**: **[AutoLISP](autolisp.md)** dentro de AutoCAD — con diferencia, el Lisp con
  más usuarios del mundo, aunque casi ninguno se llame a sí mismo "programador Lisp".
- **Configuración y extensión de herramientas**: **Emacs Lisp**; el editor Emacs es, literalmente, un
  intérprete de Lisp con un editor escrito encima.
- **Sistemas con reglas complejas**: motores de planificación, sistemas expertos, optimización
  combinatoria. El caso históricamente documentado es **ITA Software**, el motor de búsqueda de
  vuelos escrito en Common Lisp que compró Google y que está detrás de Google Flights.
- **Investigación**: procesamiento del lenguaje, razonamiento simbólico, demostradores de teoremas,
  y como lenguaje de implementación de otros lenguajes.
- **Aeroespacial**: el *Remote Agent* de la NASA que controló autónomamente la sonda **Deep Space 1**
  en 1999 estaba escrito en Common Lisp; el equipo llegó a **depurar el software en vuelo, a 150
  millones de kilómetros, conectándose al REPL de la nave**. Es probablemente la mejor anécdota que
  existe sobre desarrollo interactivo.

## 🧠 Por qué no ha muerto

**1. Las macros permiten construir el lenguaje que el problema necesita.** Como el código es una
lista, una macro recibe la estructura del código y devuelve otra estructura, antes de compilar. En
un dominio complejo puedes crear notación propia y escribir la solución en ella. En otros lenguajes,
eso exige un preprocesador, un generador de código o un DSL externo con su parser.

**2. El sistema de condiciones es superior al `try/catch`.** Cuando una función de Lisp señala un
error, el manejador se ejecuta **antes de desenrollar la pila**, y puede elegir entre varios
**reinicios** (*restarts*) que la función que falló dejó disponibles: reintentar, usar otro valor,
saltar el elemento. En Java o Python, para cuando atrapas la excepción, el contexto ya se destruyó y
la única opción es reintentar todo desde fuera. [PL/I](pl-i.md) tuvo una idea parecida en 1964; casi
nadie más la siguió.

**3. Desarrollo interactivo real.** Con SLIME/Sly sobre Emacs puedes recompilar una única función
dentro de una imagen en ejecución, con el estado intacto. Es el mismo modelo de trabajo vivo de
[Smalltalk](smalltalk.md).

**4. CLOS y el despacho múltiple.** Un método de CLOS se selecciona según los tipos de **todos** sus
argumentos, no solo del receptor. Eso resuelve limpiamente el problema del "doble despacho" que en
Java o C# obliga al patrón *Visitor*. Además, el **Protocolo de Metaobjetos (MOP)** permite
modificar cómo funciona la propia orientación a objetos.

**5. Es rápido.** SBCL compila a código nativo. La fama de "lenguaje lento e interpretado" viene de
los años 70 y hoy es simplemente falsa.

## 🔄 Lo que se ha modernizado

El estándar ANSI está congelado desde 1994 —eso es una decisión, no un abandono—, pero **todo lo que
rodea al lenguaje se ha renovado**:

- **SBCL publica una versión al mes**, con mejoras continuas de compilador y recolector de basura.
  Compila a nativo y es competitivo en rendimiento con lenguajes mucho más jóvenes.
- **Gestión de dependencias moderna**: **Quicklisp** para bibliotecas, y **Qlot** o **CLPM** para
  fijar versiones por proyecto, que es lo que faltaba para reproducibilidad real.
- **Web y servicios**: **Clack** y **Hunchentoot** como servidores, **Jonathan** y **Yason** para
  JSON, **Dexador** como cliente HTTP. Construir una API REST en Common Lisp es rutinario.
- **Coalton**: un lenguaje con **tipado estático al estilo ML**, con inferencia y tipos algebraicos,
  implementado **como una biblioteca de macros** sobre Common Lisp e interoperable con él. Es la mejor
  demostración posible de para qué sirven las macros: añadir un sistema de tipos a un lenguaje
  dinámico sin cambiar el compilador.
- **Herramientas de edición actuales**: además de Emacs con SLIME/Sly, hay extensiones para
  **VS Code** (Alive) y para IntelliJ.
- **Uso reciente documentado**: la computación cuántica de Rigetti desarrolló su compilador **Quilc**
  y su simulador en Common Lisp, precisamente por la manipulación simbólica.

## ⚙️ Cómo se ejecuta hoy

```bash
sudo apt-get install -y sbcl

sbcl --script total-venta.lisp < entrada.txt

# El REPL, que es donde de verdad se trabaja:
sbcl
* (+ 1 2)
3
```

**Implementaciones:** **SBCL** (*Steel Bank Common Lisp*, libre, la más usada y la más rápida),
**CCL** (Clozure), **ECL** (empotrable en C), **ABCL** (sobre la JVM), y las comerciales
**LispWorks** y **Allegro CL** (Franz), con IDE, entrega de aplicaciones y soporte.

**Ecosistema:** **[Quicklisp](https://www.quicklisp.org/)** es el gestor de bibliotecas de facto y
**ASDF** el sistema de construcción. Para editar, **Emacs + SLIME/Sly** sigue siendo la experiencia
de referencia, aunque hay extensiones para VS Code (Alive) y un plugin para IntelliJ.

## 🧪 El programa de la clase 041 en Common Lisp

```lisp
;;; total-venta.lisp — clase 041
(setf *read-default-float-format* 'double-float)

(let* ((precio    (read))
       (cantidad  (read))
       (descuento (read))
       (total     (* precio cantidad (- 1 descuento))))
  (format t "Total: ~,2F~%" total))
```

**Recorrido, línea a línea.**

- **Todo son paréntesis, y la regla es una sola:** `(operador argumento argumento ...)`. El primer
  elemento de la lista es lo que se aplica; el resto, sus argumentos. `(* precio cantidad)` es
  multiplicación en notación prefija. Esa uniformidad —conocida como *s-expresiones*— es exactamente
  lo que hace posible que un programa manipule programas: no hay sintaxis especial que analizar.
- `*read-default-float-format*` es una **variable global especial** (la convención `*asteriscos*` las
  marca). Le decimos al lector que los literales reales sean de doble precisión. Fíjate en que estamos
  **configurando el analizador sintáctico del lenguaje desde el propio programa**; en la mayoría de
  los lenguajes eso ni siquiera es expresable.
- `(read)` es una función asombrosa por lo que hace: lee de la entrada estándar **una expresión de
  Lisp** y devuelve el objeto correspondiente. `15000` llega como entero, `0.10` como real. No hay
  `split`, ni `parseFloat`, ni conversión de tipos: el lector del lenguaje es también el analizador
  de la entrada. Es el mismo `read` que usa el REPL.
- `let*` liga variables locales **en secuencia**, de modo que `total` puede usar `precio`, `cantidad`
  y `descuento` ya calculados. Su hermano `let` liga en paralelo y no lo permitiría. Que exista esa
  distinción explícita es típico de Lisp: el orden de evaluación no se deja a la costumbre.
- `(- 1 descuento)` es `1 - descuento`. Cuesta un rato acostumbrarse, y a cambio no hay que memorizar
  ninguna tabla de precedencia de operadores: la estructura del paréntesis **es** la precedencia.
- `format` es un mini-lenguaje de plantillas dentro del lenguaje. `~,2F` significa "real con 2
  decimales" y `~%` es el salto de línea. El primer argumento `t` es el destino (la salida estándar).
  `format` es notoriamente potente: tiene condicionales, iteración sobre listas y hasta pluralización.

**Y ahora el motivo real de estudiarlo.** Supón que quieres una notación propia para las reglas de
precios de tu negocio. En Lisp la creas:

```lisp
(defmacro con-descuento ((var porcentaje) &body cuerpo)
  "Ejecuta CUERPO con VAR ligada al factor multiplicador del descuento."
  `(let ((,var (- 1 (/ ,porcentaje 100))))
     ,@cuerpo))

(con-descuento (factor 10)
  (format t "Total: ~,2F~%" (* 15000 2 factor)))
;; => Total: 27000.00
```

`con-descuento` **no es una función**: es una macro que se ejecuta en tiempo de compilación y
**reescribe el código** antes de compilarlo. El acento grave abre una plantilla, la coma inserta un
valor y `,@` inserta una lista de expresiones. El resultado es una construcción sintáctica nueva,
indistinguible de las que trae el lenguaje. En Python o Java, para conseguir esto harías falta un
generador de código externo; en Lisp es una función más que devuelve listas, porque **el código es
una lista**.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En Common Lisp es… |
|---|---|
| `a + b * c` | `(+ a (* b c))` — prefijo, sin precedencia que memorizar |
| `x = 5` | `(setf x 5)` — y `setf` funciona sobre cualquier "lugar" |
| Variable local | `(let ((x 1) (y 2)) ...)` |
| `def f(x): ...` | `(defun f (x) ...)` |
| Lambda | `(lambda (x) ...)` |
| `if / elif / else` | `(if c a b)` o `(cond (c1 ...) (c2 ...) (t ...))` |
| `switch` | `(case x (1 ...) (2 ...) (otherwise ...))` |
| Clase con métodos | `defclass` + `defgeneric` + `defmethod` — **los métodos viven fuera de la clase** |
| `try / catch / finally` | `handler-case`, `handler-bind` + `restart-case`, `unwind-protect` |
| Anotaciones / decoradores | `defmacro` — pero de verdad |
| `null` | `nil`, que además es la lista vacía y el falso lógico |

## ⚠️ Errores comunes al leerlo

- **Contar paréntesis a mano.** No se hace: se usa un editor con emparejamiento y edición
  estructural (paredit, smartparens). Quien lucha con los paréntesis es siempre quien no ha
  configurado el editor.
- **Confundir `list` con `quote`.** `(list 1 2)` evalúa sus argumentos; `'(1 2)` devuelve la lista
  literal sin evaluar. La comilla es la puerta entre "código" y "datos".
- **Creer que `nil` y `false` son cosas distintas.** `nil` es a la vez la lista vacía, el falso lógico
  y el símbolo `nil`. Cualquier otro valor es verdadero, incluido `0`.
- **Escribir macros donde bastaría una función.** El consejo clásico de la comunidad: una macro solo
  se justifica cuando necesitas controlar **si** o **cuándo** se evalúan los argumentos.
- **Comparar con `=`.** `=` es solo para números. Para el resto están `eq`, `eql`, `equal` y `equalp`,
  en orden creciente de laxitud; elegir mal es la fuente clásica de errores sutiles.
- **Asumir que es interpretado y lento.** SBCL compila a nativo, y con declaraciones de tipo puede
  acercarse a C.

## 📚 Fuentes y bibliografía

- [Common Lisp HyperSpec](https://www.lispworks.com/documentation/HyperSpec/Front/) — el estándar
  ANSI en formato navegable; la referencia definitiva.
- [SBCL](https://www.sbcl.org/) y [Quicklisp](https://www.quicklisp.org/) — la implementación y el
  gestor de bibliotecas que usarás.
- [Common Lisp Cookbook](https://lispcookbook.github.io/cl-cookbook/) — recetas prácticas y actuales.
- **Peter Seibel**, *Practical Common Lisp*, Apress —
  [gratis en línea](https://gigamonkeys.com/book/); la mejor entrada para quien ya programa.
- **Paul Graham**, *On Lisp* — el libro sobre macros;
  [descarga gratuita del autor](http://www.paulgraham.com/onlisp.html).
- **Peter Norvig**, *Paradigms of Artificial Intelligence Programming*, Morgan Kaufmann — construye
  sistemas de IA clásica desde cero; uno de los mejores libros de programación jamás escritos, y
  liberado por el autor.
- **Sonya Keene**, *Object-Oriented Programming in Common Lisp* — la referencia sobre CLOS.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [AutoLISP](autolisp.md) · [Smalltalk](smalltalk.md) · [PL/I](pl-i.md)
