# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 114

> [⬅️ Volver a la clase 114](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Doblar cada elemento sin tocar la lista original. Es `map`, la operación fundacional del paradigma
funcional, y su nombre viene de aquí: **`maplist` está en el manual de Lisp de 1960**. Y hay una
sorpresa en esta página: **Fortran resuelve esta clase sin bucle y sin función auxiliar** —`v * 2`— y
lo hace por una razón que no tiene nada que ver con la elegancia funcional.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **transformación sin mutación**, y estos lenguajes lo enseñan porque muestran
> las dos motivaciones históricas, que son distintas. **Lisp (1958)** llegó a las funciones puras por el
> cálculo lambda y el razonamiento matemático. **Fortran 90** llegó a lo mismo por el rendimiento: `v =
> v * 2` y `pure` existen **para que el compilador pueda vectorizar y paralelizar**, y esa es la razón
> por la que Fortran tiene la única declaración de pureza comprobada de toda la página.
>
> Dos caminos opuestos —la demostración y la máquina— hacia la misma propiedad: **si nada muta, el orden
> no importa**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `doblados=<cada x·2 unidos por ->`
- **Regla:** `doblados = map(x → 2x, lista)`

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6` |
| `5` | `doblados=10` |
| `2 4` | `doblados=4-8` |

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
PROGRAM-ID. FUNC1.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2)  COMP VALUE 0.
01  I       PIC 9(4)  COMP.
01  L       PIC 9(4)  COMP.
01  N       PIC 9(4)  COMP VALUE 0.
01  ORIGEN.
    05  ELEM  PIC S9(9) COMP-3 OCCURS 100 TIMES.
01  DESTINO.
    05  ELEM-D PIC S9(18) COMP-3 OCCURS 100 TIMES.
01  SALIDA  PIC X(200) VALUE SPACES.
01  SPOS    PIC 9(4) COMP VALUE 1.
01  ED      PIC -(17)9.
01  TXT     PIC X(20).

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

    *> La tabla ORIGEN no se toca: el resultado va a DESTINO
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE ELEM-D(I) = ELEM(I) * 2
    END-PERFORM

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE ELEM-D(I) TO ED
        MOVE FUNCTION TRIM(ED) TO TXT
        MOVE 0 TO L
        INSPECT FUNCTION REVERSE(TXT) TALLYING L FOR LEADING SPACE
        COMPUTE L = 20 - L
        IF I > 1
            MOVE "-" TO SALIDA(SPOS:1)
            ADD 1 TO SPOS
        END-IF
        MOVE TXT(1:L) TO SALIDA(SPOS:L)
        ADD L TO SPOS
    END-PERFORM

    COMPUTE L = SPOS - 1
    DISPLAY "doblados=" SALIDA(1:L)
    STOP RUN.

CERRAR-TOKEN.
    IF TLEN > 0
        ADD 1 TO N
        COMPUTE ELEM(N) = FUNCTION NUMVAL(TOKEN)
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** COBOL **no tiene nada funcional**: no hay `map`, no hay
funciones de primera clase (clase 085) y no hay estructuras inmutables. Lo que hace este programa es
lo único posible: **escribir el resultado en una tabla distinta y no tocar la original**.

Y eso, que parece pobre, resulta ser **la disciplina central del procesamiento por lotes**.

```text
FICHERO-ENTRADA  →  programa  →  FICHERO-SALIDA
```

Un lote COBOL clásico **no modifica su entrada**: la lee y escribe un fichero nuevo. El de ayer sigue
ahí. Si algo sale mal, se vuelve a ejecutar con el mismo fichero de entrada y **se obtiene exactamente
el mismo resultado**.

Eso es una función pura a escala de sistema: **misma entrada, misma salida, sin efectos sobre lo que
había**. Y no es teoría — es la razón de que los procesos nocturnos de un banco se puedan repetir
cuando falla uno intermedio, y de que exista la práctica de conservar generaciones de ficheros.

En z/OS eso tiene incluso soporte del sistema: los **grupos de datos generacionales**.

```text
//SALIDA DD DSN=BANCO.MOVTOS(+1),DISP=(NEW,CATLG)
```

`(+1)` crea **la generación siguiente**; `(0)` es la actual y `(-1)` la anterior. El sistema conserva
automáticamente las últimas N versiones. Es control de versiones de datos integrado en el sistema
operativo desde los años sesenta, y es **inmutabilidad a nivel de fichero**.

Quien haya trabajado con almacenamiento inmutable, con *event sourcing* o con la arquitectura de un
*data lake* reconocerá el patrón inmediatamente: **no modifiques, añade una versión nueva**. Los
mainframes llevan sesenta años haciéndolo, y por la misma razón — **poder repetir el proceso**.

Y dentro del programa, COBOL sí tiene **funciones intrínsecas puras** desde 1989: `FUNCTION NUMVAL`,
`FUNCTION MAX`, `FUNCTION REVERSE`, `FUNCTION TRIM`. Se usan en expresiones y no tienen efectos. Es
poco, y es lo que hay.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program func1
   implicit none
   integer, allocatable :: v(:), doblados(:)
   integer :: n, ios, i
   character(len=400) :: linea, salida
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

   doblados = v * 2            ! sin bucle: `v` NO se modifica

   salida = ''
   do i = 1, n
      write(buf, '(I0)') doblados(i)
      if (i == 1) then
         salida = trim(buf)
      else
         salida = trim(salida) // '-' // trim(buf)
      end if
   end do

   write(*, '(A)') 'doblados=' // trim(salida)
end program func1
```

**Lo que esta clase enseña en Fortran.** `doblados = v * 2` es la línea de esta clase, y merece
insistir en lo que ya se apuntó en la clase 107: **es programación declarativa, y llegó a Fortran por
el rendimiento, no por la elegancia**.

Cuando el compilador ve `doblados = v * 2`, sabe **que cada elemento es independiente del resto**. Con
eso puede:

- Emitir instrucciones SIMD que procesan 8 o 16 elementos por ciclo.
- Repartir el arreglo entre hilos.
- Mandarlo a una GPU con `do concurrent`.

Un bucle escrito a mano con un acumulador **no le da esa información**, porque el orden de las
operaciones queda fijado por el programa.

Y de ahí sale la familia entera de construcciones "funcionales" de Fortran, todas por el mismo motivo:

```fortran
where (v < 0) v = 0                     ! asignación condicional sobre todo el arreglo
w = merge(a, b, mascara)                 ! elegir elemento a elemento
w = pack(v, v > 0)                        ! filtrar
s = sum(v)  /  m = maxval(v)               ! reducciones
forall (i = 1:n) w(i) = v(i) * 2            ! F95: sin orden garantizado
do concurrent (i = 1:n)                      ! F2008: "estas vueltas son independientes"
   w(i) = v(i) * 2
end do
```

**`do concurrent`** es la culminación: **el programador PROMETE que las iteraciones son
independientes**, y el compilador puede paralelizarlas o enviarlas a una GPU. Con `nvfortran` o
`gfortran -fopenmp`, ese bucle se ejecuta en una tarjeta gráfica sin escribir CUDA.

Y **`pure`** (clase 084) es el sello de todo esto: **la única declaración de pureza comprobada por un
compilador en toda esta página**. Una función `pure` no puede modificar sus argumentos, ni variables
globales, ni hacer entrada/salida, y **solo puede llamar a otras funciones puras**.

```fortran
pure function doblar(x) result(r)
```

Es exactamente la definición de función pura del paradigma funcional, y Fortran la exige **para poder
llamarla dentro de un `forall` o un `do concurrent`**.

La ironía es buena: **el lenguaje más antiguo de la página tiene la garantía funcional más fuerte, y
la tiene por razones de máquina**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Func1 is
   type Vector is array (Positive range <>) of Integer;

   --  Función PURA: recibe un vector y devuelve otro. No modifica nada.
   function Doblar (V : Vector) return Vector is
      R : Vector (V'Range);
   begin
      for I in V'Range loop
         R (I) := V (I) * 2;
      end loop;
      return R;
   end Doblar;

   Datos  : Vector (1 .. 100);
   N      : Natural := 0;
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
      N := N + 1;
      Datos (N) := Valor;
      Pos := Fin + 1;
   end loop;

   Put ("doblados=");
   declare
      R : constant Vector := Doblar (Datos (1 .. N));
   begin
      for I in R'Range loop
         Put (R (I), Width => 1);
         if I < R'Last then
            Put ("-");
         end if;
      end loop;
   end;
   New_Line;
end Func1;
```

**Lo que esta clase enseña en Ada.** `function Doblar (V : Vector) return Vector` **devuelve un arreglo
completo**, y eso en Ada funciona desde 1983 sin reservar memoria a mano: el tamaño del resultado se
deduce de `V'Range`, y el compilador se encarga.

Es una función pura en el sentido estricto —no toca nada de fuera— y hasta Ada 2012 el lenguaje **lo
imponía por gramática**: una función no podía tener parámetros `in out` (clase 109).

Ada 2012 relajó eso y a cambio dio la herramienta que va más lejos que cualquier otra de esta página:

```ada
function Doblar (V : Vector) return Vector
   with Global => null,                       --  NO toca NINGÚN estado global
        Post   => (for all I in V'Range => Doblar'Result (I) = V (I) * 2);
```

**`Global => null`** declara que la función no lee ni escribe ninguna variable de fuera. Y
**`Post` con un cuantificador universal** especifica el resultado completo, no un caso.

Y aquí está lo importante: **con SPARK, eso no se comprueba en ejecución — se DEMUESTRA**.

```bash
gnatprove --level=2 func1.adb
```

La herramienta genera obligaciones de prueba y las envía a demostradores automáticos (Z3, CVC5, Alt-
Ergo). Si pasan, **está matemáticamente probado que la función cumple su contrato para toda entrada
posible**, y que no hay desbordamientos, ni divisiones por cero, ni accesos fuera de rango.

Eso es lo que el paradigma funcional persigue con la pureza —**poder razonar sobre el código como
sobre matemáticas**— llevado hasta el final: no razonar a mano, sino que lo demuestre una máquina.

Y no es un ejercicio académico. SPARK se usa en el sistema de control de tráfico aéreo británico
(iFACTS), en el metro sin conductor de París, en aviónica de Airbus y en implementaciones
criptográficas.

Ada 2012 añadió además `for all` y `for some` **como expresiones normales del lenguaje**, no solo en
contratos:

```ada
if (for all I in V'Range => V (I) > 0) then ...
```

Cuantificadores lógicos en un `if`. Es la sintaxis de las matemáticas dentro de un lenguaje
imperativo.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Func1;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TVector = array of Integer;

{ Función pura: devuelve un vector NUEVO }
function Doblar(const V: TVector): TVector;
var
  I: Integer;
begin
  SetLength(Result, Length(V));
  for I := 0 to High(V) do
    Result[I] := V[I] * 2;
end;

var
  V, D: TVector;
  Linea, Tok, Salida: string;
  I: Integer;
  C: Char;

begin
  ReadLn(Linea);

  SetLength(V, 0);
  Tok := '';
  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        SetLength(V, Length(V) + 1);
        V[High(V)] := StrToInt(Tok);
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  D := Doblar(V);

  Salida := '';
  for I := 0 to High(D) do
  begin
    if Salida <> '' then Salida := Salida + '-';
    Salida := Salida + IntToStr(D[I]);
  end;

  WriteLn('doblados=', Salida);
end.
```

**Lo que esta clase enseña en Pascal.** Pascal no es funcional y tiene una pieza de esta clase que
conviene mirar de cerca: **el `const` del parámetro**.

```pascal
function Doblar(const V: TVector): TVector;
```

`const` hace dos cosas a la vez (clase 109): **prohíbe modificar el parámetro** —que es la mitad de la
definición de función pura— y **evita la copia**. Es la única forma en Pascal de expresar "recibo esto
para leerlo".

Y Object Pascal moderno tiene lo que hace falta para el estilo funcional, llegado tarde:

```pascal
type
  TFuncion = reference to function(X: Integer): Integer;   { Delphi 2009: CLAUSURA }

function Mapear(const V: TVector; F: TFuncion): TVector;
begin
  SetLength(Result, Length(V));
  for var I := 0 to High(V) do        { Delphi 10.3: variable EN LÍNEA }
    Result[I] := F(V[I]);
end;

D := Mapear(V, function(X: Integer): Integer
                begin Result := X * 2 end);
```

**`reference to function`** es la clausura: captura variables del ámbito y lleva conteo de referencias
para gestionarse sola (clase 083). Con ella, `map`, `filter` y `reduce` se escriben sin problema.

Free Pascal y Delphi traen además `TArray.Sort<T>` y `TEnumerable` con `Select` y `Where` al estilo
LINQ en `Spring4D`, la biblioteca comunitaria de referencia.

Sobre inmutabilidad, Pascal ofrece poco: **no hay estructuras persistentes ni tipos inmutables**. Lo
que hay es la disciplina de `const` y la copia al escribir de las cadenas (clase 102).

Y merece señalarse una asimetría llamativa que ya apareció en la clase 102: **las cadenas largas de
Pascal tienen copia al escribir y los arreglos dinámicos no**. Una cadena se comporta como un valor
inmutable; un arreglo, no. Esa incoherencia es lo que hace que el estilo funcional en Pascal exija más
cuidado del que parece — `Result := V` en una función **comparte**, no copia.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((v '()))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (push x v))
  (setf v (nreverse v))

  ;;  mapcar: la operación fundacional. `v` no se toca.
  (format t "doblados=~{~D~^-~}~%" (mapcar (lambda (x) (* 2 x)) v)))
```

**Lo que esta clase enseña en Common Lisp.** **`maplist` aparece en el manual del LISP 1.5 de 1962, y
`maplist` está en el memorando de McCarthy de 1960.** La palabra `map` que hoy usan JavaScript,
Python, Rust y todos los demás viene de ahí.

Y Lisp tiene una familia entera, con distinciones que la mayoría de los lenguajes no hace:

```lisp
(mapcar #'f lista)          ; aplica a cada ELEMENTO, devuelve lista
(mapcar #'+ l1 l2)          ; VARIAS listas a la vez, elemento a elemento
(maplist #'f lista)         ; aplica a cada SUBLISTA (la cola completa)
(mapcan #'f lista)          ; como mapcar, y CONCATENA los resultados
(mapc #'f lista)            ; solo por el EFECTO, devuelve la lista original
(map 'vector #'f secuencia) ; sobre cualquier secuencia, con el TIPO del resultado
(reduce #'+ lista)          ; el fold
(remove-if-not #'evenp l)   ; el filter
```

`(map 'vector ...)` merece atención: **el primer argumento dice de qué tipo será el resultado**, así
que la misma función sirve para producir una lista, un vector o una cadena. Es una generalidad que en
otros lenguajes exige convertir después.

Y `mapc` frente a `mapcar` es la distinción que esta clase quiere marcar: **uno es para transformar y
el otro para provocar efectos**. Tenerlos separados y con nombres distintos es una forma de decir en el
código cuál es la intención.

Ahora, la honestidad histórica que esta clase exige: **Lisp nunca fue funcional puro**. Como se dijo
en la clase 108, `setq`, `rplaca` y `nconc` están desde el principio, y el estilo dominante en Common
Lisp es mixto.

Lo que Lisp aportó no fue la pureza, sino **las funciones como valores y la recursión como herramienta
central**, que son los cimientos sobre los que ML, Haskell, Scheme y todos los demás construyeron la
pureza.

Y para inmutabilidad de verdad, la respuesta moderna del ecosistema son las **estructuras persistentes
con compartición estructural** (clase 097): `FSet` en Common Lisp, y sobre todo **Clojure**, un Lisp
que hizo de la inmutabilidad su decisión central y demostró que se puede pagar el coste.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set v [split [string trim $linea]]

#  lmap: el `map` de Tcl (8.6). `v` no se modifica.
set doblados [lmap x $v { expr {$x * 2} }]

puts "doblados=[join $doblados -]"
```

**Lo que esta clase enseña en Tcl.** **`lmap` llegó en Tcl 8.6 (2012)**, veinticuatro años después del
lenguaje, y su historia dice algo sobre cómo evolucionan los lenguajes de guion.

Antes, el idioma era construir la lista a mano:

```tcl
set doblados {}
foreach x $v { lappend doblados [expr {$x * 2}] }
```

Y `lmap` es literalmente eso con otra sintaxis: **acepta las mismas formas que `foreach`**, incluidas
las dos que se mencionaron en la clase 108:

```tcl
lmap x $v { ... }                 ;# uno a uno
lmap {a b} $v { ... }              ;# de DOS en dos
lmap a $l1 b $l2 { ... }            ;# dos listas EN PARALELO
```

Esa última hace en Tcl lo que `(mapcar #'+ l1 l2)` en Lisp y `zip` en Python, y es más general que el
`map` de la mayoría de los lenguajes.

Y aquí está lo importante de esta clase en Tcl: **la inmutabilidad no es una opción, es el modelo**
(clase 102). Todos los valores son inmutables desde el punto de vista del programa, y
`set doblados [lmap ...]` produce una lista nueva sin que `v` pueda verse afectada.

Por debajo hay copia al escribir con conteo de referencias, así que la semántica funcional se obtiene
con el coste de la imperativa **mientras haya una sola referencia**.

Esa última condición es la trampa de rendimiento que ya se explicó y que aquí conviene repetir con su
consecuencia funcional:

```tcl
set b $a          ;# ahora hay DOS referencias
lset b 0 99        ;# aquí se duplica la lista entera
```

**El estilo funcional en Tcl es correcto y puede ser caro**, y el idioma para lo caro es `upvar` con
el nombre de la variable, que es imperativo.

Tcl 8.6 añadió además `apply` para lambdas anónimas (clase 083) y `tcl::mathop` para pasar operadores
como valores (clase 085), con lo que el estilo funcional es escribible:

```tcl
lmap x $v {*}[list apply {{x} {expr {$x * 2}}}]
```

Es viable y nadie lo escribe así: el bloque literal de `lmap` es más claro. Es un buen recordatorio de
que **tener las piezas no hace idiomático el estilo**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

my @doblados = map { $_ * 2 } @v;      # @v no se toca

print "doblados=", join('-', @doblados), "\n";
```

**Lo que esta clase enseña en Perl.** `map`, `grep` y `sort` con bloque están en Perl **desde 1987**,
cuando ningún otro lenguaje mayoritario de uso general los tenía en la sintaxis.

```perl
map  { $_ * 2 } @v          # transformar
grep { $_ > 0 } @v           # filtrar
sort { $a <=> $b } @v         # ordenar con comparador
reverse @v
List::Util: sum, max, min, first, reduce, any, all, none, pairs
```

Y `map` en Perl es más general que en casi todos: **el bloque puede devolver cualquier número de
elementos**, no solo uno.

```perl
map { ($_, $_ * 2) } @v      # DUPLICA la longitud: 1,2  2,4  3,6
map { $_ % 2 ? $_ : () } @v   # devolver () DESCARTA: map hace de filter
```

Ese comportamiento —**`map` es en realidad un *flatMap***— es lo que en Haskell es `concatMap` y en
JavaScript `flatMap`, y en Perl es el comportamiento por defecto desde el principio.

Ahora la advertencia importante de esta clase, y es específica de Perl: **`$_` dentro de `map` y
`grep` es un ALIAS, no una copia**.

```perl
my @v = (1, 2, 3);
my @m = map { $_ *= 2; $_ } @v;     # ¡MODIFICA @v!
print "@v";                          # 2 4 6
```

Modificar `$_` dentro del bloque **cambia la lista original**, exactamente como `@_` en las subrutinas
(clase 079). Es la trampa clásica del estilo funcional en Perl, y la razón de que la forma correcta
sea `map { $_ * 2 }` —sin asignación— y no `map { $_ *= 2 }`.

Es un caso limpio de lo que dice el cierre de esta clase: **el estilo funcional necesita que la
inmutabilidad esté garantizada por algo**, y en Perl no lo está.

Para inmutabilidad real, CPAN ofrece `Readonly`, `const` (Perl 5.28 tiene `use constant` y atributos
`:const`) e `Hash::Util::lock_hash`, que congela una estructura y hace que modificarla sea un error.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};

    std::vector<int> doblados;
    doblados.reserve(v.size());
    std::transform(v.begin(), v.end(), std::back_inserter(doblados),
                   [](int x) { return x * 2; });

    std::cout << "doblados=";
    for (std::size_t i = 0; i < doblados.size(); ++i) {
        if (i != 0) std::cout << '-';
        std::cout << doblados[i];
    }
    std::cout << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::transform` **es el `map` de C++**, y su nombre distinto no
es casual: la STL nombró sus algoritmos con vocabulario matemático y de la tradición de C, no de Lisp.

La declaración `const std::vector<int> v` es la parte importante del programa: **`const` es la única
garantía de inmutabilidad que ofrece C++**, y es una garantía fuerte —modificar `v` no compila— con
una grieta conocida:

```cpp
const int x = 5;
const_cast<int&>(x) = 6;      // compila; comportamiento INDEFINIDO si x era const de verdad
mutable int cache;             // un campo modificable dentro de un método const
```

`const_cast` existe para interoperar con APIs de C mal declaradas, y usarlo para modificar algo
realmente constante es comportamiento indefinido.

Y C++ tiene una segunda forma de "puro" que ya apareció en la clase 107 y que es más fuerte que la de
casi todos: **`constexpr`**.

```cpp
constexpr int doblar(int x) { return x * 2; }
static_assert(doblar(21) == 42);        // se evalúa AL COMPILAR
constexpr std::array<int, 3> v{1, 2, 3};
```

Una función `constexpr` **puede evaluarse en tiempo de compilación**, lo que exige que sea pura en el
sentido práctico: sin entrada/salida, sin estado global mutable, sin memoria dinámica salvo la que se
libere dentro (C++20). Y `consteval` (C++20) **obliga** a que se evalúe al compilar.

No es una declaración de pureza como el `pure` de Fortran —una `constexpr` sí puede modificar sus
locales— y para el propósito de esta clase da la misma propiedad: **el resultado depende solo de los
argumentos**.

C++20 añadió además las *ranges*, que dan el estilo funcional componible que faltaba:

```cpp
auto doblados = v | std::views::transform([](int x) { return x * 2; });
```

**Y es perezoso**: `doblados` no calcula nada hasta que se recorre, y no reserva memoria. Es
evaluación diferida en C++, que es lo que Haskell hace por defecto — con la diferencia de que aquí se
pide explícitamente y su coste es visible.

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

dcl-pi FUNC1;
  entrada char(200) const;
end-pi;

dcl-s texto    varchar(200);
dcl-s tok      varchar(20) inz('');
dcl-s c        char(1);
dcl-s i        int(10);
dcl-s origen   int(10) dim(100);
dcl-s doblados int(20) dim(100);
dcl-s n        int(10) inz(0);
dcl-s salida   varchar(200) inz('');

texto = %trimr(entrada);

for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      n += 1;
      origen(n) = %int(tok);
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

// origen no se modifica: el resultado va a otra tabla
for i = 1 to n;
  doblados(i) = origen(i) * 2;
endfor;

for i = 1 to n;
  if salida <> '';
    salida += '-';
  endif;
  salida += %char(doblados(i));
endfor;

dsply ('doblados=' + salida);

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG no tiene `map`, ni funciones de primera clase idiomáticas, ni
inmutabilidad, y su respuesta es la misma que la de COBOL: **una tabla de origen y otra de destino**.

Lo que sí tiene, y es más de lo que parece, son **operaciones sobre tablas completas** (clase 089):

```rpgle
suma = %sum(%subarr(v : 1 : n));       // reducción
sorta v;                                 // ordenar en el sitio
pos = %lookup(clave : v);                 // buscar
%subarr(destino : 1 : n) = %subarr(origen : 1 : n);   // copiar un tramo
```

`%sum` es un `reduce` integrado, y `%subarr` permite trabajar con rebanadas — las secciones de arreglo
de Fortran, con otra sintaxis.

Y donde RPG sí es funcional sin llamarlo así es en el sitio donde la plataforma pone la potencia:
**SQL**.

```rpgle
exec sql
  select sum(importe), avg(importe), max(importe)
    into :total, :media, :maximo
    from movimientos
   where fecha between :desde and :hasta
   group by cliente;
```

Eso es `map`, `filter`, `reduce` y `group by` en una sentencia declarativa, sin bucles y sin mutación,
ejecutada por un motor que decide el plan. **Es el paradigma funcional-declarativo en el sitio donde
están los datos**, que es la clase 117.

Y sobre inmutabilidad, la plataforma aporta algo que el lenguaje no: **el registro de diario**
(*journaling*).

```text
STRJRNPF FILE(BIBLIO/CLIENTES) JRN(BIBLIO/QSQJRN) IMAGES(*BOTH)
```

Con `IMAGES(*BOTH)`, el sistema **guarda la imagen anterior y la posterior de cada cambio**, en un
diario inmutable y ordenado. Con eso se puede reconstruir el estado en cualquier instante, deshacer
cambios y replicar a otro sistema.

Es **registro de eventos inmutable**, integrado en el sistema operativo desde 1988, y es exactamente
la arquitectura que hoy se llama *event sourcing* — con treinta años de ventaja y sin nombre de moda.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 func1: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare origen(100)   fixed binary(31);
    declare doblados(100) fixed binary(31);
    declare (i, n) fixed binary(31);
    declare salida char(200) varying initial('');

    get edit (linea) (a(200));
    linea = trim(linea);
    n = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             n = n + 1;
             origen(n) = tok;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    /* aritmetica de arreglos: sin bucle, y `origen` no se toca */
    doblados = origen * 2;

    do i = 1 to n;
       if salida ^= '' then salida = salida || '-';
       salida = salida || trim(char(doblados(i)));
    end;

    put skip list ('doblados=' || salida);

 end func1;
```

**Lo que esta clase enseña en PL/I.** `doblados = origen * 2;` **es aritmética de arreglos, y PL/I la
tenía en 1964** — veintiséis años antes que Fortran 90, como se dijo en la clase 089.

```pli
 v = 0;                 /* a todos los elementos */
 w = v * 2 + u;          /* elemento a elemento */
 s = sum(v);              /* reducción */
 put list (v);             /* imprimir el arreglo entero */
 cliente.saldo = 0;         /* un CAMPO de cien registros a la vez */
```

Esa última línea, ya mencionada en la clase 095, es lo que hoy se llama procesamiento columnar, y no
tiene equivalente en ningún lenguaje del núcleo.

Y aquí conviene hacer una precisión importante para no exagerar: **PL/I tenía la notación, no la
garantía**. La aritmética de arreglos de PL/I es azúcar sobre bucles generados por el compilador, y el
lenguaje **no tiene ninguna declaración de pureza** — nada equivalente al `pure` de Fortran 95.

Sin esa garantía, el compilador no puede saber si una función que aparece en una expresión de arreglo
tiene efectos, así que **no puede reordenar ni paralelizar con seguridad**. La notación es cómoda; la
optimización que Fortran obtiene de la suya, PL/I no la obtiene.

Es la diferencia entre **parecer declarativo y serlo**, y esta clase es buen sitio para señalarla,
porque explica por qué Fortran sigue dominando el cálculo numérico y PL/I nunca compitió ahí pese a
tener aritmética de arreglos antes.

Sobre funciones de primera clase, PL/I sí tiene las **variables `entry`** (clase 085), así que un
`map` genérico es escribible:

```pli
 mapear: procedure (v, n, f);
    declare f entry (fixed binary(31)) returns (fixed binary(31)) variable;
    do i = 1 to n;
       v(i) = f(v(i));
    end;
 end mapear;
```

Funciona, y no es idiomático: en 1964 nadie escribía así, y el código PL/I que hay en producción es
imperativo de principio a fin.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
FUNC1 ; Funcional I -- clase 114
 read linea
 kill doblados
 set n = $length(linea, " ")
 ; el array `doblados` es nuevo: `linea` no se modifica
 for i=1:1:n set doblados(i) = $piece(linea, " ", i) * 2
 set salida = ""
 for i=1:1:n do
 . if salida '= "" set salida = salida _ "-"
 . set salida = salida _ doblados(i)
 write "doblados=", salida, !
 quit
```

**Lo que esta clase enseña en M.** M **no tiene nada funcional**: no hay `map`, no hay funciones de
primera clase, no hay clausuras y no hay inmutabilidad. El programa recorre y construye otro array.

Lo que sí tiene, y es lo que esta clase puede aprovechar, es una propiedad que se apuntó en la clase
101 y que aquí encaja del todo: **en M no existen las estructuras compartidas**.

```mumps
 set a = b          ; copia el valor
 merge a = b         ; copia el árbol ENTERO (clase 102)
```

**No hay ninguna forma de que dos nombres designen la misma estructura.** Nunca hay que preguntarse si
una modificación se propagará a otro sitio, que es exactamente la pregunta que el cierre de esta clase
dice que la inmutabilidad elimina.

M la elimina por el otro camino: **no compartiendo nunca**. Es más caro —cada copia es una copia real—
y da la misma tranquilidad.

Y en la capa de datos, M tiene la pieza que hace posible razonar sobre estado compartido: **la
transacción**.

```mumps
 tstart
 set ^SALDO(a) = ^SALDO(a) - importe
 set ^SALDO(b) = ^SALDO(b) + importe
 tcommit
```

Dentro de `tstart`/`tcommit`, **los cambios son invisibles para los demás procesos hasta confirmar**, y
si algo falla se deshacen. Es aislamiento, y resuelve el mismo problema que la inmutabilidad —que
nadie vea un estado a medias— con la herramienta de las bases de datos en lugar de la de los
lenguajes.

Merece cerrar con esa observación, porque recorre toda esta parte del curso: **los lenguajes
funcionales y las bases de datos transaccionales atacan el mismo problema desde lados opuestos**. Uno
dice "no cambies nada"; el otro, "cambia lo que quieras, pero que nadie lo vea hasta que esté".

Clojure, que es un Lisp obsesionado con la inmutabilidad, tiene **memoria transaccional por software**
con `dosync` — y su autor cita explícitamente las bases de datos como inspiración. Los dos mundos
llevan sesenta años convergiendo.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v doblados |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

"collect: es el map. `v` no se modifica: devuelve una colección NUEVA"
doblados := v collect: [ :cada | cada * 2 ].

Transcript
    show: 'doblados=', ((doblados collect: [ :cada | cada printString ])
        inject: '' into: [ :acc :cada |
            acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ]);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** **`collect:` es el `map` de Smalltalk**, y su nombre es
anterior a que "map" se generalizara fuera de Lisp. El vocabulario completo de la jerarquía de
colecciones (clase 089) es este:

```smalltalk
coleccion collect: [ :x | ... ]        "map"
coleccion select: [ :x | ... ]          "filter"
coleccion reject: [ :x | ... ]           "filter negado"
coleccion detect: [ :x | ... ] ifNone: [ ]   "find"
coleccion inject: 0 into: [ :a :b | ]     "reduce / fold"
coleccion do: [ :x | ... ] separatedBy: [ ]
coleccion anySatisfy: / allSatisfy:
```

Y la regla *species* de la clase 090 hace que `collect:` sobre un `Set` devuelva un `Set` y sobre una
`String` devuelva una `String`. Es más cuidadoso que el `map` de la mayoría, que siempre devuelve una
lista.

Ahora bien, hay que decir la verdad sobre la inmutabilidad: **Smalltalk es profundamente mutable**.
Los objetos tienen estado, `at:put:` modifica en el sitio, las cadenas son mutables (clase 093) y no
hay tipos inmutables en el núcleo.

Lo que sí hay, y es de las cosas más peculiares del sistema, es **la inmutabilidad como propiedad de
un objeto individual**, activable en marcha:

```smalltalk
objeto beReadOnlyObject.
objeto isReadOnly.
objeto beWritableObject.
```

**Cualquier objeto se puede congelar**, y a partir de ahí un intento de modificarlo dispara
`ModificationForbidden`, que es una excepción normal y por tanto **manejable**.

Con eso se construyen cosas que en otros lenguajes exigen soporte del compilador: **detectar quién
modifica un objeto** —congelándolo y capturando la excepción para ver la pila— o implementar
**transacciones a nivel de objeto**.

Y esa propiedad viene de lo mismo que todo en este lenguaje: **la inmutabilidad es una bandera en la
cabecera del objeto, comprobada por la máquina virtual**, y como todo en Smalltalk, se puede consultar
y cambiar desde el propio sistema.

---

## Y de vuelta a la clase

Lo transferible: **la inmutabilidad no se pide por pureza moral, se pide porque elimina una pregunta**.
Con datos mutables, ante cualquier valor hay que saber quién más lo tiene y cuándo lo tocó; sin
mutación, esa pregunta desaparece y con ella los errores de concurrencia, los alias sorprendentes
(clase 102) y media clase de fallos difíciles de reproducir. El coste es copiar, y ahí está la salida
que descubrió Lisp y que hoy usan Clojure y Rust: **compartir lo que no cambia** (clase 097).

⏮️ [Volver a la clase 114](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
