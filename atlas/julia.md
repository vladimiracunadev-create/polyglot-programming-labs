# 🔬 Julia — 2012

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Julia nació para resolver **el problema de los dos lenguajes**: escribir el prototipo en
[Python](python.md) o [MATLAB](matlab.md) y luego reescribir lo lento en [C](c.md) o
[Fortran](fortran.md). Su propuesta es que **un lenguaje puede ser cómodo y rápido a la vez**, y lo
consigue con una idea poco frecuente: **despacho múltiple compilado especializando por tipos en
ejecución**.

> **🎯 Por qué está en este programa**
>
> Julia es un **primo de la familia array / científica** ([Atlas](README.md#array-cientifica)), junto a
> [APL](apl.md), [J](j.md), [R](r.md), [MATLAB](matlab.md) y [Fortran](fortran.md).
>
> Aporta al programa **el despacho múltiple como paradigma central**
> ([clase 111](../classes/parte-7-paradigmas/111-herencia-composicion-y-polimorfismo/README.md)) — la
> idea que [Common Lisp](common-lisp.md) tenía con CLOS, aquí convertida en la forma normal de
> organizar el código. Y aporta el ejemplo más claro de **JIT especializante** (clase 126).

| | |
|---|---|
| **Año** | 2012; **1.0** en 2018, con promesa de estabilidad; **1.11** actual |
| **Autoría** | **Jeff Bezanson, Stefan Karpinski, Viral Shah, Alan Edelman** — MIT |
| **Familia** | Array / científica; con [Lisp](common-lisp.md), [Python](python.md), MATLAB y R dentro |
| **Paradigma** | Multiparadigma con **despacho múltiple**; funcional y por arreglos |
| **Tipado** | **Dinámico con tipos ricos**, usados para especializar en compilación |
| **Memoria** | Recolección de basura |
| **Ejecución** | **JIT sobre LLVM**, compilando una versión por combinación de tipos |
| **Estado** | 🟢 **En crecimiento** en cálculo científico, optimización y simulación |

---

## 📜 Historia

En **2012**, cuatro investigadores del MIT publicaron un manifiesto —*Why We Created Julia*— que
enumeraba lo que querían, y que se lee como una lista de deseos imposible:

> Queremos la velocidad de C, el dinamismo de Ruby, la homoiconicidad de Lisp con macros de verdad,
> la notación matemática de MATLAB, la potencia estadística de R, la facilidad de Python para
> guiones, la capacidad de Perl para procesar texto y la potencia lineal de Matlab. **Y que sea fácil
> de aprender.**

El problema concreto que atacaban tiene nombre en la comunidad científica: **el problema de los dos
lenguajes**. Se prototipa en un lenguaje cómodo y, cuando hace falta rendimiento, **se reescriben las
partes críticas en C o Fortran** (clase 155) — con el coste de mantener dos versiones y la frontera
entre ellas.

**La solución de Julia es el despacho múltiple con especialización en compilación**, y es lo que hace
que funcione: **el JIT compila una versión de cada función para cada combinación concreta de tipos con
la que se llama**, así que el código genérico acaba siendo tan rápido como el escrito a mano para esos
tipos.

**Julia 1.0 (2018)** estabilizó el lenguaje, y desde entonces la evolución se ha centrado en el
arranque —su punto débil histórico— y en las herramientas.

## 🏭 Dónde vive hoy

- **Cálculo científico y simulación**: ecuaciones diferenciales (**DifferentialEquations.jl** es de las
  mejores bibliotecas que existen en cualquier lenguaje), mecánica, clima.
- **Optimización matemática**: **JuMP** es referencia en programación lineal y entera.
- **Aprendizaje automático científico**: **Flux**, **SciML**, y la diferenciación automática, que en
  Julia es especialmente natural.
- **Farmacometría y biología de sistemas**: Pumas es un caso comercial notable.
- **Y en investigación en general**, como alternativa a [MATLAB](matlab.md) sin licencia.

## 🧠 Lo que enseña: despacho múltiple

Es el concepto central y merece verlo con calma (clase 111):

```julia
area(c::Circulo) = π * c.r^2
area(r::Rectangulo) = r.a * r.b

# Y con DOS tipos a la vez:
interactuar(a::Asteroide, n::Nave) = "la nave esquiva"
interactuar(a::Asteroide, p::Planeta) = "impacto"
interactuar(n::Nave, p::Planeta) = "aterrizaje"
```

**El método se elige según los tipos de TODOS los argumentos**, no solo del primero. En un lenguaje
con despacho simple —[Java](java.md), [C++](cpp.md), [Python](python.md)— eso obliga al patrón
Visitante o al doble despacho (clase 151); aquí **es la forma normal de escribir**.

**Y la consecuencia arquitectónica es grande, y explica el ecosistema de Julia:**

```text
Un paquete define el tipo `Cuaternion`.
OTRO paquete, sin conocerlo, define la función `graficar`.
Y un TERCERO puede escribir `graficar(::Cuaternion)` sin tocar ninguno de los dos.
```

**Eso hace que las bibliotecas se combinen sin haberlo previsto** —lo que la comunidad llama
composabilidad— y es la razón de que el ecosistema científico de Julia sea tan interoperable.

**Y el JIT especializante es la otra mitad:**

```julia
f(x, y) = x * y + 1

f(2, 3)          # compila una versión para (Int64, Int64)
f(2.0, 3.0)       # compila OTRA para (Float64, Float64)
@code_native f(2, 3)     # ← se puede VER el código máquina generado
```

**El mismo código genérico produce código máquina especializado**, sin comprobaciones de tipo en el
bucle interno. Eso es lo que iguala el rendimiento con C.

> **Y el coste, que hay que decir** (clase 164): **el tiempo hasta el primer gráfico**. Como se compila
> al llamar, **la primera ejecución de cada función paga la compilación** — lo que hacía frustrante el
> arranque interactivo. Julia 1.9+ lo ha mejorado mucho con la caché de código nativo en los paquetes,
> y sigue siendo su punto más criticado.

## 🔄 Lo que se ha modernizado

- **Precompilación de código nativo en paquetes** (1.9): reduce drásticamente el tiempo hasta el
  primer resultado.
- **`PackageCompiler.jl`** y las imágenes de sistema: binarios autocontenidos (clase 174).
- **Multihilo maduro** (`Threads.@threads`, tareas) y computación distribuida en la biblioteca
  estándar (clase 135).
- **Interoperabilidad excelente**: `ccall` con C **sin escribir envoltorios** (clase 156), y
  `PythonCall`, `RCall`, `MATLAB.jl` para llamar a los vecinos.
- **Y `Pkg`**, el gestor de paquetes, con entornos por proyecto y `Manifest.toml` como fichero de
  bloqueo (clase 143) — de lo mejor diseñado de esta lista.

## ⚙️ Cómo se ejecuta hoy

```bash
julia main.jl < entrada.txt          # el comando
julia --project=. -e 'using Pkg; Pkg.test()'    # pruebas con el entorno del proyecto

julia                                 # el REPL, que es donde se trabaja de verdad
# ] activate .    ] instantiate    ] test        ← el modo de paquetes
```

## 🧪 El programa de la clase 041 en Julia

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```julia
v = parse.(Float64, split(readline()))
total = v[1] * v[2] * (1 - v[3])
println("Total: ", round(total; digits=2))
```

**Lo que hay que ver.**

- **`parse.(Float64, ...)` con el punto es la difusión (*broadcasting*)**: el punto **aplica la
  función a cada elemento**. Es la marca de la casa, y funciona con **cualquier** función y **cualquier**
  operador: `a .+ b`, `sin.(v)`, `f.(x, y)`. **Es `map` convertido en sintaxis uniforme** (clase 115),
  y elimina la mayoría de los bucles.
- **Los índices empiezan en 1**, como [Fortran](fortran.md), [R](r.md), [MATLAB](matlab.md) y
  [APL](apl.md) — la convención de la familia científica.
- **`v` es un `Vector{Float64}` con tipo concreto**, y el compilador lo sabe: por eso la aritmética de
  la segunda línea genera el mismo código máquina que en C.
- **`round(total; digits=2)`** usa un argumento con nombre tras el punto y coma — otra decisión de
  legibilidad de la familia científica.
- **Y compárese con [R](r.md)**: los dos tratan la línea como un vector, pero Julia **conoce el tipo
  del vector y compila para él**, mientras que R interpreta.

## 📚 Fuentes y bibliografía

- [Documentación de Julia](https://docs.julialang.org/) — el manual es muy bueno; el apartado
  *Performance Tips* es material directo de la clase 152.
- **Bezanson, Karpinski, Shah, Edelman**, *Why We Created Julia* (2012) y *Julia: A Fresh Approach to
  Numerical Computing* (SIAM Review, 2017) — el manifiesto y el artículo técnico.
- **Ben Lauwens, Allen Downey**, *Think Julia* — libre en línea; introducción desde cero.
- [Julia Academy](https://juliaacademy.com/) y [JuliaCon](https://juliacon.org/) — cursos y charlas.
- **Stefan Karpinski**, *The Unreasonable Effectiveness of Multiple Dispatch* (JuliaCon 2019) — la
  mejor explicación de por qué el despacho múltiple cambia la composición de bibliotecas (clase 151).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Python](python.md) · [R](r.md) · [MATLAB](matlab.md) · [Fortran](fortran.md) ·
[Common Lisp](common-lisp.md)
