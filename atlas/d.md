# 🅳 D — 2001

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

D es **el C++ que Walter Bright habría hecho si hubiera podido empezar de cero**, y lo dice con
autoridad: Bright escribió el primer compilador nativo de C++ del mundo. Es un lenguaje excelente,
técnicamente adelantado a su tiempo en varias cosas, y **el caso de estudio más claro de que la calidad
técnica no basta** (clase 164).

> **🎯 Por qué está en este programa**
>
> D es un **primo de la familia C / llaves** ([Atlas](README.md#c-llaves)), cuyo representante en el
> núcleo es [C](c.md).
>
> Aporta al programa una idea que hoy está en todas partes y que D tuvo primero: **ejecutar código
> del propio lenguaje en tiempo de compilación** —CTFE, de 2007—, que es lo que
> [Zig](zig.md) llama `comptime`, [C++](cpp.md) llama `constexpr` y [Rust](rust.md) llama `const fn`
> ([clase 122](../classes/parte-7-paradigmas-de-programacion/122-metaprogramacion/README.md)). Y
> aporta el ejemplo más didáctico de **cómo una decisión de gobernanza puede hundir un lenguaje**.

| | |
|---|---|
| **Año** | 2001; **D2** en 2007, incompatible con D1; estable desde ~2010 |
| **Autoría** | **Walter Bright** (autor del compilador Zortech C++), con **Andrei Alexandrescu** |
| **Familia** | C / llaves; rediseño de C++ con influencia de [Java](java.md) y [Python](python.md) |
| **Paradigma** | Multiparadigma: imperativo, OO, funcional, genérico y metaprogramación |
| **Tipado** | **Estático y fuerte**, con inferencia, `immutable` y `pure` comprobados |
| **Memoria** | **Recolector opcional**: se puede usar, evitar (`@nogc`) o gestionar a mano |
| **Ejecución** | Compilado a nativo — tres compiladores: DMD (rápido), LDC (LLVM), GDC (GCC) |
| **Estado** | 🟡 **Vivo y minoritario**: excelente, con adopción industrial pequeña |

---

## 📜 Historia

**Walter Bright** había escrito **Zortech C++ (1987)**, el primer compilador de C++ que generaba código
nativo directamente en vez de traducir a C. Nadie conocía mejor las esquinas del lenguaje ni sus
problemas.

En **1999** empezó **D**: mantener lo bueno de C++ —rendimiento, acceso al sistema, control— y
**quitar la carga histórica**: el preprocesador, la compatibilidad con C a nivel de fuente, los
ficheros de cabecera, las plantillas ilegibles.

Y trajo cosas que en 2001 eran adelantadas:

- **Módulos de verdad**, en lugar de `#include` (clase 149).
- **Pruebas unitarias en el lenguaje**: bloques `unittest` dentro del propio fichero (clase 139).
- **Contratos**: `in`, `out` e `invariant` — la idea de [Ada](ada.md) y Eiffel (clase 118).
- **CTFE (2007)**: ejecutar funciones normales en tiempo de compilación.
- **Arreglos con longitud y rebanadas**, sin la degradación a puntero de C.

Y entonces vino el error que lo marcó: **D2 (2007) rompió la compatibilidad con D1** en medio de la
adopción, y **la biblioteca estándar se partió en dos** —Phobos y Tango— con la comunidad dividida.
Cuando se resolvió, años después, el hueco lo estaban ocupando otros.

> **Es la lección más útil de esta ficha**, y la clase 175 la desarrolla: **la compatibilidad y la
> cohesión del ecosistema pesan más que las características**. [Go](go.md) triunfó con menos
> características y una promesa de compatibilidad que ha cumplido.

## 🏭 Dónde vive hoy

- **Sistemas financieros de baja latencia**: es su nicho más sólido, por el control sobre el
  recolector.
- **Herramientas internas** en empresas que lo adoptaron pronto — Sociomantic (después Dunnhumby) fue
  el caso más conocido.
- **El propio compilador**: DMD está escrito en D desde 2017.
- **Y como lenguaje de sustitución de C++ en proyectos concretos**, con interoperabilidad directa
  (clase 156).

## 🧠 Lo que enseña: metaprogramación legible y contratos

**CTFE — ejecutar el lenguaje al compilar:**

```d
int factorial(int n) pure { return n <= 1 ? 1 : n * factorial(n - 1); }

enum resultado = factorial(10);   // ← calculado EN COMPILACIÓN, con la MISMA función
```

**Y esa es la aportación**: no hay un lenguaje de macros aparte. Una función normal, si es `pure` y
sus argumentos se conocen, **se ejecuta al compilar**. Es lo que C++ tardó hasta `constexpr` (2011)
en tener, y con mucha menos ceremonia.

**Los contratos**, que son la idea de [Ada](ada.md) y de Eiffel (clase 118):

```d
int dividir(int a, int b)
in  { assert(b != 0); }
out (r) { assert(r * b <= a); }
do { return a / b; }
```

**Las pruebas en el propio fichero**, que resuelven un problema real de la clase 139:

```d
unittest {
    assert(dividir(10, 2) == 5);
}
```

**Se compilan solo con `-unittest`**, viven junto al código que prueban y **no hay marco que
instalar**. Es una decisión que muy pocos lenguajes han tomado —[Rust](rust.md) y [Go](go.md) lo
hacen parecido— y que sube muchísimo la probabilidad de que las pruebas existan.

**Y el recolector opcional**, que es la respuesta de D a la tensión de la clase 131:

```d
@nogc void funcionCritica() { /* el compilador PROHÍBE reservar aquí */ }
```

**Se puede tener recolector donde no importa y prohibirlo donde sí**, comprobado por el compilador.

## 🔄 Lo que se ha modernizado

- **`@safe`, `@trusted`, `@system`**: subconjuntos de seguridad de memoria comprobados por el
  compilador. `@safe` prohíbe la aritmética de punteros y las conversiones inseguras — la idea de la
  clase 153 sin cambiar de lenguaje.
- **Comprobación de tiempos de vida** (`@live`), en la línea de [Rust](rust.md).
- **`betterC`**: usar D sin tiempo de ejecución ni recolector, para sistemas embebidos y para
  integrarse en proyectos C.
- **Interoperabilidad con C++** que va mucho más allá de `extern "C"` — llamar a clases y plantillas
  (clase 156).
- **DUB** como gestor de paquetes y sistema de construcción (clase 143).

## ⚙️ Cómo se ejecuta hoy

```bash
dmd -run main.d < entrada.txt        # DMD: compilación rapidísima, para desarrollar
ldc2 -O3 main.d                       # LDC (LLVM): el que hay que usar en producción
dmd -unittest -main -run main.d        # ← ejecutar las pruebas del propio fichero

dub build && dub test                  # con proyecto y dependencias
```

## 🧪 El programa de la clase 041 en D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto v = readln().split().map!(to!double).array;
    const total = v[0] * v[1] * (1 - v[2]);
    writefln("Total: %.2f", total);
}
```

**Lo que hay que ver.**

- **`map!(to!double)`** usa `!` para los **argumentos de plantilla**: `to!double` es la función de
  conversión instanciada para `double`. Es la sintaxis de genéricos de D, mucho más ligera que
  `<...>` de [C++](cpp.md), y **se resuelve en compilación** sin coste.
- **La cadena `readln().split().map!(...).array`** es el estilo de rangos de D — los *ranges* son la
  respuesta de D a los iteradores de C++, y son **perezosos**: nada se calcula hasta el `.array` final
  (clase 115).
- **`const total`** es inmutabilidad real, comprobada por el compilador y **transitiva**: en D,
  `immutable` significa que **nada alcanzable desde ahí puede cambiar** (clase 102), que es más fuerte
  que el `const` de C++.
- **`auto`** infiere el tipo, y el programa **no pierde ni una comprobación** por ello: sigue siendo
  estático y fuerte.
- **Comparado con [C++](cpp.md)**, hace lo mismo en cuatro líneas y con la mitad de ceremonia. Y esa
  comparación, junto con la historia de esta ficha, es exactamente la lección de la clase 164: **ser
  mejor no es suficiente**.

## 📚 Fuentes y bibliografía

- [dlang.org](https://dlang.org/) — especificación, biblioteca Phobos y el tour interactivo.
- [D Language Tour](https://tour.dlang.org/) — la mejor introducción, ejecutable en el navegador.
- **Andrei Alexandrescu**, *The D Programming Language*, Addison-Wesley — el libro de referencia,
  escrito por el codiseñador; también autor de *Modern C++ Design*.
- **Ali Çehreli**, *Programming in D* — libre en línea, muy completo y didáctico.
- [Blog de la D Foundation](https://dlang.org/blog/) — artículos técnicos sobre CTFE, rangos y
  seguridad de memoria.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [C++](cpp.md) · [Nim](nim.md) · [Zig](zig.md) · [Rust](rust.md) · [Ada](ada.md)
