# 🎾 Racket — 1995

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Racket empezó como un [Scheme](scheme.md) para enseñar y acabó convirtiéndose en algo que ningún otro
lenguaje de esta lista es: **una plataforma para construir lenguajes**. Su lema —*"un lenguaje de
programación programable"*— se toma literalmente: en Racket, **crear un lenguaje nuevo con su propia
sintaxis es una operación normal**.

> **🎯 Por qué está en este programa**
>
> Racket es un **primo de la familia Lisp** ([Atlas](README.md#lisp)).
>
> Aporta al programa la forma más extrema de **metaprogramación**
> ([clase 122](../classes/parte-8-como-funcionan-los-lenguajes/123-del-codigo-a-la-ejecucion-fases-de-compilacion/README.md)) y de
> **lenguaje de dominio** (clase 163): no ya macros que añaden construcciones, sino **lenguajes
> completos con otra sintaxis y otra semántica**, definidos como bibliotecas. Y aporta **los contratos
> en ejecución** (clase 118) en un lenguaje dinámico.

| | |
|---|---|
| **Año** | 1995 (como PLT Scheme); **Racket** desde 2010; **Racket 8** actual |
| **Autoría** | **Matthias Felleisen** y el grupo PLT (Northeastern, Utah, Brown, otras) |
| **Familia** | Lisp; descendiente directo de [Scheme](scheme.md) |
| **Paradigma** | Multiparadigma; funcional por defecto, con OO, lógico y lo que se defina |
| **Tipado** | **Dinámico**, con **contratos** y con **Typed Racket** para tipado estático gradual |
| **Memoria** | Recolección de basura |
| **Ejecución** | Compilado a bytecode sobre **Chez Scheme** desde Racket 8 |
| **Estado** | 🟢 **Vivo**: enseñanza, investigación en lenguajes y proyectos propios |

---

## 📜 Historia

**PLT Scheme** nació en **1995** con un objetivo docente: **DrScheme** —después DrRacket— era un
entorno diseñado para principiantes, con **niveles de lenguaje** que iban activando características
según avanzaba el curso, y con mensajes de error pensados para enseñar.

De ahí salió **How to Design Programs (HtDP)**, un método de enseñanza de programación basado en
**recetas de diseño** —del tipo de datos se deriva la forma de la función— que se usa en decenas de
universidades y que es, en sí mismo, una aportación pedagógica seria.

Pero lo que convirtió a Racket en lo que es fue una decisión posterior: **hacer del sistema de macros
una plataforma para definir lenguajes enteros**. En **2010** el cambio de nombre marcó ese giro, y hoy
el primer renglón de un fichero Racket **dice en qué lenguaje está escrito**:

```racket
#lang racket          ; el lenguaje por defecto
#lang typed/racket     ; con tipos estáticos
#lang scribble/base     ; ← un lenguaje de DOCUMENTOS
#lang datalog            ; ← Datalog, dentro de Racket
#lang mi-lenguaje         ; ← el tuyo
```

**Y todos interoperan**, porque todos compilan al mismo núcleo.

## 🏭 Dónde vive hoy

- **Enseñanza**: HtDP y *Bootstrap* —un currículo que enseña álgebra programando— en institutos y
  universidades.
- **Investigación en lenguajes de programación**: es la plataforma de referencia para prototipar
  lenguajes y sistemas de tipos.
- **Scribble**: la documentación de Racket está escrita en un lenguaje hecho en Racket para escribir
  documentación (clase 154).
- **Herramientas y aplicaciones propias** de su comunidad, y algunos usos industriales de nicho.

## 🧠 Lo que enseña: definir lenguajes como bibliotecas

Este es el concepto, y no lo tiene ningún otro lenguaje de este Atlas con esta profundidad:

```racket
#lang racket

(provide (rename-out [mi-app #%app])    ; ← redefinir cómo funciona LA APLICACIÓN
         (except-out (all-from-out racket) #%app))
```

**Se puede redefinir qué significa llamar a una función, qué significa un literal numérico, o cómo se
lee el texto del fichero.** Un `#lang` es un módulo que exporta el lector y las macros del lenguaje.

Y de ahí salen cosas como **`#lang scribble`** —donde el texto plano es lo normal y el código va
marcado, al revés que en un lenguaje de programación— o **`#lang datalog`**, que es
[Datalog](datalog.md) de verdad, con su semántica lógica, dentro del mismo sistema.

**Es la clase 163 llevada al límite**: en lugar de incrustar un lenguaje ajeno, **el lenguaje
anfitrión permite fabricar el incrustado**.

Y la segunda aportación son **los contratos** (clase 118), que Racket implementa mejor que ningún otro
lenguaje dinámico:

```racket
(provide (contract-out
          [dividir (-> number? (and/c number? (not/c zero?)) number?)]))
```

**El contrato se comprueba en la frontera del módulo, en ejecución** — y cuando falla, **el mensaje
dice quién tiene la culpa**: si el que llamó pasó un argumento malo, o si la función devolvió algo que
no debía.

**Esa atribución de culpa es la aportación técnica**: en un lenguaje dinámico, saber **de qué lado de
la frontera está el error** es la mitad del diagnóstico (clase 137).

## 🔄 Lo que se ha modernizado

- **Racket CS (8.0)**: el tiempo de ejecución reescrito sobre **Chez Scheme**, con mejoras grandes de
  rendimiento.
- **Typed Racket**: tipado estático gradual que **convive con módulos sin tipar**, insertando
  contratos en la frontera — una implementación muy estudiada del tipado gradual (clase 146).
- **Rhombus**: un lenguaje nuevo sobre la plataforma **con sintaxis de expresiones en lugar de
  paréntesis**, para atraer a quien rechaza la notación Lisp. Es la demostración definitiva de la
  tesis: **cambiar la sintaxis del lenguaje es un proyecto dentro del propio lenguaje**.
- **`raco`** como herramienta única: construir, empaquetar, documentar, probar y publicar.

## ⚙️ Cómo se ejecuta hoy

```bash
racket main.rkt < entrada.txt        # ejecutar
raco test main.rkt                    # pruebas (clase 139)
raco exe main.rkt                      # ejecutable autocontenido (clase 174)
raco pkg install <paquete>
```

## 🧪 El programa de la clase 041 en Racket

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```racket
#lang racket

(define campos (string-split (read-line)))
(define nums (map string->number campos))
(define total (* (first nums) (second nums) (- 1 (third nums))))

(printf "Total: ~a\n" (real->decimal-string total 2))
```

**Lo que hay que ver.**

- **`#lang racket` en la primera línea** es la característica del lenguaje: **declara en qué lenguaje
  está escrito el fichero**. Cambiarlo por `#lang typed/racket` haría el mismo programa estáticamente
  tipado.
- **`first`, `second`, `third`** en lugar de `car`, `cadr` y `caddr` de [Scheme](scheme.md): Racket
  eligió nombres legibles, coherente con su origen docente.
- **`real->decimal-string`** en lugar de una directiva de formato: es más explícito sobre lo que
  hace, otra vez la vocación pedagógica.
- **`(* a b (- 1 c))` con notación prefija** y aridad variable, como todo Lisp.
- **Y no hay mutación**: `define` liga nombres, no asigna variables (clase 102).

## 📚 Fuentes y bibliografía

- [docs.racket-lang.org](https://docs.racket-lang.org/) — la documentación, escrita con Scribble; el
  *Racket Guide* y la *Reference* son excelentes.
- [How to Design Programs](https://htdp.org/) — **Felleisen et al.**, libre en línea; **es un método
  de diseño de programas**, no un manual de sintaxis, y merece leerse aunque no se use Racket
  (clase 166).
- [Beautiful Racket](https://beautifulracket.com/) — **Matthew Butterick**; cómo crear lenguajes con
  `#lang`, explicado paso a paso. Material directo de las clases 122 y 163.
- **Matthias Felleisen et al.**, *The Racket Manifesto* — la tesis de la programación orientada a
  lenguajes.
- [Rhombus](https://racket-lang.org/rhombus/) — el proyecto de sintaxis alternativa.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Scheme](scheme.md) · [Common Lisp](common-lisp.md) · [Clojure](clojure.md) ·
[Datalog](datalog.md)
