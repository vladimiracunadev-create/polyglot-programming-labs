# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 084

> [⬅️ Volver a la clase 084](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Elevar un número al cuadrado. La función más inocente posible, y la excusa para la pregunta que
define la programación funcional: **¿esta función hace algo más que devolver un valor?** Si no toca
nada de fuera, se puede memorizar, reordenar, paralelizar y probar sin montar nada. Y **Fortran es el
único lenguaje de esta página donde el compilador lo COMPRUEBA**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **pureza**, y estos lenguajes lo enseñan porque uno de ellos la convirtió en
> palabra clave por un motivo puramente práctico. **`pure` en Fortran 95 no se añadió por elegancia
> funcional: se añadió para poder paralelizar.** Una función pura se puede llamar desde un `forall` o un
> `do concurrent` sin riesgo, y el compilador **rechaza** el código que la viole.
>
> Ada llegó al mismo sitio desde otro lado, con `Global => null` y SPARK, por la certificación. Y en el
> extremo opuesto, COBOL y M no tienen ningún concepto de pureza porque **todas sus variables son
> globales**: la pregunta no se puede ni formular.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `puro=<n²>`
- **Regla:** `cuadrado(n) = n * n (sin efectos)`

| stdin | esperado |
|---|---|
| `4` | `puro=16` |
| `-3` | `puro=9` |
| `0` | `puro=0` |

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
PROGRAM-ID. PURA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    COMPUTE R = N * N

    MOVE R TO ED-R
    DISPLAY "puro=" FUNCTION TRIM(ED-R)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **En COBOL la pureza no se puede ni expresar.** Un párrafo no
tiene parámetros ni retorno (clase 073) y todas las variables son globales (clase 082), así que
**cualquier párrafo puede modificar cualquier cosa**. No hay nada que declarar ni que comprobar.

Eso no significa que el concepto sea inútil ahí: significa que es **disciplina**. Las guías de estilo
de COBOL llevan décadas recomendando párrafos que "solo calculen", con una convención de nombres que
lo indique, y que los efectos —E/S, actualización de ficheros— estén concentrados en párrafos
separados. Es exactamente la separación entre núcleo puro y cáscara con efectos que hoy se predica en
arquitectura hexagonal.

Donde COBOL sí se acerca es en las **funciones definidas por el usuario** de COBOL 2002:

```cobol
IDENTIFICATION DIVISION.
FUNCTION-ID. CUADRADO.
DATA DIVISION.
LINKAGE SECTION.
01  X  PIC S9(9) COMP-3.
01  R  PIC S9(18) COMP-3.
PROCEDURE DIVISION USING X RETURNING R.
    COMPUTE R = X * X.
END FUNCTION CUADRADO.
```

Una `FUNCTION-ID` **tiene parámetros y valor de retorno**, y se puede usar dentro de una expresión:
`COMPUTE TOTAL = FUNCTION CUADRADO(A) + FUNCTION CUADRADO(B)`. Es lo más cerca que llega COBOL a una
función en el sentido matemático.

Sigue sin haber garantía de pureza —la función puede tener su propio `WORKING-STORAGE` estático y
acordarse de llamadas anteriores— pero al menos el flujo de datos entra y sale por la firma.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program pura
   implicit none
   integer :: n

   read(*, *) n
   write(*, '(A,I0)') 'puro=', cuadrado(n)

contains

   pure function cuadrado(x) result(r)
      integer, intent(in) :: x
      integer :: r
      r = x * x
   end function cuadrado

end program pura
```

**Lo que esta clase enseña en Fortran.** **`pure` es la única palabra clave de pureza COMPROBADA por el
compilador en toda esta página**, y Fortran la tiene desde **Fortran 95**.

Dentro de una función `pure` está **prohibido**:

- modificar cualquier argumento (todos deben ser `intent(in)` o `value`);
- modificar variables del anfitrión, de un módulo o `save`;
- ejecutar cualquier operación de **entrada/salida**;
- llamar a un procedimiento que no sea `pure`;
- ejecutar `stop`.

El compilador **rechaza** el código que lo viole. No es documentación: es un contrato.

Y no se añadió por convicción funcional. Se añadió porque **`forall` y `do concurrent` necesitan
garantizar que las iteraciones son independientes**:

```fortran
do concurrent (i = 1:n)
   v(i) = cuadrado(v(i))      ! solo es seguro si cuadrado es PURE
end do
```

Sin la garantía, el compilador no puede vectorizar ni mandar el bucle a la GPU. **La pureza es la
condición que habilita el paralelismo**, y por eso está en un lenguaje de cálculo numérico y no en uno
funcional.

Y `elemental` va un paso más allá: implica `pure` y hace que la función se aplique **elemento a
elemento sobre arrays de cualquier rango**:

```fortran
elemental function cuadrado(x) result(r)
...
w = cuadrado(v)        ! sobre un array entero, sin bucle
m = cuadrado(matriz)   ! y sobre una matriz
```

Existe además `impure elemental`, para el caso raro en que se quiere la aplicación elemento a elemento
pero con efectos. Que haya que escribir `impure` explícitamente dice mucho de las prioridades.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Pura is

   --  El contrato dice qué garantiza la función, y SPARK lo demuestra.
   function Cuadrado (X : Integer) return Integer
     with Post => Cuadrado'Result >= 0;

   function Cuadrado (X : Integer) return Integer is
   begin
      return X * X;
   end Cuadrado;

   N : Integer;
begin
   Get (N);

   Put ("puro=");
   Put (Cuadrado (N), Width => 1);
   New_Line;
end Pura;
```

**Lo que esta clase enseña en Ada.** Ada llegó a la pureza desde la **certificación**, no desde el
paralelismo, y su vocabulario lo refleja.

Hasta Ada 2005, una **función no podía tener parámetros `out`**, lo que la empujaba hacia la pureza
sin nombrarla. Y desde Ada 2012 hay contratos que la declaran explícitamente:

```ada
function Cuadrado (X : Integer) return Integer
  with Global => null,           --  NO accede a ninguna variable global
       Pre    => X in -46340 .. 46340,   --  no desborda
       Post   => Cuadrado'Result = X * X;
```

`Global => null` es la declaración de pureza, y **SPARK la demuestra estáticamente**: no comprueba en
ejecución, **prueba** que la función no toca nada de fuera. Si accede a una global sin declararla, el
analizador lo rechaza.

Y `Pre`/`Post` van más lejos que la pureza: describen **qué exige y qué garantiza**. Con SPARK, la
precondición se demuestra en cada sitio de llamada, y si se demuestra, la comprobación en ejecución se
elimina.

Ada tiene además el `pragma Pure` a nivel de **paquete completo**, que declara que un paquete no tiene
estado y permite al compilador compartir su código entre particiones distribuidas.

La comparación con Fortran es instructiva: **los dos llegaron a la misma característica por motivos
opuestos** —uno para paralelizar, otro para certificar— y la implementaron casi igual. Es una señal
bastante clara de que la pureza es una propiedad útil con independencia del paradigma.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Pura;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function Cuadrado(X: Integer): Int64;
begin
  Result := Int64(X) * X;
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('puro=', IntToStr(Cuadrado(N)));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal **no tiene ninguna forma de declarar pureza**, y la
distinción `function` / `procedure` es lo más cerca que llega: por convención, una **función devuelve
un valor y no debería tener efectos**; un **procedimiento** hace algo.

Wirth lo consideraba una regla de estilo, no del lenguaje. Y el propio Pascal la incumple: nada impide
que una función modifique una global o escriba en un fichero.

Ese es un caso claro de lo que esta clase quiere mostrar: **una convención sin comprobación es una
convención que se rompe**. El código Pascal real está lleno de funciones con efectos, y la única forma
de saberlo es leerlas.

Free Pascal y Delphi añadieron `const` en los parámetros (clase 079), que impide modificar el
argumento — la mitad del problema. Lo que falta es impedir el acceso a globales.

Fíjate también en `Int64(X) * X` de este programa: la conversión **antes** de multiplicar. Sin ella, la
multiplicación se haría en `Integer` de 32 bits y desbordaría con valores grandes antes de promocionar
al `Int64` del resultado. Es un error clásico que ninguna anotación de pureza evita, y que aparece en
todos los lenguajes con tipos enteros de ancho fijo:

```pascal
Result := X * X;          { desborda en Integer y LUEGO promociona }
Result := Int64(X) * X;   { correcto: la multiplicación ya es de 64 bits }
```

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun cuadrado (x)
  (* x x))

(let ((n (read)))
  (format t "puro=~D~%" (cuadrado n)))
```

**Lo que esta clase enseña en Common Lisp.** Common Lisp **no es un lenguaje puro** y no tiene forma
estándar de declarar pureza — es multiparadigma y `setf` está por todas partes.

Lo que sí tiene son **declaraciones de optimización que dependen de la pureza**, y SBCL las aprovecha:

```lisp
(declaim (ftype (function (fixnum) fixnum) cuadrado))
(defun cuadrado (x)
  (declare (optimize (speed 3)) (type fixnum x))
  (the fixnum (* x x)))
```

Y hay una construcción que **explota la pureza directamente**: las **funciones incorporadas marcadas
como "flushable" y "foldable"** en el compilador. Si SBCL sabe que una función es pura y su resultado
no se usa, **elimina la llamada entera**; si sus argumentos son constantes, la **evalúa al compilar**.

```lisp
(defun f () (sqrt 2.0))     ; SBCL calcula la raíz AL COMPILAR
```

Eso es exactamente `constexpr` de C++, deducido en lugar de declarado.

Y la comunidad Lisp aporta a esta clase el concepto que da nombre a todo esto: **la transparencia
referencial**. Una expresión es transparente si se puede sustituir por su valor sin cambiar el
programa. Con `(cuadrado 4)` se puede; con `(read)` no.

Ese es el criterio operativo de la pureza, y es más útil que la definición formal: **¿puedo sustituir
la llamada por su resultado?** Si sí, es pura, y entonces se puede memorizar —la técnica de la clase
069— reordenar y paralelizar.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc cuadrado {x} {
    return [expr {$x * $x}]
}

gets stdin linea
set n [string trim $linea]

puts "puro=[cuadrado $n]"
```

**Lo que esta clase enseña en Tcl.** Tcl **no tiene ninguna noción de pureza**, y no puede tenerla
fácilmente: cualquier procedimiento puede usar `global`, `upvar` o `uplevel` para tocar el entorno de
quien lo llama (clases 080 y 082).

De hecho, `uplevel` hace que **ni siquiera se pueda saber estáticamente qué toca un procedimiento**,
porque el código que evalúa puede venir de una cadena construida en ejecución.

Lo que Tcl sí ofrece, y encaja en esta clase, es una forma muy directa de aprovechar la pureza cuando
existe: **la memorización con un array**.

```tcl
proc cuadrado {x} {
    global memo
    if {[info exists memo($x)]} { return $memo($x) }
    set memo($x) [expr {$x * $x}]
    return $memo($x)
}
```

Ese patrón —comprobar la caché, calcular, guardar— es la aplicación práctica de la pureza, y solo es
correcto **si la función es pura**. Si dependiera de algo externo que cambia, la caché devolvería
resultados obsoletos.

Es exactamente la memorización de la ficha de Lisp de la clase 069, y la razón de que esta clase
importe aunque el lenguaje no la comprueba: **la pureza es lo que hace que una optimización sea
correcta**.

Y hay una ironía útil: los **valores de Tcl son inmutables** (clase 081), así que en la práctica una
gran parte del código Tcl es más puro de lo que parece — lo que se modifica son variables, no valores
compartidos.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub cuadrado {
    my ($x) = @_;
    return $x * $x;
}

my $n = <STDIN>;
chomp $n;

print "puro=", cuadrado($n), "\n";
```

**Lo que esta clase enseña en Perl.** Perl no tiene declaración de pureza, y **su modelo de `@_` la
dificulta especialmente**: como los argumentos son alias (clase 080), una subrutina puede modificar
las variables del llamante sin que nada lo indique.

Por eso `my ($x) = @_;` no es solo comodidad: **es lo que hace pura a la función**. Sin esa línea,
cualquier escritura en `$_[0]` sería un efecto secundario invisible.

Lo que Perl sí tiene es una **memorización de una sola línea**, gracias a `Memoize`, un módulo del
núcleo:

```perl
use Memoize;
memoize('cuadrado');       # a partir de aquí, cachea los resultados
```

`memoize` **reemplaza la subrutina por una envoltura con caché** en tiempo de ejecución, sin tocar su
código. Es posible porque en Perl la tabla de símbolos es modificable —`*cuadrado = sub {...}`— y es
el mismo mecanismo que `rename` en Tcl (clase 073).

Y funciona **solo si la función es pura**. La documentación de `Memoize` lo dice explícitamente y
enumera los casos en que no debe usarse: funciones con efectos, que dependan del tiempo, del estado
global o del contexto.

Perl 5.36 añadió además los **atributos de subrutina** `:const` y `:lvalue`, y el pragma `builtin`
con funciones que el compilador sabe puras. Son pasos pequeños hacia lo que Fortran tiene desde 1995.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

//  constexpr: se puede evaluar en tiempo de COMPILACIÓN si los argumentos
//  se conocen. Implica restricciones muy parecidas a la pureza.
constexpr long long cuadrado(int x) {
    return static_cast<long long>(x) * x;
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    static_assert(cuadrado(4) == 16);      // comprobado AL COMPILAR

    std::cout << "puro=" << cuadrado(n) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** **`constexpr` es la pureza de C++**, aunque no se llame así. Una
función `constexpr` **no puede** tener efectos observables: no puede modificar globales, no puede
hacer E/S, y **si sus argumentos se conocen al compilar, se evalúa entonces**.

El `static_assert` de este programa lo demuestra: `cuadrado(4)` se calcula **durante la compilación** y
el resultado se comprueba ahí mismo. Si fuera 15, el programa no compilaría.

Y la misma función sirve para las dos cosas: con `n` leído de la entrada, se ejecuta normalmente. Es
una propiedad muy práctica — no hay que escribir dos versiones.

C++ ha ido acumulando calificadores en esta línea, y conviene distinguirlos:

| | Qué promete |
|---|---|
| `constexpr` | **Puede** evaluarse al compilar |
| `consteval` (C++20) | **Debe** evaluarse al compilar; si no, error |
| `constinit` (C++20) | Se inicializa en compilación, pero no es constante |
| `noexcept` | No lanza |
| `[[nodiscard]]` | Avisa si se ignora el resultado — típico de funciones puras |
| `const` (método) | No modifica el objeto |

Lo que C++ **no** tiene es una declaración de "esta función no toca ninguna global" para el caso
general en ejecución. GCC y Clang ofrecen los atributos `__attribute__((pure))` y `((const))`, que
habilitan optimizaciones fuertes —eliminar llamadas repetidas— pero **no los comprueban**: si mientes,
el resultado es comportamiento indefinido.

Ahí está la diferencia con Fortran: **una promesa comprobada frente a una promesa creída**.

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

dcl-pi PURA;
  n int(10) const;
end-pi;

dcl-s salida char(40);

salida = 'puro=' + %char(cuadrado(n));
dsply salida;

*inlr = *on;
return;

dcl-proc cuadrado;
  dcl-pi *n int(20);
    x int(10) const;      // const: no modifica el argumento
  end-pi;
  return x * x;           // y no toca ninguna global
end-proc;
```

**Lo que esta clase enseña en RPG.** RPG **no tiene declaración de pureza**, y su equivalente práctico
es una combinación de dos cosas que sí se declaran:

1. **`const` en todos los parámetros** — garantiza que no se modifican (clase 079).
2. **Ninguna variable global del módulo** — que no se puede declarar, solo respetar.

La segunda es la que falta, y es exactamente el problema de esta clase: **la mitad de la pureza es
comprobable y la otra mitad es disciplina**.

RPG tiene además una palabra que va en la dirección contraria y que conviene conocer, porque su
presencia delata que un procedimiento **no** es puro:

```rpgle
dcl-proc contador;
  dcl-s n int(10) static;    // STATIC: recuerda entre llamadas
  n += 1;
  return n;
end-proc;
```

`static` en una variable local es la marca de estado entre invocaciones (clase 069). Un procedimiento
con `static` **nunca es puro**, y buscar esa palabra es la forma práctica de auditar un módulo.

Y hay una razón por la que esto importa mucho en IBM i: los procedimientos de un **módulo de servicio**
se comparten entre trabajos, y un `static` mal usado puede filtrar datos de un usuario a otro. Es un
problema de seguridad, no solo de corrección, y la guía de la plataforma insiste en que el estado
compartido se declare y se justifique.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 pura: procedure options(main);

    declare n fixed binary(31);

    get list (n);
    put skip list ('puro=' || trim(char(cuadrado(n))));

 cuadrado: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    return (x * x);
 end cuadrado;

 end pura;
```

**Lo que esta clase enseña en PL/I.** PL/I **no tiene ninguna noción de pureza**, y su modelo la hace
especialmente difícil de garantizar: el paso por referencia por defecto (clase 080) significa que
cualquier procedimiento puede modificar sus argumentos, y el anidamiento léxico (clase 083) le da
acceso a todo lo que lo contenga.

Lo que PL/I sí tiene, y es una idea de esta clase, son las **funciones incorporadas matemáticas
declaradas como tales**: `sqrt`, `sin`, `log`, `abs`, `mod`, `max`. El compilador **sabe que son
puras** y las evalúa en compilación cuando los argumentos son constantes.

```pli
declare tabla(10) float initial((10) 0);
x = sqrt(2);      /* el compilador puede calcularlo al compilar */
```

Es el mismo mecanismo que el *constant folding* de cualquier compilador moderno, y funciona
únicamente porque la pureza de esas funciones **está codificada en el compilador**, no declarada por
el programador.

Esa es, en el fondo, la observación que cierra esta clase para toda la sección: **todos estos
lenguajes aprovechan la pureza cuando la conocen**. Lo que cambia es quién se lo dice al compilador:

- **Fortran**: el programador, con `pure`, y se comprueba.
- **Ada/SPARK**: el programador, con `Global => null`, y se demuestra.
- **C++**: el programador, con `constexpr`, y se comprueba parcialmente.
- **Lisp, PL/I, COBOL**: solo lo sabe el compilador de sus propias intrínsecas.
- **Tcl, Perl, M, RPG**: nadie; es disciplina.

Y esa escala —de la garantía a la costumbre— es exactamente lo que separa a un lenguaje que puede
paralelizar automáticamente de uno que no.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PURA ; Funciones puras -- clase 084
 read n
 write "puro=", $$cuadrado(n), !
 quit
 ;
cuadrado(x) ; devuelve x al cuadrado
 quit x * x
```

**Lo que esta clase enseña en M.** **En M la pureza es prácticamente inexpresable.** Todas las
variables son globales al proceso (clase 082), cualquier rutina puede leerlas y escribirlas, y la
indirección (clase 068) permite ejecutar código construido en tiempo de ejecución.

Ni siquiera se puede saber **estáticamente qué toca una rutina**.

Y hay un motivo de fondo que va más allá del lenguaje: **en M, el efecto secundario es el propósito**.
Un sistema clínico existe para escribir en `^PACIENTE`, no para calcular valores. La operación
central del lenguaje —`set ^GLOBAL(clave) = valor`— es una escritura en disco visible
inmediatamente para todos los procesos (clase 054).

En ese modelo, una función pura es la excepción, no la norma.

Lo que M sí tiene, y es lo que ocupa el lugar de las garantías de pureza, es el **control de
concurrencia**:

```mumps
 lock +^PACIENTE(id)          ; bloqueo cooperativo sobre ese nodo
 tstart                        ; inicio de TRANSACCIÓN
 set ^PACIENTE(id,"saldo") = nuevo
 tcommit
 lock -^PACIENTE(id)
```

`lock`, `tstart`, `tcommit` y `trollback` dan atomicidad y aislamiento sobre los efectos. Es la
respuesta de una base de datos al mismo problema que la pureza resuelve en un lenguaje funcional:
**hacer que los efectos sean predecibles**.

Dos estrategias opuestas —evitar los efectos o controlarlos transaccionalmente— y las dos llevan
décadas funcionando en producción.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'puro=', (n * n) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk **no tiene declaración de pureza**, y su modelo
—objetos con estado que se envían mensajes— está construido alrededor del efecto: un mensaje suele
cambiar el estado del receptor.

Pero la comunidad Smalltalk aportó a esta clase una distinción de diseño que hoy es doctrina y que se
enseña con su nombre: **la separación entre consulta y orden** (*command-query separation*), formulada
por Bertrand Meyer en el contexto de Eiffel, muy cercano a este mundo.

> **Un método o bien devuelve un valor y no cambia nada, o bien cambia algo y no devuelve nada. Nunca
> las dos cosas.**

Y la biblioteca de Smalltalk la sigue de forma muy visible, con una convención de nombres que la hace
evidente:

```smalltalk
coleccion size            "CONSULTA: pura"
coleccion sorted          "CONSULTA: devuelve una copia ordenada"
coleccion sort            "ORDEN: ordena en el sitio, devuelve self"
cadena asUppercase        "CONSULTA: una copia nueva"
cadena reversed           "CONSULTA"    vs   reverse  "ORDEN"
```

El participio (`sorted`, `reversed`) para la versión pura y el imperativo (`sort`, `reverse`) para la
que muta. Es la misma convención que Ruby resuelve con el sufijo `!` y que Lisp resuelve con el
prefijo `n` de la clase 054.

Que tres comunidades distintas hayan inventado una marca tipográfica para lo mismo dice bastante: **si
el lenguaje no distingue lo puro de lo impuro, los programadores lo distinguen en los nombres**.

---

## Y de vuelta a la clase

Lo transferible: **la pureza no es una preferencia estética, es una licencia para el compilador**. Si
una función es pura, se puede memorizar, eliminar si su resultado no se usa, ejecutar en otro hilo o
evaluar en compilación. Por eso `pure` está en Fortran, `constexpr` en C++ y `Global => null` en Ada:
los tres son promesas comprobadas a cambio de optimización. Y por eso, cuando un lenguaje no puede
comprobarlo, la pureza pasa a ser disciplina — que es exactamente lo que ocurre en el 80 % del código
de esta página.

⏮️ [Volver a la clase 084](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
