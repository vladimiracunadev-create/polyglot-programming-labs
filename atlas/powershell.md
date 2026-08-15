# 🔷 PowerShell — 2006

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

PowerShell parte de una idea que replantea cincuenta años de tradición Unix: **¿y si por las tuberías
viajaran objetos en lugar de texto?** El resultado elimina de un golpe el análisis con expresiones
regulares que domina el trabajo en [Bash](bash.md) — y trae sus propias asperezas.

> **🎯 Por qué está en este programa**
>
> PowerShell es un **primo de la familia históricos / shell** ([Atlas](README.md#historicos-shell)),
> junto a [Bash](bash.md) y [JCL](jcl.md).
>
> Aporta al programa **la alternativa al contrato de texto**
> ([clases 159 y 161](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md)):
> una tubería con datos estructurados y tipados, en lugar de con cadenas que hay que volver a
> analizar. Es la mejor demostración de que **el formato de la frontera decide el trabajo que hay que
> hacer en los dos lados**.

| | |
|---|---|
| **Año** | 2006; **PowerShell Core 6** multiplataforma y libre (2018); **7.x** actual |
| **Autoría** | **Jeffrey Snover**, Microsoft — a partir del *Monad Manifesto* (2002) |
| **Familia** | Históricos / shell; sobre **.NET** ([C#](csharp.md)) |
| **Paradigma** | Imperativo y de canalización, **orientado a objetos** |
| **Tipado** | **Dinámico con tipos de .NET**; con anotaciones opcionales |
| **Memoria** | La del CLR: recolección de basura |
| **Ejecución** | Interpretado sobre .NET, con compilación a IL de los bloques de guion |
| **Estado** | 🟢 **Estándar** en administración de Windows, Azure y Microsoft 365 |

---

## 📜 Historia

En **2002**, **Jeffrey Snover** escribió el ***Monad Manifesto***, un documento que empieza con un
diagnóstico incómodo para Microsoft: **la administración de Windows por interfaz gráfica no escala**, y
**el modelo de Unix —herramientas de texto compuestas por tuberías— no se puede copiar directamente**.

Y la razón que daba es interesante: **en Unix, la configuración está en ficheros de texto**, así que
`grep` y `sed` bastan. **En Windows, la configuración está en el registro, en WMI y en APIs de
objetos**, y convertir eso a texto para volver a analizarlo **pierde información y es frágil**.

Su propuesta fue **cambiar lo que viaja por la tubería**:

```powershell
Get-Process | Where-Object CPU -gt 100 | Sort-Object CPU -Descending | Select-Object -First 5
```

**Ahí no viaja texto: viajan objetos `Process`**, con sus propiedades y sus métodos. **No hay que
analizar nada**, porque `CPU` es un número y no una columna que haya que extraer.

**PowerShell 1.0 salió en 2006**, y su adopción fue lenta hasta que Microsoft tomó una decisión
estratégica: **exigir que todo producto de servidor expusiera su funcionalidad como cmdlets**, y que
**la interfaz gráfica se construyera encima**. Exchange fue el primero.

**En 2016 se abrió el código y en 2018 llegó PowerShell Core**, multiplataforma sobre .NET Core — que
lo llevó a Linux y a macOS.

## 🏭 Dónde vive hoy

- **Administración de Windows**: es la forma estándar; el Administrador de Servidor genera PowerShell.
- **Azure y Microsoft 365**: `Az` y `Microsoft.Graph` son la vía de automatización.
- **Integración continua y despliegue**: pasos de canalización en Azure DevOps y GitHub Actions
  (clases 147 y 171).
- **Gestión de configuración**: DSC (*Desired State Configuration*) — el modelo declarativo de estado
  deseado que la clase 171 recomienda.
- **Y en Linux**, sobre todo en entornos mixtos y para gestionar servicios de Microsoft.

## 🧠 Lo que enseña: objetos por la tubería

**La comparación con [Bash](bash.md) es el contenido de esta ficha:**

```bash
# Bash: TODO es texto, hay que extraer columnas y confiar en el formato
ps aux | awk '$3 > 50 {print $11}' | sort | head -5
```

```powershell
# PowerShell: viajan objetos, se accede a propiedades con nombre
Get-Process | Where-Object CPU -gt 50 | Select-Object -First 5 -Property Name
```

**Y las diferencias son de fondo:**

| | Texto ([Bash](bash.md)) | Objetos (PowerShell) |
|---|---|---|
| Extraer un dato | **analizar** con `awk`, `cut`, `sed` | acceder a la propiedad |
| Si cambia el formato | **se rompe en silencio** | no hay formato que cambiar |
| Tipos | todo cadena; convertir a mano | `DateTime`, `Int`, `FileInfo`… |
| Interoperabilidad | **universal**: cualquier programa | dentro del ecosistema .NET |
| Rendimiento | procesos ligeros, texto barato | objetos y CLR: más pesado |

**Y las dos últimas filas son el precio.** El contrato de texto de Unix es **universal**: cualquier
programa, en cualquier lenguaje, de cualquier época, participa (clase 161). **Los objetos de
PowerShell solo los entiende PowerShell** — y al llamar a `git` o a `docker`, **vuelve el texto**.

Es exactamente la tensión de la clase 159: **el formato que captura más información es el que menos
gente entiende**.

**Y hay una segunda cosa que PowerShell hace notablemente bien: la coherencia.**

```powershell
Get-Process   Get-Service   Get-ChildItem   Get-Content
Set-Location  Remove-Item   New-Item        Start-Service
```

**Todos los comandos son `Verbo-Sustantivo`**, con una **lista aprobada de verbos**. Eso significa que
**se puede adivinar el nombre de un comando que no se conoce** — y `Get-Verb` la lista.

Es la misma virtud que la clase 167 señalaba en los comandos CL de [IBM i](rpg.md): **la consistencia
hace que aprender uno sea aprender todos**, frente a la libertad total de Unix donde cada herramienta
inventa sus opciones.

## 🔄 Lo que se ha modernizado

- **PowerShell 7**: multiplataforma, con `&&` y `||`, operador ternario, `??` y paralelismo en
  `ForEach-Object -Parallel`.
- **PSScriptAnalyzer**: análisis estático con reglas, al estilo de la clase 146.
- **Pester**: marco de pruebas maduro para guiones (clase 139).
- **`SecretManagement`**: gestión de credenciales sin ponerlas en el guion (clase 153).
- **Clases y enumerados** en el lenguaje, y módulos con manifiesto y versión (clase 143).
- **Y `ConvertTo-Json` / `ConvertFrom-Json`**, que son el puente al mundo del texto estructurado
  (clase 159).

## ⚙️ Cómo se ejecuta hoy

```powershell
pwsh main.ps1                              # PowerShell 7, multiplataforma
powershell.exe -File main.ps1               # Windows PowerShell 5.1

Invoke-ScriptAnalyzer -Path main.ps1        # análisis (clase 146)
Invoke-Pester                                # pruebas (clase 139)
```

## 🧪 El programa de la clase 041 en PowerShell

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```powershell
$campos = ($input | Select-Object -First 1) -split '\s+'

[double]$precio    = $campos[0]
[double]$cantidad  = $campos[1]
[double]$descuento = $campos[2]

$total = $precio * $cantidad * (1 - $descuento)

'Total: {0:F2}' -f $total
```

**Lo que hay que ver.**

- **`[double]$precio` es una conversión con tipo**, no una anotación: PowerShell **convierte y
  comprueba**, y falla si no puede. Es tipado dinámico **con los tipos de .NET** disponibles.
- **`-split '\s+'` usa una expresión regular** y devuelve **un arreglo de verdad**, no una cadena que
  haya que volver a partir.
- **`-f` es el operador de formato**, y `{0:F2}` es el formato de .NET — **el mismo `F2` que en
  [C#](csharp.md) y [VB.NET](vbnet.md)** (clase 157). Y con la misma advertencia: **la cultura
  regional afecta al separador decimal**, así que en un guion serio conviene fijarla.
- **La última línea no lleva `Write-Output`**: **el resultado de una expresión suelta va a la
  tubería**. Es una decisión del lenguaje que ahorra ceremonia y que despista al principio.
- **Y este programa es lo menos representativo de PowerShell posible**: su terreno no es leer texto de
  la entrada estándar, sino **componer cmdlets que devuelven objetos**. Es un **contrato adaptado**
  (clase 040).

## 📚 Fuentes y bibliografía

- [Documentación de PowerShell](https://learn.microsoft.com/powershell/) — extensa; y `Get-Help` con
  `-Examples` dentro del propio shell.
- **Jeffrey Snover**, *Monad Manifesto* (2002) — libre en línea; **el documento de diseño**, y una
  lectura excelente para la clase 175: plantea el problema, descarta alternativas y justifica la
  decisión.
- **Don Jones, Jeffery Hicks**, *Learn PowerShell in a Month of Lunches*, Manning — la introducción de
  referencia.
- **Bruce Payette, Richard Siddaway**, *Windows PowerShell in Action*, 3.ª ed., Manning — escrito por
  uno de los diseñadores del lenguaje; el más profundo.
- [PSScriptAnalyzer](https://github.com/PowerShell/PSScriptAnalyzer) y
  [Pester](https://pester.dev/) — calidad y pruebas.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Bash](bash.md) · [C#](csharp.md) · [Tcl](tcl.md) · [JCL](jcl.md) · [Perl](perl.md)
