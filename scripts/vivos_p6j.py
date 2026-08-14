# -*- coding: utf-8 -*-
"""Parte 6, lote J — clase 100. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 100 — Enumeraciones y tipos algebraicos
# ---------------------------------------------------------------------------
SPECS["100"] = dict(
    gancho="""
Una figura que puede ser dos cosas distintas, cada una con sus propios campos. Es el tipo suma, y aquí
hay un hallazgo que descoloca: **Ada tiene el registro variante con comprobación desde 1983 y Pascal
desde 1970**, mientras que C++ no tuvo `std::variant` hasta 2017. La diferencia entre los dos es
exactamente la que separa un tipo algebraico de una `union` de C: **quién comprueba que estás leyendo
la variante correcta**.
""",
    porque="""
Aquí el concepto es el **tipo suma con discriminante**, y estos lenguajes lo enseñan porque tienen las
tres versiones. **Ada** lo hace bien: el discriminante forma parte del tipo y acceder a la variante
equivocada **lanza `Constraint_Error`**. **Pascal** lo hace a medias: la sintaxis es casi idéntica y
**no comprueba nada**, con lo que el registro variante fue durante décadas la forma idiomática de
reinterpretar bytes. Y **COBOL, Fortran, RPG, PL/I y M** no lo tienen: usan una marca de tipo y una
redefinición, que es lo mismo sin red.

Y las **enumeraciones** cuentan otra historia: Ada y Pascal las tienen desde el principio como tipos
propios; **Fortran no tiene enumeraciones de verdad ni hoy**.
""",
    cierre="""
Lo transferible: **una unión sin discriminante comprobado es una bomba de relojería, y el discriminante
por sí solo no basta**. Lo que hace seguro un tipo algebraico es que **el lenguaje impida leer la
variante equivocada**, no que el programador recuerde mirar la etiqueta antes. Ada lo comprueba en
ejecución, Rust y ML lo comprueban en compilación obligando a cubrir todos los casos, y C, Pascal y
PL/I no lo comprueban en absoluto. Cuando escribas un `switch` sobre una etiqueta de tipo, la pregunta
importante es qué pasa si mañana alguien añade una variante — y la respuesta buena es "no compila".
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. FIGURA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  T0      PIC X(20).
01  T1      PIC X(20).
01  T2      PIC X(20).
01  A       PIC S9(9)  COMP-3 VALUE 0.
01  B       PIC S9(9)  COMP-3 VALUE 0.
01  AREA    PIC S9(18) COMP-3 VALUE 0.
01  ED-A    PIC -(17)9.
01  CLASE   PIC X(12).
    88  ES-CUADRADO    VALUE "cuadrado".
    88  ES-RECTANGULO  VALUE "rectangulo".

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO T0 T1 T2
    MOVE T0 TO CLASE

    COMPUTE A = FUNCTION NUMVAL(T1)
    IF T2 NOT = SPACES
        COMPUTE B = FUNCTION NUMVAL(T2)
    END-IF

    EVALUATE TRUE
        WHEN ES-CUADRADO    COMPUTE AREA = A * A
        WHEN ES-RECTANGULO  COMPUTE AREA = A * B
        WHEN OTHER          MOVE 0 TO AREA
    END-EVALUATE

    MOVE AREA TO ED-A
    DISPLAY "area=" FUNCTION TRIM(ED-A)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL **no tiene enumeraciones ni tipos algebraicos**, y tiene
dos cosas que juntas hacen la mitad del trabajo.

**El nivel 88** es la enumeración de COBOL, y ya apareció en la clase 092:

```cobol
01  CLASE  PIC X(12).
    88  ES-CUADRADO    VALUE "cuadrado".
    88  ES-RECTANGULO  VALUE "rectangulo".
```

Da nombre a valores concretos y se usa como booleano —`IF ES-CUADRADO`— lo que hace el código
legible sin literales sueltos. Y `SET ES-CUADRADO TO TRUE` asigna el valor.

Lo que **no** hace es restringir: `CLASE` sigue siendo un `X(12)` que puede contener cualquier cosa.
No hay comprobación de que el valor sea uno de los declarados, y por eso el `WHEN OTHER` del
`EVALUATE` es obligatorio en código serio.

**Y `REDEFINES`** es la unión, sin ninguna comprobación:

```cobol
01  REG-FIGURA.
    05  TIPO-FIG  PIC X.
        88  ES-CUAD  VALUE "C".
        88  ES-RECT  VALUE "R".
    05  DATOS-CUAD.
        10  LADO   PIC 9(9).
    05  DATOS-RECT REDEFINES DATOS-CUAD.
        10  ANCHO  PIC 9(5).
        10  ALTO   PIC 9(4).
```

Ese es el registro variante de COBOL: una etiqueta, y dos vistas de los mismos bytes. **Nada impide
leer `ANCHO` cuando `TIPO-FIG` vale `"C"`**, y el resultado son las cifras de otro campo.

Es exactamente la `union` de C, y con el mismo riesgo. La disciplina que lo sostiene es de proceso:
**el copybook define la estructura, y hay una norma de que ningún programa lea la variante sin
comprobar la etiqueta primero**.

Y hay un detalle que hace esto menos temerario de lo que suena en contexto: **el registro viene de un
fichero**, donde la etiqueta y los datos llegan juntos y consistentes desde el sistema que los
escribió. El problema no es leer la variante equivocada por accidente; es que dos programas discrepen
sobre qué significa la etiqueta — que es un problema de gestión de copybooks (clase 088).
"""),
        "fortran": ("""
program figura
   implicit none

   integer, parameter :: CUADRADO = 1, RECTANGULO = 2

   character(len=200) :: linea
   character(len=20)  :: tipo
   integer :: clase, a, b, area

   read(*, '(A)') linea
   read(linea, *) tipo

   b = 0
   if (trim(tipo) == 'cuadrado') then
      clase = CUADRADO
      read(linea, *) tipo, a
   else
      clase = RECTANGULO
      read(linea, *) tipo, a, b
   end if

   select case (clase)
   case (CUADRADO)
      area = a * a
   case (RECTANGULO)
      area = a * b
   case default
      area = 0
   end select

   write(*, '(A,I0)') 'area=', area
end program figura
""", """
**Lo que esta clase enseña en Fortran.** Aquí hay una carencia que conviene decir sin adornos:
**Fortran no tiene enumeraciones de verdad, ni siquiera en 2026**.

Lo que hay es la constante con nombre:

```fortran
integer, parameter :: CUADRADO = 1, RECTANGULO = 2
```

Que es lo mismo que un `#define` de C: **no crea un tipo**, así que `clase = 47` compila sin queja y
nada impide pasar un código de figura donde se espera un código de error.

Fortran 2003 añadió `enum, bind(c)`, y su propósito es más estrecho de lo que su nombre sugiere:

```fortran
enum, bind(c)
   enumerator :: rojo = 1, verde, azul
end enum
```

**Existe para interoperar con los `enum` de C**, no para dar seguridad de tipos en Fortran: los
valores siguen siendo enteros y no hay tipo nuevo. Es una carencia reconocida, y hay propuestas para
Fortran 202y con enumeraciones tipadas de verdad.

Tampoco hay tipos suma. El idioma en código real es **un tipo derivado con una etiqueta y todos los
campos**, desperdiciando memoria:

```fortran
type :: forma
   integer :: clase
   integer :: lado, ancho, alto     ! sobran dos, siempre
end type
```

O, desde Fortran 2003, **polimorfismo con `class` y `select type`**, que es la forma correcta:

```fortran
type, abstract :: forma
end type
type, extends(forma) :: cuadrado
   integer :: lado
end type

select type (f)
type is (cuadrado)
   area = f%lado ** 2
type is (rectangulo)
   area = f%ancho * f%alto
class default
   error stop 'figura desconocida'
end select
```

`select type` es el equivalente del emparejamiento de patrones sobre tipos, y **el compilador no
obliga a cubrir todos los casos** — de ahí que `class default` con `error stop` sea la práctica
recomendada. Es la mitad del trabajo que hacen Rust y ML, y es lo que hay.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Figura is
   type Clase is (Cuadrado, Rectangulo);

   type Forma (C : Clase) is record       --  DISCRIMINANTE: parte del tipo
      case C is
         when Cuadrado   => Lado : Integer;
         when Rectangulo => Ancho, Alto : Integer;
      end case;
   end record;

   function Area (F : Forma) return Integer is
   begin
      case F.C is
         when Cuadrado   => return F.Lado * F.Lado;
         when Rectangulo => return F.Ancho * F.Alto;
      end case;
   end Area;

   Linea  : String (1 .. 200);
   Ultimo : Natural;
   Corte  : Natural := 0;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         Corte := I;
         exit;
      end if;
   end loop;

   Put ("area=");

   if Linea (1 .. Corte - 1) = "cuadrado" then
      declare
         Lado : Integer;
         Fin  : Positive;
      begin
         Get (Linea (Corte + 1 .. Ultimo), Lado, Fin);
         Put (Area (Forma'(C => Cuadrado, Lado => Lado)), Width => 1);
      end;
   else
      declare
         Ancho, Alto : Integer;
         Fin : Positive;
         Pos : Integer := Corte + 1;
      begin
         Get (Linea (Pos .. Ultimo), Ancho, Fin);
         Pos := Fin + 1;
         Get (Linea (Pos .. Ultimo), Alto, Fin);
         Put (Area (Forma'(C => Rectangulo, Ancho => Ancho, Alto => Alto)),
              Width => 1);
      end;
   end if;

   New_Line;
end Figura;
""", """
**Lo que esta clase enseña en Ada.** Este es uno de los sitios donde Ada de 1983 sigue por delante de
lenguajes de 2017, y merece verse con detalle.

**El discriminante forma parte del tipo:**

```ada
type Forma (C : Clase) is record
   case C is
      when Cuadrado   => Lado : Integer;
      when Rectangulo => Ancho, Alto : Integer;
   end case;
end record;
```

Y con eso el compilador y el runtime garantizan **cuatro** cosas que ni C ni Pascal garantizan:

1. **Acceder a la variante equivocada lanza `Constraint_Error`.** `F.Lado` sobre un rectángulo es un
   error detectado, no basura.
2. **El discriminante de un objeto con valor inicial es inmutable.** `F : Forma (Cuadrado);` es un
   cuadrado para siempre; no se puede convertir en rectángulo asignándole el campo.
3. **El agregado debe cubrir exactamente los campos de su variante.** No se puede construir un valor
   incoherente.
4. **El `case` sobre el discriminante debe cubrir todos los valores** o llevar `others`. Añadir
   `Circulo` a `Clase` **rompe la compilación** de todos los `case` incompletos.

Ese cuarto punto es la exhaustividad que hoy se asocia a Rust y a los lenguajes ML, y en Ada aplica a
**cualquier `case` sobre una enumeración**.

Y las enumeraciones de Ada son tipos completos, no enteros con nombre:

```ada
type Clase is (Cuadrado, Rectangulo);
Clase'First, Clase'Succ (X), Clase'Pos (X), Clase'Image (X), Clase'Value ("CUADRADO")
for Clase use (Cuadrado => 1, Rectangulo => 7);   --  representación explícita
```

`'Image` y `'Value` convierten a texto y de vuelta **sin escribir ninguna tabla**, que es lo que en
C++ sigue exigiendo un mapa a mano o una biblioteca de reflexión.

El precio es la verbosidad, visible en este programa. Y el beneficio es que un tipo con variantes en
Ada **no puede leerse mal**, ni por accidente ni por descuido.
"""),
        "pascal": ("""
program Figura;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TClase = (Cuadrado, Rectangulo);

  TForma = record
    case Clase: TClase of              { REGISTRO VARIANTE, sin comprobación }
      Cuadrado:   (Lado: Integer);
      Rectangulo: (Ancho, Alto: Integer);
  end;

function Area(const F: TForma): Integer;
begin
  case F.Clase of
    Cuadrado:   Result := F.Lado * F.Lado;
    Rectangulo: Result := F.Ancho * F.Alto;
  else
    Result := 0;
  end;
end;

var
  F: TForma;
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
    F.Clase := Cuadrado;
    F.Lado := StrToInt(Resto);
  end
  else
  begin
    F.Clase := Rectangulo;
    P2 := Pos(' ', Resto);
    F.Ancho := StrToInt(Copy(Resto, 1, P2 - 1));
    F.Alto := StrToInt(Trim(Copy(Resto, P2 + 1, Length(Resto))));
  end;

  WriteLn('area=', IntToStr(Area(F)));
end.
""", """
**Lo que esta clase enseña en Pascal.** El registro variante de Pascal es **de 1970 y es el origen del
de Ada**, con una sintaxis casi idéntica y una diferencia decisiva: **Pascal no comprueba nada**.

```pascal
F.Clase := Cuadrado;
F.Lado := 5;
WriteLn(F.Ancho);     { compila, se ejecuta, devuelve los bytes de Lado }
```

Wirth lo diseñó como tipo suma —esa era la intención— y la implementación no podía comprobarlo sin
coste, así que quedó como una unión con etiqueta **por convención**. El informe original de Pascal
reconoce el agujero.

Y eso tuvo una consecuencia que define décadas de código Pascal: **el registro variante se convirtió
en la forma idiomática de reinterpretar bytes**, el `REDEFINES` de COBOL.

```pascal
type
  TConversor = record
    case Boolean of
      True:  (Entero: LongInt);
      False: (Bytes: array[0..3] of Byte);
  end;
```

Escribir en `Entero` y leer en `Bytes` es la manera clásica de ver los bytes de un número en Pascal, y
aparece en código de serialización, de red y de gráficos de los años ochenta y noventa. Es un abuso
declarado de la característica, y funcionaba.

Las **enumeraciones**, en cambio, Pascal las hizo bien y fue el primero:

```pascal
type TDia = (Lun, Mar, Mie);
Ord(Mie)     Succ(Lun)     Pred(Mie)     Low(TDia)     High(TDia)
for D := Low(TDia) to High(TDia) do ...
```

Un tipo propio, ordenado, recorrible y utilizable como índice de arreglo y como base de un `set`
(clase 094). De ahí lo tomaron Ada, C —que lo degradó a enteros con nombre— y todos los demás.

Free Pascal moderno añade `{$SCOPEDENUMS ON}`, que obliga a cualificar —`TDia.Lun`— y evita que los
identificadores contaminen el ámbito. Es el `enum class` de C++11, con la misma motivación.
"""),
        "lisp": ("""
(let* ((tipo (symbol-name (read)))
       (a (read))
       (area (if (string-equal tipo "cuadrado")
                 (* a a)
                 (* a (read)))))
  (format t "area=~D~%" area))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp **no tiene enumeraciones ni tipos algebraicos**, y
tiene algo que cubre buena parte de su uso: **los símbolos**.

Un símbolo es un objeto internado y único (clase 093), así que comparar dos es comparar punteros. Con
eso, `'cuadrado` **es** un valor de enumeración: legible, imprimible, comparable en tiempo constante y
sin declarar nada.

```lisp
(case tipo
  (cuadrado   (* lado lado))
  (rectangulo (* ancho alto))
  (t          (error "figura desconocida")))
```

Y para declarar el conjunto de valores válidos, Common Lisp tiene especificadores de tipo:

```lisp
(deftype clase () '(member cuadrado rectangulo))
(declare (type clase c))
```

Con `(optimize (safety 3))`, SBCL **comprueba eso en ejecución**; y su compilador va más allá:
**detecta en compilación** un `case` que no cubre todos los miembros de un tipo declarado, y avisa.
No es exhaustividad obligatoria como en ML, pero se acerca más de lo que el lenguaje promete.

Para tipos suma con datos, el idioma es una **lista etiquetada** o una jerarquía CLOS:

```lisp
(list :cuadrado 5)                          ; lista etiquetada
(list :rectangulo 3 4)

(defclass forma () ())                       ; o con CLOS
(defclass cuadrado (forma) ((lado :initarg :lado)))
(defmethod area ((f cuadrado)) ...)
(defmethod area ((f rectangulo)) ...)
```

La versión CLOS es interesante porque invierte el problema: en lugar de un `case` que hay que
actualizar al añadir una variante, **cada variante trae su método**. Añadir `Circulo` es escribir una
clase y un método, **sin tocar nada existente** — ni siquiera recompilar.

Ese es el viejo dilema del *expression problem*: el tipo suma con `case` facilita añadir operaciones y
dificulta añadir variantes; la jerarquía de clases hace lo contrario. Lisp es de los pocos lenguajes
donde las dos opciones son igual de idiomáticas, y CLOS con **despacho múltiple** resuelve además el
caso en que la operación depende de dos tipos a la vez —`(defmethod interseca ((a circulo) (b
rectangulo)))`—, que es donde ambas soluciones clásicas fallan.
"""),
        "tcl": ("""
gets stdin linea
set partes [split [string trim $linea]]
set tipo [lindex $partes 0]

switch -exact -- $tipo {
    cuadrado   { set area [expr {[lindex $partes 1] ** 2}] }
    rectangulo { set area [expr {[lindex $partes 1] * [lindex $partes 2]}] }
    default    { set area 0 }
}

puts "area=$area"
""", """
**Lo que esta clase enseña en Tcl.** **Tcl no tiene tipos, así que no tiene enumeraciones ni tipos
suma.** Una etiqueta es una cadena, y el despacho es un `switch`.

Y `switch` en Tcl es más rico de lo que parece, porque **elige el modo de comparación**:

```tcl
switch -exact -- $x { ... }      ;# comparación literal
switch -glob  -- $x { *.txt {...} }    ;# con comodines
switch -regexp -- $x { {^[0-9]+$} {...} }   ;# con expresiones regulares
switch -- $x { a - b { ... } }    ;# "a - b": dos etiquetas, un cuerpo
```

El **`--`** separa las opciones del valor, y es obligatorio en código serio: sin él, un valor que
empiece por guion se interpretaría como opción. Es la misma convención que en las órdenes de Unix, y
es un buen ejemplo de que en Tcl **todo es una llamada a comando**, con las mismas reglas.

Y `-regexp` como modo de `switch` es potente: permite despachar sobre la forma del dato, no sobre un
valor exacto — un emparejamiento de patrones textual.

Para representar un tipo suma con datos, lo idiomático es una **lista cuyo primer elemento es la
etiqueta**, exactamente como en Lisp:

```tcl
set f [list cuadrado 5]
set f [list rectangulo 3 4]
lassign $f tipo a b
```

Otra vez la misma respuesta que Lisp, y por la misma razón: cuando la lista es la estructura universal
del lenguaje, la lista etiquetada es el tipo suma natural.

La contrapartida es la de siempre y conviene decirla: **nada comprueba que la etiqueta sea válida ni
que los datos correspondan**. Un `switch` sin `default` **no falla**: no hace nada y deja `area` sin
definir, y el error aparece dos líneas después con un mensaje de "variable desconocida". De ahí que la
guía práctica en Tcl sea poner siempre `default` con un `error`.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($tipo, @args) = split ' ', $linea;

my $area = $tipo eq 'cuadrado'
    ? $args[0] ** 2
    : $args[0] * $args[1];

print "area=$area\\n";
""", """
**Lo que esta clase enseña en Perl.** **Perl no tiene enumeraciones**, y el idioma es la cadena
literal o el módulo `constant`, que es del núcleo:

```perl
use constant {
    CUADRADO   => 0,
    RECTANGULO => 1,
};
```

`use constant` define subrutinas de aridad cero que el compilador **integra en línea**, así que no
cuestan nada en ejecución. No crean un tipo: son enteros con nombre, con el mismo alcance que un
`#define`.

Y para el tipo suma, el idioma es **un hash con una clave de tipo**:

```perl
my $f = { tipo => 'cuadrado', lado => 5 };
my $g = { tipo => 'rectangulo', ancho => 3, alto => 4 };

my %area = (
    cuadrado   => sub { $_[0]{lado} ** 2 },
    rectangulo => sub { $_[0]{ancho} * $_[0]{alto} },
);
$area{ $f->{tipo} }->($f);
```

Esa **tabla de despacho de la clase 085** es la forma idiomática de Perl para tipos suma, y tiene una
virtud sobre el `if`/`switch`: **añadir una variante es añadir una entrada al hash**, y se puede hacer
desde otro módulo.

Perl 5.10 añadió `given`/`when`, un intento de emparejamiento de patrones con comparación
inteligente:

```perl
use feature 'switch';
given ($tipo) {
    when ('cuadrado')   { ... }
    when ('rectangulo') { ... }
}
```

Y es un caso instructivo: **fue marcado como experimental, generó avisos de deprecación y en Perl 5.42
se ha retirado**. La razón es que su comparación inteligente —el operador `~~`— hacía cosas distintas
según los tipos de los operandos de una forma imposible de predecir al leer el código.

Es un buen ejemplo de que **añadir emparejamiento de patrones a un lenguaje dinámico sin tipos es más
difícil de lo que parece**: sin tipos que discriminar, hay que adivinar la intención, y adivinar mal
es peor que no tener la característica.
"""),
        "cpp": ("""
#include <iostream>
#include <string>
#include <type_traits>
#include <variant>

struct Cuadrado   { int lado; };
struct Rectangulo { int ancho, alto; };

using Forma = std::variant<Cuadrado, Rectangulo>;

int area(const Forma& f) {
    return std::visit([](const auto& x) -> int {
        using T = std::decay_t<decltype(x)>;
        if constexpr (std::is_same_v<T, Cuadrado>) {
            return x.lado * x.lado;
        } else {
            return x.ancho * x.alto;
        }
    }, f);
}

int main() {
    std::string tipo;
    if (!(std::cin >> tipo)) return 1;

    Forma f = Cuadrado{0};
    if (tipo == "cuadrado") {
        int l{};
        std::cin >> l;
        f = Cuadrado{l};
    } else {
        int a{}, b{};
        std::cin >> a >> b;
        f = Rectangulo{a, b};
    }

    std::cout << "area=" << area(f) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ heredó de C la `union` sin discriminante —la forma más
insegura de tipo suma que existe— y **tardó hasta 2017 en tener `std::variant`**, treinta y cuatro
años después de que Ada lo tuviera comprobado.

```cpp
union Mala { int i; float f; };      // NADIE comprueba cuál está activo
std::variant<int, float> Buena;       // el índice activo se guarda y se comprueba
```

`std::variant` guarda **qué alternativa está activa** y `std::get` **lanza `std::bad_variant_access`**
si te equivocas. Es el comportamiento de Ada, en biblioteca en lugar de en el lenguaje.

`std::visit` es la pieza que da exhaustividad: **la lambda debe poder aplicarse a todas las
alternativas o no compila**. Añadir un tipo al `variant` y olvidar su caso es un error de compilación,
que es justo lo que pide el cierre de esta clase.

El `if constexpr` del programa es la selección en tiempo de compilación (C++17): la rama que no
corresponde **ni siquiera se compila** para cada tipo. Sin él, `x.lado` sobre un `Rectangulo` no
compilaría.

Y hay un idioma que conviene conocer, porque es más legible que el `if constexpr`:

```cpp
template <class... Ts> struct sobrecarga : Ts... { using Ts::operator()...; };
template <class... Ts> sobrecarga(Ts...) -> sobrecarga<Ts...>;

std::visit(sobrecarga{
    [](const Cuadrado& c)   { return c.lado * c.lado; },
    [](const Rectangulo& r) { return r.ancho * r.alto; },
}, f);
```

Ese `sobrecarga` —el *overloaded pattern*— compone varias lambdas en un objeto con varios
`operator()`, y consigue algo muy parecido a un `match` de Rust. Es tan común que **C++23 lo incluyó
como `std::visit` con lambdas sobrecargadas** en la práctica, y hay propuestas de emparejamiento de
patrones nativo para C++26.

Sobre enumeraciones, C++11 arregló la herencia de C con **`enum class`**:

```cpp
enum Vieja { rojo, verde };            // se convierte a int SOLA, contamina el ámbito
enum class Nueva { rojo, verde };      // tipo propio, hay que cualificar, sin conversión
```
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi FIGURA;
  entrada char(200) const;
end-pi;

// RPG no tiene enumeraciones: constantes con nombre
dcl-c CUADRADO   'cuadrado';
dcl-c RECTANGULO 'rectangulo';

dcl-s texto varchar(200);
dcl-s tipo  varchar(20);
dcl-s resto varchar(200);
dcl-s corte int(10);
dcl-s a     int(10) inz(0);
dcl-s b     int(10) inz(0);
dcl-s area  int(20) inz(0);

texto = %trimr(entrada);
corte = %scan(' ' : texto);
tipo  = %subst(texto : 1 : corte - 1);
resto = %trim(%subst(texto : corte + 1 : %len(texto) - corte));

corte = %scan(' ' : resto);
if corte = 0;
  a = %int(resto);
else;
  a = %int(%subst(resto : 1 : corte - 1));
  b = %int(%subst(resto : corte + 1 : %len(resto) - corte));
endif;

select;
  when tipo = CUADRADO;    area = a * a;
  when tipo = RECTANGULO;  area = a * b;
  other;                   area = 0;
endsl;

dsply ('area=' + %char(area));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene enumeraciones ni tipos suma**, y usa `dcl-c`
—constantes con nombre— más `select`/`when`, que es exactamente el nivel de COBOL.

Donde RPG sí tiene algo interesante para esta clase es en las **estructuras solapadas** de la clase
091, que dan la unión:

```rpgle
dcl-ds figura qualified;
  tipo char(1);
  datos char(9);
  lado  packed(9:0) overlay(datos);       // vista de CUADRADO
  ancho packed(5:0) overlay(datos : 1);   // vista de RECTANGULO
  alto  packed(4:0) overlay(datos : 6);
end-ds;
```

Sin comprobación, como en COBOL, y con el mismo uso real: **describir registros de fichero cuyo
formato depende de un código de tipo**, que es un patrón muy común en los ficheros de intercambio
bancario y de EDI.

Y hay una construcción de RPG que es lo más parecido a una enumeración que tiene la plataforma, y que
merece mención porque no está en el lenguaje sino en la base de datos:

```sql
create table figuras (
  tipo char(10) not null
       check (tipo in ('cuadrado', 'rectangulo'))
);
```

Una **restricción de comprobación** en Db2 for i limita los valores válidos de una columna, y el
sistema la impone **para todos los programas que escriban en esa tabla**, sean RPG, COBOL, SQL o Java.

Es la enumeración implementada en el sitio donde de verdad importa: **el dato**. Un `enum` en el
lenguaje protege un programa; una restricción en la tabla protege los cuarenta programas que la usan y
los que se escriban dentro de diez años.

Ese argumento —**la validación pertenece al dato, no al código**— es la razón de que en las
plataformas de gestión las reglas vivan en el esquema, y es exactamente lo mismo que hace FileMan en
M (clase 099).
"""),
        "pli": ("""
 figura: procedure options(main);

    declare linea char(200) varying;
    declare tipo  char(20)  varying;
    declare resto char(200) varying;
    declare corte fixed binary(31);
    declare (a, b) fixed binary(31) initial(0);
    declare area fixed binary(31) initial(0);

    get edit (linea) (a(200));
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
       when ('cuadrado')   area = a * a;
       when ('rectangulo') area = a * b;
       otherwise           area = 0;
    end;

    put skip list ('area=' || trim(char(area)));

 end figura;
""", """
**Lo que esta clase enseña en PL/I.** **PL/I no tiene enumeraciones.** No hay tipo enumerado, y los
códigos se representan con constantes declaradas o con literales sueltos:

```pli
%declare CUADRADO character;
%CUADRADO = '''cuadrado''';        /* constante del PREPROCESADOR */
```

Usar el preprocesador para las constantes es el idioma clásico, con los mismos problemas que
`#define` en C: **no hay tipo, no hay ámbito y no hay comprobación**.

Y para tipos suma, PL/I tiene la unión sin discriminante, con dos formas:

```pli
declare 1 figura,
          2 tipo char(1),
          2 datos,
            3 lado fixed binary(31);

declare 1 vista_rect based(addr(figura.datos)),   /* superponer con un puntero */
          2 ancho fixed binary(15),
          2 alto  fixed binary(15);
```

```pli
declare 1 v union,          /* UNION explícita, en PL/I moderno */
          2 entero fixed binary(31),
          2 real   float binary(21);
```

**`union` como atributo de estructura** existe en Enterprise PL/I y es exactamente la `union` de C:
todos los miembros comparten memoria y **nadie comprueba cuál está activo**.

`select` / `when` / `otherwise`, en cambio, es una de las mejores construcciones de PL/I y anticipa el
`switch` moderno:

```pli
 select (x);
    when (1, 2, 3)  ...        /* varios valores */
    when (y > 10)   ...        /* también acepta CONDICIONES */
    otherwise       ...
 end;
```

Fíjate en dos cosas: **no hay caída entre casos** —a diferencia de C, que necesita `break`— y
**`select` sin expresión evalúa condiciones**, con lo que hace de `if`/`else if` encadenado.

Que PL/I acertara con `select` en 1964 y C fallara con `switch` en 1972, obligando a `break` y
permitiendo la caída accidental, es una de las regresiones de diseño más citadas en la historia de los
lenguajes.
"""),
        "mumps": ("""
FIGURA ; Tipos algebraicos -- clase 100
 read linea
 set tipo = $piece(linea, " ", 1)
 set a = $piece(linea, " ", 2)
 set b = $piece(linea, " ", 3)
 set area = 0
 if tipo = "cuadrado" set area = a * a
 if tipo = "rectangulo" set area = a * b
 write "area=", area, !
 quit
""", """
**Lo que esta clase enseña en M.** M **no tiene tipos, así que no tiene enumeraciones ni tipos suma**,
y esta clase es donde esa ausencia se ve con más crudeza: la etiqueta es una cadena, el despacho son
dos `if` y nada comprueba nada.

Lo que sí tiene M, y es relevante aquí, es un mecanismo de despacho sobre la etiqueta que no tiene
ningún otro lenguaje de la página: **la indirección** de la clase 085.

```mumps
 set area = $$@(tipo _ "^AREAS")(a, b)
```

Esa línea llama a la etiqueta cuyo nombre **es** el valor de `tipo`. Añadir una figura nueva es añadir
una etiqueta a la rutina `AREAS`, **sin tocar el despachador**. Es una tabla de despacho sin tabla.

Es elegante y es exactamente lo que hace imposible el análisis estático (clase 086): ninguna
herramienta puede saber qué se ejecuta ahí.

Y M no tiene ni siquiera `select`/`case`. Lo que hay son los **postcondicionales** de la clase 060:

```mumps
 set:tipo="cuadrado" area = a * a
 set:tipo="rectangulo" area = a * b
```

Dos puntos después del comando: la instrucción **solo se ejecuta si la condición es cierta**. Se puede
poner en `set`, `do`, `write`, `quit`, `kill` y casi todo, y es la construcción condicional más usada
del lenguaje.

Ese diseño —**sin bloques, sin `else` en el sentido habitual, con condición por comando**— viene de
una restricción real: M se diseñó para máquinas con 8 KB de memoria, y cada carácter contaba. De ahí
también los nombres de una letra y las abreviaturas de un carácter para todos los comandos: `s` por
`set`, `w` por `write`, `q` por `quit`.

Leer código M abreviado —`s:x="a" y=1 w y,!`— es lo que le ha dado su fama de ilegible, y es la marca
de una época en la que la densidad del código era una necesidad física, no una preferencia.
"""),
        "smalltalk": ("""
| partes tipo a area |

partes := stdin nextLine substrings.
tipo := partes first.
a := (partes at: 2) asNumber.

"En Smalltalk el 'tipo suma' se resuelve con POLIMORFISMO, no con un case"
area := tipo = 'cuadrado'
    ifTrue: [ a * a ]
    ifFalse: [ a * (partes at: 3) asNumber ].

Transcript show: 'area=', area printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk **no tiene enumeraciones ni tipos algebraicos**, y
la razón es doctrinal: **un `case` sobre el tipo de un objeto se considera un error de diseño**.

La respuesta ortodoxa es el polimorfismo:

```smalltalk
Figura subclass: #Cuadrado   instanceVariableNames: 'lado'.
Figura subclass: #Rectangulo instanceVariableNames: 'ancho alto'.

Cuadrado   >> area  ^lado * lado
Rectangulo >> area  ^ancho * alto

figuras inject: 0 into: [ :suma :f | suma + f area ]
```

Cada figura sabe calcular su área. **No hay `case`, no hay etiqueta y no hay despachador**, y añadir
`Circulo` es escribir una clase con un método `area` — **sin tocar ni recompilar nada**.

Es el otro extremo del *expression problem* que apareció en la página de Lisp: la jerarquía facilita
añadir variantes y dificulta añadir operaciones —para una operación nueva hay que tocar todas las
clases—, mientras que el tipo suma con `case` hace lo contrario.

Y como enumeración, lo idiomático es el **símbolo** (clase 093):

```smalltalk
#norte    #sur    #este    #oeste
estado := #pendiente.
estado == #pendiente ifTrue: [ ... ]
```

Únicos, comparables por identidad, imprimibles y sin declarar nada. Es la misma solución que Lisp, con
el mismo mecanismo.

Y hay un patrón clásico de Smalltalk que resuelve el caso de los estados con comportamiento, y que
lleva su nombre por esto: **el patrón Estado**. En lugar de una variable `estado` con un símbolo y un
`case` en cada método, el objeto **delega en un objeto estado** y cambiar de estado es cambiar esa
referencia.

```smalltalk
Pedido >> procesar    ^estado procesar: self
```

Los patrones de diseño del libro de la *Banda de los Cuatro* (1994) salieron en buena parte de la
comunidad Smalltalk, y varios de ellos —Estado, Estrategia, Visitante— son formas de **sustituir un
`case` por polimorfismo**. Que hoy se enseñen como patrones en lenguajes que sí tienen tipos suma es
una ironía histórica: en muchos casos, el tipo suma con emparejamiento exhaustivo es más simple y más
seguro que el patrón que se inventó para evitarlo.
"""),
    },
)
