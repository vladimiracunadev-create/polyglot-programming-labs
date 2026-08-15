# 🦀 Rust — 2010

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Rust resolvió un problema que llevaba cincuenta años abierto: **conseguir seguridad de memoria sin
recolector de basura y sin perder rendimiento**. Lo hizo con una idea —**la propiedad y el préstamo**—
que no existía en ningún lenguaje mayoritario, y que hoy están copiando todos.

> **🎯 Por qué está en este programa**
>
> **Rust es uno de los diez lenguajes del núcleo** y, junto a [Go](go.md), el **representante de la
> familia de sistemas** ([Atlas](README.md#sistemas)).
>
> Aporta al programa el concepto que da nombre a una clase entera: **propiedad, movimiento y
> préstamo**
> ([clase 081](../classes/parte-5-funciones-y-modularidad/081-semantica-de-movimiento-y-prestamo-rust/README.md)
> y [clase 132](../classes/parte-8-como-funcionan-los-lenguajes/132-raii-propiedad-y-prestamos-rust-c-plus-plus/README.md)),
> y el de **concurrencia sin carreras garantizada por el compilador**
> ([clase 136](../classes/parte-8-como-funcionan-los-lenguajes/136-el-modelo-de-memoria-y-las-condiciones-de-carrera/README.md)).
> Es el contrapunto exacto de [C++](cpp.md) y el complemento de [Go](go.md).

| | |
|---|---|
| **Año** | 2010 (público); **1.0** en 2015; **ediciones** 2015, 2018, 2021, 2024 |
| **Autoría** | **Graydon Hoare**, como proyecto personal (2006); adoptado por Mozilla |
| **Familia** | Sistemas; con influencia fuerte de **ML**, [OCaml](ocaml.md) y **Cyclone** |
| **Paradigma** | Multiparadigma: imperativo, funcional y con genéricos por rasgos |
| **Tipado** | **Estático, fuerte, con inferencia** y tipos algebraicos |
| **Memoria** | **Sin recolector**: propiedad, préstamos y tiempos de vida comprobados al compilar |
| **Ejecución** | Compilado a nativo sobre **LLVM**; sin tiempo de ejecución significativo |
| **Estado** | 🟢 **En crecimiento fuerte**; en el núcleo de Linux, Windows y Android |

---

## 📜 Historia

**Graydon Hoare** empezó Rust en **2006** como proyecto personal. La anécdota de origen es buena: el
ascensor de su edificio se había averiado por un fallo de software, y le pareció absurdo que en 2006
siguiéramos escribiendo software de sistemas en lenguajes que permiten corromper memoria.

**Mozilla** lo adoptó en **2009** con un objetivo concreto: **Servo**, un motor de navegador
paralelo. Porque el problema real era ese — **paralelizar el renderizado de una página en C++ era
inviable** por las carreras de datos, y hacía falta un lenguaje donde eso fuera seguro.

Rust cambió mucho antes de la **1.0 (2015)**: llegó a tener recolector de basura, hilos ligeros y
punteros con sigilo, y **todo eso se quitó**. Lo que quedó fue el sistema de propiedad, que es la
aportación real.

**El sistema de ediciones** (2018, 2021, 2024) resuelve un problema de la clase 143 de forma elegante:
**se pueden hacer cambios incompatibles de sintaxis sin romper nada**, porque cada *crate* declara su
edición y **las ediciones interoperan**. Es una idea que merece copiarse.

Y desde **2021**, tras la reestructuración de Mozilla, el lenguaje lo gobierna la **Rust Foundation**,
con AWS, Google, Microsoft, Meta y Huawei entre sus miembros.

## 🏭 Dónde vive hoy

- **Núcleos de sistemas operativos**: **Linux** admite controladores en Rust desde 2022; **Windows** y
  **Android** tienen componentes reescritos, con reducción medible de vulnerabilidades (clase 153).
- **Infraestructura de red**: Cloudflare (Pingora), Discord, Dropbox, AWS (Firecracker).
- **Herramientas de desarrollo rapidísimas**: `ripgrep`, `fd`, `bat`, y toda la generación nueva de
  herramientas de JavaScript y Python —`swc`, `ruff`, `uv`, `biome`— **escritas en Rust** (clase 167).
- **WebAssembly**: es el lenguaje con mejor soporte del ecosistema (clase 162).
- **Sistemas embebidos y criptografía**, donde la ausencia de recolector es un requisito.
- **Bases de datos**: TiKV, InfluxDB 3, Datafusion.

## 🧠 La idea: propiedad, préstamo y tiempos de vida

Es el concepto que hay que llevarse de esta ficha, y se resume en tres reglas:

```rust
let a = String::from("hola");
let b = a;              // MOVIMIENTO: ahora b es el dueño
// println!("{a}");      // ✗ error de compilación: a ya no vale

let c = &b;              // PRÉSTAMO inmutable: se puede tener muchos
let d = &mut b;           // PRÉSTAMO mutable: solo UNO, y ninguno inmutable a la vez
```

**Las tres reglas del comprobador de préstamos:**

1. **Cada valor tiene exactamente un dueño.**
2. **Puede haber muchas referencias inmutables, o una mutable — nunca las dos cosas.**
3. **Ninguna referencia puede vivir más que el valor al que apunta.**

**Y de esas tres reglas salen, gratis, tres garantías** que la clase 136 desarrolla:

- **No hay uso después de liberar**, porque la referencia no sobrevive al valor.
- **No hay doble liberación**, porque solo hay un dueño.
- **Y no hay carreras de datos**, porque no puede haber una escritura y una lectura simultáneas.

**La tercera es la que asombra**: el mismo mecanismo que gestiona la memoria **elimina las carreras de
datos en tiempo de compilación**, sin coste en ejecución. Es lo que Mozilla necesitaba para Servo, y es
la razón por la que existe el lenguaje.

> **Y el precio hay que decirlo, porque es real**: **la curva de aprendizaje es empinada**. El
> comprobador de préstamos rechaza programas correctos que no sabe demostrar, y aprender a
> estructurar el código para que pase **es el trabajo de las primeras semanas**. A cambio, quien
> escribe Rust deja de depurar corrupciones de memoria (clase 153) — pero el cambio no es gratis.

## 🔄 Lo que se ha modernizado

- **`async`/`await`** (2019) con tiempos de ejecución intercambiables (Tokio, async-std), y el
  ecosistema asíncrono maduro.
- **Edición 2024** con `gen`, mejoras del comprobador de préstamos y `impl Trait` en más sitios.
- **Rust en el núcleo de Linux**, con las abstracciones seguras sobre las interfaces C (clase 156).
- **Herramientas de verificación**: **Kani**, **Creusot**, **Prusti** — demostración formal sobre
  Rust, persiguiendo lo que [SPARK](ada.md) tiene maduro (clase 164).
- **`cargo` como referencia**: gestor de paquetes, sistema de construcción, pruebas, documentación,
  formateo y análisis **en una sola herramienta**, con fichero de bloqueo (clase 143). Es el estándar
  con el que se comparan los demás ecosistemas.

## ⚙️ Cómo se ejecuta hoy

```bash
rustc main.rs -O && ./main < entrada.txt      # el camino de la clase 041
cargo run --release

cargo fmt && cargo clippy -- -D warnings       # calidad (clase 146)
cargo test                                      # pruebas, integradas
cargo doc --open                                 # documentación desde los comentarios (clase 154)
```

## 🧪 El programa de la clase 041 en Rust

```rust
use std::io::Read;

fn main() {
    let mut entrada = String::new();
    std::io::stdin().read_to_string(&mut entrada).unwrap();
    let campos: Vec<&str> = entrada.split_whitespace().collect();

    // Rust: inmutable por defecto (`let`), tipos explícitos, conversión con `as`.
    let precio_unitario: f64 = campos[0].parse().unwrap();
    let cantidad: i64 = campos[1].parse().unwrap();
    let descuento: f64 = campos[2].parse().unwrap();

    let subtotal = precio_unitario * cantidad as f64;
    let total = subtotal * (1.0 - descuento);

    println!("Total: {total:.2}");
}
```

**Lo que hay que ver.**

- **`let` es inmutable por defecto**; para poder modificar hay que escribir `let mut`. Es lo contrario
  de casi todos los lenguajes de esta lista, y la clase 102 explica por qué importa: **la
  inmutabilidad por defecto convierte cada mutación en una decisión visible**.
- **`Vec<&str>` es la clave del sistema de propiedad en este programa**: los campos **no son copias**,
  son **referencias prestadas** a la cadena `entrada`. Por eso `entrada` tiene que seguir viva mientras
  se usen — y el compilador lo comprueba. En [Java](java.md) o [Go](go.md) eso sería una copia.
- **`.unwrap()` es una decisión, no un descuido**: `parse` devuelve `Result`, y **el lenguaje obliga a
  tratarlo** (clase 116). `unwrap` dice "si falla, aborta" — aceptable en un ejemplo, y en producción
  se escribiría `?` o un `match`.
- **`cantidad as f64` es explícito**, igual que en [Go](go.md): Rust no convierte números sin
  permiso.
- **`{total:.2}` interpola la variable directamente** en la cadena de formato, y el formato se
  comprueba **en compilación** — como `std::format` de [C++20](cpp.md) (clase 142).

## 📚 Fuentes y bibliografía

- [*The Rust Programming Language*](https://doc.rust-lang.org/book/) — "el libro", oficial, libre y
  uno de los mejores textos de introducción de cualquier lenguaje.
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/) y
  [Rustlings](https://github.com/rust-lang/rustlings) — para practicar el comprobador de préstamos.
- [El Rustonomicon](https://doc.rust-lang.org/nomicon/) — para cuando haga falta `unsafe`; explica lo
  que el compilador estaba garantizando.
- **Jon Gjengset**, *Rust for Rustaceans*, No Starch Press — el libro para después del primero; tipos,
  rasgos, `async` y `unsafe` a fondo.
- **Steve Klabnik, Carol Nichols**, *The Rust Programming Language*, 2.ª ed. impresa, No Starch Press.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [C++](cpp.md) · [Go](go.md) · [Zig](zig.md) · [OCaml](ocaml.md) · [Ada](ada.md)
