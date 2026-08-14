# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 074

> [⬅️ Volver a la clase 074](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Elevar un número a una potencia, con el exponente **2 si no se indica**. El valor por defecto es una
de esas comodidades que parecen triviales hasta que se cuenta cuántos de estos doce lenguajes la
tienen: **cinco**. Los otros siete resuelven el problema de tres maneras distintas, y una de ellas
—la de Smalltalk— es tan limpia que hace innecesaria la característica.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **argumento ausente**, y estos lenguajes enseñan las cuatro respuestas
> posibles. **Valor por defecto en la declaración**: Ada, Lisp, Tcl, Pascal moderno y C++. **Argumento
> declarado opcional más una pregunta**: Fortran con `optional` y `present()`, RPG con `options(*nopass)`
> y `%parms`. **Nada, hay que comprobar**: COBOL, PL/I, M. Y **métodos distintos con nombres
> distintos**: Smalltalk.
>
> Esa última merece atención: cuando el nombre del método incluye sus argumentos, `pot:` y `pot:exp:`
> son dos métodos, y uno puede llamar al otro. **La sobrecarga por número de argumentos deja de existir
> como problema.**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea: `base` (exp por defecto 2) o `base exp` → stdout: `resultado=<base^exp>`
- **Regla:** `potencia(base, exp=2) = base^exp`

| stdin | esperado |
|---|---|
| `3` | `resultado=9` |
| `2 3` | `resultado=8` |
| `5` | `resultado=25` |

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
PROGRAM-ID. POTENCIA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-B   PIC X(20).
01  TXT-E   PIC X(20).
01  BASE-V  PIC S9(9)  COMP-3.
01  EXPO    PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  I       PIC 9(4)   COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TXT-E
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-B TXT-E

    MOVE FUNCTION NUMVAL(TXT-B) TO BASE-V

    IF TXT-E = SPACES
        MOVE 2 TO EXPO
    ELSE
        MOVE FUNCTION NUMVAL(TXT-E) TO EXPO
    END-IF

    MOVE 1 TO R
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > EXPO
        COMPUTE R = R * BASE-V
    END-PERFORM

    MOVE R TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene parámetros por defecto ni opcionales.** Un
`CALL` con menos argumentos de los que el programa espera es un error en ejecución, no un valor por
defecto.

La comprobación de este programa —`IF TXT-E = SPACES`— es el idioma real: **usar el valor "vacío"
como señal de ausencia**, que es exactamente el problema de los centinelas de la clase 053. Funciona
mientras "vacío" no sea un dato legítimo.

Cuando hace falta de verdad, COBOL tiene dos mecanismos, y ninguno es cómodo:

```cobol
*> 1) El programa llamado pregunta cuántos argumentos recibió
CALL "SUBPROG" USING A, B
...
*> en SUBPROG, con la extensión de IBM:
IF NUMBER-OF-CALL-PARAMETERS = 1 ...

*> 2) Un campo indicador explícito
CALL "SUBPROG" USING A, B, WS-B-PRESENTE
```

La segunda —pasar una bandera diciendo qué argumentos son válidos— es la que se ve en código real, y
es exactamente lo que hace RPG con `%parms` pero sin apoyo del lenguaje.

Y hay una razón histórica para esta ausencia: en COBOL, **la lista de parámetros es un contrato de
memoria**. `USING` pasa direcciones, y el programa llamado las mapea sobre su `LINKAGE SECTION`. No
hay un mecanismo que "rellene" un hueco, porque no hay quien lo rellene: el enlace es directo.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program potencia
   implicit none
   character(len=100) :: linea
   integer :: base, expo, ios

   read(*, '(A)') linea

   read(linea, *, iostat=ios) base, expo
   if (ios /= 0) then
      read(linea, *) base
      write(*, '(A,I0)') 'resultado=', pot(base)
   else
      write(*, '(A,I0)') 'resultado=', pot(base, expo)
   end if

contains

   pure function pot(b, e) result(r)
      integer, intent(in) :: b
      integer, intent(in), optional :: e     ! OPCIONAL, sin valor por defecto
      integer :: r, i, ee
      ee = 2
      if (present(e)) ee = e                 ! el defecto se escribe DENTRO
      r = 1
      do i = 1, ee
         r = r * b
      end do
   end function pot

end program potencia
```

**Lo que esta clase enseña en Fortran.** Fortran tiene **`optional`, pero no valores por defecto**, y
esa combinación es característica: el argumento puede faltar, y **el defecto se escribe dentro de la
función** con `present()`.

```fortran
integer, intent(in), optional :: e
...
if (present(e)) then ... else ... end if
```

Puede parecer un rodeo frente a `e = 2` en la firma, y tiene una ventaja concreta: **el defecto puede
depender de los otros argumentos**, cosa que un valor en la declaración no permite.

```fortran
if (present(tolerancia)) then
   tol = tolerancia
else
   tol = epsilon(x) * 100.0        ! depende del TIPO del otro argumento
end if
```

Y hay una regla que causa errores reales: **`present()` solo se puede llamar sobre el propio
parámetro**, y **usar un argumento opcional ausente es comportamiento indefinido**. Compilar con
`-fcheck=all` lo detecta.

Fortran combina además `optional` con los **argumentos por palabra clave** de la clase 075, y ahí es
donde la característica cobra sentido:

```fortran
call resolver(matriz, tolerancia=1e-9)     ! salto los intermedios
```

Con `optional` a secas, para pasar el quinto argumento habría que pasar los cuatro anteriores. Con
palabras clave, no. **Las dos características juntas son lo que hace usables las interfaces de
LAPACK**, que tienen rutinas de quince parámetros.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Potencia is

   --  El valor por defecto va EN LA FIRMA.
   function Pot (B : Integer; E : Integer := 2) return Integer is
      R : Integer := 1;
   begin
      for I in 1 .. E loop
         R := R * B;
      end loop;
      return R;
   end Pot;

   Linea      : String (1 .. 100);
   Ultimo     : Natural;
   Pos        : Positive := 1;
   Fin        : Positive;
   Base, Expo : Integer;
   Hay_Expo   : Boolean := False;
begin
   Get_Line (Linea, Ultimo);
   Get (Linea (Pos .. Ultimo), Base, Fin);
   Pos := Fin + 1;

   if Pos <= Ultimo then
      Get (Linea (Pos .. Ultimo), Expo, Fin);
      Hay_Expo := True;
   end if;

   Put ("resultado=");
   if Hay_Expo then
      Put (Pot (Base, Expo), Width => 1);
   else
      Put (Pot (Base), Width => 1);
   end if;
   New_Line;
end Potencia;
```

**Lo que esta clase enseña en Ada.** `E : Integer := 2` en la firma es el valor por defecto, y Ada lo
combina con la **asociación por nombre** de la clase 075 para conseguir algo que C++ no puede:
**omitir un parámetro intermedio**.

```ada
procedure Dibujar (X, Y : Integer; Color : Color_T := Negro;
                   Grosor : Positive := 1; Relleno : Boolean := False);

Dibujar (10, 20);                          --  todos por defecto
Dibujar (10, 20, Relleno => True);         --  ¡salto Color y Grosor!
Dibujar (X => 10, Y => 20, Grosor => 3);
```

En C++ los valores por defecto **solo pueden omitirse desde el final**: para pasar el quinto hay que
pasar los cuatro anteriores. En Ada, con nombres, no. Es la misma ventaja que Fortran obtiene con
`optional` más palabras clave, y la razón de que estas dos características se diseñen juntas.

Y hay un detalle de Ada que merece la pena: **el valor por defecto se evalúa en cada llamada**, en el
ámbito de la declaración. Así que puede ser una expresión, incluso una llamada a función:

```ada
procedure Registrar (Msg : String; Cuando : Time := Clock);   --  la hora ACTUAL
```

Compara con Python, donde el defecto se evalúa **una sola vez al definir** y `def f(x=[])` es el error
clásico. Ada, C++ y Ruby evalúan en cada llamada; Python y JavaScript (con `var`) no. Es una
diferencia que conviene comprobar en cada lenguaje nuevo.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Potencia;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function Pot(B: Integer; E: Integer = 2): Int64;
var
  I: Integer;
begin
  Result := 1;
  for I := 1 to E do
    Result := Result * B;
end;

var
  Linea: string;
  P: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);
  P := Pos(' ', Linea);

  if P = 0 then
    WriteLn('resultado=', IntToStr(Pot(StrToInt(Linea))))
  else
    WriteLn('resultado=', IntToStr(Pot(StrToInt(Copy(Linea, 1, P - 1)),
                                       StrToInt(Trim(Copy(Linea, P + 1, Length(Linea)))))));
end.
```

**Lo que esta clase enseña en Pascal.** **El Pascal ISO no tiene valores por defecto.** Los añadieron
Delphi 4 (1999) y Free Pascal, con la sintaxis `E: Integer = 2` de este programa.

Y llevan una restricción que conviene conocer: **el valor por defecto debe ser una constante conocida
al compilar**, no una expresión.

```pascal
function F(A: Integer = 10): Integer;              { correcto }
function G(A: Integer = Calcular): Integer;        { NO compila }
function H(const S: string = ''): Integer;         { correcto }
```

Es una restricción más estricta que la de Ada y C++, y viene del modelo de compilación en una sola
pasada: el valor se incrusta en el sitio de la llamada, así que tiene que ser un literal.

De ahí que el idioma clásico de Pascal para el argumento opcional sea la **sobrecarga**, disponible
desde Delphi 1:

```pascal
function Pot(B: Integer): Int64; overload;
function Pot(B, E: Integer): Int64; overload;
```

Dos funciones con el mismo nombre y distinta firma. `overload` es obligatorio en Object Pascal —a
diferencia de C++, donde la sobrecarga es implícita— y esa obligación es deliberada: **declara la
intención**, y evita que dos funciones colisionen por accidente al fusionar código.

Fíjate también en `Pos(' ', Linea)`, que devuelve la posición de la primera aparición o **0** si no
está. Es el mismo cero de la clase 053 haciendo de centinela: funciona porque las posiciones de
cadena en Pascal empiezan en 1.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun pot (b &optional (e 2))
  (expt b e))

(let* ((base (read))
       (expo (read *standard-input* nil :sin)))
  (if (eq expo :sin)
      (format t "resultado=~D~%" (pot base))
      (format t "resultado=~D~%" (pot base expo))))
```

**Lo que esta clase enseña en Common Lisp.** `&optional (e 2)` declara un parámetro opcional **con su
valor por defecto en la propia lambda-lista**, y Lisp añade dos refinamientos que casi nadie tiene.

El primero: **el valor por defecto puede usar los parámetros anteriores**.

```lisp
(defun rango (inicio &optional (fin (+ inicio 10)) (paso (if (> fin inicio) 1 -1)))
  ...)
```

`fin` depende de `inicio`, y `paso` depende de los dos. Se evalúan de izquierda a derecha, en cada
llamada. Es la ventaja que Fortran consigue escribiendo el defecto dentro del cuerpo, aquí obtenida
en la firma.

El segundo, y es el que resuelve un problema real: **la variable "¿lo pasaron?"**.

```lisp
(defun f (a &optional (b 0 b-dado))
  (if b-dado
      (format t "me pasaron b, y vale ~D" b)
      (format t "b no vino; uso el defecto")))
```

El tercer elemento de la lista —`b-dado`— es un booleano que dice si el argumento **se pasó
explícitamente**. Eso distingue "no lo pasó" de "pasó justo el valor por defecto", que son cosas
distintas y que en C++, Ada y Pascal no se pueden separar. Es exactamente el problema de la clase 053
aplicado a los parámetros.

Y `(expt b e)` es la exponenciación de Lisp, que con enteros da **resultados exactos sin límite**:
`(expt 2 1000)` devuelve el número completo.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc pot {base {expo 2}} {
    return [expr {$base ** $expo}]
}

gets stdin linea
set partes [split [string trim $linea]]

if {[llength $partes] == 1} {
    puts "resultado=[pot [lindex $partes 0]]"
} else {
    puts "resultado=[pot [lindex $partes 0] [lindex $partes 1]]"
}
```

**Lo que esta clase enseña en Tcl.** `{expo 2}` en la lista de parámetros declara el valor por
defecto, y la sintaxis revela cómo funciona: **la lista de parámetros de `proc` es una lista de
Tcl**, donde cada elemento es o bien un nombre, o bien una lista de dos elementos —nombre y defecto—.

```tcl
proc f {a {b 10} {c "hola"} args} { ... }
```

No hay sintaxis especial: es la estructura de datos normal del lenguaje, interpretada por `proc`. Por
eso se puede construir en ejecución:

```tcl
set params [list a [list b 10]]
proc dinamica $params { ... }        ;# la FIRMA se construye como un dato
```

Y como se vio en la clase 073, `info args` y `info default` permiten **inspeccionar la firma** de
cualquier procedimiento, incluidos los defectos. Eso es lo que usan los generadores de documentación
y los envoltorios automáticos.

Sobre la comprobación: Tcl **sí verifica la aridad**. Llamar `pot` sin argumentos da
`wrong # args: should be "pot base ?expo?"`, con los opcionales entre interrogaciones. Ese formato de
mensaje es una convención de todo el lenguaje y de sus bibliotecas.

Y `**` es el operador de exponenciación, disponible dentro de `expr` desde Tcl 8.5, con enteros de
precisión arbitraria detrás.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub pot {
    my ($base, $expo) = @_;
    $expo //= 2;                 # // : solo si NO ESTÁ DEFINIDO
    return $base ** $expo;
}

my $linea = <STDIN>;
chomp $linea;
my @partes = split ' ', $linea;

print "resultado=", pot(@partes), "\n";
```

**Lo que esta clase enseña en Perl.** `$expo //= 2` es el idioma clásico, y la elección del operador
es la lección: **`//=` asigna solo si el valor no está DEFINIDO**, mientras que `||=` lo haría también
si fuera falso.

```perl
$expo ||= 2;     # MAL: un exponente 0 se convertiría en 2
$expo //= 2;     # BIEN: solo si no vino
```

Es exactamente el problema de la clase 053 —distinguir "no hay valor" de "el valor es cero"— aplicado
a los parámetros, y es un error real: `pot(5, 0)` debería dar 1 y con `||=` daría 25.

Fíjate también en `pot(@partes)`: al pasar un array a una subrutina, **se aplana en `@_`**. Si
`@partes` tiene un elemento, la subrutina recibe uno; si tiene dos, dos. No hace falta comprobar
nada en el sitio de la llamada. Ese aplanamiento es una característica de Perl que sorprende y que
aquí resulta muy cómoda — aunque es también la razón de que pasar dos arrays a una función exija
referencias.

Y **Perl 5.36 permite el valor por defecto en la firma**, que es como se escribe hoy:

```perl
use v5.36;
sub pot ($base, $expo = 2) { return $base ** $expo }
sub log_msg ($msg, $nivel = 'info', @extra) { ... }
```

El defecto en una firma se evalúa **en cada llamada** y puede usar los parámetros anteriores, igual
que en Lisp: `sub rango ($ini, $fin = $ini + 10) { ... }`.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <sstream>
#include <string>

long long pot(int base, int expo = 2) {
    long long r = 1;
    for (int i = 0; i < expo; ++i) r *= base;
    return r;
}

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::istringstream iss(linea);
    int base{}, expo{};
    iss >> base;

    if (iss >> expo) {
        std::cout << "resultado=" << pot(base, expo) << '\n';
    } else {
        std::cout << "resultado=" << pot(base) << '\n';
    }
    return 0;
}
```

**Lo que esta clase enseña en C++.** Los argumentos por defecto de C++ tienen **dos restricciones
importantes** que conviene tener claras.

La primera: **solo se pueden omitir desde el final**. No hay forma de pasar el tercero sin pasar el
segundo, porque C++ no tiene argumentos nombrados —clase 075—.

La segunda, y es la que causa errores: **el valor por defecto pertenece a la DECLARACIÓN, no a la
función**, y si la declaración está en una cabecera, **cada unidad de traducción puede ver un defecto
distinto**.

```cpp
// cabecera.h
void f(int x = 10);

// otro.cpp
void f(int x = 20);      // legal en OTRO ámbito: dos defectos para la misma función
```

Por eso la regla es: **el defecto se escribe una sola vez, en la declaración de la cabecera, y nunca
en la definición**.

Y hay un aviso de fondo: **los argumentos por defecto no participan en el polimorfismo**. Si una clase
derivada redefine un método virtual con otro defecto, **se usa el defecto del tipo ESTÁTICO** y el
cuerpo del dinámico:

```cpp
struct Base    { virtual void f(int x = 1) { ... } };
struct Derivada: Base { void f(int x = 2) override { ... } };

Base* p = new Derivada;
p->f();      // llama a Derivada::f... ¡con x = 1!
```

Es un comportamiento sorprendente, está en todas las listas de trampas de C++, y la recomendación de
las *Core Guidelines* es tajante: **no pongas argumentos por defecto en funciones virtuales**.

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

dcl-pi POTENCIA;
  base int(10) const;
  expo int(10) const options(*nopass);   // OPCIONAL: se puede no pasar
end-pi;

dcl-s e      int(10);
dcl-s r      int(20) inz(1);
dcl-s i      int(10);
dcl-s salida char(40);

// %parms dice CUÁNTOS argumentos llegaron de verdad.
if %parms >= 2;
  e = expo;
else;
  e = 2;
endif;

for i = 1 to e;
  r *= base;
endfor;

salida = 'resultado=' + %char(r);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG resuelve esta clase con dos piezas que van siempre juntas:
**`options(*nopass)`** en la firma, que declara que el argumento puede no venir, y **`%parms`**, que
dice cuántos llegaron de verdad.

```rpgle
dcl-pi *n;
  a int(10) const;
  b int(10) const options(*nopass);
  c int(10) const options(*nopass);   // los *nopass van SIEMPRE al final
end-pi;

if %parms >= 3; ... endif;
```

Los opcionales tienen que ir al final, como en C++, y por la misma razón: sin nombres, la posición es
lo único que identifica al argumento.

Y hay una trampa de seguridad que conviene conocer, porque es específica de RPG: **acceder a un
parámetro `*nopass` que no se pasó es leer memoria ajena**. No hay comprobación automática; el
programa lee lo que haya en esa dirección. Es tan peligroso como leer un puntero no inicializado en
C, y la única protección es comprobar `%parms` **antes**.

RPG tiene además `options(*omit)`, que permite pasar `*omit` explícitamente en una posición
intermedia:

```rpgle
dcl-pi *n;
  a pointer options(*omit);
end-pi;
...
callp proceso(*omit : otro);       // el primero se omite EXPLÍCITAMENTE
if %addr(a) <> *null; ... endif;
```

Con `*omit` sí se pueden saltar posiciones intermedias, y la comprobación es sobre la dirección. Es
la versión de RPG del argumento nombrado, y es tan incómoda como suena.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 potencia: procedure options(main);

    declare linea character(80) varying;
    declare (base_v, expo, r, i) fixed binary(31);
    declare p fixed binary(31);

    get edit (linea) (a(80));
    linea = trim(linea);

    p = index(linea, ' ');
    if p = 0 then do;
       base_v = linea;
       expo = 2;                      /* el defecto se escribe A MANO */
    end;
    else do;
       base_v = substr(linea, 1, p - 1);
       expo = substr(linea, p + 1);
    end;

    r = 1;
    do i = 1 to expo;
       r = r * base_v;
    end;

    put skip list ('resultado=' || trim(char(r)));

 end potencia;
```

**Lo que esta clase enseña en PL/I.** **PL/I no tiene parámetros por defecto ni opcionales**, y es
llamativo en un lenguaje que tenía casi todo lo demás. La comprobación se escribe a mano, como en
COBOL.

Lo que sí ofrece, y es su respuesta a esta clase, es el atributo **`generic`**, que selecciona entre
varios procedimientos **según el número y el tipo de los argumentos**:

```pli
declare pot generic (pot2 when (fixed binary),
                     potn when (fixed binary, fixed binary));

x = pot(3);        /* llama a pot2 */
y = pot(2, 3);     /* llama a potn */
```

Es **sobrecarga por aridad y por tipo**, declarada explícitamente en una tabla en lugar de deducida
por el compilador. Funciona igual que el `overload` de Object Pascal y que la sobrecarga implícita de
C++, con la diferencia de que aquí las alternativas están **enumeradas en un solo sitio** y se pueden
leer.

Esa explicitud tiene una ventaja que se aprecia al mantener código: para saber a qué se llama con
`pot(3)`, se lee la declaración `generic`, no se reconstruye mentalmente el algoritmo de resolución de
sobrecarga del compilador.

Y `index(cadena, subcadena)` de este programa es la función de búsqueda de PL/I —devuelve 0 si no
encuentra—, la misma que `Pos` en Pascal y `%scan` en RPG.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
POT ; Parametros opcionales -- clase 074
 read linea
 set base = $piece(linea, " ", 1)
 set expo = $piece(linea, " ", 2)
 if expo = "" write "resultado=", $$pot(base), ! quit
 write "resultado=", $$pot(base, expo), !
 quit
 ;
pot(b, e) ; b elevado a e (e por defecto 2)
 new i, r
 set e = $get(e, 2)          ; $GET con valor por defecto: el idioma de M
 set r = 1
 for i = 1:1:e set r = r * b
 quit r
```

**Lo que esta clase enseña en M.** **`$get(variable, valorPorDefecto)`** es la respuesta de M, y es
más elegante de lo que parece: en M, **llamar a una función con menos argumentos de los declarados es
perfectamente legal**, y los parámetros que faltan quedan simplemente **sin definir**.

```mumps
 set x = $$pot(3)          ; e queda INDEFINIDA dentro de pot
 set e = $get(e, 2)        ; y $get le da el valor por defecto
```

No hay que declarar nada opcional ni preguntar cuántos argumentos llegaron: **la ausencia es un
estado del dato**, y `$data`/`$get` son las funciones que ya se vieron en la clase 053.

Esa uniformidad es notable: el mismo mecanismo que distingue "esta variable no existe" de "vale
cero" sirve para "este parámetro no se pasó". En los demás lenguajes de esta página hacen falta dos
mecanismos distintos —`present()` y `$data`, `%parms` y `%nullind`—.

Y M lleva la idea más lejos: **también se puede llamar con MÁS argumentos de los declarados**, y los
sobrantes se ignoran. Es tan permisivo que un error de aridad no da ningún aviso, lo que enlaza con
todo lo dicho sobre M: máxima flexibilidad, cero comprobación.

`new i, r` al principio de la función es lo de la clase 069: sin él, las variables temporales serían
globales y la recursión se rompería.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes base expo |

partes := stdin nextLine substrings.
base := partes first asNumber.
expo := partes size > 1
    ifTrue:  [ partes second asNumber ]
    ifFalse: [ 2 ].

Transcript show: 'resultado=', (base raisedTo: expo) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene parámetros por defecto, y no los
necesita.** Como el nombre del método incluye sus argumentos —clase 073—, dos aridades distintas son
**dos métodos con nombres distintos**, y uno delega en el otro:

```smalltalk
Number >> potencia
    ^self potencia: 2                 "el defecto: delega"

Number >> potencia: exponente
    ^self raisedTo: exponente
```

`potencia` y `potencia:` son selectores diferentes. No compiten, no hay sobrecarga que resolver, y el
"valor por defecto" es simplemente **el argumento que el método corto le pasa al largo**.

Ese patrón recorre toda la biblioteca y es reconocible al instante:

```smalltalk
coleccion detect: unBloque
coleccion detect: unBloque ifNone: otroBloque

diccionario at: clave
diccionario at: clave ifAbsent: unBloque

cadena indexOf: caracter
cadena indexOf: caracter startingAt: indice
cadena indexOf: caracter startingAt: indice ifAbsent: unBloque
```

Cada versión larga añade información y la corta delega con un valor razonable. Es más verboso de
declarar y **mucho más legible en el sitio de la llamada**, porque el nombre dice exactamente qué
hace esa variante.

Y tiene una ventaja de mantenimiento real: cambiar el valor por defecto es editar **un método**, no
recompilar a todos los que llamaban con el defecto — que es exactamente el problema de C++ con los
defectos en cabeceras.

---

## Y de vuelta a la clase

Lo transferible es una advertencia sobre los valores por defecto: **en la mayoría de los lenguajes se
evalúan en el sitio de la LLAMADA, pero no en todos**. En C++ y Ada, el valor por defecto se evalúa en
cada llamada; en Python —el caso famoso— se evalúa **una sola vez, al definir la función**, y por eso
un valor por defecto mutable es un error clásico. Antes de poner un valor por defecto que no sea una
constante, comprueba cuándo se evalúa en tu lenguaje.

⏮️ [Volver a la clase 074](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
