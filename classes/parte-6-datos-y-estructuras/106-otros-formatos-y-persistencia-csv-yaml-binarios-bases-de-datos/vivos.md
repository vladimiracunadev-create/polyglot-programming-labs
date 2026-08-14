# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 106

> [⬅️ Volver a la clase 106](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Unir unos valores con comas. La última clase de la Parte 6 cierra el recorrido por los datos con el
formato más viejo y más subestimado de todos: **CSV es anterior a casi todos estos lenguajes** —viene
de las tarjetas perforadas y del formato *comma-separated* de FORTRAN— y sigue moviendo más datos
empresariales que JSON. Y esconde una trampa que ha arruinado más migraciones que ningún otro
formato.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **persistencia y el intercambio**, y estos lenguajes lo enseñan porque son los
> que llevan sesenta años haciéndolo. **COBOL, RPG y PL/I no ven CSV como un formato de texto**: lo ven
> como un caso pobre del registro con estructura que ya manejaban, y les falta lo que a ellos les
> sobraba —**tipos, longitudes y una definición compartida**.
>
> Y ese contraste es la lección: **CSV no tiene esquema**, y por eso es universal y por eso falla. El
> `FD` de COBOL, la `DDS` de IBM i y el `DECLARE` de PL/I **son el esquema que a CSV le falta**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `csv=<valores separados por coma> campos=<cantidad>`
- **Regla:** `csv = unir con coma ; campos = cantidad de valores`

| stdin | esperado |
|---|---|
| `1 2 3` | `csv=1,2,3 campos=3` |
| `5` | `csv=5 campos=1` |
| `10 20` | `csv=10,20 campos=2` |

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
PROGRAM-ID. ACSV.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2) COMP VALUE 0.
01  I       PIC 9(4) COMP.
01  L       PIC 9(4) COMP.
01  N       PIC 9(4) COMP VALUE 0.
01  SALIDA  PIC X(200) VALUE SPACES.
01  SPOS    PIC 9(4) COMP VALUE 1.
01  ED-N    PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM CERRAR-TOKEN
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM CERRAR-TOKEN

    COMPUTE L = SPOS - 1
    MOVE N TO ED-N
    DISPLAY "csv=" SALIDA(1:L) " campos=" FUNCTION TRIM(ED-N)
    STOP RUN.

CERRAR-TOKEN.
    IF TLEN > 0
        ADD 1 TO N
        IF N > 1
            MOVE "," TO SALIDA(SPOS:1)
            ADD 1 TO SPOS
        END-IF
        MOVE TOKEN(1:TLEN) TO SALIDA(SPOS:TLEN)
        ADD TLEN TO SPOS
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** COBOL puede generar CSV con `STRING` y `DELIMITED BY`, y en la
práctica lo hace constantemente — **el CSV es el idioma en que el mainframe habla con el resto del
mundo desde hace décadas**.

```cobol
STRING CLI-ID     DELIMITED BY SIZE  ","
       FUNCTION TRIM(CLI-NOMBRE) DELIMITED BY SIZE  ","
       CLI-SALDO  DELIMITED BY SIZE
    INTO LINEA-CSV
    WITH POINTER POS
END-STRING
```

Y en sentido inverso, `UNSTRING ... DELIMITED BY ","` reparte los campos.

Ahora bien, la advertencia del cierre de esta clase es especialmente grave aquí, por una razón
concreta: **los campos COBOL vienen de registros de longitud fija con contenido arbitrario**. Un
nombre puede llevar una coma —"García, S.L."— y ese `STRING` produce un CSV **con un campo de más**,
en silencio. Es un error clásico de las interfaces entre sistemas.

Lo correcto es escapar según RFC 4180 —entrecomillar el campo y duplicar las comillas de dentro— o
usar la utilidad del sistema, que es lo habitual: **DFSORT y SyncSort convierten registros de longitud
fija a CSV** con una sentencia de control, y lo hacen bien.

Y esta clase es buen sitio para el argumento de fondo: **COBOL tiene lo que a CSV le falta**. El
`FD` con su `01` declara **nombre, tipo, longitud y posición de cada campo**, y esa definición vive en
un copybook compartido por todos los programas que tocan el fichero (clase 088).

```cobol
FD  CLIENTES.
01  REG-CLIENTE.
    05  CLI-ID     PIC 9(9).
    05  CLI-SALDO  PIC S9(11)V99 COMP-3.
```

Un CSV con la misma información **pierde el tipo, la escala decimal y la longitud**, y quien lo lea
tiene que adivinarlos. Por eso las migraciones de mainframe a plataformas modernas fallan tan a menudo
por los datos y no por la lógica: **el esquema estaba en el copybook, y el CSV no lo lleva**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program acsv
   implicit none
   integer :: v(100), n, ios, i
   character(len=400) :: linea, salida
   character(len=20)  :: buf

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   salida = ''
   do i = 1, n
      write(buf, '(I0)') v(i)
      if (i == 1) then
         salida = trim(buf)
      else
         salida = trim(salida) // ',' // trim(buf)
      end if
   end do

   write(*, '(A,I0)') 'csv=' // trim(salida) // ' campos=', n
end program acsv
```

**Lo que esta clase enseña en Fortran.** Fortran tiene una relación directa con este formato que casi
nadie conoce: **la lectura con formato libre —`read(*, *)`— acepta la coma como separador desde
1957**.

```fortran
read(*, *) a, b, c        ! lee "1, 2, 3" y también "1 2 3"
```

Esa es una de las razones por las que el formato *comma-separated* se llamó así y se popularizó: era
lo que las tarjetas de datos de FORTRAN ya aceptaban. **CSV es, en parte, un fósil del formato de
entrada de Fortran.**

Y Fortran 2003 añadió el modo que lo cierra del todo:

```fortran
write(10, '(*(G0,:,","))') v          ! separado por comas, sin espacios
read(10, *, delim='quote') texto
open(10, file='d.csv', delim='quote')  ! ENTRECOMILLA las cadenas al escribir
```

**`delim='quote'`** hace que la escritura con formato libre entrecomille las cadenas, que es
exactamente lo que pide RFC 4180. Y el descriptor `G0` —Fortran 2008— escribe **cualquier tipo con la
anchura mínima**, lo que elimina el problema de los espacios de relleno que arrastraban los formatos
`I` y `F`.

El `(*(G0,:,","))` del ejemplo merece desmontarse: `*` es repetición ilimitada, `G0` la anchura
mínima, y **`:` es el descriptor de terminación** — detiene el formato cuando se acaban los datos, de
modo que **no se escribe una coma final**. Ese `:` resuelve el problema del separador sobrante que en
otros lenguajes obliga a un `if` dentro del bucle, y está en Fortran desde 1977.

Sobre persistencia, el ecosistema científico se ha movido a formatos que CSV no puede cubrir:
**NetCDF** y **HDF5**, ambos con enlaces oficiales para Fortran, que guardan **arreglos
multidimensionales con metadatos, comprimidos y con acceso parcial**. Un modelo climático no escribe
CSV: escribe NetCDF, y ese fichero lleva las unidades, las coordenadas y la procedencia dentro.

Es exactamente la información que a CSV le falta, resuelta en el otro extremo del espectro.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Acsv is
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
   N      : Natural := 0;
begin
   Get_Line (Linea, Ultimo);

   Put ("csv=");

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      N := N + 1;
      if N > 1 then
         Put (",");
      end if;
      Put (Valor, Width => 1);
      Pos := Fin + 1;
   end loop;

   Put (" campos=");
   Put (N, Width => 1);
   New_Line;
end Acsv;
```

**Lo que esta clase enseña en Ada.** Ada no tiene CSV en el estándar, y su ecosistema tiene varias
opciones —`Ada_CSV`, el paquete CSV de GNATCOLL— pero lo interesante de esta clase en Ada está en otro
sitio: **en cómo Ada trata la persistencia con seguridad de tipos**.

Ya se vio en la clase 104 con `Ada.Sequential_IO` y `Ada.Direct_IO`, ficheros ligados a un tipo. Y
`Ada.Streams` con los atributos `'Write` y `'Read` da serialización binaria automática para cualquier
tipo, incluidos registros con variantes.

Lo que añade esta clase es **`GNATCOLL.SQL`**, que resuelve la persistencia de verdad de una forma que
merece verse:

```ada
--  Generado desde el ESQUEMA de la base de datos:
Q : constant SQL_Query :=
      SQL_Select (Fields  => Clientes.Nombre & Clientes.Saldo,
                  From    => Clientes,
                  Where   => Clientes.Saldo > 1000);
```

Eso **no es SQL en una cadena**: `Clientes.Nombre` es un objeto Ada tipado, generado a partir del
esquema real por una herramienta. El compilador comprueba que el campo existe, que el tipo de la
comparación encaja y que la consulta está bien formada.

Con eso, **una consulta mal escrita no compila**, y la inyección SQL es imposible por construcción —
no hay concatenación de texto que envenenar.

Es la misma idea que en RPG hace `extname` (clase 099) y que en el mundo moderno hacen Diesel en Rust
y jOOQ en Java: **el esquema de la base de datos convertido en tipos del lenguaje**.

Y conecta con el cierre de esta clase de forma directa: **el problema de CSV es que no tiene esquema**.
Todas las soluciones serias de persistencia de esta página —el `FD` de COBOL, la DDS de IBM i, el
`file of T` de Pascal, `Sequential_IO` de Ada, NetCDF en Fortran— consisten en **poner el esquema
donde el programa pueda verlo**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Acsv;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok, Salida: string;
  I, N: Integer;
  C: Char;

begin
  ReadLn(Linea);

  Salida := '';
  N := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Inc(N);
        if Salida <> '' then Salida := Salida + ',';
        Salida := Salida + Tok;
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('csv=', Salida, ' campos=', IntToStr(N));
end.
```

**Lo que esta clase enseña en Pascal.** Free Pascal y Delphi traen CSV hecho, y la clase que lo hace
es la de la clase 095: **`TStringList`**.

```pascal
var L: TStringList;
begin
  L := TStringList.Create;
  try
    L.Delimiter := ',';
    L.StrictDelimiter := True;      { NO partir también por espacios }
    L.QuoteChar := '"';
    L.DelimitedText := '1,"García, S.L.",3';
    WriteLn(L.Count);                { 3 -- respeta las comillas }
    WriteLn(L[1]);                    { García, S.L. }
  finally
    L.Free;
  end;
end;
```

**`DelimitedText` con `QuoteChar` implementa el entrecomillado de RFC 4180**, así que un campo con
comas dentro se lee bien. Es exactamente lo que el cierre de esta clase pide y lo que un
`split(',')` no hace.

Y `StrictDelimiter := True` merece la advertencia: **sin él, `TStringList` parte también por espacios
y por tabuladores**, por compatibilidad con su comportamiento original. Es una de las trampas más
conocidas del ecosistema, y la causa de muchos CSV mal leídos.

Para persistencia de verdad, Pascal tiene tres capas que conviene conocer:

- **`file of T`** (clase 104): registros tipados con acceso aleatorio, la base de datos casera de
  Turbo Pascal.
- **`TDataset`** y sus descendientes: la abstracción de conjunto de resultados de Delphi, con
  `TSQLQuery`, `TBufDataset` y controles visuales que se enlazan a ella. Es de 1995 y es el
  antepasado directo de `DataSet` en .NET, con el mismo autor detrás (clase 073).
- **Bases de datos empotradas**: `SQLdb` con SQLite, Firebird, PostgreSQL y MySQL, todo con la misma
  interfaz.

Y ese `TDataset` con controles enlazados es lo que hizo a Delphi dominante en aplicaciones de gestión
en los noventa: **arrastrar una tabla a un formulario y tener una aplicación funcionando**. Es la
misma promesa que hoy hacen las herramientas de bajo código, con treinta años de diferencia.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((v '()))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (push x v))
  (setf v (nreverse v))
  (format t "csv=~{~D~^,~} campos=~D~%" v (length v)))
```

**Lo que esta clase enseña en Common Lisp.** La directiva **`~{~D~^,~}`** resuelve el problema del
separador en una expresión, y merece desmontarse porque es de las cosas más útiles de `format`:

- **`~{ ... ~}`** itera sobre una lista.
- **`~D`** imprime cada elemento como entero.
- **`~^`** es *escape si no queda nada*: **termina la iteración si no hay más elementos**, así que la
  coma que va detrás **no se imprime tras el último**.

Ese `~^` es el equivalente del `:` de Fortran de esta misma clase, y los dos resuelven el mismo
problema: **el separador que no debe ir al final**. En los lenguajes sin esa facilidad hay que poner
un `if` dentro del bucle, que es lo que hacen casi todos los programas de esta página.

`format` tiene además directivas condicionales y de alineación que lo convierten en un pequeño
lenguaje:

```lisp
(format t "~:[no~;sí~]" x)            ; condicional booleano
(format t "~[cero~;uno~;dos~:;muchos~]" n)   ; selección por índice
(format t "~10:@<~A~>" texto)          ; centrar en 10 columnas
(format t "~,,' ,3:D" 1234567)          ; 1 234 567 -- separador de MILES
(format t "~R" 42)                       ; "cuarenta y dos" en inglés
```

La última existe de verdad y es célebre por su gratuidad. `~:D` con separador de miles, en cambio, es
sorprendentemente práctica y no la tiene casi nadie.

Para CSV real, el ecosistema tiene `cl-csv` y `fare-csv`, con manejo correcto de comillas y saltos de
línea embebidos.

Y para persistencia, Common Lisp tiene una opción que no tiene ningún otro lenguaje de esta página:
**guardar la imagen entera**.

```lisp
(sb-ext:save-lisp-and-die "mi-app" :executable t)
```

Eso escribe **todo el estado del sistema** —funciones, datos, variables globales— en un ejecutable que
al arrancar continúa donde estaba. Es el modelo de imagen de Smalltalk (clase 041), disponible en
SBCL, y se usa tanto para desplegar aplicaciones como para no repetir una carga costosa.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set v [split [string trim $linea]]

puts "csv=[join $v ,] campos=[llength $v]"
```

**Lo que esta clase enseña en Tcl.** `join $v ,` y ya está. Y aquí conviene ser explícito sobre el
aviso del cierre, porque en Tcl la tentación es máxima: **`split $linea ,` NO es un lector de CSV**.

```tcl
split {1,"García, S.L.",3} ,      ;# {1 {"García} { S.L."} 3} -- CUATRO campos, mal
```

Tcllib trae el paquete correcto, y hace lo que hay que hacer:

```tcl
package require csv

csv::split {1,"García, S.L.",3}      ;# {1 {García, S.L.} 3} -- bien
csv::join {1 {García, S.L.} 3}        ;# entrecomilla lo que hace falta
csv::split -alternate ...              ;# el dialecto de Excel
csv::read2matrix $canal m , auto       ;# leer un fichero entero a una matriz
```

`csv::join` **entrecomilla automáticamente los campos que contienen el separador, comillas o saltos de
línea**. Es la diferencia entre generar CSV y generar CSV correcto.

Y sobre persistencia, Tcl tiene una integración que sorprende por lo cómoda: **SQLite fue escrito por
D. Richard Hipp con una interfaz para Tcl como objetivo de diseño**, y esa relación se nota.

```tcl
package require sqlite3
sqlite3 db mi.db
db eval {SELECT nombre, saldo FROM clientes WHERE saldo > $minimo} {
    puts "$nombre: $saldo"
}
```

Fíjate en dos cosas. **`$minimo` dentro del SQL no es interpolación de cadena**: SQLite lo convierte
en un **parámetro enlazado**, así que la inyección SQL es imposible. Y **las columnas se convierten en
variables Tcl dentro del bloque**, sin recorrer un cursor ni pedir campos por índice.

Esa integración es de las más limpias que existen entre un lenguaje y una base de datos, y es
consecuencia directa de que SQLite naciera dentro del ecosistema Tcl. Hoy SQLite es la base de datos
más desplegada del mundo —está en todos los móviles y todos los navegadores— y su suite de pruebas,
con millones de casos, **sigue escrita en Tcl**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

print "csv=", join(',', @v), " campos=", scalar(@v), "\n";
```

**Lo que esta clase enseña en Perl.** `join(',', @v)` y `split` son operaciones básicas del lenguaje, y
por eso Perl es donde más se comete el error del cierre de esta clase: **`split /,/` parece suficiente
y no lo es**.

La respuesta correcta es **`Text::CSV`** —o `Text::CSV_XS`, su versión en C—, y su interfaz enseña
todo lo que CSV esconde:

```perl
use Text::CSV;

my $csv = Text::CSV->new({
    binary       => 1,        # campos con caracteres no ASCII
    sep_char     => ';',      # el separador español
    quote_char   => '"',
    escape_char  => '"',
    eol          => "\r\n",   # fin de línea de Windows
    allow_whitespace => 1,
    auto_diag    => 1,
});

$csv->combine(@campos) and print $csv->string;
while (my $fila = $csv->getline($fh)) { ... }
$csv->column_names($csv->getline($fh));       # usar la CABECERA
my $h = $csv->getline_hr($fh);                 # cada fila como HASH
```

Cada una de esas opciones existe porque alguien se encontró con un CSV que la necesitaba. Es la mejor
documentación posible de que **el formato no es simple**.

Y `getline_hr` —cada fila como un hash con las claves de la cabecera— es lo que convierte un CSV en
algo cómodo de manejar, y es el equivalente pobre del esquema del que habla esta clase.

Para persistencia, Perl tiene **DBI**, que merece un lugar en la historia: es de **1994** y fue **la
primera interfaz de base de datos independiente del motor** de un lenguaje de guion.

```perl
use DBI;
my $dbh = DBI->connect("dbi:Pg:dbname=mi", $usuario, $clave);
my $sth = $dbh->prepare("SELECT nombre FROM clientes WHERE saldo > ?");
$sth->execute($minimo);
while (my $f = $sth->fetchrow_hashref) { ... }
```

**El `?` con `execute` es un parámetro enlazado**, no interpolación: la defensa correcta contra la
inyección SQL, disponible desde 1994.

DBI es el antepasado directo de JDBC —que llegó en 1997, tres años después— y de la DB-API de Python.
Su modelo de controladores intercambiables con una interfaz común es hoy tan obvio que cuesta
recordar que alguien tuvo que inventarlo.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    std::vector<int> v{std::istream_iterator<int>(std::cin),
                       std::istream_iterator<int>()};

    std::cout << "csv=";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i != 0) std::cout << ',';
        std::cout << v[i];
    }
    std::cout << " campos=" << v.size() << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** El bucle con `if (i != 0)` es el idioma universal del separador
que no va al final, y es lo que Fortran resuelve con `:` y Lisp con `~^`. C++20 lo alivió con las
*ranges*:

```cpp
#include <ranges>
std::cout << (v | std::views::join_with(',') | ...);   // C++23
```

Y **la biblioteca estándar no tiene CSV**, como no tiene JSON ni grafos. El ecosistema lo cubre con
`fast-cpp-csv-parser`, `csv2` y `rapidcsv`, y el primero es interesante porque **usa plantillas para
declarar las columnas y sus tipos**:

```cpp
io::CSVReader<3> in("datos.csv");
in.read_header(io::ignore_extra_column, "id", "nombre", "saldo");
int id; std::string nombre; double saldo;
while (in.read_row(id, nombre, saldo)) { ... }
```

Eso es, otra vez, **poner el esquema donde el compilador lo vea** — el tema que recorre toda esta
clase.

Para persistencia, C++ tiene desde 2017 lo que le faltaba desde 1985:

```cpp
#include <filesystem>
namespace fs = std::filesystem;

for (const auto& e : fs::directory_iterator("/datos")) {
    if (e.path().extension() == ".csv") { ... }
}
fs::file_size(p);  fs::last_write_time(p);  fs::create_directories(p);
```

**`<filesystem>`** llegó en C++17, adoptado de Boost, y resolvió por fin las rutas, los directorios y
los metadatos de forma portable. Antes, cada proyecto tenía su capa sobre POSIX y Win32.

Y para bases de datos, C++ sigue sin una interfaz estándar: se usa la API en C del motor —libpq,
SQLite, MySQL— o envoltorios como SOCI y `sqlite_orm`. Es una de las carencias más señaladas del
lenguaje frente a Java, C# y Python, y refleja una decisión consciente del comité: **el estándar de
C++ evita todo lo que dependa de un sistema externo**.

Esa política explica a la vez su portabilidad extrema y por qué hacen falta tantas bibliotecas para
cosas cotidianas.

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

dcl-pi ACSV;
  entrada char(200) const;
end-pi;

dcl-s texto  varchar(200);
dcl-s tok    varchar(20) inz('');
dcl-s salida varchar(200) inz('');
dcl-s c      char(1);
dcl-s i      int(10);
dcl-s n      int(10) inz(0);

texto = %trimr(entrada);

for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      n += 1;
      if salida <> '';
        salida += ',';
      endif;
      salida += tok;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('csv=' + salida + ' campos=' + %char(n));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG genera CSV con concatenación, como este programa, y **no lo
necesita casi nunca**: en IBM i, exportar una tabla a CSV es una sentencia SQL.

```sql
CALL QSYS2.QCMDEXC('CPYTOIMPF FROMFILE(BIBLIO/CLIENTES)
                    TOSTMF(''/tmp/clientes.csv'')
                    RCDDLM(*CRLF) STRDLM(''"'') FLDDLM('','')');
```

**`CPYTOIMPF`** —copiar a fichero de importación— y su inverso `CPYFRMIMPF` son órdenes del sistema
operativo que convierten entre tablas de base de datos y ficheros de texto delimitado, **con
entrecomillado correcto, control de codificación y conversión de tipos**. Existen desde los años
noventa.

Es la misma conclusión que en COBOL con DFSORT: **la conversión de formatos la hace la plataforma**.

Y esta clase cierra la parte con lo que mejor resume a IBM i, que es su integración de datos.
**Un fichero de base de datos en IBM i tiene un esquema en el sistema**, definido con DDS o con
`CREATE TABLE`, y ese esquema está disponible para todo:

```rpgle
dcl-f CLIENTES;                             // los campos aparecen COMO VARIABLES
dcl-ds cliente extname('CLIENTES') end-ds;  // o como estructura (clase 099)

exec sql select * from clientes into :cliente;   // o por SQL, a la misma estructura
```

**Las tres formas acceden al mismo objeto**, y el compilador toma la definición del catálogo del
sistema. No hay mapeo objeto-relacional porque no hay dos modelos que mapear.

Ese es el argumento que recorre toda la Parte 6 en los lenguajes de gestión y que conviene dejar
dicho al cerrarla: **COBOL con VSAM, RPG con Db2 integrado y M con los *globals* resolvieron el
problema de la persistencia no construyendo un puente entre el programa y los datos, sino no abriendo
nunca la brecha**.

Es una arquitectura distinta, no una arquitectura antigua.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 acsv: procedure options(main);

    declare linea  char(200) varying;
    declare tok    char(20)  varying initial('');
    declare salida char(200) varying initial('');
    declare c      char(1);
    declare (i, n) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea);
    n = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             n = n + 1;
             if salida ^= '' then salida = salida || ',';
             salida = salida || tok;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('csv=' || salida || ' campos=' || trim(char(n)));

 end acsv;
```

**Lo que esta clase enseña en PL/I.** PL/I tiene una peculiaridad en la entrada y salida de flujo que
conecta directamente con esta clase: **`get list` acepta la coma como separador**, igual que Fortran.

```pli
 get list (a, b, c);      /* lee "1,2,3" y también "1 2 3" */
 put list (a, b, c);       /* escribe separado por espacios */
```

Y tiene un modo que ningún otro lenguaje de esta página ofrece: **`get data` y `put data`**, la
entrada y salida **autodescriptiva**.

```pli
 put data (a, b, c);
```

Eso escribe literalmente:

```text
A=          1 B=          2 C=          3;
```

**Nombre de la variable, signo igual, valor**, terminado en punto y coma. Y `get data` lo lee de
vuelta, **asignando a las variables por su nombre y en cualquier orden**:

```pli
 get data (a, b, c);      /* acepta "C=3, A=1;" y asigna correctamente */
```

Es un formato de intercambio **con esquema incorporado**, en 1964, y hace exactamente lo que a CSV le
falta: los campos van etiquetados. Es, en espíritu, un antepasado de JSON y de las `namelist` de
Fortran.

Se usaba sobre todo para **depuración** —volcar el estado de un programa en una forma legible y
recargable— y esa es todavía su aplicación típica. Su límite es que es propio de PL/I: nadie más lo
lee.

Para persistencia real, un programa PL/I usa `read`/`write` sobre VSAM o **SQL incrustado** contra
DB2, con la misma sintaxis que COBOL:

```pli
 exec sql select nombre into :nombre from clientes where id = :id;
```

Y el CSV, como en COBOL, se genera con la utilidad SORT o con una rutina de conversión — no a mano,
por las razones del cierre de esta clase.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ACSV ; Otros formatos y persistencia -- clase 106
 read linea
 set n = $length(linea, " ")
 set salida = ""
 for i=1:1:n do
 . if salida '= "" set salida = salida _ ","
 . set salida = salida _ $piece(linea, " ", i)
 write "csv=", salida, " campos=", n, !
 quit
```

**Lo que esta clase enseña en M.** El programa usa `$piece` con un delimitador, y ahí está el punto:
**el formato nativo de datos de M ES un CSV con `^` como separador** (clase 090).

```mumps
 set ^PAC(id, 0) = nombre_"^"_fecha_"^"_sexo
 set nombre = $piece(^PAC(id, 0), "^", 1)
```

Cambiar la coma por el acento circunflejo no es casualidad: **se eligió un carácter que casi nunca
aparece en texto médico**, evitando exactamente el problema de escape que el cierre de esta clase
señala. Es una solución pragmática de los años setenta que sigue funcionando.

Y `$piece` es tan directo para esto que M convierte a CSV cambiando un carácter:

```mumps
 set csv = $translate(^PAC(id, 0), "^", ",")
```

Con el aviso de siempre: **si un campo lleva una coma, esto rompe**. La utilidad depende de que los
datos no la contengan.

Sobre persistencia, esta clase cierra la parte donde M la empezó: **M no tiene el problema de la
persistencia**. Un *global* es la estructura de datos y la base de datos a la vez (clases 089, 095,
097 y 098), y no hay serialización, ni conexión, ni mapeo, ni caché que invalidar.

Lo que las plataformas modernas de M añadieron es **hablar los formatos de los demás**:

- **InterSystems IRIS** es una base de datos **multimodelo**: los mismos datos se ven como *globals*,
  como objetos, como **tablas SQL** y como **documentos JSON**, sin copiarlos ni convertirlos.
- **YottaDB** ofrece enlaces con Python, Node.js, Go y Rust, y un modo de trabajo en el que la lógica
  se escribe en cualquiera de esos y los datos siguen en *globals*.
- Y las dos hablan **FHIR** (clase 105), que es el JSON del mundo sanitario.

Ese es el resumen de la Parte 6 vista desde el lenguaje más antiguo de la página: **el problema nunca
fue guardar los datos, sino compartirlos**. M resolvió lo primero en 1966 y ha dedicado los últimos
veinte años a lo segundo.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v salida |

v := stdin nextLine substrings.

salida := v inject: '' into: [ :acc :cada |
    acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, ',', cada ] ].

Transcript
    show: 'csv=', salida;
    show: ' campos=', v size printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** El `inject:into:` con la comprobación de vacío es el idioma
del separador, y Smalltalk tiene una forma mejor que ya apareció en la clase 093:

```smalltalk
String streamContents: [ :flujo |
    v do: [ :cada | flujo nextPutAll: cada ]
      separatedBy: [ flujo nextPut: $, ] ]
```

**`do:separatedBy:`** ejecuta el segundo bloque **entre** elementos, nunca al final. Es el `~^` de
Lisp y el `:` de Fortran, expresado como un mensaje de la jerarquía de colecciones — y disponible
sobre cualquier colección, incluidos conjuntos y diccionarios.

Y para cerrar la Parte 6, esta clase toca el asunto que en Smalltalk es más peculiar: **la
persistencia**.

Como se dijo en la clase 104, **la imagen ya es persistente**: un objeto creado hoy sigue ahí mañana.
Eso resolvió el problema tan bien que durante años **fue un obstáculo**, porque no había forma de
compartir esos datos con nada que no fuera otra imagen.

La comunidad lo resolvió por capas, y todas están en Pharo hoy:

```smalltalk
STON toString: unObjeto.               "texto legible, con clases y ciclos (clase 105)"
FLSerializer serializeToByteArray: x.   "Fuel: binario, RÁPIDO"
NeoCSV                                   "CSV correcto"
Voyage                                   "objetos en MongoDB"
Glorp                                    "mapeo objeto-relacional"
Garage / P3                              "acceso a PostgreSQL"
```

**Fuel** merece mención: serializa grafos de objetos a binario **manteniendo la identidad y los
ciclos**, y es de las implementaciones más rápidas que existen en cualquier lenguaje. Puede serializar
incluso **clausuras y contextos de método** —los `thisContext` de la clase 096—, lo que permite
guardar un proceso a medias y reanudarlo después, en otra máquina.

Eso último no lo puede hacer casi ningún otro sistema, y resume por qué Smalltalk sigue apareciendo en
esta clase de discusiones: **cuando todo es un objeto y la pila también, serializar el estado del
programa es serializar objetos**.

Y con eso cierra la parte: **cada uno de estos lenguajes resolvió la persistencia con la estructura
que ya tenía** — COBOL con el registro, M con el árbol, Lisp con la lista, Smalltalk con el objeto. Y
los cuatro siguen funcionando.

---

## Y de vuelta a la clase

Lo transferible: **CSV parece trivial y no lo es**. Un campo con una coma, con comillas o con un salto
de línea dentro exige entrecomillado y escape; el separador cambia con la configuración regional —en
España suele ser `;` porque la coma es el decimal—; la codificación no se declara en ninguna parte; y
no hay tipos, así que `007`, `1/2/2026` y `+34 600...` se convierten solos en algo que no eran. **Usa
un lector de CSV de verdad, nunca `split(',')`**. Es la misma advertencia que la clase 105 dio con
JSON, y aquí duele más porque el formato engaña.

⏮️ [Volver a la clase 106](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
