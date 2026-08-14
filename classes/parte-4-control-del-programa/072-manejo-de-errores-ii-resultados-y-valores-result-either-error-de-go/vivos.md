# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 072

> [⬅️ Volver a la clase 072](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

El mismo problema que la clase anterior, con la estrategia opuesta: **el error no interrumpe nada, se
devuelve como un valor**. Es el modelo de Go, de Rust y de `std::expected`, y la revolución de la
última década en manejo de errores. Y también, casi exactamente, **lo que COBOL lleva haciendo desde
1968 con el `FILE STATUS`**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **el error como dato en lugar de como salto**, y estos lenguajes lo enseñan
> porque **es su modelo nativo**. COBOL comprueba un código de dos caracteres después de cada operación
> de fichero; Fortran devuelve `iostat`; Ada usa parámetros `out`; M devuelve un valor de estado. Ninguno
> de ellos "adoptó" el modelo de Go: **es el modelo del que Go partió**.
>
> Y Lisp aporta la variante más elegante: **valores múltiples**, donde el segundo valor lleva el error
> y **ignorarlo es gratis** — sin `_` obligatorio, sin construir una tupla, sin envolver nada.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `ok=<a/b entera>` o `err=division` si b es 0
- **Regla:** `si b != 0 → Ok(a/b); si b == 0 → Err(division)`

| stdin | esperado |
|---|---|
| `10 2` | `ok=5` |
| `7 0` | `err=division` |
| `8 4` | `ok=2` |

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
PROGRAM-ID. DIVVAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  R       PIC S9(9) COMP-3.
01  ESTADO  PIC 9.
    88  TODO-BIEN  VALUE 0.
    88  ERR-DIV    VALUE 1.
01  ED-R    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    PERFORM DIVIDIR

    IF ERR-DIV
        DISPLAY "err=division"
    ELSE
        MOVE R TO ED-R
        DISPLAY "ok=" FUNCTION TRIM(ED-R)
    END-IF

    STOP RUN.

DIVIDIR.
    IF B = 0
        SET ERR-DIV TO TRUE
        MOVE 0 TO R
    ELSE
        SET TODO-BIEN TO TRUE
        DIVIDE A BY B GIVING R
    END-IF.
```

**Lo que esta clase enseña en COBOL.** **Este es el modelo nativo de COBOL, y es de 1968.** El
`FILE STATUS` es exactamente "errores como valores", con una convención que sigue vigente:

```cobol
SELECT CLIENTES ASSIGN TO ENTRADA
    FILE STATUS IS WS-ESTADO.

01  WS-ESTADO  PIC XX.
    88  OK              VALUE "00".
    88  FIN-FICHERO     VALUE "10".
    88  NO-ENCONTRADO   VALUE "23".
    88  DUPLICADO       VALUE "22".

READ CLIENTES
EVALUATE TRUE
    WHEN OK             PERFORM PROCESAR
    WHEN FIN-FICHERO    SET TERMINADO TO TRUE
    WHEN NO-ENCONTRADO  PERFORM AVISAR
    WHEN OTHER          PERFORM ERROR-GRAVE
END-EVALUATE
```

Un **código de dos caracteres** después de cada operación, comprobado con `EVALUATE`. Compáralo con
`if err != nil` de Go: es la misma disciplina, con nombres de condición en lugar de un tipo de error,
y **cincuenta años antes**.

Y COBOL tiene el mismo problema que Go: **nadie te obliga a comprobarlo**. Un `READ` cuyo estado no
se mira es un error silencioso, y las guías de estilo COBOL llevan décadas insistiendo en que se
compruebe siempre. Es exactamente el mismo debate que hoy se tiene sobre Go y su `err`.

La diferencia con la clase anterior es de reparto de responsabilidad: `ON SIZE ERROR` obliga a decidir
en el sitio; `FILE STATUS` deja el resultado disponible y confía en que lo mires.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program divval
   implicit none
   integer :: a, b, r, estado

   read(*, *) a, b
   call dividir(a, b, r, estado)

   if (estado /= 0) then
      write(*, '(A)') 'err=division'
   else
      write(*, '(A,I0)') 'ok=', r
   end if

contains

   subroutine dividir(x, y, res, stat)
      integer, intent(in)  :: x, y
      integer, intent(out) :: res, stat
      if (y == 0) then
         res  = 0
         stat = 1
      else
         res  = x / y
         stat = 0
      end if
   end subroutine dividir

end program divval
```

**Lo que esta clase enseña en Fortran.** Este **es** el modelo de Fortran, y no tiene alternativa: sin
excepciones, un error solo puede viajar como dato.

La convención del lenguaje está estandarizada y es muy uniforme —el argumento se llama `stat` o
`iostat`, y siempre vale **cero si todo fue bien**:

```fortran
read(u, *, iostat=ios, iomsg=msg) v
allocate(v(n), stat=err, errmsg=msg)
deallocate(v, stat=err)
close(u, iostat=ios)
```

Y hay un detalle de diseño que Fortran hace mejor que Go y que conviene señalar: **el argumento de
estado es OPCIONAL, y su ausencia significa "aborta"**.

```fortran
read(u, *) v                    ! si falla, el programa TERMINA
read(u, *, iostat=ios) v        ! si falla, me lo dices y yo decido
```

Esa elección por llamada resuelve la queja más común contra los errores como valores —que obligan a
escribir `if err != nil` incluso cuando no vas a hacer nada útil con él—. En Fortran, si no vas a
manejarlo, **no pides el código y el programa falla ruidosamente**, que suele ser lo correcto.

Es una tercera vía entre la excepción y el valor: **el error es un valor si lo pides, y una parada si
no**. Rust hace algo parecido con `unwrap()`, pero al revés: allí hay que escribir algo para que
falle.

`intent(in)` e `intent(out)` en los parámetros son obligatorios en código moderno, y el compilador
comprueba que un `out` se asigne antes de salir.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Divval is

   procedure Dividir (A, B : Integer; R : out Integer; Ok : out Boolean) is
   begin
      if B = 0 then
         R  := 0;
         Ok := False;
      else
         R  := A / B;
         Ok := True;
      end if;
   end Dividir;

   A, B, R : Integer;
   Ok      : Boolean;
begin
   Get (A);
   Get (B);
   Dividir (A, B, R, Ok);

   if Ok then
      Put ("ok="); Put (R, Width => 1); New_Line;
   else
      Put_Line ("err=division");
   end if;
end Divval;
```

**Lo que esta clase enseña en Ada.** Los **parámetros `out`** son el mecanismo de Ada, y tienen una
propiedad que casi ningún lenguaje comparte: **el compilador comprueba que se asignen antes de salir
del procedimiento**, y avisa si se leen antes de asignarlos.

Ada distingue tres modos, y escribirlos es obligatorio en código serio:

| Modo | Significado |
|---|---|
| `in` | Solo lectura — es el valor por defecto |
| `out` | Solo escritura: el valor de entrada no existe |
| `in out` | Se lee y se modifica |

Esa distinción está **en la firma**, así que quien llama sabe qué se va a modificar sin leer el
cuerpo. En C hay que mirar si el parámetro es un puntero y confiar; en C++ ayuda el `const&`, pero un
`T&` no distingue si se lee o se escribe.

Y en sistemas críticos, este modelo **se prefiere a las excepciones**, por la razón de la clase 071:
el tiempo de propagación de una excepción es difícil de acotar, y el `if` sobre un booleano es
predecible.

Ada tiene además una variante que va más allá y que es lo más parecido a Rust de esta página: los
**contratos**.

```ada
procedure Dividir (A, B : Integer; R : out Integer)
  with Pre => B /= 0;      --  el error NO PUEDE OCURRIR: es responsabilidad del que llama
```

Con SPARK, esa precondición **se demuestra estáticamente** en todas las llamadas del programa. No hay
que devolver un error porque **se ha probado que la situación es imposible**. Es el nivel al que
aspira el manejo de errores cuando el fallo no es una opción.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Divval;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function TryDividir(A, B: Integer; out R: Integer): Boolean;
begin
  if B = 0 then
  begin
    R := 0;
    Result := False;
  end
  else
  begin
    R := A div B;
    Result := True;
  end;
end;

var
  A, B, R: Integer;

begin
  Read(A, B);

  if TryDividir(A, B, R) then
    WriteLn('ok=', IntToStr(R))
  else
    WriteLn('err=division');
end.
```

**Lo que esta clase enseña en Pascal.** El prefijo **`Try`** de `TryDividir` no es una elección
arbitraria: es una **convención establecida de la biblioteca de Delphi y Free Pascal**, y merece
conocerse porque resuelve muy bien el problema de esta clase.

La biblioteca ofrece cada conversión en **tres variantes**:

```pascal
StrToInt('42')              { lanza EConvertError si falla }
StrToIntDef('x', 0)         { devuelve un valor por defecto }
TryStrToInt('x', N)         { devuelve False y no toca N  <- errores como valores }
```

Las tres existen porque **las tres situaciones son legítimas**: si el dato viene de tu propio código y
un fallo indica un bug, quieres la excepción; si viene de una configuración con valor por defecto
razonable, quieres `Def`; y si viene de un usuario y hay que reaccionar, quieres `Try`.

Que la biblioteca ofrezca las tres, con nombres sistemáticos, es una lección de diseño de API mejor
que la de casi cualquier lenguaje moderno — donde normalmente hay una sola forma y el resto se
construye a mano.

Y `out` en Pascal significa lo mismo que en Ada: **el valor de entrada no importa** y el compilador lo
sabe. Se distingue de `var` (que es `in out`) y del paso por valor. Es la misma tríada, con otros
nombres.

Delphi moderno añadió además genéricos, con los que la comunidad ha construido tipos `TResult<T>` y
`TOption<T>` al estilo de Rust — pero sin comprobación obligatoria del compilador, así que son una
convención más.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun dividir (a b)
  (if (zerop b)
      (values nil :division)
      (values (truncate a b) nil)))

(let* ((a (read))
       (b (read)))
  (multiple-value-bind (r err) (dividir a b)
    (if err
        (format t "err=division~%")
        (format t "ok=~D~%" r))))
```

**Lo que esta clase enseña en Common Lisp.** Los **valores múltiples** son la aportación de Lisp a
esta clase, y son mejores que la tupla de Go y que el `Result` de Rust en un aspecto concreto:
**ignorarlos es gratis**.

```lisp
(dividir 10 2)                                  ; en contexto normal, solo el PRIMERO
(multiple-value-bind (r err) (dividir 10 0) ...)  ; los dos, si los quieres
(multiple-value-list (dividir 10 2))            ; como lista, si te hace falta
(nth-value 1 (dividir 10 0))                    ; solo el segundo
```

No se construye ninguna estructura. Si el llamante no pide el segundo valor, **no existe coste**: no
hay tupla que asignar ni objeto que descartar. En Go hay que escribir `_` para ignorar el error; en
Rust hay que hacer algo con el `Result` o el compilador avisa.

El estándar usa este mecanismo por todas partes, y los ejemplos son elocuentes:

```lisp
(gethash clave tabla)      ; => valor, ¿estaba?   (la clase 053)
(truncate 17 5)            ; => 3, 2             (cociente y resto, clase 049)
(floor -7 3)               ; => -3, 2
(parse-integer "42x" :junk-allowed t)  ; => 42, 2  (valor y dónde paró)
(read-line f nil)          ; => línea, ¿fue por EOF?
(round 2.5)                ; => 2, 0.5
```

En todos, **el primer valor es lo que casi siempre quieres y el segundo es la información
adicional**. Esa asimetría es el diseño: el caso común es corto, y el caso completo está disponible.

La contrapartida honesta: **el compilador no obliga a mirar el segundo valor**. Es el mismo problema
que COBOL con `FILE STATUS` y Go con `err`. Solo Rust lo resolvió, y a costa de obligar siempre.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc dividir {a b} {
    if {$b == 0} {
        return [list 0 "division"]
    }
    return [list [expr {$a / $b}] ""]
}

gets stdin linea
lassign [split [string trim $linea]] a b
lassign [dividir $a $b] r err

if {$err ne ""} {
    puts "err=$err"
} else {
    puts "ok=$r"
}
```

**Lo que esta clase enseña en Tcl.** Devolver una **lista de dos elementos** —resultado y error— es el
idioma directo, y `lassign` la desempaqueta en una línea. Es exactamente la tupla de Go, construida
con las piezas normales del lenguaje.

Pero lo interesante es que **Tcl ya tiene errores como valores integrados**, y es `catch` de la clase
anterior:

```tcl
set codigo [catch { operacion } resultado opciones]
```

`catch` **devuelve un número**: 0 si fue bien, 1 si hubo error, y 2, 3 o 4 para `return`, `break` y
`continue`. El resultado o el mensaje van a la segunda variable, y el diccionario de opciones a la
tercera.

Es decir: en Tcl **la excepción y el valor de error son el mismo mecanismo visto de dos maneras**. Un
error se propaga si nadie lo captura, y se convierte en un valor en cuanto alguien pone `catch`. No
hay dos modelos que elegir.

El diccionario de opciones lleva la información estructurada:

```tcl
catch { error "fallo" "" {BANCO SALDO 42} } msg opciones
dict get $opciones -errorcode      ;# {BANCO SALDO 42}
dict get $opciones -errorinfo      ;# la pila
return -options $opciones $msg     ;# RE-LANZAR conservándolo todo
```

Ese último idioma —`return -options` para relanzar sin perder la pila original— resuelve un problema
que en Java exige `throw e;` con cuidado y en Python el `raise ... from ...`. En Tcl es pasar un
diccionario.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub dividir {
    my ($x, $y) = @_;
    return (undef, 'division') if $y == 0;
    return (int($x / $y), undef);
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

my ($r, $err) = dividir($p, $q);

if (defined $err) {
    print "err=$err\n";
} else {
    print "ok=$r\n";
}
```

**Lo que esta clase enseña en Perl.** Devolver una lista de dos elementos es natural porque **las
subrutinas de Perl devuelven listas por defecto**, sin necesidad de construir una tupla ni un objeto.

Y Perl tiene una capacidad que ningún otro lenguaje de esta página comparte: **una función puede saber
en qué contexto la están llamando**, y devolver cosas distintas.

```perl
sub dividir {
    my ($x, $y) = @_;
    return wantarray ? (undef, 'division') : undef  if $y == 0;
    my $r = int($x / $y);
    return wantarray ? ($r, undef) : $r;
}

my $r = dividir(10, 2);              # contexto ESCALAR: solo el resultado
my ($r, $e) = dividir(10, 0);        # contexto de LISTA: resultado y error
```

`wantarray` devuelve verdadero en contexto de lista, falso en contexto escalar y `undef` si el valor
se descarta. Con eso se consigue el mismo efecto que los valores múltiples de Lisp: **el caso común es
corto y el completo está disponible**, sin coste para quien no lo pide.

El modelo clásico de Unix también está presente y es el que usan las funciones del sistema:

```perl
open(my $fh, '<', $f) or die "no puedo: $!";   # falso + $! con el motivo
```

Devolver **falso** y dejar el motivo en la variable global `$!` es el modelo de `errno` de C, y en
Perl convive con las excepciones de la clase 071 y con las listas de este programa. Tres modelos a la
vez, que es muy TMTOWTDI y también una fuente de inconsistencia entre bibliotecas.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <optional>

std::optional<int> dividir(int a, int b) {
    if (b == 0) return std::nullopt;
    return a / b;
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    if (const auto r = dividir(a, b)) {
        std::cout << "ok=" << *r << '\n';
    } else {
        std::cout << "err=division\n";
    }
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::optional<int>` (C++17) expresa "puede que no haya
resultado", y `if (const auto r = ...)` combina la llamada, la declaración y la comprobación en una
línea. Es el mismo `if err != nil` de Go, con el error dentro del tipo en lugar de al lado.

Lo que le falta a `optional` es **decir por qué falló**, y eso llegó con **C++23**:

```cpp
enum class ErrorDiv { division_por_cero };

std::expected<int, ErrorDiv> dividir(int a, int b) {
    if (b == 0) return std::unexpected(ErrorDiv::division_por_cero);
    return a / b;
}

auto r = dividir(a, b);
if (r) { usar(*r); } else { informar(r.error()); }
```

`std::expected<T, E>` es literalmente el `Result<T, E>` de Rust, adoptado en 2023. Y trae las
operaciones **monádicas** que permiten encadenar sin anidar `if`:

```cpp
auto salida = dividir(a, b)
                .and_then(validar)
                .transform(formatear)
                .value_or("desconocido");
```

Y hay una nota histórica que cierra esta clase: **C++ ya tuvo un modelo de errores como valores y lo
descartó**. `std::error_code` y `std::system_error` (C++11) ofrecían las dos vías, y la biblioteca de
sistema de archivos las expone en pares —`fs::remove(p)` lanza, `fs::remove(p, ec)` devuelve—.

Que un lenguaje con excepciones de treinta años haya añadido `expected` no es que las excepciones
fueran un error: es que **cada modelo sirve para una clase distinta de fallo**. El fallo esperable
—fichero que no está, entrada mal formada— es un valor; el inesperado —memoria agotada, invariante
roto— es una excepción.

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

dcl-pi DIVVAL;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s r      int(10);
dcl-s estado int(10);
dcl-s salida char(40);

if b = 0;
  estado = 1;
  r = 0;
else;
  estado = 0;
  r = %div(a : b);
endif;

if estado <> 0;
  salida = 'err=division';
else;
  salida = 'ok=' + %char(r);
endif;

dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Este es el modelo nativo de la plataforma, y en IBM i tiene una
forma muy reconocible: **funciones incorporadas que consultan el resultado de la última operación**.

```rpgle
chain (clave) CLIENTES;
if not %found(CLIENTES);       // ¿encontró el registro?
  ...
endif;
if %error;                      // ¿hubo un error de verdad?
  ...
endif;

read CLIENTES;
dow not %eof(CLIENTES);        // ¿fin de fichero?
```

`%found`, `%eof`, `%error`, `%status` y `%equal` **no reciben el resultado como valor de retorno**:
consultan el **estado de la última operación** sobre ese fichero. Es el modelo de `errno` de C, con
funciones en lugar de una variable global.

Tiene la ventaja de que la operación se lee limpia —`chain` no devuelve nada— y el inconveniente
clásico: **hay que preguntar antes de hacer otra cosa**, porque la siguiente operación pisa el estado.

Y RPG tiene una tercera vía, la que se usa cuando el error tiene que cruzar módulos: la **estructura
de datos de estado del programa**, declarada con `psds`, que expone el código de error, el nombre del
programa, la sentencia que falló y la hora. Es introspección del fallo sin excepciones.

En la práctica, un RPG moderno mezcla los tres: `%found`/`%error` para la E/S, `monitor` de la clase
071 para lo excepcional, y códigos de retorno propios entre subprocedimientos.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 divval: procedure options(main);

    declare (a, b, r) fixed binary(31);
    declare estado    fixed binary(31);

    get list (a, b);
    call dividir(a, b, r, estado);

    if estado ^= 0 then
       put skip list ('err=division');
    else
       put skip list ('ok=' || trim(char(r)));

 dividir: procedure (x, y, res, stat);
    declare (x, y) fixed binary(31);
    declare (res, stat) fixed binary(31);
    if y = 0 then do;
       res = 0;
       stat = 1;
       return;
    end;
    res = divide(x, y, 31);
    stat = 0;
 end dividir;

 end divval;
```

**Lo que esta clase enseña en PL/I.** PL/I tiene los dos modelos —las condiciones `ON` de la clase 071
y los códigos de estado de este programa— y su biblioteca los combina de una forma que conviene
conocer: **la condición ocurre igualmente, pero puedes consultarla como dato**.

```pli
on error begin;
   put skip list ('código: ' || oncode());       /* NÚMERO del error */
   put skip list ('en: '     || onloc());        /* dónde ocurrió */
   put skip list ('dato: '   || onsource());     /* el valor que falló */
end;
```

`oncode()` devuelve el código numérico de la condición activa, y con él el manejador puede decidir. Es
introspección del error **dentro** del mecanismo de excepciones — algo que en Java se consigue con
`instanceof` sobre la jerarquía de clases y en Go directamente comprobando el valor.

Y para la E/S, PL/I usa códigos como todos los de esta página:

```pli
declare f file record input;
on undefinedfile(f) ...
on endfile(f) ...
read file(f) into(registro);
```

Fíjate en que las condiciones se declaran **por fichero**, igual que las DECLARATIVES de COBOL. Es el
patrón de la época: cada recurso lleva su manejador.

Y hay una decisión de diseño que PL/I hizo y que conviene señalar: **algunas condiciones están
desactivadas por defecto por rendimiento**, y hay que encenderlas.

```pli
(subscriptrange, stringrange): procedure options(main);   /* prefijos de condición */
```

`SUBSCRIPTRANGE` comprueba los índices de array y **está apagada salvo que la pidas**, porque cuesta.
Es exactamente la misma decisión que `{$R+}` en Pascal y `-fcheck=bounds` en Fortran: la seguridad
disponible, y desactivada por defecto.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DIVVAL ; Errores como valores -- clase 072
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set res = $$dividir(a, b)
 if $piece(res, "^", 1) = "err" write "err=division",! quit
 write "ok=", $piece(res, "^", 2), !
 quit
 ;
dividir(x, y) ; devuelve "ok^valor" o "err^0"
 quit:y=0 "err^0"
 quit "ok^" _ (x\y)
```

**Lo que esta clase enseña en M.** Devolver **`"ok^valor"` o `"err^0"`** —una cadena con delimitador—
es el idioma real de M para los resultados compuestos, y es coherente con todo lo visto en las clases
048 y 065: **la cadena delimitada es la estructura de datos ligera del lenguaje**.

No hay tuplas, no hay registros de retorno y no hay tipos suma. Hay una cadena con `^` en medio, y
`$piece` para leerla. Es exactamente lo mismo que devolver `(valor, error)` en Go, con la diferencia
de que aquí no hay nada que declarar y la comprobación es textual.

Y en los sistemas M de verdad, este patrón está estandarizado por el marco de trabajo. En **VistA**,
la convención de FileMan es devolver el error en un array con estructura fija:

```mumps
 do UPDATE^DIE(.FDA, , , .ERR)
 if $data(ERR) do        ; el array de errores tiene contenido
 . write ERR("DIERR", 1, "TEXT", 1), !
```

Un **array local con subíndices convenidos** que el llamante inspecciona con `$data`. Es la clase 053
aplicada al manejo de errores: no hay `null`, hay un nodo que existe o no existe.

Que un sistema de la escala de VistA —millones de líneas, décadas de mantenimiento— funcione con esta
convención dice algo importante para cerrar la Parte 4: **la disciplina del equipo puede sustituir a
las garantías del lenguaje, y funciona… mientras la disciplina se mantenga**. Ese es exactamente el
argumento que Rust vino a resolver poniendo la comprobación en el compilador.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b r |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

r := b = 0 ifTrue: [ nil ] ifFalse: [ a // b ].

Transcript
    show: (r ifNil: [ 'err=division' ] ifNotNil: [ :v | 'ok=', v printString ]);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Devolver `nil` y comprobarlo con `ifNil:ifNotNil:` es el
modelo directo, y es la clase 053 aplicada aquí. Pero la respuesta idiomática de Smalltalk a esta
clase es otra, y es una de las mejores ideas de la biblioteca: **pasar un bloque para el caso de
fallo**.

```smalltalk
diccionario at: clave ifAbsent: [ 0 ]
coleccion detect: [ :x | ... ] ifNone: [ nil ]
coleccion first ifEmpty: [ 'vacía' ]
numero / cero ifError: [ 0 ]
```

El patrón **`...ifAusente:`** recorre toda la biblioteca, y resuelve el problema de esta clase sin
excepciones, sin códigos de estado y sin tipos suma: **el llamante entrega, en el sitio de la llamada,
qué hacer si no se puede**.

Es más expresivo que devolver `nil` por tres motivos. Primero, **el bloque solo se evalúa si hace
falta**, así que el valor por defecto puede ser caro de calcular. Segundo, puede hacer cualquier cosa
—registrar, lanzar, devolver otro valor— no solo aportar un sustituto. Y tercero, **no hay que
comprobar nada después**: el resultado ya es válido.

Y para la operación sin bloque, la biblioteca ofrece las dos variantes:

```smalltalk
diccionario at: clave                    "lanza si no está"
diccionario at: clave ifAbsent: [ 0 ]    "devuelve el valor por defecto"
```

Es la misma tríada de Delphi —lanzar, valor por defecto, comprobar— que apareció en la ficha de
Pascal, resuelta con bloques en lugar de con tres nombres de función. En un lenguaje donde pasar
código es gratis, la API se diseña así.

---

## Y de vuelta a la clase

La comparación que cierra la Parte 4: **una excepción es difícil de ignorar y fácil de olvidar
manejar; un valor de error es fácil de ignorar y difícil de olvidar que existe**, porque está en la
firma. Ninguno de los dos modelos gana: por eso Rust puso el error en el tipo **y** obligó a
tratarlo con `#[must_use]`, y por eso C++23 añadió `std::expected` sin quitar las excepciones.

Lo que sí es cierto es que este modelo, presentado como novedad en 2012, tiene sesenta años de
producción detrás en los lenguajes de esta página. Conviene saberlo antes de creer que algo se acaba
de inventar.

⏮️ [Volver a la clase 072](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
