# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 077

> [⬅️ Volver a la clase 077](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Cociente y resto en una sola operación. El procesador los calcula a la vez —una sola instrucción de
división produce los dos—, y sin embargo la mayoría de los lenguajes obligan a pedirlos por separado
y a dividir dos veces. Esta clase es sobre **cómo devuelve un lenguaje más de un valor**, y sobre por
qué **COBOL, que es de 1959, lo hace mejor que C**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **retorno múltiple**, y estos lenguajes cubren las cuatro estrategias.
> **COBOL** tiene `DIVIDE … GIVING … REMAINDER`: una sentencia, dos resultados, que es lo que hace el
> hardware. **Ada, Fortran, Pascal, PL/I y RPG** usan **parámetros de salida**, con el modo declarado
> en la firma. **Lisp** tiene **valores múltiples**, un mecanismo del lenguaje sin coste. Y **Perl,
> Tcl, M y Smalltalk** devuelven una **estructura** y la desmontan al recibirla.
>
> Y C++ estuvo cuarenta años sin nada de esto hasta las **descomposiciones estructuradas** de C++17.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (enteros positivos, b != 0) → stdout: `cociente=<a/b> resto=<a%b>`
- **Regla:** `(cociente, resto) = (a/b, a%b)`

| stdin | esperado |
|---|---|
| `17 5` | `cociente=3 resto=2` |
| `10 2` | `cociente=5 resto=0` |
| `7 3` | `cociente=2 resto=1` |

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
PROGRAM-ID. DIVMOD.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  COC     PIC S9(9) COMP-3.
01  RES     PIC S9(9) COMP-3.
01  ED-C    PIC -(8)9.
01  ED-R    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    DIVIDE A BY B GIVING COC REMAINDER RES

    MOVE COC TO ED-C
    MOVE RES TO ED-R
    DISPLAY "cociente=" FUNCTION TRIM(ED-C)
            " resto=" FUNCTION TRIM(ED-R)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **`DIVIDE A BY B GIVING COC REMAINDER RES` es una sola
sentencia que produce dos resultados**, y es exactamente lo que hace el procesador: la instrucción de
división de cualquier arquitectura devuelve cociente y resto a la vez.

En C hay que escribir `a / b` y `a % b`. El compilador **suele** reconocer el patrón y emitir una sola
división, pero es una optimización, no una garantía — y por eso la biblioteca estándar de C tiene
`div()` y `ldiv()`, que devuelven una estructura con los dos.

COBOL lo tiene en el verbo desde 1959, y no es el único caso:

```cobol
DIVIDE A BY B GIVING C REMAINDER R
UNSTRING LINEA DELIMITED BY "," INTO A B C
    WITH POINTER P TALLYING EN N          *> ¡tres salidas a la vez!
INSPECT TEXTO TALLYING N FOR ALL "a"
    REPLACING ALL "b" BY "c"              *> cuenta Y sustituye en una pasada
```

`UNSTRING` con `POINTER` y `TALLYING` devuelve los trozos, la posición final **y** cuántos campos
llenó. `INSPECT` cuenta y sustituye en un solo recorrido.

El patrón de fondo es el mismo: **los verbos de COBOL están diseñados alrededor de lo que la máquina
hace en una pasada**, no alrededor de la idea matemática de función con un solo resultado. Es una
consecuencia de venir del hardware en lugar de venir del cálculo lambda, y en esta clase concreta
juega a su favor.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program divmod
   implicit none
   integer :: a, b, cociente, resto

   read(*, *) a, b
   call dividir(a, b, cociente, resto)

   write(*, '(A,I0,A,I0)') 'cociente=', cociente, ' resto=', resto

contains

   pure subroutine dividir(x, y, coc, res)
      integer, intent(in)  :: x, y
      integer, intent(out) :: coc, res      ! DOS salidas declaradas
      coc = x / y
      res = mod(x, y)
   end subroutine dividir

end program divmod
```

**Lo que esta clase enseña en Fortran.** La distinción entre **`function`** y **`subroutine`** de
Fortran existe precisamente para esto: una función devuelve **un** valor y se usa dentro de una
expresión; una subrutina no devuelve nada y comunica por **parámetros `intent(out)`**.

```fortran
y = f(x)                      ! función: un resultado, dentro de una expresión
call s(x, a, b, c)            ! subrutina: varios resultados, sentencia propia
```

Y `intent(out)` tiene una garantía que conviene conocer: **el valor de entrada del argumento no
existe dentro de la subrutina**. El compilador puede asumirlo y avisar si lo lees antes de asignarlo.
No es solo documentación; cambia lo que el optimizador puede suponer.

Cuando los valores están relacionados, el Fortran moderno prefiere un **tipo derivado**, que es la
alternativa a los parámetros de salida:

```fortran
type :: Resultado
   integer :: cociente, resto
end type

function dividir(x, y) result(r)
   type(Resultado) :: r
   r%cociente = x / y
   r%resto = mod(x, y)
end function
```

Devolver una estructura es más limpio en el sitio de la llamada —`z = dividir(a, b)`— y permite usar
el resultado en una expresión. Lo que Fortran **no** tiene es desestructuración: hay que escribir
`z%cociente`, no `[c, r] = dividir(...)`.

Y `pure subroutine` es legal: una subrutina puede ser pura si sus únicos efectos son sus `intent(out)`.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Divmod is

   procedure Dividir (X, Y : in Integer; Coc, Res : out Integer) is
   begin
      Coc := X / Y;
      Res := X mod Y;
   end Dividir;

   A, B, Cociente, Resto : Integer;
begin
   Get (A);
   Get (B);
   Dividir (A, B, Cociente, Resto);

   Put ("cociente="); Put (Cociente, Width => 1);
   Put (" resto=");   Put (Resto, Width => 1);
   New_Line;
end Divmod;
```

**Lo que esta clase enseña en Ada.** Los parámetros `out` son el mecanismo, y Ada añade una garantía
que ningún otro lenguaje de esta página da: **el compilador comprueba que todo `out` se asigne en
todos los caminos** antes de salir, y avisa si se lee antes de escribirlo.

Y la alternativa idiomática, cuando los valores forman una unidad conceptual, es **devolver un
registro**:

```ada
type Division is record
   Cociente, Resto : Integer;
end record;

function Dividir (X, Y : Integer) return Division is
begin
   return (Cociente => X / Y, Resto => X mod Y);    --  agregado NOMBRADO
end Dividir;

D : constant Division := Dividir (17, 5);
```

Fíjate en dos cosas. La primera: el **agregado con nombres** de la clase 075 hace que el retorno se
lea sin ambigüedad. La segunda, y es la que importa: **el resultado puede declararse `constant`**, cosa
imposible con parámetros `out`.

Ese es el argumento que empujó a Ada 2012 a permitir funciones con efectos y que empuja hoy a todos
los lenguajes hacia devolver estructuras en lugar de rellenar parámetros: **inmutabilidad**.

Lo que Ada no tiene es desestructuración en la recepción. `D.Cociente` es la forma; no existe
`(C, R) := Dividir (...)`. Es la misma carencia que Fortran, y la diferencia con Lisp, Perl, Tcl y el
C++ moderno.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Divmod;
{$MODE OBJFPC}{$H+}
uses SysUtils;

procedure Dividir(X, Y: Integer; out Coc, Res: Integer);
begin
  Coc := X div Y;
  Res := X mod Y;
end;

var
  A, B, Cociente, Resto: Integer;

begin
  Read(A, B);
  Dividir(A, B, Cociente, Resto);

  WriteLn('cociente=', IntToStr(Cociente), ' resto=', IntToStr(Resto));
end.
```

**Lo que esta clase enseña en Pascal.** `out` en Object Pascal es lo mismo que en Ada: **solo
escritura**, el valor de entrada no cuenta. Se distingue de `var` —que es entrada y salida— y del paso
por valor.

Hay un detalle de implementación que diferencia `out` de `var` en Delphi y que conviene conocer:
**con `out`, el compilador libera el valor anterior del argumento antes de la llamada** si es un tipo
gestionado —una cadena, una interfaz, un array dinámico—. Con `var` no lo hace. Elegir mal produce
fugas o liberaciones dobles con tipos gestionados.

La alternativa de Pascal es el **registro**, y Object Pascal moderno permite devolverlo directamente:

```pascal
type
  TDivision = record
    Cociente, Resto: Integer;
  end;

function Dividir(X, Y: Integer): TDivision;
begin
  Result.Cociente := X div Y;
  Result.Resto := X mod Y;
end;
```

Es más limpio y permite `const D := Dividir(17, 5);` con la inferencia de la clase 052.

Y Pascal **no tiene desestructuración**: hay que escribir `D.Cociente`. Es una carencia que se nota
al lado de Lisp o del C++17 de esta misma página, y que ninguna versión ha resuelto.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (b (read)))
  (multiple-value-bind (cociente resto) (truncate a b)
    (format t "cociente=~D resto=~D~%" cociente resto)))
```

**Lo que esta clase enseña en Common Lisp.** `truncate` **ya devuelve los dos valores**: no hay que
escribir nada. Es una función del estándar, y devolver cociente y resto juntos es su comportamiento
normal desde 1984.

Los **valores múltiples** de Lisp son un mecanismo del lenguaje, no una tupla, y esa diferencia es la
clave:

```lisp
(truncate 17 5)                                  ; en contexto normal, solo el PRIMERO
(multiple-value-bind (c r) (truncate 17 5) ...)   ; los dos
(multiple-value-list (truncate 17 5))             ; => (3 2)  como lista, si hace falta
(nth-value 1 (truncate 17 5))                     ; => 2  solo el segundo
(values 1 2 3)                                    ; devolver varios
(values)                                          ; devolver NINGUNO
```

**Ignorar los valores extra es gratis**: no se construye ninguna estructura, no hay que escribir `_`
y no hay coste. En Go hay que poner `_`; en Rust hay que destruir la tupla; en Python se construye
una tupla real aunque solo quieras el primero.

Toda la biblioteca lo aprovecha, y ya lo hemos visto en varias clases: `gethash` devuelve valor y "¿la
clave estaba?" (053), `floor` y `round` devuelven cociente y resto (049), `parse-integer` devuelve el
número y dónde paró, `read-line` devuelve la línea y si terminó por fin de fichero.

Y `destructuring-bind` cubre la otra mitad de esta clase —desmontar una estructura anidada— con
soporte para opcionales, `&rest` y valores por defecto, como se vio en la clase 062.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc dividir {a b} {
    return [list [expr {$a / $b}] [expr {$a % $b}]]
}

gets stdin linea
lassign [split [string trim $linea]] a b
lassign [dividir $a $b] cociente resto

puts "cociente=$cociente resto=$resto"
```

**Lo que esta clase enseña en Tcl.** Como **todo comando devuelve una cadena**, devolver varios
valores es devolver **una lista**, y `lassign` la desmonta. Es el mismo mecanismo para las dos
direcciones.

```tcl
lassign {1 2 3} a b c           ;# a=1 b=2 c=3
lassign {1 2} a b c             ;# c queda VACÍA, no da error
set sobra [lassign {1 2 3 4} a b]   ;# lassign DEVUELVE lo que sobró: {3 4}
```

Ese último detalle es útil y poco conocido: `lassign` devuelve los elementos no asignados, así que se
puede encadenar para procesar una lista por trozos.

Y Tcl tiene una segunda vía, la de la clase 073: **modificar las variables del llamante** con
`upvar`.

```tcl
proc dividir {a b cocVar resVar} {
    upvar 1 $cocVar coc
    upvar 1 $resVar res
    set coc [expr {$a / $b}]
    set res [expr {$a % $b}]
}
dividir 17 5 c r        ;# se pasan los NOMBRES de las variables
```

`upvar 1 $nombre local` liga una variable local al **nombre** de una variable del llamante. Es el
paso por referencia de Tcl, y funciona porque en Tcl las variables se identifican por su nombre en
tiempo de ejecución.

Ese es el mecanismo con el que están escritos comandos como `scan`, `regexp` y `binary scan`, que
dejan sus resultados en variables en lugar de devolverlos — como se vio en la clase 062.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub dividir {
    my ($x, $y) = @_;
    return (int($x / $y), $x % $y);      # devolver una LISTA
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

my ($cociente, $resto) = dividir($p, $q);

print "cociente=$cociente resto=$resto\n";
```

**Lo que esta clase enseña en Perl.** Las subrutinas de Perl **devuelven listas de forma nativa**, y
la asignación de listas las desmonta. No hay tuplas ni estructuras: es el mismo mecanismo de la clase
076, en la dirección contraria.

Y aquí aparece el **contexto** de la clase 041 en su forma más importante:

```perl
my ($c, $r) = dividir(17, 5);     # contexto de LISTA: recibe los dos
my $x = dividir(17, 5);           # contexto ESCALAR: recibe... ¿qué?
```

Esa segunda línea es la trampa. `return (a, b)` en contexto escalar **no devuelve una lista**:
devuelve **el último elemento**, porque el operador coma en contexto escalar evalúa y descarta. Así
que `$x` vale el resto, no el cociente ni un contador.

Por eso el idioma correcto en Perl es usar `wantarray` de la clase 072 para decidir, o devolver una
**referencia** cuando el resultado debe comportarse como una unidad:

```perl
return { cociente => $c, resto => $r };     # una referencia a hash
my $d = dividir(17, 5);
print $d->{cociente};
```

La desestructuración de Perl va bastante lejos, con `undef` para descartar y desmontado de hashes:

```perl
my (undef, $segundo, @resto) = @lista;      # descartar el primero
my ($a, $b) = @hash{qw(x y)};                # "rebanada" de hash por claves
```

Lo que no tiene es desestructuración anidada al estilo de JavaScript o Rust; para eso está
`List::Util` o la desreferencia explícita.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

struct Division {
    int cociente;
    int resto;
};

Division dividir(int a, int b) {
    return {a / b, a % b};
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    const auto [cociente, resto] = dividir(a, b);   // DESCOMPOSICIÓN, C++17

    std::cout << "cociente=" << cociente << " resto=" << resto << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `auto [cociente, resto] = ...` es la **descomposición
estructurada**, y llegó con **C++17**. Antes de eso, devolver dos valores era incómodo de las tres
maneras posibles:

```cpp
// 1) Parámetros de salida, como C
void dividir(int a, int b, int* c, int* r);

// 2) std::pair, con nombres inútiles
std::pair<int,int> d = dividir(a, b);
usar(d.first, d.second);          // ¿cuál era cuál?

// 3) std::tie, con las variables declaradas ANTES
int c, r;
std::tie(c, r) = dividir(a, b);   // no permite const, no permite auto
```

La descomposición resuelve las tres: **declara, nombra y permite `const`** en una sola línea. Y
funciona sobre `std::pair`, `std::tuple`, arrays y **cualquier estructura con campos públicos** — como
la `Division` de este programa, sin necesidad de que herede ni implemente nada.

Combinada con el `if` con inicializador de la clase 058, da el idioma moderno para las operaciones que
devuelven valor y estado:

```cpp
if (const auto [it, insertado] = conjunto.insert(x); insertado) { ... }
for (const auto& [clave, valor] : mapa) { ... }
```

Un detalle que conviene conocer: **los nombres de la descomposición no son variables de verdad**, son
alias de los miembros. Por eso no se pueden capturar en una lambda en C++17 —se arregló en C++20— y
por eso `auto&` frente a `auto` cambia si se copia o no toda la estructura.

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

dcl-pi DIVMOD;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-ds resultado qualified;
  cociente int(10);
  resto    int(10);
end-ds;

dcl-s salida char(60);

resultado.cociente = %div(a : b);
resultado.resto    = %rem(a : b);

salida = 'cociente=' + %char(resultado.cociente)
       + ' resto='   + %char(resultado.resto);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG tiene las dos formas, y la elección entre ellas cambió con el
tiempo.

La clásica son los **parámetros de salida**: como el paso por referencia es el defecto en RPG
(clase 073), cualquier parámetro sin `const` ni `value` es una salida potencial.

```rpgle
dcl-pr dividir;
  a   int(10) const;
  b   int(10) const;
  coc int(10);          // sin const: se MODIFICA
  res int(10);
end-pr;
```

La moderna, y la recomendada, es **devolver una estructura de datos**, como en este programa. Desde
IBM i 7.2, un subprocedimiento **puede devolver una `dcl-ds` completa**:

```rpgle
dcl-proc dividir;
  dcl-pi *n likeds(tipoResultado);
    a int(10) const;
    b int(10) const;
  end-pi;
  dcl-ds r likeds(tipoResultado);
  r.cociente = %div(a : b);
  r.resto = %rem(a : b);
  return r;
end-proc;
```

Antes de 7.2 eso no era posible y había que usar parámetros de salida obligatoriamente. Es otro
ejemplo de característica añadida recientemente a un lenguaje de 1959.

RPG **no tiene desestructuración**: hay que escribir `r.cociente`. Y `qualified` sigue siendo
necesario para que los subcampos no invadan el espacio de nombres global, como se vio en la clase 075.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 divmod: procedure options(main);

    declare (a, b, cociente, resto) fixed binary(31);

    get list (a, b);
    call dividir(a, b, cociente, resto);

    put skip list ('cociente=' || trim(char(cociente)) ||
                   ' resto='   || trim(char(resto)));

 dividir: procedure (x, y, coc, res);
    declare (x, y, coc, res) fixed binary(31);
    coc = divide(x, y, 31);
    res = mod(x, y);
 end dividir;

 end divmod;
```

**Lo que esta clase enseña en PL/I.** PL/I usa parámetros de salida, con la particularidad de la clase
073: **el paso es por referencia por defecto**, así que cualquier parámetro que se asigne dentro
modifica el del llamante. No hay que declarar nada — y por eso tampoco hay forma de saber, leyendo la
llamada, cuáles son salidas.

Ese es exactamente el problema que resolvieron los modos `in`/`out` de Ada y los `intent` de Fortran.

Lo que PL/I sí tiene, y es su aportación a esta clase, es que **una función puede devolver una
estructura completa**, con toda la aritmética de estructuras disponible:

```pli
declare 1 division,
          2 cociente fixed binary(31),
          2 resto    fixed binary(31);

f: procedure (x, y) returns (like division);   /* LIKE: el tipo de otra estructura */
   declare 1 r like division;
   r.cociente = divide(x, y, 31);
   r.resto = mod(x, y);
   return (r);
end f;
```

`returns (like division)` usa el atributo `like` de la clase 052 para no repetir la declaración. Y
`by name` de la clase 075 permite copiar entre estructuras emparejando campos.

PL/I **no tiene desestructuración**, pero tiene algo cercano en el otro sentido: **`get data`** de la
clase 056, que lee variables **por su nombre** desde la entrada. Es desmontar una estructura textual
en variables, resuelto en el sistema de E/S en lugar de en la asignación.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DIVMOD ; Multiples retornos -- clase 077
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set r = $$dividir(a, b)
 write "cociente=", $piece(r, "^", 1)
 write " resto=", $piece(r, "^", 2), !
 quit
 ;
dividir(x, y) ; devuelve "cociente^resto"
 quit (x\y) _ "^" _ (x#y)
```

**Lo que esta clase enseña en M.** Devolver **una cadena con delimitador** —`"3^2"`— es el idioma de M
para los resultados compuestos, y ya apareció en las clases 048 y 072. `$piece` es la
desestructuración.

Pero M tiene una segunda forma, más potente, que es la que se usa en las APIs reales: **rellenar un
array pasado por referencia**.

```mumps
 do DIVIDIR^MAT(17, 5, .resultado)
 write resultado("cociente"), " ", resultado("resto")
 ;
DIVIDIR(x, y, res) ;
 set res("cociente") = x\y
 set res("resto") = x#y
 quit
```

Ese patrón tiene tres ventajas sobre la cadena: **los campos van nombrados** (clase 075), **puede ser
jerárquico**, y **no hay límite de tamaño**. Es la convención de FileMan y de prácticamente todas las
APIs de VistA.

Y como se vio en la clase 072, el mismo array sirve para devolver **el resultado y los errores** a la
vez, en subárboles distintos:

```mumps
 set res("datos", 1) = ...
 set res("error", "codigo") = ...
```

En un lenguaje sin tipos, sin estructuras y sin retornos múltiples, **el array local por referencia
acaba haciendo de todo**: parámetros nombrados, retorno múltiple, estructura anidada y canal de
errores. Es una sola herramienta muy afilada, que es la descripción exacta de M.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b resultado |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

resultado := Array with: a // b with: a \\ b.

Transcript
    show: 'cociente=', resultado first printString;
    show: ' resto=', resultado second printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk **no tiene retornos múltiples**: un método
devuelve **un objeto**, siempre. Y no lo echa de menos, porque devolver un objeto compuesto es
barato:

```smalltalk
^Array with: cociente with: resto           "un array"
^cociente -> resto                           "una ASOCIACIÓN clave->valor"
^Dictionary newFrom: { #cociente -> c. #resto -> r }
^DivisionResultado cociente: c resto: r      "una CLASE propia"
```

La cuarta es la que la comunidad recomienda, y el argumento es de diseño: **si dos valores van
siempre juntos, probablemente son un concepto que merece nombre**. Un `Punto`, un `Intervalo`, un
`ResultadoDeBusqueda`. Devolver una tupla anónima es aplazar esa decisión.

Y hay una alternativa muy idiomática que evita el problema por completo: **pasar un bloque que reciba
los dos valores**.

```smalltalk
Numero >> dividir: b conResultado: unBloque
    ^unBloque value: self // b value: self \\ b

17 dividir: 5 conResultado: [ :c :r | Transcript show: c printString, '/', r printString ]
```

El "retorno múltiple" se convierte en **una llamada con dos argumentos**, y no hay estructura
intermedia que construir ni desmontar. Es el mismo patrón que `at:ifAbsent:` de la clase 072 — en un
lenguaje donde pasar código es gratis, muchos problemas de retorno se convierten en problemas de
continuación.

Y `\\` y `//` son el resto y la división al suelo de la clase 055.

---

## Y de vuelta a la clase

Lo transferible: **si dos valores se calculan juntos, devolverlos juntos evita calcular dos veces**.
`divmod`, `minmax`, `find` con posición y encontrado, `parse` con valor y resto — todos son la misma
forma. Y la desestructuración en el sitio de la recepción es lo que hace que esa forma sea cómoda: sin
ella, un retorno múltiple obliga a declarar variables antes y estorba más de lo que ayuda. Por eso las
dos características —devolver varios y desmontarlos— aparecen siempre juntas en los lenguajes
modernos.

⏮️ [Volver a la clase 077](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
