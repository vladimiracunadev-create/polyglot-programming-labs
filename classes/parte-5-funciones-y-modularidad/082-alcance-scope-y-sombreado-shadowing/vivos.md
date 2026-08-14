# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 082

> [⬅️ Volver a la clase 082](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un valor calculado **dentro** de un ámbito y otro que sigue intacto **fuera**. Parece elemental, y
resulta que **COBOL no tiene ámbitos**: todas sus variables son globales al programa, siempre, sin
excepción. Y Fortran tuvo que esperar hasta **2008** para tener bloques con variables locales.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **ámbito léxico**, y estos lenguajes lo enseñan porque muestran su ausencia.
> En **COBOL** todo es global: un programa de cinco mil líneas tiene un solo espacio de nombres, y por
> eso sus variables llevan prefijos —`WS-`, `CLI-`, `LK-`— que son un sistema de ámbitos hecho a mano
> con convenciones de nombres.
>
> Y **M** tiene la respuesta más distinta de todas: **ámbito dinámico** con `new`, donde una variable no
> es local al bloque sino a la **duración de la llamada**, y las rutinas llamadas la ven. Es el mismo
> mecanismo que `local` en Perl y las variables especiales de Lisp, y comparar los dos modelos es lo
> más valioso de esta clase.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `interno=<n+10> externo=<n>`
- **Regla:** `externo x = n; en un bloque interno x = n+10; al salir, x = n`

| stdin | esperado |
|---|---|
| `5` | `interno=15 externo=5` |
| `0` | `interno=10 externo=0` |
| `-3` | `interno=7 externo=-3` |

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
PROGRAM-ID. ALCANCE.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA    PIC X(80).
01  N        PIC S9(9) COMP-3.
01  INTERNO  PIC S9(9) COMP-3.
01  ED-I     PIC -(8)9.
01  ED-N     PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    PERFORM CALCULAR

    MOVE INTERNO TO ED-I
    MOVE N       TO ED-N
    DISPLAY "interno=" FUNCTION TRIM(ED-I)
            " externo=" FUNCTION TRIM(ED-N)
    STOP RUN.

CALCULAR.
    COMPUTE INTERNO = N + 10.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene ámbitos.** Ni de bloque, ni de párrafo, ni de
sección. Todo lo declarado en `WORKING-STORAGE` es visible desde cualquier punto del programa, y no
hay forma de declarar algo "solo para este trozo".

La consecuencia es que un programa de cinco mil líneas tiene **un único espacio de nombres**, y el
sustituto que inventó la industria son las **convenciones de prefijos**:

```cobol
01  WS-CONTADOR      PIC 9(4).     *> WS = Working-Storage
01  LK-PARAMETRO     PIC X(10).    *> LK = Linkage
01  CLI-NOMBRE       PIC X(40).    *> por módulo funcional
01  I-CLIENTES-KEY   PIC X(8).     *> por fichero
```

Eso no es estilo: es un **sistema de ámbitos implementado con nombres**, y toda instalación grande
tiene su estándar documentado. Cuando falla —dos módulos que usan `WS-CONTADOR` para cosas distintas
en el mismo programa— aparece el error más difícil de encontrar de COBOL.

COBOL sí tiene una forma de ámbito, y llegó tarde: los **programas anidados** de COBOL-85.

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. PRINCIPAL.
...
    IDENTIFICATION DIVISION.
    PROGRAM-ID. INTERNO IS COMMON.
    DATA DIVISION.
    WORKING-STORAGE SECTION.
    01  PRIVADO  PIC 9(4).      *> invisible desde PRINCIPAL
    ...
    END PROGRAM INTERNO.
END PROGRAM PRINCIPAL.
```

Un programa anidado tiene su propio `WORKING-STORAGE` **privado**, y solo ve lo que el padre marque
con `GLOBAL`. Es encapsulación de verdad, disponible desde 1985 y **muy poco usada** — porque para
entonces ya había millones de líneas escritas con prefijos.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program alcance
   implicit none
   integer :: n, interno

   read(*, *) n

   block                          ! Fortran 2008: bloque con declaraciones
      integer :: n_local
      n_local = n + 10
      interno = n_local
   end block                      ! n_local deja de existir aquí

   write(*, '(A,I0,A,I0)') 'interno=', interno, ' externo=', n
end program alcance
```

**Lo que esta clase enseña en Fortran.** La construcción **`block`** —con declaraciones propias— llegó
en **Fortran 2008**. Hasta entonces, **el ámbito más pequeño de Fortran era el procedimiento**: todas
las declaraciones iban arriba y valían para toda la subrutina.

Eso obligaba a un estilo reconocible: procedimientos con veinte declaraciones al principio, la mitad
de ellas temporales usadas en un solo bucle. Es la misma limitación que Pascal, y por el mismo motivo
histórico —la compilación en una pasada—.

`block` permite además **sombrear**:

```fortran
integer :: x
x = 1
block
   integer :: x      ! SOMBREA la exterior
   x = 99
end block
print *, x           ! 1: la exterior no se tocó
```

Y tiene una capacidad que va más allá del ámbito: **dentro de un `block` se puede usar `exit` con
nombre** para salir de él, como se vio en la clase 058, lo que da un bloque con salida temprana sin
`goto`.

El otro mecanismo de ámbito de Fortran son los **procedimientos internos** en `contains`, que **ven
las variables del anfitrión** —eso es la clase 083— y los **módulos**, que son la clase 086.

Y una nota importante: en Fortran, **una variable local de un procedimiento no conserva su valor entre
llamadas**, salvo que lleve `save` o esté inicializada en la declaración — la trampa de la clase 042.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Alcance is
   N : Integer;
begin
   Get (N);

   declare
      Interno : constant Integer := N + 10;   --  solo existe aquí
   begin
      Put ("interno=");
      Put (Interno, Width => 1);
   end;

   Put (" externo=");
   Put (N, Width => 1);
   New_Line;
end Alcance;
```

**Lo que esta clase enseña en Ada.** El bloque **`declare … begin … end`** puede aparecer **en
cualquier punto** donde vaya una sentencia, y crea un ámbito con sus propias declaraciones. Es la
misma idea que el `block` de Fortran 2008, disponible en Ada desde 1983.

Y tiene una ventaja concreta sobre declarar arriba: **permite `constant`**. `Interno` se calcula
justo donde se sabe su valor, y queda sellado. Declararlo al principio del procedimiento obligaría a
dejarlo variable.

Los bloques de Ada pueden además **llevar nombre** y **manejadores de excepción propios**:

```ada
Validacion : declare
   Datos : Registro := Leer;
begin
   Procesar (Datos);
exception
   when Constraint_Error =>
      Put_Line ("datos inválidos");     --  solo captura lo de ESTE bloque
end Validacion;
```

Un ámbito con su propio manejo de errores, acotado a las líneas que lo necesitan. Es exactamente lo
que en C++ se consigue anidando un `try` y en Java un bloque `try`, con la diferencia de que aquí el
bloque **también** delimita las declaraciones.

Sobre el sombreado, Ada lo permite pero es **muy estricto con la ambigüedad**: si dos nombres visibles
por `use` colisionan, **ninguno de los dos es visible** y hay que cualificar. Eso evita el problema
clásico de "importé un paquete y ahora mi función llama a otra cosa" — el compilador se niega en lugar
de elegir por ti.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Alcance;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, Interno: Integer;

procedure Calcular;
var
  Temp: Integer;        { local al PROCEDIMIENTO: no existe fuera }
begin
  Temp := N + 10;       { ve N, del ámbito que lo contiene }
  Interno := Temp;
end;

begin
  Read(N);
  Calcular;
  WriteLn('interno=', IntToStr(Interno), ' externo=', IntToStr(N));
end.
```

**Lo que esta clase enseña en Pascal.** **Pascal no tiene ámbito de bloque**: `begin`/`end` agrupa
sentencias pero **no puede declarar variables**. El ámbito más pequeño es el **procedimiento**.

Lo que Pascal sí tiene, y fue una de sus grandes aportaciones, son los **procedimientos anidados**
con **ámbito léxico completo**:

```pascal
procedure Externo;
var
  A: Integer;

  procedure Interno;
  var
    B: Integer;
  begin
    B := A + 1;        { VE la A de Externo }
  end;

begin
  A := 1;
  Interno;
end;
```

Un procedimiento anidado **ve todas las variables de los que lo contienen**, a cualquier profundidad.
Eso viene de ALGOL 60 y **C nunca lo tuvo** —solo funciones al nivel superior—, lo que obligó a C a
usar variables globales o a pasar estructuras de contexto.

La implementación de eso es lo interesante: hace falta un **enlace estático** en cada marco de pila,
que apunta al marco del procedimiento que lo contiene léxicamente, para poder llegar a sus variables.
Es el mecanismo que después se generalizó en las clausuras de la clase 083.

Ada, Fortran (con `contains`), PL/I y JavaScript tienen anidamiento léxico; C, Java y Go no —Java lo
recuperó con las clases internas y Go con las clausuras—.

Y el sombreado funciona: una variable interna con el mismo nombre oculta a la externa, y Free Pascal
avisa con `-vh` si sospecha que fue un accidente.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "interno=~D externo=~D~%"
          (let ((n (+ n 10))) n)     ; esta n SOMBREA la exterior
          n))                         ; aquí vuelve a ser la exterior
```

**Lo que esta clase enseña en Common Lisp.** El sombreado de este programa es visible en una línea:
la `n` interna del `let` oculta a la externa **dentro de sus paréntesis**, y fuera vuelve a valer la
original.

Y Lisp es el lenguaje donde mejor se ve la diferencia entre los **dos tipos de ámbito**, porque tiene
los dos:

```lisp
(defvar *tasa* 0.21)                  ; variable ESPECIAL: ámbito DINÁMICO
(defun con-iva (x) (* x (+ 1 *tasa*)))

(defun ejemplo ()
  (let ((*tasa* 0.10))                ; reenlaza la especial...
    (con-iva 100)))                    ; ...y con-iva ve 0.10, aunque no lo sepa
```

`con-iva` **no recibe la tasa como parámetro y no la ve por ámbito léxico**: la ve porque quien la
llamó reenlazó la variable especial. Eso es **ámbito dinámico**, y en Lisp está marcado por
convención con asteriscos —los *earmuffs*— precisamente para que se note.

Con una variable normal (`let` sobre un símbolo no especial), el ámbito es **léxico**: solo la ve el
código escrito dentro.

Tener los dos, y distinguirlos tipográficamente, es lo que hace de Lisp el mejor sitio para entender
esta clase. El dinámico sirve para el **contexto implícito** —la tasa vigente, el flujo de salida, el
nivel de registro— que en otros lenguajes obliga a pasar un parámetro por toda la cadena de llamadas
o a usar una variable global sin restaurar.

Es exactamente lo que hace `new` en M y `local` en Perl, y lo que Java resuelve con `ThreadLocal`.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc calcular {n} {
    set n [expr {$n + 10}]     ;# n es LOCAL al proc: no toca la del llamante
    return $n
}

gets stdin linea
set n [string trim $linea]

puts "interno=[calcular $n] externo=$n"
```

**Lo que esta clase enseña en Tcl.** El ámbito de Tcl es **el procedimiento, y nada más**: no hay
ámbito de bloque, y —esto es lo llamativo— **un `proc` NO ve las variables globales**.

```tcl
set config "algo"
proc f {} {
    puts $config        ;# ERROR: "can't read config: no such variable"
}
```

Hay que declararlo explícitamente:

```tcl
proc f {} {
    global config       ;# ahora sí
    puts $config
}
```

Esa decisión —**las globales son invisibles salvo que las pidas**— es exactamente la contraria de la
de casi todos los lenguajes, y es deliberada: en un lenguaje de guion incrustado en una aplicación
grande, que un procedimiento pueda leer accidentalmente cualquier variable del sistema sería un
desastre.

Python tomó la decisión inversa y a medias: **puede leer** las globales sin declarar nada, pero para
**escribirlas** necesita `global`. Tcl es más estricto en las dos direcciones.

Y Tcl tiene además `namespace`, que da un tercer nivel:

```tcl
namespace eval ::miapp {
    variable contador 0          ;# variable de ESPACIO DE NOMBRES
    proc incrementar {} {
        variable contador        ;# se declara para verla
        incr contador
    }
}
```

`variable` es a los espacios de nombres lo que `global` al nivel superior. Con eso Tcl tiene tres
niveles —local, de espacio de nombres y global— y **los tres exigen declaración explícita** para
usarse desde dentro de un procedimiento.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $interno;
{
    my $n = $n + 10;      # el $n de la DERECHA es todavía el EXTERIOR
    $interno = $n;
}

print "interno=$interno externo=$n\n";
```

**Lo que esta clase enseña en Perl.** La línea `my $n = $n + 10;` merece explicación porque parece
imposible y es correcta: **una variable declarada con `my` no es visible hasta que TERMINA la
sentencia que la declara**.

Así que en el lado derecho, `$n` todavía se refiere al **exterior**. A partir de la siguiente línea,
`$n` es el nuevo. Es una regla precisa y muy útil para el idioma
`my $x = $x` —tomar una copia local de algo del ámbito exterior—.

Perl tiene **tres declaradores**, y esta clase es donde se distinguen:

| | Ámbito | Qué hace |
|---|---|---|
| `my` | **Léxico** | Variable nueva, visible solo en el bloque |
| `our` | Léxico | Un **alias** a la variable global del paquete |
| `local` | **DINÁMICO** | Guarda el valor de una global y lo restaura al salir |

`local` es la que sorprende, y es exactamente el `new` de M y las variables especiales de Lisp:

```perl
our $separador = ',';
sub imprimir { print join($separador, @_) }

sub con_tabulador {
    local $separador = "\t";     # cambia la GLOBAL durante esta llamada
    imprimir(@_);                  # imprimir ve el tabulador, sin saberlo
}                                  # y al salir se restaura la coma
```

`imprimir` no recibe el separador y no lo ve por ámbito léxico: lo ve porque `local` lo cambió
temporalmente. Es el contexto implícito de la ficha de Lisp, con otra palabra.

El uso más común de `local` en Perl real es sobre las variables especiales del propio lenguaje:
`local $/ = undef;` para leer un fichero entero de una vez, o `local $_` para no pisar la variable
implícita.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    int interno{};
    {
        const int n_interno = n + 10;   // ámbito de BLOQUE
        interno = n_interno;
    }   // n_interno deja de existir aquí

    std::cout << "interno=" << interno << " externo=" << n << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene **ámbito de bloque** desde C, y cualquier par de llaves
crea uno. Y el sombreado es legal, con un aviso:

```cpp
int x = 1;
{
    int x = 2;      // SOMBREA; -Wshadow lo avisa
}
```

`-Wshadow` no está en `-Wall` y conviene activarlo: el sombreado accidental —sobre todo de un
parámetro por una variable local— es una fuente real de errores.

Lo que C++ añade a esta clase, y es lo importante, es que **el ámbito determina el tiempo de vida**:

```cpp
{
    std::lock_guard<std::mutex> cierre(m);   // se bloquea aquí
    std::ofstream f("salida.txt");           // se abre aquí
    ...
}   // el destructor de f cierra el fichero, el de cierre libera el mutex
```

Ese es **RAII**, y es la razón de que en C++ el ámbito sea una herramienta de gestión de recursos y no
solo de visibilidad. Abrir un bloque `{ }` sin más motivo que **acotar el tiempo de vida de un
recurso** es un idioma normal del lenguaje.

C++17 añadió además el inicializador en `if` y `switch`, que acota el ámbito a la sentencia:

```cpp
if (auto it = m.find(k); it != m.end()) { ... }   // it muere al salir del if
```

Y C++20 los espacios de nombres en línea, los módulos y `using enum`, que refinan la visibilidad —
tema de la clase 086.

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
ctl-opt dftactgrp(*no) actgrp(*caller) main(Principal);

dcl-s global_n int(10);          // GLOBAL: visible en todo el módulo

dcl-proc Principal;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dcl-s salida char(50);

  global_n = n;
  salida = 'interno=' + %char(calcular())
         + ' externo=' + %char(global_n);
  dsply salida;
end-proc;

dcl-proc calcular;
  dcl-pi *n int(10);
  end-pi;
  dcl-s temp int(10);            // LOCAL al procedimiento
  temp = global_n + 10;
  return temp;
end-proc;
```

**Lo que esta clase enseña en RPG.** RPG tiene **dos niveles y solo dos**: lo declarado fuera de
cualquier `dcl-proc` es **global al módulo**, y lo declarado dentro es **local al procedimiento**. No
hay ámbito de bloque.

Y esa distinción **no existía antes de ILE**. En el RPG clásico, absolutamente todo era global —como
en COBOL— y las subrutinas (`begsr`/`endsr`) compartían todas las variables del programa. Por eso el
código antiguo usa prefijos por subrutina, exactamente igual que COBOL con `WS-`.

Los subprocedimientos de ILE trajeron el ámbito local, y con él la posibilidad de escribir código
reutilizable de verdad.

RPG tiene además dos palabras que afinan la visibilidad **entre módulos**:

```rpgle
dcl-s contador int(10) static;    // conserva el valor entre llamadas
dcl-proc calcular export;         // VISIBLE desde otros módulos
dcl-proc auxiliar;                // sin export: PRIVADO del módulo
```

`export` en un `dcl-proc` es lo que decide si el procedimiento entra en la interfaz del módulo. Sin
él, es privado. Es exactamente el `static` de C aplicado a funciones, con la lógica invertida —en C
hay que escribir `static` para ocultar; en RPG hay que escribir `export` para mostrar—.

Esa inversión es mejor: **lo privado por defecto** es lo que hoy recomiendan todas las guías, y lo
que hacen Rust, Java (paquete) y los módulos de C++20.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 alcance: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    begin;                              /* BLOQUE con su propio ámbito */
       declare interno fixed binary(31);
       interno = n + 10;
       put skip list ('interno=' || trim(char(interno)) ||
                      ' externo=' || trim(char(n)));
    end;

 end alcance;
```

**Lo que esta clase enseña en PL/I.** El **bloque `begin`** de PL/I es un ámbito completo con sus
propias declaraciones, y estaba en el lenguaje **desde 1964** — mucho antes que en Fortran (2008) y
que en C.

Y PL/I tiene **anidamiento léxico ilimitado** con la regla clásica de ALGOL: un bloque interno ve
todo lo de los que lo contienen, y puede sombrearlo.

```pli
declare x fixed binary(31);
begin;
   declare x character(10);      /* SOMBREA el x exterior, y con OTRO TIPO */
   ...
end;
```

Lo que distingue a PL/I es la interacción del ámbito con las **clases de almacenamiento** de la clase
042: un `begin` block **activa el almacenamiento automático** de lo que declara, así que entrar y
salir tiene coste. Por eso existe `do; ... end;`, que agrupa **sin** crear ámbito ni marco:

```pli
if c then do;  ... end;      /* solo agrupa: barato */
if c then begin; ... end;    /* ámbito nuevo: puede declarar, cuesta más */
```

Tener las dos construcciones con esa diferencia de coste explícita es muy propio del lenguaje, y
también es la clase de detalle que hay que conocer para leer código ajeno: `begin` y `do` parecen
intercambiables y no lo son.

Y `begin` puede llevar sus propios manejadores `ON`, igual que el bloque de Ada — el ámbito delimita
también el manejo de errores.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ALCANCE ; Alcance y sombreado -- clase 082
 read n
 do calcular
 write "interno=", interno, " externo=", n, !
 quit
 ;
calcular ; usa NEW para no pisar variables del llamante
 new temp
 set temp = n + 10
 set interno = temp
 quit
```

**Lo que esta clase enseña en M.** **M no tiene ámbito léxico. Todas las variables son globales al
proceso**, y lo único que existe es **`new`**, que da **ámbito dinámico**.

```mumps
calcular ;
 new temp              ; guarda el valor ACTUAL de temp (sea de quien sea)...
 set temp = 5
 quit                  ; ...y lo restaura al salir
```

`new temp` **no crea una variable local**: guarda en una pila el valor que `temp` tuviera en todo el
proceso, lo deja indefinido, y lo restaura al salir de la rutina.

La diferencia con el ámbito léxico es la que da la lección de esta clase: **una rutina llamada desde
aquí VE la `temp` de esta rutina**, porque no hay barrera léxica. Con ámbito léxico eso sería
imposible.

```mumps
 new formato
 set formato = "corto"
 do IMPRIMIR^REP      ; IMPRIMIR ve "corto" sin que nadie se lo pase
```

Ese es el contexto implícito de la ficha de Lisp y del `local` de Perl, y en M **es el único modelo
que hay**. Todo el código de VistA lo usa: se establecen variables convenidas antes de llamar, y las
rutinas llamadas las leen.

Es frágil —un `new` olvidado corrompe el estado del llamante— y es la razón de que las guías de estilo
de M sean obsesivas con `new`. Y es potente: permite pasar contexto a través de veinte niveles de
llamada sin tocar ninguna firma.

Existe además `new` **exclusivo**: `new (a, b)` guarda **todo menos** `a` y `b`, que es la forma de
aislar completamente una rutina.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n interno |

n := stdin nextLine trimBoth asNumber.

interno := [ :x | | temp | temp := x + 10. temp ] value: n.

Transcript
    show: 'interno=', interno printString;
    show: ' externo=', n printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** El bloque de este programa declara su propia temporal
—`| temp |` dentro de los corchetes— y esa variable **solo existe durante la evaluación del bloque**.

Smalltalk tiene una jerarquía de ámbitos muy clara, de dentro afuera:

1. **Temporales del bloque** — `[ :x | | t | ... ]`
2. **Argumentos y temporales del método**
3. **Variables de instancia** del objeto
4. **Variables de clase**, compartidas por la clase y sus instancias
5. **Variables globales**, en el diccionario `Smalltalk`

Y todo es **léxico**: un bloque ve las variables del método que lo creó, aunque se evalúe muy lejos —
eso es la clase 083.

Lo que hace especial a Smalltalk en esta clase es que **el ámbito es un objeto inspeccionable**.
`thisContext` de la clase 066 da acceso al marco de activación actual, con sus temporales, su receptor
y su llamante:

```smalltalk
thisContext tempNames          "los nombres de las temporales"
thisContext receiver            "el objeto que recibió el mensaje"
thisContext sender              "el marco que llamó"
```

Por eso el depurador de Smalltalk puede mostrar y **modificar** las variables locales de cualquier
marco de la pila, y continuar. En un lenguaje compilado esa información solo existe si se compiló con
símbolos de depuración; aquí **es parte del modelo de objetos**.

Y las variables de instancia no llevan `self.` delante: se escriben a secas, lo que hace que un método
de Smalltalk se lea muy limpio y exija conocer la clase para saber qué es local y qué es de instancia.

---

## Y de vuelta a la clase

Lo transferible: **el ámbito léxico se determina leyendo el texto; el dinámico, ejecutando el
programa**. Con léxico, una función solo ve lo que está escrito alrededor de ella. Con dinámico, ve lo
que haya puesto quien la llamó, así que el mismo código se comporta distinto según desde dónde se
invoque. El léxico ganó porque es analizable — pero el dinámico sigue vivo donde hace falta un
contexto implícito: `local` en Perl, las variables especiales de Lisp, y prácticamente todo el código
de MUMPS.

⏮️ [Volver a la clase 082](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
