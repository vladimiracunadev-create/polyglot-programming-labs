# -*- coding: utf-8 -*-
"""Parte 6, lote L — clase 102. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 102 — Copia superficial frente a profunda; referencia frente a valor
# ---------------------------------------------------------------------------
SPECS["102"] = dict(
    gancho="""
Copiar una lista, tocar la copia y comprobar que el original no cambia. Suena obvio, y es donde más
programas fallan en silencio. Aquí hay un dato que resume la clase entera: **en COBOL, Fortran, Ada,
PL/I y M este programa no puede fallar**, porque en esos lenguajes **una asignación es siempre una
copia**. En Pascal con arreglos dinámicos, en cambio, `Copia := V` **no copia: comparte**.
""",
    porque="""
Aquí el concepto es la **semántica de asignación**, y estos lenguajes lo enseñan porque los más
antiguos son los que menos problemas tienen. Los lenguajes de la era de los ficheros —COBOL, Fortran,
PL/I, RPG— trabajan con **valores en bloques de memoria**: asignar copia bytes, siempre, y no hay
estructuras compartidas que sorprendan.

Los que introdujeron punteros y referencias —Pascal moderno, Lisp, Perl, C++, Smalltalk— ganaron
expresividad y heredaron el problema: **la copia superficial duplica el contenedor y comparte lo que
contiene**, y descubrirlo tarde produce los errores más difíciles de reproducir que existen.
""",
    cierre="""
Lo transferible: **"copiar" no es una operación, son tres**, y hay que saber cuál te dan. La copia de
referencia comparte todo; la superficial duplica el contenedor y comparte los elementos; la profunda
duplica todo el grafo. Ninguna es la correcta siempre: la profunda es cara y **se rompe con ciclos**,
la de referencia es gratis y peligrosa. La regla práctica que funciona: **si la estructura es
inmutable, comparte sin miedo**. Media industria se ha movido hacia los datos inmutables precisamente
para no tener que responder a esta pregunta cada vez.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. COPIA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2) COMP VALUE 0.
01  I       PIC 9(4) COMP.
01  L       PIC 9(4) COMP.
01  N       PIC 9(4) COMP VALUE 0.
01  TABLA.
    05  ELEM  PIC S9(9) COMP-3 OCCURS 100 TIMES.
01  TABLA-COPIA.
    05  ELEM-C PIC S9(9) COMP-3 OCCURS 100 TIMES.
01  SAL-O   PIC X(200) VALUE SPACES.
01  SAL-C   PIC X(200) VALUE SPACES.
01  PO      PIC 9(4) COMP VALUE 1.
01  PC      PIC 9(4) COMP VALUE 1.
01  LO      PIC 9(4) COMP.
01  LC      PIC 9(4) COMP.
01  ED      PIC -(8)9.
01  TXT     PIC X(10).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM CERRAR-TOKEN
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM CERRAR-TOKEN

    *> Un MOVE de grupo copia los BYTES: copia completa, siempre
    MOVE TABLA TO TABLA-COPIA
    MOVE 99 TO ELEM-C(N)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE ELEM(I) TO ED
        PERFORM MEDIR
        IF I > 1
            MOVE "-" TO SAL-O(PO:1)
            ADD 1 TO PO
        END-IF
        MOVE TXT(1:L) TO SAL-O(PO:L)
        ADD L TO PO

        MOVE ELEM-C(I) TO ED
        PERFORM MEDIR
        IF I > 1
            MOVE "-" TO SAL-C(PC:1)
            ADD 1 TO PC
        END-IF
        MOVE TXT(1:L) TO SAL-C(PC:L)
        ADD L TO PC
    END-PERFORM

    COMPUTE LO = PO - 1
    COMPUTE LC = PC - 1
    DISPLAY "original=" SAL-O(1:LO) " copia=" SAL-C(1:LC)
    STOP RUN.

MEDIR.
    MOVE FUNCTION TRIM(ED) TO TXT
    MOVE 0 TO L
    INSPECT FUNCTION REVERSE(TXT) TALLYING L FOR LEADING SPACE
    COMPUTE L = 10 - L.

CERRAR-TOKEN.
    IF TLEN > 0
        ADD 1 TO N
        COMPUTE ELEM(N) = FUNCTION NUMVAL(TOKEN)
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
""", """
**Lo que esta clase enseña en COBOL.** **En COBOL este programa no puede fallar.** `MOVE TABLA TO
TABLA-COPIA` copia los bytes del grupo entero, y las dos tablas quedan completamente independientes.

No hay copia superficial porque **no hay nada que compartir**: una tabla COBOL no contiene punteros,
contiene datos. La distinción de esta clase, que en Java o Python cuesta una tarde de depuración, **en
COBOL no existe**.

Esa propiedad —**semántica de valor en todo**— es la que hace tan predecible el procesamiento por
lotes: cada registro se lee, se copia, se transforma y se escribe, y ningún cambio se propaga a donde
no debe.

Y va más lejos: **también los parámetros son por valor si se declaran así**.

```cobol
CALL "SUBPROG" USING BY CONTENT  REG-CLIENTE      *> copia: el llamado no puede tocar el original
CALL "SUBPROG" USING BY REFERENCE REG-CLIENTE     *> por referencia: sí puede (el DEFECTO)
```

`BY CONTENT` es la copia explícita en la llamada, y es la forma de garantizar que un subprograma no
modifique lo que recibe (clase 079). El defecto es `BY REFERENCE`, que es lo contrario, así que
escribirlo importa.

COBOL también tiene la operación inversa, que conviene conocer porque parece igual y no lo es:

```cobol
MOVE CORRESPONDING REG-A TO REG-B
```

**`MOVE CORRESPONDING` copia campo a campo, emparejando por NOMBRE**, y convierte los tipos si hacen
falta. Es la asignación `by name` de PL/I (clase 091), y sirve para copiar entre registros de formas
parecidas pero no idénticas.

La diferencia con el `MOVE` normal es importante: el `MOVE` de grupo es **una copia de bytes que
ignora la estructura** —y falla en silencio si las estructuras no coinciden—; `MOVE CORRESPONDING`
mira los nombres. El primero es rapidísimo; el segundo, seguro.
"""),
        "fortran": ("""
program copia
   implicit none
   integer, allocatable :: v(:), c(:)
   integer :: n, ios, i
   character(len=400) :: linea, so, sc
   character(len=20)  :: buf

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      if (allocated(v)) deallocate(v)
      allocate(v(i))
      read(linea, *, iostat=ios) v
      if (ios /= 0) exit
      n = i
   end do
   if (allocated(v)) deallocate(v)
   allocate(v(n))
   read(linea, *) v

   c = v                    ! asignación de arreglo: COPIA completa
   c(n) = 99

   so = ''
   sc = ''
   do i = 1, n
      write(buf, '(I0)') v(i)
      if (i == 1) then
         so = trim(buf)
      else
         so = trim(so) // '-' // trim(buf)
      end if
      write(buf, '(I0)') c(i)
      if (i == 1) then
         sc = trim(buf)
      else
         sc = trim(sc) // '-' // trim(buf)
      end if
   end do

   write(*, '(A)') 'original=' // trim(so) // ' copia=' // trim(sc)
end program copia
""", """
**Lo que esta clase enseña en Fortran.** `c = v` **copia el arreglo entero**, siempre. La semántica de
Fortran es de valor, y con `allocatable` la asignación además **redimensiona el destino
automáticamente** (Fortran 2003) — si `c` no estaba reservado o tenía otro tamaño, se ajusta solo.

Donde sí hay que tener cuidado en Fortran es con los **punteros** (clase 097), porque ahí la
distinción de esta clase reaparece con toda su fuerza:

```fortran
integer, pointer :: p(:), q(:)
allocate(p(3))
q => p            ! ALIAS: q y p son el mismo arreglo
q = p             ! COPIA: los valores de p en el arreglo de q
```

`=>` frente a `=` es exactamente referencia frente a valor, y escrito con símbolos distintos, que es
más claro que en la mayoría de los lenguajes de esta página, donde la misma sintaxis hace una cosa u
otra según el tipo.

Y hay una construcción de Fortran que es una copia con nombre propio: **las secciones de arreglo**.

```fortran
c = v(2:5)            ! copia una rebanada
call sub(v(2:5))      ! pasa una VISTA... o una copia, según el caso
```

Cuando se pasa una sección no contigua —`v(1:10:2)`, los impares— a una subrutina que espera un
arreglo contiguo, **el compilador crea una copia temporal, la pasa y la copia de vuelta al salir**.
Eso se llama *copy-in/copy-out*, es invisible en el código y puede dominar el tiempo de ejecución en
un bucle caliente.

Detectarlo es cosa de herramientas: `gfortran -Warray-temporaries` avisa de cada copia temporal que
genera. Es una de las opciones más útiles y menos conocidas del compilador, y en códigos numéricos
grandes suele revelar cuellos de botella inesperados.

La forma de evitarlo es declarar los argumentos como `contiguous` (Fortran 2008) o pasar secciones
contiguas.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Containers.Vectors;

procedure Copia is
   package Vectores is new Ada.Containers.Vectors (Positive, Integer);
   use Vectores;

   V, C   : Vector;
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
   N      : Integer;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;
      Get (Linea (Pos .. Ultimo), Valor, Fin);
      V.Append (Valor);
      Pos := Fin + 1;
   end loop;

   N := Integer (V.Length);

   C := V;                      --  asignación de contenedor: COPIA completa
   C.Replace_Element (N, 99);

   Put ("original=");
   for I in 1 .. N loop
      Put (V.Element (I), Width => 1);
      if I < N then Put ("-"); end if;
   end loop;

   Put (" copia=");
   for I in 1 .. N loop
      Put (C.Element (I), Width => 1);
      if I < N then Put ("-"); end if;
   end loop;

   New_Line;
end Copia;
""", """
**Lo que esta clase enseña en Ada.** `C := V;` sobre un contenedor **copia**, y eso está garantizado
por el estándar: los contenedores de Ada tienen **semántica de valor**, al contrario que las
colecciones de Java o Python.

Y Ada da el mecanismo para que un tipo propio haga lo mismo: **los tipos controlados** de la clase
099.

```ada
type Recurso is new Ada.Finalization.Controlled with record
   Datos : Acceso_Buffer;
end record;

overriding procedure Adjust (R : in out Recurso) is
begin
   R.Datos := new Buffer'(R.Datos.all);     --  copia PROFUNDA al asignar
end Adjust;
```

`Adjust` se ejecuta **después de la copia bit a bit**, y ahí es donde se duplica lo que estaba
compartido. Con eso, `A := B` sobre un tipo con punteros dentro hace una copia profunda de verdad, sin
que el usuario del tipo tenga que saberlo.

Es el mismo papel que el constructor de copia de C++ y `clone` de Rust, con dos diferencias: **se
ejecuta automáticamente en toda asignación** y **el punto de partida ya es una copia**, así que solo
hay que arreglar lo compartido.

Y Ada ofrece la alternativa explícita para cuando copiar no tiene sentido:

```ada
type Fichero is limited private;     --  SIN asignación: no se puede copiar
```

**`limited`** prohíbe la asignación en el propio tipo (clase 101). Un tipo limitado no se puede
copiar por accidente, ni pasar por valor, ni devolver de una función sin construirlo en su sitio. Es
la forma de Ada de decir lo que en C++ se dice borrando el constructor de copia y en Rust se consigue
no implementando `Copy`.

Y hay un detalle: **Ada 2005 introdujo la construcción en el sitio** para los tipos limitados, así que
`X : Fichero := Abrir ("datos");` funciona — la función construye directamente en `X`, sin copia
intermedia. Es la elisión de copia garantizada que C++ no tuvo hasta C++17.
"""),
        "pascal": ("""
program Copia;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  V, C: array of Integer;
  Linea, Tok, SO, SC: string;
  I: Integer;
  Ch: Char;

begin
  ReadLn(Linea);

  SetLength(V, 0);
  Tok := '';
  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then Ch := Linea[I] else Ch := ' ';
    if Ch = ' ' then
    begin
      if Tok <> '' then
      begin
        SetLength(V, Length(V) + 1);
        V[High(V)] := StrToInt(Tok);
        Tok := '';
      end;
    end
    else
      Tok := Tok + Ch;
  end;

  { OJO: `C := V` COMPARTIRÍA el arreglo. Copy() hace una copia real. }
  C := Copy(V);
  C[High(C)] := 99;

  SO := '';
  SC := '';
  for I := 0 to High(V) do
  begin
    if SO <> '' then SO := SO + '-';
    SO := SO + IntToStr(V[I]);
    if SC <> '' then SC := SC + '-';
    SC := SC + IntToStr(C[I]);
  end;

  WriteLn('original=', SO, ' copia=', SC);
end.
""", """
**Lo que esta clase enseña en Pascal.** Aquí Pascal tiene la trampa más afilada de la página, y por
eso el programa lleva un comentario en mayúsculas:

```pascal
C := V;          { NO copia: las dos variables apuntan al MISMO arreglo }
C := Copy(V);    { copia de verdad }
```

Los **arreglos dinámicos** de Pascal (clase 090) son **contados por referencia**, así que asignarlos
comparte. Y como el conteo de referencias es transparente, `C[0] := 99` modifica **también `V[0]`**,
sin ningún aviso.

Lo que hace esto especialmente traicionero es que **los arreglos ESTÁTICOS sí se copian**:

```pascal
var
  A, B: array[1..3] of Integer;      { estáticos }
  C, D: array of Integer;             { dinámicos }
begin
  B := A;      { COPIA }
  D := C;      { COMPARTE }
end;
```

**La misma sintaxis, dos comportamientos opuestos**, decididos por si el arreglo lleva límites en la
declaración. Es una de las incoherencias más criticadas de Object Pascal, y viene de haber añadido los
arreglos dinámicos en 1998 sobre un lenguaje de 1970.

Las `string` largas se comportan igual —contadas por referencia— **con una diferencia crucial**:
tienen **copia al escribir**. Modificar una cadena compartida la duplica automáticamente, así que el
problema no aparece.

```pascal
S2 := S1;        { comparte }
S2[1] := 'X';    { AHORA se duplica: S1 no cambia }
```

Los arreglos dinámicos **no tienen copia al escribir**, y esa asimetría —cadenas sí, arreglos no— es
exactamente la clase de detalle que produce errores que no se reproducen.

Para objetos, la regla es la de la clase 101: `O2 := O1` comparte la referencia, y copiar exige un
método propio. Delphi ofrece `TPersistent.Assign` como convención para eso, con
`AssignTo` para el sentido contrario, y es el patrón que sigue toda la biblioteca visual.
"""),
        "lisp": ("""
(let ((v '()))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (push x v))
  (setf v (nreverse v))

  (let ((c (copy-list v)))            ; copia SUPERFICIAL de la lista
    (setf (nth (1- (length c)) c) 99)
    (format t "original=~{~D~^-~} copia=~{~D~^-~}~%" v c)))
""", """
**Lo que esta clase enseña en Common Lisp.** Common Lisp expone las tres copias de la clase **con tres
funciones distintas**, y esa explicitud es lo que hay que aprender aquí:

```lisp
(setf c v)          ; NADA: c y v son la misma lista
(copy-list v)       ; copia SUPERFICIAL: conses nuevos, elementos compartidos
(copy-seq v)        ; igual, para cualquier secuencia
(copy-tree v)       ; copia PROFUNDA: recorre las sublistas
(copy-structure s)  ; superficial, para defstruct
```

La diferencia entre `copy-list` y `copy-tree` es exactamente la de esta clase:

```lisp
(let* ((interior (list 1 2))
       (v (list interior 3))
       (c (copy-list v)))
  (setf (car interior) 99)
  c)                 ; ((99 2) 3) -- la copia superficial VE el cambio
```

Con `copy-tree`, no lo vería. Y `copy-tree` **entra en bucle infinito con estructuras circulares** —
que es la limitación general de toda copia profunda y una de las razones del cierre de esta clase.

Y aquí conviene señalar algo sobre el estilo de Lisp que esta clase ilumina: **la distinción entre
funciones destructivas y no destructivas está en el nombre**.

| No destructiva | Destructiva | Qué hace la destructiva |
|---|---|---|
| `reverse` | `nreverse` | reutiliza los *conses* del original |
| `append` | `nconc` | enlaza las listas sin copiar |
| `remove` | `delete` | modifica en el sitio |
| `sort` (copia) | `sort` (destructiva) | **`sort` YA es destructiva** |

La **`n`** inicial significa "no consing": no reserva memoria nueva, **destruye la entrada**. Son más
rápidas y **el argumento queda en estado indefinido** después.

La última fila es la trampa: **`sort` en Common Lisp es destructiva**, sin `n`, por razones
históricas. `(sort lista #'<)` puede dejar `lista` apuntando al medio del resultado. La forma correcta
es `(sort (copy-seq lista) #'<)`, y olvidarlo es un error clásico que el nombre no ayuda a evitar.
"""),
        "tcl": ("""
gets stdin linea
set v [split [string trim $linea]]

set c $v            ;# en Tcl esto YA es una copia: los valores son inmutables
lset c end 99

puts "original=[join $v -] copia=[join $c -]"
""", """
**Lo que esta clase enseña en Tcl.** **En Tcl esta clase no tiene trampa, y la razón es de las más
elegantes de la página: todos los valores son inmutables.**

`set c $v` copia el valor. `lset c end 99` modifica `c` y no toca `v`. **Nunca hay que preguntarse si
una modificación afectará a otra variable**, porque no puede.

Y aquí viene lo interesante: **eso no significa que se copie de verdad**.

Internamente, `set c $v` solo **incrementa un contador de referencias** sobre el mismo objeto. La
copia real ocurre únicamente cuando alguien intenta modificar un valor cuyo contador es mayor que uno.
Es **copia al escribir**, y da la semántica de valor al precio de la de referencia.

```tcl
set c $v          ;# O(1): comparte, incrementa el contador
lset c end 99     ;# AQUÍ se duplica, porque hay dos referencias
```

Ese diseño es lo que hace viable el modelo de Tcl. Sin él, pasar una lista de un millón de elementos a
un procedimiento copiaría un millón de elementos en cada llamada.

Y tiene una consecuencia de rendimiento que conviene conocer, porque es la trampa inversa:

```tcl
proc modificar {nombreLista} {
    upvar 1 $nombreLista lista      ;# por NOMBRE: no hay segunda referencia
    lappend lista nuevo              ;# modifica en el sitio, O(1)
}

proc devolver {lista} {
    lappend lista nuevo              ;# hay dos referencias: DUPLICA la lista
    return $lista
}
```

La primera es O(1); la segunda es O(n) por llamada, y en un bucle es O(n²). Es la razón de que el
idioma de Tcl para modificar estructuras grandes sea `upvar` con el nombre de la variable, y no pasar
y devolver el valor.

Es el mismo compromiso que en Clojure, Immutable.js y las estructuras persistentes de la clase 097: la
inmutabilidad simplifica el razonamiento, y hay que entender su implementación para no pagarla cara.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

my @c = @v;              # copia SUPERFICIAL: los escalares se copian
$c[-1] = 99;

print "original=", join('-', @v),
      " copia=",   join('-', @c), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `my @c = @v;` **copia**, porque los elementos son escalares y los
escalares se copian por valor. Este programa funciona.

La trampa aparece en cuanto hay referencias dentro, que es siempre que la estructura tenga más de un
nivel (clase 097):

```perl
my @v = ([1, 2], [3, 4]);
my @c = @v;             # copia el arreglo EXTERIOR, comparte los interiores
$c[0][0] = 99;
print $v[0][0];         # 99  <-- el original CAMBIÓ
```

Es la copia superficial en su forma más clásica, y en Perl es especialmente fácil caer porque **la
sintaxis no distingue**: `@v` y `@c` se ven igual, tengan escalares o referencias dentro.

Para la copia profunda, Perl tiene dos respuestas del ecosistema, y las dos son instructivas:

```perl
use Storable qw(dclone);
my $copia = dclone($original);        # copia profunda, en C, rápida

use Clone qw(clone);
my $copia = clone($original);
```

**`Storable`** es del núcleo y funciona serializando y deserializando la estructura en memoria — que
es, en el fondo, cómo se hace una copia profunda en casi cualquier lenguaje sin soporte nativo. Maneja
**referencias circulares** correctamente, que es lo que distingue una implementación seria de una
recursión ingenua.

Y el `-1` de `$c[-1]` es el índice desde el final, otra aportación de Perl que después copiaron
Python, Ruby y PHP.

Un último apunte que conecta con la clase 079: **la asignación `my @c = @v` es distinta de `@_`**. Los
elementos de `@_` son **alias** a los argumentos del llamante, así que modificar `$_[0]` modifica la
variable original. Es el único sitio de Perl con paso por referencia implícito, y es la excepción que
confirma que todo lo demás se copia.
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    std::vector<int> v{std::istream_iterator<int>(std::cin),
                       std::istream_iterator<int>()};
    if (v.empty()) return 1;

    std::vector<int> c = v;        // copia PROFUNDA de los elementos
    c.back() = 99;

    std::cout << "original=";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i != 0) std::cout << '-';
        std::cout << v[i];
    }
    std::cout << " copia=";
    for (std::size_t i = 0; i < c.size(); ++i) {
        if (i != 0) std::cout << '-';
        std::cout << c[i];
    }
    std::cout << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `std::vector<int> c = v;` **copia todos los elementos**, y esa es
la decisión de diseño central de C++: **la semántica de valor por defecto**, al contrario que Java,
C# o Python, donde asignar un objeto comparte la referencia.

Y esa decisión trae consigo lo que se llama la **regla de los cinco**:

```cpp
class Recurso {
    ~Recurso();                                  // destructor
    Recurso(const Recurso&);                      // constructor de COPIA
    Recurso& operator=(const Recurso&);           // asignación por copia
    Recurso(Recurso&&) noexcept;                  // constructor de MOVIMIENTO
    Recurso& operator=(Recurso&&) noexcept;       // asignación por movimiento
};
```

**Si necesitas escribir uno, probablemente necesitas los cinco.** El caso típico es una clase con un
puntero dentro: el destructor libera, y si no escribes el constructor de copia, **la copia por
defecto duplica el puntero y los dos objetos liberan la misma memoria** — la doble liberación, uno de
los errores más peligrosos del lenguaje.

La regla complementaria, y la que hay que aplicar en la práctica, es **la regla del cero**: si usas
`std::vector`, `std::string` y `std::unique_ptr` en lugar de punteros crudos, **no escribas ninguno de
los cinco** y deja que el compilador los genere. Es la recomendación de las guías modernas.

Y esta clase es donde encaja la **semántica de movimiento** de la clase 081:

```cpp
std::vector<int> c = v;              // COPIA: v sigue válido
std::vector<int> d = std::move(v);   // MOVIMIENTO: roba el búfer, v queda vacío
```

El movimiento es la tercera opción que faltaba entre "compartir" y "copiar caro": **transferir**. Es
lo que hace que devolver un contenedor grande de una función no cueste nada, y es lo que Fortran tenía
en 2003 con `move_alloc`.

Para copias profundas de jerarquías polimórficas, C++ usa el idioma del **constructor virtual**:

```cpp
virtual std::unique_ptr<Figura> clonar() const = 0;
```

Porque copiar por el tipo base **trunca** los campos del derivado — el *slicing* que se mencionó en la
clase 099, y una de las razones de que Pascal, C# y Swift eviten la herencia con semántica de valor.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi COPIA;
  entrada char(200) const;
end-pi;

dcl-s v    int(10) dim(100);
dcl-s c    int(10) dim(100);
dcl-s n    int(10) inz(0);
dcl-s i    int(10);
dcl-s tok  varchar(20) inz('');
dcl-s ch   char(1);
dcl-s so   varchar(200) inz('');
dcl-s sc   varchar(200) inz('');

for i = 1 to %len(%trimr(entrada)) + 1;
  if i <= %len(%trimr(entrada));
    ch = %subst(entrada : i : 1);
  else;
    ch = ' ';
  endif;
  if ch = ' ';
    if tok <> '';
      n += 1;
      v(n) = %int(tok);
      tok = '';
    endif;
  else;
    tok += ch;
  endif;
endfor;

// Asignar una tabla completa copia todos sus elementos
c = v;
c(n) = 99;

for i = 1 to n;
  if so <> '';
    so += '-';
    sc += '-';
  endif;
  so += %char(v(i));
  sc += %char(c(i));
endfor;

dsply ('original=' + so + ' copia=' + sc);

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Como COBOL, RPG tiene **semántica de valor en todo**: `c = v`
sobre dos tablas copia todos los elementos, y `dsA = dsB` sobre dos estructuras de datos copia sus
bytes.

Y hay una operación de RPG que merece mención porque es literalmente esta clase con nombre propio:
**`eval-corr`**.

```rpgle
eval-corr destino = origen;
```

**Copia campo a campo emparejando por NOMBRE y por tipo**, ignorando los campos que solo existen en
uno de los dos. Es el `MOVE CORRESPONDING` de COBOL y el `by name` de PL/I, en RPG desde la versión
7.1 (2010).

Su uso real es el que cabe esperar: **convertir entre la estructura de un registro de base de datos y
la estructura interna del programa**, cuando comparten muchos campos pero no todos. Sin `eval-corr`
son treinta asignaciones a mano, y una de ellas se olvida.

La distinción de esta clase reaparece en RPG en cuanto entran los punteros de la clase 090:

```rpgle
dcl-s p pointer;
dcl-s q pointer;
dcl-ds datos based(p);
  campo int(10);
end-ds;

q = p;          // COMPARTE: q apunta a lo mismo
```

Asignar punteros comparte, como en cualquier sitio. Y como RPG no tiene recolector de basura, aquí
aparecen los dos errores clásicos a la vez: liberar dos veces con `dealloc` y usar un puntero después
de liberarlo.

La diferencia con C es de exposición: **en RPG los punteros son una herramienta especializada**, no la
forma normal de trabajar, así que la mayor parte del código nunca los toca. Es el mismo argumento que
hace tan predecible el COBOL de gestión, y explica por qué esta clase, que en C++ ocupa un capítulo,
en RPG es una nota al pie.
"""),
        "pli": ("""
 copia: procedure options(main);

    declare linea char(200) varying;
    declare v(100) fixed binary(31);
    declare c(100) fixed binary(31);
    declare (n, i) fixed binary(31);
    declare tok char(20) varying initial('');
    declare ch char(1);
    declare so char(200) varying initial('');
    declare sc char(200) varying initial('');

    get edit (linea) (a(200));
    n = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then ch = substr(linea, i, 1); else ch = ' ';
       if ch = ' ' then do;
          if tok ^= '' then do;
             n = n + 1;
             v(n) = tok;
             tok = '';
          end;
       end;
       else tok = tok || ch;
    end;

    c = v;                 /* asignación de arreglo: copia TODOS los elementos */
    c(n) = 99;

    do i = 1 to n;
       if so ^= '' then do; so = so || '-'; sc = sc || '-'; end;
       so = so || trim(char(v(i)));
       sc = sc || trim(char(c(i)));
    end;

    put skip list ('original=' || so || ' copia=' || sc);

 end copia;
""", """
**Lo que esta clase enseña en PL/I.** `c = v;` copia el arreglo entero, y esa aritmética de arreglos de
la clase 089 hace que la semántica de valor de PL/I sea completa y cómoda.

Lo que PL/I añade aquí es la asignación **`by name`**, que ya apareció en la clase 091 y que es el
antepasado de `MOVE CORRESPONDING` y de `eval-corr`:

```pli
 resumen = cliente, by name;
```

Copia **solo los campos que existen en ambas estructuras**, emparejados por nombre y convertidos si
hace falta. Es una proyección estructural resuelta por el compilador, en 1964.

Y el otro lado de la clase, la referencia, aparece en PL/I de tres formas distintas:

```pli
 declare p pointer;
 q = p;                        /* compartir: los dos apuntan a lo mismo */

 declare 1 vista based(p), ...;  /* superponer una estructura sobre memoria */

 call sub(x);                   /* los parámetros son POR REFERENCIA por defecto */
```

La tercera es la que sorprende y la que hay que recordar de la clase 079: **PL/I pasa por referencia
por defecto**, así que un subprograma puede modificar sus argumentos sin que la llamada lo indique.

Para pasar por valor hay que forzar una copia con paréntesis:

```pli
 call sub((x));      /* los paréntesis crean una EXPRESIÓN: se pasa una copia */
```

Ese idioma —**dobles paréntesis para forzar copia**— es de los más oscuros de PL/I y una fuente
conocida de errores en los dos sentidos: quien no los pone y esperaba una copia, y quien los pone sin
querer y pierde el resultado.

C, veinte años después, tomó la decisión contraria —**todo por valor, siempre**— y obligó a pasar
punteros explícitamente. Es más verboso y no tiene ninguna ambigüedad, y hoy se considera claramente
la elección correcta.
"""),
        "mumps": ("""
COPIA ; Copia superficial y profunda -- clase 102
 read linea
 kill v, c
 set n = $length(linea, " ")
 for i=1:1:n set v(i) = $piece(linea, " ", i)
 ; MERGE copia un arbol ENTERO, con todos sus subindices
 merge c = v
 set c(n) = 99
 set so = "", sc = ""
 for i=1:1:n do
 . if so '= "" set so = so _ "-", sc = sc _ "-"
 . set so = so _ v(i), sc = sc _ c(i)
 write "original=", so, " copia=", sc, !
 quit
""", """
**Lo que esta clase enseña en M.** M tiene un comando dedicado exactamente a esta clase, y es de los
mejores del lenguaje: **`merge`**.

```mumps
 merge c = v
```

**Copia el árbol entero**, con todos sus subíndices y a cualquier profundidad. No es una copia
superficial: es profunda por definición, porque en M **no hay referencias que compartir**.

Y funciona en las cuatro combinaciones que importan:

```mumps
 merge local = local              ; entre variables locales
 merge ^GLOBAL = local            ; de memoria a DISCO
 merge local = ^GLOBAL            ; de disco a memoria
 merge ^A("x") = ^B("y")          ; entre subárboles de globals distintos
 merge ^A = $$obtener^SERVIDOR()  ; en implementaciones con acceso remoto
```

La segunda y la tercera son las que definen a M: **volcar una estructura en memoria a la base de
datos, o traerla, es un comando**. Sin serializar, sin transacción explícita —aunque la haya— y sin
capa de persistencia.

Y `merge` **fusiona en lugar de reemplazar**: los nodos que ya existan en el destino y no estén en el
origen **se conservan**. Para reemplazar de verdad hay que hacer `kill` primero, y olvidarlo es el
error clásico con este comando.

El resto de la semántica de M es de valor puro: `set a = b` copia la cadena, y **no hay ninguna forma
de que dos nombres designen la misma estructura**. Como se dijo en la clase 101, en M nunca hay que
preguntarse si una modificación se propagará.

El precio de esa simplicidad es el que se ha visto en toda esta parte: **no hay estructuras
compartidas, así que no hay objetos, ni grafos con enlaces cruzados, ni nada que dependa de la
identidad**. M cambió expresividad por previsibilidad, y para su dominio —registros clínicos y
financieros, procesados por miles de procesos concurrentes— fue probablemente el cambio correcto.
"""),
        "smalltalk": ("""
| v c so sc |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

c := v copy.                      "copy es SUPERFICIAL; deepCopy es profunda"
c at: c size put: 99.

so := (v collect: [ :cada | cada printString ])
    inject: '' into: [ :acc :cada |
        acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ].

sc := (c collect: [ :cada | cada printString ])
    inject: '' into: [ :acc :cada |
        acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ].

Transcript show: 'original=', so, ' copia=', sc; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk fue el lenguaje que **puso nombre a esta
distinción**, y sus tres mensajes siguen siendo el vocabulario que usa medio mundo:

```smalltalk
objeto shallowCopy      "copia SUPERFICIAL: campos copiados, contenido compartido"
objeto copy              "shallowCopy + postCopy -- lo que la clase decida"
objeto deepCopy          "copia PROFUNDA: recorre el grafo entero"
objeto veryDeepCopy      "profunda respetando la identidad y los CICLOS"
```

Las palabras *shallow copy* y *deep copy* entraron en el vocabulario común desde aquí.

Y hay dos detalles de diseño que merecen atención.

**`copy` no es `shallowCopy`.** `copy` está definido como `^self shallowCopy postCopy`, y **`postCopy`
es el gancho que cada clase redefine** para arreglar lo que la copia superficial dejó compartido:

```smalltalk
MiClase >> postCopy
    super postCopy.
    coleccionInterna := coleccionInterna copy
```

Es exactamente el `Adjust` de Ada, con el mismo diseño: **primero se copia todo superficialmente,
después se arregla lo que hace falta**. Que dos lenguajes tan distintos llegaran a la misma solución
dice que es la correcta.

**Y `veryDeepCopy` existe porque `deepCopy` no basta.** Una copia profunda ingenua sobre una
estructura con ciclos entra en bucle infinito, y sobre un grafo con nodos compartidos **los duplica**,
rompiendo la topología. `veryDeepCopy` lleva un diccionario de lo ya copiado —una
`IdentityDictionary`, clase 101— y devuelve la misma copia cuando se encuentra dos veces el mismo
objeto.

Que Smalltalk tuviera ese matiz resuelto y con nombre en 1980 es notable: es el mismo algoritmo que
usan hoy `deepcopy` de Python, `structuredClone` de JavaScript y `Storable` de Perl.

Y la lección del cierre de esta clase queda más clara vista así: **la copia profunda correcta es un
recorrido de grafo con memoria**, no una recursión. Quien la escriba sin el diccionario, la escribirá
mal.
"""),
    },
)
