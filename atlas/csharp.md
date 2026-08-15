# 🟪 C# — 2000

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

C# nació como la respuesta de Microsoft a [Java](java.md) y acabó adelantándolo en casi todo lo que
significa "características del lenguaje". Es, probablemente, **el lenguaje mayoritario que más rápido
ha incorporado ideas de la investigación**: genéricos reificados, consultas integradas, `async`/`await`
y tipos que distinguen si algo puede ser nulo.

> **🎯 Por qué está en este programa**
>
> **C# es uno de los diez lenguajes del núcleo** y el **representante de la familia .NET**
> ([Atlas](README.md#dotnet)): quien entiende la versión C# de una clase reconoce después
> [F#](fsharp.md) y [VB.NET](vbnet.md), que comparten con él el mismo tiempo de ejecución, la misma
> biblioteca y los mismos tipos.
>
> Y aporta al programa dos cosas que ningún otro del núcleo enseña igual: **los genéricos
> reificados** —los tipos existen en ejecución, a diferencia de Java (clase 108)— y **el origen de
> `async`/`await`**, que C# inventó en 2012 y que hoy está en JavaScript, Python, Rust, Kotlin y
> C++ (clase 134).

| | |
|---|---|
| **Año** | 2000; **2.0** con genéricos (2005); **5.0** con `async` (2012); anual desde 2019 |
| **Autoría** | **Anders Hejlsberg**, Microsoft — antes [Turbo Pascal](pascal.md) y [Delphi](delphi.md) |
| **Familia** | .NET; sintaxis de C, arquitectura influida por Java y por Delphi |
| **Paradigma** | Multiparadigma: OO, funcional, imperativo y —con LINQ— declarativo |
| **Tipado** | **Estático, nominal y fuerte**; genéricos **reificados**; nulabilidad comprobada |
| **Memoria** | Recolección de basura, con `struct` de valor y `Span<T>` sin copia |
| **Ejecución** | Bytecode (**IL**) sobre el CLR, con JIT; también AOT nativo |
| **Estado** | 🟢 **Muy usado**, multiplataforma y de código abierto desde 2016 |

---

## 📜 Historia

Microsoft tenía en los noventa un problema con Java: quería usarlo y quería extenderlo, Sun se opuso,
y de ahí salió **un pleito** y la decisión de hacer una plataforma propia.

En **2000** presentó **.NET** y **C#**, diseñado por **Anders Hejlsberg** — la misma persona que había
hecho Turbo Pascal y Delphi, y que después dirigiría [TypeScript](typescript.md). Esa continuidad se
nota: propiedades, eventos y delegados vienen directamente de Delphi (clase 120).

Y desde el principio hubo una decisión que lo separó de Java y que resultó ser la correcta:
**el CLR se diseñó para varios lenguajes**, con un sistema de tipos común. Por eso
[VB.NET](vbnet.md), [F#](fsharp.md) y C# comparten biblioteca e interoperan sin fricción — que es lo
que la clase 157 llama **ABI definido por la plataforma**, igual que ILE en [IBM i](rpg.md).

Los hitos:

- **C# 2.0 (2005)**: **genéricos reificados** —el CLR los conoce en ejecución, a diferencia del
  borrado de Java— y métodos anónimos.
- **C# 3.0 (2007)**: **LINQ**, expresiones lambda, tipos anónimos, `var`, métodos de extensión. LINQ
  llevó las consultas al lenguaje, con comprobación de tipos (clase 170).
- **C# 5.0 (2012)**: **`async`/`await`**. Es la aportación más influyente de C# a la industria
  (clase 134).
- **2016**: **.NET Core** — multiplataforma, de código abierto y sin dependencia de Windows. El giro
  que salvó a la plataforma.
- **C# 8 (2019)**: **tipos de referencia nulables**, que separan `string` de `string?` y hacen
  comprobable el error del billón de dólares.
- **C# 9-13**: registros, emparejamiento de patrones, `init`, programas de nivel superior,
  `required`, colecciones literales.

## 🏭 Dónde vive hoy

- **Software empresarial en Windows y, cada vez más, en Linux**: ASP.NET Core mueve una parte grande
  de la web corporativa.
- **Videojuegos**: **Unity** usa C# como lenguaje de guion; es probablemente el mayor volumen de C#
  escrito por número de personas.
- **Aplicaciones de escritorio**: WPF, WinUI y MAUI — el nicho que en su día ocupó
  [Delphi](delphi.md).
- **Servicios en la nube**: Azure Functions, servicios de fondo, integraciones.
- **Herramientas y automatización**: PowerShell está construido sobre .NET (ficha
  [PowerShell](powershell.md)).

## 🧠 Lo que enseña y no enseña ningún otro del núcleo

**Uno, genéricos reificados** (clase 108). En Java, `List<String>` y `List<Integer>` **son el mismo
tipo en ejecución**: los genéricos se borran. En C#, no:

```csharp
var lista = new List<string>();
Console.WriteLine(lista.GetType());        // System.Collections.Generic.List`1[System.String]
```

**El CLR conoce el argumento de tipo**, así que se puede preguntar por él, serializar con él y
especializar el código para `List<int>` sin boxing — lo que tiene consecuencias directas de
rendimiento (clase 128).

**Dos, el origen de `async`/`await`** (clase 134). C# lo introdujo en 2012 sobre la máquina de estados
que el compilador genera, y **de ahí lo copiaron casi todos**: TypeScript, Python, Rust, Kotlin, Swift
y C++20.

**Y tres, LINQ**, que es la respuesta más elegante que existe al desajuste de impedancia de la clase
170:

```csharp
var caros = from p in productos
            where p.Precio > 100
            orderby p.Nombre
            select new { p.Nombre, p.Precio };
```

**Esa consulta se comprueba en compilación**, y **se puede traducir a SQL** por un proveedor —Entity
Framework— o ejecutarse en memoria. Es la misma idea que las consultas como estructura de
[Lisp](common-lisp.md) y que `sqlpp11` en [C++](cpp.md): **la consulta es un árbol tipado, no una
cadena** (clase 153).

## 🔄 Lo que se ha modernizado

- **Multiplataforma y de código abierto**: .NET 8/9/10 corren en Linux, macOS, ARM y contenedores.
- **AOT nativo**: binario sin máquina virtual, con arranque de milisegundos y una imagen mínima
  (clase 174) — la respuesta al problema de arranque de las plataformas gestionadas.
- **`Span<T>` y `Memory<T>`**: trabajar con memoria **sin copiar y sin recolector**, lo que ha llevado
  a C# a competir en escenarios de baja latencia (clase 152).
- **Tipos nulables comprobados**, registros y emparejamiento de patrones — la influencia de
  [F#](fsharp.md) sobre su hermano.
- **Interoperabilidad moderna**: `LibraryImport` con generación de código en vez de reflexión, y
  punteros de función (clase 156).

## ⚙️ Cómo se ejecuta hoy

```bash
dotnet run < entrada.txt                    # el comando de la clase 041
dotnet build -c Release
dotnet publish -c Release -p:PublishAot=true    # binario nativo (clase 174)

dotnet format && dotnet test                 # calidad y pruebas (clases 139 y 146)
```

## 🧪 El programa de la clase 041 en C\#

```csharp
using System;
using System.Globalization;

// C# sobre el CLR: tipado estático con cultura invariante para el formato.
string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);

double precioUnitario = double.Parse(p[0], CultureInfo.InvariantCulture);
int cantidad = int.Parse(p[1], CultureInfo.InvariantCulture);
double descuento = double.Parse(p[2], CultureInfo.InvariantCulture);

double subtotal = precioUnitario * cantidad;
double total = subtotal * (1 - descuento);

Console.WriteLine("Total: " + total.ToString("F2", CultureInfo.InvariantCulture));
```

**Lo que hay que ver.**

- **No hay `class Program` ni `static void Main`.** Son los *programas de nivel superior* de C# 9: la
  misma ceremonia que [Java](java.md) exige, eliminada. La comparación entre los dos fragmentos es la
  historia de veinte años de evolución.
- **`CultureInfo.InvariantCulture` aparece cuatro veces, y no sobra ninguna.** En una máquina con
  configuración española, `double.Parse("15000.0")` **falla** —espera coma— y `ToString("F2")`
  imprimiría `27000,00`. Es la trampa clásica de .NET, y la misma que `Locale.US` en Java.
- **`int` y `double` son alias de `System.Int32` y `System.Double`**: en C#, a diferencia de Java,
  **los primitivos también son tipos del sistema de tipos**, así que `5.ToString()` es válido.
- **`ReadToEnd` en lugar de leer una línea** es una decisión deliberada del ejemplo: hace el programa
  robusto ante la forma en que llegue la entrada, que es lo que el contrato de la clase 040 exige.

## 📚 Fuentes y bibliografía

- [Documentación de C# y .NET](https://learn.microsoft.com/dotnet/csharp/) — y las
  [notas de versión del lenguaje](https://learn.microsoft.com/dotnet/csharp/whats-new/), que explican
  cada característica con su motivación.
- [Propuestas del lenguaje (GitHub)](https://github.com/dotnet/csharplang) — el diseño en abierto.
- **Jon Skeet**, *C# in Depth*, 4.ª ed., Manning — el libro que explica **por qué** el lenguaje es como
  es; imprescindible para genéricos, `async` y LINQ.
- **Joseph Albahari**, *C# 12 in a Nutshell*, O'Reilly — la referencia completa, actualizada cada año.
- **Andrew Troelsen, Phil Japikse**, *Pro C# with .NET* — cobertura amplia de la plataforma.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [F#](fsharp.md) · [VB.NET](vbnet.md) · [Java](java.md) · [Delphi](delphi.md) ·
[TypeScript](typescript.md)
