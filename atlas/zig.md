# ⚡ Zig — 2016

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Zig es la propuesta más radical de las que intentan suceder a [C](c.md): **no añadir seguridad
automática, sino hacer visible todo lo que C esconde**. Cada reserva de memoria, cada operación que
puede fallar y cada rama del flujo de control aparecen escritas — y a cambio no hay nada oculto.

> **🎯 Por qué está en este programa**
>
> Zig es un **primo de la familia C / llaves** ([Atlas](README.md#c-llaves)) y aparece junto a los
> representantes de sistemas del núcleo, [Go](go.md) y [Rust](rust.md).
>
> Aporta al programa dos ideas que ningún otro lenguaje del curso enseña igual: **el asignador de
> memoria como parámetro explícito** —quien llama decide de dónde sale la memoria (clases 128 y
> 130)— y **`comptime`**, ejecutar código del propio lenguaje en tiempo de compilación en lugar de
> tener un lenguaje de macros aparte
> ([clase 122](../classes/parte-8-como-funcionan-los-lenguajes/123-del-codigo-a-la-ejecucion-fases-de-compilacion/README.md)).

| | |
|---|---|
| **Año** | 2016; en **0.x** — aún no ha llegado a 1.0 |
| **Autoría** | **Andrew Kelley**; hoy con la Zig Software Foundation |
| **Familia** | Sistemas / C; sin herencia sintáctica de C++ |
| **Paradigma** | Imperativo y procedimental; sin clases ni herencia |
| **Tipado** | **Estático y fuerte**, con genéricos vía `comptime` y tipos opcionales |
| **Memoria** | **Manual y explícita**, con asignadores que se pasan como argumento |
| **Ejecución** | Compilado a nativo (LLVM y motor propio); **compilador cruzado universal** |
| **Estado** | 🟡 **Preestándar**: se usa en producción con cuidado, y la API cambia |

---

## 📜 Historia

**Andrew Kelley** empezó Zig en **2015** por frustración con C y con C++: quería un lenguaje donde
**no hubiera control de flujo oculto** —nada de constructores, destructores, sobrecarga de operadores
ni excepciones— y donde **cada reserva de memoria fuera visible**.

El proyecto creció con una propiedad inesperada que lo hizo conocido antes que el lenguaje: **`zig
cc` es un compilador de C excelente**, con **compilación cruzada a cualquier plataforma sin instalar
nada más**.

```bash
zig cc -target aarch64-linux-musl hola.c    # desde cualquier máquina, sin cadena cruzada
```

Eso resolvió, de rebote, uno de los problemas más molestos de la clase 174, y hizo que mucha gente
usara Zig como herramienta antes que como lenguaje. **Bun**, el tiempo de ejecución de JavaScript,
está escrito en Zig.

El lenguaje sigue **antes de la 1.0**, con cambios incompatibles en cada versión —el sistema de
entrada y salida se está rediseñando ahora mismo— y con el compilador migrando de LLVM a un motor
propio.

## 🏭 Dónde vive hoy

- **Bun**: el tiempo de ejecución de JavaScript, escrito en Zig.
- **TigerBeetle**: base de datos financiera de alto rendimiento — un caso de uso serio y exigente.
- **Como cadena de herramientas de C**: `zig cc` y `zig build` en proyectos que no son de Zig.
- **Sistemas embebidos y desarrollo de núcleo**, por la ausencia de tiempo de ejecución.
- **Y en proyectos nuevos de infraestructura** que aceptan el riesgo de una API que aún cambia.

## 🧠 Lo que enseña: hacer visible lo que C esconde

**Uno, el asignador explícito.** En Zig, **una función que reserva memoria recibe de dónde sacarla**:

```zig
fn crearLista(asignador: std.mem.Allocator, n: usize) ![]u32 {
    return try asignador.alloc(u32, n);
}
```

**Y eso cambia el diseño entero de la biblioteca estándar**: no hay un montón global implícito. Quien
llama decide si la memoria viene del montón, de una arena que se libera de golpe, de un búfer en la
pila o de un asignador que detecta fugas en las pruebas (clases 130 y 139).

Es la idea que la clase 128 persigue —**saber de dónde sale la memoria**— convertida en firma de
función.

**Dos, los errores son valores y el flujo está escrito:**

```zig
const valor = try puedeFallar();    // ← 'try' propaga el error; SIEMPRE se ve
```

**No hay excepciones**, como en [Go](go.md), pero el error forma parte del tipo (`!u32`), así que
**ignorarlo no compila** (clase 116).

**Y tres, `comptime`:**

```zig
fn Lista(comptime T: type) type {          // los genéricos son FUNCIONES sobre tipos
    return struct { items: []T };
}
```

**El mismo lenguaje se ejecuta en tiempo de compilación** para generar tipos, desplegar bucles o
calcular tablas. Es la metaprogramación de la clase 123 **sin un lenguaje de macros aparte** — lo
contrario del preprocesador de C y de las plantillas de [C++](cpp.md).

> **Y la comparación con [Rust](rust.md) es la que importa** (clase 164): **Rust hace imposible el
> error de memoria; Zig lo hace visible.** Zig detecta el desbordamiento y el uso de memoria no
> inicializada **en modo depuración**, y en modo seguro comprueba límites — pero **no tiene
> comprobador de préstamos**, así que un uso después de liberar sigue siendo posible. Son dos
> apuestas distintas sobre el mismo problema, y merece conocer las dos antes de opinar.

## 🔄 Hacia dónde va

- **Camino a la 1.0**, con el sistema de entrada y salida rediseñado y la API estabilizándose.
- **Compilador propio sin LLVM** para las plataformas principales, con compilación mucho más rápida.
- **`zig build`** como sistema de construcción escrito en el propio Zig — sin lenguaje de
  configuración aparte (clase 144).
- **Y el papel de puente**: `zig cc` y `zig c++` como cadena de herramientas cruzada para proyectos C
  y C++ existentes, que es hoy su uso más extendido.

## ⚙️ Cómo se ejecuta hoy

```bash
zig run main.zig < entrada.txt
zig build-exe main.zig -O ReleaseSafe        # con comprobaciones; o ReleaseFast
zig build test                                # pruebas, integradas en el lenguaje

zig cc -target x86_64-windows-gnu hola.c      # ← compilar C para otra plataforma
```

## 🧪 El programa de la clase 041 en Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const precio = try std.fmt.parseFloat(f64, it.next().?);
    const cantidad = try std.fmt.parseFloat(f64, it.next().?);
    const descuento = try std.fmt.parseFloat(f64, it.next().?);
    const total = precio * cantidad * (1 - descuento);
    try std.io.getStdOut().writer().print("Total: {d:.2}\n", .{total});
}
```

**Lo que hay que ver, y es la ficha donde más se nota.**

- **`var buf: [128]u8` reserva el búfer a mano, en la pila.** Ningún otro programa de la clase 041
  hace eso: los demás piden una cadena y el lenguaje se ocupa. Aquí **el tamaño es una decisión
  visible**, y si la línea no cupiera, se vería (clase 128).
- **`try` aparece cinco veces**, y cada una es una operación que puede fallar. **El flujo de error
  está escrito en el código**, no escondido en excepciones (clase 116).
- **`.?` desempaqueta un opcional** y aborta si es nulo: Zig **distingue en el tipo** lo que puede
  faltar, como [Rust](rust.md) con `Option` (clase 100).
- **`!void` en la firma de `main`** declara que la función puede devolver un error. El tipo de retorno
  **incluye el fallo**, que es la idea central del manejo de errores del lenguaje.
- **Comparado con la versión de [C](c.md)**, que hace lo mismo en seis líneas: Zig es más largo
  **a propósito**. Lo que C oculta —el búfer, el fallo de conversión, el nulo— aquí está escrito.

## 📚 Fuentes y bibliografía

- [ziglang.org/documentation](https://ziglang.org/documentation/master/) — la referencia oficial; al
  ser preestándar, **usar siempre la de la versión que se tenga instalada**.
- [Zig Learn](https://ziglearn.org/) y [zig.guide](https://zig.guide/) — introducciones comunitarias.
- [Notas de versión](https://ziglang.org/download/) — imprescindibles: cada versión trae cambios
  incompatibles y los documenta bien.
- **Andrew Kelley**, charlas *The Road to Zig 1.0* y *Practical Data Oriented Design* — la segunda
  explica la relación entre disposición de datos y rendimiento mejor que casi cualquier texto
  (clase 152).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [C](c.md) · [Rust](rust.md) · [Go](go.md) · [Nim](nim.md) · [D](d.md)
