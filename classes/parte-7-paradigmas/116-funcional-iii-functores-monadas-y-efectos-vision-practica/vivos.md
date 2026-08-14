# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 116

> [⬅️ Volver a la clase 116](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un valor que puede no estar, y una operación que solo se aplica si está. Es `Option`/`Maybe`, la
mónada más útil que existe, y su motivo tiene nombre y fecha: **Tony Hoare llamó a la referencia nula
"mi error de mil millones de dólares"**, y la introdujo en ALGOL W en 1965. Aquí hay dos lenguajes que
**nunca tuvieron ese error**: Ada, por diseño, y Fortran, casi por accidente.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **hacer explícita la ausencia en el tipo**, y estos lenguajes lo enseñan porque
> cubren las tres posturas. **Ada** lo tiene resuelto desde 1983 con los **registros variantes con
> discriminante** (clase 100) y con los subtipos que impiden el valor inválido. **Fortran** lo consigue
> con `allocatable`: una variable no reservada **es** un `None`, y `allocated()` es la comprobación.
> **C++** llegó en 2017 con `std::optional`.
>
> Y enfrente, **COBOL, RPG y M no tienen nulos ni los necesitan**: en su modelo de datos, la ausencia es
> un valor convenido —espacios, ceros, un indicador aparte— y esa decisión, que parece pobre, evita el
> problema entero.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `resultado=<2n>` si n>0 (hay valor), o `resultado=nada` si no
- **Regla:** `Option(n si n>0).map(x → 2x)`

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=nada` |
| `-3` | `resultado=nada` |

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
PROGRAM-ID. FUNC3.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  OPCIONAL.
    05  HAY-VALOR  PIC X VALUE "N".
        88  HAY        VALUE "S".
        88  NO-HAY     VALUE "N".
    05  VALOR      PIC S9(18) COMP-3 VALUE 0.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    IF N > 0
        SET HAY TO TRUE
        MOVE N TO VALOR
    ELSE
        SET NO-HAY TO TRUE
    END-IF

    IF HAY
        COMPUTE VALOR = VALOR * 2
        MOVE VALOR TO ED-R
        DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    ELSE
        DISPLAY "resultado=nada"
    END-IF

    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene nulos**, y esa ausencia es una de las razones
por las que sus sistemas son tan estables — merece decirlo sin ironía.

En COBOL, un campo numérico **siempre tiene un número** y uno alfanumérico **siempre tiene
caracteres**. No existe el estado "esta variable no apunta a nada", así que **no existe la clase
entera de errores de referencia nula** que domina las listas de fallos de Java, C# y JavaScript.

El precio es que **la ausencia hay que representarla**, y COBOL lo hace con la construcción de este
programa: **un indicador con niveles 88** (clase 092).

```cobol
05  HAY-VALOR  PIC X.
    88  HAY     VALUE "S".
    88  NO-HAY  VALUE "N".
```

Eso es un `Option` escrito a mano: **una bandera que dice si el valor cuenta**, y un `IF HAY` antes de
usarlo. Sin comprobación del compilador, y con una legibilidad que los nombres de condición hacen
sorprendentemente buena.

Y donde COBOL sí se encuentra con nulos de verdad es en la frontera con SQL, y ahí la solución es
peculiar y merece conocerse: **las variables indicadoras**.

```cobol
01  IMPORTE      PIC S9(11)V99 COMP-3.
01  IND-IMPORTE  PIC S9(4) COMP.

EXEC SQL
    SELECT IMPORTE INTO :IMPORTE :IND-IMPORTE
      FROM FACTURAS WHERE ID = :ID
END-EXEC

IF IND-IMPORTE < 0
    DISPLAY "el importe era NULL"
END-IF
```

**Cada columna que pueda ser nula lleva una variable acompañante** que vale −1 si el valor era `NULL`.
Es exactamente `Option<T>` partido en dos variables, y está en el estándar de SQL incrustado desde los
años ochenta.

Y hay una trampa clásica: **si se omite la variable indicadora y la columna es nula, el programa
recibe un error de ejecución** —`SQLCODE -305`— en lugar de un valor. El lenguaje obliga a
enfrentarse al nulo, aunque sea a golpes.

Es la misma idea que un `Option` que no se puede ignorar, conseguida con una convención de 1985.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program func3
   implicit none
   integer, allocatable :: opcional      ! sin reservar = "no hay valor"
   integer :: n

   read(*, *) n

   if (n > 0) allocate(opcional, source=n)

   if (allocated(opcional)) then
      write(*, '(A,I0)') 'resultado=', opcional * 2
   else
      write(*, '(A)') 'resultado=nada'
   end if
end program func3
```

**Lo que esta clase enseña en Fortran.** Este programa usa algo que casi nadie asocia con Fortran y que
funciona sorprendentemente bien: **un escalar `allocatable` ES un `Option`**.

```fortran
integer, allocatable :: opcional
allocate(opcional, source=n)      ! Some(n)
deallocate(opcional)               ! volver a None
allocated(opcional)                ! isSome()
```

Una variable `allocatable` **no reservada no tiene valor**, y `allocated()` lo comprueba. Es la
distinción exacta entre `Some` y `None`, con dos ventajas notables sobre un puntero nulo:

1. **No hay puntero colgante posible**: un `allocatable` se libera al salir del ámbito (clase 103) y
   no puede tener alias.
2. **Acceder a uno no reservado es un error detectado** con `-fcheck=all`, no basura.

Y desde Fortran 2003, los **componentes `allocatable` de un tipo derivado** dan campos opcionales:

```fortran
type :: paciente
   character(len=:), allocatable :: segundo_apellido    ! puede no existir
   real, allocatable :: mediciones(:)                    ! puede estar vacío
end type
```

Eso es exactamente `Option<String>` y `Option<Vec<f64>>`, en un lenguaje de 1957 modernizado en 2003.

Y merece señalar el contraste con la otra herramienta de Fortran: **los punteros sí pueden ser nulos**,
y ahí sí reaparece el problema.

```fortran
type(nodo), pointer :: p => null()
if (associated(p)) ...          ! hay que comprobarlo
p%valor                          ! si p es nulo: comportamiento indefinido
```

La guía moderna de Fortran es tajante y encaja con toda esta clase: **usa `allocatable` siempre que
puedas y `pointer` solo cuando necesites alias o estructuras enlazadas**. Es el mismo consejo que en
Rust —`Box` frente a referencias crudas— y en C++ —valores y `optional` frente a punteros—.

Un lenguaje al que se le supone primitivo tiene, por accidente de diseño, **el tipo opcional que Java
tardó hasta 2014 en tener**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Func3 is
   --  Un Option de verdad: registro VARIANTE con discriminante (clase 100)
   type Opcional (Hay : Boolean := False) is record
      case Hay is
         when True  => Valor : Integer;
         when False => null;
      end case;
   end record;

   function Mapear (O : Opcional) return Opcional is
     (if O.Hay then (Hay => True, Valor => O.Valor * 2) else (Hay => False));

   N : Integer;
   O : Opcional;
begin
   Get (N);

   if N > 0 then
      O := (Hay => True, Valor => N);
   else
      O := (Hay => False);
   end if;

   declare
      R : constant Opcional := Mapear (O);
   begin
      if R.Hay then
         Put ("resultado=");
         Put (R.Valor, Width => 1);
         New_Line;
      else
         Put_Line ("resultado=nada");
      end if;
   end;
end Func3;
```

**Lo que esta clase enseña en Ada.** **Ada nunca tuvo el error de los mil millones de dólares**, y hay
que decirlo con precisión porque es notable: **en Ada, un tipo normal no puede ser nulo**.

`Integer`, `Float`, un registro, un arreglo — **ninguno tiene un valor "vacío"**. Solo los **tipos de
acceso** —los punteros explícitos— pueden valer `null`, y hay que declararlos como tales.

Y desde **Ada 2005** ni siquiera eso, si no se quiere:

```ada
type Ref is not null access Integer;      --  NO PUEDE ser nulo, nunca
procedure P (X : not null access Nodo);    --  el parámetro tampoco
```

**`not null` es parte del tipo**, y el compilador rechaza asignarle `null` o pasar algo que pueda
serlo. Es lo que Kotlin hizo con `String?` frente a `String` en 2011, y Ada en 2005.

El `Opcional` de este programa es un **registro variante con discriminante**, y con eso vienen las
cuatro garantías de la clase 100:

1. **Acceder a `O.Valor` cuando `Hay` es `False` lanza `Constraint_Error`.** No es basura: es un
   error detectado.
2. **El agregado debe ser coherente**: no se puede construir un `Opcional` con `Hay => False` y un
   valor dentro.
3. **Un objeto con discriminante fijo no puede cambiar de variante.**
4. **Un `case` sobre el discriminante debe cubrir los dos casos.**

Y Ada tiene además la vía que hace innecesario el `Option` en muchos casos, y que es la más
característica del lenguaje: **acotar el tipo para que el valor inválido no exista** (clase 092).

```ada
subtype Positivo is Integer range 1 .. Integer'Last;
```

Si el dominio es "un entero positivo", **no hace falta representar la ausencia**: el tipo ya excluye
lo que no vale, y asignar 0 lanza `Constraint_Error` en el punto donde ocurre, no tres capas después.

Esa es la filosofía que recorre a Ada entero y que hoy se llama *hacer que los estados inválidos sean
irrepresentables*: **antes de envolver el valor en un `Option`, pregúntate si el tipo puede
descartarlo**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Func3;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TOpcional = record
    Hay: Boolean;
    Valor: Integer;
  end;

function Mapear(const O: TOpcional): TOpcional;
begin
  if O.Hay then
  begin
    Result.Hay := True;
    Result.Valor := O.Valor * 2;
  end
  else
    Result.Hay := False;
end;

var
  N: Integer;
  O, R: TOpcional;

begin
  Read(N);

  O.Hay := N > 0;
  O.Valor := N;

  R := Mapear(O);

  if R.Hay then
    WriteLn('resultado=', IntToStr(R.Valor))
  else
    WriteLn('resultado=nada');
end.
```

**Lo que esta clase enseña en Pascal.** Pascal tiene el problema del nulo **solo en los punteros y en
las referencias de objeto**: los tipos valor —enteros, reales, registros, conjuntos— **siempre tienen
valor**.

```pascal
var
  N: Integer;        { siempre tiene un número (basura si no se inicializa) }
  P: PNodo;           { puede ser nil }
  O: TObjeto;          { referencia: puede ser nil }
```

Y esa segunda columna es la fuente de la excepción más famosa del ecosistema Delphi: **`Access
violation at address ...`**, que es lo que ocurre al llamar a un método de una referencia `nil`.

Object Pascal tiene una mitigación elegante que otros lenguajes tardaron en copiar: **algunas
operaciones sobre `nil` son seguras a propósito**.

```pascal
O.Free;              { seguro aunque O sea nil: Free lo comprueba }
FreeAndNil(O);        { libera y pone nil, para evitar el uso posterior }
```

`Free` es un método de `TObject` que comprueba `Self <> nil` antes de destruir, así que **liberar algo
que no se creó no falla**. Es una decisión pequeña que evita muchos errores.

Y Free Pascal 3.2 y Delphi 10.4 añadieron lo que esta clase pide, con genéricos:

```pascal
uses SysUtils;

var O: specialize TNullable<Integer>;      { Free Pascal }
var O: TOptional<Integer>;                  { con Spring4D en Delphi }

if O.HasValue then WriteLn(O.Value);
```

`TNullable<T>` y los `Nullable` de Spring4D son exactamente el `Option` de esta clase, implementados
como registros con un booleano y sobrecarga de operadores.

Y hay un rincón de Pascal donde la ausencia sí está en el lenguaje desde hace mucho: **los tipos
`Variant`**, heredados de COM.

```pascal
var V: Variant;
V := Null;                { el NULL de SQL }
V := Unassigned;           { "sin asignar", distinto de Null }
VarIsNull(V);
```

**`Null` y `Unassigned` son valores distintos**, lo que reproduce la distinción de SQL entre "es nulo"
y "no se ha puesto" — y es una fuente conocida de confusión, porque son tres estados donde la
intuición espera dos.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (opcional (if (> n 0) n nil))          ; nil ES la ausencia
       (r (and opcional (* 2 opcional))))     ; `and` cortocircuita: es el map
  (format t "resultado=~A~%" (or r "nada")))
```

**Lo que esta clase enseña en Common Lisp.** En Lisp, **`nil` es la ausencia**, y esta clase es un buen
sitio para explicar por qué eso es a la vez cómodo y problemático.

`nil` es **cuatro cosas a la vez**:

```lisp
nil          ; el valor falso
nil          ; la lista VACÍA
nil          ; el símbolo NIL
'()          ; y se escribe también así
```

De ahí el idioma de este programa: `(and opcional (* 2 opcional))` **devuelve `nil` si `opcional` es
`nil`**, y si no, el resultado. Y `(or r "nada")` da el valor por defecto.

**`and` y `or` en Lisp no devuelven booleanos: devuelven el último valor evaluado**, con
cortocircuito. Con eso, `and` **es** el `map` de `Option` y `or` **es** `getOrElse`, sin ninguna
biblioteca:

```lisp
(and opcional (* 2 opcional))     ; Option.map
(or valor por-defecto)             ; Option.getOrElse
(when opcional ...)                 ; Option.ifPresent
```

Es elegante y tiene el problema que esta clase quiere señalar: **`nil` no distingue "no hay valor" de
"el valor es la lista vacía" ni de "el valor es falso"**.

```lisp
(gethash clave tabla)          ; nil: ¿no está, o está y vale nil?
```

Por eso `gethash` **devuelve dos valores**:

```lisp
(multiple-value-bind (valor presente) (gethash clave tabla)
  (if presente ...))
```

**Los valores múltiples de Common Lisp** son la solución del lenguaje a este problema, y son una
característica que casi nadie más tiene: una función puede devolver varios valores **sin construir una
estructura**, y quien llama toma los que quiera.

```lisp
(floor 7 2)                    ; devuelve 3 Y 1
(values 1 2 3)
(nth-value 1 (floor 7 2))       ; el segundo valor
```

Es una forma distinta de resolver lo mismo que `Option`: en lugar de envolver, **añadir un canal**. Y
tiene una ventaja de rendimiento —no se reserva nada— y una desventaja: **el segundo valor se pierde
en silencio si nadie lo pide**, así que no obliga a mirarlo.

Y para `Option` de verdad, el ecosistema moderno tiene `cl-monad`, `trivia` para emparejamiento de
patrones y el idioma de las condiciones (clase 103) para los errores.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set opcional {}
if {$n > 0} { set opcional $n }

if {$opcional eq ""} {
    puts "resultado=nada"
} else {
    puts "resultado=[expr {$opcional * 2}]"
}
```

**Lo que esta clase enseña en Tcl.** En Tcl **no hay nulo**: todo valor es una cadena, y la ausencia se
representa con **la cadena vacía**, que es exactamente el mismo problema que `nil` en Lisp llevado más
lejos.

```tcl
set x ""          ;# ¿ausencia, o una cadena vacía de verdad?
```

`{}` es a la vez la cadena vacía, la lista vacía, el diccionario vacío y el valor falso. **No hay forma
de distinguir "no hay dato" de "el dato es una cadena vacía"**, y en un lenguaje que procesa texto eso
importa.

Tcl ofrece dos salidas, y las dos son características:

**La primera: preguntar si la variable EXISTE.**

```tcl
info exists x             ;# ¿la variable está definida?
unset x                    ;# hacerla desaparecer
dict exists $d clave        ;# ¿la clave está en el diccionario?
array names a clave          ;# lo mismo para un array
```

**La ausencia no se representa con un valor: se representa NO TENIENDO la variable.** Es una solución
distinta a la de todos los demás lenguajes de esta página, y funciona bien porque en Tcl las variables
se crean y se destruyen libremente.

Y `dict exists` frente a `dict get` con `catch` es la diferencia entre preguntar y equivocarse:

```tcl
if {[dict exists $d clave]} { set v [dict get $d clave] }
set v [dict getwithdefault $d clave 0]      ;# Tcl 8.7
```

**La segunda: los códigos de retorno y las excepciones.**

```tcl
if {[catch { operacion } resultado opciones]} {
    # falló: `resultado` tiene el mensaje
} else {
    # bien: `resultado` tiene el valor
}
```

Ese `catch` con dos variables **es un `Result<T, E>`**: una operación que devuelve o el valor o el
error, y el código está obligado a mirar cuál. Es la misma forma de la mónada `Result`, escrita con la
sintaxis de 1988.

Tcl 8.6 lo modernizó con `try`/`on error`/`trap`, y `return -code` permite propagar estados
personalizados por la pila — un mecanismo de efectos más general que el `catch` clásico.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $opcional = $n > 0 ? $n : undef;

#  el "map" del Option: solo si hay valor
my $r = defined $opcional ? $opcional * 2 : undef;

print "resultado=", (defined $r ? $r : 'nada'), "\n";
```

**Lo que esta clase enseña en Perl.** Perl tiene **`undef`**, y a diferencia de `nil` en Lisp y de la
cadena vacía en Tcl, **`undef` sí se distingue de todo lo demás**:

```perl
defined $x          # ¿tiene valor?
exists $h{k}         # ¿la clave existe? (distinto de "vale undef")
$x // $por_defecto    # operador DEFINED-OR: solo sustituye si es undef
$x //= 10;             # asignar si no está definido
```

**El operador `//`** —*defined-or*, Perl 5.10— es exactamente `Option.getOrElse`, y es más preciso que
el `||` de la mayoría de los lenguajes:

```perl
my $puerto = $config{puerto} || 8080;      # ¡0 también da 8080! BUG
my $puerto = $config{puerto} // 8080;       # solo si NO ESTÁ DEFINIDO
```

Ese error —`||` tratando el 0 y la cadena vacía como ausencia— es tan común que JavaScript añadió `??`
en 2020 por la misma razón, catorce años después de que Perl añadiera `//`.

Y `defined` frente a `exists` es la distinción que Lisp resuelve con valores múltiples:

```perl
$h{a} = undef;
exists $h{a}      # cierto: la clave ESTÁ
defined $h{a}     # falso: y su valor es undef
```

**Tres estados —no existe, existe y vale `undef`, existe con valor— distinguibles con dos funciones.**
Es más preciso que casi todo lo de esta página.

Perl tiene además el aviso que convierte el problema en detectable: con `use warnings`, **usar un
`undef` en una operación produce un aviso**:

```text
Use of uninitialized value $x in multiplication
```

No es un error de tipos y es lo bastante ruidoso como para que el fallo se encuentre en pruebas.

Para mónadas de verdad, CPAN tiene lo esperable —`Data::Monad`, `Try::Tiny` para el `Result`— y una
que merece nombrarse por lo bien que encaja con el lenguaje: **`autodie`**.

```perl
use autodie;
open(my $fh, '<', $ruta);      # ya no hace falta `or die`
```

`autodie` convierte los fallos silenciosos de las funciones del sistema **en excepciones**, que es
justo el problema que las mónadas de error resuelven: **que el caso raro no se pueda ignorar**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <optional>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::optional<int> opcional;
    if (n > 0) {
        opcional = n;
    }

    std::optional<int> doblado;
    if (opcional) {                       // el "map" del Option
        doblado = *opcional * 2;
    }

    if (doblado) {
        std::cout << "resultado=" << *doblado << '\n';
    } else {
        std::cout << "resultado=nada\n";
    }
    return 0;
}
```

**Lo que esta clase enseña en C++.** **`std::optional` llegó en C++17**, y su valor está en lo que
sustituye: durante décadas, "puede no haber valor" se expresaba con convenciones frágiles.

```cpp
int* buscar(...);           // nullptr si no está: ¿y quién lo libera?
int buscar(...);            // devuelve -1 si no está: ¿y si -1 es válido?
bool buscar(..., int& out); // el valor por parámetro de salida
std::pair<bool, int>         // una tupla con una bandera
```

Las cuatro están en código real y las cuatro tienen problemas. `std::optional<int>` los resuelve: **el
tipo dice que puede no haber valor**, no reserva memoria y no hay que liberar nada.

Su interfaz es completa:

```cpp
o.has_value()   *o   o.value()   o.value_or(0)   o.reset()
o = std::nullopt;
std::optional<int> o = std::make_optional(5);
```

**`value()` lanza `std::bad_optional_access` si está vacío; `*o` es comportamiento indefinido.** Esa
distinción —una versión comprobada y una rápida— es marca de la casa de C++, y es una trampa: `*o` sin
comprobar antes es un error que compila.

C++23 añadió lo que faltaba para que sea una **mónada de verdad**:

```cpp
auto r = opcional
    .transform([](int x) { return x * 2; })     // map
    .and_then([](int x) -> std::optional<int> { // flatMap / bind
        return x > 100 ? std::optional{x} : std::nullopt;
    })
    .or_else([] { return std::optional{0}; });
```

**`transform` es el functor, `and_then` es la mónada**, y con esos nombres —no `map` y `bind`— el
comité evitó el vocabulario de teoría de categorías a propósito.

C++23 trajo además **`std::expected<T, E>`**, que es la mónada `Result`: o el valor o el error, sin
excepciones y sin coste cuando todo va bien. Es lo que Rust tiene desde el principio y lo que muchos
proyectos de C++ implementaban a mano.

El programa de esta página usa el estilo de C++17 porque el curso compila con `-std=c++17`, que es lo
que sigue habiendo en la mayoría de los proyectos.

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

dcl-pi FUNC3;
  n int(10) const;
end-pi;

// RPG no tiene nulos: un indicador dice si hay valor
dcl-ds opcional qualified;
  hay   ind inz(*off);
  valor int(20) inz(0);
end-ds;

if n > 0;
  opcional.hay = *on;
  opcional.valor = n;
endif;

if opcional.hay;
  dsply ('resultado=' + %char(opcional.valor * 2));
else;
  dsply ('resultado=nada');
endif;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Como COBOL, **RPG no tiene nulos** en sus tipos de datos: un
`int` siempre tiene un número y un `char` siempre tiene caracteres.

Y como COBOL, se encuentra con ellos en la frontera con la base de datos, donde IBM i tiene un
mecanismo propio y bastante elegante: **el mapa de nulos**.

```rpgle
dcl-f CLIENTES usage(*input) alwnull(*usrctl);      // el programa gestiona los nulos

if %nullind(CLI_TELEFONO);
  // esta columna era NULL
else;
  telefono = CLI_TELEFONO;
endif;

%nullind(CLI_TELEFONO) = *on;      // escribir NULL
```

**`%nullind(campo)`** es un indicador asociado a cada campo que puede ser nulo, y se lee y se escribe
como un booleano. Es `Option<T>` con el valor y la bandera en dos sitios, exactamente como las
variables indicadoras de COBOL — con una sintaxis mucho mejor.

Y `alwnull(*usrctl)` en la declaración del fichero es la decisión clave: **sin ella, el sistema
sustituye los nulos por el valor por defecto del tipo** —cero o espacios— y el programa **no se entera
de que el dato faltaba**.

Ese comportamiento por defecto es cómodo y peligroso, y es la razón de que muchos programas RPG
antiguos confundan "importe cero" con "importe desconocido". Es exactamente el problema que `Option`
resuelve.

Y en la capa SQL, IBM i ofrece las funciones estándar que hacen de `getOrElse`:

```sql
coalesce(telefono, 'sin telefono')
ifnull(importe, 0)
nullif(valor, 0)                     -- convertir 0 EN nulo
```

**`coalesce` es literalmente `Option.getOrElse` con varios candidatos**, y está en SQL desde 1992.

Merece cerrar con la observación que recorre esta página: **los lenguajes de gestión no tuvieron el
problema del nulo dentro y lo tuvieron fuera**, en la base de datos. Y SQL lo resolvió con lógica de
tres valores —cierto, falso, desconocido—, que trae sus propias sorpresas: `NULL = NULL` es **falso**,
y por eso existe `IS NULL`.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 func3: procedure options(main);

    declare n fixed binary(31);
    declare 1 opcional,
              2 hay   bit(1) initial('0'b),
              2 valor fixed binary(31) initial(0);

    get list (n);

    if n > 0 then do;
       opcional.hay = '1'b;
       opcional.valor = n;
    end;

    if opcional.hay then
       put skip list ('resultado=' || trim(char(opcional.valor * 2)));
    else
       put skip list ('resultado=nada');

 end func3;
```

**Lo que esta clase enseña en PL/I.** PL/I **sí tiene nulo, y solo en los punteros**: `null()` es una
función que devuelve el puntero nulo, y los tipos de datos normales siempre tienen valor.

```pli
 declare p pointer;
 p = null();
 if p = null() then ...
 p -> estructura        /* si p es nulo: comportamiento indefinido */
```

Es la misma situación que Fortran con `pointer` y Pascal con `nil`: **el problema existe solo donde hay
indirección**.

Lo que PL/I aporta a esta clase es una construcción que ningún otro lenguaje de la página tiene y que
va en una dirección distinta: **la condición `SUBSCRIPTRANGE` y las condiciones de datos**.

```pli
 on conversion begin;
    put list('el dato no era numérico');
    onsource = '0';        /* CORREGIR el dato y REANUDAR */
 end;

 valor = cadena_de_entrada;    /* si no es numérica, salta CONVERSION */
```

**`onsource`** permite **modificar el dato que causó el error y continuar la conversión**. Es
recuperación de errores con corrección en marcha, y es una capacidad extraordinaria para 1964: lo más
parecido que existe hoy son los **reinicios de Common Lisp**.

Y ahí está el vínculo con esta clase: **una mónada de error y un sistema de condiciones atacan el
mismo problema por lados opuestos**. La mónada dice "el fallo es un valor que tienes que mirar"; el
sistema de condiciones dice "el fallo es una señal que alguien de arriba puede resolver, incluso
reparando el dato y siguiendo".

PL/I y Common Lisp son los dos lenguajes de esta página con la segunda opción, y son los dos que
tienen manejadores de alcance dinámico (clase 103). No es casualidad: **para que alguien de arriba
pueda decidir, el manejador tiene que estar activo hacia abajo**.

Es una idea que se perdió en el camino hacia `try/catch`, y que merece conocerse porque resuelve casos
—reintentar, sustituir, pedir al usuario— que un `catch` no puede.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
FUNC3 ; Funcional III -- clase 116
 read n
 kill opcional
 if n > 0 set opcional = n
 ; $data dice si la variable EXISTE: esa es la ausencia
 if $data(opcional) write "resultado=", opcional * 2, !
 else  write "resultado=nada", !
 quit
```

**Lo que esta clase enseña en M.** **M no tiene nulo**, y su forma de representar la ausencia es la
misma que la de Tcl llevada al extremo: **la variable no existe**.

```mumps
 kill opcional              ; ahora NO hay valor
 set opcional = 5            ; ahora sí
 if $data(opcional) ...       ; ¿existe?
```

Y **`$data`** (clase 094) es más fino de lo que un `Option` puede expresar, porque distingue cuatro
estados:

```mumps
 $data(v)     ; 0  = no existe
              ; 1  = tiene valor, sin hijos
              ; 10 = NO tiene valor pero SÍ tiene hijos
              ; 11 = tiene valor Y tiene hijos
```

Ese `10` —**un nodo que existe solo como rama**— no tiene equivalente en ningún `Option` de los
lenguajes modernos, y es lo que permite que la misma estructura sea árbol y diccionario a la vez.

Y **`$get`** es exactamente `getOrElse`:

```mumps
 set x = $get(v)              ; el valor, o "" si no existe
 set x = $get(v, 0)            ; el valor, o 0
 set x = $get(^PAC(id,"nom"), "desconocido")   ; también sobre globals
```

`$get` es de las funciones más usadas del lenguaje, y su existencia dice algo: **en M, preguntar por
un dato que puede no estar es tan común que tiene función propia**. En un historial clínico, la
mayoría de los campos están vacíos la mayoría de las veces.

Y aquí está la observación que cierra esta clase desde el lenguaje más viejo de la página: **el modelo
de M es disperso por diseño**. Un *global* con un millón de pacientes y trescientos campos posibles
**solo ocupa lo que realmente se rellenó**, y consultar un campo que no existe es normal, no un error.

Un `Option` es la respuesta de un lenguaje de tipos a un caso excepcional. **En M, la ausencia es el
caso normal**, y por eso está en las primitivas —`$data`, `$get`, `$order`— y no en un envoltorio.

Es una diferencia de modelo de datos, no de sofisticación: **quien guarda registros médicos vive en un
mundo donde casi todo falta**, y el lenguaje se diseñó para eso.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n opcional r |

n := stdin nextLine trimBoth asNumber.

opcional := n > 0 ifTrue: [ n ] ifFalse: [ nil ].

"ifNotNil: es el map; ifNil: es el getOrElse"
r := opcional ifNotNil: [ :v | v * 2 ].

Transcript
    show: 'resultado=', (r ifNil: [ 'nada' ] ifNotNil: [ :v | v printString ]);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene `nil`, y lo trata de la forma que le es
propia: **`nil` es un objeto**, instancia única de la clase `UndefinedObject`, y **responde a
mensajes**.

```smalltalk
nil class            "UndefinedObject"
nil isNil            "true"
nil printString      "'nil'"
```

De ahí sale la familia de mensajes que este programa usa y que son **exactamente las operaciones de
`Option`**:

```smalltalk
x ifNil: [ ... ]                          "Option.orElse"
x ifNotNil: [ :v | ... ]                   "Option.map"
x ifNil: [ ... ] ifNotNil: [ :v | ... ]     "fold"
x ifNil: [ 0 ]                               "getOrElse"
```

**`ifNotNil:` con un parámetro de bloque es el `map` de la mónada**, y está en la biblioteca desde hace
décadas, con ese nombre y esa forma. Swift copió la idea con `if let` y `?.`, y Kotlin con `?.let`.

Y como `nil` es un objeto que responde a mensajes, ocurre algo que sorprende: **llamar a un método
inexistente sobre `nil` no revienta el proceso**, dispara `doesNotUnderstand:` (clase 051) y **abre el
depurador sobre el objeto vivo**, con la pila intacta y la posibilidad de arreglar el método y
continuar.

El error de los mil millones de dólares, en Smalltalk, **es una conversación con el depurador**.

Y esta clase permite cerrar con lo que Smalltalk hace con los efectos, que es lo otro que da nombre a
la clase: **las excepciones de Smalltalk son objetos y son reanudables**.

```smalltalk
[ 1/0 ] on: ZeroDivide do: [ :e | e return: 0 ]      "devolver un valor en su lugar"
[ ... ] on: Warning do: [ :e | e resume: nil ]        "CONTINUAR donde se quedó"
[ ... ] on: Error do: [ :e | e retry ]                 "reintentar el bloque"
[ ... ] on: Error do: [ :e | e pass ]                   "pasarlo hacia arriba"
```

**`resume:` continúa la ejecución en el punto donde saltó la excepción**, con el valor que le des. Eso
es lo mismo que los reinicios de Common Lisp y el `onsource` de PL/I de esta misma página, y **no lo
tienen ni Java, ni C++, ni Python, ni Rust**.

Tres lenguajes de esta página —Smalltalk, Lisp y PL/I— comparten una idea que la industria dejó atrás:
**un fallo no tiene por qué desenrollar la pila**.

---

## Y de vuelta a la clase

Lo transferible: **una mónada es un envoltorio con dos operaciones —meter un valor y encadenar
transformaciones que devuelven envoltorios— y las usas todos los días sin llamarlas así**. `Option`
encadena cálculos que pueden faltar, `Result` los que pueden fallar, la lista los que dan varios
resultados, la promesa los que tardan. Lo que aportan no es teoría de categorías: es que **el caso
raro deja de ser un `if` que se puede olvidar y pasa a ser algo que el tipo te obliga a mirar**.

⏮️ [Volver a la clase 116](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
