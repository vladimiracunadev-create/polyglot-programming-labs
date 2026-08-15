# -*- coding: utf-8 -*-
"""Parte 8, lote G — clases 129 y 130. Ver `vivos_parte8.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 129 — Referencias, punteros y direcciones
# ---------------------------------------------------------------------------
SPECS["129"] = dict(
    gancho="""
Acceder al elemento `i` de una colección. Detrás de esa operación trivial está la pregunta que separa
a estos doce lenguajes: **¿existe la dirección de memoria como valor manipulable?** En COBOL, RPG,
PL/I, C++ y Fortran sí; en Ada existe **con comprobaciones que impiden el puntero colgante**; y en
Tcl, Lisp, Smalltalk y M **no existe en absoluto** — y sus programas funcionan igual.
""",
    porque="""
Aquí el concepto es la **indirección**, y estos lenguajes lo enseñan porque cubren desde el puntero
crudo hasta su ausencia total. **PL/I inventó el puntero de alto nivel en 1964** y de ahí lo tomaron
COBOL, RPG y —en espíritu— C. **Ada lo acotó**: sus accesos llevan comprobación de accesibilidad
(clase 083) y pueden declararse `not null` (clase 116). **Fortran distingue `pointer` de
`allocatable`** por el aliasing (clase 128).

Y los que no lo tienen enseñan lo contrario: **en M, en Tcl y en Smalltalk no hay forma de que dos
nombres designen la misma cosa mutable** —o la hay solo por objetos— y eso elimina una clase entera de
errores.
""",
    cierre="""
Lo transferible: **una referencia es un nombre de algo que vive en otro sitio, y todos los problemas
vienen de ahí**: puede apuntar a lo que ya no existe, dos referencias pueden cambiar lo mismo sin
saberlo, y comparar referencias no es comparar valores (clase 101). Los lenguajes modernos no
eliminaron el concepto —lo necesitan— sino que **restringieron quién puede tener una y hasta cuándo**:
la propiedad de Rust, los accesos de Ada y `allocatable` de Fortran son tres formas de la misma idea.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let* ((idx (read))
       (v (coerce (loop for x = (read *standard-input* nil nil)
                        while x collect x)
                  'vector)))
  (format t "valor=~D~%" (aref v idx)))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
set partes [split [string trim $linea]]

set idx [lindex $partes 0]
set v [lrange $partes 1 end]

puts "valor=[lindex $v $idx]"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($idx, @v) = split ' ', $linea;

my $ref = \\@v;                      # una REFERENCIA al arreglo

print "valor=", $ref->[$idx], "\\n";
""", """
**Lo que esta clase enseña en Perl.** `\\@v` es **una referencia**, y como se explicó en la clase 097,
las referencias llegaron en Perl 5.0 (1994) y transformaron el lenguaje: **sin ellas no hay estructuras
anidadas, ni objetos, ni clausuras útiles**.

Una referencia de Perl es **un escalar que apunta a algo**, y el lenguaje distingue a qué:

```perl
\\@a   \\%h   \\$x   \\&f        # a arreglo, hash, escalar, subrutina
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
"""),
        "cpp": ("""
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

    std::cout << "valor=" << *(p + idx) << '\\n';
    static_cast<void>(r);
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
REFEREN ; Referencias y punteros -- clase 129
 read linea
 set idx = $piece(linea, " ", 1)
 ; en M no hay punteros: se accede por subindice
 write "valor=", $piece(linea, " ", idx + 2), !
 quit
""", """
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
"""),
        "smalltalk": ("""
| partes idx v |

partes := stdin nextLine substrings.
idx := (partes at: 1) asNumber.
v := (partes copyFrom: 2 to: partes size) collect: [ :cada | cada asNumber ].

Transcript show: 'valor=', (v at: idx + 1) printString; cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 130 — Gestión manual de memoria
# ---------------------------------------------------------------------------
SPECS["130"] = dict(
    gancho="""
Reservar `n` enteros, usarlos y liberarlos. **Cinco de estos lenguajes te hacen escribir la
liberación** —COBOL, RPG, PL/I, C++ con punteros crudos y Fortran con `pointer`— y sus ecosistemas
llevan décadas conviviendo con las consecuencias. Y aquí hay una lección que la industria tardó
cuarenta años en aceptar: **la mayoría de esos lenguajes NO tienen fugas en producción, y no es por
disciplina — es porque casi no reservan**.
""",
    porque="""
Aquí el concepto es **quién libera y cuándo**, y estos lenguajes lo enseñan porque muestran las cuatro
estrategias que funcionan. **No reservar**: COBOL y RPG clásicos, con memoria estática (clase 128).
**Liberar por ámbito**: `allocatable` de Fortran, los tipos controlados de Ada, RAII en C++. **Liberar
por región**: los grupos de activación de IBM i, las áreas de PL/I, `GETMAIN` de CICS. **Y liberar a
mano**: lo que queda, y donde están los errores.

La cuarta es la que produce **fuga, doble liberación y uso tras liberar** — tres fallos que las otras
tres estrategias eliminan por construcción.
""",
    cierre="""
Lo transferible: **liberar a mano no falla por descuido, falla por caminos**. El `free` está escrito, y
hay un `return` anticipado, una excepción o una rama de error que no pasa por ahí. Por eso todas las
soluciones que funcionan —RAII, `defer`, `with`, ámbitos, regiones— tienen la misma forma: **atar la
liberación a algo que ocurre siempre**. Si te descubres escribiendo `free` en tres sitios distintos de
la misma función, ese es el síntoma.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. MANUAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4) COMP.
01  I       PIC 9(4) COMP.
01  SUMA    PIC 9(9) COMP VALUE 0.
01  TABLA.
    05  ELEM  PIC 9(9) COMP OCCURS 1 TO 1000 TIMES DEPENDING ON N.
01  ED-N    PIC Z(3)9.
01  ED-S    PIC Z(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE I TO ELEM(I)
        ADD I TO SUMA
    END-PERFORM

    MOVE N    TO ED-N
    MOVE SUMA TO ED-S
    DISPLAY "reservado=" FUNCTION TRIM(ED-N)
            " suma=" FUNCTION TRIM(ED-S)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Este programa **no reserva nada**, y esa es la respuesta de COBOL
a esta clase: **la mejor gestión manual de memoria es la que no hace falta**.

Como se dijo en la clase 128, la `WORKING-STORAGE` es estática y su tamaño se conoce al compilar. **No
hay `free` que olvidar porque no hay `malloc` que escribir.**

Y ese modelo, que parece una limitación, es lo que permite garantizar el comportamiento de un sistema
con miles de transacciones por segundo: **el consumo de memoria de cada tarea es una constante
conocida**.

Cuando sí hace falta reservar, COBOL usa lo de la clase 128:

```cobol
ALLOCATE 1000 CHARACTERS RETURNING PTR
FREE PTR
EXEC CICS GETMAIN SET(PTR) LENGTH(1000) END-EXEC
EXEC CICS FREEMAIN DATAPOINTER(PTR) END-EXEC
```

Y ahí está lo que hace distinto al mundo COBOL, y es la tercera estrategia del cierre de esta clase:
**la liberación por región**.

**Todo lo que reserva una transacción CICS se libera al terminar la transacción**, con o sin `FREEMAIN`,
haya fallado o no. La unidad de trabajo tiene un final, y ese final limpia.

Con transacciones que duran milisegundos, **una fuga dentro de una transacción es irrelevante**: se
recoge sola en cuanto termina.

Eso explica una observación que sorprende a quien viene de otros entornos: **los sistemas COBOL no
tienen problemas de fugas de memoria**, pese a estar escritos en un lenguaje sin recolector y con
liberación manual.

No es disciplina: **es que la arquitectura hace que la fuga no tenga tiempo de acumularse**.

Y es exactamente el mismo argumento que hoy se usa a favor de los procesos efímeros, los contenedores
que se reinician y las funciones sin servidor: **si el proceso vive poco, la gestión de memoria importa
menos**.
"""),
        "fortran": ("""
program manual
   implicit none
   integer, pointer :: v(:)         ! puntero: hay que liberar A MANO
   integer :: n, i, suma, ierr

   read(*, *) n

   allocate(v(n), stat=ierr)
   if (ierr /= 0) then
      write(*, '(A)') 'sin memoria'
      stop 1
   end if

   suma = 0
   do i = 1, n
      v(i) = i
      suma = suma + i
   end do

   write(*, '(A,I0,A,I0)') 'reservado=', n, ' suma=', suma

   deallocate(v)                    ! obligatorio con `pointer`
   nullify(v)
end program manual
""", """
**Lo que esta clase enseña en Fortran.** Este programa usa **`pointer` en vez de `allocatable`** para
que la liberación sea obligatoria, y así se ve la diferencia que la clase 128 explicaba:

```fortran
integer, pointer     :: p(:)    ! hay que deallocate: si no, FUGA
integer, allocatable :: a(:)     ! se libera SOLO al salir del ámbito
```

**Esa es toda la diferencia**, y es la razón de la guía moderna de Fortran: **usa `allocatable` salvo
que necesites alias o estructuras enlazadas**.

Y `stat=ierr` es la otra pieza que esta clase debe destacar:

```fortran
allocate(v(n), stat=ierr)
if (ierr /= 0) ...
deallocate(v, stat=ierr)
```

**Sin `stat=`, un fallo de reserva termina el programa.** En un cálculo de ocho horas eso es
inaceptable, y `stat=` permite reducir el tamaño del problema y seguir, o guardar el estado antes de
morir.

Y Fortran tiene una construcción propia y muy útil para el problema del cierre de esta clase —**los
caminos que no pasan por el `deallocate`**—:

```fortran
block
   integer, allocatable :: temporal(:)
   allocate(temporal(1000000))
   ...
end block                       ! se libera AQUÍ, salga por donde salga
```

**El `block`** de Fortran 2008 (clase 103) da un ámbito interno, y **los `allocatable` declarados en él
se liberan al salir**, incluido por `exit`, `return` o `error stop`.

Es liberación por ámbito con la sintaxis de un bloque, y es la respuesta idiomática al problema de esta
clase.

Y para diagnosticar fugas cuando se usan punteros, el ecosistema tiene lo esperable:

```bash
valgrind --leak-check=full ./programa
gfortran -fsanitize=address
gfortran -fcheck=pointer          # detecta punteros no asociados
```

**`-fcheck=pointer`** comprueba en ejecución que un puntero esté asociado antes de usarlo, que es
exactamente el fallo que `allocatable` hace imposible.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Unchecked_Deallocation;

procedure Manual is
   type Vector is array (Positive range <>) of Integer;
   type Ref is access Vector;

   procedure Liberar is new Ada.Unchecked_Deallocation (Vector, Ref);

   N    : Integer;
   V    : Ref;
   Suma : Integer := 0;
begin
   Get (N);

   V := new Vector (1 .. N);

   for I in 1 .. N loop
      V (I) := I;
      Suma := Suma + I;
   end loop;

   Put ("reservado=");  Put (N,    Width => 1);
   Put (" suma=");      Put (Suma, Width => 1);
   New_Line;

   Liberar (V);          --  V queda en null automáticamente
end Manual;
""", """
**Lo que esta clase enseña en Ada.** `Ada.Unchecked_Deallocation` tiene dos detalles que lo hacen más
seguro que un `free`, y merece verlos:

**Primero: pone el puntero a `null`.**

```ada
Liberar (V);        --  V pasa a ser null, NO queda colgado
```

**El parámetro es `in out`**, así que después de liberar, el puntero no apunta a memoria muerta. En C,
`free(p)` deja `p` apuntando a memoria liberada, y usarlo es el clásico *use after free*.

**Y segundo: está tipado.** El genérico se instancia con el tipo del objeto y el del acceso, así que
**no se puede liberar un puntero de otro tipo**.

Y Ada ofrece las tres estrategias del cierre de esta clase, y su cultura prefiere las tres primeras:

**No reservar** — con `pragma Restrictions (No_Allocators)` en sistemas certificados (clase 128).

**Liberar por ámbito** — con los **tipos controlados** (clase 103):

```ada
type Recurso is new Ada.Finalization.Controlled with ...;
overriding procedure Finalize (R : in out Recurso);
```

`Finalize` se ejecuta **al salir del ámbito, incluso si se propaga una excepción**. Es RAII, y llegó a
Ada en 1983 — once años antes de que C++ le pusiera nombre.

**Liberar por región** — con los ***storage pools*** (clase 128):

```ada
for Ref'Storage_Pool use Mi_Arena;
```

Un gestor propio por tipo de acceso, con el que se implementa una arena que suelta todo de golpe.

Y hay una comprobación que Ada hace y que casi nadie más: **al terminar un ámbito con un
`Storage_Pool` propio, se puede liberar el pool entero**, con lo que las fugas dentro de él dejan de
importar.

Es la misma idea que las transacciones de CICS de esta clase y que los grupos de activación de IBM i:
**si la región tiene un final, la fuga tiene fecha de caducidad**.
"""),
        "pascal": ("""
program Manual;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  V: PInteger;
  N, I, Suma: Integer;
  Q: PInteger;

begin
  Read(N);

  GetMem(V, N * SizeOf(Integer));      { reservar a mano }

  Suma := 0;
  Q := V;
  for I := 1 to N do
  begin
    Q^ := I;
    Suma := Suma + I;
    Inc(Q);                              { requiere {$POINTERMATH} o PInteger }
  end;

  WriteLn('reservado=', IntToStr(N), ' suma=', IntToStr(Suma));

  FreeMem(V);                            { liberar a mano }
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal tiene tres pares de reserva y liberación, y usarlos
cruzados es un error clásico:

```pascal
New(P);      Dispose(P);         { tipado: reserva SizeOf del tipo (clase 128) }
GetMem(P, T); FreeMem(P);          { sin tipo: como malloc }
Obj := TC.Create;  Obj.Free;        { objetos, con constructor y destructor }
```

**Mezclarlos —`New` con `FreeMem`, o `Create` con `Dispose`— produce corrupción del montón**, y es de
los errores más difíciles de diagnosticar del ecosistema.

Y el problema del cierre de esta clase —**los caminos que no pasan por la liberación**— tiene en Pascal
la solución canónica, que es la que se enseña desde el primer día:

```pascal
Obj := TClase.Create;
try
  ...                    { salga por donde salga }
finally
  Obj.Free;               { esto SIEMPRE se ejecuta }
end;
```

**`try...finally` es tan omnipresente en el código Delphi que se escribe sin pensar**, y es lo que
compensa la ausencia de destructores automáticos (clase 103).

Y hay dos alternativas que eliminan el problema:

```pascal
var I: IInterfaz;                { conteo de referencias: se libera SOLA }
var R: TRegistro;                 { valor: muere con el ámbito }
```

Free Pascal añadió además **los registros gestionados** en la versión 3.2, que son lo más cercano a
RAII que tiene el lenguaje:

```pascal
type
  TRecurso = record
    class operator Initialize(var R: TRecurso);   { constructor }
    class operator Finalize(var R: TRecurso);      { DESTRUCTOR automático }
  end;
```

**Con `Initialize` y `Finalize`, un registro se construye y se destruye solo al entrar y salir del
ámbito.** Es exactamente RAII de C++ y los tipos controlados de Ada, llegado a Pascal en 2020.

Y la herramienta que hizo por la calidad del código Delphi más que ninguna característica del lenguaje
es la de la clase 128: **FastMM**, que al terminar el programa **informa de cada fuga con la pila de
llamadas de dónde se reservó**.

Es la respuesta pragmática del cierre de esta clase: **si el lenguaje no libera solo, que al menos te
diga exactamente qué olvidaste**.
"""),
        "lisp": ("""
(let* ((n (read))
       (v (make-array n))
       (suma 0))
  (dotimes (i n)
    (setf (aref v i) (1+ i))
    (incf suma (1+ i)))
  ;; no hay que liberar: hay recolector de basura (clase 131)
  (format t "reservado=~D suma=~D~%" n suma))
""", """
**Lo que esta clase enseña en Common Lisp.** **En Lisp no hay gestión manual de memoria**, y esta clase
es el sitio para explicar por qué esa decisión, de 1959, fue tan influyente.

McCarthy inventó la recolección de basura porque **Lisp la necesitaba para existir**: un lenguaje que
construye y descarta listas constantemente no puede pedir al programador que libere cada *cons*.

Y esa decisión tuvo un coste que la industria tardó décadas en aceptar: **pausas impredecibles**. Es la
razón por la que Lisp no se usó en sistemas de tiempo real, y por la que los primeros recolectores
—que paraban el mundo— dieron mala fama al concepto.

Lo que Lisp sí ofrece es control sobre cuánto se reserva, que es la otra mitad del problema:

```lisp
(declare (dynamic-extent lista))          ; "no escapa": puede ir a la PILA (clase 128)
(make-array n :element-type 'double-float) ; vector compacto, sin punteros
(let ((*gc-inhibit* t)) ...)                ; en algunas implementaciones
(sb-ext:gc :gen 2)                           ; forzar la recolección de una generación
```

Y para la frontera con C, donde **sí hay que liberar a mano**, el ecosistema tiene CFFI (clase 129):

```lisp
(cffi:with-foreign-object (p :int 100)     ; se libera al salir del bloque
  ...)
(cffi:foreign-alloc :int :count 100)         ; y esto hay que foreign-free
```

**`with-foreign-object` es la macro que ata la liberación al ámbito** — la misma forma que
`with-open-file` (clase 103) y que todas las soluciones del cierre de esta clase.

Y es un ejemplo de lo que se dijo en la clase 107: **en Lisp, la solución a un problema del lenguaje es
una macro**. `unwind-protect` más una macro `with-` cubre cualquier recurso, y escribirla son diez
líneas.

Merece cerrar con una observación histórica: **las máquinas Lisp de los ochenta tenían recolección de
basura asistida por hardware**, con barreras de escritura implementadas en silicio. Cuando esas
máquinas desaparecieron, las técnicas pasaron al software — y hoy están en la JVM, en .NET y en Go.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set v {}
set suma 0
for {set i 1} {$i <= $n} {incr i} {
    lappend v $i
    incr suma $i
}

# no hay que liberar: conteo de referencias sobre valores inmutables
puts "reservado=$n suma=$suma"
""", """
**Lo que esta clase enseña en Tcl.** **En Tcl puro no existe la gestión manual de memoria**: el conteo
de referencias sobre valores inmutables (clase 128) libera todo automáticamente y sin ciclos posibles.

Donde sí existe —y es donde Tcl tiene sus fugas reales— es **en las extensiones escritas en C**:

```c
Tcl_Obj *obj = Tcl_NewIntObj(42);
Tcl_IncrRefCount(obj);     /* incrementar el contador */
...
Tcl_DecrRefCount(obj);      /* y decrementarlo: si llega a 0, se libera */
```

**Toda la API de C de Tcl gira alrededor de `Tcl_IncrRefCount` y `Tcl_DecrRefCount`**, y equivocarse
produce las dos caras del problema: **decrementar de más libera algo que todavía se usa; decrementar de
menos es una fuga**.

Y Tcl tiene reglas explícitas sobre quién posee qué —los objetos con contador cero son "frescos" y los
puede tomar quien los reciba— que están documentadas precisamente porque son la fuente de errores más
común al extender el lenguaje.

Para diagnosticarlo, Tcl se puede compilar con instrumentación (clase 128):

```tcl
memory info
memory active fugas.txt      ;# los bloques VIVOS, con fichero y línea de C
memory trace on
```

Y para los recursos que no son memoria —canales, ventanas, objetos— Tcl usa lo del cierre de esta
clase: **atar la liberación a algo que ocurre siempre**.

```tcl
try { ... } finally { close $canal }            ;# Tcl 8.6
trace add variable v unset { ... }               ;# al desaparecer la variable
oo::class create R { destructor { ... } }         ;# destructor de objeto
interp alias / interp delete                       ;# al morir el intérprete
```

**`trace add variable ... unset`** es la más peculiar: **engancha código a la desaparición de una
variable**, incluida la salida del procedimiento. Con eso se construye un destructor sin que el
lenguaje tenga destructores (clase 103).

Y hay un mecanismo de región muy propio de Tcl: **crear un intérprete secundario y destruirlo**.

```tcl
set i [interp create]
$i eval { ... }              ;# todo lo que cree vive AHÍ
interp delete $i              ;# y desaparece de golpe
```

Es un *arena allocator* a escala de intérprete, y se usa para ejecutar código no confiable con límites
(clase 153).
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum0);

my $n = <STDIN>;
chomp $n;

my @v = (1 .. $n);
my $suma = sum0(@v);

# no hay que liberar: conteo de referencias
print "reservado=$n suma=$suma\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl libera por **conteo de referencias**, y eso da la propiedad
que las clases 103 y 128 destacaban: **liberación determinista**, en el momento exacto en que la
última referencia desaparece.

Por eso `DESTROY` en Perl sirve para cerrar ficheros y soltar bloqueos, cosa que con un recolector de
basura sería un error de diseño.

Y por eso Perl **sí tiene un problema de gestión manual**: **los ciclos**.

```perl
my $a = {};
$a->{yo} = $a;          # ciclo: NUNCA se libera
```

La solución es explícita y hay que acordarse de ella:

```perl
use Scalar::Util qw(weaken);
$hijo->{padre} = $nodo;
weaken($hijo->{padre});      # no cuenta para el contador
```

**Cualquier estructura con enlaces al padre —árboles, grafos, observadores— necesita `weaken`**, y
olvidarlo es la fuga clásica de Perl.

Y las herramientas para encontrarla son de las mejores de esta página (clase 128):

```perl
use Devel::Cycle;  find_cycle($estructura);     # ENCONTRAR el ciclo
use Devel::Leak;                                  # contar SVs vivos
use Test::Memory::Cycle;  memory_cycle_ok($obj);   # como PRUEBA automática
```

**`Test::Memory::Cycle` convierte la ausencia de ciclos en una prueba unitaria** — es la forma correcta
de atacar el problema: **no confiar en la disciplina, comprobarlo en CI**.

Y para la frontera con C, donde Perl sí gestiona a mano, están `XS` y `Inline::C` (clase 126), con las
macros de gestión de referencias `SvREFCNT_inc` y `SvREFCNT_dec` — el mismo modelo que Tcl de esta
clase, y con los mismos errores posibles.

Es un patrón que esta clase deja claro: **los lenguajes con conteo de referencias tienen dos zonas —el
código propio, donde no hay que hacer nada, y la extensión en C, donde hay que hacerlo todo**.
"""),
        "cpp": ("""
#include <iostream>
#include <memory>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    //  reserva dinámica SIN delete: unique_ptr libera al salir
    auto v = std::make_unique<int[]>(n);

    long long suma = 0;
    for (int i = 0; i < n; ++i) {
        v[i] = i + 1;
        suma += i + 1;
    }

    std::cout << "reservado=" << n << " suma=" << suma << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** El programa reserva en el montón y **no tiene `delete`**, y esa es
toda la lección: **en C++ moderno, escribir `delete` a mano es la señal de que algo está mal**.

La progresión histórica es la de esta clase entera:

```cpp
int* v = new int[n];  ...  delete[] v;      // 1985: a mano, con todos los riesgos
std::vector<int> v(n);                        // 1998: el contenedor libera
auto v = std::make_unique<int[]>(n);           // 2014: propiedad única explícita
```

Y el problema del cierre —**los caminos que no pasan por el `delete`**— es especialmente grave en C++
por una razón concreta: **las excepciones**.

```cpp
int* v = new int[n];
procesar(v);              // si esto LANZA...
delete[] v;                // ...esto no se ejecuta: FUGA
```

**Ese fue el problema que motivó RAII** (clase 103): con excepciones, cualquier línea puede ser una
salida, y un `delete` al final no basta.

Los tres errores clásicos de la gestión manual, y qué los elimina:

| Error | Qué pasa | Qué lo elimina |
|---|---|---|
| Fuga | la memoria no se devuelve | RAII, contenedores |
| Doble liberación | corrupción del montón | propiedad única |
| Uso tras liberar | lectura de basura o peor | propiedad y tiempos de vida |

Y las herramientas que los detectan son las de la clase 128, con una nota sobre cuál usar:

```bash
valgrind --leak-check=full        # completo y LENTO (10-50x)
g++ -fsanitize=address             # rápido (2x), detecta también use-after-free
g++ -fsanitize=leak                 # solo fugas, muy barato
```

**AddressSanitizer es hoy la herramienta por defecto**, y debería estar activada en la compilación de
las pruebas de cualquier proyecto en C++.

Y hay una advertencia sobre `new[]` y `delete[]` que esta clase debe dejar: **hay que emparejarlos
correctamente**.

```cpp
int* p = new int[10];
delete p;              // ¡MAL! comportamiento indefinido: falta []
```

Es un error que no da síntomas inmediatos y que corrompe el montón. Con `make_unique<int[]>` no puede
ocurrir, porque el tipo lleva la información.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi MANUAL;
  n int(10) const;
end-pi;

dcl-s p     pointer;
dcl-s v     int(10) dim(1000) based(p);
dcl-s i     int(10);
dcl-s suma  int(20) inz(0);

p = %alloc(n * 4);                 // RESERVAR

for i = 1 to n;
  v(i) = i;
  suma += i;
endfor;

dsply ('reservado=' + %char(n) + ' suma=' + %char(suma));

dealloc p;                          // LIBERAR
p = *null;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG tiene `%alloc` y `dealloc`, y la plataforma tiene la respuesta
de la clase 128 que hace que las fugas importen poco: **los grupos de activación**.

```text
RCLACTGRP ACTGRP(MIAPP)      -- libera TODO lo del grupo
```

Y ahí está el punto que conecta con COBOL y CICS de esta misma clase: **la unidad de trabajo tiene un
final, y ese final limpia**.

Además, RPG tiene una construcción específica para el problema del cierre —los caminos que no pasan por
la liberación—:

```rpgle
monitor;
  p = %alloc(1000);
  procesar(p);
on-error;
  // manejar el error
endmon;
dealloc(n) p;        // el (n) permite liberar aunque p sea nulo
```

**`monitor`/`on-error`/`endmon` es el `try`/`catch` de RPG** (llegó con V5R1), y `dealloc(n)` con el
operando extendido **no falla si el puntero es nulo** — es el `Free` de Delphi de esta misma clase.

Y hay tres capacidades de la plataforma que conviene nombrar porque cubren lo que el lenguaje no:

**Primera: `%realloc` conserva el contenido.**

```rpgle
p = %realloc(p : nuevo_tamano);
```

Con la trampa clásica de C: **si falla, el puntero original se pierde**. La forma segura es usar una
variable temporal.

**Segunda: la memoria de un grupo de activación se puede consultar.**

```text
DSPJOB -> opción 16: almacenamiento asignado por grupo de activación
```

**Ver cuánta memoria ha reservado cada grupo, desde fuera y sin detener el trabajo.** Es la
observabilidad de la clase 142, aplicada a la memoria.

**Y tercera: los espacios de usuario** (clase 128), que son objetos del sistema con nombre, persistentes
y de hasta 16 MB — memoria que **sobrevive al trabajo que la creó** y que hay que borrar con
`DLTUSRSPC`.

Ahí sí hay una fuga posible de verdad, y es de las pocas que un sistema IBM i puede acumular: **objetos
temporales que nadie borra**. La herramienta para encontrarlos es una consulta SQL sobre
`QSYS2.OBJECT_STATISTICS` (clase 117).
"""),
        "pli": ("""
 manual: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare suma fixed binary(31) initial(0);
    declare p pointer;
    declare v(1000) fixed binary(31) based(p);

    get list (n);

    allocate v set(p);                  /* RESERVAR */

    do i = 1 to n;
       v(i) = i;
       suma = suma + i;
    end;

    put skip list ('reservado=' || trim(char(n)) ||
                   ' suma=' || trim(char(suma)));

    free v;                              /* LIBERAR */

 end manual;
""", """
**Lo que esta clase enseña en PL/I.** PL/I inventó `allocate` y `free` en 1964 (clases 128 y 129), y con
ellos **inventó también los problemas**: la fuga, la doble liberación y el uso tras liberar existen
desde entonces.

Y PL/I tiene **cuatro clases de almacenamiento** (clase 127), que son cuatro respuestas distintas a
esta clase:

| Clase | Quién libera |
|---|---|
| `static` | nadie: existe siempre |
| `automatic` | **el ámbito**, al salir |
| `controlled` | el programador, con `free` — y es una **pila** |
| `based` | el programador, con `free` |

**`controlled` es el caso interesante**, ya visto en la clase 090: cada `allocate` apila una generación
y cada `free` desapila. Eso hace que la liberación sea **más fácil de emparejar** —es una pila, no un
grafo— y `allocation(x)` dice cuántas generaciones quedan.

Y PL/I tiene la mejor respuesta de esta página al problema del cierre, ya nombrada en la clase 128:
**las áreas**.

```pli
 declare mi_area area(100000);
 allocate nodo in(mi_area) set(p);
 ...
 free mi_area;              /* libera TODO lo de dentro, de golpe */
```

**Liberar el área libera todo lo reservado dentro**, sin recorrer ni emparejar nada. Es un *arena
allocator* con sintaxis del lenguaje, en 1964, y es exactamente lo que hoy se recomienda para
estructuras con muchos objetos pequeños de vida común.

Y PL/I añade el manejo de condiciones para los fallos de reserva (clases 103 y 116):

```pli
 on condition(storage) begin;
    put list('sin memoria: liberando cachés');
    call liberar_caches();
    /* y se puede REANUDAR, reintentando la reserva */
 end;
```

**Un manejador de "sin memoria" que puede liberar cachés y reanudar** es algo que ni C, ni C++, ni Java
ofrecen de forma directa — en Java, `OutOfMemoryError` llega cuando ya casi no se puede hacer nada.

Es una capacidad que viene de que las condiciones de PL/I **no desenrollan la pila** (clase 116), y es
otro caso de una buena idea que no se difundió.
"""),
        "mumps": ("""
MANUAL ; Gestion manual de memoria -- clase 130
 read n
 kill v
 set suma = 0
 for i=1:1:n set v(i) = i, suma = suma + i
 write "reservado=", n, " suma=", suma, !
 kill v                              ; liberar: borrar el arbol
 quit
""", """
**Lo que esta clase enseña en M.** **En M no hay gestión manual de memoria en el sentido de esta
clase**: no hay reserva, así que no hay `free` que olvidar (clase 128).

Lo que hay es `kill`, que **borra un nombre y todo su subárbol**:

```mumps
 kill v              ; borra v y TODOS sus subíndices
 kill v(3)            ; solo esa rama
 kill (a, b)           ; TODO menos a y b -- el kill exclusivo
 kill ^DATOS            ; un global entero, en DISCO
```

Y ahí está la particularidad de M en esta clase: **`kill` sobre un *global* no libera memoria, libera
espacio de base de datos**, y eso tiene consecuencias que la memoria no tiene:

- **Es transaccional**: dentro de `tstart`/`tcommit`, se puede deshacer.
- **Es persistente**: lo borrado sigue borrado mañana.
- **Y el espacio no siempre vuelve al sistema operativo**: los bloques quedan libres dentro del fichero
  de base de datos, que **no encoge**.

Ese último punto es el equivalente de la fragmentación del montón, a escala de disco, y las
implementaciones tienen herramientas para ello —la reorganización de la base de datos en YottaDB e
IRIS— que son el equivalente de un compactador.

Y hay una fuga que sí existe en M y que es específica de su modelo: **las variables locales que nadie
mata**.

```mumps
 set temporal(i) = ...       ; sin `new` y sin `kill`
```

Como las variables locales son globales al proceso (clase 082), **una rutina que crea un array temporal
grande y no lo borra lo deja en memoria durante toda la sesión**. En un proceso de servidor que atiende
peticiones sin reiniciarse, eso se acumula.

De ahí que el idioma disciplinado de M sea **`new` al entrar o `kill` al salir**, y que el `kill`
exclusivo —`kill (a, b)`— exista precisamente para limpiar el espacio de nombres de golpe.

Es la misma forma que todas las soluciones del cierre de esta clase: **atar la limpieza a algo que
ocurre siempre**, y en M ese algo es el `quit` de la rutina con su `new`.
"""),
        "smalltalk": ("""
| n v suma |

n := stdin nextLine trimBoth asNumber.

v := OrderedCollection new.
suma := 0.
1 to: n do: [ :i | v add: i. suma := suma + i ].

"no hay que liberar: recolector de basura desde 1980"
Transcript
    show: 'reservado=', n printString;
    show: ' suma=', suma printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **En Smalltalk no hay gestión manual de memoria en
absoluto**: no existe `free`, no existe `delete` y no hay forma de liberar un objeto a mano.

Y esa ausencia es más radical que en Lisp o en Java, por lo que se explicó en la clase 129: **el sistema
puede mover los objetos** porque nadie guarda direcciones. Un recolector que compacta y `become:` solo
son posibles con esa garantía.

Lo que sí existe, y es la fuga que Smalltalk puede tener, es **la referencia olvidada**:

```smalltalk
| cache |
cache := Dictionary new.
cache at: clave put: objetoEnorme.        "y nadie lo quita"
```

Mientras algo lo referencie, el objeto vive. Y aquí está la particularidad del modelo de imagen (clase
041) que la clase 128 ya adelantaba: **la fuga sobrevive a la sesión**. Un objeto olvidado sigue en la
imagen mañana, y la imagen crece.

Por eso Smalltalk tiene las herramientas de diagnóstico más directas de esta página:

```smalltalk
MiClase allInstances size.            "¿cuántas hay vivas?"
objeto chasePointers.                  "¿QUIÉN me está reteniendo?"
Smalltalk garbageCollect.
SystemNavigation default allObjects size.
```

**`chasePointers` responde exactamente a la pregunta que se hace ante una fuga**, y en un mensaje. En
Java eso exige un volcado del montón y una herramienta de análisis; aquí abre un inspector.

Y para las cachés, Smalltalk tiene lo que hace falta:

```smalltalk
WeakArray with: objeto.               "referencia DÉBIL: no impide la recolección"
WeakKeyDictionary new.                 "cachés que no retienen (clase 095)"
objeto finalizationRegistry.
```

**`WeakKeyDictionary`** es la solución idiomática al problema de la caché que crece para siempre: **si
nadie más usa la clave, la entrada desaparece sola**.

Y hay un detalle histórico que cierra esta clase: **Smalltalk y Lisp fueron los dos sistemas donde se
desarrolló la recolección generacional**, y la razón fue la misma: **crean muchísimos objetos pequeños
y efímeros**.

La hipótesis de que "la mayoría de los objetos mueren jóvenes" se midió en programas Smalltalk, y de
ahí salieron los recolectores de Java, .NET y Go.
"""),
    },
)
