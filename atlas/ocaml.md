# 🐫 OCaml — 1996

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

OCaml es la rama **pragmática** de la familia ML: funcional como [Haskell](haskell.md), pero
**evaluación ansiosa**, con mutación cuando hace falta y con un compilador rapidísimo. Es el lenguaje
en el que están escritos varios de los verificadores formales más serios del mundo — y el que inspiró
directamente a [Rust](rust.md) y a [F#](fsharp.md).

> **🎯 Por qué está en este programa**
>
> OCaml es un **primo de la familia funcional tipada (ML)** ([Atlas](README.md#funcional-tipada)),
> que no tiene representante en el núcleo.
>
> Aporta al programa **el sistema de módulos más potente de esta lista** —functores: módulos que
> reciben módulos (clase 149)— y la demostración de que **un lenguaje funcional puede ser rápido y
> pragmático** sin renunciar a la seguridad de tipos.

| | |
|---|---|
| **Año** | 1996 (Objective Caml); Caml es de 1985; **OCaml 5** con efectos (2022) |
| **Autoría** | **INRIA** (Francia): Xavier Leroy, Damien Doligez, Didier Rémy y otros |
| **Familia** | Funcional tipada (ML); descendiente de ML (Milner, 1973) y de Caml |
| **Paradigma** | **Funcional, imperativo y orientado a objetos** — las tres cosas de verdad |
| **Tipado** | **Estático con inferencia total**; tipos algebraicos y módulos de primera clase |
| **Memoria** | Recolección de basura generacional, muy rápida en asignación |
| **Ejecución** | **Compilado a nativo** o a bytecode; compilación muy veloz |
| **Estado** | 🟢 **Vivo y de nicho**: verificación formal, finanzas y herramientas |

---

## 📜 Historia

**ML** —*Meta Language*— lo creó **Robin Milner** en Edimburgo en **1973**, no como lenguaje de
programación sino como **el lenguaje para escribir tácticas de un demostrador de teoremas**. De ahí
salieron dos ideas que hoy están en todas partes:

- **La inferencia de tipos Hindley-Milner**: tipado estático completo **sin escribir tipos**.
- **Los tipos algebraicos con emparejamiento de patrones** y comprobación de exhaustividad.

Milner recibió el Premio Turing en 1991, en buena parte por esto.

**INRIA** desarrolló **Caml** (1985) y después **Objective Caml (1996)**, que añadió objetos y un
sistema de módulos muy elaborado. En **2011** pasó a llamarse simplemente **OCaml**.

Y su influencia es directa y reconocida:

- **[Rust](rust.md)**: el primer compilador de Rust estaba escrito en OCaml, y su sistema de tipos
  —`Option`, `Result`, `match`, los rasgos— viene de aquí.
- **[F#](fsharp.md)** es esencialmente OCaml sobre .NET.
- **Y Flow y Hack**, las herramientas de tipos de Meta para JavaScript y PHP, están escritas en OCaml.

**OCaml 5 (2022)** fue un cambio profundo: **paralelismo real con multinúcleo** —hasta entonces había
un bloqueo global— y **manejadores de efectos**, una idea de investigación que permite implementar
corrutinas, generadores y `async` **como bibliotecas** en lugar de como características del lenguaje
(clase 134).

## 🏭 Dónde vive hoy

- **Verificación formal**: **Coq/Rocq** —el asistente de demostración con el que se verificó el
  compilador **CompCert**— está escrito en OCaml. También **Frama-C** y varias herramientas de
  análisis usadas en aviación (clase 164).
- **Finanzas**: **Jane Street** es el caso más conocido: cientos de personas escribiendo OCaml para
  negociación algorítmica, con su propia biblioteca estándar publicada.
- **Herramientas de desarrollo**: Flow, Hack, Infer (Meta), Semgrep, Unison.
- **Blockchain**: Tezos está implementado en OCaml.
- **Y compiladores en general**, que es su terreno natural.

## 🧠 Lo que enseña: módulos y functores

Es su aportación más distintiva y la que ningún otro lenguaje de esta lista tiene igual (clase 149):

```ocaml
module type ORDENABLE = sig
  type t
  val compare : t -> t -> int
end

module Conjunto (E : ORDENABLE) = struct     (* ← un MÓDULO que recibe un MÓDULO *)
  type elemento = E.t
  let vacio = []
  let rec insertar x = function
    | [] -> [x]
    | y :: r when E.compare x y < 0 -> x :: y :: r
    | y :: r -> y :: insertar x r
end

module ConjuntoEnteros = Conjunto (Int)      (* ← se instancia con otro módulo *)
```

**Un *functor* es una función de módulos a módulos**, comprobada por el sistema de tipos. Es
**parametrización a nivel de arquitectura**, no de clase — la idea que la clase 166 pide y que en otros
lenguajes se aproxima con inyección de dependencias, con genéricos o con interfaces.

Y merece la comparación con [Ada](ada.md), que tiene lo más parecido: **los genéricos de Ada con
parámetros formales de subprograma y de paquete** (clase 151) son la misma familia de idea, con otra
sintaxis.

**Y la segunda cosa que OCaml hace muy bien es ser pragmático:**

```ocaml
let contador = ref 0        (* mutable, EXPLÍCITAMENTE *)
contador := !contador + 1
let arreglo = [| 1; 2; 3 |]  (* arreglos mutables de verdad *)
```

**La mutación existe y se ve.** A diferencia de [Haskell](haskell.md), no hay que envolverla en nada:
está ahí, marcada con `ref` y `:=`, y se usa cuando conviene. Eso hace que **el rendimiento sea
predecible** —evaluación ansiosa, sin cadenas de cálculos pendientes— y es la razón de que Jane Street
pueda escribir sistemas de latencia baja en él.

## 🔄 Lo que se ha modernizado

- **OCaml 5**: **multinúcleo real** con dominios, y **manejadores de efectos** — con los que
  `async`/`await` deja de ser sintaxis y pasa a ser una biblioteca (clase 134).
- **Dune** como sistema de construcción, rápido y declarativo, y **opam** como gestor de paquetes
  con fichero de bloqueo (clase 143).
- **js_of_ocaml** y **Melange**: compilar a JavaScript (clase 162).
- **Bibliotecas estándar alternativas**: `Base` y `Core` de Jane Street, hoy muy usadas.
- **Y `ppx`**: metaprogramación mediante transformación del árbol sintáctico, con la que se generan
  serializadores y comparadores automáticamente (clases 122 y 159).

## ⚙️ Cómo se ejecuta hoy

```bash
ocaml main.ml < entrada.txt              # intérprete
ocamlfind ocamlopt -package str main.ml   # compilar a nativo

dune build && dune test                    # lo habitual (clases 143 y 147)
opam install <paquete>
```

## 🧪 El programa de la clase 041 en OCaml

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```ocaml
let () =
  let linea = read_line () in
  match String.split_on_char ' ' linea |> List.map float_of_string with
  | [precio; cantidad; descuento] ->
      Printf.printf "Total: %.2f\n" (precio *. cantidad *. (1. -. descuento))
  | _ -> prerr_endline "Se esperaban tres valores"; exit 1
```

**Lo que hay que ver.**

- **`*.` y `-.` con punto** son los operadores de **coma flotante**: en OCaml, `*` es solo para
  enteros. **No hay sobrecarga de operadores**, así que cada tipo tiene los suyos. Es incómodo y
  elimina toda ambigüedad — la misma disciplina de [Go](go.md) y [Rust](rust.md), llevada más lejos
  (clase 100).
- **El `match` trata los dos casos**: la lista con tres elementos y **todo lo demás**. El compilador
  **avisaría si faltara un caso**, y por eso el programa maneja el error de entrada sin escribir un
  `if`.
- **`|>` es la canalización**, igual que en [F#](fsharp.md) — de hecho, F# la heredó de aquí.
- **`let () = ...`** es el punto de entrada: se liga el resultado al patrón vacío, que es la forma
  idiomática de decir "esto se ejecuta por sus efectos".
- **Y no hay ni una anotación de tipo**, y el programa está completamente tipado: eso es
  Hindley-Milner.

## 📚 Fuentes y bibliografía

- [Real World OCaml](https://dev.realworldocaml.org/) — **Minsky, Madhavapeddy y Hickey**; libre en
  línea, escrito desde Jane Street; el libro de referencia.
- [ocaml.org/docs](https://ocaml.org/docs) — tutoriales oficiales y el manual del lenguaje.
- **Xavier Leroy et al.**, *The OCaml system: documentation and user's manual* — la referencia
  formal; el capítulo de módulos merece la pena.
- **Jason Hickey**, *Introduction to Objective Caml* — libre; muy bueno para el sistema de módulos.
- [CompCert](https://compcert.org/) — el compilador de C **verificado formalmente**, escrito en Coq y
  OCaml; el mejor argumento existente sobre lo que la verificación puede lograr (clase 164).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Haskell](haskell.md) · [F#](fsharp.md) · [Rust](rust.md) · [Scala](scala.md) ·
[Ada](ada.md)
