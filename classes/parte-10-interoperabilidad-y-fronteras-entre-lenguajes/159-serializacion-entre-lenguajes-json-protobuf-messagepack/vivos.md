# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 159

> [⬅️ Volver a la clase 159](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Convertir un nombre y un valor en `x:5`. Es la serialización más simple imaginable, y la clase trata de
lo que ocurre cuando eso hay que hacerlo bien entre dos lenguajes que no comparten nada. Y esta página
tiene el dato que pone JSON en perspectiva: **el copybook de COBOL es una descripción de datos binaria
con tipos, escalas y arreglos variables — es decir, un esquema— y es de 1959**; **ASN.1, con su
codificación binaria y su compilador de esquemas, es de 1984**; y Protocol Buffers, de 2008.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **formato de intercambio**, y estos lenguajes lo enseñan porque **sufrieron todos
> los problemas antes de que existiera JSON**: el orden de los bytes, la codificación de caracteres, los
> decimales con precisión, los registros de longitud variable y la evolución del esquema. **Y varios
> tienen una propiedad que la industria redescubrió: su representación textual se puede volver a leer** —
> Lisp con `print`/`read`, PL/I con `put data`/`get data`, Smalltalk con `storeString`.
>
> Y aparece la pregunta que decide el formato: **¿lo leen personas o máquinas, y quién controla las dos
> puntas?**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `clave valor` → stdout: `serializado=<clave>:<valor>`
- **Regla:** `unir clave y valor con ':'`

| stdin | esperado |
|---|---|
| `x 5` | `serializado=x:5` |
| `edad 30` | `serializado=edad:30` |
| `n 100` | `serializado=n:100` |

> **Qué está verificado en esta página.** Los lenguajes de la sección 🟢 se **ejecutan en CI**
> contra este mismo `casos.json`, igual que las diez implementaciones del núcleo
> ([workflow Labs](../../../labs/README.md)). Los de la sección 🟡 **no pueden** cumplir este
> contrato sin falsear el lenguaje, y se explica por qué. Los de la sección ⚪ sí podrían, pero
> su cadena de herramientas no está en los *runners*: son correctos, sin sello de máquina.

---

## 🟢 Se ejecutan en CI

### COBOL

[Ficha completa](../../../atlas/cobol.md) · Banca, seguros, gobierno, medios de pago · `cobc -x -free prog.cob`

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. SERIAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  C-NOM   PIC X(20).
01  C-VAL   PIC X(20).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-NOM C-VAL
    END-UNSTRING

    DISPLAY "serializado=" FUNCTION TRIM(C-NOM)
            ":" FUNCTION TRIM(C-VAL)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Aquí está el dato del gancho, y merece desarrollarse porque
cambia la perspectiva sobre lo que es nuevo y lo que no: **un copybook es un esquema de serialización
binaria**.

```cobol
       01  PEDIDO.
           05  CLIENTE        PIC X(10).
           05  FECHA          PIC 9(8).
           05  IMPORTE        PIC S9(9)V99 COMP-3.
           05  DIVISA         PIC X(3).
           05  NUM-LINEAS     PIC 9(2) COMP.
           05  LINEA OCCURS 1 TO 99 DEPENDING ON NUM-LINEAS.
               10  ARTICULO   PIC X(8).
               10  CANTIDAD   PIC S9(5) COMP-3.
```

**Eso define, sin ambigüedad, cada byte del registro**: dónde empieza cada campo, cuántos bytes ocupa,
qué codificación tiene y cuántas repeticiones hay.

Y **`COMP-3` merece la explicación** porque es la razón de que este formato siga en uso (clase 045):
**decimal empaquetado, dos dígitos por byte, con el signo en el último medio byte**.

```text
El importe 12345.67 en S9(9)V99 COMP-3 ocupa 6 bytes:
   00 01 23 45 67 0C        (C = positivo, D = negativo)
```

**Es exacto —sin el redondeo binario de `double`— y es compacto.** Un `12345.67` en JSON son ocho
caracteres; aquí son seis bytes que además no pierden precisión.

Y las tres dificultades clásicas de intercambiar estos registros con otros sistemas merecen enumerarse,
porque son las de toda esta clase:

**Una, la codificación**: el mainframe usa **EBCDIC**, el resto del mundo ASCII o UTF-8. **Y la
conversión hay que hacerla campo a campo**, porque **los campos `COMP-3` y `COMP` NO se deben
convertir**: son binarios, y traducirlos como texto los destruye.

Es el error número uno al mover ficheros del mainframe: **un FTP en modo texto convierte todo el
registro y corrompe los campos numéricos**.

**Dos, el orden de los bytes**: los `COMP` del mainframe son de byte más significativo primero; los de
Intel, al revés (clase 128).

**Y tres, la evolución del esquema.** Y aquí COBOL enseña la regla que el cierre de esta clase propone,
porque la aprendió por las malas: **los campos nuevos se añaden AL FINAL del registro y con relleno
reservado**.

```cobol
           05  FILLER PIC X(100).      *> espacio reservado para el futuro
```

**Reservar relleno en el registro** era la práctica estándar precisamente porque **cambiar la posición
de un campo obliga a recompilar y redesplegar todo lo que lo lee, a la vez** — que es exactamente el
problema que los identificadores de campo de Protobuf resuelven hoy.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program serial
   implicit none
   character(len=60) :: linea
   character(len=20) :: nombre, valor
   integer :: p1

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, ' ')
   nombre = linea(1:p1-1)
   valor  = adjustl(linea(p1+1:))

   write(*, '(A)') 'serializado=' // trim(nombre) // ':' // trim(valor)
end program serial
```

**Lo que esta clase enseña en Fortran.** Fortran tiene un formato binario propio y una trampa clásica que
merece explicarse, porque es la que más datos científicos ha hecho ilegibles: **los ficheros sin
formato**.

```fortran
open(unit=10, file='datos.bin', form='unformatted')
write(10) n, matriz
```

**Eso escribe los bytes tal cual… más algo que casi nadie espera: los marcadores de registro.**

```text
Un registro secuencial sin formato de gfortran es:
   [longitud: 4 bytes] [los datos] [longitud otra vez: 4 bytes]
```

**Los marcadores existen para poder leer hacia atrás**, y **su tamaño y presencia dependen del
compilador**: gfortran usa 4 bytes por defecto —8 con `-frecord-marker=8`—, y otros compiladores usan
otra cosa.

**Así que un fichero sin formato escrito por ifort puede no leerse con gfortran**, y desde luego **no se
puede leer con un programa en C sin conocer el detalle**.

Y a eso se suma **el orden de los bytes**:

```fortran
open(10, file='datos.bin', form='unformatted', access='stream', &
     convert='big_endian')          ! extensión, no estándar
```

**`access='stream'` (Fortran 2003) es la solución moderna**: escribe **sin marcadores de registro**, byte
a byte, y es lo que hay que usar para intercambiar con otros lenguajes.

Y de ahí que la comunidad científica adoptara formatos con esquema, y merece nombrarlos porque resuelven
exactamente lo que el cierre de esta clase pide:

| Formato | Qué aporta |
|---|---|
| **NetCDF** | arreglos con dimensiones, unidades y metadatos; **autodescriptivo** |
| **HDF5** | jerárquico, con compresión, y paralelo con MPI |
| **CF conventions** | un vocabulario estándar de nombres para variables climáticas |
| **Zarr** | arreglos por trozos, pensado para almacenamiento en la nube |

**NetCDF y HDF5 son autodescriptivos**, que es la propiedad clave: **el fichero lleva dentro qué
variables contiene, con qué dimensiones, tipos y unidades**.

Y eso significa que **un programa que no conocía ese fichero puede leerlo y entenderlo** — que es
justamente lo que un formato sin esquema no permite, y la razón por la que un `.bin` de hace veinte años
suele ser irrecuperable.

Es la lección más práctica de esta página para cualquier dominio: **los datos sobreviven a los programas
que los escribieron**, así que **el formato tiene que llevar su propia descripción**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Serial is
   Linea  : String (1 .. 60);
   Ultimo : Natural;
   Sep    : Natural;
begin
   Get_Line (Linea, Ultimo);
   Sep := Ada.Strings.Fixed.Index (Linea (1 .. Ultimo), " ");

   Put_Line ("serializado=" & Linea (1 .. Sep - 1) & ":" &
             Ada.Strings.Fixed.Trim (Linea (Sep + 1 .. Ultimo), Ada.Strings.Both));
end Serial;
```

**Lo que esta clase enseña en Ada.** Ada tiene la serialización en el estándar, con dos mecanismos que
merece distinguir porque resuelven problemas distintos.

**El primero son los *streams*:**

```ada
with Ada.Streams.Stream_IO;

type Registro is record
   Codigo : Integer;
   Nombre : String (1 .. 20);
end record;

Registro'Write (Flujo, Mi_Registro);      --  serializar
Registro'Read  (Flujo, Otro);              --  y volver a leer
```

**`'Write` y `'Read` son atributos que el compilador genera para cualquier tipo**, incluidos los
compuestos y los etiquetados —donde `'Class'Output` **escribe también la etiqueta del tipo**, para poder
reconstruir el descendiente correcto—.

Es serialización automática con polimorfismo, en el lenguaje, sin biblioteca.

**Y su límite hay que decirlo, porque es el mismo que en todos lados**: **el formato lo define la
implementación**. Sirve para guardar y recuperar con el mismo programa, **no para intercambiar entre
lenguajes**.

**Y el segundo mecanismo sí sirve para eso: las cláusulas de representación** (clase 157).

```ada
type Trama is record
   Version  : Integer range 0 .. 15;
   Tipo     : Integer range 0 .. 255;
   Longitud : Integer range 0 .. 65_535;
end record;

for Trama use record
   Version  at 0 range 0 .. 3;
   Tipo     at 0 range 4 .. 11;
   Longitud at 2 range 0 .. 15;
end record;

for Trama'Size use 32;
for Trama'Bit_Order use System.High_Order_First;   --  ¡orden de bits explícito!
```

**Con eso, el registro de Ada tiene exactamente la disposición que exige el protocolo**, y
`Unchecked_Conversion` lo convierte en bytes.

Es la mejor herramienta de esta página para **implementar un formato binario definido por una norma** —
una trama de red, un mensaje CAN, un paquete de telemetría—, porque **el formato se declara y el
compilador comprueba que cuadra**.

Y merece la comparación que resume la clase: **`'Write` es cómodo y propietario; las cláusulas de
representación son laboriosas e interoperables**.

Es la misma disyuntiva que `Storable` frente a JSON en Perl, o la serialización nativa de Java frente a
Protobuf: **el formato propio del lenguaje siempre es más fácil y nunca cruza la frontera**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Serial;
{$MODE OBJFPC}{$H+}
uses SysUtils, StrUtils;

var
  Linea, Nombre, Valor: string;
  P: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P := Pos(' ', Linea);
  Nombre := Copy(Linea, 1, P - 1);
  Valor  := Trim(Copy(Linea, P + 1, Length(Linea)));

  WriteLn('serializado=', Nombre, ':', Valor);
end.
```

**Lo que esta clase enseña en Pascal.** El ecosistema Delphi tiene un mecanismo de serialización que
merece contarse porque llegó muy pronto y por un camino inesperado: **el sistema de *streaming* de
componentes**.

```pascal
{ Un .dfm es la serialización de un árbol de objetos, en TEXTO }
object Form1: TForm1
  Left = 100
  Top = 50
  Caption = 'Mi ventana'
  object Button1: TButton
    Left = 20
    Caption = 'Aceptar'
    OnClick = Button1Click
  end
end
```

**Ese fichero se genera automáticamente desde los objetos y se vuelve a leer para reconstruirlos**, y
funciona **por la RTTI de los miembros `published`** (clase 139).

Es serialización automática dirigida por metadatos, **de 1995**, y es la misma idea que hoy usan los
serializadores por anotaciones de Java, C# y Python.

Y sus propiedades merecen verse porque son las que el cierre de esta clase pide:

- **Solo se escriben las propiedades que difieren del valor por defecto** —de ahí que un `.dfm` sea
  compacto—.
- **Al leer, una propiedad desconocida se puede ignorar**, con un manejador de errores. **Eso es
  tolerancia a lo desconocido**, la tercera regla del cierre.
- **Y hay una versión binaria y una textual del mismo formato**, convertibles entre sí.

Y el ecosistema moderno cubre el resto:

| Herramienta | Notas |
|---|---|
| **`fpjson` / `System.JSON`** | JSON en la distribución |
| **`TJSONSerializer` (Delphi)** | objetos a JSON **por RTTI extendida** |
| **mORMot** | serialización rápida, con soporte de esquemas |
| **`TFPObjectList` + streaming** | el mecanismo clásico |

Y merece señalar la trampa que este ecosistema enseña bien y que aplica a cualquier serialización por
reflexión: **si el formato se deriva automáticamente de los campos de la clase, renombrar un campo rompe
el formato**.

```pascal
[JSONName('cliente_id')]      { ← el nombre del CAMPO deja de ser el del FORMATO }
FClienteID: Integer;
```

**Anotar explícitamente el nombre externo** es la práctica que separa el modelo interno del contrato
publicado — y es la primera cosa que hay que hacer en cuanto ese contrato tenga más de un consumidor
(clase 160).

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((linea (read-line))
       (sep (position #\Space linea))
       (nombre (subseq linea 0 sep))
       (valor (string-trim '(#\Space #\Return) (subseq linea (1+ sep)))))
  (format t "serializado=~A:~A~%" nombre valor))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene la propiedad que el "por qué" de esta clase
anunciaba, y es de las más elegantes del lenguaje: **lo que `print` escribe, `read` lo vuelve a leer**.

```lisp
(with-open-file (f "datos.lisp" :direction :output)
  (let ((*print-readably* t))
    (print '(:pedido 4711 :items ((:art "A1" :cant 3) (:art "B2" :cant 1))) f)))

(with-open-file (f "datos.lisp")
  (read f))     ; → la estructura, exactamente igual
```

**No hay serializador**: el lector y el impresor del lenguaje **ya son un formato de intercambio** (clase
104).

Y sus ventajas merecen enumerarse porque son reales:

- **Cero código**: no hay esquema que declarar ni biblioteca que instalar.
- **Estructuras anidadas arbitrarias**, sin límite de profundidad.
- **Y `*print-circle*` maneja referencias compartidas y ciclos**, con la notación `#1=` y `#1#` — cosa
  que JSON no puede.

Y las desventajas, que son las del cierre de esta clase:

- **Solo lo lee Lisp.** Es el formato propio del lenguaje, como `'Write` en Ada de esta página.
- **Y `read` es peligroso sobre datos externos** (clase 153): con `*read-eval*` activado, ejecuta código.

De ahí que el ecosistema tenga formatos serios para cruzar la frontera:

| Biblioteca | Formato |
|---|---|
| **jzon / cl-json / yason** | JSON |
| **cl-messagepack** | MessagePack |
| **cl-protobufs** | Protocol Buffers, con compilador de `.proto` |
| **conspack** | binario, pensado para Lisp, con referencias compartidas |

Y merece cerrar con una observación que Lisp permite ver mejor que ningún otro lenguaje de esta página y
que es la tesis del "por qué": **el formato de intercambio de datos y el formato del código son la misma
cosa cuando el lenguaje es homoicónico**.

Eso hace que **la configuración, los datos y el programa se escriban igual**, y es lo que hicieron
después EDN en Clojure, los ficheros de Emacs Lisp y, en otro nivel, YAML y TOML — que son intentos de
tener un formato de datos legible **sin** el peligro de que sea código.

Y ese es el compromiso exacto: **la homoiconicidad hace la serialización trivial y la seguridad
difícil**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] nombre valor

puts "serializado=$nombre:$valor"
```

**Lo que esta clase enseña en Tcl.** Tcl tiene una propiedad que lo hace peculiar en esta clase y que
viene de la clase 081: **todo valor de Tcl ya tiene una representación textual canónica**.

```tcl
set d [dict create nombre "Ana" edad 30 items {a b c}]
puts $d
# → nombre Ana edad 30 items {a b c}

set d2 $d            ;# y esa cadena SE PUEDE VOLVER A INTERPRETAR como diccionario
```

**Una lista, un diccionario o un arreglo anidado son cadenas**, y **volver a interpretarlas es
gratuito**.

Es la misma propiedad que `print`/`read` en Lisp de esta página, y con la misma consecuencia práctica:
**guardar una estructura de Tcl es escribirla, y leerla es leer la línea**.

Y merece señalar el detalle de citación que lo hace correcto, porque es donde se cometen los errores:

```tcl
set l [list "un valor" "con {llaves}" "y \"comillas\""]
puts $l
# → {un valor} {con \{llaves\}} {y "comillas"}
```

**`list` genera la citación correcta automáticamente**, así que **el resultado siempre se puede volver a
leer**. Construir la cadena a mano con `join` **no lo garantiza**, y ese es el fallo clásico.

Y la regla que se deriva vale para cualquier lenguaje: **la serialización la hace la biblioteca, nunca la
concatenación**.

Y el ecosistema:

| Paquete | Formato |
|---|---|
| **`json` (tcllib)** | JSON, en las dos direcciones |
| **`huddle`** | estructuras con tipo, para generar JSON correcto |
| **`tdom`** | XML y XPath |
| **`csv` (tcllib)** | con citación correcta |
| **`binary format` / `binary scan`** | **formatos binarios, con plantilla** |

**`binary scan` merece la mención final** porque resuelve el problema de las columnas de la izquierda de
esta página con una sintaxis compacta:

```tcl
binary scan $bytes "IuIu a10 s" longitud tipo nombre flags
#              ↑ enteros big-endian sin signo, 10 chars, y un short
```

**Una cadena de plantilla describe la disposición del registro**, y `binary format` hace lo inverso.

Es la respuesta de un lenguaje sin tipos al problema de las cláusulas de representación de Ada: **no se
declara el tipo, se declara la plantilla en el punto de conversión** — más flexible, y sin ninguna
comprobación.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($nombre, $valor) = split ' ', $linea;

print "serializado=$nombre:$valor\n";
```

**Lo que esta clase enseña en Perl.** Perl tiene la colección más completa de serializadores de esta
página, y compararlos enseña bien el compromiso de la clase:

| Módulo | Formato | Nota |
|---|---|---|
| **`JSON::XS` / `Cpanel::JSON::XS`** | JSON | rapidísimo; el estándar de facto |
| **`Storable`** | binario **propio de Perl** | rápido y **solo lo lee Perl** |
| **`Data::Dumper`** | código Perl | legible y **se puede `eval`** |
| **`YAML::XS`** | YAML | legible por personas |
| **`Sereal`** | binario | **más rápido y compacto que Storable**, con compresión |
| **`Google::ProtocolBuffers`** | Protobuf | con esquema |
| **`Data::MessagePack`** | MessagePack | JSON binario |

**`Storable` merece la advertencia** porque ilustra el peligro del formato propio del lenguaje:

```perl
use Storable qw(store retrieve);
store($estructura, 'datos.bin');
my $x = retrieve('datos.bin');
```

**El formato de `Storable` ha cambiado entre versiones de Perl**, así que **un fichero guardado con una
versión puede no leerse con otra** — y no hay aviso hasta que ocurre.

Es la misma trampa que la serialización nativa de Java y que `pickle` en Python, y la regla que se
deriva es la del cierre de esta clase: **el formato propio del lenguaje sirve para una caché, nunca para
archivar ni para intercambiar**.

Y Perl aporta a esta clase las dos advertencias que más problemas causan en JSON, y merecen decirse
porque son universales:

**Una, los números grandes.**

```perl
# JSON no distingue enteros de reales, y JavaScript solo tiene double
# → un identificador de 64 bits pierde precisión al pasar por JavaScript
{"id": 9007199254740993}      # se convierte en 9007199254740992
```

**La solución que la industria adoptó es enviar los identificadores grandes como cadenas**, y merece
conocerse porque parece un rodeo y no lo es.

**Y dos, la codificación.**

```perl
use JSON::XS;
my $json = JSON::XS->new->utf8->canonical->encode($datos);
```

**`->utf8` codifica a bytes; sin él, se devuelven caracteres** — y confundirlos produce la doble
codificación clásica que convierte los acentos en `Ã¡` (clase 093).

**Y `->canonical` ordena las claves**, lo que hace la salida **determinista** — imprescindible si se va a
comparar, firmar o versionar (clase 144).

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string nombre, valor;
    if (!(std::cin >> nombre >> valor)) return 1;

    std::cout << "serializado=" << nombre << ':' << valor << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene un problema estructural con esta clase que merece
enunciarse porque explica el ecosistema entero: **C++ no tiene reflexión**.

```cpp
struct Pedido { int id; std::string cliente; double total; };
// No hay forma estándar de preguntar "¿qué campos tiene Pedido?"
```

**Así que la serialización automática es imposible**, y las tres salidas que el ecosistema encontró son
las tres formas de esta clase:

**Una, escribirla a mano:**

```cpp
void to_json(nlohmann::json& j, const Pedido& p) {
    j = {{"id", p.id}, {"cliente", p.cliente}, {"total", p.total}};
}
```

**Dos, declararla una vez con plantillas:**

```cpp
template <class Archive>
void serialize(Archive& ar, Pedido& p) {      // Boost.Serialization, cereal
    ar(CEREAL_NVP(p.id), CEREAL_NVP(p.cliente), CEREAL_NVP(p.total));
}
```

**Y tres —la que la industria eligió—: generar el código desde un esquema.**

```protobuf
message Pedido {
  int32  id      = 1;
  string cliente = 2;
  double total   = 3;
}
```

```bash
protoc --cpp_out=. --python_out=. --java_out=. pedido.proto
```

**Y ahí está la razón por la que Protocol Buffers ganó**, y merece verla: **el esquema es la fuente de
verdad y de él se generan las clases de todos los lenguajes**.

Y los números `= 1`, `= 2`, `= 3` son la pieza que resuelve el problema del cierre de esta clase:

```text
- El identificador viaja en el mensaje, NO el nombre del campo → compacto
- Un campo nuevo con un identificador nuevo lo IGNORAN los lectores antiguos
- Un campo borrado deja su identificador RESERVADO para siempre
- Y renombrar un campo NO rompe nada, porque el nombre no viaja
```

**`reserved 3, 7 to 9; reserved "total_viejo";`** es la declaración que impide reutilizar un
identificador — la segunda regla del cierre, hecha comprobable por el compilador de esquemas.

Y merece la comparación que ordena la elección:

| Formato | Tamaño | Velocidad | Legible | Esquema |
|---|---|---|---|---|
| **JSON** | grande | media | **sí** | opcional (JSON Schema) |
| **MessagePack** | medio | rápida | no | opcional |
| **Protobuf** | pequeño | muy rápida | no | **obligatorio** |
| **FlatBuffers / Cap'n Proto** | pequeño | **sin analizar** | no | obligatorio |
| **CBOR** | medio | rápida | no | opcional |

**FlatBuffers merece la mención final**: el mensaje **se lee directamente de la memoria sin
deserializar**, accediendo por desplazamientos.

Es la técnica de los registros de longitud fija de COBOL de esta página —**acceder por posición sin
analizar**— reinventada para juegos y sistemas de baja latencia, con la ventaja añadida de la evolución
de esquema.

---

## 🟡 Contrato adaptado, y declarado

Estos lenguajes **no pueden** leer de `stdin` y escribir en `stdout` sin dejar de ser ellos
mismos. No es una limitación del material: es su naturaleza. El cálculo es el mismo y la forma
de entrar y salir es la de su anfitrión. **No pasan por el verificador**, y se dice.

### RPG

[Ficha completa](../../../atlas/rpg.md) · IBM i: ERP, retail, logística, manufactura · `CRTBNDRPG sobre IBM i`

> En IBM i un programa recibe sus datos por **parámetros**, por un **fichero** o por una **pantalla**, nunca por la entrada estándar.

```rpgle
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SERIAL;
  linea char(60) const;
end-pi;

dcl-s texto  varchar(60);
dcl-s pos    int(10);
dcl-s nombre varchar(20);
dcl-s valor  varchar(20);

texto = %trim(linea);
pos = %scan(' ' : texto);

nombre = %subst(texto : 1 : pos - 1);
valor  = %trim(%subst(texto : pos + 1));

dsply ('serializado=' + nombre + ':' + valor);

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG recibió en 2018 y 2019 dos instrucciones que cambiaron por
completo su posición en esta clase, y merecen explicarse porque son de un diseño poco común:
**`DATA-INTO` y `DATA-GEN`**.

```rpgle
dcl-ds pedido qualified;
  id       int(10);
  cliente  varchar(50);
  total    packed(11:2);
  numLineas int(5);
  linea likeds(tLinea) dim(50);
end-ds;

// Analizar JSON DIRECTAMENTE a la estructura
data-into pedido %data(jsonRecibido) %parser('YAJLINTO');

// Y generarlo
data-gen pedido %data(salida) %gen('YAJLDTAGEN');
```

**`DATA-INTO` analiza JSON o XML y rellena una estructura de datos de RPG**, emparejando **por nombre de
subcampo**.

Y merece destacar la decisión de diseño que lo hace especial: **el analizador es un parámetro**.

```rpgle
%parser('YAJLINTO')        // JSON, con YAJL
%parser('XML-INTO')         // XML
%parser('MIPARSER')          // uno propio, para CSV o para un formato interno
```

**IBM no incorporó un analizador de JSON: definió una interfaz de analizadores.** Cualquiera puede
escribir uno —en RPG, en C o en el lenguaje que sea— y **`DATA-INTO` lo usa igual**.

Es exactamente la separación de la clase 158: **la instrucción es la capa idiomática y el analizador es
la capa de abajo, intercambiable**.

Y hay dos detalles prácticos que esta clase debe recoger porque son la tercera regla del cierre:

```rpgle
data-into pedido %data(json : 'allowextra=yes allowmissing=yes')
                 %parser('YAJLINTO');
```

**`allowextra=yes` ignora los campos que llegan y no están en la estructura** —tolerancia a lo
desconocido— **y `allowmissing=yes` acepta que falten** —campos opcionales—.

**Sin esas dos opciones, `DATA-INTO` falla ante cualquier campo inesperado**, y eso hace imposible
desplegar por partes: **el emisor no puede añadir un campo hasta que todos los receptores se
actualicen**.

Es la lección más práctica de esta clase, y aquí se ve con nombre propio: **la tolerancia se configura, y
hay que acordarse de configurarla**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 serial: procedure options(main);

    declare linea  char(60) varying;
    declare nombre char(20) varying;
    declare valor  char(20) varying;
    declare p      fixed binary(31);

    get edit (linea) (a(60));
    linea = trim(linea);

    p = index(linea, ' ');
    nombre = substr(linea, 1, p - 1);
    valor = trim(substr(linea, p + 1));

    put skip list ('serializado=' || nombre || ':' || valor);

 end serial;
```

**Lo que esta clase enseña en PL/I.** PL/I tiene la propiedad que el "por qué" de esta clase anunciaba, y
es de 1964: **`PUT DATA` escribe con nombres, y `GET DATA` lo vuelve a leer**.

```pli
 declare 1 pedido,
           2 id      fixed binary(31) initial(4711),
           2 cliente char(20) varying  initial('ACME'),
           2 total   fixed decimal(11,2) initial(1234.56);

 put data (pedido);
 /* → PEDIDO.ID= 4711  PEDIDO.CLIENTE='ACME'  PEDIDO.TOTAL= 1234.56; */

 get data (pedido);      /* y lo LEE de vuelta */
```

**Eso es serialización con nombres, autodescriptiva y reversible**, en dos sentencias del lenguaje.

Y merece compararlo con lo que hoy se considera moderno, porque las propiedades son las mismas:

| Propiedad | `PUT DATA` (1964) | JSON |
|---|---|---|
| Autodescriptivo | **sí**: lleva los nombres | sí |
| Legible por personas | sí | sí |
| Reversible | **sí**: `GET DATA` | sí |
| Tipos | **sí**: la declaración los da | limitados |
| **Decimales exactos** | **sí**: `FIXED DECIMAL` | **no**: `double` |
| Interoperable | **no**: solo PL/I | **sí** |

**La fila de los decimales merece subrayarse**, porque es la limitación de JSON que más problemas causa
en sistemas financieros y que este formato no tenía: **`1234.56` en `FIXED DECIMAL(11,2)` es exacto**;
en JSON depende de cómo lo lea el receptor.

Es la misma razón por la que Protobuf tiene `decimal` en algunas variantes, por la que las APIs
financieras envían los importes como cadenas, y por la que existen tipos decimales en todos los
lenguajes serios (clase 045).

Y PL/I aporta también el formato binario declarado, que es el de COBOL en esta página:

```pli
 declare 1 registro based(p),
           2 codigo  char(4),
           2 importe fixed decimal(9,2),     /* empaquetado */
           2 fecha   picture '99999999';
```

**Una estructura declarada es un formato de registro**, y `read file(f) into(registro)` **lo lee tal
cual**.

Y merece cerrar con lo que este mundo enseña y que el cierre de esta clase recoge: **estos formatos
sobrevivieron cincuenta años porque el esquema estaba escrito y era obligatorio**.

Un fichero de datos del mainframe **viene siempre acompañado de su copybook o de su declaración**, y sin
él no se puede leer. Es más rígido que JSON y tiene una ventaja que se aprecia con el tiempo: **no
existen ficheros huérfanos cuyo significado nadie recuerde**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SERIAL ; Serializar un par nombre-valor -- clase 159
 read linea
 new nombre, valor
 set nombre = $piece(linea, " ", 1)
 set valor = $piece(linea, " ", 2)
 write "serializado=", nombre, ":", valor, !
 quit
```

**Lo que esta clase enseña en M.** M tiene una relación con esta clase que merece explicarse porque es
distinta de todas: **la serialización está en el modelo de datos**.

```mumps
 set ^PEDIDO(4711, "CLIENTE") = "ACME"
 set ^PEDIDO(4711, "TOTAL") = 1234.56
 set ^PEDIDO(4711, "LINEA", 1) = "A1^3"
 set ^PEDIDO(4711, "LINEA", 2) = "B2^1"
```

**Una global ya es una estructura jerárquica persistente** (clase 099), así que **guardar no requiere
serializar**: la estructura *es* el almacenamiento.

Y el formato interno de cada nodo es la otra mitad, y es característico de este mundo: **los campos
separados por acento circunflejo**.

```mumps
 set ^DPT(dfn, 0) = nombre_"^"_sexo_"^"_fechaNac_"^"_ssn
 set nombre = $piece(^DPT(dfn, 0), "^", 1)
```

**Eso es un registro de campos delimitados**, y `$piece` es el acceso por posición.

Y merece señalar las tres propiedades que tiene y las tres que le faltan, porque es un buen resumen de
esta clase:

**Tiene**: es compacto, es rapidísimo de leer con `$piece`, y **añadir un campo al final no rompe nada**
—los lectores viejos siguen leyendo las posiciones que conocen—, que es exactamente la primera regla del
cierre.

**Le falta**: **no hay esquema declarado en el código**. La correspondencia entre la posición 3 y "fecha
de nacimiento" **vive en el diccionario de FileMan** (clase 149) o, peor, en la cabeza de alguien.

Y de ahí que la interoperabilidad de estos sistemas haya requerido siempre una capa de traducción, que
hoy es la que la clase 158 nombraba:

| Capa | Qué hace |
|---|---|
| **FileMan API** | leer y escribir por **nombre de campo**, no por posición |
| **RPC Broker** | el formato de transporte histórico |
| **HL7 v2** | el estándar sanitario clásico: **campos delimitados por `\|`** |
| **FHIR** | el moderno: **recursos JSON con esquema** |
| **`%JSON.Adaptor` (IRIS)** | objetos a JSON automáticamente |

**HL7 v2 merece la mención** porque es el mismo diseño que las globals: **segmentos y campos separados
por delimitadores, con posiciones fijas y un diccionario aparte**. Es de 1987, mueve la mayor parte de
los mensajes clínicos del mundo, y tiene exactamente los mismos problemas: **compacto, rápido y sin
esquema legible por máquina**.

**Y FHIR es la respuesta**: JSON con esquema, recursos definidos y validación — la tercera regla del
cierre aplicada a un dominio entero, treinta años después.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

Transcript
    show: 'serializado=', (partes at: 1), ':', (partes at: 2);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene la propiedad de Lisp y PL/I de esta página, y
con una vuelta de tuerca: **`storeString` produce código Smalltalk que reconstruye el objeto**.

```smalltalk
| p |
p := OrderedCollection with: 1 with: 'dos' with: 3/4.
p storeString.
"→ '((OrderedCollection new) add: 1; add: ''dos''; add: 3/4; yourself)'"

Compiler evaluate: p storeString.     "→ una colección igual"
```

**Y el detalle que lo hace notable: `3/4` sobrevive como fracción exacta**, no como `0.75`. Smalltalk
tiene números racionales y enteros de precisión arbitraria (clase 045), y **la serialización los
conserva**.

Es una propiedad que casi ningún formato de intercambio tiene, y que la columna de la izquierda de esta
página —COBOL con `COMP-3`, PL/I con `FIXED DECIMAL`— también tenía por otros medios.

Y el ecosistema tiene serializadores serios:

| Herramienta | Notas |
|---|---|
| **Fuel** | binario, rapidísimo; **serializa CUALQUIER objeto, incluidos bloques y clases** |
| **STON** | textual, legible, tipo JSON pero con clases y referencias |
| **NeoJSON** | JSON, con mapeo declarativo |
| **`storeString`** | código, para casos pequeños |

**Fuel merece el detalle** porque hace algo que ningún otro serializador de esta página puede: **serializa
grafos de objetos con ciclos, incluidas las clases y los métodos compilados**.

```smalltalk
FLSerializer serialize: unGrafoCompleto toFileNamed: 'estado.fuel'.
```

**Se puede guardar un proceso suspendido, con su pila, y reanudarlo después** — que es la misma capacidad
que hacía posible enviar el contexto de un error para depurarlo en otra máquina (clase 141).

Y **STON** es el que resuelve el problema de esta clase, y su diseño merece verse:

```text
Pedido {
  #id : 4711,
  #cliente : 'ACME',
  #total : 1234.56,
  #lineas : [ Linea { #art : 'A1', #cant : 3 } ]
}
```

**Es JSON con el nombre de la clase delante**, y con referencias compartidas (`@1`).

Y eso ilustra la tensión final de esta clase: **para que un formato conserve la identidad de las clases y
los objetos compartidos, tiene que salir de JSON** — y en cuanto sale, **deja de ser interoperable**.

Es el mismo compromiso que `'Write` en Ada, `Storable` en Perl y `pickle` en Python: **el formato que
captura todo lo que el lenguaje sabe es el formato que solo ese lenguaje entiende**.

---

## Y de vuelta a la clase

Lo transferible: **el formato es la parte fácil; el esquema y su evolución son la difícil**. Elegir entre
JSON, Protobuf o MessagePack cambia el tamaño y la velocidad; **lo que decide si el sistema sobrevive es
cómo se añade un campo sin romper a quien todavía no se ha actualizado**. De ahí las tres reglas que
atraviesan la página: **campos nuevos siempre opcionales y con valor por defecto**; **nunca reutilizar un
identificador o una posición que estuvo en uso**; y **los dos lados deben tolerar lo que no conocen** —
ignorar los campos desconocidos en lugar de fallar, que es lo que hace posible desplegar por partes.

⏮️ [Volver a la clase 159](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
