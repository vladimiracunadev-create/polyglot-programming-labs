# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 080

> [⬅️ Volver a la clase 080](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Ahora al revés: una función que **modifica la variable del llamante**. Es lo contrario de la clase
anterior y, en la mitad de estos lenguajes, **es lo que pasa si no haces nada**. La pregunta
interesante no es cómo se consigue, sino **dónde se declara**: ¿en la firma, donde lo ve quien
implementa, o en la llamada, donde lo ve quien usa?

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **mutación del argumento**, y estos lenguajes se reparten en dos escuelas.
> **En la firma**: Fortran con `intent(inout)`, Ada con `in out`, Pascal con `var`, C++ con `&`. **En la
> llamada**: COBOL con `BY REFERENCE` y M con el punto delante del argumento.
>
> La segunda escuela es hoy minoritaria y tiene una consecuencia grave: **leyendo el subprograma no se
> sabe si sus parámetros son seguros**, porque depende de cómo lo invoquen. Y leyendo la llamada tampoco
> se sabe si el subprograma va a modificar algo. La información está partida en dos sitios.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `antes=<n> despues=<2n>`
- **Regla:** `la función duplica la variable original vía referencia`

| stdin | esperado |
|---|---|
| `5` | `antes=5 despues=10` |
| `3` | `antes=3 despues=6` |
| `7` | `antes=7 despues=14` |

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
PROGRAM-ID. PORREF.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
01  ANTES   PIC S9(9) COMP-3.
01  ED-A    PIC -(8)9.
01  ED-D    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE N TO ANTES

    PERFORM DOBLAR             *> modifica N: los párrafos comparten TODO

    MOVE ANTES TO ED-A
    MOVE N     TO ED-D
    DISPLAY "antes=" FUNCTION TRIM(ED-A)
            " despues=" FUNCTION TRIM(ED-D)
    STOP RUN.

DOBLAR.
    COMPUTE N = N * 2.
```

**Lo que esta clase enseña en COBOL.** Un párrafo **siempre** trabaja sobre las variables globales, así
que en cierto sentido **todo COBOL es paso por referencia llevado al extremo**: no hay parámetros que
pasar porque no hay nada privado.

Para los subprogramas, COBOL declara el mecanismo **en la llamada**:

```cobol
CALL "SUB" USING BY REFERENCE A     *> el DEFECTO: SUB puede modificar A
```

Y el subprograma recibe las direcciones en su **`LINKAGE SECTION`**, que es una sección de datos
especial: **declara la forma de algo que vive en otro programa**.

```cobol
DATA DIVISION.
LINKAGE SECTION.
01  PARAM-A  PIC S9(9) COMP-3.

PROCEDURE DIVISION USING PARAM-A.
    COMPUTE PARAM-A = PARAM-A * 2.     *> escribe en la memoria del LLAMANTE
```

La `LINKAGE SECTION` **no reserva memoria**: describe la forma de un dato ajeno. Si el llamante pasa
un campo con otra `PIC`, el subprograma lo interpreta con la suya y el resultado es basura, **sin
ningún error**. No hay comprobación de tipos entre programas compilados por separado.

Ese es uno de los fallos más difíciles de diagnosticar del mundo COBOL, y la razón de que los
copybooks de la clase 052 sean tan importantes: **compartir la definición es la única garantía de que
los dos lados coincidan**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program porref
   implicit none
   integer :: n, antes

   read(*, *) n
   antes = n

   call doblar(n)          ! por referencia: modifica n

   write(*, '(A,I0,A,I0)') 'antes=', antes, ' despues=', n

contains

   pure subroutine doblar(x)
      integer, intent(inout) :: x     ! ENTRADA Y SALIDA, declarado
      x = x * 2
   end subroutine doblar

end program porref
```

**Lo que esta clase enseña en Fortran.** El paso por referencia es **el defecto**, así que `intent`
no cambia el mecanismo: **cambia lo que está permitido hacer**.

| `intent` | Se puede leer | Se puede escribir | El compilador… |
|---|---|---|---|
| `in` | Sí | **No** | Rechaza la escritura |
| `out` | **No** (el valor entrante no cuenta) | Sí | Avisa si se lee antes de asignar |
| `inout` | Sí | Sí | |

Es documentación **comprobada**, y es lo único que hace legible una interfaz en un lenguaje donde
todo se pasa por dirección.

Y hay una regla de Fortran que no tiene ningún lenguaje del núcleo y que es la razón de su
rendimiento: **está prohibido que dos argumentos de una subrutina se solapen en memoria**.

```fortran
call procesar(v, v)        ! ILEGAL si procesar modifica alguno
call procesar(v(1:50), v(40:90))   ! ILEGAL: se solapan
```

El estándar lo prohíbe y **el compilador puede asumir que no ocurre**, lo que le permite reordenar y
vectorizar libremente. En C, dos punteros pueden apuntar a lo mismo y el compilador debe suponer lo
peor — de ahí que C99 tuviera que inventar `restrict` para recuperar a mano lo que Fortran tiene de
serie.

Es exactamente lo que la ficha de la clase 043 anunciaba, aquí en su forma concreta: **la ausencia de
solapamiento es una obligación del programador y una licencia para el optimizador**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Porref is

   procedure Doblar (X : in out Integer) is
   begin
      X := X * 2;
   end Doblar;

   N, Antes : Integer;
begin
   Get (N);
   Antes := N;

   Doblar (N);

   Put ("antes=");     Put (Antes, Width => 1);
   Put (" despues=");  Put (N, Width => 1);
   New_Line;
end Porref;
```

**Lo que esta clase enseña en Ada.** `in out` declara la intención, y el compilador sigue eligiendo el
mecanismo — copia de entrada y salida, o dirección — como se vio en la clase 079.

Eso tiene una consecuencia que conviene conocer y que Ada documenta explícitamente: **si el mismo
objeto se pasa dos veces, el resultado no está definido**.

```ada
Intercambiar (A, A);        --  el estándar NO dice qué pasa
```

Con paso por dirección, las dos referencias son la misma. Con copia de entrada y salida, la segunda
copia de vuelta pisa a la primera. Como el estándar no fija el mecanismo, no puede fijar el
resultado. Es el mismo problema del solapamiento de Fortran, expresado a nivel de parámetros.

Y **`out` en Ada no es lo mismo que en Pascal o C#**: en Ada, un parámetro `out` de un tipo escalar
**entra sin valor definido**, y leerlo antes de asignarlo es un error que el compilador detecta. Para
tipos compuestos con partes discriminantes, sí conserva parte de la información — un matiz que está en
el manual de referencia y que casi nadie conoce.

Ada 2012 permite además `in out` en **funciones**, cosa prohibida hasta entonces. Fue una concesión
discutida: la restricción original empujaba hacia funciones puras, y levantarla facilitó la
interoperabilidad a cambio de perder esa garantía.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program PorRef;
{$MODE OBJFPC}{$H+}
uses SysUtils;

procedure Doblar(var X: Integer);      { VAR: por referencia }
begin
  X := X * 2;
end;

var
  N, Antes: Integer;

begin
  Read(N);
  Antes := N;

  Doblar(N);

  WriteLn('antes=', IntToStr(Antes), ' despues=', IntToStr(N));
end.
```

**Lo que esta clase enseña en Pascal.** **`var` es la palabra que inventó el paso por referencia
declarado en la firma**, y de ahí la copiaron C# (`ref`), Object Pascal, Modula-2 y Ada (con otro
nombre).

Antes de Pascal, la elección estaba en la llamada —COBOL— o no había elección —FORTRAN—. ALGOL 60
tenía el paso por **nombre**, que era aún más raro: el argumento se reevaluaba en cada uso, lo que
producía el célebre *dispositivo de Jensen* y una cantidad notable de confusión.

Wirth simplificó a dos modos, y ese par —por valor o `var`— es el que ha sobrevivido.

Object Pascal añadió después `const` y `out`, con lo que quedan cuatro:

```pascal
procedure P(A: Integer);          { valor }
procedure P(var A: Integer);      { referencia, lectura y escritura }
procedure P(const A: TGrande);    { referencia, solo lectura }
procedure P(out A: Integer);      { referencia, solo escritura }
```

Y hay una restricción de `var` que conviene conocer: **el argumento debe ser una variable, no una
expresión**, y **su tipo debe coincidir exactamente**. `Doblar(N + 0)` no compila, y `Doblar(B)` con
`B: Byte` tampoco, aunque `Byte` quepa en `Integer`.

Esa rigidez es deliberada: si el compilador aceptara una conversión, tendría que crear un temporal, y
entonces la modificación se perdería — el *dummy argument* de PL/I y Fortran. Pascal lo prohíbe en
lugar de permitirlo en silencio.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun doblar (celda)
  (setf (car celda) (* 2 (car celda))))   ; muta el OBJETO, no la variable

(let* ((n (read))
       (caja (list n)))                   ; una "caja": lista de un elemento
  (doblar caja)
  (format t "antes=~D despues=~D~%" n (car caja)))
```

**Lo que esta clase enseña en Common Lisp.** **Lisp no tiene paso por referencia**, y este programa
muestra el sustituto universal: **envolver el valor en un objeto mutable**.

`(list n)` crea una caja de un elemento. La función recibe la caja —por valor, como siempre— y muta su
contenido con `(setf (car celda) ...)`. El llamante ve el cambio porque **ambos apuntan al mismo
objeto**.

Es exactamente lo que se hace en Java con un array de un elemento, en Python con una lista, en Go con
un puntero y en JavaScript con un objeto. **Cuando un lenguaje no tiene referencias, la caja es el
patrón.**

Y `setf` merece un apunte, porque es una de las mejores ideas de Common Lisp: **funciona sobre
cualquier "lugar"**, no solo sobre variables.

```lisp
(setf x 1)                       ; una variable
(setf (car lista) 1)             ; el primer elemento
(setf (aref v 3) 1)              ; un elemento de array
(setf (gethash k tabla) 1)       ; una entrada de tabla hash
(setf (slot-value obj 'campo) 1) ; un campo de objeto
(setf (symbol-function 'f) g)    ; ¡la definición de una función!
```

Todos son "lugares" que se pueden leer y escribir, y `setf` es la macro que sabe cómo escribir en cada
uno. Se pueden definir lugares nuevos con `defsetf` y `define-setf-expander`, así que **una estructura
propia puede participar en `setf`** como si fuera nativa.

Es generalización llevada al límite: en vez de un operador de asignación, un protocolo de asignación
extensible.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc doblar {nombreVar} {
    upvar 1 $nombreVar x        ;# liga x a la variable del LLAMANTE
    set x [expr {$x * 2}]
}

gets stdin linea
set n [string trim $linea]
set antes $n

doblar n                        ;# se pasa el NOMBRE, no el valor

puts "antes=$antes despues=$n"
```

**Lo que esta clase enseña en Tcl.** Fíjate en la llamada: **`doblar n`, sin el `$`**. No se pasa el
valor: se pasa **el nombre de la variable**, como una cadena.

`upvar 1 $nombreVar x` liga la variable local `x` a la variable llamada así en el nivel de pila
indicado —`1` es el llamante, `2` el llamante del llamante, `#0` el nivel global—. A partir de ahí,
`x` **es** la variable del otro.

Es paso por referencia obtenido **sin punteros y sin referencias**: en Tcl las variables se resuelven
por nombre en tiempo de ejecución, así que basta con pasar el nombre.

Y ese mecanismo es la base de toda la extensibilidad del lenguaje. Los comandos del propio Tcl que
dejan resultados en variables —`scan`, `regexp`, `binary scan`, `lassign`, `catch`— están
implementados así, y por eso un procedimiento de usuario puede imitarlos exactamente.

Su hermano es **`uplevel`**, que ya apareció en la clase 041: **evalúa código en el ámbito del
llamante**. Con `upvar` y `uplevel` juntos se pueden escribir estructuras de control propias que se
comportan como las nativas:

```tcl
proc repetir {n cuerpo} {
    for {set i 1} {$i <= $n} {incr i} { uplevel 1 $cuerpo }
}
```

La contrapartida es la de siempre: **el nombre viaja como una cadena, así que nadie comprueba nada**.
Un error de escritura en el nombre crea una variable nueva en el ámbito del llamante.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub doblar {
    $_[0] *= 2;              # @_ contiene ALIAS: esto modifica al llamante
}

my $n = <STDIN>;
chomp $n;
my $antes = $n;

doblar($n);

print "antes=$antes despues=$n\n";
```

**Lo que esta clase enseña en Perl.** Esta es la cara oculta de la clase 079: **`@_` contiene alias de
los argumentos originales**, así que modificar `$_[0]` **modifica la variable del llamante**.

Perl es, por tanto, **por referencia por defecto**, y la copia es opt-in con `my ($x) = @_;`.

Ese comportamiento tiene usos legítimos y muy usados en el propio núcleo:

```perl
chomp($linea);      # modifica $linea en el sitio
chop($s);
s/a/b/ for @lista;  # modifica CADA elemento de @lista
```

Y `for` y `map` tienen el mismo aliasing, como se vio en las clases 064 y 067.

La forma **explícita** de pasar por referencia, y la que se usa cuando la intención debe verse, son
las referencias:

```perl
doblar(\$n);                    # se pasa una REFERENCIA
sub doblar { my ($ref) = @_; $$ref *= 2 }
```

`\$n` crea la referencia y `$$ref` la desreferencia. Es más verboso y **se ve en el sitio de la
llamada**, que es exactamente la ventaja: quien lee `doblar(\$n)` sabe que `$n` puede cambiar, y quien
lee `doblar($n)` supone que no — aunque técnicamente pueda.

Con **firmas** (5.36) el aliasing desaparece: los parámetros de una firma son copias, así que la única
forma de modificar al llamante pasa a ser la referencia explícita. Es una mejora de legibilidad
importante.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

void doblar(int& x) {      // REFERENCIA: modifica la variable del llamante
    x *= 2;
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    const int antes = n;
    doblar(n);

    std::cout << "antes=" << antes << " despues=" << n << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `int&` es una **referencia**, y su diferencia con el puntero de C
es la que da la lección:

| | Puntero `int*` | Referencia `int&` |
|---|---|---|
| Puede ser nulo | Sí | **No** |
| Se puede reasignar | Sí | **No**: se liga una vez |
| Sintaxis en el uso | `*p = 1` | `x = 1` |
| Sintaxis en la llamada | `f(&n)` | `f(n)` |

La última fila es la discutida: **en el sitio de la llamada, `doblar(n)` no revela que `n` puede
cambiar**. En C había que escribir `doblar(&n)`, y esa marca era información. C++ la perdió a cambio
de sintaxis limpia.

Por eso las *Core Guidelines* recomiendan: **si una función modifica un argumento, pásalo por puntero
o devuélvelo**, precisamente para que se vea en la llamada. Google llegó a prohibir las referencias no
constantes en su guía de estilo por este motivo, y años después relajó la norma.

Es el mismo debate de COBOL y M —¿la marca va en la firma o en la llamada?— con la respuesta de que lo
ideal sería en las dos.

Y C++11 añadió un tercer tipo de referencia, `int&&`, que es la clase siguiente: no significa
"modificable", significa **"consumible"**.

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

dcl-pi PORREF;
  n int(10);          // SIN const ni value: por referencia (el defecto)
end-pi;

dcl-s antes  int(10);
dcl-s salida char(50);

antes = n;
doblar(n);            // modifica n

salida = 'antes=' + %char(antes) + ' despues=' + %char(n);
dsply salida;

*inlr = *on;
return;

dcl-proc doblar;
  dcl-pi *n;
    x int(10);        // por referencia
  end-pi;
  x = x * 2;
end-proc;
```

**Lo que esta clase enseña en RPG.** El paso por referencia es **el defecto**, y basta con **no
escribir nada**: un parámetro sin `const` ni `value` es modificable y el cambio se ve fuera.

Ese defecto es el origen de un problema real de mantenimiento en RPG: **un subprocedimiento que
modifica un parámetro por error corrompe datos del llamante sin ninguna señal**, igual que en COBOL y
Fortran antes de `intent`.

Por eso la guía de estilo de la plataforma es tajante: **`const` en todo lo que sea de entrada**,
siempre, aunque sea más largo de escribir.

RPG tiene además dos cosas relacionadas que conviene conocer. La primera, **`options(*varsize)`**, que
permite pasar un campo más corto que el declarado:

```rpgle
dcl-pi *n;
  texto char(1000) options(*varsize);
  largo int(10) const;                  // y el llamante dice cuánto mide de verdad
end-pi;
```

Sin `*varsize`, RPG exige que el argumento mida exactamente lo declarado. Con él, se pasa la dirección
y el tamaño real viaja aparte — el mismo `char* + size_t` de C, con los mismos riesgos.

La segunda: **`%addr()`**, que da la dirección de una variable, y las variables `based(puntero)` de la
clase 078. Con ellas se puede hacer aritmética de punteros en RPG, y se usa para las APIs del sistema.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 porref: procedure options(main);

    declare (n, antes) fixed binary(31);

    get list (n);
    antes = n;

    call doblar(n);        /* por REFERENCIA: es el defecto */

    put skip list ('antes=' || trim(char(antes)) ||
                   ' despues=' || trim(char(n)));

 doblar: procedure (x);
    declare x fixed binary(31);
    x = x * 2;
 end doblar;

 end porref;
```

**Lo que esta clase enseña en PL/I.** El paso por referencia es el defecto y **no hay forma de
declararlo en la firma**: cualquier parámetro es modificable, y lo único que fuerza la copia son los
paréntesis extra en el sitio de la llamada, como se vio en la clase 079.

Esa ausencia —no poder decir "este parámetro es de entrada"— es una de las carencias más claras de
PL/I frente a Fortran 90 y Ada, y se nota en el mantenimiento: **para saber qué modifica un
procedimiento hay que leer su cuerpo entero**.

Lo que PL/I sí tiene, y es donde el paso por referencia se vuelve realmente potente, es la
combinación con las **variables `based`** de la clase 053:

```pli
declare p pointer;
declare v(1000) fixed binary(31) based(p);

p = addr(datos);          /* apunta a otra cosa */
v(5) = 99;                /* escribe en datos, con OTRA forma */
```

`based` permite **reinterpretar cualquier zona de memoria con la forma que quieras**, y `addr` da la
dirección de cualquier variable. Con eso se escribió Multics, y con eso se puede corromper cualquier
cosa.

Es coherente con el resto del lenguaje: PL/I da las herramientas de un lenguaje de sistemas y las
comodidades de uno de aplicación, sin separar las dos cosas. Fue una decisión valiente para 1964 y es
la razón de que hoy se cite como ejemplo de lo que no hay que hacer.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PORREF ; Paso por referencia -- clase 080
 read n
 set antes = n
 do doblar(.n)                 ; el PUNTO: por referencia
 write "antes=", antes, " despues=", n, !
 quit
 ;
doblar(x) ; dobla x en el sitio
 set x = x * 2
 quit
```

**Lo que esta clase enseña en M.** **El punto delante del argumento —`.n`— es todo el mecanismo.** Sin
él, por valor; con él, por referencia. La decisión está **en el sitio de la llamada**, como en COBOL.

Y lo que hace único a M es **qué** se puede pasar así: no una variable, sino **un árbol local
completo**.

```mumps
 kill pacientes
 do CARGAR^DATOS(.pacientes)
 ;
CARGAR(res) ;
 set res(1,"nombre") = "Ada"
 set res(1,"edad") = 36
 set res(2,"nombre") = "Grace"
 quit
```

La rutina llamada **crea la estructura entera** en el array del llamante: subíndices, niveles y todo.
Al volver, `pacientes(1,"nombre")` existe.

Eso convierte el paso por referencia en el mecanismo de retorno de estructuras del lenguaje, y explica
la forma de todas las APIs de VistA: **no devuelven objetos, rellenan arrays**.

Hay un detalle que conviene conocer y que causa errores: **el punto solo se puede poner sobre un
nombre de variable simple**, no sobre un subíndice ni una expresión. `do P(.a(1))` no es legal. Para
pasar un subárbol hay que copiarlo primero con `merge`:

```mumps
 merge temporal = pacientes(1)      ; MERGE copia un subárbol completo
 do P(.temporal)
```

`merge` es otro comando propio de M sin equivalente directo: copia un nodo **y todos sus
descendientes** de una estructura a otra, local o global, en una sola operación.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n caja |

n := stdin nextLine trimBoth asNumber.
caja := OrderedCollection with: n.        "una 'caja' mutable"

caja at: 1 put: (caja first * 2).

Transcript
    show: 'antes=', n printString;
    show: ' despues=', caja first printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene paso por referencia**, y no puede
tenerlo: los parámetros son constantes (clase 079) y los números son inmutables.

El sustituto es el mismo que en Lisp: **una caja**, un objeto mutable que contiene el valor. Aquí una
`OrderedCollection`; en código real sería una instancia de `ValueHolder`, una clase de la biblioteca
pensada exactamente para esto.

```smalltalk
| holder |
holder := ValueHolder new.
holder value: 5.
modificar: holder.          "el método puede hacer holder value: 10"
holder value.                "10"
```

`ValueHolder` es más que un truco: es la pieza central del patrón **Observador** en Smalltalk. Un
`ValueHolder` puede **notificar a quien esté escuchando** cuando su contenido cambia, y sobre eso se
construyó toda la capa de enlace de datos de VisualWorks — el antepasado del *data binding* que hoy
tienen Angular, Vue y SwiftUI.

Es un buen cierre para esta clase: **la carencia de paso por referencia empujó a Smalltalk a
convertir "un valor que cambia" en un objeto de primera clase**, y de ahí salió una idea que la
industria adoptó cuarenta años después con otro nombre.

Y en la práctica, la pregunta rara vez se plantea: como los objetos son referencias, un método que
recibe una colección o un modelo **ya puede modificarlo**. La caja solo hace falta para los
inmutables.

---

## Y de vuelta a la clase

Lo transferible: **si el lenguaje permite mutar argumentos, la firma debe decirlo**. Es la misma
regla que la clase 073 sobre los modos, y la razón de que Fortran y Ada insistan tanto en `intent` y
en `in out`. Y en los lenguajes sin paso por referencia —Lisp, Smalltalk, Java, Python— el sustituto
es siempre el mismo: **envolver el valor en un objeto mutable**, que es exactamente lo que hace este
programa en Lisp con una lista de un elemento.

⏮️ [Volver a la clase 080](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
