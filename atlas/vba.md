# 📊 VBA — 1993

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**Probablemente el entorno de programación más usado del mundo, y casi nadie lo llama programar.**
Cada departamento financiero, cada área de control de gestión y cada oficina técnica tiene hojas de
Excel con macros. Ese código mueve presupuestos, cierres contables y decisiones de inversión, y lo
escribió alguien cuyo puesto no dice "desarrollador".

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: VBA viene instalado con Microsoft Office y Microsoft mantiene su
> documentación de referencia del lenguaje y del modelo de objetos.** No está obsoleto ni
> descatalogado: la base instalada es sencillamente demasiado grande. Las alternativas modernas
> —Office Scripts en TypeScript, Power Automate, Python en Excel— se han **añadido**, no lo han
> sustituido.
>
> Entra por dos motivos. El primero es el mismo que [AutoLISP](autolisp.md): es el ejemplo canónico
> de **lenguaje incrustado en una aplicación anfitriona**, donde la biblioteca estándar es el
> **modelo de objetos** del programa que lo hospeda. El segundo es más sutil y más valioso: VBA es
> donde millones de personas descubren que **una hoja de cálculo es un programa**. Toda la
> [Parte 0](../classes/parte-0-pensamiento-computacional-y-el-metodo-poliglota/README.md) —qué es un
> algoritmo, qué es el estado, por qué importa la reproducibilidad— se juega ahí con consecuencias
> económicas reales, y ese es un contexto que ningún ejemplo de laboratorio iguala.

| | |
|---|---|
| **Año** | 1993, con Excel 5.0; **VBA 7** (con soporte de 64 bits) desde Office 2010 |
| **Autoría** | **Microsoft**, derivado de **Visual Basic** (1991) y este de QuickBASIC |
| **Familia** | BASIC |
| **Paradigma** | Imperativo y procedimental, con objetos **COM** |
| **Tipado** | Estático opcional (`Option Explicit`) y dinámico por defecto vía `Variant` |
| **Memoria** | Conteo de referencias de COM |
| **Ejecución** | **Interpretado dentro del anfitrión** (Excel, Word, Access, Outlook…) |
| **Estado** | 🟢 **Base instalada enorme** — finanzas, administración, ingeniería, informes |

---

## 📜 Historia

**Visual Basic 1.0** salió en 1991 y su idea fue revolucionaria en su momento: construir la interfaz
arrastrando controles y escribir el código detrás de los eventos. En **1993**, Microsoft incrustó el
motor de ese lenguaje dentro de **Excel 5.0** con el nombre de **Visual Basic for Applications**, para
sustituir al viejo lenguaje de macros XLM. La jugada era estratégica: si las empresas escribían sus
procesos en VBA, migrar de Office a otra suite se volvía muy caro.

Funcionó. VBA se extendió a Word, Access, PowerPoint, Outlook y Visio, y Microsoft lo licenció a
terceros: **AutoCAD**, **SolidWorks**, **CorelDRAW**, **ArcGIS** y muchas otras aplicaciones lo
incorporaron como su lenguaje de automatización.

Los años 2000 trajeron las **macros maliciosas**: los virus de documento (Melissa, ILOVEYOU y
descendientes) explotaron que abrir un fichero podía ejecutar código. La respuesta fue el modelo de
seguridad actual —macros deshabilitadas por defecto, extensiones `.xlsm` frente a `.xlsx`, firma
digital y **bloqueo automático de macros en ficheros descargados de Internet**—. Es un contexto que
hay que conocer antes de escribir la primera línea.

Con .NET, Microsoft intentó reemplazarlo: **VSTO** y **Visual Studio Tools for Office** apuntaban a
que las soluciones Office se escribieran en C# o VB.NET. Nunca desplazó a VBA, porque VBA tiene una
ventaja imbatible: **está ya instalado, no requiere permisos de administrador y se abre con Alt+F11**.
En una empresa con equipos bloqueados, eso lo decide todo.

**El estado real, sin adornos:** el lenguaje está **congelado** en VBA 7.1. No recibe características
nuevas. Microsoft ha declarado que sigue soportado y ha ido añadiendo alternativas —**Office
Scripts** (TypeScript, solo en Excel para web y escritorio con Microsoft 365), **Power Automate**,
**Python en Excel**— pero ninguna cubre todavía lo que VBA cubre en escritorio y en las aplicaciones
de terceros que lo licenciaron.

## 🏭 Dónde sobrevive hoy

- **Finanzas y control de gestión**: modelos de valoración, consolidación, presupuestos, cierres
  mensuales, informes regulatorios.
- **Administración y operaciones**: automatización de informes, conciliaciones, cruces de ficheros,
  generación masiva de documentos en Word desde datos de Excel.
- **Ingeniería y diseño**: macros en AutoCAD, SolidWorks e Inventor para automatizar tareas
  repetitivas y generar listas de materiales.
- **Access**: aplicaciones departamentales completas —formularios, informes, lógica— que en muchas
  organizaciones siguen siendo el sistema real de un área.
- **Ciencia de laboratorio y análisis**: instrumentación que exporta a Excel y se procesa con macros.

## 🧠 Por qué no ha muerto

**1. Está donde están los datos y no hay que instalar nada.** Es el argumento decisivo. Un analista
financiero puede pulsar Alt+F11 y automatizar su trabajo esta misma tarde, sin pedir permiso a nadie.
Ninguna alternativa moderna iguala esa fricción cero.

**2. El modelo de objetos de Office es enorme y muy estable.** `Range`, `Worksheet`, `PivotTable`,
`Chart`, `Document`, `MailItem`: décadas de API que casi no ha cambiado. Código de 2002 sigue
funcionando.

**3. Los volúmenes acumulados son gigantescos.** Y son **invisibles**: no están en repositorios, no
tienen pruebas, no pasan por revisión. Están dentro de ficheros `.xlsm` en carpetas compartidas. Nadie
puede siquiera inventariarlos, y mucho menos migrarlos.

**4. `Currency`: un tipo decimal exacto, integrado.** Es un entero de 64 bits escalado con cuatro
decimales fijos. Para dinero es exacto, igual que el `COMP-3` de [COBOL](cobol.md), y evita el error
clásico de acumular céntimos en punto flotante.

**5. Las alternativas tienen huecos reales.** Office Scripts no llega a todas las plataformas ni a
todo el modelo de objetos; Python en Excel se ejecuta en la nube y no automatiza la interfaz; ninguna
de las dos sirve para AutoCAD o SolidWorks.

> **⚠️ Un aviso, porque este es el único lenguaje de la lista con implicaciones de seguridad**
>
> Las macros de VBA son el vector histórico número uno de compromiso vía documento. Reglas prácticas:
> **nunca habilites macros de un fichero cuyo origen no controles**; mantén el bloqueo de macros en
> ficheros procedentes de Internet; **firma digitalmente** las tuyas y usa ubicaciones de confianza;
> y no confundas "esta hoja funciona" con "esta hoja es segura". Aprender VBA incluye aprender esto.

## 🔄 Lo que se ha modernizado

Del lenguaje, poco; **de su entorno, bastante**:

- **VBA 7 con 64 bits.** Las declaraciones de API externas necesitan `PtrSafe` y el tipo `LongPtr`, y
  la compilación condicional `#If VBA7 Then` permite que el mismo código funcione en Office de 32 y
  64 bits. Es el cambio que rompió miles de macros heredadas.
- **Convivencia con lo nuevo**: desde VBA se pueden consumir APIs REST (`MSXML2.XMLHTTP` o
  `WinHttpRequest`) y analizar JSON con bibliotecas de la comunidad, así que una macro puede hablar
  con un servicio moderno.
- **Power Query y el modelo de datos** absorbieron gran parte de lo que antes se hacía con macros de
  transformación: hoy, mucho del trabajo de limpieza no necesita VBA.
- **Office Scripts** (TypeScript) para escenarios web y automatización con Power Automate, y
  **Python en Excel** para análisis y visualización, ejecutado en la nube de Microsoft.
- **Herramientas de ingeniería sobre VBA**: **Rubberduck**, un complemento libre que añade
  refactorizaciones, análisis de código y **pruebas unitarias** al editor de VBA; y exportar los
  módulos a ficheros `.bas`/`.cls` permite versionarlos en Git.

El consejo práctico hoy: **mantener VBA para automatizar la aplicación de escritorio y las
aplicaciones de terceros; usar Power Query, Office Scripts o Python para transformar datos.**

## ⚙️ Cómo se ejecuta hoy

VBA **solo** existe dentro de su anfitrión. No hay intérprete de línea de comandos ni ejecutable.

```text
1. Abre Excel (o Word, Access, AutoCAD…)
2. Pulsa Alt + F11 para abrir el editor (VBE)
3. Insertar → Módulo
4. Escribe el código y pulsa F5, o llámalo desde una celda
5. Guarda el fichero como .xlsm (habilitado para macros)
```

**Herramientas:** el **VBE** integrado (que no ha cambiado desde 1998, con su Ventana Inmediato como
REPL rudimentario y su Ventana Locales como inspector), y **Rubberduck** como complemento
imprescindible para trabajar en serio. Para versionar, exportar los módulos a `.bas` y `.cls`.

## 🧪 El programa de la clase 041 en VBA

> ⚠️ **Contrato adaptado, y declarado.** VBA no tiene `stdin` ni `stdout`: su entrada son las celdas y
> el usuario, y su salida son las celdas, la Ventana Inmediato o un cuadro de diálogo. El cálculo es
> el mismo; la forma de entrar y salir es la del anfitrión. **No se verifica en CI**: requiere una
> instalación de Office.

```vba
Option Explicit

' Versión 1: un procedimiento que lee y escribe en la hoja.
Public Sub CalcularTotalVenta()
    Dim precio    As Currency
    Dim cantidad  As Double
    Dim descuento As Double
    Dim total     As Currency

    With ThisWorkbook.Worksheets("Ventas")
        precio    = .Range("A2").Value
        cantidad  = .Range("B2").Value
        descuento = .Range("C2").Value

        total = precio * cantidad * (1 - descuento)

        .Range("D2").Value = total
    End With

    Debug.Print "Total: " & Format(total, "0.00")
End Sub

' Versión 2: una FUNCIÓN DE HOJA. Esto es lo que hace único a VBA.
Public Function TOTALVENTA(precio As Currency, _
                           cantidad As Double, _
                           descuento As Double) As Currency
    TOTALVENTA = precio * cantidad * (1 - descuento)
End Function
```

**Recorrido, línea a línea.**

- `Option Explicit` **debe ser la primera línea de todo módulo**. Sin ella, VBA crea variables nuevas
  al vuelo cuando encuentra un nombre desconocido: un `cantiadd` mal tecleado se convierte en un
  `Variant` vacío con valor 0, el cálculo da cero y **no hay ningún error**. Es el mismo problema que
  `implicit none` resuelve en [Fortran](fortran.md) y `use strict` en [Perl](perl.md), y es la causa
  documentada de errores millonarios en modelos financieros.
- `Dim precio As Currency` — **`Currency` es el detalle importante.** Es un entero de 64 bits con
  cuatro decimales fijos, es decir, **aritmética decimal exacta**. `Double` sería punto flotante
  binario y acumularía error al sumar miles de importes. La regla es la misma de siempre: dinero en
  decimal, magnitudes físicas en flotante. VBA tiene el tipo correcto y casi nadie lo usa.
- `With ... End With` fija un objeto y permite escribir `.Range(...)` con el punto inicial. No es solo
  estética: cada acceso a la hoja cruza la frontera COM entre VBA y Excel y **es caro**. Reducir esos
  cruces es la primera regla de rendimiento en VBA, y es un caso muy concreto de la
  [Parte 10](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md): el coste
  de atravesar la frontera entre dos mundos.
- `ThisWorkbook.Worksheets("Ventas").Range("A2")` es el **modelo de objetos**: libro → hoja → rango.
  Aprender VBA es, en su mayor parte, aprender ese árbol. `ActiveSheet` y `Selection` también
  existen, y usarlos es la mala práctica más extendida del lenguaje: hacen que la macro dependa de
  dónde estaba el cursor.
- `Debug.Print` escribe en la **Ventana Inmediato** (Ctrl+G), que es el `print` de depuración.
- `Format(total, "0.00")` formatea. Ojo: `Format` **depende de la configuración regional**, así que en
  un equipo con coma decimal produce `27000,00`. Para salida estable conviene `Format$` con máscaras
  explícitas o construir la cadena a mano.
- El guion bajo `_` al final de línea es la **continuación de línea**.

**Y la versión 2 es la que hay que entender.** Al declarar una `Public Function` en un módulo estándar,
esa función **aparece en la lista de fórmulas de Excel**. En cualquier celda se puede escribir:

```text
=TOTALVENTA(A2; B2; C2)
```

Acabas de **extender el lenguaje de fórmulas de la hoja de cálculo** con una función propia, que se
recalcula sola cuando cambian sus argumentos. Eso es una *UDF* (*User Defined Function*), y es el
puente exacto entre "usuario de Excel" y "programador": la hoja pasa de ser una tabla a ser un
lenguaje al que le has añadido una primitiva.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En VBA es… |
|---|---|
| `let x = 5` | `Dim x As Long` … `x = 5` |
| `def f(a):` sin retorno | `Sub f(a) ... End Sub` |
| `def f(a):` con retorno | `Function f(a) As Tipo` … `f = valor` … `End Function` |
| `return valor` | Asignar al **nombre de la función**: `f = valor` |
| `decimal` / `BigDecimal` | `Currency` (4 decimales) o `Decimal` dentro de un `Variant` |
| `any` / tipado dinámico | `Variant` — el tipo por defecto si no declaras |
| `null` | `Empty`, `Null`, `Nothing` y `vbNullString`: **cuatro cosas distintas** |
| `for x in lista` | `For Each x In coleccion ... Next x` |
| `try / catch` | `On Error GoTo Manejador` — manejo de errores por salto, no por bloque |
| `print(x)` | `Debug.Print x` (Inmediato) o `MsgBox x` (cuadro de diálogo) |
| `import` | Referencias del proyecto (Herramientas → Referencias) |
| Objeto | Objeto COM, creado con `New` o `CreateObject("...")` |

## ⚠️ Errores comunes al leerlo

- **Falta `Option Explicit`.** Si no está, desconfía de todo lo demás.
- **`Select` y `Activate` por todas partes.** El grabador de macros genera código que selecciona
  celdas antes de tocarlas. Es lento y frágil; el código correcto trabaja con referencias directas a
  `Range` sin seleccionar nada.
- **`Double` para dinero.** Error de dominio con consecuencias contables.
- **Confundir `Empty`, `Null` y `Nothing`.** `Empty` es una variable sin inicializar, `Null` es un
  valor ausente de base de datos, `Nothing` es una referencia de objeto sin asignar. `IsEmpty`,
  `IsNull` e `Is Nothing` son las tres pruebas, y no son intercambiables.
- **Olvidar `Set` al asignar objetos.** `Set hoja = Worksheets(1)` lleva `Set`; `x = 5` no. Omitirlo
  da el error 91, el más frecuente del lenguaje.
- **`On Error Resume Next` como red general.** Silencia todos los errores, incluidos los que
  indicaban que el resultado es incorrecto. Se usa para casos puntuales y se desactiva de inmediato
  con `On Error GoTo 0`.
- **Suponer que el índice empieza en 0.** Los arrays de VBA empiezan en **1** si hay `Option Base 1`,
  en 0 si no, y `Range.Value` devuelve un array **de base 1** en ambos casos. Usa siempre `LBound` y
  `UBound`.

## 📚 Fuentes y bibliografía

- [Referencia del lenguaje VBA (Microsoft Learn)](https://learn.microsoft.com/office/vba/api/overview/language-reference)
  — la documentación oficial vigente del lenguaje.
- [Modelo de objetos de Excel (Microsoft Learn)](https://learn.microsoft.com/office/vba/api/overview/excel/object-model)
  — el árbol de objetos que constituye, en la práctica, la biblioteca estándar.
- [Bloqueo de macros en ficheros de Internet](https://learn.microsoft.com/deployoffice/security/internet-macros-blocked)
  — la política de seguridad actual; léela antes de distribuir nada.
- [Rubberduck VBA](https://rubberduckvba.com/) — refactorizaciones, análisis de código y pruebas
  unitarias dentro del editor de VBA. Cambia por completo la experiencia.
- **Rob Bovey, Dennis Wallentin, Stephen Bullen, John Green**, *Professional Excel Development*,
  2.ª ed., Addison-Wesley — el único libro que trata Excel + VBA como ingeniería de software seria:
  arquitectura, distribución, rendimiento y errores.
- **Chip Pearson**, [cpearson.com](http://www.cpearson.com/excel/topic.aspx) — archivo de referencia
  técnica sobre el modelo de objetos y sus rincones.
- **European Spreadsheet Risks Interest Group**, [eusprig.org](https://eusprig.org/) — recopilación de
  errores documentados en hojas de cálculo y sus consecuencias. Lectura obligada para entender por
  qué el rigor importa aquí tanto como en cualquier otro sitio.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [AutoLISP](autolisp.md) · [Delphi / Object Pascal](delphi.md) · [COBOL](cobol.md)
