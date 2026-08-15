# -*- coding: utf-8 -*-
"""Parte 9, lote D — clases 151 y 152. Ver `vivos_parte9.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 151 — Patrones de diseño comparados entre lenguajes
# ---------------------------------------------------------------------------
SPECS["151"] = dict(
    gancho="""
Elegir una operación por su nombre y aplicarla: eso es el patrón Estrategia. Y esta clase existe para
enseñar algo que el libro de patrones no dice y que se ve mejor aquí que en ningún sitio: **muchos
patrones son parches a carencias del lenguaje**. En Lisp, Smalltalk, Perl o Tcl, la Estrategia **no es
un patrón: es pasar una función**. Y hay un dato que lo confirma: **el libro de los cuatro autores nació
en el mundo de Smalltalk y C++**, y sus ejemplos venían de ahí.
""",
    porque="""
Aquí el concepto es el **patrón de diseño como solución recurrente**, y estos lenguajes lo enseñan
porque **cubren los dos extremos del eje que decide qué patrones hacen falta**: el de los lenguajes sin
funciones de primera clase —COBOL, Fortran 77, Ada 83, C++ antes de C++11— donde la Estrategia necesita
una jerarquía entera; y el de los que tratan el código como dato —Lisp, Smalltalk, Tcl, Perl— donde
desaparece.

Y aparece la observación de Peter Norvig que ordena la clase: **de los 23 patrones del libro, 16 son
más simples o invisibles en un lenguaje dinámico**.
""",
    cierre="""
Lo transferible: **un patrón es un nombre para una forma que se repite, y su valor está en el nombre
tanto como en la forma** — decir "aquí hay un Observador" ahorra un párrafo de explicación. Pero la
pregunta que hay que hacerse antes de aplicar uno es siempre la misma: **¿esto resuelve mi problema, o
compensa una limitación que mi lenguaje no tiene?** Aplicar una fábrica abstracta en un lenguaje con
funciones de primera clase suele ser lo segundo. Y el peor uso de un patrón es el más frecuente:
**añadir tres clases para conseguir una flexibilidad que nadie va a necesitar**.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let* ((op (read))
       (a (read))
       (b (read))
       (f (case op
            (suma     #'+)
            (resta    #'-)
            (producto #'*)
            (t        (lambda (x y) (declare (ignore x y)) 0)))))
  (format t "resultado=~D~%" (funcall f a b)))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] op a b

proc suma     {x y} { expr {$x + $y} }
proc resta    {x y} { expr {$x - $y} }
proc producto {x y} { expr {$x * $y} }

puts "resultado=[$op $a $b]"
""", """
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
"""),
        "perl": ("""
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

print "resultado=", $estrategia{$op}->($a, $b), "\\n";
""", """
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
"""),
        "cpp": ("""
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
    std::cout << "resultado=" << (it != estrategia.end() ? it->second(a, b) : 0) << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
ESTRAT ; Patron estrategia -- clase 151
 read linea
 new op, a, b, r
 set op = $piece(linea, " ", 1)
 set a = $piece(linea, " ", 2)
 set b = $piece(linea, " ", 3)
 set r = $select(op="suma" : a + b, op="resta" : a - b, op="producto" : a * b, 1 : 0)
 write "resultado=", r, !
 quit
""", """
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
   Expresión MUMPS: $$FMDIFF^XLFDT(DT, FECHA_NACIMIENTO)\\365.25
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
"""),
        "smalltalk": ("""
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
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 152 — Rendimiento y perfilado
# ---------------------------------------------------------------------------
SPECS["152"] = dict(
    gancho="""
Contar las operaciones y devolver la suma: `operaciones=5 resultado=15`. Es un programa que **se mide a
sí mismo**, que es la forma más antigua y más honesta de perfilar. Y esta clase existe por una razón
que las herramientas no arreglan: **la intuición sobre el rendimiento es sistemáticamente equivocada**.
Aquí está el caso que mejor lo demuestra: **la reescritura de LINPACK a LAPACK multiplicó por diez el
rendimiento sin cambiar un solo algoritmo** — solo el orden en que se tocaba la memoria.
""",
    porque="""
Aquí el concepto es la **medición antes que la optimización**, y estos lenguajes lo enseñan porque
**cubren todo el rango de lo que significa "rápido"**. Fortran y C++ pelean por ciclos y por caché.
COBOL y RPG pelean por operaciones de entrada y salida, que es donde está su tiempo. Ada pelea por el
**peor caso**, no por el promedio. Y Lisp y Smalltalk tienen perfiladores escritos en el propio lenguaje
que muestrean el sistema vivo.

Y aparece la distinción que ordena la clase: **latencia, rendimiento total y peor caso son tres cosas
distintas**, y optimizar una puede empeorar las otras.
""",
    cierre="""
Lo transferible: **medir, cambiar una cosa, volver a medir** — y en ese orden, siempre. La razón es que
el cuello de botella casi nunca está donde se cree: en la mayoría de los programas reales, el tiempo se
va en **esperar entrada y salida, en fallos de caché y en reservar memoria**, no en el bucle que parece
caro. Y la segunda regla, que ahorra más trabajo que ninguna optimización: **preguntar antes si hace
falta que sea rápido**. Un proceso nocturno que tarda veinte minutos y tiene ocho horas de ventana no
tiene un problema de rendimiento, por mucho que se pueda mejorar.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PERFIL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  I       PIC S9(9) COMP.
01  TOTAL   PIC S9(18) COMP VALUE 0.
01  ED-N    PIC -(8)9.
01  ED-T    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        ADD I TO TOTAL
    END-PERFORM

    MOVE N     TO ED-N
    MOVE TOTAL TO ED-T
    DISPLAY "operaciones=" FUNCTION TRIM(ED-N)
            " resultado=" FUNCTION TRIM(ED-T)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** En el mundo del lote, **el rendimiento casi nunca es cuestión de
CPU: es cuestión de entrada y salida**, y esa diferencia de enfoque merece explicarse porque sigue
siendo válida.

Un programa que procesa diez millones de registros **pasa la mayor parte del tiempo esperando al
disco**. Optimizar el cálculo no cambia nada; optimizar los accesos lo cambia todo.

Y las técnicas del mundo mainframe son de una eficacia que sorprende:

**El tamaño de bloque.** Un fichero secuencial se lee por bloques, no por registros:

```jcl
//SALIDA DD DSN=MI.FICHERO,BLKSIZE=27998,LRECL=200
```

**Con `BLKSIZE=0`, el sistema calcula el tamaño de bloque óptimo para el dispositivo** — y pasar de un
bloque pequeño a uno óptimo puede **dividir por veinte el número de operaciones físicas**.

Es la misma idea que el búfer de la clase 104, decidida a nivel de fichero.

**El orden de acceso.** Y aquí está la técnica que define el diseño de estos sistemas:

```text
❌  Leer un fichero de 10 millones de registros y, por cada uno, consultar una tabla indexada.
✓  ORDENAR el fichero por la misma clave que la tabla y leer las dos en paralelo, una vez.
```

**Eso es el *match-merge*, y convierte 10 millones de accesos aleatorios en dos recorridos
secuenciales.** La diferencia en un disco es de dos órdenes de magnitud.

Y por eso **`SORT` es el programa más ejecutado del mainframe** y por eso los productos de ordenación
—DFSORT, Syncsort— son piezas de software muy afinadas.

Es el mismo razonamiento que hoy justifica ordenar antes de unir en un sistema de datos masivos, y es de
los años sesenta.

Y la medición, que en esta plataforma es automática (clase 142):

```text
Los registros SMF dan, por paso y por transacción:
  - CPU en milisegundos
  - operaciones de E/S CONTADAS, por fichero
  - tiempo de espera
  - memoria usada
```

**Con `EXCP count` por fichero se ve exactamente qué fichero está costando el tiempo**, sin instrumentar
nada. Y **Strobe** o **APA** dan el perfil por línea de código.

Es observabilidad de rendimiento por defecto, y es la razón de que la pregunta "¿por qué tarda este
lote?" tenga respuesta en minutos.
"""),
        "fortran": ("""
program perfil
   implicit none
   integer :: n, i
   integer(kind=8) :: total

   read(*, *) n
   total = 0

   do i = 1, n
      total = total + i
   end do

   write(*, '(A,I0,A,I0)') 'operaciones=', n, ' resultado=', total
end program perfil
""", """
**Lo que esta clase enseña en Fortran.** Aquí está el caso del gancho, y merece desarrollarse porque es
la mejor lección de rendimiento que existe: **LINPACK a LAPACK**.

**LINPACK (1979)** expresaba sus algoritmos en operaciones **vector-vector** —BLAS nivel 1—. **LAPACK
(1992)** los reformuló en operaciones **matriz-matriz** —BLAS nivel 3— (clase 149).

**El mismo algoritmo matemático. Diez veces más rápido.**

Y la razón es la de la clase 128: **la jerarquía de memoria**.

```text
Producto escalar (nivel 1):  2n operaciones,  2n datos leídos  →  1 operación por dato
Matriz por vector (nivel 2): 2n² operaciones, n² datos          →  2 operaciones por dato
Matriz por matriz (nivel 3): 2n³ operaciones, 3n² datos          →  ~n operaciones por dato
```

**Solo el nivel 3 hace suficiente trabajo por dato leído como para que la caché compense**. Los otros
dos están limitados por el ancho de banda de memoria: **el procesador está esperando**.

Y la consecuencia práctica que hay que llevarse, y vale para cualquier lenguaje: **en cálculo numérico,
el cuello de botella no es la aritmética — es traer los datos**.

Y de ahí las optimizaciones características de Fortran, todas sobre la memoria:

```fortran
! El orden de los bucles importa: Fortran guarda por COLUMNAS (clase 089)
do j = 1, n
   do i = 1, n
      a(i, j) = ...      ! ✓ i variando rápido: memoria contigua
   end do
end do
! Al revés, cada acceso salta n posiciones: fallo de caché en cada uno
```

**Cambiar el orden de dos bucles puede multiplicar por diez el tiempo**, y es la optimización que más
veces se pasa por alto — porque el código se lee igual de bien de las dos formas.

Y las herramientas del ecosistema:

```bash
gprof ./prog                       # perfil clásico, por función
perf record ./prog; perf report     # muestreo, sin instrumentar
perf stat -e cache-misses ./prog     # ¡CONTADORES DEL PROCESADOR!
valgrind --tool=cachegrind ./prog     # simulación de caché
likwid-perfctr -g MEM ./prog           # ancho de banda de memoria
Intel VTune / Arm MAP                   # perfiladores completos, con MPI
```

**`perf stat -e cache-misses` merece destacarse** porque mide lo que esta explicación dice que importa:
no cuánto tiempo pasa en cada función, sino **cuántas veces el procesador tuvo que esperar a la
memoria**.

Es la métrica que hace visible el problema que LAPACK resolvió, y la que convierte "va lento" en "va
lento por esto".
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Perfil is
   N     : Integer;
   Total : Long_Long_Integer := 0;
begin
   Get (N);

   for I in 1 .. N loop
      Total := Total + Long_Long_Integer (I);
   end loop;

   Put_Line
     ("operaciones=" & Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both) &
      " resultado="  & Ada.Strings.Fixed.Trim (Total'Image, Ada.Strings.Both));
end Perfil;
""", """
**Lo que esta clase enseña en Ada.** Ada plantea esta clase desde un ángulo distinto al de todos los
demás de esta página, y merece explicarlo porque cambia qué se mide: **en tiempo real, lo que importa no
es el promedio — es el peor caso**.

```text
Un algoritmo que tarda 1 ms de media y 50 ms en el peor caso
es PEOR que uno que tarda 5 ms SIEMPRE,
si el plazo del sistema es de 10 ms.
```

Y de ahí un concepto que esta clase debe nombrar y que en otros dominios casi no existe: **el WCET, el
*tiempo de ejecución del peor caso***.

Calcularlo es un problema difícil, y las técnicas merecen conocerse:

| Método | Cómo |
|---|---|
| **Análisis estático** | recorrer todos los caminos del código y sumar los costes de las instrucciones |
| **Medición** | ejecutar con las entradas más desfavorables conocidas, muchas veces |
| **Híbrido** | medir bloques básicos y componer el peor camino |

Y las herramientas del sector —**aiT**, **RapiTime**, **Bound-T**— hacen análisis estático **teniendo en
cuenta la caché y la predicción de saltos del procesador concreto**.

Y aquí aparece una tensión que merece señalarse, porque es contraintuitiva: **las cachés y la ejecución
especulativa mejoran el promedio y empeoran la predecibilidad**.

Por eso **en sistemas críticos a veces se desactivan las cachés**, o se usan procesadores sin
especulación: **se renuncia a velocidad para poder garantizar el plazo**.

Es la aplicación más extrema del cierre de esta clase: **"rápido" no significa nada hasta que se dice
respecto a qué**.

Y las características del lenguaje que sostienen esto son las de la Parte 8 y la clase 146:

```ada
pragma Restrictions (No_Allocators);        --  sin montón: sin pausas imprevisibles
pragma Restrictions (No_Recursion);          --  pila acotada y calculable
pragma Profile (Ravenscar);                   --  planificación analizable
```

**Sin reserva dinámica y sin recursión, el peor caso se puede calcular** — que es justamente por qué
esas restricciones existen.

Y Ada tiene medición en el lenguaje:

```ada
with Ada.Real_Time; use Ada.Real_Time;
T0 : constant Time := Clock;
...
D : constant Time_Span := Clock - T0;
```

**`Ada.Real_Time.Clock` es un reloj monótono con resolución garantizada**, distinto de
`Ada.Calendar.Clock` —la hora del día, que puede saltar—. **Confundirlos es un error clásico de
medición**, y Ada los separa en el sistema de tipos.
"""),
        "pascal": ("""
program Perfil;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I: Integer;
  Total: Int64;

begin
  Read(N);
  Total := 0;

  for I := 1 to N do
    Total := Total + I;

  WriteLn('operaciones=', IntToStr(N), ' resultado=', IntToStr(Total));
end.
""", """
**Lo que esta clase enseña en Pascal.** Free Pascal y Delphi producen código nativo y rápido, y el
ecosistema tiene una tradición de medición que viene de una época en la que el rendimiento se notaba:
**Turbo Pascal competía con el ensamblador**.

Las herramientas:

```bash
fpc -O3 -Xs -CX prog.pas          # -O3: optimización; -CX: enlace inteligente
fpc -pg prog.pas && gprof ./prog   # perfil clásico
valgrind --tool=callgrind ./prog    # grafo de llamadas con costes
```

| Herramienta | Notas |
|---|---|
| **`gprof`** | por función; requiere `-pg` |
| **Sampling Profiler** (Delphi) | muestreo sin instrumentar |
| **AQtime / Nexus Quality Suite** | perfiladores comerciales del mundo Delphi |
| **`EpikTimer`** | medición de alta resolución, portable |
| **`heaptrc`** | reservas y fugas (clase 138) |

Y el ecosistema Pascal aporta a esta clase una lección muy concreta que merece destacarse, porque es la
optimización que más veces resuelve un problema real en este tipo de aplicaciones: **la concatenación de
cadenas en un bucle**.

```pascal
{ ✗ O(n²): cada concatenación copia toda la cadena }
for I := 1 to 100000 do
  S := S + Linea[I];

{ ✓ O(n): un constructor con capacidad que crece }
SB := TStringBuilder.Create;
for I := 1 to 100000 do
  SB.Append(Linea[I]);
S := SB.ToString;
```

**La primera versión con 100.000 elementos tarda minutos; la segunda, milisegundos.**

Y el motivo conecta con la clase 093: **una cadena es un bloque contiguo**, así que concatenar significa
**reservar un bloque nuevo y copiar todo lo anterior** — y hacerlo n veces es cuadrático.

Es el mismo problema en Java, C#, Python y todos los lenguajes con cadenas inmutables, y es
probablemente **el error de rendimiento más común de la programación de aplicaciones**.

Y merece extraer el principio general, porque se aplica a mucho más que a cadenas: **cuidado con las
operaciones que parecen O(1) y son O(n) sobre una estructura que crece**. Concatenar cadenas, insertar
al principio de un arreglo, buscar en una lista: cada una es barata una vez y cuadrática en un bucle.
"""),
        "lisp": ("""
(let ((n (read))
      (total 0))
  (dotimes (i n)
    (incf total (1+ i)))
  (format t "operaciones=~D resultado=~D~%" n total))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene, por lo que la clase 124 explicó, una herramienta
de medición que ningún lenguaje compilado de esta página iguala en comodidad: **`time` mide una
expresión cualquiera, en marcha, sin recompilar**.

```lisp
(time (procesar-todo datos))
```

```text
Evaluation took:
  2.340 seconds of real time
  2.310000 seconds of total run time (2.180000 user, 0.130000 system)
  [ Run times consist of 0.410 seconds GC time, and 1.900 seconds non-GC time. ]
  98.72% CPU
  6,382,142,268 processor cycles
  1,048,585,712 bytes consed          ← ¡MEMORIA RESERVADA!
```

**Las dos líneas destacadas son las que Lisp da y casi nadie más**: **cuánto tiempo se fue en el
recolector de basura** y **cuántos bytes se reservaron**.

Y eso es decisivo, porque en un lenguaje con recolección **el problema de rendimiento casi nunca es el
cálculo: es la basura que se genera** (clase 131).

**Un `1.048.585.712 bytes consed` en un bucle que "no reserva nada" es el diagnóstico completo.**

Y el perfilador estadístico:

```lisp
(require :sb-sprof)
(sb-sprof:with-profiling (:report :flat :mode :cpu)
  (procesar-todo datos))
```

```text
Self  Total  Cumul   Function
25.3   45.1   25.3   SB-KERNEL:%COERCE-CALLABLE-TO-FUN
18.2   18.2   43.5   MI-PAQUETE::CALCULAR
```

**`:mode :alloc`** cambia el eje: **muestrea reservas en lugar de tiempo**, y dice **qué función genera
la basura**.

Y Lisp tiene una capacidad de optimización que merece cerrar esta explicación y que viene de la clase
124: **el compilador dice por qué no puede optimizar**.

```lisp
(declaim (optimize (speed 3) (safety 1) (debug 0)))

(defun sumar (a b) (+ a b))
; note: doing signed word to integer coercion
;       unable to open code because: the operands might not be fixnums
```

**Esa nota es una invitación**: añadiendo una declaración de tipo, el compilador genera aritmética
nativa:

```lisp
(defun sumar (a b)
  (declare (type fixnum a b) (optimize (speed 3)))
  (+ a b))
```

**Es optimización guiada por el compilador, en diálogo**, y es una experiencia que casi ningún otro
lenguaje de esta página ofrece: los demás optimizan en silencio o no optimizan, pero no explican.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set total 0
for {set i 1} {$i <= $n} {incr i} {
    incr total $i
}

puts "operaciones=$n resultado=$total"
""", """
**Lo que esta clase enseña en Tcl.** Tcl trae la medición en el núcleo, con un comando pensado
exactamente para esta clase:

```tcl
puts [time { procesar $datos } 1000]
# → 42.7 microseconds per iteration
```

**`time` ejecuta un guion N veces y da el promedio**, que es la forma correcta de medir algo rápido:
**una sola ejecución mide sobre todo el ruido**.

Y Tcl tiene una particularidad de rendimiento que merece explicarse porque es de las más
contraintuitivas de esta página y ya apareció en la clase 146: **las llaves cambian el rendimiento por
un factor grande**.

```tcl
expr {$a + $b}      ;# se compila a bytecode UNA VEZ (clase 125)
expr "$a + $b"       ;# se sustituye y se REANALIZA en cada iteración
```

**La segunda forma puede ser diez veces más lenta**, porque el compilador de bytecode no puede compilar
una expresión que no conoce hasta que se ejecuta.

Es el mismo principio que en cualquier lenguaje con compilación: **lo que se construye en marcha no se
puede optimizar de antemano**.

Y la otra propiedad de rendimiento característica de Tcl es **la representación dual** (clase 081):

```tcl
set x 42          ;# guardado como cadena "42"
incr x             ;# ahora TAMBIÉN tiene una representación entera, en caché
puts $x            ;# vuelve a generar la cadena si hace falta
```

**Un valor de Tcl guarda a la vez su forma textual y su forma interna optimizada**, y **la conversión se
hace una vez y se recuerda**.

Y de ahí un antipatrón clásico que merece conocerse: **alternar los usos destruye la caché**.

```tcl
# ✗ cada vuelta invalida la representación interna: "shimmering"
for {set i 0} {$i < 100000} {incr i} {
    set s "$lista"        ;# fuerza la forma de CADENA
    lappend lista $i       ;# fuerza la forma de LISTA
}
```

**Ese fenómeno se llama *shimmering*** y es el problema de rendimiento más específico de Tcl: **un valor
que se usa alternativamente como lista y como cadena se reconvierte en cada paso**, y una operación
O(1) pasa a ser O(n).

Y las herramientas:

```tcl
package require profiler
::profiler::init
::profiler::print
tcl::unsupported::disassemble proc miProc     ;# ¡ver el BYTECODE! (clase 125)
```
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $total = 0;
$total += $_ for 1 .. $n;

print "operaciones=$n resultado=$total\\n";
""", """
**Lo que esta clase enseña en Perl.** `$total += $_ for 1 .. $n;` es un **modificador de sentencia**, y
`1 .. $n` en un `for` **no construye la lista**: Perl optimiza los rangos en bucles para iterar
perezosamente.

Es un detalle relevante para esta clase: **la misma sintaxis en otro contexto —`my @l = (1 .. $n)`— sí
reserva n elementos**.

Y Perl tiene el mejor perfilador de guiones de esta página, y merece explicarlo: **`Devel::NYTProf`**.

```bash
perl -d:NYTProf script.pl
nytprofhtml --open
```

Y lo que da es notablemente más de lo habitual:

- **Tiempo por LÍNEA**, no solo por subrutina.
- **Tiempo por *bloque* y por sentencia.**
- **Número de llamadas y tiempo exclusivo frente a inclusivo.**
- **Un mapa de calor sobre el código fuente**, en HTML.
- **Y el tiempo de las llamadas a `eval` y a los módulos**, incluido el tiempo de carga.

**El desglose por línea es lo que lo hace útil de verdad**, porque en un lenguaje denso una sola línea
puede contener una expresión regular, dos llamadas y una ordenación.

Y Perl aporta a esta clase la advertencia sobre las expresiones regulares, que es su problema de
rendimiento característico y que conecta con la clase 153: **el retroceso catastrófico**.

```perl
# ✗ esta expresión tarda un tiempo EXPONENCIAL con la entrada
$texto =~ /^(a+)+$/;
# con "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!" tarda años
```

**El motor prueba todas las formas de repartir las `a` entre los dos cuantificadores.**

Y las defensas:

```perl
use re 'debug';                      # ver qué hace el motor
$texto =~ /^(?>a+)+$/;                # grupo atómico: sin retroceso
$texto =~ /^a++$/;                     # cuantificador posesivo
use Regexp::Debugger;                   # depurador interactivo de regex
```

Es un problema de rendimiento que **también es una vulnerabilidad** —el ataque se llama ReDoS— y es un
buen ejemplo de por qué esta clase y la 153 están juntas: **una entrada elegida por un atacante puede
convertir un tiempo lineal en exponencial**, y ahí el rendimiento deja de ser una cuestión de comodidad.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    long long total = 0;
    for (long long i = 1; i <= n; ++i) total += i;

    std::cout << "operaciones=" << n << " resultado=" << total << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ tiene las mejores herramientas de medición de esta página, y una
lección que merece ir primero: **el compilador es más listo de lo que parece**.

```bash
g++ -O2 -S prog.cpp    # ver el ensamblador generado
```

**Con `-O2`, un bucle que suma 1..n puede desaparecer por completo** si el compilador demuestra que
equivale a `n*(n+1)/2`. Es una optimización real de GCC y LLVM.

Y de ahí la primera advertencia de esta clase, que arruina más mediciones de las que se admite: **el
compilador elimina el código cuyo resultado no se usa**.

```cpp
// ✗ esto no mide nada: el bucle se elimina entero
auto t0 = now();
for (int i = 0; i < 1000000; ++i) calcular(i);
auto t1 = now();

// ✓ impedir la eliminación
benchmark::DoNotOptimize(calcular(i));
```

**Toda medición de microrrendimiento en C++ tiene que usar una barrera de optimización**, o mide el
tiempo de un bucle vacío. Es la razón de existir de `google/benchmark`.

Y el arsenal, organizado por la pregunta que responde:

| Pregunta | Herramienta |
|---|---|
| ¿Dónde se va el tiempo? | `perf record`, VTune, Instruments |
| ¿Cuántos fallos de caché? | `perf stat -e cache-misses`, cachegrind |
| ¿Qué reserva memoria? | `heaptrack`, massif, `perf -e page-faults` |
| ¿Qué hace el compilador? | **Compiler Explorer (godbolt.org)**, `-S`, `-fopt-info` |
| ¿Cuánto tarda esta función? | `google/benchmark`, `nanobench` |
| ¿Y en producción? | **perfiladores continuos**: `pprof`, Parca, eBPF |

**Compiler Explorer merece la mención** porque cambió la cultura: **ver el ensamblador de varios
compiladores lado a lado, en el navegador, al instante** convirtió una pregunta de expertos en algo que
cualquiera puede comprobar.

Y merece cerrar con la observación que la clase 128 anticipó y que en C++ es la más rentable de todas:
**la disposición de los datos importa más que el código**.

```cpp
// ✗ Array of Structs: para sumar solo las x, se traen y y z inútilmente
struct P { float x, y, z; };  std::vector<P> puntos;

// ✓ Struct of Arrays: los x están contiguos
struct Puntos { std::vector<float> x, y, z; };
```

**El segundo puede ser tres veces más rápido en un recorrido que solo usa `x`**, porque **cada línea de
caché trae solo datos útiles**.

Es exactamente la misma lección que LAPACK en Fortran de esta página, aplicada a estructuras en lugar de
a matrices: **el rendimiento moderno es un problema de memoria, no de aritmética**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi PERFIL;
  n int(10) const;
end-pi;

dcl-s i     int(10);
dcl-s total int(20);

total = 0;

for i = 1 to n;
  total += i;
endfor;

dsply ('operaciones=' + %char(n) + ' resultado=' + %char(total));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i comparte el diagnóstico de COBOL en esta página —**el tiempo
está en la entrada y salida**— y aporta la técnica que más rendimiento ha ganado en esta plataforma en
los últimos veinte años, y que merece explicarse porque es un cambio de mentalidad completo: **pasar de
registro a registro a operar por conjuntos**.

```rpgle
// ✗ el idioma clásico de RPG: un viaje por registro
setll (cliente) pedidos;
dow %equal;
  reade (cliente) pedidos;
  if not %eof;
    total += pedidos.importe;
  endif;
enddo;
```

```sql
-- ✓ una sola llamada, y el motor optimiza el acceso
exec sql SELECT SUM(importe) INTO :total
         FROM pedidos WHERE cliente = :cliente;
```

**La diferencia con un millón de filas es de dos órdenes de magnitud**, y el motivo es doble:

**Primero, cada operación registro a registro cruza la frontera entre el programa y el gestor de base
de datos.** Un millón de registros son un millón de cruces.

**Y segundo, y es lo importante: el optimizador de Db2 puede elegir el plan.** Puede usar un índice,
puede paralelizar, puede leer solo el índice si contiene la columna. **El bucle no puede: hace lo que
dice, en el orden que dice.**

Y las herramientas de medición de la plataforma son de las mejores de esta página:

| Herramienta | Qué da |
|---|---|
| **`WRKACTJOB`** | CPU por trabajo, en tiempo real |
| **`STRPFRCOL` / Performance Tools** | recogida histórica de todo el sistema |
| **Visual Explain** | **el plan de acceso de una consulta, en gráfico** |
| **Db2 Index Advisor** | **qué índices FALTAN, deducido del uso real** |
| **`QSYS2.ACTIVE_JOB_INFO`** | todo lo anterior, por SQL (clase 142) |
| **`STRPEX`** (Performance Explorer) | perfil por sentencia de programa |

**El *Index Advisor* merece destacarse** porque hace algo poco común: **el sistema registra las
consultas que se ejecutan y deduce qué índices habrían ayudado**, con una estimación de la mejora.

```sql
SELECT * FROM QSYS2.SYSIXADV ORDER BY TIMES_ADVISED DESC;
```

**Es el sistema diciendo dónde está el cuello de botella**, sin que nadie perfile nada, y es la
aplicación más directa del cierre de esta clase: **medir primero**, con la ventaja de que aquí la medida
ya está tomada.
"""),
        "pli": ("""
 perfil: procedure options(main);

    declare n     fixed binary(31);
    declare i     fixed binary(31);
    declare total fixed binary(63) initial(0);

    get list (n);

    do i = 1 to n;
       total = total + i;
    end;

    put skip list ('operaciones=' || trim(char(n)) ||
                   ' resultado=' || trim(char(total)));

 end perfil;
""", """
**Lo que esta clase enseña en PL/I.** PL/I comparte con COBOL el mundo de la medición por SMF (clase 142)
y aporta una lección de rendimiento propia del lenguaje que merece explicarse, porque es la trampa
número uno de PL/I: **las conversiones implícitas cuestan**.

```pli
 declare a fixed decimal(15,2);
 declare b fixed binary(31);
 declare c float decimal(16);

 a = a + b;         /* binario -> decimal: CONVERSIÓN en cada vuelta */
 c = a * 1.5;        /* decimal -> flotante: otra */
```

**Cada conversión es código generado que no se ve en el fuente**, y en un bucle de millones de vueltas es
la mayor parte del tiempo.

Y el diagnóstico está donde el mundo mainframe siempre lo pone (clase 137): **en el listado de
compilación**.

```text
OPTIONS: LIST, AGGREGATE, ATTRIBUTES, XREF
```

**Con `LIST`, el compilador imprime el ensamblador generado**, y ahí se ven las llamadas a las rutinas
de conversión de la biblioteca — que en el fuente eran un signo `+`.

Es la misma técnica que Compiler Explorer en C++ de esta página, hecha con un listado impreso, y por el
mismo motivo: **ver lo que de verdad se ejecuta, no lo que se escribió**.

Y la regla práctica que se deriva y que vale para cualquier lenguaje con tipos numéricos ricos: **usar
el mismo tipo en todo el cálculo**.

```pli
 declare (a, b, total) fixed binary(63);     /* todo del mismo tipo: cero conversiones */
```

Y hay una decisión de rendimiento propia de PL/I que merece conocerse porque no tiene equivalente:
**las condiciones activadas cuestan**.

```pli
 (subscriptrange, stringrange, size):     /* comprobaciones ACTIVAS */
 procesar: procedure;
```

**Cada acceso a un arreglo comprueba el índice; cada subcadena comprueba los límites** (clases 124 y
137). En un bucle intensivo, eso puede ser el 30 % del tiempo.

Y la decisión —**activarlas en desarrollo y en pruebas, y decidir conscientemente en producción**— es
exactamente la misma que Pascal con `{$R+}`, Ada con `pragma Suppress` y C++ con `assert`.

Es la constante de toda esta parte del curso: **seguridad y velocidad son la misma palanca**, y lo único
que cambia entre lenguajes es quién decide dónde ponerla y si esa decisión queda escrita.
"""),
        "mumps": ("""
PERFIL ; Medir operaciones -- clase 152
 read n
 new i, total
 set total = 0
 for i = 1:1:n set total = total + i
 write "operaciones=", n, " resultado=", total, !
 quit
""", """
**Lo que esta clase enseña en M.** M tiene un modelo de rendimiento peculiar y muy claro: **casi todo el
tiempo se va en la base de datos**, porque **en M no hay diferencia entre una variable y la base de
datos** salvo el circunflejo.

```mumps
 set x = 1            ; memoria: nanosegundos
 set ^x = 1            ; DISCO: microsegundos, y transaccional
```

**Ese circunflejo es la diferencia entre una operación de memoria y una de base de datos**, y es un
carácter.

Y de ahí que la optimización característica de M sea la que ya apareció en la clase 099: **el diseño de
los subíndices de la global**.

```mumps
 ; ✗ recorrer todos los pacientes buscando por apellido
 for  set dfn = $order(^PACIENTE(dfn)) quit:dfn=""  do
 . if $piece(^PACIENTE(dfn, 0), "^", 1) [ apellido ...

 ; ✓ un ÍNDICE: la respuesta en un salto
 set dfn = $order(^PACIENTE("B", apellido, ""))
```

**`^PACIENTE("B", apellido, dfn)` es un índice secundario**, y en VistA se llaman así —`"B"`, `"C"`,
`"AC"`— por convención de FileMan.

**Y `$order` sobre él es O(log n)**, porque las globals son árboles B en disco (clase 099).

Es el mismo razonamiento que un índice de base de datos relacional, con una diferencia importante:
**aquí el índice lo mantiene el programa**, no el motor. Si alguien escribe sin actualizar el índice, el
índice miente — y es el fallo clásico de este mundo.

Y las herramientas de medición:

```mumps
 write $zjobexam                    ; volcado del estado del proceso
 write $storage                      ; memoria disponible
 do ^%SS                              ; estado del sistema: procesos y su actividad
 view "GVSTAT"                         ; estadísticas de acceso a globals (GT.M/YottaDB)
```

**`GVSTAT` es la métrica clave de esta plataforma**: **cuántas lecturas y escrituras de global ha hecho
el proceso**, desglosadas.

Y es la aplicación exacta del cierre de esta clase: **no se mide el tiempo, se cuentan las operaciones
que cuestan**. Un proceso que hace un millón de accesos a global tiene un problema de diseño de índices,
y eso se ve en el contador antes que en el reloj.

Es lo mismo que el `EXCP count` de COBOL en esta página: **en sistemas dominados por la entrada y
salida, contar las operaciones diagnostica mejor que cronometrar**.
"""),
        "smalltalk": ("""
| n total |

n := stdin nextLine trimBoth asNumber.
total := 0.

1 to: n do: [ :i | total := total + i ].

Transcript
    show: 'operaciones=', n printString;
    show: ' resultado=', total printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk parte de una desventaja de rendimiento evidente
—**todo es un objeto y todo es un envío de mensaje** (clase 125)— y tiene, a cambio, **el perfilador más
integrado de esta página**.

```smalltalk
MessageTally spyOn: [ self procesarTodo ].
```

Y lo que produce es un árbol de llamadas con porcentajes, sobre el sistema vivo:

```text
 - 100.0% (2,340ms) MiClase>>procesarTodo
    | 62.1% (1,453ms) MiClase>>calcular:
    |    | 48.3% (1,130ms) Collection>>detect:
    |    |    | 45.1% (1,055ms) OrderedCollection>>do:
    | 31.2% (730ms) MiClase>>formatear:
```

**Está escrito en Smalltalk, muestrea el proceso desde otro proceso, y no requiere recompilar nada.**

Y el resto del arsenal, todo dentro del sistema:

```smalltalk
[ self calcular ] timeToRun.                    "milisegundos"
[ self calcular ] bench.                         "iteraciones por segundo"
Smalltalk vmStatistics.                           "estadísticas de la máquina virtual"
Smalltalk garbageCollect; garbageCollectMost.      "forzar el recolector"
SpaceTally new spaceTally: MiClase.                 "cuánta memoria ocupa cada clase"
```

**`SpaceTally` merece la mención** porque responde a una pregunta que en la mayoría de los lenguajes es
difícil: **cuánta memoria ocupan las instancias de cada clase, en el sistema real**.

Y Smalltalk aporta a esta clase una lección que la clase 125 anticipó y que merece cerrar: **el
rendimiento de un lenguaje dinámico depende de las cachés de envío**.

```text
Envío de mensaje SIN caché:  buscar el selector en la clase, subir por la jerarquía...
Envío CON caché en línea:    comprobar si la clase es la misma que la última vez → saltar
```

**Y la caché monomórfica en línea acierta más del 90 % de las veces en el código real**, porque **en un
punto concreto del programa, casi siempre llega el mismo tipo de objeto**.

Ese descubrimiento —hecho en Smalltalk y en Self a finales de los ochenta— es el fundamento de **todos
los compiladores JIT modernos**: V8, HotSpot, LuaJIT y PyPy usan la misma técnica, con el mismo nombre.

Y la conclusión que conecta con la primera línea de esta explicación: **la desventaja teórica del
despacho dinámico se recuperó en gran parte con una observación empírica sobre cómo se comportan los
programas de verdad**.

Es la mejor ilustración del cierre de esta clase: **la intuición decía que el despacho dinámico era
inviable; la medición dijo que era predecible**.
"""),
    },
)
