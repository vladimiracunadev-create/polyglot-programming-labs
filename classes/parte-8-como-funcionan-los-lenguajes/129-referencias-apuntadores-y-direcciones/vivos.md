# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 129

> [⬅️ Volver a la clase 129](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Acceder al elemento `i` de una colección. Detrás de esa operación trivial está la pregunta que separa
a estos doce lenguajes: **¿existe la dirección de memoria como valor manipulable?** En COBOL, RPG,
PL/I, C++ y Fortran sí; en Ada existe **con comprobaciones que impiden el puntero colgante**; y en
Tcl, Lisp, Smalltalk y M **no existe en absoluto** — y sus programas funcionan igual.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **indirección**, y estos lenguajes lo enseñan porque cubren desde el puntero
> crudo hasta su ausencia total. **PL/I inventó el puntero de alto nivel en 1964** y de ahí lo tomaron
> COBOL, RPG y —en espíritu— C. **Ada lo acotó**: sus accesos llevan comprobación de accesibilidad
> (clase 083) y pueden declararse `not null` (clase 116). **Fortran distingue `pointer` de
> `allocatable`** por el aliasing (clase 128).
>
> Y los que no lo tienen enseñan lo contrario: **en M, en Tcl y en Smalltalk no hay forma de que dos
> nombres designen la misma cosa mutable** —o la hay solo por objetos— y eso elimina una clase entera de
> errores.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `indice v0 v1 v2 ...` (el primero es el índice, base 0) → stdout: `valor=<elemento en esa posición>`
- **Regla:** `valor = lista[indice]`

| stdin | esperado |
|---|---|
| `1 10 20 30` | `valor=20` |
| `0 5 6 7` | `valor=5` |
| `2 100 200 300` | `valor=300` |

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
PROGRAM-ID. REFEREN.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2) COMP VALUE 0.
01  I       PIC 9(4) COMP.
01  NT      PIC 9(4) COMP VALUE 0.
01  IDX     PIC 9(4) COMP VALUE 0.
01  TABLA.
    05  ELEM  PIC S9(9) COMP-3 OCCURS 100 TIMES.
01  ED-V    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM CERRAR
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM CERRAR

    *> el primer token es el índice, base 0
    COMPUTE I = IDX + 1
    MOVE ELEM(I) TO ED-V
    DISPLAY "valor=" FUNCTION TRIM(ED-V)
    STOP RUN.

CERRAR.
    IF TLEN > 0
        IF NT = 0
            COMPUTE IDX = FUNCTION NUMVAL(TOKEN)
        ELSE
            COMPUTE ELEM(NT) = FUNCTION NUMVAL(TOKEN)
        END-IF
        ADD 1 TO NT
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** El COBOL de gestión **no usa punteros**, y el acceso indexado
—`ELEM(I)`— es todo lo que hace falta. La ausencia de indirección es lo que hace que los programas de
esta serie sean tan predecibles (clase 128).

Y sin embargo COBOL **sí tiene punteros**, y su historia empieza con una construcción que merece
conocerse porque es la indirección más antigua del lenguaje: **`LINKAGE SECTION` con `SET ADDRESS`**.

```cobol
LINKAGE SECTION.
01  REG-EXTERNO  PIC X(100).

PROCEDURE DIVISION.
    SET ADDRESS OF REG-EXTERNO TO PTR       *> apuntar a memoria ajena
```

**La `LINKAGE SECTION` describe datos que el programa NO posee**: los parámetros que recibe, o memoria
que otro le pasa. Es, literalmente, una declaración de tipo sin almacenamiento — el `based` de PL/I con
otro nombre.

Y esa es la forma en que COBOL recibe sus parámetros: **por referencia, por defecto** (clase 079).

```cobol
CALL "SUB" USING BY REFERENCE REG      *> el llamado recibe la DIRECCIÓN
CALL "SUB" USING BY CONTENT  REG        *> recibe una COPIA
CALL "SUB" USING BY VALUE    NUM         *> por valor (COBOL 2002)
```

**`BY REFERENCE` es el defecto**, y es la razón de que un subprograma COBOL pueda modificar los datos
de quien lo llama sin que la llamada lo indique — el mismo diseño que PL/I (clase 102) y el contrario
al de C.

COBOL-2002 añadió punteros de primera clase:

```cobol
01  PTR       USAGE POINTER.
01  PTR-PROC  USAGE PROCEDURE-POINTER.
SET PTR TO ADDRESS OF REG
SET PTR-PROC TO ENTRY "MISUB"
```

**`PROCEDURE-POINTER`** es el puntero a función (clase 085), y con él se construyen las tablas de
despacho.

Y merece cerrar con el uso real: **los punteros de COBOL existen sobre todo para hablar con C y con las
APIs del sistema**. Un programa de negocio no los usa; uno que llame a una biblioteca en C, sí. Es la
misma frontera que en Fortran con `iso_c_binding` (clase 119).

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program referen
   implicit none
   integer, target  :: v(100)
   integer, pointer :: p(:)
   integer :: n, ios, i, idx
   character(len=400) :: linea

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   idx = v(1)                      ! el primero es el índice, base 0
   p => v(2:n)                      ! ALIAS a una sección: no copia

   write(*, '(A,I0)') 'valor=', p(idx + 1)
end program referen
```

**Lo que esta clase enseña en Fortran.** `p => v(2:n)` es **asociación de puntero**: `p` no es una copia,
**es otro nombre para esa parte de `v`** (clase 097). Escribir en `p(1)` cambia `v(2)`.

Y fíjate en el atributo **`target`** de la declaración de `v`:

```fortran
integer, target :: v(100)      ! "a esto se le PUEDE apuntar"
```

**En Fortran no se puede apuntar a cualquier cosa**: solo a lo declarado `target` o a lo reservado con
`allocate`. Esa restricción es la clave del rendimiento del lenguaje (clases 123 y 124): **el
compilador sabe que una variable sin `target` no puede tener alias**, así que puede mantenerla en un
registro y reordenar accesos sin miedo.

Es exactamente la información que en C hay que prometer con `restrict`, y en Fortran es el defecto
—hay que renunciar a ella explícitamente.

Y el puntero de Fortran es mucho más que una dirección: **lleva un descriptor**.

```fortran
p => v(1:100:2)         ! los elementos IMPARES: no son contiguos
size(p)                  ! 50
p(3)                      ! el elemento v(5)
```

**Un puntero de Fortran puede apuntar a una sección con paso**, y guarda los límites y el paso. Es un
objeto con estructura, no un entero.

De ahí una consecuencia práctica: **pasar un puntero a una rutina que espera un arreglo contiguo puede
generar una copia** —el *copy-in/copy-out* de la clase 102— y `gfortran -Warray-temporaries` lo avisa.

Fortran distingue además tres estados de un puntero, y el segundo es el peligroso:

```fortran
nullify(p)             ! nulo: associated(p) es falso
p => variable_local     ! si la local muere, p queda COLGADO
associated(p)            ! indefinido si p nunca se inicializó
```

**Un puntero sin inicializar tiene estado indefinido**, y `associated()` sobre él es comportamiento
indefinido. De ahí la práctica universal:

```fortran
integer, pointer :: p => null()      ! inicializar SIEMPRE a nulo
```

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Referen is
   type Vector is array (Positive range <>) of Integer;

   Datos  : aliased Vector (1 .. 100) := (others => 0);
   N      : Natural := 0;
   Idx    : Integer := 0;
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      if N = 0 then
         Idx := Valor;              --  el primero es el índice
      else
         Datos (N) := Valor;
      end if;
      N := N + 1;
      Pos := Fin + 1;
   end loop;

   Put ("valor=");
   Put (Datos (Idx + 1), Width => 1);
   New_Line;
end Referen;
```

**Lo que esta clase enseña en Ada.** Ada tiene punteros —los llama **tipos de acceso**— y los rodea de
comprobaciones que ningún otro lenguaje de esta página reúne.

**Primera: hay que declarar a qué se puede apuntar.**

```ada
X : aliased Integer;               --  "a esto se le puede apuntar"
P : access Integer := X'Access;
```

Igual que el `target` de Fortran, y por la misma razón: **sin `aliased`, el compilador sabe que nadie
tiene una referencia**.

**Segunda: la comprobación de accesibilidad** (clase 083). No se puede guardar un acceso a algo que
viva menos que el tipo del acceso — **el puntero colgante se rechaza en compilación** en los casos que
se pueden decidir estáticamente.

**Tercera: `not null`** (clase 116), que elimina el nulo del tipo:

```ada
type Ref is not null access Integer;
procedure P (X : not null access Nodo);
```

**Cuarta: los tipos de acceso llevan su propio almacenamiento** (clase 128), acotable con
`Storage_Size` y con gestor propio.

**Y quinta: la aritmética de punteros no existe.** No se puede sumar a un acceso, ni convertirlo a
entero, salvo con `System.Address_To_Access_Conversions` — cuyo nombre, otra vez, avisa.

El resultado es que **un programa Ada normal no puede tener las clases de fallo que dominan C y C++**:
uso tras liberar, desbordamiento por aritmética de punteros, o desreferencia de nulo.

Y para lo que sí necesita direcciones de verdad —programación de sistemas— Ada da el paquete `System`:

```ada
X'Address                                    --  la dirección
for Registro'Address use To_Address (16#FF00#);   --  colocar en una dirección FIJA
```

**Colocar una variable en una dirección concreta** es cómo se accede a los registros de hardware, y
combinado con la especificación de representación bit a bit (clase 117) permite escribir controladores
sin ensamblador.

Es la misma capacidad que C, con la diferencia de que **en Ada hay que pedirla y se ve**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Referen;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  V: array of Integer;
  P: ^Integer;
  Linea, Tok: string;
  I, Idx, NT: Integer;
  C: Char;

begin
  ReadLn(Linea);

  SetLength(V, 0);
  NT := 0;
  Idx := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        if NT = 0 then
          Idx := StrToInt(Tok)
        else
        begin
          SetLength(V, Length(V) + 1);
          V[High(V)] := StrToInt(Tok);
        end;
        Inc(NT);
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  P := @V[Idx];                 { la DIRECCIÓN del elemento }
  WriteLn('valor=', IntToStr(P^));
end.
```

**Lo que esta clase enseña en Pascal.** La notación de punteros de Pascal es de 1970 y sigue siendo la
más clara de esta página, como se dijo en la clase 097:

```pascal
type PNodo = ^TNodo;      { "puntero a TNodo": se lee de izquierda a derecha }
P^                          { "lo que apunta P" }
@X                           { "la dirección de X" }
```

**El `^` va a la derecha para desreferenciar y a la izquierda para declarar**, y `@` es la dirección.
En C, `*` hace las dos cosas y la declaración se lee al revés que el uso — que es la causa de que
`int *p[10]` y `int (*p)[10]` confundan a todo el mundo.

Y Pascal original tenía una restricción importante: **los punteros solo podían apuntar a memoria
reservada con `New`**, no a variables. **`@` es una extensión de Turbo Pascal**, no del Pascal
estándar.

Esa restricción no era arbitraria: **sin `@`, un puntero nunca puede apuntar a algo que muera antes que
él**, porque solo apunta al montón. Es la garantía que Ada consigue con la comprobación de
accesibilidad y Fortran con `target`.

Object Pascal moderno tiene cuatro clases de referencia, y distinguirlas es cotidiano:

```pascal
P: ^TNodo;                { puntero TIPADO }
Q: Pointer;                { puntero sin tipo, como void* }
O: TObjeto;                 { REFERENCIA a objeto: implícita, nunca ^ }
I: IInterfaz;                { con conteo de referencias (clase 103) }
```

**Una variable de clase en Delphi ya es un puntero**, y por eso se escribe `Obj.Metodo` y no
`Obj^.Metodo`. Esa asimetría —punteros explícitos para registros, implícitos para objetos— es una
decisión de comodidad que hay que tener presente al razonar sobre copias (clase 102).

Y Free Pascal tiene una directiva que esta clase debe nombrar:

```pascal
{$POINTERMATH ON}
Inc(P);          { aritmética de punteros, al estilo de C }
P[3];             { indexar un puntero }
```

**Por defecto está desactivada**: en Pascal, un puntero no se indexa ni se incrementa. Activarla es
optar explícitamente por el modelo de C — y es otra vez la misma doctrina de esta página: **lo
peligroso se declara**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((idx (read))
       (v (coerce (loop for x = (read *standard-input* nil nil)
                        while x collect x)
                  'vector)))
  (format t "valor=~D~%" (aref v idx)))
```

**Lo que esta clase enseña en Common Lisp.** **En Lisp no hay punteros**, y sin embargo la indirección
está en todas partes: **toda variable que no contenga un número pequeño o un carácter contiene una
referencia**.

```lisp
(let* ((a (list 1 2 3))
       (b a))                    ; b y a son LA MISMA lista
  (setf (car b) 99)
  a)                              ; (99 2 3) -- a también cambió
```

Eso es la clase 102 en Lisp: **las estructuras se comparten al asignar**, y `copy-list` o `copy-tree`
son las que copian.

Lo que Lisp no permite es **manipular la dirección**: no hay aritmética de punteros, no se puede
convertir una referencia a entero y no se puede apuntar a una posición arbitraria de memoria.

Y de ahí sale una propiedad que esta clase debe subrayar: **en Lisp no existe el puntero colgante**. El
recolector de basura (clase 131) garantiza que **mientras alguien tenga una referencia, el objeto
existe**.

Lo que sí existe, y es el equivalente conceptual del puntero, son **los lugares** (clase 095):

```lisp
(setf (aref v 3) 99)              ; escribir EN una posición
(setf (gethash k tabla) v)         ; en una entrada de tabla
(setf (car lista) 99)               ; en el primer cons
(setf (symbol-value 's) 42)          ; en el valor de un símbolo
```

**`setf` sobre una forma que designa un sitio es la escritura indirecta de Lisp**, y es extensible: con
`define-setf-expander` se puede hacer asignable cualquier cosa.

Y Lisp tiene además la identidad como concepto explícito (clase 101):

```lisp
(eq a b)                      ; ¿es EL MISMO objeto?
(sb-kernel:get-lisp-obj-address x)   ; la dirección, en SBCL: no portable
```

**`eq` es la comparación de referencias**, y es lo más cerca que el lenguaje deja llegar a la
dirección.

Para hablar con C, Lisp sí necesita direcciones, y el ecosistema lo resuelve con **CFFI**:

```lisp
(cffi:foreign-alloc :int :count 10)
(cffi:mem-aref ptr :int 3)
(cffi:with-foreign-object (p :int) ...)
```

**Ahí sí hay punteros de verdad, con reserva manual y sin recolector** — y con la advertencia
correspondiente: **la memoria de CFFI la libera el programador**. Es la frontera de la que habla la
clase 156.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set partes [split [string trim $linea]]

set idx [lindex $partes 0]
set v [lrange $partes 1 end]

puts "valor=[lindex $v $idx]"
```

**Lo que esta clase enseña en Tcl.** **En Tcl no hay punteros, ni referencias, ni direcciones**, y esa
ausencia es total: **no existe ninguna forma de que dos variables designen el mismo valor mutable**
(clase 102).

Lo más parecido a una referencia es **el nombre de una variable, pasado como cadena**:

```tcl
proc incrementar {nombreVar} {
    upvar 1 $nombreVar v        ;# ligar el nombre a una variable local
    incr v
}
set contador 0
incrementar contador            ;# SIN el $: se pasa el NOMBRE
```

**`upvar` es la indirección de Tcl** (clase 080), y su unidad no es una dirección: es **un nombre en un
ámbito**. Es más seguro —no puede colgar— y más limitado: solo funciona sobre variables con nombre.

Y hay una segunda forma que es la de los objetos: **el nombre de un comando** (clase 101).

```tcl
set obj [Persona new]         ;# obj contiene una CADENA: el nombre del comando
set otro $obj                  ;# ahora los dos designan el MISMO objeto
```

Ahí sí hay identidad compartida, porque **el objeto no es el valor, es el comando** al que la cadena
apunta. Es indirección por nombre en la tabla de comandos, y tiene la propiedad interesante de que
**el nombre se puede guardar en un fichero y recuperar** mientras el objeto exista.

Esa decisión —**referencias por nombre en lugar de por dirección**— tiene una consecuencia que Tcl
aprovecha: **todo se puede serializar**. Una estructura de datos de Tcl siempre es una cadena, y un
objeto es un nombre.

Y su límite es igual de claro: **no se pueden construir grafos con enlaces cruzados** salvo usando
nombres, y ahí el programador se ocupa de la coherencia.

Para la frontera con C, Tcl expone punteros como cadenas con formato:

```tcl
# los manejadores de extensiones suelen verse así:
# "0x7f8e4c001a20" o "canal5"
```

Y las extensiones en C usan `Tcl_Obj*` con conteo de referencias por debajo — que es donde sí hay
punteros y donde puede haber fugas (clase 128).

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($idx, @v) = split ' ', $linea;

my $ref = \@v;                      # una REFERENCIA al arreglo

print "valor=", $ref->[$idx], "\n";
```

**Lo que esta clase enseña en Perl.** `\@v` es **una referencia**, y como se explicó en la clase 097,
las referencias llegaron en Perl 5.0 (1994) y transformaron el lenguaje: **sin ellas no hay estructuras
anidadas, ni objetos, ni clausuras útiles**.

Una referencia de Perl es **un escalar que apunta a algo**, y el lenguaje distingue a qué:

```perl
\@a   \%h   \$x   \&f        # a arreglo, hash, escalar, subrutina
ref($r)                        # "ARRAY", "HASH", "CODE", "SCALAR", o la CLASE
$$r  $r->[0]  $r->{k}  $r->()   # desreferenciar
@$r  %$r  @{$r}[1..3]            # y las formas de bloque
```

**`ref($r)` devuelve el nombre de la clase si la referencia está bendecida** (clase 099), y por eso es
a la vez el operador de tipo y el de clase.

Y Perl expone la dirección, aunque no la aritmética:

```perl
use Scalar::Util qw(refaddr reftype blessed weaken);
refaddr($r)          # la dirección, como número
$r1 == $r2            # comparar referencias: funciona porque se numerizan (clase 101)
weaken($r)             # referencia DÉBIL: no cuenta para el conteo
```

**`weaken` es la pieza que resuelve el problema de los ciclos** (clases 097 y 128), y es obligatoria en
cualquier estructura con enlaces al padre.

Y Perl tiene una forma de indirección que ningún otro lenguaje de esta página comparte y que ya
apareció en la clase 085: **las referencias simbólicas**.

```perl
no strict 'refs';
my $nombre = "contador";
$$nombre = 5;                  # ¡asigna a la variable LLAMADA "contador"!
&{"main::$funcion"}();          # llamar a una función por su nombre
*{"main::nueva"} = sub { ... };  # DEFINIR una función en ejecución
```

**Una referencia simbólica es una cadena usada como nombre de variable**, resuelta en la tabla de
símbolos. Es exactamente la indirección de M (clase 085), y por eso `use strict 'refs'` la prohíbe:
**es potente, es la base de los generadores de accesores de CPAN, y hace el código imposible de
analizar**.

Que `strict` la desactive por defecto desde 1994 dice que la comunidad aprendió pronto la lección.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    int idx{};
    if (!(std::cin >> idx)) return 1;

    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};

    const int* p = v.data();          // puntero al primer elemento
    const int& r = v[idx];             // referencia a UNO concreto

    std::cout << "valor=" << *(p + idx) << '\n';
    static_cast<void>(r);
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene **punteros y referencias**, y la distinción es una de las
primeras cosas que hay que tener claras:

| | Puntero `T*` | Referencia `T&` |
|---|---|---|
| Puede ser nulo | **sí** | no (salvo con trucos) |
| Se puede reasignar | **sí** | no: se liga al crearse |
| Aritmética | **sí** | no |
| Sintaxis de uso | `*p`, `p->` | como el objeto |
| Puede no inicializarse | sí | **no** |

**Una referencia es un alias**; un puntero es una variable que contiene una dirección. La guía práctica:
**referencia si siempre hay un objeto, puntero si puede no haberlo** — y desde C++17,
`std::optional<T&>` no existe y para eso está el puntero o `std::reference_wrapper`.

Y C++ tiene la aritmética de punteros, que es a la vez su potencia y su mayor fuente de fallos:

```cpp
*(p + idx)        // exactamente lo mismo que p[idx]
p[idx]             // que es azúcar para *(p + idx)
idx[p]              // ¡y esto TAMBIÉN compila y funciona!
```

**`idx[p]` es legal** porque `a[b]` se define como `*(a + b)` y la suma es conmutativa. Es una rareza
que ilustra hasta qué punto los arreglos y los punteros son la misma cosa en C.

Y de ahí el problema central: **`p + idx` no comprueba nada**. Salir del arreglo es comportamiento
indefinido, y es la causa directa de una fracción enorme de los fallos de seguridad de los últimos
treinta años (clase 089).

C++ moderno lo mitiga con capas que llevan el tamaño:

```cpp
v.at(idx)                      // comprueba y lanza
std::span<const int> s{v};      // C++20: puntero + tamaño, en un tipo
s[idx]                           // sigue sin comprobar, pero s.size() existe
std::ranges::subrange            // y las ranges llevan los dos extremos
```

Y las herramientas de la clase 128 —AddressSanitizer, `-D_GLIBCXX_ASSERTIONS`— convierten el
comportamiento indefinido en un error diagnosticado.

Merece cerrar con la comparación que recorre esta clase: **Fortran con `target`, Ada con `aliased` y
Rust con la propiedad restringen quién puede tener una referencia. C++ no restringe nada, y por eso su
modelo es a la vez el más potente y el que más ha costado.**

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

dcl-pi REFEREN;
  entrada char(200) const;
end-pi;

dcl-s texto  varchar(200);
dcl-s tok    varchar(20) inz('');
dcl-s c      char(1);
dcl-s i      int(10);
dcl-s nt     int(10) inz(0);
dcl-s idx    int(10) inz(0);
dcl-s v      int(10) dim(100);
dcl-s p      pointer;
dcl-s celda  int(10) based(p);

texto = %trimr(entrada);

for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      if nt = 0;
        idx = %int(tok);
      else;
        v(nt) = %int(tok);
      endif;
      nt += 1;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

// p apunta al elemento pedido: `celda` lee a traves del puntero
p = %addr(v(idx + 1));

dsply ('valor=' + %char(celda));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG tiene punteros desde ILE, y este programa usa las dos piezas
que los hacen funcionar:

```rpgle
dcl-s p pointer;
dcl-s celda int(10) based(p);      // una variable SIN memoria propia
p = %addr(v(idx + 1));               // apuntar a un elemento
```

**`based(p)` superpone la declaración a donde apunte `p`**, y `%addr` obtiene la dirección de algo. Es
el mismo modelo que PL/I y COBOL, y viene del mismo sitio.

Y RPG tiene un uso de los punteros que es propio de la plataforma y muy frecuente: **acceder a los
parámetros de las APIs del sistema**.

```rpgle
dcl-pr listarObjetos extpgm('QUSLOBJ');
  espacio char(20) const;
  formato char(8) const;
  ...
end-pr;

// el resultado llega en un *USRSPC, y se navega con punteros:
p = %addr(cabecera) + desplazamiento;
```

**Las APIs de IBM i devuelven estructuras de longitud variable en un espacio de usuario**, con una
cabecera que dice dónde empieza cada parte. Navegarlas es aritmética de punteros, y es una de las pocas
cosas para las que un programador de RPG los usa a diario.

Y aquí RPG comparte el agujero de C que la clase 128 señalaba: **`based` sobre un `dim` grande no
comprueba índices**.

```rpgle
dcl-s tabla int(10) dim(32767) based(p);   // el dim NO reserva ni comprueba
```

Es la salida a la comprobación automática de índices que RPG sí tiene con tablas normales (clase 089),
y la razón de que la guía de la plataforma sea usar punteros solo cuando hace falta.

Y hay un tipo de puntero propio de IBM i que conviene nombrar porque no existe en ningún otro sitio:
**los punteros a espacio con autoridad**, de 128 bits y gestionados por el sistema (clase 125). **Un
programa no puede fabricar uno**, así que **el desbordamiento clásico de C no puede alcanzar memoria
ajena** — seguridad impuesta por la arquitectura, en 1978.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 referen: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare v(100) fixed binary(31);
    declare (i, nt, idx) fixed binary(31);
    declare p pointer;
    declare celda fixed binary(31) based(p);

    get edit (linea) (a(200));
    linea = trim(linea);
    nt = 0; idx = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             if nt = 0 then idx = tok;
             else v(nt) = tok;
             nt = nt + 1;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    p = addr(v(idx + 1));        /* la direccion del elemento */

    put skip list ('valor=' || trim(char(celda)));

 end referen;
```

**Lo que esta clase enseña en PL/I.** Aquí está el origen de casi todo lo de esta página: **PL/I
introdujo el puntero de alto nivel en 1964**, con las tres piezas que después copiaron todos.

```pli
 declare p pointer;                        /* el TIPO puntero */
 declare 1 nodo based(p), 2 valor ...;      /* declaración SIN memoria */
 p = addr(x);                                /* la dirección de algo */
 allocate nodo set(p);                        /* reservar y apuntar */
 p -> valor = 1;                                /* acceso a través del puntero */
```

**La flecha `->`, `based` y `addr` están aquí primero.** C tomó la flecha; COBOL y RPG tomaron `BASED`
y `%addr`.

Y PL/I añade dos formas de indirección que **no** pasaron a C y que merecen conocerse:

**Los punteros con desplazamiento (`offset`)**, que son punteros relativos a un área (clase 128):

```pli
 declare mi_area area(100000);
 declare o offset(mi_area);

 allocate nodo in(mi_area) set(p);
 o = pointer_to_offset(p, mi_area);      /* guardar como DESPLAZAMIENTO */
```

**Un `offset` sigue siendo válido si el área se mueve o se escribe en un fichero y se vuelve a leer**,
porque no es una dirección absoluta.

Esa es la propiedad que hoy tienen los formatos de datos binarios modernos —FlatBuffers, Cap'n Proto—
y las estructuras en ficheros mapeados: **punteros relativos para que el dato sea reubicable**.

**Y las variables de etiqueta y de entrada** (clases 085 y 108): punteros a **código**, no a datos.

```pli
 declare destino label;
 declare f entry (fixed binary(31)) returns (fixed binary(31)) variable;
```

Entre las cinco —puntero, `offset`, `label`, `entry` y `area`—, PL/I tiene el sistema de indirección
más completo de esta página, y de 1964.

Y su problema es el previsible y ya señalado varias veces: **ninguna de esas indirecciones se
comprueba**. Un puntero mal usado corrompe memoria, una variable de etiqueta puede saltar a un marco
que ya no existe, y una `entry` sin inicializar salta a una dirección arbitraria.

Es la diferencia con Ada de esta misma clase: **las mismas capacidades, cuarenta años después, con
comprobación**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
REFEREN ; Referencias y punteros -- clase 129
 read linea
 set idx = $piece(linea, " ", 1)
 ; en M no hay punteros: se accede por subindice
 write "valor=", $piece(linea, " ", idx + 2), !
 quit
```

**Lo que esta clase enseña en M.** **En M no hay punteros, ni referencias, ni direcciones, ni identidad
de objetos.** Es el lenguaje con el modelo más simple de esta página, y esa simplicidad tiene
consecuencias que ya han aparecido varias veces:

- **No hay punteros colgantes** (clase 129).
- **No hay estructuras compartidas** (clases 101, 102 y 114): `set a = b` copia.
- **No hay que preguntarse nunca si una modificación afectará a otro sitio.**

Lo que sí tiene M es **una indirección más radical que cualquier puntero**: la de la clase 085.

```mumps
 set nombre = "^PAC(123,""nombre"")"
 set x = @nombre                      ; leer a través del NOMBRE construido
 set @nombre = "Ada"                   ; y escribir
```

**`@` toma una cadena y la usa como referencia a una variable o a un global.** Es una referencia
simbólica —lo mismo que en Perl con `no strict 'refs'`— y es el mecanismo con el que se construyen las
capas genéricas de VistA.

Y hay una segunda forma, que es lo más parecido a pasar una referencia: **el punto en la llamada**
(clase 109).

```mumps
 do sub(.x)          ; el punto pasa la variable POR REFERENCIA
```

Ese punto es toda la diferencia entre copiar y compartir en M, y **es la única forma de que una rutina
modifique un dato del llamante**.

Y aquí conviene una precisión que esta clase permite hacer y que da la medida del modelo: **en M, la
identidad de un dato es su NOMBRE, no su dirección**.

```mumps
 ^PAC(123)           ; este dato ES este nombre
```

No hay dos formas de llegar al mismo sitio: **el camino en el árbol es la identidad**. Eso hace
imposibles los grafos con enlaces cruzados en el sentido habitual, y a cambio hace que **todo dato sea
direccionable con una cadena, guardable, transmisible y persistente**.

Es la misma decisión que Tcl con los nombres de comando de esta clase, llevada al modelo de datos
entero — y es lo que permite que un *global* sea a la vez estructura de programa y fila de base de
datos.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes idx v |

partes := stdin nextLine substrings.
idx := (partes at: 1) asNumber.
v := (partes copyFrom: 2 to: partes size) collect: [ :cada | cada asNumber ].

Transcript show: 'valor=', (v at: idx + 1) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** **En Smalltalk todo es una referencia**, y no hay ninguna
otra cosa: no hay tipos valor, no hay punteros y no hay direcciones (clase 128).

```smalltalk
| a b |
a := OrderedCollection new.
b := a.                        "b y a son EL MISMO objeto"
b add: 1.
a size.                         "1 -- claro"
a == b.                          "true: la misma identidad (clase 101)"
```

Y como todo es referencia, **la distinción de la clase 101 —`=` frente a `==`— es la que importa**, y
Smalltalk la resuelve con un carácter.

Lo que Smalltalk no permite es **manipular la dirección**. Y aun así, la reflexión llega más lejos que
en cualquier otro lenguaje de esta página:

```smalltalk
objeto identityHash.                  "un identificador estable del objeto"
objeto become: otro.                   "¡INTERCAMBIAR las identidades!"
objeto chasePointers.                   "quién apunta a este objeto"
objeto instVarAt: 1.                     "leer un campo por POSICIÓN"
objeto instVarAt: 1 put: valor.           "y escribirlo"
```

**`become:` es la operación más asombrosa del lenguaje**: intercambia dos objetos **en todas las
referencias del sistema a la vez**. Todo lo que apuntaba a `a` pasa a apuntar a `b` y viceversa,
instantáneamente.

Con eso se implementan cosas que en otros lenguajes son imposibles:

- **Migrar instancias al cambiar una clase** (clase 111): se crea la versión nueva y se hace `become:`.
- **Los proxies transparentes** (clase 122): un objeto ligero que, cuando llega el dato real, se
  convierte en él con `become:` sin que nadie se entere.
- **Crecer una colección** sustituyendo el objeto entero.

Es la indirección total: **el sistema puede reescribir cada referencia del montón**, porque conoce
todas.

Y esa capacidad depende exactamente de lo que esta clase discute: **como el programa no puede tener
direcciones crudas, el sistema es libre de mover los objetos**. Un recolector que compacta, un
`become:` que reescribe punteros y un depurador que inspecciona todo **solo son posibles si nadie
guarda direcciones a escondidas**.

Es el argumento del cierre en su forma más fuerte: **renunciar al puntero crudo es lo que compra todo
lo demás**.

---

## Y de vuelta a la clase

Lo transferible: **una referencia es un nombre de algo que vive en otro sitio, y todos los problemas
vienen de ahí**: puede apuntar a lo que ya no existe, dos referencias pueden cambiar lo mismo sin
saberlo, y comparar referencias no es comparar valores (clase 101). Los lenguajes modernos no
eliminaron el concepto —lo necesitan— sino que **restringieron quién puede tener una y hasta cuándo**:
la propiedad de Rust, los accesos de Ada y `allocatable` de Fortran son tres formas de la misma idea.

⏮️ [Volver a la clase 129](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
