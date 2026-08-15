# 🌳 Elm — 2012

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Elm hace una promesa que ningún otro lenguaje de esta lista se atreve a hacer: **si compila, no lanza
excepciones en ejecución**. Y la cumple. Es un lenguaje pequeño, deliberadamente limitado, cuya
influencia real está mucho más allá de su cuota de uso: **Redux, la arquitectura de estado que domina
el front-end, salió de aquí**.

> **🎯 Por qué está en este programa**
>
> Elm es un **primo de la familia JavaScript / web** ([Atlas](README.md#javascript-web)) y también de
> la **funcional tipada** — está en el cruce de las dos.
>
> Aporta al programa la demostración más contundente de la tesis que atraviesa el curso (clases 118,
> 146 y 164): **lo que un lenguaje prohíbe es lo que sus herramientas pueden prometer**. Elm prohíbe
> los efectos secundarios, la nulidad, las excepciones y la interoperabilidad directa — y a cambio
> garantiza que no habrá errores en ejecución.

| | |
|---|---|
| **Año** | 2012; **0.19** (2018) es la versión estable actual — sin 1.0 |
| **Autoría** | **Evan Czaplicki**, como tesis de fin de grado en Harvard |
| **Familia** | Funcional tipada (ML) aplicada a la web |
| **Paradigma** | **Funcional puro**: sin efectos secundarios en el lenguaje |
| **Tipado** | **Estático, inferido, sin `null` y sin excepciones**; tipos algebraicos |
| **Memoria** | La de JavaScript: recolección automática |
| **Ejecución** | **Compila a JavaScript** |
| **Estado** | 🟡 **Estable y de nicho**: poco movimiento, y lo que hay funciona |

---

## 📜 Historia

**Evan Czaplicki** presentó Elm en **2012** como tesis de grado. La pregunta de partida era buena:
**¿por qué las interfaces web son tan propensas a fallar en ejecución?** Y la respuesta que propuso
fue radical: **quitar del lenguaje todo lo que puede fallar**.

- **No hay `null` ni `undefined`**: lo que puede faltar se declara con `Maybe`.
- **No hay excepciones**: lo que puede fallar devuelve `Result`.
- **No hay efectos secundarios en las funciones**: los efectos los ejecuta el tiempo de ejecución.
- **No hay interoperabilidad directa con JavaScript**: se habla con él por **puertos**, mensajes con
  tipo comprobado.

De esa última restricción sale la garantía: **si el código JavaScript no puede entrar en el mundo de
Elm sin pasar por un puerto tipado, no puede romperlo**.

Y su influencia fue mucho mayor que su uso: **la arquitectura de Elm** —modelo, mensaje,
actualización, vista— **inspiró directamente a Redux** (Dan Abramov lo ha reconocido), y con Redux
llegó a millones de aplicaciones React. Es la idea de la clase 169: **interfaz = f(estado)**.

Su evolución es lenta y deliberada, con versiones espaciadas años, lo que ha generado tanto elogios
por la estabilidad como críticas por la falta de movimiento.

## 🏭 Dónde vive hoy

- **Aplicaciones web con mucha lógica de interfaz** en empresas que lo adoptaron: NoRedInk, Rakuten,
  Vendr, y varias del sector financiero.
- **Formularios y flujos complejos**, donde el coste de un error en producción justifica la
  restricción.
- **Enseñanza de programación funcional**, por la calidad de sus mensajes de error.
- **Y como influencia**, que es donde más presencia tiene: Redux, Vuex, Pinia, The Elm Architecture en
  Rust (`iced`) y en otros ecosistemas.

## 🧠 Lo que enseña: la garantía sale de la renuncia

**El mensaje de error como característica de producto.** Elm es famoso por esto:

```text
-- TYPE MISMATCH ------------------------------------------- src/Main.elm

The 1st argument to `toFloat` is not what I expect:

23|     toFloat modelo.nombre
                ^^^^^^^^^^^^^
This `nombre` value is a: String
But `toFloat` needs the 1st argument to be: Int

Hint: Want to convert a String into an Int? Use String.toInt!
```

**Ese nivel de mensaje elevó el listón de toda la industria**: Rust, TypeScript y varios compiladores
mejoraron sus errores explícitamente citando a Elm. Es un caso claro de la clase 137 — **el
diagnóstico es parte del lenguaje, no un detalle de implementación**.

**Y la arquitectura de Elm**, que es lo más transferible:

```elm
type Msg = Incrementar | Decrementar

update : Msg -> Model -> Model          -- ← una FUNCIÓN PURA: mensaje + estado → estado nuevo
update msg model =
    case msg of
        Incrementar -> { model | contador = model.contador + 1 }
        Decrementar -> { model | contador = model.contador - 1 }

view : Model -> Html Msg                 -- ← la vista es una FUNCIÓN del estado
```

**Y las propiedades que eso da son las de la clase 169**: el estado está en un sitio, los cambios son
explícitos y con nombre, la vista se deriva del estado, y **todo es probable sin navegador** porque
`update` es una función pura (clase 139).

> **Y el coste hay que decirlo, porque es alto** (clase 164): **no se puede llamar a una biblioteca de
> JavaScript directamente**. Todo pasa por puertos, con serialización de por medio. En un ecosistema
> donde la solución a cualquier problema es un paquete de npm, esa restricción es la barrera de
> adopción — y es, a la vez, exactamente lo que hace posible la garantía.

## 🔄 Estado actual

- **0.19 desde 2018**, con un ritmo de publicación muy lento; la comunidad mantiene el ecosistema.
- **`elm-review`**: análisis estático con reglas propias, en la línea de la clase 146.
- **`elm-test`** y **`elm-program-test`**: pruebas de la lógica sin navegador.
- **Y la discusión abierta y honesta** sobre si la estabilidad extrema es virtud o abandono — que es
  un debate útil para la clase 164.

## ⚙️ Cómo se ejecuta hoy

```bash
elm make src/Main.elm --output=main.js       # compilar a JavaScript
elm repl                                      # explorar el lenguaje
elm reactor                                    # servidor de desarrollo

elm-test && elm-review                         # pruebas y análisis
```

## 🧪 El programa de la clase 041 en Elm

Elm **no tiene entrada estándar**: se ejecuta en el navegador, y la entrada llega por puertos o por
eventos. Como en [SQL](sql.md) y en [JCL](jcl.md), esto es un **contrato adaptado** (clase 040), y
declararlo es más honesto que fingirlo.

```elm
module Venta exposing (total)

-- La lógica pura, que es lo que Elm quiere que sea el 95 % del programa:
total : Float -> Float -> Float -> String
total precio cantidad descuento =
    let
        resultado =
            precio * cantidad * (1 - descuento)
    in
    "Total: " ++ formatear2 resultado


-- Y el tipo de la entrada declara que PUEDE FALLAR:
parsear : String -> Result String Float
parsear texto =
    case String.toFloat texto of
        Just n -> Ok n
        Nothing -> Err ("No es un número: " ++ texto)
```

**Lo que hay que ver.**

- **`String.toFloat` devuelve `Maybe Float`, no un número.** Es la diferencia esencial con
  [JavaScript](javascript.md), donde `Number("abc")` devuelve `NaN` y sigue adelante: **aquí el fallo
  está en el tipo y el compilador obliga a tratarlo** (clase 116).
- **La firma `Float -> Float -> Float -> String` está escrita a mano** aunque Elm la infiera. Es la
  convención del ecosistema, y funciona como documentación comprobada (clase 154).
- **No hay `return`, ni sentencias, ni mutación**: `let ... in` nombra un valor intermedio, y la
  función **es** una expresión.
- **Y `Result String Float`** es un tipo algebraico: **o hay un valor, o hay un error con mensaje** —
  nunca las dos cosas ni ninguna. Es la misma idea que `Result` de [Rust](rust.md) y `Either` de
  [Haskell](haskell.md).

## 📚 Fuentes y bibliografía

- [Guía oficial de Elm](https://guide.elm-lang.org/) — corta, completa y muy bien escrita; se lee en
  una tarde.
- [Elm Packages](https://package.elm-lang.org/) — con **versionado semántico impuesto por
  herramienta**: `elm publish` **calcula** si el cambio es mayor o menor analizando la API. Es la
  clase 143 automatizada de verdad, y merece conocerse aunque no se use Elm.
- **Richard Feldman**, *Elm in Action*, Manning — el libro de referencia.
- [elm-radio](https://elm-radio.com/) — pódcast con discusiones de diseño aplicables a cualquier
  lenguaje.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Haskell](haskell.md) · [OCaml](ocaml.md) · [F#](fsharp.md) ·
[TypeScript](typescript.md) · [JavaScript](javascript.md)
