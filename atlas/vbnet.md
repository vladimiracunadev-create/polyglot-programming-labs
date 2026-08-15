# 🟦 VB.NET — 2002

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

VB.NET es el heredero de **Visual Basic**, el lenguaje que más gente ha usado para escribir su primer
programa que hacía algo útil. Su historia contiene una de las rupturas de compatibilidad más
traumáticas que ha vivido un ecosistema — y también la prueba de que **la accesibilidad es una
característica técnica**, no un adorno.

> **🎯 Por qué está en este programa**
>
> VB.NET es un **primo de la familia .NET** ([Atlas](README.md#dotnet)), cuyo representante en el
> núcleo es [C#](csharp.md); y es el pariente moderno de [VBA](vba.md), que sí tiene ficha entre los
> lenguajes vivos.
>
> Aporta al programa dos cosas: **la demostración de que en el CLR el lenguaje es intercambiable**
> —VB.NET y C# compilan al mismo IL y comparten biblioteca (clase 157)— y el **caso de estudio de una
> migración forzada**, VB6 a VB.NET, que la clase 175 usa como advertencia.

| | |
|---|---|
| **Año** | 2002 (VB.NET); **VB1** era de 1991 y **VB6**, de 1998 |
| **Autoría** | Microsoft; VB original inspirado en **QuickBASIC** de Alan Cooper |
| **Familia** | .NET; descendiente de [BASIC](basic.md) por vía de Visual Basic |
| **Paradigma** | Orientado a objetos, imperativo y dirigido por eventos |
| **Tipado** | **Estático**, con `Option Strict Off` opcional que lo relaja |
| **Memoria** | La del CLR: recolección de basura |
| **Ejecución** | Bytecode IL sobre el CLR, con JIT |
| **Estado** | 🟡 **En mantenimiento**: Microsoft no añade características desde 2020 |

---

## 📜 Historia

**Visual Basic (1991)** hizo algo que ningún lenguaje había hecho: **puso el diseñador visual y el
lenguaje juntos**, de forma que alguien sin formación podía arrastrar un botón, hacer doble clic y
escribir lo que debía pasar. Es el modelo que después copió [Delphi](delphi.md) —y lo hizo mejor— y
del que salió toda la programación dirigida por eventos (clase 120).

**Millones de personas escribieron su primer programa útil en VB**, y buena parte del software interno
de las empresas de los noventa está escrito en él. **VB6 (1998)** fue el punto culminante.

Y entonces llegó **.NET (2002)**, y con él **VB.NET** — que **no era compatible con VB6**. El modelo de
objetos cambiaba, los formularios cambiaban, los tipos cambiaban. Había herramientas de migración y
no bastaban.

**La reacción fue una de las mayores rebeliones de usuarios de la historia de Microsoft**: hubo
peticiones firmadas por decenas de miles de desarrolladores pidiendo que se mantuviera VB6, y el
resentimiento duró años. Muchos equipos **no migraron**: se quedaron en VB6 —cuyo tiempo de ejecución
Microsoft siguió soportando en Windows durante dos décadas— o se fueron a otro sitio.

> **Es exactamente la lección de la clase 175 y de la 143**: **una ruptura de compatibilidad
> técnicamente justificada puede costar el ecosistema**. Lo mismo le pasó a [Python](python.md) 2→3
> —doce años de migración—, a [D](d.md) con D2, a [Scala](scala.md) 3 y a
> [Perl](perl.md) con la saga de Perl 6.

En **2020**, Microsoft anunció que **VB.NET seguirá soportado pero ya no evolucionará**: las
características nuevas del lenguaje irán a [C#](csharp.md) y a [F#](fsharp.md).

## 🏭 Dónde vive hoy

- **Aplicaciones internas de empresa** escritas entre 2002 y 2015, muchas todavía en mantenimiento
  activo.
- **Administración pública** en varios países, con aplicaciones de gestión de largo recorrido.
- **Como puente desde [VBA](vba.md)**: quien automatiza Excel reconoce la sintaxis inmediatamente.
- **Y en enseñanza**, en algunos programas de formación profesional.

## 🧠 Lo que enseña: el lenguaje como decisión intercambiable

Este es el punto que hace interesante la ficha (clase 157):

```text
VB.NET, C# y F# compilan al MISMO bytecode (IL).
Comparten:
  - el sistema de tipos común (CTS)
  - la biblioteca de clases base entera
  - el recolector de basura y el modelo de excepciones
  - y las herramientas: depurador, perfilador, gestor de paquetes
```

**Una biblioteca escrita en C# se usa desde VB.NET sin envoltorio, sin conversión y sin fricción** —
lo mismo que ILE en [IBM i](rpg.md) y Language Environment en [z/OS](pl-i.md) (clase 157).

**Y la consecuencia es la de la clase 155**: **en el CLR, elegir lenguaje es una decisión de equipo,
no de arquitectura**. Se pueden mezclar en el mismo sistema, componente a componente.

Y VB.NET tiene una característica propia que merece conocerse:

```vb
Option Strict On       ' ← comprobación estricta: conversiones explícitas obligatorias
Option Strict Off       ' ← permite conversiones implícitas y enlace tardío
```

**El mismo lenguaje, con o sin red.** `Option Strict Off` permite escribir código dinámico al estilo
de VB6 —cómodo y peligroso—, y `On` lo convierte en un lenguaje estático estricto.

**Es tipado gradual por fichero** (clase 146), y la recomendación universal del ecosistema es
**activarlo siempre**, con las excepciones justificadas.

## 🔄 Estado actual

- **Soporte indefinido**, sin características nuevas desde 2020; sigue funcionando en .NET moderno,
  multiplataforma.
- **Interoperabilidad total** con lo que se escriba en C# o F#, que es la vía de modernización
  recomendada: **no migrar el lenguaje, escribir lo nuevo al lado** (clases 150 y 175).
- **Herramientas de conversión** VB.NET → C# que funcionan razonablemente bien, precisamente porque
  el modelo subyacente es el mismo.
- **Y VB6**, que sigue ejecutándose en Windows por compatibilidad, aunque el entorno de desarrollo
  lleve más de veinte años sin soporte.

## ⚙️ Cómo se ejecuta hoy

```bash
dotnet run                            # con un proyecto .vbproj
vbc Venta.vb && ./Venta                # compilador de línea de comandos

dotnet test                            # pruebas (clase 139)
```

## 🧪 El programa de la clase 041 en VB.NET

```vbnet
Imports System.Globalization

Module Venta
    Sub Main()
        Dim v = Console.ReadLine().Split(" "c)
        Dim precio = Double.Parse(v(0), CultureInfo.InvariantCulture)
        Dim cantidad = Double.Parse(v(1), CultureInfo.InvariantCulture)
        Dim descuento = Double.Parse(v(2), CultureInfo.InvariantCulture)
        Console.WriteLine("Total: " & (precio * cantidad * (1 - descuento)).ToString("F2", CultureInfo.InvariantCulture))
    End Sub
End Module
```

**Lo que hay que ver.**

- **La sintaxis con palabras en lugar de símbolos** —`Module`/`End Module`, `Sub`/`End Sub`, `Dim`—
  es la herencia de [BASIC](basic.md), y su motivo es el de la ficha: **legibilidad para quien empieza**.
  Compárese con la versión de [C#](csharp.md), que hace exactamente lo mismo con llaves.
- **`&` es la concatenación de cadenas**, no `+`. Es una decisión de VB para **evitar la ambigüedad**
  de que `"1" + "2"` pueda ser `"12"` o `3` — un problema real en [JavaScript](javascript.md) y
  [PHP](php.md) (clase 100). Es una buena idea que casi nadie copió.
- **`CultureInfo.InvariantCulture`, otra vez**, y por la misma razón que en C# y [Java](java.md): en
  configuración regional española el separador decimal es la coma, y sin esto el programa falla o
  imprime mal. **Es la trampa número uno de .NET.**
- **`Dim v = ...` sin tipo** usa inferencia, no tipado dinámico: con `Option Strict On`, el tipo se
  deduce y se comprueba igual que con `var` en C#.

## 📚 Fuentes y bibliografía

- [Documentación de Visual Basic](https://learn.microsoft.com/dotnet/visual-basic/) — referencia
  oficial, incluido el
  [comunicado de estrategia de 2020](https://devblogs.microsoft.com/vbteam/visual-basic-support-planned-for-net-5-0/),
  que conviene leer como documento de decisión (clase 175).
- [Guía de conversión VB.NET ↔ C#](https://learn.microsoft.com/dotnet/csharp/) — útil para leer código
  de los dos.
- **Michael Halvorson**, *Visual Basic Step by Step*, Microsoft Press — la línea clásica de
  introducción.
- **Anne Boehm, Bryan Syverson**, *Murach's Visual Basic* — orientado a aplicaciones de empresa.
- Y para el contexto histórico: los archivos de la campaña *Save VB6* (2005), que documentan lo que
  cuesta romper la compatibilidad de un ecosistema.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [C#](csharp.md) · [VBA](vba.md) · [BASIC](basic.md) · [Delphi](delphi.md) ·
[F#](fsharp.md)
