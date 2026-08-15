# λ Haskell — 1990

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Haskell es el lenguaje del que la industria lleva treinta años copiando ideas sin adoptarlo. Las
funciones de primera clase, la inferencia de tipos, las lambdas, `Option`/`Maybe`, las colecciones
inmutables, los tipos algebraicos y `async` **estaban aquí antes de estar en ningún lenguaje
mayoritario** — y su lema no oficial lo resume: *"evitar el éxito a toda costa"*.

> **🎯 Por qué está en este programa**
>
> Haskell es el representante de la **familia funcional tipada (ML)** ([Atlas](README.md#funcional-tipada)),
> que **no tiene representante en el núcleo** — su influencia llega al curso a través de
> [Rust](rust.md), [Scala](scala.md), [F#](fsharp.md) y [Elm](elm.md).
>
> Aporta al programa dos conceptos que ningún otro lenguaje del Atlas enseña igual: **la evaluación
> perezosa por defecto**
> ([clase 115](../classes/parte-7-paradigmas-de-programacion/115-funciones-de-orden-superior/README.md))
> y **la pureza con efectos en el sistema de tipos**
> ([clase 118](../classes/parte-7-paradigmas-de-programacion/118-programacion-declarativa/README.md)).

| | |
|---|---|
| **Año** | 1990; **Haskell 98** el estándar de referencia; **GHC 2021/2024** los conjuntos actuales |
| **Autoría** | **Comité académico** (Hudak, Peyton Jones, Wadler, Hughes y otros) |
| **Familia** | Funcional tipada (ML); nombrado por **Haskell Curry**, lógico |
| **Paradigma** | **Funcional puro** |
| **Tipado** | **Estático, inferido (Hindley-Milner extendido)**, con clases de tipos |
| **Memoria** | Recolección de basura generacional, muy afinada para asignación rápida |
| **Ejecución** | Compilado a nativo con **GHC**, vía su propia representación intermedia |
| **Estado** | 🟢 **Vivo, minoritario y muy influyente** |

---

## 📜 Historia

A finales de los ochenta había **más de una docena de lenguajes funcionales perezosos**, cada uno de
un grupo de investigación, y ninguno con masa crítica. En **1987**, en una conferencia en Portland, se
formó un comité para hacer **uno solo**, abierto y estándar.

El resultado, en **1990**, fue **Haskell** — con el nombre del lógico **Haskell Curry**, cuyo trabajo
sobre lógica combinatoria fundamenta el cálculo lambda tipado.

El problema que tuvieron que resolver era serio: **en un lenguaje puro y perezoso, ¿cómo se hace
entrada y salida?** Si una función no puede tener efectos y el orden de evaluación no está
determinado, imprimir en pantalla es un problema conceptual, no técnico.

La solución, hacia **1992**, fue **la mónada `IO`** —trabajo de Eugenio Moggi y Philip Wadler—, y es
la idea más influyente y peor explicada de la informática moderna: **los efectos se representan como
valores de un tipo, y se componen**.

**GHC** —el compilador de Glasgow— se convirtió en la implementación de referencia y en un laboratorio
de investigación de tipos, del que han salido las extensiones que después llegaron a otros lenguajes:
**GADT, familias de tipos, tipos de rango superior, `deriving` automático, `Applicative`**.

Y el lema *"avoid success at all costs"* —una broma de Simon Peyton Jones con doble lectura— refleja
una postura real: **priorizar la corrección del diseño sobre la adopción**, para poder seguir
cambiando cosas.

## 🏭 Dónde vive hoy

- **Finanzas**: Standard Chartered tiene un equipo grande escribiendo Haskell para modelos de
  derivados; Barclays y otros lo han usado.
- **Verificación y compiladores**: **Agda**, **Idris**, **Elm**, **PureScript** y buena parte de las
  herramientas de análisis formal están escritas en Haskell.
- **Criptomonedas**: Cardano y varios proyectos con requisitos de corrección alta.
- **Herramientas**: **Pandoc** —el conversor universal de documentos, que probablemente usas sin
  saberlo—, ShellCheck, Hasura, Semantic (GitHub).
- **Y la academia**, donde sigue siendo la lengua franca de la investigación en lenguajes.

## 🧠 Lo que enseña: pereza y efectos en el tipo

**Uno, la evaluación perezosa por defecto** (clase 115):

```haskell
naturales = [1..]                    -- una lista INFINITA
primeros10 = take 10 naturales        -- [1,2,3,4,5,6,7,8,9,10]

fibs = 0 : 1 : zipWith (+) fibs (tail fibs)   -- ← se define en términos de sí misma
```

**Nada se calcula hasta que se necesita**, así que una estructura infinita es un valor normal. Eso
permite **separar la generación del consumo** —el productor no sabe cuánto se va a consumir— y es la
misma idea que los generadores de [Python](python.md), los iteradores perezosos de
[Rust](rust.md) y los rangos de [D](d.md), **con la diferencia de que aquí es la norma y no la
excepción**.

**Y el coste hay que decirlo**: la pereza hace **muy difícil razonar sobre el consumo de memoria**.
Un acumulador que no se fuerza construye una cadena de cálculos pendientes que puede agotar la
memoria — el problema clásico de Haskell, que se resuelve con anotaciones de rigor (`seq`, `!`).

**Dos, los efectos en el tipo:**

```haskell
longitud :: String -> Int              -- pura: mismo argumento, mismo resultado, SIEMPRE
leerFichero :: FilePath -> IO String    -- ← el IO en el tipo DECLARA que hay efectos
```

**El tipo dice si una función toca el mundo.** No es una convención ni una anotación opcional: **una
función pura no puede llamar a una con efectos** sin que aparezca en su firma.

Y eso da lo que la clase 118 busca: **al leer una firma se sabe qué puede hacer la función**, y el
compilador lo garantiza. Es la versión más fuerte de la idea que [Fortran](fortran.md) tiene con
`pure` y [D](d.md) con `@nogc`.

**Y tres, las clases de tipos**, que son el sistema de polimorfismo más limpio de esta lista:

```haskell
class Mostrable a where
    mostrar :: a -> String

instance Mostrable Bool where
    mostrar True = "sí"
    mostrar False = "no"
```

**Se añade un comportamiento a un tipo existente sin tocarlo y sin herencia** — lo que
[Rust](rust.md) llama rasgos, [Scala](scala.md) implementa con implícitos y [Go](go.md) aproxima con
interfaces estructurales (clase 112).

## 🔄 Lo que se ha modernizado

- **GHC2021/GHC2024**: conjuntos de extensiones activados por defecto, que acaban con la lista de
  `{-# LANGUAGE ... #-}` al principio de cada fichero.
- **Tipos dependientes por partes**: `DataKinds`, `TypeFamilies`, `LinearTypes` — el camino hacia lo
  que [Idris](haskell.md) y Agda tienen completo.
- **Herramientas por fin buenas**: **GHCup**, **Stack**, **Cabal** con fichero de bloqueo
  (clase 143), y **HLS**, el servidor de lenguaje, que resolvió la peor queja histórica.
- **`Text` y `ByteString`** en lugar de `String` como lista de caracteres, que era una fuente clásica
  de mal rendimiento (clase 093).
- **Y el ecosistema de efectos**: `mtl`, `effectful`, `polysemy` — formas de componer efectos que van
  más allá de las mónadas anidadas.

## ⚙️ Cómo se ejecuta hoy

```bash
runghc main.hs < entrada.txt          # ejecutar directamente
ghc -O2 main.hs -o venta               # compilar optimizado
ghci                                    # consola interactiva

cabal test && hlint src                 # pruebas y análisis (clases 139 y 146)
```

## 🧪 El programa de la clase 041 en Haskell

Haskell **no está en el `primos.md` de la clase 041**, así que esta versión se escribe aquí y **no
está verificada en CI** — como el resto de los primos de lectura (clase 040).

```haskell
import Text.Printf (printf)

main :: IO ()
main = do
    linea <- getLine
    let [precio, cantidad, descuento] = map read (words linea) :: [Double]
    printf "Total: %.2f\n" (precio * cantidad * (1 - descuento))
```

**Lo que hay que ver.**

- **`main :: IO ()`** declara en el tipo que este programa **hace entrada y salida**. Es la única
  parte impura, y está marcada.
- **`<-` no es una asignación**: extrae el valor de dentro de `IO`. Y `let` sí liga un nombre a un
  valor puro. **Esa distinción es todo el modelo de efectos** en una línea.
- **`map read (words linea)`** es puro: parte y convierte sin tocar nada. **Y `:: [Double]` es
  necesario** porque `read` es polimórfico —podría leer enteros— y aquí hay que decidir; es un caso
  donde la inferencia no basta.
- **La desestructuración `[a, b, c]`** es emparejamiento de patrones sobre una lista, como en
  [Scala](scala.md): si hubiera cuatro campos, fallaría en ejecución.
- **Y `printf` está tipado**: el compilador comprueba que el `%.2f` recibe un `Double`, mediante una
  clase de tipos variádica — un truco de tipos que casi ningún lenguaje puede hacer (clase 142).

## 📚 Fuentes y bibliografía

- [Learn You a Haskell for Great Good!](http://learnyouahaskell.com/) — libre en línea; la
  introducción más amable que existe, aunque algo anticuada.
- [Haskell from First Principles](https://haskellbook.com/) — **Allen y Moronuki**; largo, exigente y
  probablemente el mejor camino para aprenderlo de verdad.
- [Documentación de GHC](https://downloads.haskell.org/ghc/latest/docs/users_guide/) — imprescindible
  para las extensiones de tipos.
- **Simon Peyton Jones**, charlas y artículos — sobre todo *A History of Haskell: Being Lazy with
  Class* (HOPL III), que cuenta el diseño desde dentro.
- **Graham Hutton**, *Programming in Haskell*, 2.ª ed., Cambridge — el libro de texto académico de
  referencia, corto y preciso.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [OCaml](ocaml.md) · [F#](fsharp.md) · [Elm](elm.md) · [Scala](scala.md) ·
[Rust](rust.md)
