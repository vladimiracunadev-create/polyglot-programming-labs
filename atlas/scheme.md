# ◯ Scheme — 1975

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Scheme es el [Lisp](common-lisp.md) minimalista: **su especificación completa cabe en unas cincuenta
páginas**, frente a las mil de Common Lisp. Fue durante décadas el lenguaje con el que se enseñaba a
programar en el MIT, y de él salieron las continuaciones, la recursión de cola garantizada y las
macros higiénicas.

> **🎯 Por qué está en este programa**
>
> Scheme es un **primo de la familia Lisp** ([Atlas](README.md#lisp)), que no tiene representante en
> el núcleo — [Common Lisp](common-lisp.md) y [AutoLISP](autolisp.md) son sus parientes entre los
> lenguajes vivos.
>
> Aporta al programa tres conceptos concretos: **las continuaciones de primera clase**
> ([clase 127](../classes/parte-8-como-funcionan-los-lenguajes/127-la-pila-y-el-marco-de-llamada/README.md)),
> **la recursión de cola garantizada por el estándar** (clase 083) y **las macros higiénicas**
> (clase 122). Y aporta la demostración de que **un lenguaje puede ser minúsculo y completo a la vez**.

| | |
|---|---|
| **Año** | 1975; **R5RS** (1998) el más querido; **R7RS** (2013) el vigente |
| **Autoría** | **Guy L. Steele** y **Gerald Jay Sussman**, MIT |
| **Familia** | Lisp; con el alcance léxico del cálculo lambda de Church |
| **Paradigma** | Multiparadigma con base funcional; sin imponer nada |
| **Tipado** | **Dinámico y fuerte**; numéricos exactos y con torre de tipos |
| **Memoria** | Recolección de basura |
| **Ejecución** | Depende de la implementación: intérprete, bytecode o nativo |
| **Estado** | 🟢 **Vivo**: enseñanza, investigación y **Guile** como lenguaje de extensión de GNU |

---

## 📜 Historia

En **1975**, **Steele** y **Sussman** en el MIT escribieron un intérprete pequeño para estudiar el
**modelo de actores** de Carl Hewitt. Y descubrieron algo que cambió el diseño de lenguajes: **al
implementar los actores con cierres léxicos, actores y funciones resultaban ser lo mismo**.

De ahí salieron **los *Lambda Papers*** —una serie de informes con títulos como *Lambda: The Ultimate
Imperative*— que demostraron que **con lambdas y alcance léxico se pueden construir todas las
estructuras de control**: bucles, condicionales, excepciones y saltos.

Y de ahí las decisiones de Scheme:

- **Alcance léxico**, cuando Lisp usaba dinámico (clase 088).
- **Un solo espacio de nombres** para funciones y valores —lo que se llama *Lisp-1*—, a diferencia de
  Common Lisp.
- **Recursión de cola obligatoria en el estándar**: un bucle escrito como recursión **no consume
  pila** (clase 083).
- **Y minimalismo radical**: si algo se puede construir con lo que hay, no entra en el lenguaje.

**SICP** —*Structure and Interpretation of Computer Programs*, de Abelson y Sussman, 1985— usó Scheme
para enseñar programación en el MIT durante veinte años, y es probablemente **el libro de informática
más influyente jamás escrito**. Está libre en línea.

Y **R6RS (2007)** provocó la única crisis del lenguaje: era grande y prescriptivo, la comunidad se
dividió, y **R7RS (2013)** volvió al minimalismo con un núcleo pequeño y módulos opcionales.

## 🏭 Dónde vive hoy

- **GNU Guile**: es **el lenguaje de extensión oficial del proyecto GNU** (clase 163) — GnuCash,
  GNU Make con Guile, Guix.
- **GNU Guix**: un gestor de paquetes y distribución **completamente definido en Scheme**, con
  construcciones reproducibles bit a bit (clase 144). Es uno de los usos más serios que existen.
- **Enseñanza**: sigue en cursos de introducción y de compiladores.
- **[Racket](racket.md)**, que empezó como Scheme y creció hasta ser otra cosa.
- **Sistemas embebidos**: Chibi Scheme y otras implementaciones diminutas.
- **Y Chez Scheme**, uno de los compiladores más rápidos que existen para un lenguaje dinámico.

## 🧠 Lo que enseña: continuaciones y recursión de cola

**Uno, `call/cc`** —capturar la continuación—, que es la construcción de control más potente que
existe (clase 127):

```scheme
(define (buscar lista objetivo)
  (call/cc
    (lambda (salir)                     ; ← 'salir' ES el resto del cálculo
      (for-each (lambda (x)
                  (if (equal? x objetivo) (salir #t)))
                lista)
      #f)))
```

**`call/cc` da como valor "todo lo que falta por hacer"**, y llamarlo salta ahí. Con eso se pueden
construir —**dentro del lenguaje, sin sintaxis nueva**— excepciones, generadores, corrutinas, hilos
cooperativos y vuelta atrás.

Es la demostración más pura de la tesis de los *Lambda Papers*, y es la razón de que
[Seaside](smalltalk.md) pudiera hacer aplicaciones web con continuaciones (clase 168).

**Dos, la recursión de cola garantizada:**

```scheme
(define (contar n acc)
  (if (= n 0) acc (contar (- n 1) (+ acc 1))))   ; ← NO crece la pila
(contar 10000000 0)                               ; funciona
```

**El estándar obliga a que una llamada en posición de cola no consuma pila** (clase 083). Eso hace que
**el bucle y la recursión sean lo mismo**, y por eso Scheme no necesita `for` ni `while`.

**Y tres, las macros higiénicas:**

```scheme
(define-syntax mi-si
  (syntax-rules ()
    ((_ c t e) (cond (c t) (else e)))))
```

**"Higiénicas" significa que las variables de la macro no capturan las de quien la usa** —el problema
clásico de las macros de [Common Lisp](common-lisp.md) y del preprocesador de [C](c.md) (clase 122)—.
Scheme lo resolvió con `syntax-rules`, y es la solución que después adoptaron
[Rust](rust.md) y [Racket](racket.md).

## 🔄 Lo que se ha modernizado

- **R7RS-small y R7RS-large**: núcleo pequeño más una biblioteca por capas, resolviendo la crisis de
  R6RS.
- **Guile 3** con JIT, y **Chez Scheme** como compilador de referencia por rendimiento.
- **Hoot**: **Guile compilado a WebAssembly con WasmGC** (clase 162).
- **Guix**: la aplicación más ambiciosa del lenguaje, con reproducibilidad verificable.
- **Y `syntax-case`**, macros higiénicas con toda la potencia procedural.

## ⚙️ Cómo se ejecuta hoy

```bash
guile main.scm < entrada.txt          # GNU Guile
chez --script main.scm                 # Chez Scheme, muy rápido
csi -s main.scm                         # Chicken Scheme (compila a C)
```

## 🧪 El programa de la clase 041 en Scheme

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```scheme
(use-modules (ice-9 rdelim))

(let* ((linea   (read-line))
       (campos  (string-split linea #\space))
       (nums    (map string->number campos))
       (total   (* (car nums) (cadr nums) (- 1 (caddr nums)))))
  (format #t "Total: ~,2f~%" total))
```

**Lo que hay que ver.**

- **`(* a b c)` toma tres argumentos**: en Lisp los operadores son funciones normales y **no tienen
  aridad fija**. Es la notación prefija, y es lo que hace que el programa sea una estructura de datos
  (clase 123).
- **`car`, `cadr`, `caddr`** —primero, segundo, tercero— son los nombres históricos de Lisp, de los
  registros del IBM 704 de 1958. **Sobreviven cincuenta años después de que el hardware
  desapareciera**, que es un buen ejemplo de la clase 154.
- **`let*` liga en secuencia**, permitiendo que cada nombre use los anteriores —a diferencia de `let`,
  que liga en paralelo—. Esa distinción explícita es muy de Scheme: **lo que en otros lenguajes es
  implícito, aquí se elige**.
- **`~,2f` es la directiva de formato** con dos decimales, la misma familia que `%.2f`.
- **Y no hay ni una asignación**: todo son enlaces (clase 102).

## 📚 Fuentes y bibliografía

- [SICP](https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/index.html)
  — **Abelson y Sussman**, libre en línea; y las
  [clases en vídeo de 1986](https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/),
  que siguen siendo excelentes.
- [The Scheme Programming Language](https://www.scheme.com/tspl4/) — **R. Kent Dybvig**, libre en
  línea; la referencia práctica.
- [Estándares R7RS](https://small.r7rs.org/) — la especificación entera cabe en un rato de lectura.
- [Manual de GNU Guile](https://www.gnu.org/software/guile/manual/) — para el uso real como lenguaje
  de extensión.
- **Steele y Sussman**, *Lambda: The Ultimate…* — los informes originales; históricos y todavía
  reveladores.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Common Lisp](common-lisp.md) · [Racket](racket.md) · [Clojure](clojure.md) ·
[Emacs Lisp](emacs-lisp.md) · [AutoLISP](autolisp.md)
