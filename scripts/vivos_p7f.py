# -*- coding: utf-8 -*-
"""Parte 7, lote F — clase 112. Ver `vivos_parte7.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 112 — Interfaces, traits y clases abstractas
# ---------------------------------------------------------------------------
SPECS["112"] = dict(
    gancho="""
Dos figuras y un `area()` común. La diferencia con la clase anterior es sutil y decisiva: **aquí lo
que se comparte es el contrato, no la implementación**. Y hay un dato que ordena la página: **la
interfaz como construcción separada de la clase es tardía** —Ada la añadió en 2005, COBOL en 2002,
Delphi en 1997— porque durante décadas se creyó que la herencia bastaba. No bastaba.
""",
    porque="""
Aquí el concepto es la **abstracción sin implementación**, y estos lenguajes lo enseñan porque probaron
las tres soluciones. **Herencia múltiple de clases abstractas**: C++, que funciona y trae el diamante.
**Herencia simple más interfaces**: Ada 2005, COBOL 2002, Delphi, Fortran con tipos abstractos — el
compromiso que ganó. **Y sin nada**: Smalltalk, Perl clásico, Tcl y Lisp, donde **si responde al
mensaje, sirve**, y el contrato es una convención.

Esa tercera vía no es inferior: es la que hace que `printOn:` funcione sobre cualquier objeto y que
`std::sort` funcione sobre cualquier cosa comparable. **La comprobación es lo que cambia, no la
capacidad.**
""",
    cierre="""
Lo transferible: **una interfaz es una promesa de comportamiento, y su valor depende de quién la
comprueba y cuándo**. Comprobada al compilar —Ada, C++, Fortran— falla pronto y cuesta ceremonia.
Comprobada al llamar —Smalltalk, Perl, Tcl— es flexible y falla tarde, en producción. Comprobada por
convención y pruebas es lo que hacen los lenguajes dinámicos serios. Ninguna es gratis; lo caro es
**no decidir cuál estás usando** y descubrirlo cuando el objeto equivocado llega al sitio equivocado.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. IFACE.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  T0      PIC X(20).
01  T1      PIC X(20).
01  T2      PIC X(20).
01  A       PIC S9(9)  COMP-3 VALUE 0.
01  B       PIC S9(9)  COMP-3 VALUE 0.
01  SUPERF  PIC S9(18) COMP-3 VALUE 0.
01  ED-A    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO T0 T1 T2

    COMPUTE A = FUNCTION NUMVAL(T1)
    IF T2 NOT = SPACES
        COMPUTE B = FUNCTION NUMVAL(T2)
    END-IF

    EVALUATE FUNCTION TRIM(T0)
        WHEN "cuadrado"    COMPUTE SUPERF = A * A
        WHEN "rectangulo"  COMPUTE SUPERF = A * B
        WHEN OTHER         MOVE 0 TO SUPERF
    END-EVALUATE

    MOVE SUPERF TO ED-A
    DISPLAY "area=" FUNCTION TRIM(ED-A)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El COBOL de producción resuelve esto con el `EVALUATE` que ya
se comentó en la clase 111, y merece decir lo que **sí** tiene el estándar de 2002: **interfaces de
verdad, con su propia unidad de compilación**.

```cobol
INTERFACE-ID. Figura.
PROCEDURE DIVISION.
METHOD-ID. Area.
DATA DIVISION.
LINKAGE SECTION.
01  RESULTADO PIC S9(18) COMP-3.
PROCEDURE DIVISION RETURNING RESULTADO.
END METHOD Area.
END INTERFACE Figura.
```

Y su implementación:

```cobol
CLASS-ID. Cuadrado INHERITS FROM Base IMPLEMENTS Figura.
```

Fíjate en la palabra **`INTERFACE-ID`**: en COBOL la interfaz **no es una clase abstracta disfrazada**,
es una construcción propia con su propia división de identificación, al mismo nivel que
`PROGRAM-ID`, `CLASS-ID` y `FUNCTION-ID`.

Ese diseño —**herencia simple más interfaces múltiples**— es exactamente el de Java, y no es
casualidad: el subcomité de orientación a objetos de COBOL trabajó en los noventa con Java delante y
con el objetivo declarado de **interoperar con él**.

De ahí sale la capacidad que se mencionó en la clase 110 y que aquí encaja del todo: en IBM Enterprise
COBOL, **una clase COBOL puede implementar una interfaz Java**, y una clase Java puede heredar de una
COBOL. Los dos modelos de objetos están alineados a propósito.

Y ahí está lo que esta sección quiere mostrar: la orientación a objetos no se añadió a COBOL para que
la gente escribiera COBOL orientado a objetos. **Se añadió para que el COBOL existente pudiera vivir
dentro de un sistema Java**, que es donde estaba yendo la industria.

Es la misma estrategia que `JSON GENERATE` (clase 105) y z/OS Connect: **modernizar la frontera, no el
núcleo**.
"""),
        "fortran": ("""
module figuras
   implicit none

   type, abstract :: figura                    ! la "interfaz"
   contains
      procedure(area_i), deferred :: area
   end type figura

   abstract interface
      function area_i(self) result(r)
         import :: figura
         class(figura), intent(in) :: self
         integer :: r
      end function area_i
   end interface

   type, extends(figura) :: cuadrado
      integer :: lado = 0
   contains
      procedure :: area => area_cuadrado
   end type cuadrado

   type, extends(figura) :: rectangulo
      integer :: ancho = 0, alto = 0
   contains
      procedure :: area => area_rectangulo
   end type rectangulo

contains

   function area_cuadrado(self) result(r)
      class(cuadrado), intent(in) :: self
      integer :: r
      r = self%lado * self%lado
   end function area_cuadrado

   function area_rectangulo(self) result(r)
      class(rectangulo), intent(in) :: self
      integer :: r
      r = self%ancho * self%alto
   end function area_rectangulo

end module figuras


program iface
   use figuras
   implicit none

   class(figura), allocatable :: f
   character(len=200) :: linea
   character(len=20)  :: tipo
   integer :: a, b

   read(*, '(A)') linea
   read(linea, *) tipo

   if (trim(tipo) == 'cuadrado') then
      read(linea, *) tipo, a
      allocate(cuadrado :: f)
      select type (f)
      type is (cuadrado)
         f%lado = a
      end select
   else
      read(linea, *) tipo, a, b
      allocate(rectangulo :: f)
      select type (f)
      type is (rectangulo)
         f%ancho = a
         f%alto  = b
      end select
   end if

   write(*, '(A,I0)') 'area=', f%area()
end program iface
""", """
**Lo que esta clase enseña en Fortran.** **Fortran no tiene interfaces**: tiene **tipos abstractos con
procedimientos diferidos**, que es el modelo de C++ y no el de Java.

```fortran
type, abstract :: figura
contains
   procedure(area_i), deferred :: area
end type
```

`deferred` es el `= 0` de C++ y el `abstract` de Pascal: **declara el método sin cuerpo y obliga a
implementarlo**. Y como la herencia de Fortran es simple, **un tipo solo puede tener un ancestro
abstracto** — no hay forma de decir "esto es dibujable y además serializable".

Esa es una carencia real y reconocida, y el apaño idiomático es el que se usa en los códigos
científicos: **componer con punteros a procedimiento** (clase 085).

```fortran
type :: modelo
   procedure(calc_i), pointer, nopass :: calcular => null()
   procedure(salida_i), pointer, nopass :: escribir => null()
end type
```

Cada campo es un método que se asigna al construir el objeto. Es programación por composición de
funciones, muy parecida a cómo se hace en Go con campos de tipo función y en C con estructuras de
punteros. Y con **`nopass`**, el procedimiento no recibe el objeto — hay que pasarlo aparte.

Y aquí hay algo que Fortran hace mejor que la mayoría y que esta clase es el sitio de contar: **la
interfaz explícita es una construcción central del lenguaje**, mucho más allá de los objetos.

```fortran
interface
   function externa(x) result(r)
      real, intent(in) :: x
      real :: r
   end function
end interface
```

Un bloque `interface` describe la firma de un procedimiento **para que el compilador compruebe sus
llamadas**, y es lo que hace falta cuando el procedimiento vive fuera de un módulo — típicamente
código en C o una biblioteca antigua. Es la misma idea que un fichero de cabecera, con dos ventajas:
**está en el lenguaje y se comprueba de verdad**.

`interface operator(+)`, `interface assignment(=)` y las **interfaces genéricas** —varios
procedimientos bajo un nombre, elegidos por los tipos de los argumentos— usan el mismo mecanismo. En
Fortran, "interfaz" significa firma comprobada, no contrato de objetos.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Iface is

   --  En un PAQUETE: solo así las operaciones despachan (clase 111).
   package Figuras is
      type Figura is interface;                       --  INTERFAZ (Ada 2005)
      function Area (F : Figura) return Integer is abstract;

      type Cuadrado is new Figura with record
         Lado : Integer := 0;
      end record;
      overriding function Area (F : Cuadrado) return Integer;

      type Rectangulo is new Figura with record
         Ancho, Alto : Integer := 0;
      end record;
      overriding function Area (F : Rectangulo) return Integer;
   end Figuras;

   package body Figuras is
      overriding function Area (F : Cuadrado) return Integer is (F.Lado * F.Lado);
      overriding function Area (F : Rectangulo) return Integer is (F.Ancho * F.Alto);
   end Figuras;

   use Figuras;

   type Ref is access all Figura'Class;

   F      : Ref;
   Linea  : String (1 .. 200);
   Ultimo : Natural;
   Corte  : Natural := 0;
   A, B   : Integer := 0;
   Fin    : Positive;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         Corte := I;
         exit;
      end if;
   end loop;

   if Linea (1 .. Corte - 1) = "cuadrado" then
      Get (Linea (Corte + 1 .. Ultimo), A, Fin);
      F := new Cuadrado'(Lado => A);
   else
      Get (Linea (Corte + 1 .. Ultimo), A, Fin);
      Get (Linea (Fin + 1 .. Ultimo), B, Fin);
      F := new Rectangulo'(Ancho => A, Alto => B);
   end if;

   Put ("area=");
   Put (Area (F.all), Width => 1);
   New_Line;
end Iface;
""", """
**Lo que esta clase enseña en Ada.** **Ada tardó veintidós años en tener interfaces**: el lenguaje es
de 1983, la orientación a objetos llegó en 1995 y `type X is interface` en **Ada 2005**.

Esa espera está documentada y la razón es la de siempre en Ada: **el comité no añade nada hasta saber
exactamente qué garantías da**. Y la solución que eligieron tiene tres tipos distintos de interfaz,
que ningún otro lenguaje de esta página distingue:

```ada
type Figura           is interface;              --  cualquier implementación
type Recurso          is limited interface;       --  implementaciones NO copiables
type Sensor           is synchronized interface;   --  solo tareas u objetos protegidos
type Bomba            is task interface;            --  solo TAREAS
type Contador_Seguro  is protected interface;        --  solo objetos protegidos
```

Las tres últimas son propias del modelo de concurrencia de Ada y no tienen equivalente: **declaran que
lo que implemente esta interfaz debe ser un objeto concurrente**, con lo que el compilador garantiza
que las llamadas están sincronizadas.

Eso permite escribir código genérico sobre "algo que se puede llamar de forma segura desde varias
tareas", con comprobación en compilación. En Java, `synchronized` es una propiedad del método; aquí es
parte del tipo.

Ada permite **implementar varias interfaces** y **heredar de una sola clase**, el compromiso que ganó:

```ada
type Perro is new Animal and Sonoro and Serializable with record ... end record;
```

Y hay una regla que evita el problema clásico de la herencia múltiple: **las interfaces de Ada no
pueden tener componentes ni implementación**. Solo declaran operaciones. Sin estado, no hay diamante
de datos que resolver.

Ada 2012 añadió una capacidad que las hace mucho más útiles: **las operaciones de interfaz pueden
tener un cuerpo por defecto** —los *null procedures* y las funciones de expresión— con lo que se
consigue el equivalente de los métodos `default` de Java 8, ocho años antes.

Y como en la clase 111, **los contratos se heredan y se comprueban**: una implementación no puede
debilitar la postcondición declarada en la interfaz.
"""),
        "pascal": ("""
program Iface;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TFigura = class                          { clase ABSTRACTA }
    function Area: Integer; virtual; abstract;
  end;

  TCuadrado = class(TFigura)
    Lado: Integer;
    function Area: Integer; override;
  end;

  TRectangulo = class(TFigura)
    Ancho, Alto: Integer;
    function Area: Integer; override;
  end;

function TCuadrado.Area: Integer;
begin
  Result := Lado * Lado;
end;

function TRectangulo.Area: Integer;
begin
  Result := Ancho * Alto;
end;

var
  F: TFigura;
  Linea, Tipo, Resto: string;
  P1, P2: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P1 := Pos(' ', Linea);
  Tipo := Copy(Linea, 1, P1 - 1);
  Resto := Trim(Copy(Linea, P1 + 1, Length(Linea)));

  if Tipo = 'cuadrado' then
  begin
    F := TCuadrado.Create;
    TCuadrado(F).Lado := StrToInt(Resto);
  end
  else
  begin
    F := TRectangulo.Create;
    P2 := Pos(' ', Resto);
    TRectangulo(F).Ancho := StrToInt(Copy(Resto, 1, P2 - 1));
    TRectangulo(F).Alto  := StrToInt(Trim(Copy(Resto, P2 + 1, Length(Resto))));
  end;

  try
    WriteLn('area=', IntToStr(F.Area));
  finally
    F.Free;
  end;
end.
""", """
**Lo que esta clase enseña en Pascal.** El programa usa una **clase abstracta** porque es lo más
directo, y Object Pascal tiene además **interfaces de verdad** desde Delphi 3 (1997), con un origen
muy concreto: **COM, el modelo de componentes de Windows**.

```pascal
type
  IFigura = interface
    ['{8A2B4C10-1234-5678-9ABC-DEF012345678}']    { GUID obligatorio }
    function Area: Integer;
  end;

  TCuadrado = class(TInterfacedObject, IFigura)
    function Area: Integer;
  end;
```

Ese **GUID** entre corchetes es lo que las distingue de todas las demás interfaces de esta página, y
explica su diseño: **una interfaz de Delphi ES una interfaz COM**. El identificador global permite
preguntar a un objeto en ejecución si soporta un contrato:

```pascal
if Supports(Objeto, IFigura, F) then
  WriteLn(F.Area);
```

`Supports` es `QueryInterface` de COM con otro nombre. Y por eso las interfaces de Delphi heredan de
`IUnknown` y llevan **conteo de referencias** con `AddRef`/`Release`, lo que da la gestión automática
de memoria que se comentó en la clase 103.

Esa herencia de COM tiene una consecuencia práctica que sorprende a quien viene de Java: **mezclar
referencias de objeto y de interfaz al mismo objeto produce doble liberación**, porque el conteo solo
ve unas.

Y Delphi 10.3 (2018) añadió lo que faltaba para la composición:

```pascal
type
  IFigura = interface
    function Area: Integer;
  end;

  TFiguraHelper = class helper for TFigura         { HELPER: métodos añadidos }
    function Descripcion: string;
  end;
```

Los **helpers de clase y de registro** permiten añadir métodos a un tipo existente **sin heredar y sin
tocarlo** — las extensiones de clase de Smalltalk (clase 109), los métodos de extensión de C# y las
extensiones de Swift, con la misma limitación: **solo un helper activo por tipo y por ámbito**, lo que
evita el problema de las colisiones pero limita mucho su uso.
"""),
        "lisp": ("""
(defgeneric area (f))                          ; la "interfaz": una función genérica

(defclass cuadrado ()
  ((lado :initarg :lado :reader lado)))
(defmethod area ((f cuadrado)) (* (lado f) (lado f)))

(defclass rectangulo ()
  ((ancho :initarg :ancho :reader ancho)
   (alto  :initarg :alto  :reader alto)))
(defmethod area ((f rectangulo)) (* (ancho f) (alto f)))

(let* ((tipo (symbol-name (read)))
       (a (read))
       (f (if (string-equal tipo "cuadrado")
              (make-instance 'cuadrado :lado a)
              (make-instance 'rectangulo :ancho a :alto (read)))))
  (format t "area=~D~%" (area f)))
""", """
**Lo que esta clase enseña en Common Lisp.** Fíjate en algo que rompe la intuición de quien viene de
Java o C++: **`cuadrado` y `rectangulo` no comparten ninguna superclase**. No hay `figura`, no hay
interfaz y no hay jerarquía.

Lo único que las une es que **existe una función genérica `area` con un método para cada una**.

```lisp
(defgeneric area (f))
(defmethod area ((f cuadrado)) ...)
(defmethod area ((f rectangulo)) ...)
```

En CLOS, **la función genérica ES la interfaz**, y las clases no la "implementan": simplemente hay un
método que las cubre. Y como los métodos se definen fuera de las clases (clase 110), **se puede añadir
`area` a una clase ajena**, incluidas las del sistema:

```lisp
(defmethod area ((f integer)) f)       ; hacer que los enteros cumplan la interfaz
```

Eso es exactamente lo que en Rust son las implementaciones de *trait* para tipos externos, y en Lisp
está desde 1988.

Common Lisp no tiene interfaces declaradas, y por tanto **no comprueba que una clase implemente todo
lo necesario**. La comprobación llega al llamar, con un error claro:

```text
There is no applicable method for the generic function AREA when called with (#<COSA>).
```

Y hay dos mecanismos que se acercan a lo que otros lenguajes declaran:

```lisp
(defgeneric area (f)
  (:method (f) (error "~S no tiene área" f))       ; método por DEFECTO
  (:documentation "Superficie de una figura."))

(defclass mixin-serializable () ())                 ; herencia MÚLTIPLE como mixin
(defclass cuadrado (figura mixin-serializable) ())
```

La herencia múltiple de CLOS con linealización C3 (clase 111) hace innecesarias las interfaces en la
práctica: **un mixin es una clase sin estado propio que aporta métodos**, y componer varios es lo
normal.

La diferencia con las interfaces de Java es la del cierre de esta clase: **aquí nadie comprueba nada
hasta la llamada**. A cambio, extender tipos ajenos y componer comportamiento no requiere permiso de
quien los escribió.
"""),
        "tcl": ("""
oo::class create Figura {
    method area {} { error "metodo abstracto" }
}

oo::class create Cuadrado {
    superclass Figura
    variable lado
    constructor {l} { set lado $l }
    method area {} { return [expr {$lado * $lado}] }
}

oo::class create Rectangulo {
    superclass Figura
    variable ancho alto
    constructor {a b} { set ancho $a; set alto $b }
    method area {} { return [expr {$ancho * $alto}] }
}

gets stdin linea
set partes [split [string trim $linea]]

if {[lindex $partes 0] eq "cuadrado"} {
    set f [Cuadrado new [lindex $partes 1]]
} else {
    set f [Rectangulo new [lindex $partes 1] [lindex $partes 2]]
}

puts "area=[$f area]"
""", """
**Lo que esta clase enseña en Tcl.** **TclOO no tiene interfaces ni clases abstractas declaradas**, y
la forma idiomática es la de este programa: **una superclase cuyo método lanza un error**.

Es la misma solución que `subclassResponsibility` de Smalltalk (clase 111), y por la misma razón: en
un lenguaje sin tipos declarados, **no hay nada que comprobar antes de llamar**.

Lo que sí ofrece Tcl es la forma de **preguntar** antes de llamar:

```tcl
if {"area" in [info object methods $f -all]} { ... }
[info object class $f]
[info object isa typeof $f Figura]        ;# ¿es de esta clase o descendiente?
[info object isa mixin $f Registrable]     ;# ¿tiene este mixin?
```

**`info object`** es la introspección de TclOO, y `isa typeof` es el `instanceof` del lenguaje. Con
`info object methods ... -all` se obtiene la lista completa de métodos, incluidos los heredados y los
de los mixins.

Y la respuesta idiomática de Tcl al problema de esta clase no son las interfaces: **son los mixins**
de la clase 111.

```tcl
oo::class create Areable {
    method describir {} { return "area: [my area]" }
}

oo::define Cuadrado mixin Areable
```

Un mixin **aporta comportamiento y da por supuesto que el objeto responde a `my area`**. Es
exactamente lo que en Perl es un rol con `requires` y en Rust un *trait* con métodos por defecto —
sin la parte del `requires`, que en Tcl no se puede expresar.

`my` merece una nota: **es el comando que envía un mensaje al propio objeto** dentro de un método,
incluidos los privados. Es el `self` implícito de otros lenguajes convertido en comando, y sin él no
se podrían llamar los métodos propios.

La conclusión encaja con el cierre: **Tcl elige la flexibilidad total y paga con la comprobación
tardía**. Un objeto que no responda a `area` falla al llamarlo, no al construirlo.
"""),
        "perl": ("""
use strict;
use warnings;

package Cuadrado;
sub new  { my ($c, $l) = @_; return bless { lado => $l }, $c }
sub area { return $_[0]{lado} ** 2 }

package Rectangulo;
sub new  { my ($c, $a, $b) = @_; return bless { ancho => $a, alto => $b }, $c }
sub area { return $_[0]{ancho} * $_[0]{alto} }

package main;

my $linea = <STDIN>;
chomp $linea;
my ($tipo, @args) = split ' ', $linea;

my $f = $tipo eq 'cuadrado'
    ? Cuadrado->new($args[0])
    : Rectangulo->new(@args);

print "area=", $f->area, "\\n";
""", """
**Lo que esta clase enseña en Perl.** Como en Lisp y en Tcl, **las dos clases no comparten nada**: no
hay superclase, no hay interfaz y no hay declaración de contrato. Funciona porque las dos responden a
`area`.

Perl da la herramienta para preguntar:

```perl
$f->can('area')            # ¿existe el método? Devuelve la REFERENCIA o undef
$f->isa('Figura')          # ¿es de esta clase o descendiente?
$f->DOES('Sonoro')          # ¿cumple este ROL? (Perl 5.10)
ref($f)                      # el nombre de la clase
```

**`can` no devuelve un booleano: devuelve la referencia a la subrutina**, así que se puede usar
directamente:

```perl
if (my $m = $f->can('area')) { print $m->($f) }
```

Y **`DOES`** es la que interesa en esta clase. Se introdujo en Perl 5.10 con una intención explícita:
separar **"desciende de"** de **"cumple el contrato de"**. Por defecto hace lo mismo que `isa`, y una
clase puede redefinirlo para declarar que cumple un rol sin heredar de nada.

La solución completa son los **roles** de `Moose` y `Moo`, ya presentados en la clase 111 y que aquí
están en su terreno:

```perl
package Figura;
use Moose::Role;
requires 'area';                    # EXIGE que quien lo use implemente area

package Cuadrado;
use Moose;
with 'Figura';                       # error EN TIEMPO DE COMPOSICIÓN si falta area
has lado => (is => 'ro', isa => 'Int', required => 1);
sub area { $_[0]->lado ** 2 }
```

**`requires` es lo que a Tcl le falta** y lo que Java tiene con las interfaces: la comprobación ocurre
**al componer el rol**, no al llamar al método. Si `Cuadrado` no define `area`, el `with 'Figura'`
falla al cargar el módulo.

Y un rol puede además **aportar métodos**, no solo exigirlos, con lo que es a la vez interfaz y mixin
— exactamente el diseño de los *traits* de Rust y de Scala, y del artículo original de la comunidad
Smalltalk (clase 111).
"""),
        "cpp": ("""
#include <iostream>
#include <memory>
#include <string>

struct Figura {
    virtual ~Figura() = default;
    virtual int area() const = 0;          // = 0 : método PURO
};

struct Cuadrado : Figura {
    int lado;
    explicit Cuadrado(int l) : lado(l) {}
    int area() const override { return lado * lado; }
};

struct Rectangulo : Figura {
    int ancho, alto;
    Rectangulo(int a, int b) : ancho(a), alto(b) {}
    int area() const override { return ancho * alto; }
};

int main() {
    std::string tipo;
    if (!(std::cin >> tipo)) return 1;

    std::unique_ptr<Figura> f;
    if (tipo == "cuadrado") {
        int l{};
        std::cin >> l;
        f = std::make_unique<Cuadrado>(l);
    } else {
        int a{}, b{};
        std::cin >> a >> b;
        f = std::make_unique<Rectangulo>(a, b);
    }

    std::cout << "area=" << f->area() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** **C++ no tiene interfaces**, y no las necesita: una **clase
abstracta pura** —solo métodos virtuales puros, sin estado— es exactamente una interfaz, y la herencia
múltiple permite implementar varias.

```cpp
struct Dibujable  { virtual void dibujar() const = 0; virtual ~Dibujable() = default; };
struct Serializable { virtual std::string serializar() const = 0; virtual ~Serializable() = default; };

class Figura : public Dibujable, public Serializable { ... };
```

Es el mismo resultado que Java, conseguido sin añadir una construcción nueva al lenguaje. La
diferencia es que **C++ no impide que una "interfaz" tenga estado**, así que la disciplina la pone el
programador.

Y esta clase es el sitio para la alternativa que en C++ moderno suele ser mejor: **los conceptos**.

```cpp
#include <concepts>

template <typename T>
concept Figura = requires(const T& f) {
    { f.area() } -> std::convertible_to<int>;
};

template <Figura F>
void mostrar(const F& f) { std::cout << f.area(); }
```

Un **concepto** (C++20) es un contrato **comprobado en compilación** sobre cualquier tipo que tenga
las operaciones requeridas, **sin herencia, sin `vtable` y sin coste en ejecución**. `Cuadrado` no
tiene que heredar de nada ni saber que `Figura` existe.

Eso es *duck typing* con comprobación estática, y es la misma idea que los *traits* de Rust: **el
contrato se comprueba, la jerarquía no hace falta**.

La diferencia práctica con la clase abstracta es la del cierre de esta clase, y decide cuál usar:

| | Clase abstracta | Concepto |
|---|---|---|
| Comprobación | compilación | compilación |
| Coste | indirección por llamada | **ninguno** |
| Colección heterogénea | **sí** | no |
| Requiere modificar el tipo | **sí** | no |
| Errores de compilación | claros | mejoraron mucho con C++20 |

**La regla: concepto si el tipo se conoce al compilar; clase abstracta si necesitas meter cosas
distintas en el mismo `vector`.** Antes de C++20, esa segunda columna existía igual con plantillas,
pero los errores eran las páginas ilegibles que hicieron famosas a las plantillas (clase 098).
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi IFACE;
  tipo char(12) const;
  a    int(10)  const;
  b    int(10)  const options(*nopass);
end-pi;

dcl-s superf int(20) inz(0);
dcl-s alto   int(10) inz(0);

if %parms() >= 3;
  alto = b;
endif;

select;
  when %trim(tipo) = 'cuadrado';    superf = a * a;
  when %trim(tipo) = 'rectangulo';  superf = a * alto;
  other;                            superf = 0;
endsl;

dsply ('area=' + %char(superf));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG no tiene interfaces ni clases abstractas, y lo que sí tiene
—y es lo más cercano a un contrato comprobado— es **el prototipo**.

```rpgle
dcl-pr calcularArea int(20) extproc('CALC_AREA');
  figura likeds(datosFigura) const;
end-pr;
```

Un `dcl-pr` **declara la firma de un procedimiento sin implementarlo**, y el compilador comprueba
todas las llamadas contra él. Si el procedimiento real tiene otra firma, **el enlazador falla**.

Es exactamente un fichero de cabecera, y su uso idiomático lo convierte casi en una interfaz: los
prototipos van en un miembro compartido con `/copy`, y **varios módulos pueden implementar la misma
firma** — el que se enlace decide cuál se usa.

```rpgle
/copy qrpglesrc,prototipos          // el "contrato"
ctl-opt bnddir('MIAPP/GEOMETRIA');   // dónde buscar la implementación
```

Eso es **inyección de dependencias resuelta en el enlazado**, y es un patrón real en IBM i: se compila
contra el mismo prototipo y se enlaza con un programa de servicio u otro según el entorno —producción,
pruebas, simulación—.

Y hay una pieza de este programa que merece destacarse porque no se ha visto antes:

```rpgle
b int(10) const options(*nopass);
...
if %parms() >= 3;
```

**`options(*nopass)`** declara un parámetro **opcional**, y `%parms()` dice cuántos llegaron
realmente. Es lo que en la clase 109 se mencionó como la clave de la compatibilidad de las APIs de la
plataforma: **se añaden parámetros al final y los programas antiguos siguen funcionando**.

Las otras opciones completan el juego: `*omit` permite pasar `*OMIT` explícitamente en una posición
intermedia, y `*varsize` acepta un parámetro más corto de lo declarado.

Es un sistema de contratos muy elaborado para un lenguaje sin objetos, y está orientado a lo que a esa
plataforma le importa: **que lo compilado hace treinta años siga enlazando**.
"""),
        "pli": ("""
 iface: procedure options(main);

    declare linea  char(80) varying;
    declare tipo   char(20) varying;
    declare resto  char(80) varying;
    declare corte  fixed binary(31);
    declare (a, b) fixed binary(31) initial(0);
    declare superf fixed binary(31) initial(0);

    get edit (linea) (a(80));
    linea = trim(linea);

    corte = index(linea, ' ');
    tipo  = substr(linea, 1, corte - 1);
    resto = trim(substr(linea, corte + 1));

    corte = index(resto, ' ');
    if corte = 0 then a = resto;
    else do;
       a = substr(resto, 1, corte - 1);
       b = substr(resto, corte + 1);
    end;

    select (tipo);
       when ('cuadrado')   superf = a * a;
       when ('rectangulo') superf = a * b;
       otherwise           superf = 0;
    end;

    put skip list ('area=' || trim(char(superf)));

 end iface;
""", """
**Lo que esta clase enseña en PL/I.** PL/I no tiene interfaces ni objetos, y lo más cercano a un
contrato es la **declaración `entry`**, que ya apareció en la clase 085:

```pli
 declare calcular_area entry (fixed binary(31), fixed binary(31))
                       returns (fixed binary(31)) external;
```

Eso declara **la firma de un procedimiento externo**, y el compilador comprueba las llamadas contra
ella. Es el prototipo de RPG y el fichero de cabecera de C, con la misma limitación grave que se
señaló en la clase 088: **el enlazador empareja por nombre y no comprueba que la declaración coincida
con la definición real**.

Si un programa declara `entry (fixed binary(31))` y el procedimiento real espera `fixed decimal(15,2)`,
**enlaza igualmente** y el resultado es corrupción de datos. Esa es exactamente la carencia que Ada
resolvió en 1983 con la comprobación entre unidades de compilación, y la razón por la que el paquete
de Ada se considera el antepasado del módulo moderno.

Lo que PL/I sí tiene, y aquí encaja, es **`generic`** (clase 109):

```pli
 declare area generic (area_cuadrado when (fixed binary),
                       area_real     when (float));
```

Un nombre que **despacha a un procedimiento u otro según el tipo del argumento**, resuelto en
compilación. Es sobrecarga, y en términos de esta clase es lo más parecido a "varios tipos que
cumplen el mismo contrato" que ofrece el lenguaje — con la diferencia esencial de que **el despacho es
estático y por tipo declarado**, no dinámico.

Y merece cerrar señalando lo que esta clase deja claro sobre PL/I: **tenía la declaración de firma, la
sobrecarga y los punteros a procedimiento, y le faltó el pegamento**. Con esos tres ingredientes, C++
construyó clases abstractas y Ada construyó interfaces.

La diferencia entre un lenguaje con las piezas y uno con la característica vuelve a ser la misma de la
clase 111: **quién comprueba, y cuándo**.
"""),
        "mumps": ("""
IFACE ; Interfaces y clases abstractas -- clase 112
 read linea
 set tipo = $piece(linea, " ", 1)
 set a = $piece(linea, " ", 2)
 set b = $piece(linea, " ", 3)
 set superf = 0
 ; "interfaz": la etiqueta AREA<tipo> debe existir en esta rutina
 if $text(@("area"_tipo_"^IFACE"))'="" set superf = $$@("area"_tipo_"^IFACE")(a, b)
 write "area=", superf, !
 quit
 ;
areacuadrado(x, y)   quit x * x
arearectangulo(x, y) quit x * y
""", """
**Lo que esta clase enseña en M.** M no tiene interfaces, clases ni tipos, y este programa muestra su
equivalente funcional: **una convención de nombres comprobada con `$text`**.

```mumps
 if $text(@("area"_tipo_"^IFACE"))'=""
```

El "contrato" es: **para cada tipo de figura debe existir una etiqueta llamada `area<tipo>`**. `$text`
(clase 111) comprueba que existe antes de llamarla por indirección.

Es una interfaz implementada con **nombres y una comprobación en ejecución**, y es exactamente lo que
hacen los sistemas grandes de M. En **VistA** ese patrón está institucionalizado con un nombre propio:
**los puntos de integración** o *IA* (*Integration Agreements*).

Un IA es un **acuerdo documentado y numerado** entre paquetes: el paquete de Farmacia declara que
ofrece la entrada `DOSIS^PSSDOSE(x)` con unos parámetros y un valor de retorno, y otros paquetes
pueden llamarla. Cambiarla exige un proceso formal.

Merece detenerse en lo que eso significa: **el contrato existe, está escrito, está numerado y hay una
oficina que lo administra — y no está en el lenguaje**. La comprobación la hacen personas y
procedimientos, no un compilador.

Es la conclusión más honesta que se puede sacar de esta clase entera: **la interfaz es una idea que
existe con o sin soporte del lenguaje**. Lo que aporta el lenguaje es **cuándo se detecta el
incumplimiento** — al compilar, al ejecutar, o en una reunión.

Y en VistA, con cuarenta años y decenas de paquetes desarrollados por hospitales distintos, ese
sistema documental **ha funcionado**. Con un coste: hay miles de IA, su base de datos es en sí misma
una aplicación, y romper uno sin darse cuenta es un problema recurrente.

Las implementaciones modernas sí lo resuelven en el lenguaje: **IRIS tiene clases abstractas e
interfaces** con comprobación al compilar.
"""),
        "smalltalk": ("""
| partes tipo a superf |

partes := stdin nextLine substrings.
tipo := partes first.
a := (partes at: 2) asNumber.

"Sin interfaz declarada: si responde al mensaje, sirve"
superf := tipo = 'cuadrado'
    ifTrue: [ a * a ]
    ifFalse: [ a * (partes at: 3) asNumber ].

Transcript show: 'area=', superf printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene interfaces, ni las ha tenido nunca, ni
las considera necesarias.** La versión con clases sería:

```smalltalk
Object subclass: #Figura.
Figura >> area   ^self subclassResponsibility

Figura subclass: #Cuadrado.
Cuadrado >> area   ^lado * lado
```

Y ni siquiera hace falta la superclase: **si un objeto responde a `area`, sirve**. La comprobación
está en la llamada, y el mensaje de error es claro:

```text
MessageNotUnderstood: Cosa>>#area
```

Lo que Smalltalk aportó a esta clase es lo que después se convirtió en un paradigma: **los *traits***.

El artículo *Traits: Composable Units of Behaviour* (Schärli, Ducasse, Nierstrasz y Black, 2003) se
escribió sobre Smalltalk, y su motivación era exactamente el problema de esta página: **la herencia
simple no basta y la herencia múltiple es peor**.

```smalltalk
Trait named: #TAreable
    uses: {}
    package: 'Ejemplo'.

TAreable >> describir   ^'área: ', self area printString
```

Un *trait* es un conjunto de métodos **sin estado**, que se compone en una clase. Y sus tres reglas de
diseño son lo importante:

1. **La clase tiene prioridad sobre el trait.** Si la clase define el método, gana.
2. **Los conflictos entre traits son ERRORES**, no se resuelven en silencio por orden.
3. **Se pueden resolver explícitamente**, excluyendo un método o dándole un alias.

Esa segunda regla es la diferencia esencial con la herencia múltiple y con los mixins: **componer no
puede sorprenderte**. Si dos traits aportan `imprimir`, hay que decir cuál se quiere.

De ahí salieron **los traits de PHP (2012), los de Scala, los de Rust y los roles de Perl** — todos
citan ese artículo. Y Rust fue más lejos: **sus traits sí declaran el contrato y se comprueban al
compilar**, uniendo las dos mitades que esta clase separa.

Es un caso limpio de investigación académica sobre un lenguaje de 1980 que acabó definiendo cómo se
compone comportamiento en los lenguajes de 2015.
"""),
    },
)
