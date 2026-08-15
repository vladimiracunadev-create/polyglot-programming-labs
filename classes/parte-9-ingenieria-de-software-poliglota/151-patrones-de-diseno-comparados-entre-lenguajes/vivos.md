# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 151

> [⬅️ Volver a la clase 151](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Elegir una operación por su nombre y aplicarla: eso es el patrón Estrategia. Y esta clase existe para
enseñar algo que el libro de patrones no dice y que se ve mejor aquí que en ningún sitio: **muchos
patrones son parches a carencias del lenguaje**. En Lisp, Smalltalk, Perl o Tcl, la Estrategia **no es
un patrón: es pasar una función**. Y hay un dato que lo confirma: **el libro de los cuatro autores nació
en el mundo de Smalltalk y C++**, y sus ejemplos venían de ahí.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **patrón de diseño como solución recurrente**, y estos lenguajes lo enseñan
> porque **cubren los dos extremos del eje que decide qué patrones hacen falta**: el de los lenguajes sin
> funciones de primera clase —COBOL, Fortran 77, Ada 83, C++ antes de C++11— donde la Estrategia necesita
> una jerarquía entera; y el de los que tratan el código como dato —Lisp, Smalltalk, Tcl, Perl— donde
> desaparece.
>
> Y aparece la observación de Peter Norvig que ordena la clase: **de los 23 patrones del libro, 16 son
> más simples o invisibles en un lenguaje dinámico**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `estrategia a b` (estrategia ∈ {suma, resta, producto}) → stdout: `resultado=<a estrategia b>`
- **Regla:** `aplicar la estrategia elegida a a y b`

| stdin | esperado |
|---|---|
| `suma 3 4` | `resultado=7` |
| `resta 10 3` | `resultado=7` |
| `producto 5 6` | `resultado=30` |

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
PROGRAM-ID. ESTRAT.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  C-OP    PIC X(10).
01  C-A     PIC X(20).
01  C-B     PIC X(20).
01  A       PIC S9(9) COMP.
01  B       PIC S9(9) COMP.
01  R       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-OP C-A C-B
    END-UNSTRING

    COMPUTE A = FUNCTION NUMVAL(C-A)
    COMPUTE B = FUNCTION NUMVAL(C-B)

    EVALUATE FUNCTION TRIM(C-OP)
        WHEN "suma"     COMPUTE R = A + B
        WHEN "resta"    COMPUTE R = A - B
        WHEN "producto" COMPUTE R = A * B
        WHEN OTHER      MOVE 0 TO R
    END-EVALUATE

    MOVE R TO ED
    DISPLAY "resultado=" FUNCTION TRIM(ED)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El `EVALUATE` del programa es **la forma que toma la Estrategia
cuando el lenguaje no tiene funciones de primera clase**: una selección explícita.

Y merece decir con claridad que **eso no está mal**. Con tres casos conocidos y cerrados, un `EVALUATE`
es más legible que tres clases y una interfaz, y no requiere ningún mecanismo.

El patrón hace falta cuando **el conjunto de estrategias tiene que poder crecer sin tocar este código**,
y ahí COBOL sí tiene una respuesta:

```cobol
       01  WS-PROGRAMA PIC X(8).
       ...
           MOVE "CALCSUMA" TO WS-PROGRAMA
           CALL WS-PROGRAMA USING A B R
```

**`CALL` con un nombre en una variable es una llamada dinámica**: el programa a ejecutar **se decide en
ejecución**, y puede estar en una tabla configurable.

Eso es la Estrategia de verdad, y en COBOL tiene una propiedad interesante: **la nueva estrategia se
despliega sin recompilar ni reenlazar a quien la usa** (clase 148), porque el enlace ocurre al llamar.

Y COBOL tiene un patrón propio que merece nombrarse porque es de su mundo y no aparece en ningún
catálogo: **la tabla de decisión**.

```text
       01  TABLA-REGLAS.
           05  REGLA OCCURS 200.
               10  R-CONDICION  PIC X(20).
               10  R-PROGRAMA   PIC X(8).
```

**Las reglas de negocio se guardan en una tabla o en un fichero, no en el código**, y el programa las
recorre. Cambiar una regla es cambiar un dato.

Es exactamente la idea del motor de reglas moderno, y en los sistemas de seguros y banca lleva
funcionando desde los años setenta — con el mismo compromiso que la clase 149 señalaba en FileMan:
**flexibilidad a cambio de que la lógica deje de estar en el código y deje de ser revisable** (clase
146).

Y merece cerrar con el patrón más usado del mundo COBOL, que sí está en el catálogo: **Plantilla**.

```cobol
       PERFORM INICIAR
       PERFORM PROCESAR UNTIL FIN
       PERFORM TERMINAR
```

**Ese esqueleto de tres pasos es la estructura de decenas de miles de programas de lote**, con los
párrafos rellenados según el caso. Es el Método Plantilla sin herencia, conseguido por convención — y
es la prueba de que un patrón es una forma reconocible antes que un mecanismo.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program estrat
   implicit none
   character(len=80) :: linea
   character(len=20) :: op
   integer :: a, b, r, p1

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, ' ')
   op = linea(1:p1-1)
   read(linea(p1+1:), *) a, b

   select case (trim(op))
   case ('suma');     r = a + b
   case ('resta');    r = a - b
   case ('producto'); r = a * b
   case default;      r = 0
   end select

   write(*, '(A,I0)') 'resultado=', r
end program estrat
```

**Lo que esta clase enseña en Fortran.** Fortran vivió los dos extremos de esta clase, y el cambio tiene
fecha: **Fortran 2003 añadió los punteros a procedimiento**.

**Antes**, la Estrategia se hacía con lo que había:

```fortran
      EXTERNAL SUMAR
      CALL APLICAR(SUMAR, A, B, R)      ! pasar un procedimiento como argumento
```

**Eso funcionaba desde Fortran 66**, y es la razón por la que las bibliotecas numéricas clásicas
—QUADPACK, ODEPACK, MINPACK— **reciben la función a integrar o a minimizar como argumento**.

**Es el patrón Estrategia en su forma más pura, cuarenta años antes del libro de patrones.**

Y su límite era grave: **el procedimiento pasado no llevaba estado**, así que los parámetros del
problema **había que pasarlos por `COMMON`** (clase 088) — con todos los problemas que la clase 150
describía.

**Hoy** hay dos mecanismos que lo resuelven:

```fortran
! 1. puntero a procedimiento, con interfaz comprobada
abstract interface
   pure function operacion(x, y) result(r)
      integer, intent(in) :: x, y
      integer :: r
   end function
end interface

procedure(operacion), pointer :: estrategia => null()
estrategia => sumar
r = estrategia(a, b)
```

```fortran
! 2. procedimiento ligado a tipo: el objeto LLEVA su estrategia y su estado
type :: integrador
   real(dp) :: tolerancia
contains
   procedure(nucleo), pointer, nopass :: metodo => null()
end type
```

**La segunda forma es la Estrategia del libro**, con el estado que le faltaba a la versión de 1966.

Y merece señalar el patrón que domina de verdad el código Fortran moderno y que no está en el catálogo
clásico: **el tipo con procedimientos ligados como fachada de un algoritmo numérico**.

```fortran
type(solver) :: s
call s%configurar(tolerancia=1e-10_dp, max_iter=1000)
call s%resolver(matriz, vector, solucion)
```

Es una fachada y una estrategia a la vez, y su valor real en este dominio es otro: **da un nombre a los
parámetros**. Un `call dgesv(n, nrhs, a, lda, ipiv, b, ldb, info)` con ocho argumentos posicionales es
la interfaz que este patrón vino a sustituir.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings.Fixed;

procedure Estrat is
   type Operacion is access function (X, Y : Integer) return Integer;

   function Suma     (X, Y : Integer) return Integer is (X + Y);
   function Resta    (X, Y : Integer) return Integer is (X - Y);
   function Producto (X, Y : Integer) return Integer is (X * Y);

   Linea      : String (1 .. 80);
   Ultimo     : Natural;
   Sep1, Sep2 : Natural;
   A, B       : Integer;
   Elegida    : Operacion;
begin
   Get_Line (Linea, Ultimo);

   Sep1 := Ada.Strings.Fixed.Index (Linea (1 .. Ultimo), " ");
   Sep2 := Ada.Strings.Fixed.Index (Linea (Sep1 + 1 .. Ultimo), " ");

   if Linea (1 .. Sep1 - 1) = "suma" then
      Elegida := Suma'Access;
   elsif Linea (1 .. Sep1 - 1) = "resta" then
      Elegida := Resta'Access;
   else
      Elegida := Producto'Access;
   end if;

   A := Integer'Value (Linea (Sep1 + 1 .. Sep2 - 1));
   B := Integer'Value (Linea (Sep2 + 1 .. Ultimo));

   Put ("resultado=");
   Put (Elegida (A, B), Width => 1);
   New_Line;
end Estrat;
```

**Lo que esta clase enseña en Ada.** El programa usa **`access function`** —un puntero a función con la
firma declarada— y `'Access` para tomar la dirección de cada una. Es la Estrategia con el tipo del
algoritmo comprobado por el compilador.

Y Ada aporta a esta clase algo que ningún otro lenguaje de esta página tiene: **los genéricos con
parámetros formales de subprograma**, que son la Estrategia **resuelta en compilación**.

```ada
generic
   type Elemento is private;
   with function Comparar (A, B : Elemento) return Boolean;
package Ordenacion is
   procedure Ordenar (V : in out Vector);
end Ordenacion;

package Ordenar_Por_Edad is new Ordenacion (Persona, Menor_Edad);
```

**`with function Comparar` es un parámetro formal del genérico**: la estrategia se pasa **al
instanciar**, no al llamar.

Y las consecuencias merecen compararse, porque son las dos mitades del compromiso de esta clase:

| Vía | Cuándo se decide | Coste | Flexibilidad |
|---|---|---|---|
| `access function` | **ejecución** | una indirección | se puede cambiar en marcha |
| **genérico** | **compilación** | **cero: se puede incorporar** | fija al instanciar |
| tipo etiquetado + despacho | ejecución | tabla de métodos | jerarquía extensible |

**Las tres están en el lenguaje y son idiomáticas**, y elegir es una decisión de diseño real, no de
gusto.

Y en el dominio de Ada hay una restricción que decide muchas veces: **los sistemas certificados suelen
prohibir el despacho dinámico y los punteros a función**, porque **impiden demostrar qué código se
ejecuta** (clase 146).

Así que **en aviónica, la Estrategia se hace con genéricos**, y toda la variabilidad se resuelve antes
de ejecutar.

Y merece cerrar con un patrón que Ada tiene en el lenguaje y que en otros sitios requiere maquinaria: el
**Objeto Protegido como Monitor** (clase 135).

```ada
protected type Recurso is
   entry Adquirir;
   procedure Liberar;
private
   Libre : Boolean := True;
end Recurso;
```

**Eso es el patrón Monitor, con la exclusión mutua y la espera con condición garantizadas por el
compilador** — y es un buen ejemplo del cierre de esta clase: **cuando el lenguaje incorpora un patrón,
el patrón deja de serlo y pasa a ser una construcción**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Estrat;
{$MODE OBJFPC}{$H+}
uses SysUtils, StrUtils;

type
  TOperacion = function(X, Y: Integer): Integer;

function Suma(X, Y: Integer): Integer;     begin Result := X + Y; end;
function Resta(X, Y: Integer): Integer;    begin Result := X - Y; end;
function Producto(X, Y: Integer): Integer; begin Result := X * Y; end;

var
  Linea, Op: string;
  P1, P2, A, B: Integer;
  Elegida: TOperacion;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P1 := Pos(' ', Linea);
  P2 := PosEx(' ', Linea, P1 + 1);

  Op := Copy(Linea, 1, P1 - 1);
  A  := StrToInt(Copy(Linea, P1 + 1, P2 - P1 - 1));
  B  := StrToInt(Copy(Linea, P2 + 1, Length(Linea)));

  if Op = 'suma' then Elegida := @Suma
  else if Op = 'resta' then Elegida := @Resta
  else Elegida := @Producto;

  WriteLn('resultado=', IntToStr(Elegida(A, B)));
end.
```

**Lo que esta clase enseña en Pascal.** El tipo `TOperacion = function(...): Integer` es un **tipo
procedimental**, presente en Turbo Pascal desde 1985 — de los primeros lenguajes imperativos populares
en tenerlos.

Y Object Pascal aporta a esta clase una variante que merece explicarse porque resuelve el problema que
la clase 121 planteaba: **el método de objeto como valor**.

```pascal
type
  TOperacionDeObjeto = function(X, Y: Integer): Integer of object;
```

**`of object` es la clave**: ese tipo no guarda un puntero, **guarda dos** —el código y el objeto—, y al
llamarlo **el método se ejecuta con su `Self`**.

Es exactamente lo que un cierre necesita: **código más el estado al que se refiere** (clase 121). Y es
de 1995, cuando C++ no tenía nada equivalente y Java tampoco.

Y esa característica es la que hace funcionar el modelo de eventos de Delphi (clase 120):

```pascal
Button1.OnClick := Form1.MiManejador;    { el objeto viaja con el método }
```

**El diseñador visual asigna un método de un formulario a un evento de un botón**, y funciona porque el
puntero lleva el objeto.

Y Delphi moderno añadió lo que faltaba:

```pascal
type TFuncion = reference to function(X, Y: Integer): Integer;
var f: TFuncion;
begin
  f := function(X, Y: Integer): Integer begin Result := X * Y end;   { ANÓNIMA }
```

**`reference to` es un cierre de verdad**: captura las variables locales del ámbito donde se define, con
conteo de referencias para mantenerlas vivas (clase 121).

Y merece cerrar con el patrón más característico del ecosistema Delphi, que la clase 146 ya rozó y que
está en el catálogo: **el Prototipo, vía el sistema de componentes**.

Un componente puesto en un formulario **se guarda en el `.dfm` con sus propiedades**, y al abrir el
formulario **se crea una copia a partir de esa descripción**. Es clonación desde un prototipo
serializado, y es el mecanismo que hacía funcionar el diseñador visual entero.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((op (read))
       (a (read))
       (b (read))
       (f (case op
            (suma     #'+)
            (resta    #'-)
            (producto #'*)
            (t        (lambda (x y) (declare (ignore x y)) 0)))))
  (format t "resultado=~D~%" (funcall f a b)))
```

**Lo que esta clase enseña en Common Lisp.** Aquí está el argumento del gancho en una línea: **`#'+` es
la estrategia**. No hay interfaz, no hay clase, no hay fábrica — **hay una función guardada en una
variable**.

Y esta es la clase donde toca desarrollar la observación de **Peter Norvig**, que la formuló en 1996 en
*Design Patterns in Dynamic Languages* tras analizar los 23 patrones del libro de los cuatro autores:

> **16 de los 23 patrones son invisibles o mucho más simples en Lisp o en Dylan.**

Y merece ver el detalle, porque la lista es instructiva:

| Patrón | En un lenguaje dinámico |
|---|---|
| **Estrategia** | una función en una variable |
| **Comando** | una función, o un cierre |
| **Fábrica abstracta** | una función que devuelve funciones |
| **Método Plantilla** | una función que recibe funciones |
| **Iterador** | integrado en el lenguaje (`loop`, `map`) |
| **Singleton** | una variable global, o el paquete |
| **Prototipo** | `copy-structure`, o simplemente un cierre |
| **Decorador** | envolver la función y redefinirla |
| **Estado** | cambiar la función guardada |
| **Visitante** | **despacho múltiple de CLOS** (clase 111) |
| **Adaptador** | una función que traduce |
| **Fachada** | una función |

**El Visitante merece el detalle**, porque es el caso más claro de patrón que compensa una limitación:

El Visitante existe **porque en un lenguaje con despacho simple no se puede elegir el método según dos
tipos a la vez**. Su maquinaria —`accept`, `visit`, el doble despacho— **es enteramente el rodeo para
conseguirlo**.

Y en CLOS:

```lisp
(defmethod imprimir ((doc Informe) (medio PDF)) ...)
(defmethod imprimir ((doc Informe) (medio HTML)) ...)
(defmethod imprimir ((doc Factura) (medio PDF)) ...)
```

**El despacho múltiple hace el trabajo directamente**, y el patrón desaparece.

Y hay que decir la otra mitad, porque Norvig también la dijo: **los 7 restantes siguen haciendo falta**
—Observador, Compuesto, Intérprete, Mediador— porque **resuelven problemas de estructura, no
limitaciones del lenguaje**.

Es exactamente la distinción del cierre de esta clase, y saber en qué grupo cae cada patrón es lo que
evita la mitad de la ceremonia inútil que se escribe.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] op a b

proc suma     {x y} { expr {$x + $y} }
proc resta    {x y} { expr {$x - $y} }
proc producto {x y} { expr {$x * $y} }

puts "resultado=[$op $a $b]"
```

**Lo que esta clase enseña en Tcl.** Fíjate en la última línea: **`[$op $a $b]`**. La variable `$op`
contiene el texto `suma`, y **eso ES la llamada**.

En Tcl, **el nombre del comando es el primer elemento y puede venir de una variable**, así que la
Estrategia se reduce a **usar el dato como nombre de procedimiento**. Ni tabla, ni interfaz, ni
despacho: **la sustitución de variables lo hace**.

Es el ejemplo más extremo de esta página del argumento del cierre, y también el más peligroso, porque
merece la advertencia: **si `$op` viene de fuera, esto ejecuta cualquier comando que el usuario
escriba** (clases 146 y 153).

```tcl
# ✗ inseguro si $op es entrada externa
puts [$op $a $b]

# ✓ lista blanca explícita
if {$op ni {suma resta producto}} { error "operación no permitida" }
puts [$op $a $b]
```

**Esa es la lección práctica de esta página**: en los lenguajes donde el patrón desaparece, **también
desaparece la barrera que el patrón imponía sin querer**. Una interfaz con tres implementaciones no
puede ejecutar `exec`; una llamada por nombre, sí.

Y Tcl tiene mecanismos que dan la flexibilidad del patrón con control:

```tcl
# un espacio de nombres como registro de estrategias
namespace eval ops {
    proc suma {x y} { expr {$x + $y} }
}
if {[info procs ::ops::$op] eq ""} { error "no existe" }
::ops::$op $a $b
```

**Restringir el espacio de nombres es la lista blanca**, y es la forma idiomática.

Y merece cerrar con dos patrones que en Tcl son una línea y que en otros lenguajes son bibliotecas:

```tcl
# Decorador: envolver un comando existente (clase 138)
rename ::procesar ::procesar_orig
proc ::procesar {args} {
    set t [clock microseconds]
    set r [::procesar_orig {*}$args]
    puts "tardó [expr {[clock microseconds] - $t}] us"
    return $r
}
```

```tcl
# Comando: un comando es un valor; se guarda, se pasa y se ejecuta después
lappend cola [list procesar $pedido]
foreach c $cola { eval $c }
```

**El Decorador aplicado a código ajeno sin tocarlo** es lo que en otros ecosistemas requiere
intercepción, envoltorios generados o programación orientada a aspectos.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($op, $a, $b) = split ' ', $linea;

my %estrategia = (
    suma     => sub { $_[0] + $_[1] },
    resta    => sub { $_[0] - $_[1] },
    producto => sub { $_[0] * $_[1] },
);

print "resultado=", $estrategia{$op}->($a, $b), "\n";
```

**Lo que esta clase enseña en Perl.** El programa usa **una tabla de despacho**: un `hash` cuyos valores
son **referencias a subrutina**.

```perl
my %estrategia = ( suma => sub { ... }, ... );
$estrategia{$op}->($a, $b);
```

**Ese es el idioma canónico de Perl para la Estrategia, el Comando y la máquina de estados**, y merece
destacarse por dos motivos:

**Primero, es más seguro que el `[$op ...]` de Tcl en esta página**: **la tabla ES la lista blanca**. Un
`$op` que no esté en el `hash` da `undef` y falla, no ejecuta nada arbitrario.

**Y segundo, se puede construir en marcha**:

```perl
$estrategia{$nueva} = cargar_complemento($fichero);     # registro dinámico
```

Es una fábrica y un registro de complementos, en una asignación.

Y Perl aporta a esta clase su propio catálogo, distinto del clásico, con nombres reconocibles en la
comunidad:

| Idioma de Perl | Equivale a |
|---|---|
| **Tabla de despacho** | Estrategia, Comando, Estado |
| **Cierre como generador** | Iterador |
| **`AUTOLOAD`** | Proxy, Métodos fantasma |
| **`tie`** | **Decorador sobre una variable** |
| **Roles de Moose** | Mixin, composición sin herencia (clase 149) |
| **`local`** | Contexto dinámico, inyección temporal (clase 088) |

**`tie` merece la explicación** porque no tiene equivalente en casi ningún lenguaje de esta página:

```perl
tie my %cache, 'MiClase::ConDisco', 'fichero.db';
$cache{clave} = $valor;      # parece un hash normal... y va al disco
```

**`tie` intercepta las operaciones básicas de una variable** —leer, escribir, borrar, iterar— y las
redirige a métodos de una clase.

Es el patrón Proxy aplicado **a la sintaxis del lenguaje**, no a un objeto: el código que usa el hash
**no sabe ni tiene que saber** que hay un disco, una caché o una base de datos detrás.

Y **`local`** (clase 088) merece la mención final porque implementa un patrón que el catálogo clásico no
tiene: **sustituir temporalmente algo global y que se restaure solo al salir del ámbito**.

```perl
{
    local $SIG{__WARN__} = sub { };    # silenciar avisos AQUÍ
    hacer_algo_ruidoso();
}                                       # y se restaura, incluso si hay excepción
```

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <functional>
#include <iostream>
#include <map>
#include <string>

int main() {
    std::string op;
    long long a{}, b{};
    if (!(std::cin >> op >> a >> b)) return 1;

    const std::map<std::string, std::function<long long(long long, long long)>> estrategia{
        {"suma",     [](auto x, auto y) { return x + y; }},
        {"resta",    [](auto x, auto y) { return x - y; }},
        {"producto", [](auto x, auto y) { return x * y; }},
    };

    const auto it = estrategia.find(op);
    std::cout << "resultado=" << (it != estrategia.end() ? it->second(a, b) : 0) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Este programa es una demostración directa de la tesis de la clase,
porque **C++ es el lenguaje donde nació el catálogo y el que más ha cambiado desde entonces**.

**El libro de los cuatro autores es de 1994**, y su Estrategia canónica en C++ era:

```cpp
class Operacion { public: virtual int aplicar(int, int) = 0; virtual ~Operacion() = default; };
class Suma : public Operacion { int aplicar(int a, int b) override { return a + b; } };
class Resta : public Operacion { ... };
class Producto : public Operacion { ... };
// más una fábrica que elige, más gestión de memoria
```

**Cuatro clases, una jerarquía, memoria dinámica y despacho virtual** para lo que ahora son tres
lambdas.

Y lo que cambió tiene fechas concretas:

| Versión | Qué aportó | Qué patrón simplificó |
|---|---|---|
| **C++11** | lambdas, `std::function`, `auto` | Estrategia, Comando, Observador |
| **C++11** | `unique_ptr`, `shared_ptr` | quitó la gestión manual del Compuesto |
| **C++11** | plantillas variádicas | Fábrica genérica |
| **C++17** | `std::variant` + `std::visit` | **Visitante**, sin jerarquía |
| **C++20** | conceptos, rangos | Iterador, Adaptador |
| **C++20** | corrutinas | Iterador perezoso, Generador |

**`std::variant` con `std::visit` merece el detalle**, porque elimina el Visitante igual que el despacho
múltiple de Lisp en esta página:

```cpp
using Forma = std::variant<Circulo, Cuadrado, Triangulo>;

double area(const Forma& f) {
    return std::visit(overloaded{
        [](const Circulo& c)   { return 3.14159 * c.r * c.r; },
        [](const Cuadrado& c)  { return c.lado * c.lado; },
        [](const Triangulo& t) { return t.base * t.altura / 2; },
    }, f);
}
```

**Sin clase base, sin métodos virtuales, sin `accept`/`visit`, sin memoria dinámica** — y **el
compilador comprueba que se han cubierto todos los casos**.

Y esa última propiedad es una mejora sobre el patrón original: **el Visitante clásico no avisa si añades
un tipo y olvidas un visitante**; `std::visit` **no compila**.

Y merece cerrar con el compromiso que sigue vivo en C++ y que la clase 149 anticipó: **la Estrategia con
`std::function` cuesta una indirección y puede reservar memoria**; **con un parámetro de plantilla es
gratis pero se decide en compilación**.

Es la misma disyuntiva que Ada plantea en esta página, y en C++ hay que elegir explícitamente cada vez.

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

dcl-pi ESTRAT;
  op char(10) const;
  a  int(10) const;
  b  int(10) const;
end-pi;

dcl-s r int(20);

select;
  when %trim(op) = 'suma';     r = a + b;
  when %trim(op) = 'resta';    r = a - b;
  when %trim(op) = 'producto'; r = a * b;
  other;                       r = 0;
endsl;

dsply ('resultado=' + %char(r));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG moderno tiene punteros a procedimiento, y la Estrategia se
escribe así:

```rpgle
dcl-pr operacion int(20) extproc(*dclcase);
  x int(10) const;
  y int(10) const;
end-pr;

dcl-s elegida pointer(*proc);

elegida = %paddr(suma);
r = elegida(a : b);        // llamada por puntero
```

**`%paddr` toma la dirección de un procedimiento y `pointer(*proc)` la guarda**, con la firma declarada
en el prototipo.

Y IBM i tiene además una forma de Estrategia que es propia de la plataforma y merece explicarse, porque
opera a otro nivel: **la llamada dinámica por nombre**.

```rpgle
dcl-pr ejecutar extpgm(nombrePrograma);
  ...
end-pr;
dcl-s nombrePrograma char(10);

nombrePrograma = %trim(reglaDeLaTabla);
ejecutar(datos);           // se llama al programa que diga la TABLA
```

**El programa a ejecutar sale de un dato**, igual que el `CALL` dinámico de COBOL en esta página, y con
la misma consecuencia valiosa: **añadir una estrategia es desplegar un programa nuevo y añadir una fila,
sin tocar ni recompilar el que decide**.

Y esa combinación —**tabla de reglas más llamada dinámica**— es el patrón dominante del software de
gestión de esta plataforma, y merece verlo con nombre propio:

```text
Tabla PARAMS:
  TIPO_CLIENTE  PROGRAMA_DESCUENTO
  ------------  ------------------
  VIP           DESCVIP
  MAYORISTA     DESCMAY
  NORMAL        DESCNOR
```

**Es una Fábrica y una Estrategia a la vez, configurable por el usuario de negocio y sin despliegue.**

Y el compromiso que hay que reconocer es el mismo que en COBOL y en FileMan (clase 149): **la lógica se
va de donde se puede revisar**. Nadie ve en el código qué descuentos existen; hay que consultar la
tabla, y la tabla no está en git (clase 145).

La práctica que lo mitiga y que merece extraerse: **versionar el contenido de esas tablas junto al
código**, exportándolas como datos en el repositorio. Es una decisión pequeña que convierte
configuración opaca en algo revisable y con historial.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 estrat: procedure options(main);

    declare op char(10) varying;
    declare (a, b, r) fixed binary(31);

    get list (op, a, b);

    select (op);
       when ('suma')     r = a + b;
       when ('resta')    r = a - b;
       when ('producto') r = a * b;
       otherwise         r = 0;
    end;

    put skip list ('resultado=' || trim(char(r)));

 end estrat;
```

**Lo que esta clase enseña en PL/I.** PL/I tiene punteros a entrada desde 1964, así que la Estrategia
como valor es tan vieja como el lenguaje:

```pli
 declare operacion entry (fixed binary(31), fixed binary(31))
                   returns (fixed binary(31)) variable;

 operacion = suma;                 /* asignar un procedimiento a una variable */
 r = operacion(a, b);
```

**`entry ... variable`** declara una variable que contiene un procedimiento, con la firma comprobada.

Y PL/I aporta a esta clase un mecanismo que **implementa un patrón entero en el lenguaje** y que ya
apareció en la clase 137: **el manejo de condiciones como Cadena de Responsabilidad**.

```pli
 nivel1: procedure;
    on error begin;
       if puedo_manejarlo then do; corregir(); goto seguir; end;
       /* si no, se propaga al nivel anterior */
    end;
    call nivel2();
 seguir:
 end nivel1;
```

**Los manejadores `on` se apilan por ámbito**, y una condición **sube por la pila hasta que alguien la
maneja** — que es exactamente la definición del patrón Cadena de Responsabilidad.

Y la diferencia con `try`/`catch` merece señalarse: **el manejador de PL/I puede corregir y reanudar**
(clase 116), así que la cadena no es solo "quién se ocupa del error" sino **"quién sabe arreglarlo"**.

Y hay un patrón que PL/I practica y que la clase 149 nombró, y que aquí conviene ver como patrón: **la
canalización de pasos** de COBOL en esta página **es el patrón Tubería y Filtros**, con una propiedad que
el catálogo de objetos no tiene: **cada filtro es un proceso independiente**.

Es un recordatorio útil de que **el catálogo de los cuatro autores es de patrones de objetos**, y que
hay catálogos enteros de patrones de otras escalas:

| Catálogo | Ámbito |
|---|---|
| **Gang of Four** (1994) | objetos dentro de un programa |
| **POSA** (1996) | arquitectura de sistemas |
| **Fowler, *Patterns of Enterprise Application Architecture*** (2002) | aplicaciones con datos |
| **Hohpe, *Enterprise Integration Patterns*** (2003) | mensajería entre sistemas |
| **Nygard, *Release It!*** (2007) | estabilidad en producción |

**Y buena parte de los tres últimos describe cosas que el mundo del mainframe llevaba décadas
haciendo** —colas de mensajes, procesamiento por lotes, compensación de transacciones, aislamiento de
fallos—, con otros nombres.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ESTRAT ; Patron estrategia -- clase 151
 read linea
 new op, a, b, r
 set op = $piece(linea, " ", 1)
 set a = $piece(linea, " ", 2)
 set b = $piece(linea, " ", 3)
 set r = $select(op="suma" : a + b, op="resta" : a - b, op="producto" : a * b, 1 : 0)
 write "resultado=", r, !
 quit
```

**Lo que esta clase enseña en M.** M lleva la tesis de esta clase al extremo, por la razón de la clase
123: **el código es texto, así que una estrategia es una cadena**.

```mumps
 set estrategia("suma") = "a + b"
 set estrategia("resta") = "a - b"
 set estrategia("producto") = "a * b"
 set r = @estrategia(op)              ; la INDIRECCIÓN evalúa la cadena
```

**`@` evalúa el contenido de la variable como código M.** El patrón Estrategia desaparece por completo:
**es una tabla de cadenas**.

Y en VistA eso está por todas partes, con una consecuencia que define la plataforma: **las reglas de
negocio viven en el diccionario de datos de FileMan** (clase 149).

```text
Campo "EDAD" del fichero PACIENTE:
   Tipo: calculado
   Expresión MUMPS: $$FMDIFF^XLFDT(DT, FECHA_NACIMIENTO)\365.25
```

**Ese código está en la base de datos, no en una rutina**, y FileMan lo evalúa al mostrar el campo.

Es la Estrategia, el Método Plantilla y el campo calculado, todo resuelto con "guardar código como
dato".

**Y el precio es el que esta página lleva señalando y aquí es máximo:**

- **No se puede analizar** (clase 150): ninguna herramienta sabe qué hace ese campo.
- **No se puede revisar** (clase 146): no está en git.
- **Y es ejecución de código arbitrario** (clase 153): quien pueda editar el diccionario ejecuta lo que
  quiera.

Y VistA lo sabe y lo controla con lo que tiene: **permisos muy restringidos sobre el diccionario, y un
proceso de aprobación** — que es un control organizativo donde otros ecosistemas tienen uno técnico.

Y merece cerrar con el patrón más útil de esta página en M, que es una convención y no un mecanismo:
**el punto de entrada con nombre**.

```mumps
 do EN^PSOORDER          ; EN = entry, el punto de entrada estándar del paquete
 do KILL^PSOORDER         ; limpieza
```

**Todos los paquetes de VistA exponen puntos de entrada con nombres convenidos** —`EN`, `EN1`, `KILL`,
`HELP`—, y eso hace que **cualquier paquete se pueda llamar de la misma forma** sin conocerlo.

Es una interfaz sin declaración de interfaz, sostenida por el estándar de codificación (clase 146), y es
la misma solución que los prefijos de dos letras: **una convención que sustituye a una característica del
lenguaje**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes op a b r |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

op := partes at: 1.
a := (partes at: 2) asNumber.
b := (partes at: 3) asNumber.

r := op = 'suma'
        ifTrue: [ a + b ]
        ifFalse: [ op = 'resta'
            ifTrue: [ a - b ]
            ifFalse: [ a * b ] ].

Transcript show: 'resultado=', r printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Aquí está el dato del gancho: **el libro de los cuatro autores
nació en el mundo de Smalltalk y C++**, y **Erich Gamma, Richard Helm, Ralph Johnson y John Vlissides
daban los ejemplos en los dos lenguajes**.

Y merece señalar lo que eso significa: **muchos de los patrones se descubrieron mirando código
Smalltalk**, donde ya se usaban sin nombre. **Ralph Johnson**, además, es quien dirigió el Refactoring
Browser (clase 150) — la misma comunidad produjo las dos ideas.

Y Smalltalk demuestra la tesis de esta clase de la forma más contundente, porque **la Estrategia idiomática
es un bloque**:

```smalltalk
| operaciones |
operaciones := Dictionary newFrom: {
    'suma'     -> [ :x :y | x + y ].
    'resta'    -> [ :x :y | x - y ].
    'producto' -> [ :x :y | x * y ] }.

(operaciones at: op) value: a value: b
```

**Y hay algo más profundo que eso**, y es lo que hace a Smalltalk peculiar en esta página: **el propio
lenguaje está construido con patrones**.

```smalltalk
condicion ifTrue: [ ... ] ifFalse: [ ... ]
```

**`ifTrue:ifFalse:` no es sintaxis: es un mensaje** (clase 084). Y su implementación **es el patrón
Estado en estado puro**:

```smalltalk
True >> ifTrue: bloqueV ifFalse: bloqueF     ^ bloqueV value
False >> ifTrue: bloqueV ifFalse: bloqueF     ^ bloqueF value
```

**Dos clases, un método cada una, y no hay ningún `if` en la implementación del `if`.** El
comportamiento depende de la clase del receptor — que es la definición del despacho polimórfico y del
patrón Estado.

Lo mismo con los bucles, las colecciones y las excepciones: **el lenguaje se define a sí mismo con
mensajes y bloques**.

Y merece cerrar con el patrón que Smalltalk aportó al catálogo y que hoy está en todas partes: **el
Observador**, que en Smalltalk-80 no era un patrón sino **un método de `Object`** (clase 149):

```smalltalk
modelo addDependent: vista.
modelo changed: #saldo.
```

**Estaba en la raíz de la jerarquía**, disponible para cualquier objeto del sistema desde 1980. Y de ahí
salió MVC, y de MVC, la arquitectura de las interfaces gráficas de los siguientes cuarenta años.

---

## Y de vuelta a la clase

Lo transferible: **un patrón es un nombre para una forma que se repite, y su valor está en el nombre
tanto como en la forma** — decir "aquí hay un Observador" ahorra un párrafo de explicación. Pero la
pregunta que hay que hacerse antes de aplicar uno es siempre la misma: **¿esto resuelve mi problema, o
compensa una limitación que mi lenguaje no tiene?** Aplicar una fábrica abstracta en un lenguaje con
funciones de primera clase suele ser lo segundo. Y el peor uso de un patrón es el más frecuente:
**añadir tres clases para conseguir una flexibilidad que nadie va a necesitar**.

⏮️ [Volver a la clase 151](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
