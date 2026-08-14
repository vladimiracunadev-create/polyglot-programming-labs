# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 117

> [⬅️ Volver a la clase 117](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar los pares. Con un bucle es imperativo; **diciendo qué quieres** es declarativo, y aquí hay dos
lenguajes que lo escriben en una expresión: **Fortran con `sum(v, mask=...)`** y Lisp con `loop ...
when ... sum`. Y hay algo más importante: **COBOL, RPG y PL/I llevan sesenta años siendo anfitriones
del lenguaje declarativo más usado del mundo** —SQL— y su relación con él define su arquitectura.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **decir qué en lugar de cómo**, y estos lenguajes lo enseñan porque tienen el
> caso de éxito más grande de la historia del paradigma. **SQL se diseñó en IBM en los años setenta
> para ser incrustado en COBOL y PL/I**, y esa decisión —un lenguaje declarativo dentro de uno
> imperativo— es el modelo que después copiaron LINQ, los ORM y todos los DSL de consulta.
>
> Y **Fortran** aporta el otro caso: su aritmética de arreglos y `do concurrent` son declarativos por
> una razón práctica —**el compilador necesita libertad para optimizar**— que es exactamente la misma
> por la que existe el optimizador de consultas de una base de datos.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `suma_pares=<suma de los pares>`
- **Regla:** `suma de los x tales que x es par`

| stdin | esperado |
|---|---|
| `1 2 3 4` | `suma_pares=6` |
| `2 4 6` | `suma_pares=12` |
| `1 3 5` | `suma_pares=0` |

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
PROGRAM-ID. DECLAR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2)  COMP VALUE 0.
01  I       PIC 9(4)  COMP.
01  VALOR   PIC S9(9) COMP-3.
01  RESTO   PIC S9(9) COMP-3.
01  SUMA    PIC S9(18) COMP-3 VALUE 0.
01  ED-S    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM ACUMULAR-PAR
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM ACUMULAR-PAR

    MOVE SUMA TO ED-S
    DISPLAY "suma_pares=" FUNCTION TRIM(ED-S)
    STOP RUN.

ACUMULAR-PAR.
    IF TLEN > 0
        COMPUTE VALOR = FUNCTION NUMVAL(TOKEN)
        COMPUTE RESTO = FUNCTION MOD(VALOR, 2)
        IF RESTO = 0
            ADD VALOR TO SUMA
        END-IF
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** El programa es imperativo porque la entrada es una línea de
texto, y eso no es COBOL. **El COBOL de verdad escribe esta clase así**:

```cobol
EXEC SQL
    SELECT SUM(IMPORTE) INTO :TOTAL
      FROM MOVIMIENTOS
     WHERE MOD(IMPORTE, 2) = 0
       AND FECHA BETWEEN :DESDE AND :HASTA
END-EXEC
```

Y ahí está el dato histórico que esta clase quiere dejar claro: **SQL nació para esto**.

El lenguaje se diseñó en **IBM San José a mediados de los setenta** —el proyecto System R, y antes
SEQUEL— y **su forma de uso principal era incrustado en COBOL y PL/I**. El precompilador lee las
sentencias `EXEC SQL`, las sustituye por llamadas y comprueba los tipos de las variables de
acogida —las que llevan `:` delante—.

Eso significa que **el primer lenguaje declarativo de éxito masivo se diseñó como huésped de un
lenguaje imperativo**, no como sustituto. Y ese modelo —un DSL declarativo incrustado, con
comprobación en compilación— es el que después reprodujeron LINQ en C#, los *query builders* tipados y
las macros de consulta de Rust.

Y hay una segunda cosa declarativa en COBOL que se mencionó en la clase 107 y que merece cerrar aquí:
**`SORT` con procedimientos de entrada y salida**.

```cobol
SORT FICHERO-TRABAJO
    ON ASCENDING KEY IMPORTE
    INPUT PROCEDURE IS FILTRAR-PARES
    OUTPUT PROCEDURE IS SUMAR
```

`SORT` **dice qué orden se quiere, no cómo ordenar**, y detrás hay una implementación —DFSORT,
SyncSort— con décadas de optimización, que elige entre algoritmos según el volumen y la memoria
disponible, usa varios discos de trabajo y aprovecha instrucciones específicas del hardware.

Es exactamente la relación que describe el cierre de esta clase: **declaras porque hay alguien que
decide mejor que tú**. En el mainframe, ese alguien lleva sesenta años afinándose.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program declar
   implicit none
   integer, allocatable :: v(:)
   integer :: n, ios, i

   character(len=400) :: linea

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      if (allocated(v)) deallocate(v)
      allocate(v(i))
      read(linea, *, iostat=ios) v
      if (ios /= 0) exit
      n = i
   end do
   if (allocated(v)) deallocate(v)
   allocate(v(n))
   read(linea, *) v

   !  Declarativo: se describe QUÉ se suma, no cómo recorrerlo
   write(*, '(A,I0)') 'suma_pares=', sum(v, mask = mod(v, 2) == 0)
end program declar
```

**Lo que esta clase enseña en Fortran.** `sum(v, mask = mod(v, 2) == 0)` es la línea de esta clase, y
merece desmontarla:

- `mod(v, 2)` aplica la operación **a todo el arreglo** y devuelve otro arreglo.
- `== 0` lo compara elemento a elemento y devuelve **un arreglo de lógicos**.
- `sum(..., mask=...)` suma **solo donde la máscara es cierta**.

**Ni un bucle, ni un `if`, ni un acumulador.** Y lo importante no es que sea corto: es que **el
compilador ve la operación completa** y puede vectorizarla, paralelizarla o mandarla a una GPU (clase
114).

La familia de intrínsecas con máscara cubre casi todo lo que una consulta necesita:

```fortran
sum(v, mask=c)      product(v, mask=c)     count(c)
maxval(v, mask=c)   minloc(v, mask=c)       any(c)      all(c)
pack(v, c)           unpack(v, c, campo)
merge(a, b, c)        where (c) v = 0        forall (i=1:n, c(i)) ...
```

Traducidas a SQL, esas líneas son `SUM ... WHERE`, `COUNT`, `MAX`, `EXISTS`, `SELECT ... WHERE` y
`CASE WHEN`. **Es el mismo vocabulario declarativo, aplicado a arreglos en memoria en lugar de a
filas en disco.**

Y la analogía va más lejos de lo que parece. Fortran tiene además:

```fortran
sum(a, dim=2)                  ! reducir por una DIMENSIÓN: es un GROUP BY
matmul(a, b)                    ! una operación completa, no un triple bucle
transpose(a)
```

**`sum(a, dim=2)` sobre una matriz suma cada fila**, produciendo un vector. Eso es agregación por
grupo, y el compilador elige cómo recorrer la memoria para hacerlo rápido — exactamente lo que hace un
motor de base de datos con un `GROUP BY`.

Que las dos comunidades —cálculo numérico y bases de datos— llegaran independientemente a un
vocabulario declarativo con reducciones, filtros y agrupaciones no es casualidad: **las dos tenían un
optimizador capaz de aprovechar la libertad**, que es el argumento del cierre de esta clase.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Declar is
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
   Suma   : Integer := 0;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      if Valor mod 2 = 0 then
         Suma := Suma + Valor;
      end if;
      Pos := Fin + 1;
   end loop;

   Put ("suma_pares=");
   Put (Suma, Width => 1);
   New_Line;
end Declar;
```

**Lo que esta clase enseña en Ada.** Ada no tiene comprensiones de lista ni operaciones sobre arreglos
completos como Fortran, y **Ada 2012 y 2022 le han ido añadiendo un vocabulario declarativo** que
merece verse.

**Las expresiones cuantificadas** (2012), ya mencionadas en la clase 114:

```ada
if (for all I in V'Range => V (I) > 0) then ...
if (for some I in V'Range => V (I) = Buscado) then ...
```

**Cuantificadores lógicos como expresiones normales.** Es `all` y `any` con la sintaxis de las
matemáticas, y su uso principal está en los contratos:

```ada
procedure Ordenar (V : in out Vector)
   with Post => (for all I in V'First .. V'Last - 1 => V (I) <= V (I + 1));
```

**Esa postcondición dice, en una línea, que el vector queda ordenado**, y con SPARK **se demuestra**.
Es especificación declarativa del resultado, que es la forma más pura de "decir qué en lugar de cómo".

**Y las expresiones de agregado iteradas** de Ada 2022:

```ada
Cuadrados : constant Vector := [for I in 1 .. 10 => I * I];
Pares : constant Vector := [for E of V when E mod 2 = 0 => E];
```

Eso **es una comprensión de lista**, con filtro incluido, y llegó a Ada en 2022 — cuarenta años
después del lenguaje y treinta después de que Haskell y Python la popularizaran. Ada es
característicamente lento en adoptar, y característicamente cuidadoso: la sintaxis con corchetes y el
`for ... of ... when` encaja con el resto sin ambigüedades.

Y hay una tercera forma declarativa que es muy de Ada y que esta clase debe nombrar: **los aspectos y
las representaciones**.

```ada
type Registro is record
   Bandera : Boolean;
   Codigo  : Integer range 0 .. 255;
end record
with Size => 16, Bit_Order => High_Order_First;

for Registro use record
   Bandera at 0 range 0 .. 0;      --  el bit exacto
   Codigo  at 0 range 1 .. 8;
end record;
```

**Se declara la disposición binaria exacta** —qué bit ocupa cada campo— y el compilador genera el
código de acceso. Es declarativo aplicado al formato de datos, y es lo que permite escribir en Ada
protocolos de red y registros de hardware sin desplazamientos ni máscaras a mano.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Declar;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Valor, Suma: Integer;
  C: Char;

begin
  ReadLn(Linea);

  Suma := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Valor := StrToInt(Tok);
        if Valor mod 2 = 0 then
          Suma := Suma + Valor;
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('suma_pares=', IntToStr(Suma));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal es imperativo y **su aportación declarativa está en un
sitio que casi nadie mira: el diseño visual y la persistencia de formularios**.

Un formulario de Delphi no se construye con código: **se declara en un fichero `.dfm`**.

```text
object Form1: TForm1
  Caption = 'Clientes'
  object Edit1: TEdit
    Left = 24
    Top = 40
    OnChange = Edit1Change
  end
end
```

Ese fichero es **una descripción declarativa de la interfaz**, y el runtime la lee y construye los
objetos con la RTTI que genera `published` (clases 087 y 105). El programador declara qué hay; el
sistema decide cómo instanciarlo.

Es exactamente el modelo que después usaron XAML en .NET, los `.ui` de Qt, los *layouts* XML de
Android y JSX. **Y el `.dfm` es de 1995.**

Dentro del lenguaje, lo declarativo llegó con los genéricos y las clausuras, y hoy hay bibliotecas que
dan estilo de consulta:

```pascal
uses Spring.Collections;

Suma := TEnumerable.From<Integer>(Lista)
          .Where(function(const X: Integer): Boolean
                 begin Result := X mod 2 = 0 end)
          .Sum;
```

**Spring4D** es la biblioteca comunitaria que trae LINQ a Delphi, con `Where`, `Select`, `OrderBy` y
evaluación perezosa.

Y para las consultas de verdad, Pascal tiene la integración que le dio su cuota de mercado: los
**`TDataset`** con SQL y controles enlazados a datos (clase 106). Un `TSQLQuery` con su SQL, una
rejilla enlazada, y la aplicación funciona. Es declarativo en la capa de datos y en la de interfaz, con
código imperativo solo en medio.

Ese sándwich —**declarar los datos, declarar la interfaz, escribir a mano solo la lógica**— es lo que
hizo a Delphi dominante en aplicaciones de gestión en los noventa, y es exactamente lo que hoy hacen
los marcos de desarrollo web.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((v '()))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (push x v))

  ;;  loop declarativo: qué sumar, con la condición dentro
  (format t "suma_pares=~D~%"
          (loop for x in v when (evenp x) sum x)))
```

**Lo que esta clase enseña en Common Lisp.** `(loop for x in v when (evenp x) sum x)` es una consulta
escrita en inglés, y `loop` —ya presentado en la clase 092— es **el minilenguaje declarativo más
completo del estándar**:

```lisp
(loop for x in v when (evenp x) sum x)
(loop for x in v maximize x)
(loop for x in v count (> x 100))
(loop for x in v collect (* x 2) into dobles finally (return dobles))
(loop for (k . val) in alista when val collect k)
(loop for i from 1 to 10 for x in v collect (cons i x))
```

`sum`, `count`, `maximize`, `minimize`, `collect`, `append`, `thereis`, `always`, `never` son
**cláusulas de agregación**, y su parecido con SQL no es superficial: son las mismas operaciones.

Y aquí está la aportación de Lisp a esta clase, que es mayor que la sintaxis: **la programación
lógica y las bases de datos deductivas se desarrollaron en Lisp**.

- **Planner** (Hewitt, 1969) y **Conniver**: los primeros lenguajes de reglas, en Lisp, y la
  influencia directa de Prolog (clase 118).
- **OPS5** (1977), el lenguaje de sistemas expertos con el **algoritmo RETE** de Charles Forgy, que
  sigue siendo la base de los motores de reglas de negocio actuales —Drools, CLIPS, Jess—.
- **KL-ONE** y las lógicas descriptivas, que son el antepasado de OWL y la web semántica.

Y algo que esta clase debe nombrar por lo extremo: **Screamer**, una biblioteca que añade a Common
Lisp **búsqueda no determinista con retroceso**.

```lisp
(all-values
  (let ((x (an-integer-between 1 10)))
    (unless (evenp x) (fail))
    x))                            ; (2 4 6 8 10)
```

`an-integer-between` **devuelve todos los valores posibles**, `fail` descarta una rama y `all-values`
recoge las que sobreviven. Eso es el motor de Prolog, **implementado como biblioteca sobre un lenguaje
que no lo tenía**, usando continuaciones y macros.

Es el argumento de la clase 107 en su forma más contundente: **Lisp no adopta paradigmas, los
hospeda**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set suma 0
foreach x [split [string trim $linea]] {
    if {$x % 2 == 0} {
        incr suma $x
    }
}

puts "suma_pares=$suma"
```

**Lo que esta clase enseña en Tcl.** Tcl es imperativo y tiene una relación con lo declarativo que es
muy suya: **su especialidad es SER el anfitrión de lenguajes declarativos**.

Dentro del lenguaje, lo más cercano es `lmap` con filtro:

```tcl
set pares [lmap x $lista { expr {$x % 2 == 0 ? $x : [continue]} }]
```

**`continue` dentro de `lmap` descarta el elemento** —una peculiaridad de Tcl 8.6— así que `lmap` hace
de `map` y de `filter` a la vez.

Pero donde Tcl brilla en esta clase es en el uso para el que se diseñó (clase 107): **ser el lenguaje
de configuración y descripción de otras herramientas**. Y ahí, un guion Tcl **se lee como una
declaración**:

```tcl
# Tk: describir una interfaz
pack [button .b -text "Aceptar" -command aceptar] -side left -padx 5
grid [entry .e -textvariable nombre] -row 0 -column 1 -sticky ew

# Vivado / síntesis de circuitos
create_clock -period 10 -name clk [get_ports clk]
set_property PACKAGE_PIN Y9 [get_ports clk]

# ns-3 / simulación de redes
$ns duplex-link $n0 $n2 5Mb 2ms DropTail
```

Esas líneas **son comandos Tcl**, y se leen como un fichero de configuración declarativo. Es la
propiedad que hace que Tcl esté dentro de tantas herramientas profesionales: **la misma sintaxis vale
para describir y para programar**, y cuando la descripción necesita un bucle o una condición, ya está
el lenguaje entero disponible.

Es la diferencia con un YAML o un JSON de configuración, que cuando necesitan lógica obligan a
inventar un lenguaje de plantillas encima — el problema que hoy tienen Helm, Ansible y GitHub Actions.

Y para las consultas de verdad, la integración con SQLite de la clase 106:

```tcl
db eval {SELECT sum(importe) AS total FROM movs WHERE importe % 2 = 0} {
    puts "suma_pares=$total"
}
```

Con las columnas convertidas en variables Tcl dentro del bloque. Es de las integraciones
lenguaje-base de datos más limpias que existen, y no es casualidad: **SQLite se escribió con Tcl como
cliente de referencia**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

my @v = split ' ', $linea;

#  declarativo: filtrar y sumar, sin bucle ni acumulador
print "suma_pares=", sum0(grep { $_ % 2 == 0 } @v), "\n";
```

**Lo que esta clase enseña en Perl.** `sum0(grep { ... } @v)` es una consulta: **filtrar y agregar, en
una expresión**. `sum0` es como `sum` pero devuelve 0 con la lista vacía —de ahí el `0` del nombre—,
que es justo lo que el tercer caso de prueba necesita.

Perl fue **de los primeros lenguajes de uso general con `map`, `grep` y `sort` en la sintaxis** (clase
114), y encadenarlos da el estilo declarativo sin ninguna biblioteca:

```perl
my @resultado =
    sort { $a->{fecha} <=> $b->{fecha} }
    map  { { %$_, total => $_->{base} * 1.21 } }
    grep { $_->{estado} eq 'activo' }
    @registros;
```

Eso es `SELECT ... WHERE ... ORDER BY` escrito de abajo arriba, y el **idioma de la transformación de
Schwartz** —*Schwartzian transform*— es su versión optimizada, con nombre propio en la comunidad Perl:

```perl
my @ordenado =
    map  { $_->[1] }                    # 3. quedarse con el original
    sort { $a->[0] <=> $b->[0] }         # 2. ordenar por la clave
    map  { [ calcular($_), $_ ] }         # 1. calcular la clave UNA vez
    @lista;
```

Calcula la clave de ordenación una sola vez por elemento en lugar de en cada comparación. Es la
optimización que en SQL hace el motor solo y que en Perl se escribe a mano — y que tiene nombre porque
Randal Schwartz la popularizó en un grupo de noticias en 1994.

Y Perl es, junto con COBOL, uno de los grandes anfitriones de lo declarativo, por dos vías:

**Las expresiones regulares** (clase 093), que son un lenguaje declarativo de reconocimiento de
patrones integrado en la sintaxis. **Describes la forma del texto, no cómo recorrerlo**, y un motor
optimizado decide.

**Y DBI** (clase 106), que fue la primera interfaz de base de datos independiente del motor de un
lenguaje de guion.

Es un patrón que recorre esta clase entera: **los lenguajes que mejor hospedan lo declarativo no son
los declarativos, son los que tienen buena sintaxis para incrustarlo**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};

    const int suma = std::accumulate(v.begin(), v.end(), 0,
        [](int acc, int x) { return x % 2 == 0 ? acc + x : acc; });

    std::cout << "suma_pares=" << suma << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** El programa usa `std::accumulate` con una lambda porque el curso
compila con `-std=c++17`. **C++20 permite escribirlo como una consulta**:

```cpp
#include <ranges>

auto pares = v | std::views::filter([](int x) { return x % 2 == 0; });
int suma = std::ranges::fold_left(pares, 0, std::plus{});   // C++23
```

Y ese `|` es deliberadamente **la tubería de Unix**: cada vista transforma la anterior, sin
contenedores intermedios y sin reservar memoria (clase 115).

Lo que hace especial a C++ en esta clase es que **su declarativo se resuelve en compilación**. El tipo
de `pares` es una plantilla anidada que el compilador conoce por completo, así que el bucle final
compila a lo mismo que un bucle con un `if` escrito a mano. **Declarativo con coste cero**, que es
algo que ni SQL ni Fortran pueden prometer.

Y C++ tiene el otro lado del paradigma, ya nombrado en la clase 107: **la metaprogramación con
plantillas es declarativa por naturaleza**.

```cpp
template <typename T>
concept Sumable = requires(T a, T b) { { a + b } -> std::same_as<T>; };

if constexpr (std::is_integral_v<T>) { ... }
static_assert(sizeof(T) <= 8);
```

**Se declaran propiedades que el tipo debe cumplir**, y el compilador comprueba y decide. No hay
ejecución: hay especificación resuelta al compilar.

Para consultas de verdad sobre datos, C++ no tiene nada estándar y el ecosistema ofrece
`sqlpp11` —SQL con comprobación de tipos, en la línea de `GNATCOLL.SQL` de la clase 106— y las APIs en
C de cada motor.

Y merece una nota final que conecta con el cierre: **`std::sort` es un ejemplo perfecto de declarativo
con optimizador**. Dices "ordena esto según este criterio" y la biblioteca elige —introsort, con
inserción para tramos pequeños y montículo si la recursión se descontrola—. Nadie escribe una
ordenación a mano en C++ moderno, y la razón es la del cierre de esta clase: **hay alguien que decide
mejor**.

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

dcl-pi DECLAR;
  entrada char(200) const;
end-pi;

dcl-s texto varchar(200);
dcl-s tok   varchar(20) inz('');
dcl-s c     char(1);
dcl-s i     int(10);
dcl-s valor int(10);
dcl-s suma  int(20) inz(0);

texto = %trimr(entrada);

for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      valor = %int(tok);
      if %rem(valor : 2) = 0;
        suma += valor;
      endif;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('suma_pares=' + %char(suma));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG empezó siendo declarativo (clase 107), se volvió imperativo, y
**hoy es declarativo otra vez** — por SQL.

El programa de arriba es el RPG imperativo. El RPG que se escribe hoy en IBM i es esto:

```rpgle
exec sql
  select sum(importe) into :total
    from movimientos
   where mod(importe, 2) = 0;
```

Y merece verse hasta dónde llega esa integración, porque va mucho más allá de ejecutar consultas.

**SQL como generador de tablas de resultados en el propio lenguaje**:

```rpgle
exec sql declare c cursor for
  select cliente, sum(importe)
    from movimientos group by cliente having sum(importe) > 1000;
exec sql open c;
exec sql fetch c into :cliente, :total;
```

**Funciones de tabla escritas en SQL y usadas como si fueran ficheros**:

```sql
CREATE FUNCTION pares(desde DATE) RETURNS TABLE (...)
  RETURN SELECT ... ;
```

**Y las funciones de servicio de IBM i**, que son la modernización más llamativa de la plataforma:

```sql
SELECT * FROM TABLE(QSYS2.ACTIVE_JOB_INFO());
SELECT * FROM QSYS2.OBJECT_STATISTICS('MIBIB', '*PGM');
SELECT * FROM QSYS2.SYSTEM_STATUS_INFO;
```

**El estado del sistema operativo se consulta con SQL**: los trabajos activos, los objetos, el uso de
disco, los mensajes, las conexiones de red, los certificados. Hay más de trescientas de esas funciones,
y son la forma recomendada de administrar la máquina desde 2014.

Eso es declarativo aplicado a la administración de sistemas, y no lo tiene ninguna otra plataforma con
esa profundidad. Lo que en Linux exige `ps`, `df`, `netstat` y analizar su salida, aquí es una consulta
con `WHERE` y `ORDER BY` — y con el optimizador decidiendo cómo obtenerlo.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 declar: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare (i, valor) fixed binary(31);
    declare suma fixed binary(31) initial(0);

    get edit (linea) (a(200));
    linea = trim(linea);

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             valor = tok;
             if mod(valor, 2) = 0 then suma = suma + valor;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('suma_pares=' || trim(char(suma)));

 end declar;
```

**Lo que esta clase enseña en PL/I.** PL/I es, con COBOL, **uno de los dos lenguajes para los que se
diseñó el SQL incrustado**, y el precompilador de DB2 los trata igual:

```pli
 exec sql
    select sum(importe) into :total
      from movimientos
     where mod(importe, 2) = 0;

 if sqlcode ^= 0 then call error_sql();
```

**`SQLCODE`** —la variable de estado que el precompilador declara— es de 1981 y sigue siendo el
mecanismo estándar de comprobación de errores en SQL incrustado, junto con `SQLSTATE`.

Y PL/I tiene una ventaja concreta sobre COBOL como anfitrión de SQL, que explica por qué se usó tanto
en el software de sistemas de IBM: **sus tipos encajan mejor**. `fixed decimal(11,2)` es exactamente
`DECIMAL(11,2)`, `char(n) varying` es `VARCHAR(n)`, y los punteros permiten manejar áreas de descriptor
—las **SQLDA**— para consultas cuya forma no se conoce hasta ejecutar:

```pli
 exec sql prepare s from :sentencia;
 exec sql describe s into :sqlda;
 exec sql execute s using descriptor :sqlda;
```

Eso es **SQL dinámico**: construir la consulta en ejecución y descubrir su forma —cuántas columnas, de
qué tipos— consultando un descriptor. Es lo que hacen JDBC y ODBC por dentro, y en PL/I se escribe
directamente porque el lenguaje tiene punteros y estructuras basadas.

Y aquí conviene señalar lo que esta clase quiere dejar claro sobre estos tres lenguajes: **COBOL, PL/I
y RPG no son "lenguajes imperativos antiguos" en su uso real — son la capa imperativa de un sistema
cuya capa de datos es declarativa desde hace cuarenta años**.

La arquitectura que hoy se describe como "lógica de negocio en el lenguaje, consultas en SQL, con
comprobación de tipos en la frontera" **es literalmente la arquitectura de un programa PL/I con SQL
incrustado de 1985**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DECLAR ; Declarativo -- clase 117
 read linea
 set suma = 0
 for i=1:1:$length(linea, " ") do
 . set x = $piece(linea, " ", i)
 . if x#2 = 0 set suma = suma + x
 write "suma_pares=", suma, !
 quit
```

**Lo que esta clase enseña en M.** M es imperativo puro y no tiene nada declarativo en el lenguaje —ni
comprensiones, ni agregaciones, ni consultas—. El `#` del programa es el operador módulo, una de las
abreviaturas características de M.

Y sin embargo, esta clase tiene mucho que contar en M, porque **la comunidad M construyó su capa
declarativa encima y lleva cuarenta años usándola**.

**FileMan** (clases 087 y 099) no es solo un diccionario de datos: **es un lenguaje de consulta**.

```text
VA FileMan 22.2
Select OPTION: PRINT FILE ENTRIES
OUTPUT FROM WHAT FILE: PATIENT
SORT BY: NAME
START WITH NAME: A//
FIRST PRINT FIELD: NAME
THEN PRINT FIELD: DATE OF BIRTH
```

Eso es un `SELECT ... ORDER BY` con una interfaz de preguntas, y **el usuario final lo usa sin
programar**. FileMan genera el recorrido óptimo de los índices y produce el informe.

Y hay más, en la misma línea:

- **El lenguaje de búsqueda de FileMan**, con condiciones compuestas y expresiones de campo calculado.
- **Los *computed fields***, que son campos definidos por una expresión M guardada como dato (clase
  113) — columnas calculadas, en 1982.
- **MUMPS SQL** y los pasarelas ODBC, que exponen los *globals* como tablas relacionales.

Y la modernización va justo por ahí: **InterSystems IRIS ofrece SQL completo sobre los mismos
globals**, con optimizador de consultas, índices bitmap y ejecución paralela.

```sql
SELECT AVG(edad) FROM Hospital.Paciente WHERE servicio = 'CARDIO'
```

Esa consulta se ejecuta sobre la misma estructura que un programa M recorre con `$order`, **sin copiar
ni convertir nada**.

Es la conclusión que esta clase busca: **lo declarativo no necesita que el lenguaje lo sea, necesita un
motor que decida el cómo**. M puso el motor en la capa de datos y dejó el lenguaje como estaba — que
es exactamente lo que hicieron COBOL, RPG y PL/I con SQL.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v suma |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

"select: filtra, inject:into: agrega -- una consulta en dos mensajes"
suma := (v select: [ :cada | cada even ])
            inject: 0 into: [ :acc :cada | acc + cada ].

Transcript show: 'suma_pares=', suma printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** `select:` seguido de `inject:into:` **es una consulta**:
filtrar y agregar, con dos mensajes y sin bucle. El protocolo de colecciones (clase 089) es un
vocabulario declarativo completo, y lo es desde 1980.

Lo que Smalltalk aporta específicamente a esta clase es una idea que se adelantó veinte años a lo que
hoy es normal: **la consulta como objeto**.

```smalltalk
| consulta |
consulta := [ :cada | cada edad > 65 ].
pacientes select: consulta.
```

Un bloque es un objeto (clase 083), así que **el criterio se puede guardar, pasar, componer y meter en
una colección**. Es exactamente lo que en .NET son las expresiones lambda de LINQ y lo que en Java son
los `Predicate`.

Y va más lejos con **`MessageSend`** (clase 115) y con la reflexión: en Smalltalk **se puede
inspeccionar un bloque, ver sus variables capturadas y su código fuente**, que es lo que LINQ necesita
para traducir una lambda a SQL y que en .NET exige el tipo especial `Expression<Func<>>`.

Sobre bases de datos, el ecosistema Smalltalk tiene lo esperable —**Glorp** como mapeador
objeto-relacional, **Voyage** para MongoDB— y una idea propia que merece nombrarse: **GemStone/S**.

**GemStone es una base de datos de objetos Smalltalk**: los objetos viven en una imagen compartida y
persistente, con transacciones, y **el código de consulta es Smalltalk normal**.

```smalltalk
(Paciente allInstances select: [ :p | p edad > 65 ]) size
```

Esa línea **se ejecuta sobre millones de objetos persistentes**, con índices que GemStone mantiene, y
sin ninguna traducción a otro lenguaje. Es la promesa de "sin impedancia objeto-relacional" cumplida
de verdad, y lleva funcionando desde 1986 en sistemas financieros y logísticos.

Es el mismo argumento que IRIS en la página de M (clase 110) y desde el lado contrario: **en lugar de
enseñar SQL al lenguaje de objetos, hacer que la base de datos hable objetos**.

Las dos soluciones existen, las dos funcionan, y las dos llevan décadas siendo minoritarias frente al
ORM — que es la peor de las tres y la que ganó.

---

## Y de vuelta a la clase

Lo transferible: **declarar en lugar de ordenar sirve cuando hay alguien capaz de decidir mejor que
tú, y solo entonces**. Un optimizador de SQL con estadísticas de las tablas elige un plan que tú no
elegirías; un compilador de Fortran vectoriza mejor de lo que tú lo harías a mano. Cuando no hay tal
optimizador, lo declarativo es solo una sintaxis más bonita, y a veces más lenta. **La pregunta antes
de escribir declarativo es siempre: ¿quién va a decidir el cómo, y sabe más que yo?**

⏮️ [Volver a la clase 117](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
