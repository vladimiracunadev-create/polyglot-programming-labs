# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 069

> [⬅️ Volver a la clase 069](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Fibonacci, el ejemplo canónico de recursión. Y también el canónico de **por qué la recursión ingenua
es una mala idea**: `fib(30)` hace más de dos millones de llamadas para calcular un número que un
bucle obtiene en treinta pasos. Pero la pregunta de esta página es anterior a la eficiencia:
**¿puede este lenguaje llamarse a sí mismo?** Y en dos de ellos, la respuesta original fue *no*.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **recursión y el coste de la pila**, y estos lenguajes lo enseñan porque
> muestran **de dónde vino la prohibición**. En COBOL clásico el `WORKING-STORAGE` es estático: hay un
> solo juego de variables por programa, así que una segunda llamada pisaría las de la primera.
> **FORTRAN 77 prohibía explícitamente la recursión** por el mismo motivo. No era una omisión: era una
> consecuencia de no tener pila de activación.
>
> Enfrente, Lisp y Pascal se diseñaron **alrededor** de la recursión, y M la consigue con `new`, que
> es ámbito dinámico en lugar de una pila léxica.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (0 <= n <= 30) → stdout: `fib=<F(n)>`
- **Regla:** `F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)`

| stdin | esperado |
|---|---|
| `10` | `fib=55` |
| `1` | `fib=1` |
| `0` | `fib=0` |

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
PROGRAM-ID. FIBONACCI.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4)  COMP-3.
01  I       PIC 9(4)  COMP-3.
01  A       PIC 9(18) COMP-3.
01  B       PIC 9(18) COMP-3.
01  T       PIC 9(18) COMP-3.
01  ED-F    PIC Z(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE 0 TO A
    MOVE 1 TO B

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE T = A + B
        MOVE B TO A
        MOVE T TO B
    END-PERFORM

    MOVE A TO ED-F
    DISPLAY "fib=" FUNCTION TRIM(ED-F)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Este programa es **iterativo, y es lo correcto**, porque el
COBOL clásico **no puede recurrir**. La razón es la de la clase 042: `WORKING-STORAGE` es
**estático**. Existe un solo juego de variables por programa, creado al cargarlo. Si un programa se
llamara a sí mismo, la segunda invocación escribiría encima de las variables de la primera.

No es una limitación arbitraria: es la consecuencia directa de un modelo de memoria sin pila de
activación. Lo mismo pasaba en FORTRAN 77 y en el PL/I sin el atributo `recursive`.

**COBOL 2002 lo resolvió** con dos piezas que hay que declarar juntas:

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. FIB RECURSIVE.          *> 1) el programa se declara recursivo

DATA DIVISION.
LOCAL-STORAGE SECTION.              *> 2) almacenamiento por INVOCACIÓN
01  TEMPORAL  PIC 9(9) COMP-3.
WORKING-STORAGE SECTION.
01  CONTADOR  PIC 9(9) COMP-3.      *> esto sigue siendo compartido
```

`LOCAL-STORAGE` se crea **al entrar y se destruye al salir**, como una variable local de C. Es
literalmente la pila que COBOL no tenía. Y la coexistencia de las dos secciones en el mismo programa
es reveladora: puedes elegir, campo a campo, qué es compartido y qué es por invocación.

Aun así, el COBOL de producción es iterativo casi siempre — y para Fibonacci, la versión iterativa de
arriba hace **30 pasos** donde la recursiva ingenua haría 2,7 millones.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program fibonacci
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0)') 'fib=', fib(n)

contains

   recursive function fib(k) result(f)
      integer, intent(in) :: k
      integer :: f
      if (k < 2) then
         f = k
      else
         f = fib(k - 1) + fib(k - 2)
      end if
   end function fib

end program fibonacci
```

**Lo que esta clase enseña en Fortran.** La palabra **`recursive`** de la línea de la función no es
decorativa: **hasta Fortran 90, la recursión estaba prohibida por el estándar**.

El motivo es idéntico al de COBOL. En FORTRAN 77, las variables locales de una subrutina eran
**estáticas**: se asignaban una vez, al cargar el programa. Muchos compiladores incluso guardaban la
dirección de retorno en una posición fija dentro de la propia subrutina — así que una segunda llamada
la sobrescribía y el `RETURN` volvía al sitio equivocado.

Fortran 90 introdujo `recursive` como palabra que **activa el almacenamiento automático** para esa
función. Y `result(f)` es obligatorio en las funciones recursivas del F90/F95: sin él, el nombre de
la función designaría a la vez el resultado y la llamada recursiva, y sería ambiguo.

**Fortran 2018 invirtió la regla**: ahora los procedimientos son recursivos **por defecto** y existe
`non_recursive` para declarar lo contrario. Un lenguaje de 1957 cambiando su valor por defecto en
2018 es exactamente lo que esta sección quiere mostrar.

Y `contains` merece una nota: los procedimientos internos declarados ahí **ven las variables del
programa que los contiene**, como una clausura. Es el mecanismo de anidamiento de Pascal y de Ada,
que C nunca tuvo.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Fibonacci is

   function Fib (K : Natural) return Natural is
   begin
      if K < 2 then
         return K;
      else
         return Fib (K - 1) + Fib (K - 2);
      end if;
   end Fib;

   N : Integer;
begin
   Get (N);
   Put ("fib="); Put (Fib (N), Width => 1); New_Line;
end Fibonacci;
```

**Lo que esta clase enseña en Ada.** La recursión funciona sin declarar nada: Ada nació con
almacenamiento automático, porque venía de la tradición ALGOL/Pascal y no de la de FORTRAN.

Fíjate en el tipo del parámetro: **`Natural`**, no `Integer`. `Natural` es un subtipo predefinido
—`subtype Natural is Integer range 0 .. Integer'Last`— y eso significa que **llamar a `Fib (-1)`
levanta `Constraint_Error` en el punto de la llamada**, no dentro de la función.

Es una guarda que no hay que escribir. En C, en Java o en Python, la protección contra el argumento
negativo es un `if` al principio de la función que alguien tiene que recordar poner, y que se
comprueba en cada llamada aunque el llamante ya supiera que el valor era válido.

Ada tiene además la pieza que hace de esto una garantía y no solo una comprobación: los **contratos**.

```ada
function Fib (K : Natural) return Natural
  with Pre  => K <= 30,
       Post => Fib'Result >= 0;
```

Con SPARK, esas condiciones **se demuestran estáticamente**: el analizador verifica que ninguna
llamada del programa puede violar la precondición, y entonces la comprobación en ejecución se
elimina. Seguridad sin coste.

Y sobre la pila: en sistemas embebidos con memoria limitada, la recursión se **prohíbe por norma de
proyecto** —el perfil Ravenscar y las guías de aviónica lo exigen— porque el consumo de pila debe ser
analizable antes de volar. Ahí, la versión iterativa no es una optimización: es un requisito.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Fibonacci;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function Fib(K: Integer): Int64;
begin
  if K < 2 then
    Result := K
  else
    Result := Fib(K - 1) + Fib(K - 2);
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('fib=', IntToStr(Fib(N)));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal se diseñó **alrededor de la recursión**: Wirth venía de
ALGOL, donde el almacenamiento automático y la pila de activación eran el modelo desde el principio.
No hay ninguna palabra que activar.

Y Pascal permite algo que ni C ni Java tienen: **procedimientos anidados dentro de procedimientos**,
que ven las variables del que los contiene.

```pascal
function Fib(K: Integer): Int64;

  function Auxiliar(A, B, Cuenta: Int64): Int64;   { anidada: ve K }
  begin
    if Cuenta = 0 then Auxiliar := A
    else Auxiliar := Auxiliar(B, A + B, Cuenta - 1);
  end;

begin
  Result := Auxiliar(0, 1, K);
end;
```

Esa `Auxiliar` es **recursiva de cola**: la llamada recursiva es lo último que hace, así que no hay
nada pendiente en el marco de pila y un compilador puede convertirla en un salto. FPC lo hace con
`-O2` en muchos casos, aunque **no está garantizado por el estándar**.

Y Pascal tiene una construcción para la recursión mutua que hoy casi nadie usa pero que fue
influyente: **`forward`**.

```pascal
function Par(N: Integer): Boolean; forward;      { se declara ahora, se define luego }
function Impar(N: Integer): Boolean;
begin ... Par(N - 1) ... end;
function Par(N: Integer): Boolean;
begin ... Impar(N - 1) ... end;
```

`forward` existe porque Pascal compila en **una sola pasada** —la razón de su velocidad, vista en la
clase 042— y necesita conocer la firma antes del uso. Es el antepasado directo de los prototipos de C.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun fib (k)
  (if (< k 2)
      k
      (+ (fib (- k 1)) (fib (- k 2)))))

(let ((n (read)))
  (format t "fib=~D~%" (fib n)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp **nació recursivo**. La definición original de
McCarthy en 1958 no tenía bucles: `car`, `cdr`, `cons`, `cond` y la recursión eran todo el lenguaje.
Los bucles llegaron después, como conveniencia.

Y aquí hay una advertencia que sorprende a mucha gente: **el estándar de Common Lisp NO garantiza la
optimización de llamadas de cola.**

```lisp
(defun fib-cola (k &optional (a 0) (b 1))
  (if (zerop k) a (fib-cola (1- k) b (+ a b))))   ; recursiva de COLA
```

Esa función **no consume pila en SBCL** con `(optimize (debug 1))`, y **sí la consume** con
`(debug 3)`, porque en modo depuración el compilador conserva los marcos para poder mostrarlos. El
mismo código, dos comportamientos, según una declaración.

**Scheme sí lo garantiza en el estándar**, y esa es una de las diferencias de diseño más importantes
entre los dos dialectos: en Scheme se puede escribir un bucle infinito como recursión de cola y es
correcto por definición; en Common Lisp hay que confiar en el compilador o usar `loop`.

Y para Fibonacci, la solución idiomática de Lisp no es ninguna de las dos: es **memorizar**.

```lisp
(defvar *memo* (make-hash-table))
(defun fib (k)
  (or (gethash k *memo*)
      (setf (gethash k *memo*)
            (if (< k 2) k (+ (fib (- k 1)) (fib (- k 2)))))))
```

Con eso, `fib(100)` es instantáneo y exacto —los enteros no desbordan—, y la estructura recursiva se
conserva. Es la técnica que convierte el ejemplo canónico de "recursión ineficiente" en un algoritmo
lineal sin dejar de ser recursivo.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc fib {k} {
    if {$k < 2} { return $k }
    return [expr {[fib [expr {$k - 1}]] + [fib [expr {$k - 2}]]}]
}

gets stdin linea
set n [string trim $linea]

puts "fib=[fib $n]"
```

**Lo que esta clase enseña en Tcl.** La recursión funciona, y Tcl tiene un límite explícito y
consultable que casi ningún lenguaje expone así:

```tcl
interp recursionlimit {} 1000        ;# consultar y fijar la profundidad máxima
```

Por defecto son 1000 niveles. Superarlo da un error capturable —"too many nested evaluations"— en
lugar de un desbordamiento de pila que revienta el proceso. Es una decisión típica de un lenguaje de
guion incrustado: **fallar de forma controlada dentro de una aplicación anfitriona** importa más que
apurar la pila.

Y Tcl 8.6 añadió **`tailcall`**, que es la optimización de llamada de cola **explícita**:

```tcl
proc fib-cola {k {a 0} {b 1}} {
    if {$k == 0} { return $a }
    tailcall fib-cola [expr {$k - 1}] $b [expr {$a + $b}]
}
```

`tailcall` **reemplaza el marco de pila actual** en lugar de apilar uno nuevo. Con él, la recursión de
cola es un bucle de verdad y no hay límite de profundidad.

Que sea un comando explícito en vez de una optimización automática es coherente con todo el diseño de
Tcl: **si algo cambia el comportamiento, se escribe**. Y tiene una ventaja sobre la optimización
implícita — no depende del nivel de optimización ni del compilador, así que se puede confiar en ella.

Junto a `coroutine` de la clase 066, `tailcall` forma parte del paquete de control de flujo avanzado
que Tcl añadió en 8.6, todo construido sobre la máquina de ejecución sin pila (*NRE*) que reescribió
el intérprete en 2008.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub fib {
    my ($k) = @_;
    return $k if $k < 2;
    return fib($k - 1) + fib($k - 2);
}

my $n = <STDIN>;
chomp $n;

print "fib=", fib($n), "\n";
```

**Lo que esta clase enseña en Perl.** La recursión funciona sin ceremonia, y Perl avisa si se pasa:
con `use warnings`, más de 100 niveles produce *"Deep recursion on subroutine"*. Es un aviso, no un
error, y se puede silenciar — pero por defecto te dice que algo puede estar mal.

Perl tiene además una forma **explícita** de llamada de cola, con una sintaxis que sorprende:

```perl
sub fib_cola {
    my ($k, $a, $b) = @_;
    return $a if $k == 0;
    @_ = ($k - 1, $b, $a + $b);
    goto &fib_cola;              # reemplaza el marco actual: NO apila
}
```

`goto &subrutina` **no es un salto**: sustituye el marco de la llamada actual por el de la nueva, con
los argumentos que haya en `@_`. Es exactamente `tailcall` de Tcl, con un nombre desafortunado
heredado de la época en que `goto` no tenía mala prensa.

Se usa poco para recursión y mucho para **delegación**: una función que decide a quién llamar y le
cede su propio marco, de modo que el llamante original ni se entera. Es la base de varias técnicas de
`AUTOLOAD` y de despacho dinámico en CPAN.

Y para Fibonacci, la solución idiomática de Perl es memorizar con un hash, exactamente como en Lisp:

```perl
my %memo;
sub fib { my ($k) = @_; $memo{$k} //= $k < 2 ? $k : fib($k-1) + fib($k-2) }
```

Una línea, gracias a `//=` —el operador de coalescencia de la clase 053— que asigna solo si el valor
no estaba definido.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

long long fib(int k) {
    if (k < 2) return k;
    return fib(k - 1) + fib(k - 2);
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "fib=" << fib(n) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** La recursión funciona, y el **desbordamiento de pila es
comportamiento indefinido**: no hay excepción, no hay error controlado, el proceso muere con una
violación de segmento. Es una de las diferencias más prácticas con Tcl, Perl o Java.

C++ aplica la optimización de llamada de cola con `-O2` cuando puede, pero **no está garantizada por
el estándar**, así que no se puede escribir un bucle infinito como recursión de cola y confiar en
ello.

Lo que sí tiene C++ es algo que ningún otro lenguaje de esta página ofrece: **recursión en tiempo de
compilación**.

```cpp
constexpr long long fib(int k) {
    return k < 2 ? k : fib(k - 1) + fib(k - 2);
}

constexpr long long f10 = fib(10);      // 55, calculado AL COMPILAR
static_assert(f10 == 55);               // y comprobado también al compilar
```

Con `constexpr` (C++11, ampliado en C++14 y C++20), la misma función sirve para las dos cosas: si los
argumentos se conocen al compilar, **el resultado se incrusta como una constante** y no queda ninguna
llamada en el binario; si no, se ejecuta normalmente.

Antes de `constexpr`, esto se hacía con **metaprogramación de plantillas**:

```cpp
template<int N> struct Fib { static const long long v = Fib<N-1>::v + Fib<N-2>::v; };
template<> struct Fib<0> { static const long long v = 0; };
template<> struct Fib<1> { static const long long v = 1; };
```

Ese estilo —descubierto casi por accidente en los 90, cuando alguien se dio cuenta de que las
plantillas de C++ eran accidentalmente Turing-completas— es el antepasado de todo el cálculo en
tiempo de compilación moderno. Y la recursión era su única forma de iterar.

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

dcl-proc Principal;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dcl-s salida char(40);

  salida = 'fib=' + %char(fib(n));
  dsply salida;
end-proc;

dcl-proc fib;
  dcl-pi *n int(20);
    k int(10) const;
  end-pi;

  if k < 2;
    return k;
  endif;
  return fib(k - 1) + fib(k - 2);
end-proc;
```

**Lo que esta clase enseña en RPG.** **El RPG clásico no podía recurrir**, por la misma razón que
COBOL: el almacenamiento del programa era estático y el ciclo del programa no contemplaba una segunda
activación.

**ILE lo cambió.** Los **subprocedimientos** (`dcl-proc`) tienen **almacenamiento automático por
defecto**: sus variables se crean al entrar y se destruyen al salir, en la pila. Con eso, la recursión
funciona sin declarar nada, como en este programa.

La diferencia se ve en la declaración:

```rpgle
dcl-proc fib;
  dcl-s temporal int(10);              // AUTOMÁTICA: una por invocación
  dcl-s contador int(10) static;       // ESTÁTICA: compartida entre invocaciones
```

`static` es la palabra que devuelve el comportamiento antiguo, y se usa deliberadamente para
contadores y cachés que deben sobrevivir entre llamadas. Es la misma pareja que `LOCAL-STORAGE` y
`WORKING-STORAGE` en COBOL 2002, y que `automatic` y `static` en PL/I desde 1964.

Que los tres lenguajes de negocio de esta página tengan **exactamente la misma distinción con
nombres distintos** no es casualidad: es la consecuencia de haber nacido sin pila y haberla añadido
después.

Y el `main()` en `ctl-opt` de este programa es lo que desactiva el ciclo, como se vio en la clase 044:
sin él, el ciclo intentaría gobernar la ejecución y los subprocedimientos convivirían con él de forma
confusa.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 fibonacci: procedure options(main);

    declare n fixed binary(31);

    get list (n);
    put skip list ('fib=' || trim(char(fib(n))));

 fib: procedure (k) returns (fixed binary(31)) recursive;
    declare k fixed binary(31);
    if k < 2 then return (k);
    return (fib(k - 1) + fib(k - 2));
 end fib;

 end fibonacci;
```

**Lo que esta clase enseña en PL/I.** La palabra **`recursive`** al final de la cabecera es
obligatoria, y es la misma historia que en COBOL y Fortran: **sin ella, el almacenamiento del
procedimiento es estático** y la segunda invocación pisaría la primera.

Lo que hace distinto a PL/I es que la relación entre recursión y almacenamiento está **explícita en
el vocabulario del lenguaje** desde 1964, con las cuatro clases de la clase 042:

| Clase | Comportamiento |
|---|---|
| `automatic` | Por invocación — es lo que la recursión necesita |
| `static` | Una sola copia para todo el programa |
| `controlled` | Una **pila de asignaciones** que tú manejas con `allocate`/`free` |
| `based` | Donde apunte un puntero |

`controlled` merece atención en esta clase porque **es una pila explícita**: cada `allocate` de una
variable `controlled` **apila** una instancia nueva, y `free` desapila la anterior. Con eso se puede
implementar recursión a mano, guardando el estado sin depender de la pila del procesador.

En 1964, cuando muchas máquinas no tenían instrucciones de pila y la recursión era cara, poder
gestionar una pila de datos desde el lenguaje era una herramienta seria. Hoy es una curiosidad — pero
explica cómo se escribían algoritmos recursivos antes de que la recursión fuera barata.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
FIB ; Fibonacci -- clase 069
 read n
 write "fib=", $$fib(n), !
 quit
 ;
fib(k) ; el k-esimo numero de Fibonacci
 quit:k<2 k
 quit $$fib(k-1) + $$fib(k-2)
```

**Lo que esta clase enseña en M.** La recursión funciona, y la razón es la pieza más peculiar del
lenguaje: **`new`**.

En M **todas las variables son globales al proceso** por defecto. Una rutina que se llame a sí misma
compartiría las variables con su propia invocación anterior, exactamente el problema de COBOL. La
solución es declarar explícitamente qué se quiere salvar:

```mumps
fib(k) ;
 new a, b                ; guarda los valores ACTUALES de a y b...
 set a = $$fib(k-1)
 set b = $$fib(k-2)
 quit a + b              ; ...y al salir, se restauran
```

`new` no crea variables locales en el sentido léxico: **guarda el valor que la variable tuviera —sea
de quien sea— y lo restaura al salir de la rutina**. Es **ámbito dinámico**, el mismo mecanismo que
`local` en Perl y que las variables especiales de Common Lisp.

La consecuencia es sutil y hay que conocerla: si `fib` llamara a otra rutina que usara `a`, **esa
rutina vería la `a` de `fib`**, no la suya. Con ámbito léxico eso sería imposible. Es más frágil y a
la vez permite cosas que el ámbito léxico no: una rutina puede fijar un valor "para todo lo que llame
desde aquí", que es el patrón que en otros lenguajes se resuelve con un parámetro de contexto pasado
por toda la cadena de llamadas.

Este programa no necesita `new` porque los parámetros de una función extrínseca ya son automáticos.
Pero cualquier variable temporal declarada dentro sí lo necesitaría, y olvidarlo es el error clásico
de la recursión en M.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n fib |

n := stdin nextLine trimBoth asNumber.

fib := nil.
fib := [ :k | k < 2 ifTrue: [ k ] ifFalse: [ (fib value: k - 1) + (fib value: k - 2) ] ].

Transcript show: 'fib=', (fib value: n) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Fíjate en las dos líneas de `fib`: primero se declara
`nil` y **después** se le asigna el bloque. Eso es necesario porque el bloque **se refiere a `fib`
desde dentro**, y la variable tiene que existir antes de que el bloque la capture.

Es el problema clásico de la **recursión anónima**: un bloque sin nombre no puede llamarse a sí mismo.
La solución de este programa —una variable capturada por la clausura— es la que usan JavaScript,
Python y cualquier lenguaje con lambdas. La solución teórica elegante es el **combinador Y**, que
existe y que en la práctica nadie escribe.

Lo normal en Smalltalk, claro, es que la recursión sea entre **métodos**, donde el nombre existe:

```smalltalk
Integer >> fib
    self < 2 ifTrue: [ ^self ].
    ^(self - 1) fib + (self - 2) fib
```

Y ahí aparece algo notable: **acabas de añadir un método a la clase `Integer`**, la del sistema. En
Smalltalk las clases están abiertas y se pueden extender desde tu código; `10 fib` funcionaría en toda
la imagen. Ruby heredó esa capacidad —y el debate sobre si conviene, que allí se llama *monkey
patching*—.

Sobre la pila: `thisContext` de la clase 066 **es** el marco de activación como objeto, así que en
Smalltalk se puede **inspeccionar la pila de recursión desde el propio programa**, contar su
profundidad o modificarla. No hay optimización de llamada de cola en el estándar, y el desbordamiento
levanta una excepción capturable en lugar de matar el proceso.

---

## Y de vuelta a la clase

Dos ideas. La primera: **la recursión necesita almacenamiento automático**, y por eso los lenguajes
que nacieron sin pila no la tenían. Cuando veas `RECURSIVE` en COBOL, `recursive` en Fortran o PL/I,
o `LOCAL-STORAGE`, estás viendo la palabra que activa la pila.

La segunda: **la recursión de cola no es magia, es una optimización que el compilador puede hacer o
no**. Scheme la garantiza en el estándar; Common Lisp **no**; C++, Ada y Fortran la hacen si
optimizan; Python la rechaza por decisión de diseño. Escribir una función recursiva de cola no la
convierte en un bucle salvo que alguien te lo prometa por escrito.

⏮️ [Volver a la clase 069](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
