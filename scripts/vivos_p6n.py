# -*- coding: utf-8 -*-
"""Parte 6, lote N — clase 104. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 104 — Archivos: leer y escribir, texto y binario
# ---------------------------------------------------------------------------
SPECS["104"] = dict(
    gancho="""
Contar las palabras y los caracteres de una línea. El programa es corto; la clase, no, porque **el
fichero es el terreno de casa de la mitad de estos lenguajes**. COBOL, RPG y PL/I nacieron para
procesar ficheros y tienen para ello un vocabulario que ningún lenguaje moderno iguala: **acceso
indexado, longitud variable, bloqueo de registro y códigos de estado, todo en la sintaxis del
lenguaje**.
""",
    porque="""
Aquí el concepto es la **entrada y salida persistente**, y estos lenguajes lo enseñan porque tienen el
modelo completo que los lenguajes modernos redujeron a "un flujo de bytes". En **COBOL** un fichero se
declara con su estructura, su organización y su clave, y `READ` devuelve un registro tipado. En
**RPG**, además, se puede **bloquear un registro concreto** mientras se actualiza. En **Fortran**, la
E/S formateada con `format` sigue siendo la más potente que existe para tablas numéricas.

Enfrente, **C++, Perl, Tcl y Lisp** ven un fichero como una secuencia de bytes o de caracteres, y todo
lo demás es biblioteca.
""",
    cierre="""
Lo transferible: **"fichero de texto" y "fichero binario" no son dos formatos, son dos contratos**. En
texto hay codificación, saltos de línea que cambian según el sistema y análisis; en binario hay
tamaños, orden de bytes y alineación. Los lenguajes que no distinguen —C, Perl, Tcl en Unix— te dejan
mezclarlos, y de ahí salen los ficheros corruptos al abrir en modo texto en Windows. Y hay una tercera
categoría que estos lenguajes viejos sí modelan y los modernos delegan: **el fichero con estructura**,
que hoy llamamos base de datos.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. FICHERO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  NCAR    PIC 9(4) COMP VALUE 0.
01  NPAL    PIC 9(4) COMP VALUE 0.
01  DENTRO  PIC 9   COMP VALUE 0.
01  ED-P    PIC Z(3)9.
01  ED-C    PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    MOVE 0 TO NCAR
    INSPECT FUNCTION REVERSE(LINEA) TALLYING NCAR FOR LEADING SPACE
    COMPUTE NCAR = 200 - NCAR

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > NCAR
        IF LINEA(I:1) = SPACE
            MOVE 0 TO DENTRO
        ELSE
            IF DENTRO = 0
                ADD 1 TO NPAL
                MOVE 1 TO DENTRO
            END-IF
        END-IF
    END-PERFORM

    MOVE NPAL TO ED-P
    MOVE NCAR TO ED-C
    DISPLAY "palabras=" FUNCTION TRIM(ED-P)
            " caracteres=" FUNCTION TRIM(ED-C)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Este programa lee de la entrada estándar porque el curso lo
exige, y eso **no es COBOL**. El COBOL de verdad declara sus ficheros, y esa declaración es una de las
cosas más completas del lenguaje:

```cobol
ENVIRONMENT DIVISION.
INPUT-OUTPUT SECTION.
FILE-CONTROL.
    SELECT CLIENTES ASSIGN TO "CLIENTES.DAT"
        ORGANIZATION IS INDEXED           *> secuencial, relativa o INDEXADA
        ACCESS MODE IS DYNAMIC             *> secuencial, aleatorio o dinámico
        RECORD KEY IS CLI-ID               *> la clave primaria
        ALTERNATE RECORD KEY IS CLI-NIF WITH DUPLICATES
        FILE STATUS IS FS-CLIENTES.

DATA DIVISION.
FILE SECTION.
FD  CLIENTES.
01  REG-CLIENTE.
    05  CLI-ID     PIC 9(9).
    05  CLI-NOMBRE PIC X(40).
```

Mira lo que hay ahí, porque no está en ningún lenguaje moderno:

- **`ORGANIZATION IS INDEXED`** declara un fichero con **árbol B integrado**. `READ ... KEY IS` es una
  búsqueda por clave; `START` posiciona y `READ NEXT` recorre en orden. Es una base de datos sin base
  de datos, y es lo que hace VSAM en z/OS.
- **`ALTERNATE RECORD KEY`** son **índices secundarios**, con o sin duplicados.
- **`FILE STATUS`** recibe un código de dos caracteres en **cada** operación: `00` correcto, `10` fin
  de fichero, `23` no encontrado, `22` clave duplicada. Comprobarlo tras cada `READ` y `WRITE` es la
  disciplina básica del oficio.
- **El registro está tipado.** `READ CLIENTES` rellena `REG-CLIENTE` con sus campos: no hay análisis,
  no hay conversión y no hay coste.

Y las operaciones son las de una base de datos: `OPEN`, `READ`, `WRITE`, `REWRITE`, `DELETE`, `START`,
`CLOSE`.

Ese es el motivo real de que COBOL siga procesando lo que procesa. Un lote que lee cien millones de
registros de longitud fija y escribe otros tantos **no analiza nada**: mueve bytes a estructuras que
ya tienen esa forma.

COBOL moderno añadió además `LINE SEQUENTIAL` para ficheros de texto normales con salto de línea, que
es lo que usa GnuCOBOL por defecto en Linux — y la distinción entre eso y `SEQUENTIAL` puro es
exactamente la del cierre de esta clase.
"""),
        "fortran": ("""
program fichero
   implicit none
   character(len=400) :: linea
   integer :: ncar, npal, i
   logical :: dentro

   read(*, '(A)') linea
   ncar = len_trim(linea)

   npal = 0
   dentro = .false.
   do i = 1, ncar
      if (linea(i:i) == ' ') then
         dentro = .false.
      else if (.not. dentro) then
         npal = npal + 1
         dentro = .true.
      end if
   end do

   write(*, '(A,I0,A,I0)') 'palabras=', npal, ' caracteres=', ncar
end program fichero
""", """
**Lo que esta clase enseña en Fortran.** La entrada y salida de Fortran es la más antigua que sigue en
uso —**de 1957**— y también la más potente para datos numéricos, gracias a las **especificaciones de
formato**:

```fortran
write(6, '(A10, I5, F10.3, E12.4, 3(2X, I4))') nombre, n, x, y, v
```

Ese formato dice: 10 caracteres, un entero en 5 columnas, un real con 3 decimales en 10, uno en
notación exponencial, y **tres repeticiones** de dos espacios y un entero en 4. Producir una tabla
alineada en Fortran es una línea; en C++ son cinco manipuladores de flujo.

Y la apertura de ficheros lleva una lista de opciones que cubre todo el modelo:

```fortran
open(unit=10, file='datos.txt', status='old', action='read',   &
     form='formatted', access='sequential', iostat=ios)

open(unit=11, file='datos.bin', form='unformatted', access='stream')
open(unit=12, file='reg.dat', access='direct', recl=100)
```

Tres accesos distintos, y los tres importan:

- **`sequential`** con `form='formatted'`: texto.
- **`direct`** con `recl`: **registros de longitud fija accesibles por número**, `read(12, rec=57)`.
  Es el fichero relativo de COBOL.
- **`stream`** (Fortran 2003): **bytes crudos sin estructura**, que es lo que hace falta para
  interoperar con C y para formatos binarios ajenos.

Esa última llegó tarde por una razón histórica que conviene conocer: el `form='unformatted'` clásico
de Fortran **no escribe bytes crudos**, sino que envuelve cada registro entre marcadores de longitud.
Un fichero binario escrito por Fortran **no lo puede leer C** sin conocer ese detalle, y ha sido
fuente de incompatibilidades durante décadas. `access='stream'` lo arregló.

El `unit=` numérico es otro fósil precioso: **los ficheros se identifican por un número**, herencia
de las unidades de cinta físicas. Por convención, 5 es la entrada, 6 la salida y 0 el error.
Fortran 2008 añadió `newunit=` para que el compilador asigne uno libre, evitando las colisiones que
antes se gestionaban con una tabla en un `COMMON`.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Fichero is
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Npal   : Natural := 0;
   Dentro : Boolean := False;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         Dentro := False;
      elsif not Dentro then
         Npal := Npal + 1;
         Dentro := True;
      end if;
   end loop;

   Put ("palabras=");     Put (Npal, Width => 1);
   Put (" caracteres="); Put (Ultimo, Width => 1);
   New_Line;
end Fichero;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene **cuatro** paquetes de entrada y salida, y la elección
entre ellos es una decisión de tipos, no de comodidad:

| Paquete | Qué maneja |
|---|---|
| `Ada.Text_IO` | texto, línea a línea |
| `Ada.Sequential_IO` | **registros TIPADOS**, en secuencia |
| `Ada.Direct_IO` | registros tipados, **por número de registro** |
| `Ada.Streams.Stream_IO` | bytes, para formatos ajenos |

Los dos del medio son genéricos y se instancian con el tipo:

```ada
package Registros is new Ada.Sequential_IO (Cliente);
```

**El fichero queda ligado al tipo `Cliente`**, y leer devuelve un `Cliente` completo. No se puede
escribir un `Producto` en él: no compila. Es seguridad de tipos aplicada a la persistencia, y no la
tiene ningún lenguaje del núcleo.

`Ada.Text_IO` tiene además el modelo más detallado de esta página, con conceptos que otros no
distinguen:

```ada
New_Line;  New_Page;  Set_Col (20);  Set_Line (5);
Col;  Line;  Page;                      --  posición ACTUAL
End_Of_Line;  End_Of_Page;  End_Of_File;
```

**Columna, línea y página** como conceptos del paquete, con `Set_Col` para alinear. Viene de la época
de las impresoras de línea, y sigue siendo lo más cómodo para generar informes de texto.

Y `Ada.Streams` es la pieza que hace elegante la serialización:

```ada
Cliente'Write (Flujo, C);        --  escribir cualquier tipo
Cliente'Read  (Flujo, C);        --  y leerlo
```

**Los atributos `'Write` y `'Read` los genera el compilador para cualquier tipo**, incluidos registros
con variantes y arreglos no restringidos. Y se pueden redefinir para controlar el formato — que es
exactamente lo que hace falta para hablar un protocolo binario ajeno.

Es serialización integrada en el lenguaje y con seguridad de tipos, en 1995.
"""),
        "pascal": ("""
program Fichero;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I, NPal: Integer;
  Dentro: Boolean;

begin
  ReadLn(Linea);

  NPal := 0;
  Dentro := False;
  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
      Dentro := False
    else if not Dentro then
    begin
      Inc(NPal);
      Dentro := True;
    end;
  end;

  WriteLn('palabras=', IntToStr(NPal),
          ' caracteres=', IntToStr(Length(Linea)));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal tiene una construcción que casi nadie más tiene y que
merece conocerse: **el fichero como TIPO parametrizado**.

```pascal
var
  T: Text;                        { fichero de TEXTO }
  F: file of TCliente;             { fichero de REGISTROS de ese tipo }
  B: file;                         { fichero SIN TIPO: bloques de bytes }
```

**`file of T`** declara un fichero cuyos elementos son de tipo `T`, y `Read(F, C)` lee **un registro
completo**, con seguridad de tipos comprobada en compilación. Es lo mismo que `Ada.Direct_IO`, con
sintaxis del lenguaje en lugar de un genérico.

Y como los elementos tienen tamaño conocido, el acceso aleatorio es directo:

```pascal
Seek(F, 57);       { posicionarse en el registro 57 }
Read(F, C);
FileSize(F);       { cuántos registros hay }
```

Esa era la forma canónica de hacer una pequeña base de datos en Turbo Pascal, y funcionaba
sorprendentemente bien. Sigue en producción en aplicaciones antiguas.

`Text` es el otro tipo integrado, y con él `ReadLn`, `WriteLn`, `Eof` y `Eoln` — el `Eoln`, "fin de
línea", es un concepto que Pascal distingue de `Eof` y que la mayoría de los lenguajes no ofrece.

Y hay un detalle histórico que explica una peculiaridad del lenguaje: `Read` y `Write` **aceptan un
número variable de argumentos de tipos distintos**, cosa que ningún procedimiento escrito por el
usuario puede hacer en Pascal. Son **procedimientos mágicos del compilador**, y esa asimetría —el
lenguaje puede hacer algo que su usuario no— es una de las críticas clásicas de Kernighan en *Why
Pascal Is Not My Favorite Programming Language* (1981).

Free Pascal y Delphi modernos añadieron encima toda la capa de flujos:

```pascal
TFileStream, TMemoryStream, TStringStream, TBufferedFileStream
```

Que son objetos con `Read`, `Write`, `Seek` y `CopyFrom`, componibles y con la misma interfaz. Es el
modelo de flujos que después normalizaron Java y .NET.
"""),
        "lisp": ("""
(let* ((linea (string-right-trim '(#\\Return) (read-line)))
       (npal 0)
       (dentro nil))
  (loop for c across linea
        do (if (char= c #\\Space)
               (setf dentro nil)
               (unless dentro
                 (incf npal)
                 (setf dentro t))))
  (format t "palabras=~D caracteres=~D~%" npal (length linea)))
""", """
**Lo que esta clase enseña en Common Lisp.** El modelo de Lisp es el **flujo** (*stream*), y la
apertura idiomática es la macro de la clase 103:

```lisp
(with-open-file (f "datos.txt" :direction :input
                               :element-type 'character
                               :external-format :utf-8
                               :if-does-not-exist :error)
  (loop for linea = (read-line f nil nil)
        while linea do (procesar linea)))
```

`:element-type` es la clave de la distinción texto/binario de esta clase:

```lisp
:element-type 'character            ; texto, con codificación
:element-type '(unsigned-byte 8)    ; BINARIO: bytes crudos
```

Y `read-byte` / `write-byte` frente a `read-char` / `write-char`. Es la misma distinción que en
Fortran y en Pascal, hecha explícita en la apertura.

Lo que distingue a Lisp es lo que ya apareció en las clases 091 y 097: **la serialización es
gratuita**.

```lisp
(with-open-file (f "estado.lisp" :direction :output)
  (print *datos* f))

(with-open-file (f "estado.lisp")
  (setf *datos* (read f)))
```

`print` escribe una estructura de datos en un formato que `read` **puede volver a leer**, y eso cubre
listas, vectores, cadenas, números, símbolos y estructuras de `defstruct`. Sin biblioteca, sin
esquema y sin decisión de formato.

Es la misma propiedad que hace de Lisp un buen formato de configuración, y es por lo que muchos
sistemas Lisp guardan su estado en ficheros `.lisp` legibles.

**Con dos avisos importantes.** El primero: `read` **evalúa macros de lectura**, así que leer un
fichero no fiable es ejecutar código —el `#.` lo permite explícitamente—. La defensa es
`(let ((*read-eval* nil)) ...)`, y es obligatoria si el fichero viene de fuera.

El segundo: los objetos CLOS y las clausuras **no se imprimen de forma legible**, así que la
propiedad no es universal. Para eso están `cl-store` y los sistemas de persistencia del ecosistema.
"""),
        "tcl": ("""
gets stdin linea

puts "palabras=[llength [string trim $linea]] caracteres=[string length $linea]"
""", """
**Lo que esta clase enseña en Tcl.** El modelo de Tcl es el **canal**, y es uno de los mejor diseñados
de esta página, porque **abstrae ficheros, tuberías, sockets y dispositivos serie bajo la misma
interfaz**.

```tcl
set c [open "datos.txt" r]
set c [open "|comando arg" r]        ;# una TUBERÍA a otro proceso
set c [socket www.ejemplo.com 80]     ;# un SOCKET
```

Los tres devuelven un canal, y **los tres se usan con `gets`, `read`, `puts`, `seek` y `close`**. Que
el socket y el fichero sean el mismo tipo de cosa era una idea avanzada en 1990.

`fconfigure` es donde vive la distinción de esta clase, y su detalle es notable:

```tcl
fconfigure $c -translation binary      ;# BINARIO: sin traducir nada
fconfigure $c -translation crlf         ;# saltos de línea de Windows
fconfigure $c -translation lf           ;# de Unix
fconfigure $c -translation auto         ;# detectar (el defecto en lectura)
fconfigure $c -encoding utf-8            ;# la CODIFICACIÓN, aparte
fconfigure $c -blocking 0                ;# lectura NO BLOQUEANTE
fconfigure $c -buffering line
```

Fíjate en que **`-translation` y `-encoding` son opciones distintas**: los saltos de línea y la
codificación de caracteres son problemas separados, y Tcl los separa. La mayoría de los lenguajes los
mezcla en un "modo texto" o "modo binario" que hace las dos cosas a la vez, y eso produce las
sorpresas que el cierre de esta clase menciona.

Y `-blocking 0` con `fileevent` da entrada y salida asíncrona sobre el bucle de eventos de la clase
096:

```tcl
fileevent $c readable { procesar [gets $c] }
vwait forever
```

Eso es programación dirigida por eventos sobre ficheros y sockets, **sin hilos**, en 1990. Es el
modelo que años después popularizaron Node.js y las corrutinas asíncronas, y en Tcl es un comando.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @palabras = split ' ', $linea;

printf "palabras=%d caracteres=%d\\n", scalar(@palabras), length($linea);
""", """
**Lo que esta clase enseña en Perl.** Perl fue diseñado para esto, y su entrada y salida está llena de
atajos que se convirtieron en idiomas:

```perl
while (my $linea = <$fh>) { ... }         # leer línea a línea
my @todas = <$fh>;                          # el fichero ENTERO en una lista
{ local $/; $todo = <$fh>; }                # el fichero entero en un ESCALAR
while (<>) { ... }                           # los ficheros de @ARGV, o stdin
```

La cuarta es la que hizo famoso al lenguaje: **`<>` lee los ficheros que se pasen en la línea de
órdenes, y si no hay ninguno, la entrada estándar**. Con eso, un filtro de Unix cabe en tres líneas, y
con `-n` o `-p` en la línea de órdenes, en cero:

```bash
perl -ne 'print if /error/' *.log
perl -i.bak -pe 's/viejo/nuevo/g' *.conf
```

`-i.bak` edita los ficheros **en el sitio** guardando copia de seguridad. Esa opción sola explica una
parte enorme del uso de Perl en administración de sistemas durante veinte años.

La variable **`$/`** —el separador de registro— es el mecanismo que hay debajo, y es más general de lo
que parece:

```perl
local $/ = undef;      # leer TODO de golpe
local $/ = "";         # modo PÁRRAFO: separa por líneas en blanco
local $/ = \\4096;      # leer en bloques de 4096 bytes
local $/ = "\\n\\n---\\n"; # un separador arbitrario
```

El `local` es el de la clase 096: cambia la variable global **y la restaura al salir del ámbito**.

Y la distinción texto/binario se hace con capas de entrada y salida:

```perl
binmode($fh);                              # binario
binmode($fh, ':encoding(UTF-8)');           # texto con codificación
binmode($fh, ':crlf');                      # traducir saltos de línea
open(my $fh, '<:encoding(UTF-8)', $ruta);    # o en la apertura
```

Ese sistema de **capas apilables** —`:raw`, `:crlf`, `:encoding`, `:gzip` con un módulo— es más
flexible que el modo binario de un solo interruptor de casi todos los demás, y es del mismo espíritu
que el `fconfigure` de Tcl.
"""),
        "cpp": ("""
#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::istringstream flujo(linea);
    std::string palabra;
    int n = 0;
    while (flujo >> palabra) {
        ++n;
    }

    std::cout << "palabras=" << n
              << " caracteres=" << linea.size() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Los **flujos** de C++ son de 1985 y su diseño tiene una idea
excelente y una ejecución muy criticada.

La idea: **el mismo interfaz para consola, fichero y cadena**.

```cpp
std::cout << x;                 // consola
std::ofstream f("d.txt"); f << x;   // fichero
std::ostringstream s; s << x;        // una CADENA en memoria
```

Ese `istringstream` del programa es exactamente eso: **tratar una cadena como un fichero** para
reutilizar el análisis de `>>`. Es un idioma muy útil y poco conocido.

Las críticas, que son justas:

- **El formateo es doloroso.** `std::setw`, `std::setprecision`, `std::hex` son **manipuladores
  pegajosos**: cambian el estado del flujo y siguen activos después. Producir una tabla alineada es
  incomparablemente más incómodo que el `format` de Fortran.
- **Los errores son silenciosos.** Si `>>` falla, el flujo queda en estado de error y las operaciones
  siguientes **no hacen nada**, sin avisar. De ahí el `if (!(std::cin >> x))` de todos los programas
  de esta serie.
- **Son lentos** comparados con `printf`, por la maquinaria de localización y estado.

**C++20 introdujo `std::format`**, que resuelve el primer problema tomando el diseño de Python:

```cpp
std::cout << std::format("{:>10} {:.3f}\\n", nombre, x);
std::println("palabras={} caracteres={}", n, linea.size());   // C++23
```

Y sobre texto frente a binario, C++ tiene la trampa heredada de C:

```cpp
std::ifstream f("datos.bin", std::ios::binary);    // sin el flag, en Windows
                                                    //  traduce CRLF y corrompe
```

**Olvidar `std::ios::binary` en Windows corrompe los ficheros binarios**, y el mismo código funciona
en Linux, donde no hay traducción. Es el error de portabilidad clásico y el ejemplo exacto de lo que
dice el cierre de esta clase.

C++17 añadió además `<filesystem>`, con rutas, iteración de directorios y metadatos portables — algo
que C++ no tuvo durante treinta y cuatro años.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi FICHERO;
  entrada char(200) const;
end-pi;

dcl-s texto  varchar(200);
dcl-s i      int(10);
dcl-s npal   int(10) inz(0);
dcl-s dentro ind inz(*off);

texto = %trimr(entrada);

for i = 1 to %len(texto);
  if %subst(texto : i : 1) = ' ';
    dentro = *off;
  else;
    if not dentro;
      npal += 1;
      dentro = *on;
    endif;
  endif;
endfor;

dsply ('palabras=' + %char(npal) + ' caracteres=' + %char(%len(texto)));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** El manejo de ficheros de RPG es, junto con el de COBOL, el más
completo de esta página — y en un aspecto es superior: **el control de concurrencia está en el
lenguaje**.

```rpgle
dcl-f CLIENTES usage(*update : *delete) keyed;

chain (id) CLIENTES;              // leer POR CLAVE, y BLOQUEAR el registro
if %found(CLIENTES);
  saldo += importe;
  update CLIREG;                   // reescribir y soltar el bloqueo
else;
  unlock CLIENTES;                  // o soltarlo sin escribir
endif;
```

**`chain` con un fichero declarado `*update` bloquea el registro leído**, y el bloqueo se suelta con
`update`, `unlock` o al terminar el programa. Si otro trabajo intenta leer el mismo registro para
actualizarlo, **espera o recibe un error**, según la configuración.

Ese es control de concurrencia a nivel de registro, escrito en dos líneas y sin ninguna base de datos
explícita, y es lo que sostiene aplicaciones con miles de usuarios simultáneos sobre los mismos
ficheros.

El resto del vocabulario cubre lo esperable, y `keyed` es la clave:

```rpgle
setll (clave) FICHERO;     // posicionarse
reade (clave) FICHERO;     // leer los que coincidan con la clave
readp FICHERO;             // leer hacia ATRÁS
write / update / delete
%eof()  %found()  %error()  %status()
```

**`readp`** —leer el registro anterior— no lo tiene casi ningún lenguaje moderno, y es lo que permite
recorrer un índice en orden descendente sin cargar nada en memoria.

Y todo eso funciona sobre **tablas SQL**, porque en IBM i **un fichero y una tabla son el mismo
objeto**: se puede crear una tabla con `CREATE TABLE`, leerla con `chain` desde RPG y consultarla con
SQL, a la vez y desde el mismo programa.

Es la integración que las plataformas modernas persiguen con capas de mapeo, y aquí es una propiedad
del sistema operativo.
"""),
        "pli": ("""
 fichero: procedure options(main);

    declare linea char(200) varying;
    declare (i, npal) fixed binary(31);
    declare dentro bit(1);

    get edit (linea) (a(200));
    linea = trim(linea);

    npal = 0;
    dentro = '0'b;

    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then dentro = '0'b;
       else do;
          if ^dentro then do;
             npal = npal + 1;
             dentro = '1'b;
          end;
       end;
    end;

    put skip list ('palabras=' || trim(char(npal)) ||
                   ' caracteres=' || trim(char(length(linea))));

 end fichero;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tiene **dos modelos de entrada y salida completamente
distintos**, y esa dualidad es marca de su ambición de unificar Fortran y COBOL.

**El de flujo (`STREAM`)**, que es el de Fortran:

```pli
 get list (a, b, c);                    /* formato libre */
 get edit (nombre, edad) (a(20), f(3));  /* con FORMATO explícito */
 put skip list ('resultado: ', x);
 put edit (x) (f(10,2));
```

`get edit` y `put edit` con especificaciones de formato —`a`, `f`, `e`, `p`, `x`, `column`— son el
equivalente del `format` de Fortran, y **`p`** es exclusivo: el **formato de imagen**, que es el `PIC`
de COBOL aplicado a la entrada y salida.

```pli
 put edit (importe) (p'$$$,$$9.99');
```

**El de registro (`RECORD`)**, que es el de COBOL:

```pli
 declare clientes file record input env(vsam);
 read file(clientes) into(reg) key(id);
 write file(salida) from(reg);
 locate reg file(salida);       /* escribir SIN copiar: construir en el búfer */
```

**`locate`** es la joya olvidada: en lugar de construir el registro en una variable y copiarlo al
búfer del fichero, **posiciona un puntero basado directamente sobre el búfer** y se escribe ahí. Es
entrada y salida sin copias, en 1964, y es el antepasado de las técnicas de *zero-copy* que hoy se
persiguen con `mmap` y búferes directos.

Y PL/I integra la E/S con su manejo de condiciones de la clase 103:

```pli
 on endfile(clientes)  eof = '1'b;
 on key(clientes)      put list('clave no encontrada');
 on undefinedfile(clientes) put list('no se pudo abrir');
 on record(clientes)   put list('longitud incorrecta');
```

Cuatro condiciones distintas para cuatro fallos distintos, declarativas y con alcance dinámico. Es más
fino que el `FILE STATUS` de COBOL —que devuelve un código que hay que comprobar— y anticipa las
excepciones tipadas por cincuenta años.
"""),
        "mumps": ("""
FICHERO ; Archivos -- clase 104
 read linea
 set npal = 0, dentro = 0
 for i=1:1:$length(linea) do
 . if $extract(linea, i) = " " set dentro = 0
 . else  if 'dentro set npal = npal + 1, dentro = 1
 write "palabras=", npal, " caracteres=", $length(linea), !
 quit
""", """
**Lo que esta clase enseña en M.** M tiene una respuesta a esta clase que ya se ha visto en toda la
parte y que aquí llega a su conclusión lógica: **en M casi no se usan ficheros, porque los datos viven
en los *globals***.

Un programa M no abre un fichero para guardar datos: escribe en `^DATOS(...)`, que ya es
persistente, transaccional y compartido (clase 089). El fichero solo aparece para **intercambiar con
el exterior**.

Y para eso M tiene un mecanismo llamativo: **el dispositivo**.

```mumps
 open "/tmp/datos.txt":(newversion)
 use "/tmp/datos.txt"
 write "una linea",!
 close "/tmp/datos.txt"
```

**`use` redirige TODA la entrada y salida al dispositivo indicado.** A partir de ese momento, `write`
escribe ahí y `read` lee de ahí, sin pasar un descriptor a ninguna función. Es una variable global de
"dispositivo actual", y viene de la época de los teletipos, donde el programa hablaba con un
terminal físico identificado por un número.

Ese mismo mecanismo sirve para todo: terminales, impresoras, ficheros, tuberías y —en las
implementaciones modernas— **sockets TCP**:

```mumps
 open dispositivo:(connect="servidor:80:TCP")
```

Es simple y es la forma más global de estado que se ha visto en el curso: **una rutina que llame a
otra puede cambiarle el dispositivo de salida sin que se entere**. De ahí que el idioma disciplinado
sea guardar y restaurar el dispositivo con `$io`:

```mumps
 set anterior = $io
 use fichero
 ...
 use anterior
```

Otra vez el patrón de guardar y restaurar de la clase 096, esta vez a mano.

Y `$zseek`, `$zwidth` y las extensiones `$z` de cada implementación cubren lo demás — el prefijo `$z`
es, por convención del estándar, **el espacio reservado para las extensiones del fabricante**, que es
lo más parecido a un mecanismo de extensión que tiene el lenguaje.
"""),
        "smalltalk": ("""
| linea npal dentro |

linea := stdin nextLine.

npal := 0.
dentro := false.
linea do: [ :c |
    c = $  " un espacio "
        ifTrue: [ dentro := false ]
        ifFalse: [ dentro ifFalse: [ npal := npal + 1. dentro := true ] ] ].

Transcript
    show: 'palabras=', npal printString;
    show: ' caracteres=', linea size printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene la relación más peculiar de toda la página
con los ficheros, y la razón es la clase 041: **el sistema vive en una imagen**, y la imagen ya es
persistente.

Un objeto creado hoy **sigue ahí mañana** sin guardarlo en ningún sitio. La pregunta "¿cómo guardo mi
estado?" no se hace de la misma manera que en un lenguaje donde el proceso muere y se lleva todo.

Cuando sí hacen falta ficheros, el modelo es el **flujo**, con la misma jerarquía que las colecciones
(clase 089):

```smalltalk
'datos.txt' asFileReference readStreamDo: [ :flujo |
    [ flujo atEnd ] whileFalse: [ Transcript show: flujo nextLine ] ].

'salida.txt' asFileReference writeStreamDo: [ :flujo |
    flujo nextPutAll: 'hola'; nl ].
```

Y aquí está lo interesante: **`ReadStream` y `WriteStream` funcionan igual sobre una colección en
memoria que sobre un fichero**.

```smalltalk
ReadStream on: #(1 2 3 4)          "un flujo sobre un ARRAY"
ReadStream on: 'texto'              "sobre una cadena"
WriteStream on: String new          "construir texto por trozos (clase 093)"
```

Que el flujo sea una abstracción sobre **cualquier secuencia** y no solo sobre ficheros es de 1980, y
es la misma idea que después normalizaron Java con `InputStream` y .NET con `Stream`. El
`istringstream` de C++ de esta misma clase es lo mismo, llegado cinco años después.

Y para la distinción de esta clase, Pharo separa explícitamente:

```smalltalk
flujo binary.                     "bytes crudos"
flujo ascii.
ZnCharacterReadStream on: flujo encoding: 'utf8'
```

**La codificación es una capa que se envuelve alrededor del flujo binario**, no una opción de la
apertura. Es el mismo diseño que las capas de Perl y el `fconfigure` de Tcl, y es el correcto: **un
fichero siempre es bytes, y el texto es una interpretación**.
"""),
    },
)
