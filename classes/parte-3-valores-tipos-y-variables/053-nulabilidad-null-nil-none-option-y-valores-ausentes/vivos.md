# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 053

> [⬅️ Volver a la clase 053](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Distinguir "el valor es cero" de "no hay valor". Tony Hoare llamó a la referencia nula *su error de
mil millones de dólares*, y esta clase es donde se ve por qué: en la mitad de estos lenguajes **la
ausencia no se puede representar**, así que se finge con un valor especial —un cero, un espacio, una
fecha imposible— y tarde o temprano alguien lo confunde con un dato real.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **cómo se representa lo que no está**, y estos lenguajes lo cubren mejor que el
> núcleo porque incluyen las dos épocas. COBOL, Fortran clásico y RPG **no tienen null**: usan valores
> centinela, y de ahí vienen las fechas `9999-12-31` y los códigos `-1` que siguen apareciendo en
> bases de datos de todo el mundo.
>
> Y luego está M, que tiene la respuesta más sofisticada de toda la página y la más desconocida:
> **`$data` devuelve cuatro valores distintos**, porque en M una variable puede no existir, existir con
> valor, existir solo con descendientes, o las dos cosas. Es un modelo de ausencia con más matices que
> el `Option` de Rust.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (0 significa ausente) → stdout: `valor=<n>` si hay valor, o `valor=ausente` si n es 0
- **Regla:** `si n == 0 → 'ausente'; si no → n`

| stdin | esperado |
|---|---|
| `5` | `valor=5` |
| `0` | `valor=ausente` |
| `42` | `valor=42` |

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
PROGRAM-ID. NULABLE.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
    88  AUSENTE   VALUE 0.
01  ED-N    PIC -(9)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    IF AUSENTE
        DISPLAY "valor=ausente"
    ELSE
        MOVE N TO ED-N
        DISPLAY "valor=" FUNCTION TRIM(ED-N)
    END-IF
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene null.** Un `PIC S9(9)` siempre contiene un
número; no hay ningún estado que signifique "vacío". La ausencia se representa con un **valor
centinela**, y el nivel 88 sirve al menos para **darle nombre**: `AUSENTE` documenta que el cero
tiene un significado especial, en lugar de dejar un `IF N = 0` sin explicación.

Esa es la respuesta pragmática, y es el origen de convenciones que siguen vivas en bases de datos de
medio mundo:

- fechas `00000000` o `99991231` para "sin fecha" y "sin caducidad";
- códigos `-1` o `999` para "desconocido";
- campos alfanuméricos a `SPACES` para "no informado";
- `HIGH-VALUES` y `LOW-VALUES` como centinelas de ordenación.

Todas funcionan hasta que el valor centinela se convierte en un dato legítimo, y entonces el fallo es
silencioso y muy caro de encontrar.

Donde COBOL **sí** tiene nulos de verdad es al hablar con **Db2**, porque SQL sí los tiene. Y la
solución es exactamente la de RPG y la de `std::optional`: **llevar la ausencia en una variable
aparte**.

```cobol
EXEC SQL
    SELECT SALDO INTO :WS-SALDO :WS-SALDO-IND FROM CUENTAS WHERE ID = :WS-ID
END-EXEC

IF WS-SALDO-IND < 0     *> el indicador negativo significa NULL
    DISPLAY "sin saldo informado"
END-IF
```

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program nulable
   implicit none
   integer, allocatable :: valor
   integer :: n

   read(*, *) n
   if (n /= 0) allocate(valor, source=n)

   if (allocated(valor)) then
      write(*, '(A,I0)') 'valor=', valor
   else
      write(*, '(A)') 'valor=ausente'
   end if
end program nulable
```

**Lo que esta clase enseña en Fortran.** El Fortran clásico tampoco tenía forma de expresar la
ausencia, y usaba los mismos centinelas que COBOL —el `-999` de los ficheros de datos científicos es
una institución—. El Fortran moderno tiene **dos** mecanismos, y los dos son buenos.

El primero es el de este programa: **un escalar `allocatable`**. Una variable que puede estar
asignada o no, y `allocated()` lo pregunta. No es un puntero: no puede apuntar a otra cosa, no se
puede desreferenciar por error y **se libera sola al salir del ámbito**. Es, en la práctica, un
`Option` sin sintaxis especial.

El segundo es para argumentos, y es el que se usa a diario:

```fortran
subroutine dibujar(x, y, color)
   integer, intent(in) :: x, y
   integer, intent(in), optional :: color      ! puede no venir
   if (present(color)) then
      ...
   end if
end subroutine
```

`optional` más `present()` resuelve el argumento ausente **sin necesidad de un valor centinela ni de
sobrecargas**. Java, C y Go no lo tienen; C++ lo aproxima con valores por defecto, que no distinguen
"no lo pasó" de "pasó justo el valor por defecto".

Y hay un tercer estado en Fortran que conviene conocer: los **punteros** (`pointer`) tienen tres
situaciones —asociado, no asociado e **indefinido**—, y `associated()` sobre uno indefinido es
comportamiento indeterminado. De ahí que la guía moderna sea usar `allocatable` siempre que se pueda
y `pointer` solo cuando haga falta apuntar de verdad.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Nulable is
   type Acceso_Entero is access Integer;

   Valor : Acceso_Entero := null;
   N     : Integer;
begin
   Get (N);
   if N /= 0 then
      Valor := new Integer'(N);
   end if;

   if Valor = null then
      Put_Line ("valor=ausente");
   else
      Put ("valor="); Put (Valor.all, Width => 1); New_Line;
   end if;
end Nulable;
```

**Lo que esta clase enseña en Ada.** Ada tiene `null`, pero **solo para los tipos de acceso**
(punteros). Un `Integer` nunca puede ser nulo, así que el error de Hoare está acotado a los sitios
donde escribiste `access`.

Y desde **Ada 2005** hay algo que casi ningún lenguaje de esta lista ofrece: un tipo de puntero que
**no puede ser nulo**, comprobado por el compilador.

```ada
type Acceso_Entero      is access Integer;             --  puede ser null
subtype Acceso_Seguro   is not null Acceso_Entero;     --  NO puede ser null

procedure Procesar (P : not null Acceso_Entero);       --  el parámetro tampoco
```

Con `not null`, el compilador rechaza asignarle `null` y **elimina la comprobación en el punto de
uso**, porque ya la hizo antes. Es la misma idea que `&T` frente a `Option<&T>` en Rust y que los
tipos no nulos de Kotlin, disponible en 2005.

Ada tiene además una segunda respuesta, más idiomática y sin memoria dinámica:

```ada
type Valor_Opcional (Presente : Boolean := False) is record
   case Presente is
      when True  => Dato : Integer;
      when False => null;
   end case;
end record;
```

Es un **registro con discriminante**, es decir, un tipo suma comprobado por el compilador: si accedes
a `Dato` sin que `Presente` sea cierto, salta `Constraint_Error`. Es el `Option` de Rust y el
`sealed interface` de Java, escrito en 1983 y sin tocar el montículo — que es justo lo que un sistema
de aviónica necesita.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Nulable;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;
  Valor: ^Integer;

begin
  Read(N);

  Valor := nil;
  if N <> 0 then
  begin
    New(Valor);
    Valor^ := N;
  end;

  if Valor = nil then
    WriteLn('valor=ausente')
  else
    WriteLn('valor=', IntToStr(Valor^));

  if Valor <> nil then Dispose(Valor);
end.
```

**Lo que esta clase enseña en Pascal.** `nil` existe **solo para punteros**, igual que en Ada. Un
`Integer` no puede ser `nil`, así que el problema queda acotado.

Lo que Pascal aporta a esta clase es que **el puntero tiene tipo**, y en 1970 eso no era evidente.
`^Integer` apunta a un entero y a nada más: no se puede asignar a un `^Real` sin conversión, ni hacer
aritmética sobre él, ni desreferenciar a otro tipo. Compara con C, donde un `void*` va a cualquier
sitio y `p + 1` mueve el puntero según un tamaño que hay que recordar.

Fíjate también en el par **`New`/`Dispose`**, que es el `malloc`/`free` de Pascal con una diferencia
importante: **`New` conoce el tipo**, así que reserva el tamaño correcto sin que se lo digas. En C,
`malloc(sizeof(int))` con el `sizeof` equivocado compila perfectamente.

Y la trampa clásica: **`Dispose` no pone el puntero a `nil`**. Tras liberarlo, `Valor` sigue
apuntando a memoria que ya no es tuya —un *dangling pointer*— y `Valor = nil` da falso. El idioma
correcto es `Dispose(Valor); Valor := nil;`, y la razón de que Object Pascal añadiera `FreeAndNil`
para los objetos, que hace las dos cosas.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (valor (if (zerop n) nil n)))
  (if valor
      (format t "valor=~D~%" valor)
      (format t "valor=ausente~%")))
```

**Lo que esta clase enseña en Common Lisp.** `nil` es la ausencia… y también el falso lógico, y
también la lista vacía, y también el símbolo `nil`. **Cuatro papeles en un solo objeto**, y esa
sobrecarga es una de las decisiones más discutidas de la historia del lenguaje.

Es cómoda —`(if lista ...)` funciona para "¿hay elementos?"— y es ambigua, porque no se puede
distinguir "no hay valor" de "el valor es la lista vacía" ni de "el valor es falso". Scheme lo
resolvió separándolos: allí `'()` y `#f` son objetos distintos.

Cuando la distinción importa, el idioma de Common Lisp es devolver **dos valores**, el mismo
mecanismo de la clase 049:

```lisp
(gethash 'clave tabla)
; => NIL, NIL     la clave no está
; => NIL, T       la clave SÍ está, y su valor es NIL

(multiple-value-bind (valor encontrado) (gethash 'clave tabla)
  (if encontrado ...))
```

El segundo valor separa "no está" de "está y vale `nil`". Es exactamente el patrón `value, ok :=` de
Go, treinta años antes, y con la ventaja de que ignorarlo es gratis y no obliga a escribir `_`.

Y una nota sobre `(if valor ...)`: funciona aquí porque el contrato dice que 0 significa ausente,
pero **en Lisp `0` es verdadero**. En un caso general habría que escribir `(if (null valor) ...)` en
vez de confiar en la falsedad — la trampa que ya apareció en la clase 043.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

if {$n != 0} { set valor $n }

if {[info exists valor]} {
    puts "valor=$valor"
} else {
    puts "valor=ausente"
}
```

**Lo que esta clase enseña en Tcl.** No hay `null`, no hay `nil` y no hay `undef`. La cadena vacía es
un valor perfectamente normal, así que no puede hacer de ausencia. Lo que Tcl tiene en su lugar es
**la variable que no existe**, y `info exists` es cómo se pregunta.

Es una distinción más limpia de lo que parece: en vez de un valor especial dentro de la variable, la
ausencia está **fuera** de ella. `unset valor` la devuelve al estado de no existir. Y leer una
variable inexistente **no da `nil`: da un error**, lo que evita que la ausencia se propague en
silencio como ocurre con `undefined` en JavaScript.

Lo mismo se aplica a los diccionarios y a los arrays asociativos:

```tcl
info exists arr(clave)      ;# ¿existe ese elemento?
dict exists $d clave        ;# lo mismo para un dict
dict get $d clave           ;# ERROR si no existe -- no devuelve vacío
```

Que el acceso falle en vez de devolver un valor por defecto es la decisión contraria a la de PHP y a
la de M, y significa que un error de escritura en el nombre de una clave se detecta al instante.

El contrapunto honesto: como las variables se crean al asignarlas, **una errata en un `set` crea una
variable nueva** en silencio, igual que en Perl sin `use strict`. Tcl no tiene un `strict` que lo
impida.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $valor = $n != 0 ? $n : undef;

printf "valor=%s\n", defined($valor) ? $valor : 'ausente';
```

**Lo que esta clase enseña en Perl.** `undef` es un valor de primera clase que significa "sin
definir", y `defined()` es cómo se pregunta. Lo importante es que **`defined` y "verdadero" son
cosas distintas**, porque `0` y `""` son falsos pero están perfectamente definidos.

Esa distinción es la que Perl resolvió con un operador propio, y merece conocerse porque es la
respuesta a un error muy común:

```perl
my $reintentos = $config{reintentos} || 3;   # MAL: si vale 0, pone 3
my $reintentos = $config{reintentos} // 3;   # BIEN: solo si es undef
```

`||` mira la **verdad**; `//` mira la **definición**. Un contador configurado a cero es un valor
legítimo que `||` destruye. JavaScript adoptó exactamente el mismo operador —`??`— en 2020 por
exactamente el mismo motivo, y le añadió `??=` igual que Perl tiene `//=`.

Perl distingue además **tres estados** donde otros ven dos, y esta clase es el sitio para verlos:

```perl
exists $h{clave}     # ¿existe la clave?
defined $h{clave}    # ¿tiene valor?  (existe pero puede ser undef)
$h{clave}            # ¿es verdadero? (puede ser 0 o "")
```

Los tres son preguntas diferentes y confundirlos es la fuente de errores más común con hashes. Es el
mismo trío que en Tcl (`info exists`) y en M (`$data`), y una vez que se ve en tres lenguajes
distintos deja de parecer una rareza para parecer lo que es: **la forma correcta de modelar la
ausencia**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <optional>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::optional<int> valor;          // vacío por defecto
    if (n != 0) valor = n;

    if (valor.has_value()) {
        std::cout << "valor=" << *valor << '\n';
    } else {
        std::cout << "valor=ausente\n";
    }
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::optional<int>` (C++17) es la respuesta moderna, y su valor
está en lo que **no** hace: no reserva memoria dinámica, no es un puntero y **no se puede
desreferenciar por accidente sin que el código lo diga**. El objeto contiene el entero y un booleano,
en la pila.

Compara con la alternativa antigua, `int*`, que arrastra tres significados a la vez —"no hay valor",
"apunta a un entero", "apunta a un array de enteros"— y no dice cuál.

Las formas de sacar el valor están graduadas a propósito:

```cpp
*valor                      // rápido; UB si está vacío -- tú garantizas que hay
valor.value()               // lanza std::bad_optional_access si está vacío
valor.value_or(0)           // valor por defecto
if (valor) { ... }          // conversión a bool explícita
```

Que existan las cuatro es la filosofía de C++: la insegura y rápida disponible, pero **con un nombre
distinto** para que se vea en la revisión de código.

Y C++23 añadió las operaciones **monádicas** —`and_then`, `transform`, `or_else`— que permiten
encadenar sin escribir `if` anidados, tomando prestado directamente de Rust y de Haskell:

```cpp
auto r = buscar(id).and_then(validar).transform(formatear).value_or("desconocido");
```

Los punteros crudos, claro, siguen ahí. `nullptr` (C++11) al menos sustituyó al `NULL` de C, que era
literalmente `0` y se colaba en sobrecargas que esperaban un entero.

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

dcl-pi NULABLE;
  n int(10) const;
end-pi;

dcl-s valor  int(10);
dcl-s hay    ind inz(*off);
dcl-s salida char(40);

if n <> 0;
  valor = n;
  hay = *on;
endif;

if hay;
  salida = 'valor=' + %char(valor);
else;
  salida = 'valor=ausente';
endif;
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Como COBOL, RPG **no tiene null en sus tipos**: un `int(10)`
siempre vale algo. La ausencia se lleva en una **variable aparte** —aquí el indicador `hay`—, que es
exactamente la estructura interna de `std::optional`, escrita a mano.

Pero RPG tiene una respuesta de primera clase para el sitio donde esto importa de verdad, que es la
base de datos. **Db2 for i sí tiene nulos**, y RPG los maneja con `%nullind`:

```rpgle
dcl-f CLIENTES usage(*input) alwnull(*usrctl);

read CLIENTES;
if %nullind(CLI_SALDO);          // ¿el campo es NULL en la fila leída?
  // no informado
else;
  total += CLI_SALDO;
endif;

%nullind(CLI_FECHA) = *on;       // y se puede ESCRIBIR: marcar el campo como nulo
```

`%nullind(campo)` es un booleano **asociado al campo** que se lee y se escribe. La ausencia no viaja
dentro del dato: viaja **en paralelo**, exactamente como los indicadores de nulo del SQL embebido en
COBOL.

Y `alwnull(*usrctl)` es la palabra clave que hay que recordar: **sin ella, RPG lee un campo nulo como
su valor por defecto —cero o blancos— sin avisar**. El comportamiento por defecto de la plataforma
es el centinela silencioso; hay que pedir explícitamente que te dejen ver la diferencia.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 nulable: procedure options(main);

    declare n     fixed binary(31);
    declare p     pointer initial(null());
    declare valor fixed binary(31) based(p);

    get list (n);
    if n ^= 0 then do;
       allocate valor set(p);
       valor = n;
    end;

    if p = null() then
       put skip list ('valor=ausente');
    else
       put skip list ('valor=' || trim(char(valor)));

 end nulable;
```

**Lo que esta clase enseña en PL/I.** `null()` es una **función incorporada** que devuelve el puntero
nulo, no una palabra clave. Y las variables `based(p)` son la construcción característica: `valor`
**no tiene almacenamiento propio**, vive donde apunte `p`. Cambiar `p` cambia a qué mira `valor`, sin
tocar ninguna sintaxis de desreferencia.

Es potente y es exactamente lo que hoy se considera peligroso: el mismo nombre puede referirse a
memoria distinta en cada momento, y si `p` es nulo, **usar `valor` es comportamiento indefinido sin
ninguna marca visible en el punto de uso**. En C al menos hay que escribir `*p`.

PL/I ofrece a cambio algo que compensa parcialmente: la condición `ON` puede capturar el error.

```pli
on error begin;
   put skip list ('acceso invalido');
end;
```

Y para el caso de esta clase, el mundo PL/I real usa el mismo recurso que COBOL: **campos indicadores
en paralelo** al hablar con Db2, y valores centinela documentados dentro del programa.

La lección de diseño que deja aquí, y que enlaza con la clase 050, es la misma: PL/I da mecanismos
muy potentes y **ninguna barandilla**. `based` es la abstracción que permitió escribir Multics en un
lenguaje de alto nivel; también es la que hace que revisar un PL/I ajeno cueste tanto.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
NULABLE ; Nulabilidad -- clase 053
 read n
 if n'=0 set valor = n
 if $data(valor) write "valor=", valor, ! quit
 write "valor=ausente", !
 quit
```

**Lo que esta clase enseña en M.** La mejor respuesta de toda la página, y la menos conocida.
**`$data(x)` no devuelve un booleano: devuelve cuatro valores posibles**, porque en M una variable no
es una casilla, es un **nodo de un árbol**:

| `$data` | Significado |
|---|---|
| **0** | No existe: ni valor ni descendientes |
| **1** | Tiene valor y **no** tiene descendientes |
| **10** | **No tiene valor** pero sí tiene descendientes |
| **11** | Tiene valor **y** descendientes |

El estado **10** es el que no existe en ningún otro lenguaje de esta lista. Significa: `^PACIENTE(7)`
no tiene ningún dato propio, pero `^PACIENTE(7,"nombre")` sí existe. Es un nodo intermedio de un árbol
disperso — algo que en un modelo de objetos se representaría con un objeto vacío, y que aquí es un
estado del propio dato.

Y es útil de verdad. Recorrer una estructura clínica exige distinguir "este paciente no está" de
"este paciente existe pero no tiene alergias registradas" de "tiene alergias y además una nota". Un
booleano no daría para eso.

M añade `$get(x)` como atajo —devuelve el valor o la cadena vacía si no existe, con un valor por
defecto opcional: `$get(x, "sin datos")`— que es el `value_or` de C++ y el `//` de Perl.

La ironía de esta página: el lenguaje sin tipos y sin declaraciones tiene el modelo de ausencia más
matizado de los doce.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n valor |

n := stdin nextLine trimBoth asNumber.
valor := n = 0 ifTrue: [ nil ] ifFalse: [ n ].

Transcript
    show: 'valor=', (valor ifNil: [ 'ausente' ] ifNotNil: [ :v | v printString ]);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** `nil` **es un objeto**: la única instancia de la clase
`UndefinedObject`. No es una palabra clave ni un puntero nulo — tiene clase, responde a mensajes, y
puedes abrir su implementación en el navegador.

Eso cambia por completo la ergonomía de la ausencia, porque los métodos de manejo están **en el
propio `nil`**:

```smalltalk
nil isNil            "true"
nil ifNil: [ 0 ]     "0 -- implementado en UndefinedObject como: ^unBloque value"
5   ifNil: [ 0 ]     "5 -- implementado en Object como: ^self"
valor ifNil: [ 'ausente' ] ifNotNil: [ :v | v printString ]
```

`ifNil:` está implementado dos veces: en `UndefinedObject` evalúa el bloque, y en `Object` devuelve
`self`. **Otra vez el condicional resuelto por polimorfismo**, igual que `ifTrue:` en la clase 046.
No hay ninguna comprobación de nulo en el lenguaje; hay dos métodos.

Y `ifNotNil:` recibe un bloque **con parámetro**, así que el valor no nulo llega ya desempaquetado.
Es el `map` de un `Option`, disponible con esa sintaxis desde hace décadas.

La contrapartida honesta: como cualquier variable puede valer `nil`, Smalltalk **no** tiene la
garantía estática que dan `not null` de Ada o los tipos no nulos de Kotlin. El error de Hoare sigue
siendo posible; lo que cambia es que enviar un mensaje a `nil` no revienta el proceso, **abre el
depurador con la pila viva** y permite arreglarlo y continuar.

---

## Y de vuelta a la clase

Dos lecciones. La primera: **un valor centinela es una bomba de relojería**. `0` significa ausente
hasta el día en que cero es un dato legítimo; `-1` funciona hasta que llega un saldo negativo. Si el
lenguaje no distingue, la distinción hay que llevarla aparte —una bandera, un indicador, un
`has_value`—, y eso es exactamente lo que hacen `std::optional`, el `not null access` de Ada y los
indicadores de nulo de RPG.

La segunda: **`nil` no es una cosa, son varias**. En Lisp es a la vez falso, lista vacía y ausencia;
en Smalltalk es un objeto con métodos; en Perl `undef` se distingue de `0` con `//` pero no con `||`.
Saber cuál de esas es la de tu lenguaje evita la clase de error que Hoare lamentaba.

⏮️ [Volver a la clase 053](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
