# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 075

> [⬅️ Volver a la clase 075](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Construir el texto `punto(x=3, y=4)`. Un programa trivial que sirve de excusa para la pregunta de la
clase: **¿se puede decir a qué parámetro corresponde cada argumento en el sitio de la llamada?**
Porque `dibujar(10, 20, 1, 0, 1)` no se entiende sin ir a buscar la firma, y ese problema tiene
sesenta años.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto son los **argumentos nombrados**, y estos lenguajes lo enseñan porque **tres de
> ellos los tienen desde hace décadas y son mejores que los de casi todo el núcleo**. **Ada** los
> introdujo en 1983 con `Nombre => Valor` y permite mezclarlos con los posicionales. **Fortran 90** los
> tiene y son la razón de que las interfaces de LAPACK, con quince parámetros, sean usables. **Lisp**
> los tiene con `&key`. Y **Smalltalk** los tiene de una forma que hace innecesaria la característica:
> **el nombre está en el selector**, así que todos los argumentos van siempre nombrados.
>
> Enfrente, **C++ sigue sin tenerlos** en 2026, y esa es una de sus carencias más comentadas.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros: x, y) → stdout: `punto(x=<a>, y=<b>)`
- **Regla:** `punto(x=a, y=b)`

| stdin | esperado |
|---|---|
| `3 4` | `punto(x=3, y=4)` |
| `0 -2` | `punto(x=0, y=-2)` |
| `5 5` | `punto(x=5, y=5)` |

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
PROGRAM-ID. PUNTO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  X-V     PIC S9(9) COMP-3.
01  Y-V     PIC S9(9) COMP-3.
01  ED-X    PIC -(8)9.
01  ED-Y    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO X-V
    MOVE FUNCTION NUMVAL(TXT-B) TO Y-V

    MOVE X-V TO ED-X
    MOVE Y-V TO ED-Y
    DISPLAY "punto(x=" FUNCTION TRIM(ED-X)
            ", y=" FUNCTION TRIM(ED-Y) ")"
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL **no tiene argumentos nombrados**, y un `CALL ... USING`
con seis campos es exactamente el problema que esta clase describe.

Pero COBOL tiene una solución al mismo problema que es característica suya y que sigue siendo buena:
**pasar una estructura con campos nombrados en lugar de una lista de argumentos**.

```cobol
01  PARAMETROS-DIBUJO.
    05  PD-X         PIC S9(4) COMP-3.
    05  PD-Y         PIC S9(4) COMP-3.
    05  PD-COLOR     PIC X(10).
    05  PD-GROSOR    PIC 9(2)  COMP-3.
    05  PD-RELLENO   PIC X.
        88  CON-RELLENO  VALUE "S".

MOVE 10 TO PD-X
MOVE 20 TO PD-Y
SET CON-RELLENO TO TRUE
CALL "DIBUJAR" USING PARAMETROS-DIBUJO
```

Cada valor se asigna **por su nombre** antes de la llamada, y la llamada pasa un solo argumento. Es
verboso y es completamente legible: se ve qué se está poniendo y qué se deja como estaba.

Ese patrón —el "bloque de parámetros"— es el estándar de facto en el mundo mainframe, y es idéntico a
lo que hoy se hace en C++ con un `struct` de opciones, en JavaScript con un objeto y en Go con el
patrón de opciones funcionales. **Cuando un lenguaje no tiene argumentos nombrados, todos acaban
inventando el mismo sustituto.**

Y el copybook de la clase 052 hace que esa estructura se comparta entre todos los programas que la
usan.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program punto
   implicit none
   integer :: a, b

   read(*, *) a, b

   !  Llamada con PALABRAS CLAVE: el orden deja de importar.
   call mostrar(x = a, y = b)

contains

   subroutine mostrar(x, y)
      integer, intent(in) :: x, y
      character(len=32) :: bx, by
      write(bx, '(I0)') x
      write(by, '(I0)') y
      write(*, '(A,A,A,A,A)') 'punto(x=', trim(bx), ', y=', trim(by), ')'
   end subroutine mostrar

end program punto
```

**Lo que esta clase enseña en Fortran.** `call mostrar(x = a, y = b)` usa **argumentos por palabra
clave**, que Fortran tiene desde 1990 y que casi nadie asocia con este lenguaje.

La regla es la misma que en Python: **los posicionales primero, los nombrados después**, y una vez que
empiezas a nombrar ya no puedes volver a la posición.

```fortran
call resolver(matriz, vector, tolerancia = 1e-9, maxiter = 500)
```

Y aquí está el motivo real de que exista: **combinado con `optional` de la clase 074, permite saltar
parámetros intermedios**. Las rutinas de LAPACK y de las bibliotecas numéricas tienen firmas de
quince argumentos, la mayoría opcionales, y sin palabras clave serían inutilizables.

Hay un requisito importante: **la palabra clave es el nombre del parámetro tal como aparece en la
interfaz**, así que el compilador tiene que conocerla. Eso obliga a que la rutina esté en un `module`
o en un `contains`, o a declarar una `interface` explícita. Con las subrutinas externas al estilo
FORTRAN 77 —sin interfaz— **no se pueden usar palabras clave**.

Es una de las razones de que el Fortran moderno insista tanto en poner todo dentro de módulos: sin
interfaz explícita se pierden las palabras clave, la comprobación de tipos en las llamadas y los
argumentos opcionales.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;         use Ada.Strings;
with Ada.Strings.Fixed;

procedure Punto is

   function Formatear (X, Y : Integer) return String is
      use Ada.Strings.Fixed;
   begin
      return "punto(x=" & Trim (Integer'Image (X), Both) &
             ", y=" & Trim (Integer'Image (Y), Both) & ")";
   end Formatear;

   A, B : Integer;
begin
   Get (A);
   Get (B);

   --  ASOCIACIÓN POR NOMBRE: el orden deja de importar.
   Put_Line (Formatear (X => A, Y => B));
end Punto;
```

**Lo que esta clase enseña en Ada.** `X => A` es la **asociación por nombre**, y Ada la tiene desde
1983 — antes que ningún otro lenguaje de uso general.

Y no es solo para llamadas: **la misma sintaxis funciona en todos los sitios donde hay una
correspondencia**.

```ada
Formatear (X => 10, Y => 20);                       --  llamadas
V : Vector := (1 => 10, 2 => 20, others => 0);      --  agregados de array
P : Punto  := (X => 10, Y => 20);                   --  agregados de registro
package Mi_IO is new Text_IO.Integer_IO (Num => Mi_Tipo);   --  genéricos
Put (Item => X, Width => 5, Base => 16);            --  y con valores por defecto
```

Esa uniformidad es muy propia de Ada: **un mecanismo, aplicado en todos los contextos donde tiene
sentido**.

Y hay una construcción que merece verse porque no tiene equivalente: **el agregado con `others`**.

```ada
Config : Opciones := (Color => Rojo, others => <>);
```

`others => <>` significa "el resto, con su valor por defecto". Con eso, un registro de veinte campos
se construye nombrando solo los tres que interesan, y el compilador **comprueba que estén todos
cubiertos**. Es lo que en C++ se intenta con los inicializadores designados de C++20 y en Rust con
`..Default::default()`.

La regla de Ada es la misma que en Fortran: los posicionales primero, y una vez nombrado, todo
nombrado.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Punto;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  P, X, Y: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);
  P := Pos(' ', Linea);
  X := StrToInt(Copy(Linea, 1, P - 1));
  Y := StrToInt(Trim(Copy(Linea, P + 1, Length(Linea))));

  WriteLn(Format('punto(x=%d, y=%d)', [X, Y]));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal **no tiene argumentos nombrados**, y su sustituto es el
**registro**, que es la misma solución que el bloque de parámetros de COBOL:

```pascal
type
  TOpcionesDibujo = record
    X, Y: Integer;
    Color: TColor;
    Grosor: Integer;
    Relleno: Boolean;
  end;

var
  Op: TOpcionesDibujo;
begin
  Op := Default(TOpcionesDibujo);    { todo a cero/vacío }
  Op.X := 10;
  Op.Y := 20;
  Op.Relleno := True;
  Dibujar(Op);
```

`Default(T)` de Delphi moderno inicializa el registro entero a valores nulos, lo que evita el
problema de olvidar un campo.

Fíjate también en `Format('punto(x=%d, y=%d)', [X, Y])`: es el `printf` de Object Pascal, con los
argumentos en un **array abierto** entre corchetes. Y admite **índices de argumento**, que es lo más
cerca que llega Pascal a los nombres en el formato:

```pascal
Format('%1:d viene antes de %0:d', [A, B]);     { reordena los argumentos }
```

Ese `%1:d` es útil para traducciones, donde el orden de las palabras cambia según el idioma. Es la
misma idea que `{0}` y `{1}` en C# y `%1$s` en `printf` de POSIX.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun punto (&key x y)
  (format nil "punto(x=~D, y=~D)" x y))

(let* ((a (read))
       (b (read)))
  (format t "~A~%" (punto :x a :y b)))
```

**Lo que esta clase enseña en Common Lisp.** `&key` declara parámetros **de palabra clave**, y la
llamada los pasa con `:nombre valor`. El orden es irrelevante y los que falten toman su valor por
defecto.

```lisp
(defun dibujar (&key x y (color :negro) (grosor 1) relleno)
  ...)

(dibujar :y 20 :x 10 :relleno t)     ; en cualquier orden, saltando los que sea
```

Y `:x` no es una cadena ni un identificador: es un **símbolo de palabra clave**, un objeto de primera
clase que se puede guardar, comparar y pasar como dato. Eso permite construir listas de argumentos en
ejecución:

```lisp
(let ((args (list :x 10 :y 20)))
  (apply #'dibujar args))            ; los argumentos, como DATO
```

Ese patrón —una lista de propiedades que se aplica a una función— es la base de gran parte del código
de configuración en Lisp, y es lo que hace que las funciones con muchas opciones sean cómodas de
envolver.

Lisp permite además combinar las cuatro clases de parámetro que ya aparecieron en la clase 073, y
tiene `&allow-other-keys` para aceptar claves que no conoce —útil para pasar opciones a una función
interna sin enumerarlas—.

La contrapartida honesta: `&key` tiene un coste en ejecución. Cada llamada recorre la lista buscando
las claves, así que en un bucle muy caliente se prefieren los posicionales. Es la misma disyuntiva
que en Python.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc punto {args} {
    array set op {-x 0 -y 0}
    array set op $args
    return "punto(x=$op(-x), y=$op(-y))"
}

gets stdin linea
lassign [split [string trim $linea]] a b

puts [punto -x $a -y $b]
```

**Lo que esta clase enseña en Tcl.** Tcl **no tiene argumentos nombrados en el lenguaje**, y sin
embargo los usa por todas partes — porque los construye con las piezas normales.

El idioma es el de este programa: **`args` recoge todo, y `array set` lo interpreta como pares
opción-valor**, sobre unos valores por defecto puestos antes. Tres líneas.

```tcl
array set op {-x 0 -y 0 -color negro}    ;# defectos
array set op $args                        ;# los del usuario los pisan
```

Y funciona porque `args` recibe una lista plana y `array set` espera exactamente eso: una lista de
pares. **No hay ninguna sintaxis nueva.**

Esa convención —opciones con guion delante— es la de todos los comandos del propio Tcl:

```tcl
lsort -integer -decreasing $lista
string match -nocase $patron $texto
switch -regexp -matchvar m -- $x { ... }
regsub -all -- $patron $texto $reemplazo
```

Por eso los procedimientos de usuario la imitan: **la coherencia con el lenguaje es más valiosa que
una sintaxis dedicada**.

Para casos serios, Tcllib ofrece `cmdline::getoptions`, que además genera el mensaje de uso. Y el
`--` que aparece en varios de esos ejemplos es lo de la clase 061: marca el final de las opciones,
para que un valor que empiece por guion no se confunda con una.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub punto {
    my %arg = @_;                  # los argumentos, como pares clave => valor
    return "punto(x=$arg{x}, y=$arg{y})";
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

print punto(x => $p, y => $q), "\n";
```

**Lo que esta clase enseña en Perl.** `my %arg = @_;` es el idioma universal de Perl para argumentos
nombrados, y funciona por una razón elegante: **`@_` es una lista plana, y asignar una lista a un
hash la interpreta como pares clave-valor**.

Y `=>` no es un operador especial: es **una coma que además entrecomilla lo que tiene a su
izquierda**. Por eso `x => 3` es exactamente `'x', 3`.

```perl
punto(x => 3, y => 4);      # la subrutina recibe la lista ('x', 3, 'y', 4)
```

El patrón completo, con valores por defecto y validación, es este:

```perl
sub dibujar {
    my %arg = (color => 'negro', grosor => 1, @_);   # defectos PRIMERO
    die "falta x" unless exists $arg{x};
    ...
}
```

Poner los defectos **antes** de `@_` en la lista hace que los del usuario los pisen, porque en la
construcción de un hash **gana la última aparición de cada clave**. Es el mismo truco que
`array set` en Tcl, con otra sintaxis.

Y en Perl moderno se usa `Params::Validate` o el módulo del núcleo `builtin` para validar, o bien la
firma de 5.36 con un hash:

```perl
use v5.36;
sub dibujar ($x, $y, %opciones) { ... }     # posicionales y luego nombrados
```

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

struct Punto {
    int x;
    int y;
};

std::string formatear(const Punto& p) {
    return "punto(x=" + std::to_string(p.x) + ", y=" + std::to_string(p.y) + ")";
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << formatear(Punto{a, b}) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** **C++ no tiene argumentos nombrados**, en 2026, y es una de sus
carencias más señaladas. Ha habido propuestas repetidas al comité y ninguna ha prosperado.

Los sustitutos son tres, y todos son incómodos:

```cpp
// 1) Struct de opciones -- el más usado
struct OpcionesDibujo { int x; int y; Color color = Negro; int grosor = 1; };
dibujar({.x = 10, .y = 20, .grosor = 3});     // inicializadores DESIGNADOS, C++20

// 2) Tipos fuertes para que no se confundan
dibujar(Ancho{10}, Alto{20});

// 3) Encadenar setters -- el patrón "builder"
Dibujo{}.x(10).y(20).grosor(3).ejecutar();
```

La primera es la más cercana, y llegó con **C++20**: los **inicializadores designados** —`.x = 10`—
permiten construir un agregado nombrando los campos. Vienen de C99, donde existían desde hacía veinte
años, y **C++ los adoptó con una restricción**: tienen que ir **en el orden de declaración**, cosa que
en C no hace falta.

La segunda merece atención porque es una técnica de diseño transferible: envolver cada parámetro en
su propio tipo hace **imposible confundir el orden**. `dibujar(Alto{20}, Ancho{10})` no compila. Es
más trabajo y da una garantía que ningún argumento nombrado da — es la idea de los tipos de Ada de la
clase 050, aplicada a las firmas.

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

dcl-pi PUNTO;
  x int(10) const;
  y int(10) const;
end-pi;

dcl-s salida char(60);

salida = 'punto(x=' + %char(x) + ', y=' + %char(y) + ')';
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG **no tiene argumentos nombrados**, y su sustituto es el mismo
que el de COBOL: **una estructura de datos con campos nombrados**.

```rpgle
dcl-ds opcionesDibujo qualified template;
  x       int(10);
  y       int(10);
  color   char(10) inz('negro');
  grosor  int(10)  inz(1);
end-ds;

dcl-ds op likeds(opcionesDibujo);

op.x = 10;
op.y = 20;
op.grosor = 3;
dibujar(op);
```

Tres palabras clave hacen que esto funcione bien, y merecen conocerse:

- **`qualified`** obliga a escribir `op.x` en lugar de `x` a secas. Sin ella, los subcampos serían
  nombres globales del programa —herencia del RPG antiguo— y colisionarían.
- **`template`** declara la estructura **sin reservar memoria**: solo sirve como molde para `likeds`.
  Es el `typedef` que RPG no tenía.
- **`likeds`** declara una variable con la misma forma que otra, que es la inferencia de la clase 052.

`inz()` en los campos da los valores por defecto, así que la estructura nace con ellos y solo hay que
tocar lo que cambie. Es exactamente el patrón de la clase 074 resuelto con datos en lugar de con
parámetros.

Y `qualified` es una de esas mejoras pequeñas que cambian mucho un lenguaje: pasar de un espacio de
nombres global plano a nombres cualificados es lo que permitió que RPG tuviera estructuras
reutilizables.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 punto: procedure options(main);

    declare (x, y) fixed binary(31);

    get list (x, y);

    put skip list ('punto(x=' || trim(char(x)) ||
                   ', y='     || trim(char(y)) || ')');

 end punto;
```

**Lo que esta clase enseña en PL/I.** PL/I **no tiene argumentos nombrados**, pero tiene una
construcción que resuelve el mismo problema desde otro ángulo y que no existe en ningún lenguaje del
núcleo: **`BY NAME`**.

```pli
declare 1 origen,
          2 x fixed binary(31),
          2 y fixed binary(31),
          2 color character(10);

declare 1 destino,
          2 x fixed binary(31),
          2 y fixed binary(31),
          2 grosor fixed binary(31);

destino = origen, by name;      /* copia SOLO los campos que coinciden POR NOMBRE */
```

`by name` copia estructura a estructura **emparejando los campos por su nombre**, ignorando los que
no existan en el otro lado. Es una operación que hoy se resuelve a mano campo a campo, o con
reflexión, o con una biblioteca de mapeo de objetos.

RPG tiene la misma idea con **`eval-corr`** (*evaluate corresponding*), y COBOL con **`MOVE
CORRESPONDING`**. Los tres lenguajes de negocio la tienen, y los de sistemas no — porque el caso de
uso es el mismo: **mover datos entre dos registros parecidos pero no idénticos**, que es lo que hace
una aplicación de gestión todo el día.

Es un buen ejemplo de que "lenguaje antiguo" no significa "menos expresivo": significa **expresivo en
otras cosas**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PUNTO ; Argumentos nombrados -- clase 075
 read linea
 set x = $piece(linea, " ", 1)
 set y = $piece(linea, " ", 2)
 write "punto(x=", x, ", y=", y, ")", !
 quit
```

**Lo que esta clase enseña en M.** M **no tiene argumentos nombrados**, y su sustituto es el más
natural del lenguaje: **pasar un array por referencia**, con los nombres como subíndices.

```mumps
 kill opciones
 set opciones("x") = 10
 set opciones("y") = 20
 set opciones("relleno") = 1
 do DIBUJAR^GRAF(.opciones)          ; el punto = por referencia
 ;
DIBUJAR(op) ;
 new x, y
 set x = $get(op("x"), 0)            ; con valor por defecto, clase 074
 set y = $get(op("y"), 0)
 ...
```

Ese patrón es el estándar de facto en el mundo M, y en **VistA** es literalmente la convención de
todas las APIs de FileMan: se rellena un array local con subíndices convenidos y se pasa con punto.

Tiene dos propiedades interesantes. La primera: **el array puede tener cualquier estructura**, así que
un "argumento nombrado" puede ser a su vez un subárbol completo —`opciones("borde","color")`—. Es
JSON antes de JSON.

La segunda: **la rutina llamada puede añadir campos al array**, así que el mismo mecanismo sirve para
devolver resultados y errores, que es lo de la clase 072.

La contrapartida es la de siempre en M: **ningún nombre está declarado en ninguna parte**. Escribir
`opciones("colr")` no da error; simplemente ese campo nunca se lee. La documentación del array es el
único contrato, y por eso FileMan tiene un diccionario que la describe.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes x y |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
x := partes first.
y := partes second.

Transcript
    show: 'punto(x=', x printString, ', y=', y printString, ')';
    cr.
```

**Lo que esta clase enseña en Smalltalk.** **En Smalltalk todos los argumentos van nombrados,
siempre, y no hay forma de que no lo estén.** El nombre del método está **intercalado** entre ellos:

```smalltalk
Punto x: 10 y: 20
rectangulo desde: origen hasta: esquina
coleccion copyFrom: 1 to: 5
imagen dibujarEn: lienzo con: color grosor: 2 relleno: true
```

Esa última llamada se lee entera sin consultar ninguna firma. Compárala con
`dibujar(lienzo, color, 2, true)` en cualquier lenguaje posicional: los dos últimos argumentos son
indescifrables sin ir a buscar la declaración.

Y la propiedad importante es que **el nombre no es opcional ni decorativo: ES el selector**. El
método se llama `dibujarEn:con:grosor:relleno:`, con las cuatro partes. Cambiar el orden no es
reordenar argumentos: es **llamar a otro método que probablemente no existe**, y el compilador lo
detecta.

De ahí se siguen tres cosas:

1. **No hay sobrecarga**, porque dos métodos con distintos argumentos tienen distinto nombre.
2. **No hacen falta argumentos por defecto**, porque la variante corta es otro selector (clase 074).
3. **No hay confusión de orden**, porque el orden está fijado por el nombre.

Es la decisión de diseño más influyente de Smalltalk que **casi nadie copió** —solo Objective-C y,
parcialmente, Swift—, y sigue siendo la respuesta más limpia a esta clase.

---

## Y de vuelta a la clase

Lo transferible es una regla de diseño de APIs: **si una función tiene más de tres parámetros del
mismo tipo, el sitio de la llamada es ilegible sin nombres**. Los lenguajes que no los tienen han
inventado sustitutos —un `struct` de opciones en C++, un hash en Perl, un objeto de configuración en
JavaScript— y todos son el mismo remedio. Cuando diseñes una firma larga, la pregunta no es cuántos
parámetros caben: es **si alguien podrá leer la llamada dentro de un año**.

⏮️ [Volver a la clase 075](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
