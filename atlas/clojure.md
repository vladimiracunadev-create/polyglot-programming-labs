# 🍀 Clojure — 2007

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Clojure es un **[Lisp](common-lisp.md) moderno sobre la JVM**, diseñado por una sola persona con una
tesis muy clara: **el problema del software no es la complejidad del dominio, sino la complejidad que
añadimos nosotros — y la mayor parte viene del estado mutable**. Todo el lenguaje es la consecuencia
de esa idea.

> **🎯 Por qué está en este programa**
>
> Clojure es un **primo de la familia JVM** ([Atlas](README.md#jvm)) y también de la **familia
> Lisp**: comparte máquina virtual con [Java](java.md) y modelo con
> [Common Lisp](common-lisp.md).
>
> Aporta al programa **la inmutabilidad como decisión total** (clase 102) y **las estructuras de datos
> persistentes** que la hacen viable; y aporta un modelo de concurrencia distinto de todos los del
> curso: **identidades separadas de valores**, con `atom` y con memoria transaccional
> ([clases 135 y 136](../classes/parte-8-como-funcionan-los-lenguajes/README.md)).

| | |
|---|---|
| **Año** | 2007; **1.0** en 2009; **1.12** actual |
| **Autoría** | **Rich Hickey**, tras dos años y medio de trabajo en solitario |
| **Familia** | Lisp sobre JVM; con influencia de Common Lisp, Scheme, Haskell y ML |
| **Paradigma** | **Funcional, con datos inmutables**; sin orientación a objetos |
| **Tipado** | **Dinámico y fuerte**; con `spec` y `malli` para contratos en ejecución |
| **Memoria** | La de la JVM |
| **Ejecución** | Bytecode JVM; también **ClojureScript** (a JS) y **ClojureCLR** |
| **Estado** | 🟢 **Nicho sólido y estable**; comunidad pequeña y muy influyente |

---

## 📜 Historia

**Rich Hickey** llevaba veinte años programando en C++, Java y .NET cuando, en **2005**, se tomó un
paréntesis de dos años y medio —financiado con sus ahorros— para diseñar el lenguaje que quería usar.

El resultado, publicado en **2007**, parte de un diagnóstico que expuso en su charla *Simple Made
Easy*, una de las más citadas de la historia de la disciplina:

> **Confundimos "simple" con "fácil".** Simple es *no entrelazado*; fácil es *familiar*. **El estado
> mutable compartido es lo contrario de simple**, aunque nos resulte facilísimo.

Y de ahí las decisiones:

- **Los datos son inmutables por defecto.** No hay que pedirlo: es lo que hay.
- **Las estructuras son persistentes**: modificar devuelve una versión nueva que **comparte** casi
  toda la anterior (clase 102), así que la inmutabilidad no cuesta memoria ni tiempo.
- **Estado e identidad se separan**: una identidad (`atom`, `ref`, `agent`) **apunta a un valor
  inmutable**, y cambiarla es cambiar a qué apunta, de forma controlada.
- **Sintaxis de Lisp**, con literales para mapas, vectores y conjuntos — lo que la hace mucho más
  legible que la de Common Lisp para datos.

**ClojureScript (2011)** llevó el lenguaje al navegador, y de ahí salió **Reagent/Re-frame**, cuya
arquitectura de estado influyó en el ecosistema React (clase 169).

Y su comunidad tiene una particularidad que merece nombrarse: **es de las más estables de esta lista**.
El lenguaje cambia poco y a propósito, y la compatibilidad hacia atrás se cuida — la misma disciplina
de [Go](go.md) y [Tcl](tcl.md) (clase 154).

## 🏭 Dónde vive hoy

- **Servicios de fondo** en empresas de datos, finanzas y salud: Nubank —el banco digital brasileño,
  uno de los mayores usuarios del mundo—, Walmart, Cisco, Apple.
- **Análisis y procesamiento de datos**, por la facilidad de componer transformaciones.
- **Front-end con ClojureScript**: Re-frame, y herramientas como Figwheel con recarga en caliente.
- **Datomic**: una base de datos —del mismo autor— cuyo modelo es **inmutable y con historia
  completa**: nunca se borra, se añaden hechos con su instante (clase 172).

## 🧠 Lo que enseña: valores, identidades y tiempo

Esta es la idea que hay que llevarse, y no la tiene ningún otro lenguaje del curso:

```clojure
(def cuenta (atom {:saldo 100}))       ; una IDENTIDAD que apunta a un VALOR inmutable

(swap! cuenta update :saldo + 50)       ; ← cambia a QUÉ VALOR apunta, atómicamente
@cuenta                                  ; {:saldo 150}
```

**El mapa `{:saldo 100}` nunca cambia.** Lo que cambia es a qué valor apunta `cuenta`, y ese cambio
es **atómico y sin cerrojos** — con comparación e intercambio por debajo.

**Y de ahí sale una propiedad enorme para la clase 136**: **no hay carreras de datos sobre los
valores**, porque los valores no se pueden modificar. Solo hay que coordinar las identidades, que son
pocas y están declaradas.

Y las estructuras persistentes son lo que lo hace asequible:

```clojure
(def a [1 2 3])
(def b (conj a 4))     ; b es nuevo... y COMPARTE la estructura interna de a
```

**No se copia el vector.** Por debajo hay un árbol con factor de ramificación 32, y añadir un elemento
crea unos pocos nodos nuevos. Es la técnica que la clase 102 describe y que también usan
[Scala](scala.md) y las bibliotecas inmutables de JavaScript.

Y hay una tercera idea, muy práctica, que Clojure defiende: **usar mapas en lugar de definir clases**.

```clojure
{:nombre "Ana" :edad 30}      ; ← no hace falta declarar un tipo Persona
```

**Los datos son datos**, y las funciones genéricas de la biblioteca —`get`, `assoc`, `update`,
`merge`, `select-keys`— funcionan sobre todos ellos. Es lo contrario del modelado con clases, y
`clojure.spec` añade la validación **donde hace falta** en lugar de en todas partes.

## 🔄 Lo que se ha modernizado

- **`clojure.spec`** y **malli**: contratos y validación de datos **en ejecución**, con generación de
  casos de prueba a partir de la especificación (clases 118 y 140).
- **Herramientas oficiales**: `deps.edn` y la CLI de Clojure, con dependencias declarativas y
  fichero de bloqueo (clase 143).
- **`core.async`**: canales y procesos ligeros al estilo de [Go](go.md) (clase 134), implementados con
  macros que transforman el código en una máquina de estados.
- **ClojureScript con compilación avanzada** (Closure Compiler) y **shadow-cljs**.
- **Y `babashka`**: un intérprete de Clojure **con arranque instantáneo** compilado con GraalVM, para
  guiones de línea de comandos — la respuesta al problema de arranque de la JVM (clase 167).

## ⚙️ Cómo se ejecuta hoy

```bash
clojure -M main.clj < entrada.txt      # el comando de la clase 041
bb main.clj                             # babashka: arranque en milisegundos

clj -X:test                              # pruebas
clj-kondo --lint src                      # análisis estático, muy bueno (clase 146)
```

## 🧪 El programa de la clase 041 en Clojure

```clojure
(require '[clojure.string :as str])

(let [[precio cantidad descuento] (map read-string (str/split (read-line) #" "))
      total (* precio cantidad (- 1 descuento))]
  (println (format "Total: %.2f" (double total))))
```

**Lo que hay que ver.**

- **La notación prefija** —`(* precio cantidad ...)`— es la de [Lisp](common-lisp.md): **el operador
  va primero y admite cualquier número de argumentos**. Es lo que permite que el código sea una
  estructura de datos (clase 123).
- **`let` con desestructuración `[[a b c] ...]`** liga tres nombres de una vez, y **no son variables:
  son enlaces que no se reasignan**. En todo el programa **no hay una sola mutación** (clase 102).
- **`(double total)` no sobra**: `read-string` puede devolver un entero o una **fracción exacta**
  —Clojure tiene racionales, como [Smalltalk](smalltalk.md) (clase 072)— y `%.2f` necesita un doble.
  Ese detalle es un buen recordatorio de que **el modelo numérico varía mucho entre lenguajes**.
- **Y compárese con [Java](java.md), en la misma máquina virtual**: la diferencia no es de sintaxis,
  es de paradigma. Clojure no crea ningún objeto ni declara ninguna clase.

## 📚 Fuentes y bibliografía

- [clojure.org](https://clojure.org/guides/getting_started) — guías oficiales y la referencia; el
  apartado sobre **estado e identidad** es lectura obligatoria para la clase 136.
- **Rich Hickey**, charlas *Simple Made Easy*, *The Value of Values* y *Are We There Yet?* — de lo
  mejor que se ha dicho sobre diseño de software, y aplicable a cualquier lenguaje.
- **Daniel Higginbotham**, *Clojure for the Brave and True* — libre en línea; la mejor introducción.
- **Alex Miller, Stuart Halloway, Aaron Bedra**, *Programming Clojure*, 3.ª ed., Pragmatic.
- **Chas Emerick et al.**, *Clojure Programming*, O'Reilly — completo, con el modelo de concurrencia
  bien explicado.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Common Lisp](common-lisp.md) · [Scheme](scheme.md) · [Java](java.md) ·
[Scala](scala.md) · [Elixir](elixir.md)
