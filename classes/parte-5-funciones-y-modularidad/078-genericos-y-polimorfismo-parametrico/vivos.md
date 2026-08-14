# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 078

> [⬅️ Volver a la clase 078](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

El mayor de dos valores. Escrito una vez y que funcione **con enteros, con reales, con fechas y con
cualquier cosa que se pueda comparar**. Eso es el polimorfismo paramétrico, y esta clase reparte a
los doce lenguajes en tres grupos muy nítidos: los que lo resuelven **al compilar**, los que lo
resuelven **al ejecutar** por no tener tipos, y los que **no lo resuelven**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto son los **genéricos**, y estos lenguajes lo enseñan porque **Ada los tuvo primero, en
> 1983**, con un diseño que sigue siendo el más explícito de todos: los parámetros del genérico se
> declaran, incluidas las operaciones que necesita, y la instanciación es una sentencia visible. C++
> llegó después con las plantillas —más potentes y con la instanciación implícita—, y Java y C# mucho
> más tarde.
>
> Y en el otro extremo, **COBOL no tiene genéricos** y **Fortran los resuelve con interfaces genéricas**
> que son sobrecarga con otro nombre. Ver las tres estrategias juntas explica por qué "genérico"
> significa cosas distintas según el lenguaje.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `max=<el mayor>`
- **Regla:** `max<T>(a, b) = a si a>b, si no b`

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

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
PROGRAM-ID. MAXIMO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  MAYOR   PIC S9(9) COMP-3.
01  ED-M    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE MAYOR = FUNCTION MAX(A, B)

    MOVE MAYOR TO ED-M
    DISPLAY "max=" FUNCTION TRIM(ED-M)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene genéricos, y no los ha tenido nunca.** Cada
subprograma trabaja con los tipos exactos declarados en su `LINKAGE SECTION`, y para otro tipo hay
que escribir otro subprograma.

Lo que sí tiene, y cumple una función parecida, es el **copybook con `REPLACING`**:

```cobol
*> En el copybook TABLA:
01  :PREFIJO:-TABLA.
    05  :PREFIJO:-CUANTOS  PIC 9(4) COMP-3.
    05  :PREFIJO:-ELEM     OCCURS 1 TO 100 TIMES
                           DEPENDING ON :PREFIJO:-CUANTOS
                           PIC :TIPO:.

*> Y en cada programa:
COPY TABLA REPLACING ==:PREFIJO:== BY ==CLI==
                     ==:TIPO:==    BY ==X(40)==.
COPY TABLA REPLACING ==:PREFIJO:== BY ==IMP==
                     ==:TIPO:==    BY ==S9(11)V99 COMP-3==.
```

`COPY ... REPLACING` es **sustitución textual en tiempo de compilación**, parametrizada. Es
exactamente lo que hacían las macros de C antes de las plantillas, y tiene los mismos problemas:
ninguna comprobación de tipos, errores que aparecen en el texto expandido, y ninguna forma de
restringir qué se puede sustituir.

Es genérico en el sentido más literal —el mismo texto, con otros nombres— y es la razón de que el
material de esta clase sea tan revelador: **la diferencia entre una macro y un genérico es la
comprobación**, y esa comprobación es lo que Ada añadió en 1983.

`FUNCTION MAX` de este programa sí es polimórfica, pero está incorporada al compilador: no se puede
escribir otra igual.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program maximo
   implicit none
   integer :: a, b

   read(*, *) a, b
   write(*, '(A,I0)') 'max=', mayor(a, b)

contains

   pure function mayor(x, y) result(m)
      integer, intent(in) :: x, y
      integer :: m
      m = merge(x, y, x > y)
   end function mayor

end program maximo
```

**Lo que esta clase enseña en Fortran.** Fortran **no tiene genéricos con parámetros de tipo**. Lo que
tiene son **interfaces genéricas**, que son sobrecarga: se escriben varias versiones y se agrupan bajo
un nombre común.

```fortran
interface mayor
   module procedure mayor_entero
   module procedure mayor_real
   module procedure mayor_doble
end interface

! Y ahora `mayor(a, b)` elige según los tipos, en tiempo de compilación.
```

Es exactamente el mecanismo con el que están construidas las funciones intrínsecas del propio
lenguaje: `max`, `abs`, `sqrt` y `sum` funcionan con todos los tipos numéricos porque hay una versión
por tipo detrás.

El precio es evidente: **hay que escribir cada versión**. Para una función corta como esta, es
copiar y pegar cambiando el tipo — el problema que los genéricos vinieron a resolver.

Por eso una parte del mundo Fortran usa **el preprocesador de C** (`fpp` o `cpp`) para generar las
versiones a partir de una plantilla:

```fortran
#define TIPO integer
#include "mayor.inc"
#define TIPO real(real64)
#include "mayor.inc"
```

Que es, otra vez, la macro textual de COBOL con otra sintaxis.

El comité lleva años trabajando en **plantillas genéricas** para el estándar siguiente, y es la
característica más pedida por la comunidad. En 2026 todavía no están, y es probablemente la carencia
más señalada del lenguaje.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Generico is

   --  Un GENÉRICO: declara qué necesita del tipo que le pasen.
   generic
      type Elemento is private;
      with function "<" (L, R : Elemento) return Boolean is <>;
   function Mayor_Gen (A, B : Elemento) return Elemento;

   function Mayor_Gen (A, B : Elemento) return Elemento is
   begin
      if A < B then
         return B;
      else
         return A;
      end if;
   end Mayor_Gen;

   --  INSTANCIACIÓN explícita: se genera la versión para Integer.
   function Mayor is new Mayor_Gen (Integer);

   A, B : Integer;
begin
   Get (A);
   Get (B);

   Put ("max=");
   Put (Mayor (A, B), Width => 1);
   New_Line;
end Generico;
```

**Lo que esta clase enseña en Ada.** **Ada tuvo genéricos en 1983**, antes que C++, Java y C#, y su
diseño sigue siendo el más explícito de todos. La clave está en el bloque `generic`:

```ada
generic
   type Elemento is private;                                  --  el TIPO
   with function "<" (L, R : Elemento) return Boolean is <>;  --  la OPERACIÓN que necesita
```

**El genérico declara todo lo que exige del tipo**: no basta con decir "un tipo cualquiera", hay que
enumerar las operaciones que se van a usar. Si el tipo que instancias no tiene `<`, **no compila la
instanciación**, con un error que apunta al sitio correcto.

Compara con las plantillas de C++ antes de los conceptos: allí el error aparecía **dentro** de la
plantilla, con veinte niveles de expansión, y decía algo sobre un operador que faltaba en una línea
que no habías escrito. Los **conceptos de C++20** son exactamente esto de Ada, cuarenta años después.

Y la **instanciación es explícita**: `function Mayor is new Mayor_Gen (Integer);` es una sentencia que
se ve. En C++ ocurre sola al usar la plantilla, lo que es cómodo y hace muy difícil saber cuántas
versiones se están generando —una de las causas de los binarios enormes y las compilaciones lentas—.

Ada permite además parametrizar por **paquete completo**, no solo por tipo o función, lo que da un
sistema de módulos genéricos que Java y C# no tienen. Toda la biblioteca de contenedores de Ada 2005
está construida así.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Maximo;
{$MODE OBJFPC}{$H+}
uses SysUtils, Math;

var
  A, B: Integer;

begin
  Read(A, B);
  WriteLn('max=', IntToStr(Max(A, B)));
end.
```

**Lo que esta clase enseña en Pascal.** El Pascal ISO **no tiene genéricos**, y su sustituto histórico
era el **puntero sin tipo** —`Pointer`— con conversiones manuales, que es tan inseguro como suena.

Free Pascal y Delphi los añadieron en 2006, con una sintaxis propia:

```pascal
{ Free Pascal, modo ObjFPC }
generic function Mayor<T>(A, B: T): T;
begin
  if A < B then Result := B else Result := A;
end;

var
  M: Integer;
begin
  M := specialize Mayor<Integer>(3, 7);
end.
```

Las palabras **`generic`** y **`specialize`** son obligatorias en modo ObjFPC, y no existen en Delphi
—que usa la sintaxis `function Mayor<T>(...)` sin adornos—. Esa divergencia entre los dos dialectos es
una de las incompatibilidades más molestas del ecosistema Pascal.

Y hay una restricción importante: **el genérico se resuelve por instanciación explícita**, como en Ada,
y **no hay inferencia de argumentos de tipo** en las funciones libres. Hay que escribir
`specialize Mayor<Integer>(...)`, no `Mayor(3, 7)`. Delphi sí infiere en muchos casos.

Los genéricos de Object Pascal **generan código por tipo** —monomorfización, como C++ y Ada— así que
son rápidos y engordan el binario. `Generics.Collections` es la biblioteca estándar construida sobre
ellos, y es lo que dio a Delphi contenedores con tipos treinta años después de Turbo Pascal.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun mayor (a b)
  (if (< a b) b a))

(let* ((a (read))
       (b (read)))
  (format t "max=~D~%" (mayor a b)))
```

**Lo que esta clase enseña en Common Lisp.** En un lenguaje dinámico, **el polimorfismo paramétrico es
gratis**: `mayor` funciona con enteros, reales, fracciones, cadenas y cualquier cosa para la que `<`
esté definido. No hay que declarar nada.

Lo que Lisp añade, y no tiene ningún lenguaje del núcleo, es el **despacho múltiple** de CLOS:

```lisp
(defgeneric combinar (a b))

(defmethod combinar ((a number) (b number))  (+ a b))
(defmethod combinar ((a string) (b string))  (concatenate 'string a b))
(defmethod combinar ((a list)   (b list))    (append a b))
(defmethod combinar ((a number) (b string))  (format nil "~D~A" a b))
```

El método se elige según **los tipos de TODOS los argumentos**, no solo del primero. En Java, C++ o
Smalltalk el despacho es sobre el receptor y punto: para depender de dos tipos hay que usar el patrón
*Visitor*, que es notoriamente incómodo.

Y CLOS añade los **métodos auxiliares**, que permiten componer comportamiento sin herencia:

```lisp
(defmethod combinar :before ((a number) (b number)) (print "sumando..."))
(defmethod combinar :around (a b) (list :resultado (call-next-method)))
```

`:before`, `:after` y `:around` se ejecutan alrededor del método principal. Es programación orientada
a aspectos, en el estándar de 1994.

Y para el rendimiento, las **declaraciones de tipo** de la clase 052 permiten que SBCL genere código
especializado cuando hace falta: lo genérico por defecto, lo específico cuando se pide.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc mayor {a b} {
    return [expr {$a > $b ? $a : $b}]
}

gets stdin linea
lassign [split [string trim $linea]] a b

puts "max=[mayor $a $b]"
```

**Lo que esta clase enseña en Tcl.** Sin tipos no hay nada que parametrizar: `mayor` funciona con lo
que sea que `expr` sepa comparar. Es polimorfismo por ausencia de restricciones.

Y esa ausencia tiene una consecuencia que conviene ver: **la comparación depende de cómo interprete
`expr` los operandos**, no de un tipo declarado.

```tcl
expr {"10" > "9"}          ;# 1  -- los lee como NÚMEROS
expr {"abc" > "abd"}       ;# 0  -- como CADENAS, porque no son números
expr {"10" gt "9"}         ;# 0  -- forzando comparación de cadenas
```

Es exactamente la ambigüedad de la clase 051, aquí aplicada a una función "genérica": la misma función
compara de dos maneras distintas según los datos que reciba, y **eso puede ser lo que quieres o un
error silencioso**.

Cuando el comportamiento debe ser explícito, Tcl usa lo que la clase 068 llamaba tabla de despacho:
**pasar el comparador como argumento**.

```tcl
proc mayorCon {a b comparador} {
    return [expr {[apply $comparador $a $b] ? $a : $b}]
}
mayorCon 3 7 {{x y} {expr {$x > $y}}}
```

Es el mismo mecanismo que el parámetro `with function "<"` del genérico de Ada, resuelto en ejecución
en lugar de al compilar. Y es exactamente lo que hace `lsort -command` de la biblioteca estándar,
que ordena con el criterio que le des.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub mayor {
    my ($x, $y) = @_;
    return $x > $y ? $x : $y;
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

print "max=", mayor($p, $q), "\n";
```

**Lo que esta clase enseña en Perl.** Como en Tcl, sin tipos no hay genéricos: la función acepta lo
que sea. Y como en Tcl, la trampa es que **hay que elegir el operador según cómo quieras comparar**
—la tabla de la clase 051—:

```perl
sub mayor_num { $_[0] > $_[1] ? $_[0] : $_[1] }     # numérico
sub mayor_txt { $_[0] gt $_[1] ? $_[0] : $_[1] }    # alfabético
```

Escribir una sola función que sirva para los dos exige **pasar el comparador**, que es el mismo patrón
de Ada y Tcl:

```perl
sub mayor_con {
    my ($cmp, $x, $y) = @_;
    return $cmp->($x, $y) > 0 ? $x : $y;
}
mayor_con(sub { $_[0] <=> $_[1] }, 3, 7);      # numérico
mayor_con(sub { $_[0] cmp $_[1] }, 'a', 'b');  # textual
```

`<=>` y `cmp` son los **operadores de comparación de tres vías** de la clase 055, y son exactamente lo
que `sort` espera:

```perl
sort { $a <=> $b } @numeros;
sort { $a->{edad} <=> $b->{edad} } @personas;
```

Y Perl tiene una forma de polimorfismo que sí se parece a los genéricos: **la sobrecarga de
operadores** con el pragma `overload`, que permite que una clase propia responda a `<`, `+` o `""`.
Con ella, una función escrita para números funciona con tu tipo sin cambiarla — que es la definición
operativa del polimorfismo paramétrico en un lenguaje dinámico.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

template <typename T>
T mayor(const T& a, const T& b) {
    return (a < b) ? b : a;
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "max=" << mayor(a, b) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `template <typename T>` genera **una función distinta por cada
tipo con el que se use**, en tiempo de compilación. Eso se llama **monomorfización**, y es la razón de
las tres características de C++ en este terreno:

1. **Sin coste en ejecución**: no hay conversiones, no hay indirección, el cuerpo se integra en línea.
2. **Binarios grandes y compilación lenta**: cada instanciación es código nuevo.
3. **Errores descomunales**: si el tipo no tiene `<`, el error aparece **dentro** de la plantilla.

C++20 resolvió el tercero con los **conceptos**, que son literalmente lo que Ada tenía en 1983:

```cpp
template <typename T>
concept Comparable = requires(T a, T b) { { a < b } -> std::convertible_to<bool>; };

template <Comparable T>
T mayor(const T& a, const T& b) { return (a < b) ? b : a; }
```

Ahora el error dice "`T` no satisface `Comparable`" en el sitio de la llamada, que es lo correcto.

Y la comparación con **Java** es la que da la lección de esta clase: Java **borra los tipos**. Hay una
sola versión del código, `List<String>` y `List<Integer>` son la misma clase en ejecución, y por eso
no puedes hacer `new T[]` ni `instanceof List<String>`. A cambio, el binario es pequeño y la
compilación rápida.

C++, Ada, Rust y C# (para tipos de valor) monomorfizan; Java y C# (para referencias) borran. **Ninguna
es mejor**, y saber cuál usa tu lenguaje explica muchas de sus limitaciones aparentemente
arbitrarias.

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

dcl-pi MAXIMO;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s mayorV like(a);       // LIKE: el tipo se hereda, no se repite
dcl-s salida char(30);

if a > b;
  mayorV = a;
else;
  mayorV = b;
endif;

salida = 'max=' + %char(mayorV);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** **RPG no tiene genéricos.** No hay parámetros de tipo, no hay
plantillas y no se puede escribir una función que sirva para `packed` y para `char`.

Lo que tiene, y cubre una parte del problema, son las **plantillas de datos** de la clase 052:

```rpgle
dcl-s tipoImporte packed(11:2) template;    // TEMPLATE: no ocupa memoria
dcl-s total  like(tipoImporte);
dcl-s parcial like(tipoImporte);

dcl-ds tipoCliente qualified template;
  codigo char(8);
  nombre char(40);
end-ds;
dcl-ds cliente likeds(tipoCliente);
```

`template` declara un molde y `like`/`likeds` lo copian. Eso resuelve la **duplicación de
declaraciones** —si cambia el tipo, cambia en un sitio— pero **no la duplicación de código**: sigue
haciendo falta una función por tipo.

Y hay dos mecanismos de bajo nivel que dan algo parecido a la genericidad, con las garantías de C:

```rpgle
dcl-pi *n;
  datos pointer;                       // un puntero a lo que sea
  tam   int(10) const;
end-pi;
...
dcl-s buffer char(65535) based(datos); // interpretar esos bytes como caracteres
```

`based(puntero)` es la variable `based` de PL/I de la clase 053: un nombre que mira donde apunte un
puntero. Con él se escriben rutinas que operan sobre "cualquier cosa", sin ninguna comprobación de
tipos. Se usa para hablar con las APIs del sistema, y en código de negocio se evita.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 maximo: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    put skip list ('max=' || trim(char(max(a, b))));

 end maximo;
```

**Lo que esta clase enseña en PL/I.** PL/I **no tiene genéricos con parámetros de tipo**, pero tiene
el atributo **`generic`**, que ya apareció en la clase 074 y que aquí es central: **selecciona entre
varios procedimientos según los tipos de los argumentos**.

```pli
declare mayor generic (
   mayor_bin  when (fixed binary, fixed binary),
   mayor_dec  when (fixed decimal, fixed decimal),
   mayor_char when (character, character)
);

x = mayor(1, 2);          /* llama a mayor_bin */
y = mayor('a', 'b');      /* llama a mayor_char */
```

Es exactamente la **interfaz genérica de Fortran** con otra sintaxis: sobrecarga declarada en una
tabla explícita. Y comparte su limitación: **hay que escribir cada versión**.

La ventaja frente a la sobrecarga implícita de C++ es que **la tabla se lee**. Para saber a qué se
llama, se mira la declaración `generic`, en lugar de reconstruir el algoritmo de resolución del
compilador.

Y PL/I tiene, en su lugar, algo que sí es genuinamente genérico y que ningún lenguaje del núcleo
ofrece: **la aritmética funciona sobre cualquier combinación de base y escala**. Una rutina escrita
para `fixed decimal(15,2)` acepta un `fixed binary(31)` porque el lenguaje convierte. Es
polimorfismo por conversión implícita — cómodo, y con todos los problemas de la clase 050.

Es una constante de esta sección: **PL/I resuelve muchos problemas por conversión donde los lenguajes
posteriores los resuelven por tipos**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript show: 'max=', (a max: b) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** `max:` está implementado **una sola vez**, en la clase
abstracta `Magnitude`, y funciona con todo lo que sepa compararse:

```smalltalk
Magnitude >> max: unaMagnitud
    ^self > unaMagnitud ifTrue: [ self ] ifFalse: [ unaMagnitud ]
```

`Number`, `Character`, `Date`, `Time`, `String` y `Duration` heredan de `Magnitude`. Basta con
implementar **`<`** en una clase nueva para heredar `max:`, `min:`, `between:and:`, `>`, `<=` y `>=`,
todos definidos en términos de `<`.

Eso es polimorfismo **por herencia de interfaz**, y es la respuesta de Smalltalk a esta clase: no hay
parámetros de tipo porque no hay tipos, y la reutilización viene de la jerarquía.

Y es exactamente el mismo diseño que `Comparable` de Java, `Ord` de Haskell y `PartialOrd` de Rust:
**una operación primitiva, y el resto derivado**. Smalltalk lo hizo en los 70 y sin necesidad de
declarar la interfaz — basta con responder al mensaje.

La contrapartida, honesta: **no hay comprobación estática**. Si pasas a `max:` un objeto que no
entiende `<`, el error aparece **cuando se ejecuta esa línea**, no al compilar. Es el mismo
compromiso de toda la sección sobre Smalltalk, y es la razón de que estos proyectos se apoyen tanto en
pruebas — y de que SUnit naciera aquí.

Existen investigaciones de tipado estático para Smalltalk —Strongtalk, y hoy los *type hints* de
Pharo— pero nunca entraron en el lenguaje.

---

## Y de vuelta a la clase

Lo transferible es la distinción entre **borrado de tipos** y **monomorfización**. Java borra: hay
**una** versión del código y los tipos desaparecen en ejecución. C++, Ada y Rust **generan una versión
por cada tipo usado**: más rápido, sin conversiones, y a costa de binarios grandes y tiempos de
compilación largos. Ninguna es mejor en abstracto, y saber cuál usa tu lenguaje explica sus tiempos de
compilación, el tamaño de su binario y por qué en Java no puedes hacer `new T[]`.

⏮️ [Volver a la clase 078](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
