# 🔵 F# — 2005

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

F# es **[OCaml](ocaml.md) sobre .NET**, y es la demostración de que un lenguaje funcional puede vivir
en un ecosistema empresarial sin renunciar a nada: usa las mismas bibliotecas que
[C#](csharp.md), interopera sin fricción, y **muchas de las mejores ideas de C# de la última década
llegaron desde aquí**.

> **🎯 Por qué está en este programa**
>
> F# es un **primo de la familia .NET** ([Atlas](README.md#dotnet)), cuyo representante en el núcleo
> es [C#](csharp.md), y también de la **familia funcional tipada (ML)**.
>
> Aporta al programa la **inferencia de tipos completa al estilo Hindley-Milner** —tipado estático sin
> escribir casi ningún tipo— y **los tipos de datos algebraicos con emparejamiento exhaustivo**
> ([clase 100](../classes/parte-6-datos-y-estructuras/100-enumeraciones-y-tipos-algebraicos-adt-sum-types/README.md)), que son las
> dos ideas de ML que hoy están llegando a todos los lenguajes.

| | |
|---|---|
| **Año** | 2005; **1.0** en 2010; hoy en **F# 9**, con .NET |
| **Autoría** | **Don Syme**, Microsoft Research Cambridge — también autor de los genéricos de .NET |
| **Familia** | .NET y funcional tipada (ML); descendiente directo de [OCaml](ocaml.md) |
| **Paradigma** | **Funcional primero**, con OO completo cuando hace falta |
| **Tipado** | **Estático con inferencia total**; tipos algebraicos y unidades de medida |
| **Memoria** | La del CLR: recolección de basura |
| **Ejecución** | Bytecode IL sobre el CLR, con JIT o AOT nativo |
| **Estado** | 🟢 **Vivo y minoritario**; muy usado en finanzas y análisis de datos |

---

## 📜 Historia

**Don Syme** trabajaba en Microsoft Research y tiene un mérito que conviene conocer: **diseñó e
implementó los genéricos de .NET** —**reificados**, a diferencia de los de [Java](java.md) (clase
108)— y lo hizo, en parte, **porque los necesitaba para poder llevar ML a la plataforma**.

Es una historia poco común: **una característica del ecosistema entero existe porque alguien quería
hacer un lenguaje funcional en él**.

F# apareció en **2005** como puerto de OCaml sobre .NET, y se convirtió en producto oficial de
Microsoft en **2010**. Desde entonces es de código abierto y multiplataforma, con la **F# Software
Foundation** implicada en su gobierno.

Y su influencia sobre su hermano mayor es grande y está documentada: **los registros, el
emparejamiento de patrones, los tipos con nulabilidad, `async`/`await` y las expresiones `switch` de
[C#](csharp.md) vienen, en buena parte, de F#**. Es el laboratorio de la plataforma.

## 🏭 Dónde vive hoy

- **Finanzas cuantitativas**: es su nicho más fuerte; bancos y fondos lo usan para modelos y
  valoración, donde la corrección importa más que la popularidad.
- **Análisis de datos y ciencia**: con los **proveedores de tipos**, que son su característica más
  original.
- **Servicios de fondo y APIs**: con Giraffe o Falco sobre ASP.NET Core.
- **Cálculo y simulación**, y como lenguaje de guion analítico dentro de organizaciones .NET.

## 🧠 Lo que enseña: inferencia total y tipos algebraicos

**Uno, la inferencia Hindley-Milner:**

```fsharp
let sumar a b = a + b            // ← ni un tipo escrito
// el compilador deduce: int -> int -> int

let procesar lista =
    lista |> List.filter (fun x -> x > 0) |> List.sum
// deduce: int list -> int
```

**Tipado estático completo sin escribir tipos.** Es más fuerte que la inferencia local de
[C#](csharp.md) con `var` o de [Java](java.md): **F# infiere las firmas de las funciones**, no solo
las variables locales.

**Dos, los tipos algebraicos con exhaustividad:**

```fsharp
type Forma =
    | Circulo of radio: float
    | Rectangulo of ancho: float * alto: float

let area f =
    match f with
    | Circulo r -> System.Math.PI * r * r
    | Rectangulo (a, b) -> a * b
    // ← si falta un caso, el compilador AVISA
```

**Y la combinación de las dos cosas es lo que hace productivo el estilo**: se modela el dominio con
tipos que **hacen imposible representar un estado inválido**, y el compilador comprueba que se han
tratado todos los casos (clase 166).

**Y tres, dos cosas que F# tiene y casi nadie más:**

```fsharp
[<Measure>] type m
[<Measure>] type s
let velocidad = 100.0<m> / 9.58<s>    // float<m/s>
// let error = 100.0<m> + 9.58<s>       ← ✗ NO COMPILA
```

**Las unidades de medida comprobadas en compilación, sin coste en ejecución.** Es exactamente lo que
la clase 166 señalaba con el Mars Climate Orbiter: **el contrato de las unidades, en el tipo**.

```fsharp
type Datos = CsvProvider<"ventas.csv">     // ← el TIPO se genera del fichero
let filas = Datos.Load("ventas.csv")
filas.Rows |> Seq.sumBy (fun r -> r.Importe)   // con autocompletado y comprobación
```

**Los proveedores de tipos** leen un esquema —CSV, JSON, SQL, un servicio web— **en tiempo de
compilación** y generan los tipos. Es metaprogramación (clase 123) aplicada al problema de la
clase 170: **el desajuste de impedancia resuelto generando el tipo desde el esquema**.

## 🔄 Lo que se ha modernizado

- **F# 6-9**: `task { }` para interoperar con el `async` de C#, expresiones de índice, y mejoras
  grandes de rendimiento del compilador.
- **AOT nativo** sobre .NET, con binarios de arranque instantáneo (clase 174).
- **Fable**: compila F# **a JavaScript**, y también a Python, Rust y Dart — un objetivo múltiple poco
  común (clase 162).
- **`dotnet fsi`**: consola interactiva de primer nivel para explorar datos, al estilo de
  [Lisp](common-lisp.md) (clase 124).
- **Y una comunidad activa** que empuja las novedades hacia C#, que es donde acaban llegando.

## ⚙️ Cómo se ejecuta hoy

```bash
dotnet fsi main.fsx < entrada.txt         # ejecutar como guion
dotnet run                                  # como proyecto

dotnet fsi                                  # consola interactiva
dotnet test                                  # pruebas, con Expecto o xUnit (clase 139)
```

## 🧪 El programa de la clase 041 en F\#

```fsharp
let [| precio; cantidad; descuento |] =
    stdin.ReadLine().Split(' ') |> Array.map float
let total = precio * cantidad * (1.0 - descuento)
printfn "Total: %.2f" total
```

**Lo que hay que ver.**

- **`|>` es el operador de canalización**, y es la marca de la casa: `x |> f` es `f x`. Permite leer
  la transformación **de izquierda a derecha, en el orden en que ocurre** —en lugar de anidada de
  dentro afuera— y es lo que después adoptaron [Elixir](elixir.md), [R](r.md) y JavaScript en
  propuesta.
- **`let [| a; b; c |] = ...` es emparejamiento de patrones sobre un arreglo**, igual que en
  [Scala](scala.md): si la línea no trajera tres campos, fallaría.
- **`1.0` con decimal no es un capricho**: F# **no convierte números implícitamente**, así que
  `1 - descuento` con un entero **no compila**. Es la misma disciplina de [Go](go.md) y
  [Rust](rust.md) (clase 100).
- **`printfn "Total: %.2f"` está comprobado en compilación**: el `%.2f` **exige un `float`**, y el
  compilador lo verifica. Es más fuerte que el `printf` de [C](c.md), que no comprueba nada
  (clase 142), y que el de C#.
- **Y no hay clase, ni `main`, ni llaves**: la sangría marca el bloque, como en
  [Python](python.md).

## 📚 Fuentes y bibliografía

- [F# for Fun and Profit](https://fsharpforfunandprofit.com/) — **Scott Wlaschin**; probablemente el
  mejor sitio para aprender programación funcional aplicada, con o sin F#. Su serie sobre **modelar el
  dominio con tipos** es directamente material de la clase 166.
- [Documentación oficial de F#](https://learn.microsoft.com/dotnet/fsharp/) y
  [fsharp.org](https://fsharp.org/).
- **Scott Wlaschin**, *Domain Modeling Made Functional*, Pragmatic — cómo llevar el diseño dirigido por
  el dominio a tipos que no permiten estados inválidos.
- **Don Syme, Adam Granicz, Antonio Cisternino**, *Expert F#*, Apress — la referencia del autor del
  lenguaje.
- [Fable](https://fable.io/) — para el objetivo JavaScript y los demás.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [OCaml](ocaml.md) · [C#](csharp.md) · [Haskell](haskell.md) · [Elm](elm.md) ·
[Scala](scala.md)
