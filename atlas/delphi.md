# 🏗️ Delphi / Object Pascal — 1995

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**Está más vivo de lo que parece.** Miles de aplicaciones de escritorio que usan empresas todos los
días —terminales de punto de venta, gestión de almacén, laboratorios, software industrial, ERP
regionales— son ejecutables de Delphi. No se ven porque nadie las publica en GitHub: se venden a
clientes que llevan veinte años usándolas.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: Delphi es un producto comercial en desarrollo activo.** Embarcadero
> publica versiones nuevas con regularidad —**Delphi 13 Community Edition** salió en agosto de
> 2026— y su alternativa libre, **Free Pascal + Lazarus**, tiene desarrollo continuo. No es un
> lenguaje que sobreviva por inercia: es uno que se factura.
>
> Entra porque **es el mejor ejemplo vivo de un modelo que el núcleo no cubre**: la
> **construcción visual de aplicaciones (RAD)** sobre un **modelo de componentes con propiedades,
> eventos y publicación de metadatos**. La VCL de Delphi es el antepasado directo de Windows Forms y
> de la arquitectura de propiedades de C# — no por parecido, sino por autoría: **Anders Hejlsberg
> diseñó los dos**. Cuando en C# escribes `public string Nombre { get; set; }` o suscribes un evento
> con `+=`, estás usando ideas que se probaron primero aquí. Y muestra un segundo concepto que
> importa: la **compilación a un único ejecutable nativo sin runtime**, que es exactamente el debate
> que Go reabrió veinte años después.

| | |
|---|---|
| **Año** | **Turbo Pascal** 1983; **Delphi 1** en febrero de 1995 |
| **Autoría** | **Anders Hejlsberg** y el equipo de **Borland** — después CodeGear, Embarcadero, Idera |
| **Familia** | [Pascal](pascal.md) — Object Pascal es su dialecto orientado a objetos |
| **Paradigma** | Imperativo y **orientado a objetos**, con componentes y eventos |
| **Tipado** | **Estático y fuerte**, con genéricos e inferencia parcial |
| **Memoria** | Manual (`Create`/`Free`) con conteo de referencias para interfaces y cadenas; ARC en móvil |
| **Ejecución** | **Compilado a nativo**: un único `.exe` sin máquina virtual |
| **Estado** | 🟢 **Más vivo de lo que parece** — escritorio empresarial, TPV, industria, ERP |

---

## 📜 Historia

En 1983, un joven danés llamado **Anders Hejlsberg** vendió a Borland un compilador de
[Pascal](pascal.md) que había escrito para CP/M. Se publicó como **Turbo Pascal** por 49,95 dólares
—frente a los cientos que costaban los compiladores serios de la época— y cambió el mercado. Cabía en
un disquete, integraba editor y compilador en un solo programa y compilaba en segundos cuando lo
normal era esperar minutos.

En **febrero de 1995** Borland lanzó **Delphi 1**, para Windows 3.1. Su aportación fue el
**desarrollo rápido de aplicaciones (RAD)** llevado a un lenguaje compilado a nativo: arrastras
controles a un formulario, ajustas sus propiedades en un inspector, haces doble clic para escribir el
manejador del evento, y compilas un **`.exe` único que no necesita instalar nada**. Visual Basic hacía
lo primero pero era interpretado y dependía de runtime; C++ compilaba a nativo pero exigía un
esfuerzo enorme para la interfaz. Delphi hizo las dos cosas.

La pieza clave era la **VCL** (*Visual Component Library*), y para que funcionara Hejlsberg tuvo que
añadir al lenguaje algo que no existía: **propiedades** (campos con `read`/`write` que parecen datos
pero ejecutan métodos), **eventos** como punteros a método asignables, y **RTTI publicada**
(metadatos que el diseñador visual lee en tiempo de ejecución para saber qué puede editar de cada
componente). Ese trío es el modelo de componentes que después reaparecería en .NET.

En 1996 Microsoft fichó a Hejlsberg. Allí diseñó **J++**, luego **C#** y el CLR, y más tarde
**TypeScript**. La genealogía es directa y admitida: quien conoce Delphi reconoce medio C# a primera
vista.

Borland pasó por varios dueños —CodeGear, **Embarcadero**, hoy dentro de **Idera**— y el producto
siguió. **FireMonkey (FMX)**, introducido en 2011, añadió compilación a macOS, iOS, Android y Linux
desde el mismo código. En paralelo, el proyecto libre **Free Pascal** alcanzó una compatibilidad muy
alta con el dialecto de Delphi, y su IDE **Lazarus** replicó el entorno visual: hoy es una
alternativa gratuita y seria.

## 🏭 Dónde sobrevive hoy

- **Software empresarial de escritorio para Windows**: ERP regionales, gestión comercial,
  contabilidad, nóminas — especialmente en España, Latinoamérica, Italia, Alemania y Europa del Este.
- **Punto de venta (TPV) y retail**: terminales de caja, gestión de tiendas.
- **Software industrial y de laboratorio**: control de máquinas, adquisición de datos, instrumentación.
- **Aplicaciones verticales**: clínicas, gestorías, talleres, logística — el software que una empresa
  compró en 2003, que funciona, y que su proveedor sigue manteniendo.
- **Aplicaciones de escritorio conocidas** construidas históricamente con Delphi: **Total Commander**,
  **FL Studio** o el cliente de escritorio original de **Skype** son casos citados habitualmente.

## 🧠 Por qué no ha muerto

**1. Un `.exe` y nada más.** Sin máquina virtual, sin intérprete, sin `node_modules`, sin instalar un
runtime en el equipo del cliente. Se copia el fichero y funciona. En entornos corporativos con
equipos bloqueados, eso sigue siendo una ventaja real y difícil de igualar.

**2. Productividad en aplicaciones con muchos formularios.** Para una aplicación de gestión con
ochenta pantallas conectadas a una base de datos, el flujo de Delphi —componentes de datos, controles
enlazados, diseñador visual— sigue siendo extraordinariamente rápido. Es un nicho que las herramientas
web no han mejorado, solo desplazado.

**3. Compatibilidad hacia atrás muy larga.** Código de Delphi 7 (2002) se recompila hoy con ajustes
moderados. Para una empresa con medio millón de líneas, eso es la diferencia entre mantener y
reescribir.

**4. El coste de reescribir es el argumento de siempre**, con el agravante habitual: el conocimiento
del negocio vive en ese código y su autor a menudo ya no está.

**5. El lenguaje ha seguido creciendo.** Genéricos, métodos anónimos (*closures*), atributos, ayudantes
de tipo, `for..in`, inferencia con `var`, ARC en plataformas móviles. El Object Pascal de 2026 no se
parece al de 1995.

> **Y una advertencia honesta:** la licencia comercial es cara y la comunidad es pequeña comparada con
> la de cualquier lenguaje del núcleo. Encontrar programadores Delphi es un problema real para las
> empresas que dependen de él, y es una de las razones por las que muchas migran. Si te acercas por
> curiosidad, empieza por **Lazarus**, que es libre.

## 🔄 Lo que se ha modernizado

Delphi es, de esta lista, el que más se ha transformado sin cambiar de nombre:

- **Multiplataforma real con FireMonkey (FMX)**: del mismo código fuente salen ejecutables para
  **Windows, macOS, iOS, Android y Linux**, incluidos ARM64 y Apple Silicon.
- **El lenguaje creció**: genéricos, **métodos anónimos** (closures), atributos personalizados y RTTI
  extendida, ayudantes de tipo, `for..in`, inferencia con `var x := ...`, y operadores nulos.
- **Servicios y nube**: **RAD Server** para publicar APIs REST, clientes HTTP/REST integrados,
  componentes para servicios en la nube y **FireDAC** para acceso a prácticamente cualquier base de
  datos.
- **IDE moderno**: motor **LSP** para completado y navegación de código, refactorizaciones, y
  soporte de Git integrado.
- **Pruebas unitarias y CI**: **DUnitX** y **Delphi-Mocks** dan pruebas automatizadas, y la
  compilación por línea de comandos (`dcc32`/`dcc64`, MSBuild) permite integrarlo en pipelines.
- **Community Edition gratuita**, que bajó la barrera de entrada para quien quiera probarlo sin
  licencia comercial.
- Y en paralelo, **Free Pascal + Lazarus** ofrecen la misma capacidad multiplataforma con licencia
  libre, incluida compilación a **WebAssembly**.

## ⚙️ Cómo se ejecuta hoy

```bash
# Free Pascal (libre) — compatible con el dialecto de Delphi
sudo apt-get install -y fpc
fpc -Mdelphi total_venta.pas
echo "15000 2 0.10" | ./total_venta
# Total: 27000.00
```

```text
REM Delphi (Embarcadero), desde la línea de comandos
dcc64 TotalVenta.dpr
TotalVenta.exe
```

**Herramientas:** **Delphi / RAD Studio** de Embarcadero, con **Community Edition** gratuita para uso
individual y pequeñas empresas; **Free Pascal** (`fpc`) más **Lazarus** como alternativa libre y
multiplataforma. Gestión de paquetes: **GetIt** en Delphi, **Online Package Manager** en Lazarus.

**Ficheros del ecosistema:** `.pas` (unidad de código), `.dpr` (proyecto), `.dfm` (formulario, un
fichero de texto con las propiedades de los componentes, versionable en Git), `.dproj` (configuración
del proyecto).

## 🧪 El programa de la clase 041 en Object Pascal

```pascal
program TotalVenta;
{$MODE DELPHI}{$H+}

uses
  SysUtils;

type
  TVenta = class
  private
    FPrecio, FCantidad, FDescuento: Double;
    function GetTotal: Double;
  public
    constructor Create(APrecio, ACantidad, ADescuento: Double);
    property Precio    : Double read FPrecio;
    property Cantidad  : Double read FCantidad;
    property Descuento : Double read FDescuento;
    property Total     : Double read GetTotal;      // se calcula al leerla
  end;

constructor TVenta.Create(APrecio, ACantidad, ADescuento: Double);
begin
  inherited Create;
  FPrecio    := APrecio;
  FCantidad  := ACantidad;
  FDescuento := ADescuento;
end;

function TVenta.GetTotal: Double;
begin
  Result := FPrecio * FCantidad * (1 - FDescuento);
end;

var
  Precio, Cantidad, Descuento: Double;
  Venta: TVenta;

begin
  Read(Precio, Cantidad, Descuento);

  Venta := TVenta.Create(Precio, Cantidad, Descuento);
  try
    WriteLn('Total: ', Venta.Total:0:2);
  finally
    Venta.Free;
  end;
end.
```

**Recorrido, línea a línea.**

- `{$MODE DELPHI}` pone a Free Pascal en dialecto Delphi. Con Delphi de Embarcadero esta directiva no
  hace falta.
- `uses SysUtils;` es la importación de unidades. El sistema de módulos de Object Pascal —una unidad
  con secciones `interface` e `implementation`— viene de **Modula-2**, y es una de las razones de la
  velocidad de compilación: el compilador solo necesita la `interface` de las dependencias.
- `type TVenta = class` declara una clase. La convención `T` inicial para tipos es universal en este
  ecosistema, igual que `F` para campos privados (*field*) y `A` para argumentos.
- **`property Total: Double read GetTotal;` es la línea que hay que entender.** Desde fuera,
  `Venta.Total` se lee **exactamente como un campo**: `WriteLn(Venta.Total)`. Pero por dentro se
  ejecuta el método `GetTotal`. Eso es una **propiedad**, y en 1995 era una novedad: permitía cambiar
  un campo público por un cálculo sin romper a ningún cliente, y permitía al **inspector de objetos**
  del IDE mostrar y editar los atributos de un componente sin conocerlo. Es, literalmente, el mismo
  concepto que `public double Total => ...` en C#, con veinte años de diferencia y el mismo autor.
- `constructor Create` — el constructor **tiene nombre** y se llama por convención `Create`; no hay
  sintaxis especial. Y se invoca **sobre la clase**: `TVenta.Create(...)`, no `new TVenta(...)`.
- **`try ... finally Venta.Free; end;` no es opcional.** En Windows, Object Pascal **no tiene
  recolector de basura**: todo objeto creado con `Create` debe liberarse con `Free`. El bloque
  `try..finally` garantiza que ocurra aunque haya una excepción, y es el idioma más repetido de todo
  el código Delphi del mundo. (En las plataformas móviles hubo un periodo con ARC; hoy el modelo se ha
  reunificado hacia la gestión manual.)
- `Result := ...` es cómo una función devuelve un valor en Object Pascal. `Result` es una variable
  implícita, no una palabra de retorno: se le puede asignar varias veces y el código continúa.
- `Venta.Total:0:2` reutiliza el formateo integrado de [Pascal](pascal.md): ancho 0, dos decimales.

**Y el modelo que de verdad define a Delphi**, aunque no quepa en un ejemplo de consola: en una
aplicación real el mismo cálculo estaría enganchado a un evento.

```pascal
procedure TFormVenta.EditCantidadChange(Sender: TObject);
begin
  LabelTotal.Caption := Format('Total: %.2f', [CalcularTotal]);
end;
```

El IDE generó esa firma al hacer doble clic sobre el control, la asoció al evento `OnChange` en el
fichero `.dfm`, y `Sender` identifica quién lo disparó. **Un evento es un puntero a método asignable
en tiempo de ejecución** — el mismo concepto que un `delegate` de C#, y por la misma razón: el mismo
diseñador.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En Object Pascal es… |
|---|---|
| `new Clase(args)` | `TClase.Create(args)` — el constructor se llama sobre la clase |
| `delete` / recolector | `.Free` dentro de `try..finally` |
| `public int X { get; set; }` (C#) | `property X: Integer read FX write FX;` — el original |
| `event` / `delegate` (C#) | `property OnAlgo: TNotifyEvent read FOnAlgo write FOnAlgo;` |
| `interface` | `interface`, con conteo de referencias vía `IInterface` |
| `List<T>` | `TList<T>` de `System.Generics.Collections` |
| Lambda | `procedure of object` (método) o método anónimo `procedure begin ... end` |
| `foreach` | `for X in Coleccion do` |
| `string.Format(...)` | `Format('%.2f', [x])` — con los argumentos en un array abierto |
| `try/catch/finally` | `try..except` y `try..finally` — **bloques separados**, no uno solo |
| `var x = ...` (inferencia) | `var x := ...;` (Delphi 10.3 en adelante) |

## ⚠️ Errores comunes al leerlo

- **Olvidar `Free`.** Fuga de memoria silenciosa. Y liberar dos veces es peor: corrupción.
- **Confundir `try..except` con `try..finally`.** Son dos construcciones distintas y **no** se
  combinan en un solo bloque como en Java o C#; hay que anidarlas.
- **Creer que una propiedad es un campo.** `Venta.Total` puede estar ejecutando código, abriendo una
  conexión o disparando un evento. En depuración, esa distinción importa.
- **Suponer que `string` es igual en todas partes.** Sin `{$H+}` es de 255 caracteres. En Delphi
  moderno es UTF-16 con conteo de referencias; en Free Pascal el detalle depende del modo.
- **Ignorar el `.dfm`.** El formulario no está en el `.pas`: está en un fichero de texto paralelo con
  las propiedades de cada componente. Quien lee solo el código no ve la mitad de la aplicación.
- **Asumir que Delphi es solo Windows.** Con FireMonkey compila para macOS, iOS, Android y Linux; con
  Free Pascal/Lazarus, para más plataformas todavía.

## 📚 Fuentes y bibliografía

- [Embarcadero Delphi](https://www.embarcadero.com/products/delphi) — el producto comercial y su
  **Community Edition** gratuita.
- [DocWiki de Embarcadero](https://docwiki.embarcadero.com/RADStudio/en/Main_Page) — la referencia
  oficial del lenguaje y de las bibliotecas.
- [Lazarus IDE](https://www.lazarus-ide.org/) y [Free Pascal](https://www.freepascal.org/) — la
  alternativa libre, por donde conviene empezar.
- **Marco Cantù**, *Object Pascal Handbook* — el libro de referencia del lenguaje moderno; el autor
  publica versiones actualizadas y hay ediciones de descarga gratuita.
- **Marco Cantù**, *Mastering Delphi* (serie) — la obra clásica sobre la VCL y el desarrollo de
  aplicaciones.
- **Nick Hodges**, *Coding in Delphi* y *More Coding in Delphi* — Delphi moderno con genéricos,
  inyección de dependencias y pruebas unitarias; el puente hacia prácticas actuales.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [Pascal](pascal.md) · [VBA](vba.md) · [Ada](ada.md)
