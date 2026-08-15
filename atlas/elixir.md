# 💧 Elixir — 2011

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Elixir es lo que pasa cuando alguien mira [Erlang](erlang.md), reconoce que su máquina virtual es
extraordinaria y decide que **el problema es todo lo demás**: la sintaxis, las herramientas y la
documentación. El resultado conserva el modelo de actores y la tolerancia a fallos, con la ergonomía
de [Ruby](ruby.md).

> **🎯 Por qué está en este programa**
>
> Elixir es un **primo de la familia concurrente / actor** ([Atlas](README.md#concurrente-actor)),
> junto a [Erlang](erlang.md), con quien comparte máquina virtual.
>
> Aporta al programa una lección de la clase 164 en estado puro: **el ecosistema y la ergonomía pesan
> más que el modelo técnico**. Erlang tenía el modelo desde 1986 y seguía siendo minoritario; Elixir
> **no cambió el modelo** —cambió la sintaxis y las herramientas— y multiplicó la adopción.

| | |
|---|---|
| **Año** | 2011; **1.0** en 2014; **1.18** actual, con análisis de tipos |
| **Autoría** | **José Valim**, que venía del núcleo de Ruby on Rails |
| **Familia** | Concurrente / actor; sobre la **BEAM** de Erlang |
| **Paradigma** | **Funcional y concurrente**, con datos inmutables |
| **Tipado** | **Dinámico y fuerte**; con **inferencia de tipos gradual** en desarrollo |
| **Memoria** | La de la BEAM: montón y recolector **por proceso** |
| **Ejecución** | Bytecode sobre la BEAM, con JIT |
| **Estado** | 🟢 **En crecimiento**: web en tiempo real, sistemas distribuidos, IoT |

---

## 📜 Historia

**José Valim** era miembro del equipo central de **Ruby on Rails** y se topó con un problema
estructural: **Ruby no aprovecha bien los procesadores multinúcleo** por su bloqueo global del
intérprete (clase 135). Buscando alternativas, encontró la BEAM.

Su diagnóstico fue el que define esta ficha: **la máquina virtual de Erlang es una obra maestra de
ingeniería, y su lenguaje y sus herramientas son la barrera de entrada**.

Así que en **2011** construyó **Elixir**: **el mismo modelo, la misma máquina virtual, la misma
interoperabilidad total con Erlang** —se pueden llamar módulos de Erlang directamente, sin capa— y
encima:

- **Sintaxis inspirada en Ruby**, mucho más familiar.
- **Macros higiénicas** al estilo Lisp, con las que se construye buena parte del lenguaje.
- **Herramientas modernas**: `mix` para construir, `hex` para dependencias con fichero de bloqueo
  (clase 143), `ExUnit` para pruebas (clase 139) y **documentación de primera clase**.
- **Y `iex`**, una consola interactiva excelente.

**Phoenix** (2014) hizo por Elixir lo que Rails hizo por Ruby, y en **2018** llegó **LiveView**: una
forma de construir interfaces web interactivas **sin escribir JavaScript**, manteniendo el estado en
el servidor con un proceso por usuario — algo que solo es viable porque **los procesos de la BEAM son
baratísimos** (clase 168).

## 🏭 Dónde vive hoy

- **Aplicaciones web en tiempo real**: Discord —millones de usuarios concurrentes—, Pinterest,
  Bleacher Report, Heroku.
- **Sistemas distribuidos y mensajería**, donde la tolerancia a fallos importa.
- **Internet de las cosas**: **Nerves** permite ejecutar Elixir en dispositivos embebidos, con
  actualización remota y supervisión.
- **Procesamiento de datos**: **Broadway** para canalizaciones con contrapresión (clase 168).
- **Y aprendizaje automático**: **Nx** y **Livebook** —cuadernos ejecutables, al estilo de Jupyter—
  son un desarrollo reciente y notable.

## 🧠 Lo que enseña: la misma potencia con otra puerta

**Uno, la canalización**, que es la marca de la casa:

```elixir
"1 2 3"
|> String.split()
|> Enum.map(&String.to_float/1)
|> Enum.sum()
```

**`|>` pasa el resultado como primer argumento de la siguiente función.** Viene de
[F#](fsharp.md) y de [OCaml](ocaml.md), y hace que las transformaciones se lean **en el orden en que
ocurren** en lugar de anidadas.

**Dos, el emparejamiento de patrones como control de flujo:**

```elixir
def procesar({:ok, valor}), do: "todo bien: #{valor}"
def procesar({:error, razon}), do: "falló: #{razon}"
```

**Varias cláusulas de la misma función, seleccionadas por la forma del argumento** — como en
[Erlang](erlang.md) y en [Haskell](haskell.md). Y la convención `{:ok, ...}` / `{:error, ...}` es el
manejo de errores idiomático (clase 116): **el resultado lleva el éxito o el fallo en su forma**.

**Y tres, las macros**, con las que está construido el propio lenguaje:

```elixir
defmodule MiPrueba do
  use ExUnit.Case            # ← una macro que inyecta el comportamiento de prueba
  test "suma" do             # ← 'test' también es una macro
    assert 1 + 1 == 2         # ← y 'assert' MUESTRA los valores al fallar
  end
end
```

**`if`, `unless`, `def` y `defmodule` son macros**, no palabras clave del lenguaje. Es la
homoiconicidad de [Lisp](common-lisp.md) (clase 122) aplicada con una sintaxis convencional — y es lo
que permite que Phoenix y Ecto tengan las API que tienen.

Y merece señalar lo que **no** cambió: **el modelo de procesos, la supervisión y "déjalo fallar" son
exactamente los de Erlang**. Un módulo de Erlang se llama desde Elixir con `:modulo.funcion()`, sin
puente ni conversión (clase 155).

## 🔄 Lo que se ha modernizado

- **Inferencia de tipos gradual** (desde 1.17): un sistema de **conjuntos de tipos** que detecta
  errores **sin anotaciones**, integrado en el compilador. Es uno de los desarrollos de diseño de
  lenguajes más interesantes en curso (clase 146).
- **LiveView**: interfaz web con estado en el servidor y actualizaciones por WebSocket — con un
  proceso por usuario (clases 168 y 169).
- **Nx, Axon, Bumblebee y Livebook**: aprendizaje automático y cuadernos ejecutables sobre la BEAM.
- **Nerves**: sistemas embebidos con la misma tolerancia a fallos.
- **Y `mix format`** sin opciones, como `gofmt` (clase 146).

## ⚙️ Cómo se ejecuta hoy

```bash
elixir main.exs < entrada.txt        # como guion
iex                                   # consola interactiva

mix new proyecto && mix test          # construcción y pruebas (clases 139 y 147)
mix format && mix credo                # estilo y análisis (clase 146)
mix dialyzer                            # análisis de tipos con Dialyzer
```

## 🧪 El programa de la clase 041 en Elixir

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```elixir
[precio, cantidad, descuento] =
  IO.gets("")
  |> String.trim()
  |> String.split()
  |> Enum.map(&String.to_float/1)

total = precio * cantidad * (1 - descuento)
IO.puts("Total: #{:erlang.float_to_binary(total, decimals: 2)}")
```

**Lo que hay que ver.**

- **La canalización se lee de arriba abajo**, en el orden de las operaciones: leer, recortar, partir,
  convertir. Compárese con la versión anidada que haría falta sin `|>`.
- **`[a, b, c] = ...` es emparejamiento**, igual que en [Erlang](erlang.md): **el `=` de Elixir es un
  operador de coincidencia, no de asignación** (clase 041).
- **`&String.to_float/1`** es la captura de una función con su aridad — la aridad forma parte de la
  identidad de la función, herencia directa de Erlang.
- **`:erlang.float_to_binary(...)` llama a Erlang directamente**, con `:` para los átomos de módulo.
  **Esa es la interoperabilidad total**: no hay envoltorio ni conversión (clase 155).
- **Y `#{...}` es interpolación de cadenas**, tomada de [Ruby](ruby.md) — la ergonomía que Valim vino
  a traer.

## 📚 Fuentes y bibliografía

- [elixir-lang.org](https://elixir-lang.org/getting-started/introduction.html) — la guía oficial;
  **la documentación de Elixir es de las mejores de cualquier lenguaje**, y eso fue deliberado.
- [Elixir School](https://elixirschool.com/es) — en español, comunitario.
- **Dave Thomas**, *Programming Elixir ≥ 1.6*, Pragmatic — la introducción de referencia.
- **Saša Jurić**, *Elixir in Action*, 3.ª ed., Manning — **el mejor libro para entender OTP y la
  concurrencia**, no solo la sintaxis.
- **Chris McCord et al.**, *Programming Phoenix LiveView* — para la parte web (clases 168 y 169).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Erlang](erlang.md) · [Ruby](ruby.md) · [Clojure](clojure.md) · [Go](go.md) ·
[F#](fsharp.md)
