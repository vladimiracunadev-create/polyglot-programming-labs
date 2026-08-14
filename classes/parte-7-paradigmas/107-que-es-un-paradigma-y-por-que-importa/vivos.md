# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 107

> [⬅️ Volver a la clase 107](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar de 1 a n. Doce lenguajes, doce formas, y ninguna es "la traducción" de otra: **cada una revela
qué considera normal su lenguaje**. Y aquí empieza la parte del curso donde estos doce dejan de ser
curiosidades históricas para convertirse en argumentos: **casi todos los paradigmas que hoy se
enseñan se inventaron en un lenguaje de esta página**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **paradigma** mismo, y estos lenguajes lo enseñan porque **son los originales**.
> La programación estructurada se peleó y se ganó en **COBOL, Fortran y PL/I** durante los setenta. La
> orientación a objetos se inventó en Simula y **se definió en Smalltalk**. La programación funcional
> nació en **Lisp** en 1958. La genérica, en **Ada**. La concurrencia con paso de mensajes, en **Ada** y
> en Smalltalk.
>
> Ver el mismo problema resuelto en los doce **antes** de estudiar los paradigmas uno a uno da la
> perspectiva que falta cuando cada paradigma se aprende en el lenguaje que lo popularizó y no en el que
> lo inventó.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (n >= 1) → stdout: `suma=<1+2+...+n>`
- **Regla:** `suma = 1 + 2 + ... + n`

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `3` | `suma=6` |
| `1` | `suma=1` |

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
PROGRAM-ID. SUMAN.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA  PIC X(80).
01  N      PIC S9(9)  COMP-3.
01  I      PIC S9(9)  COMP-3.
01  SUMA   PIC S9(18) COMP-3 VALUE 0.
01  ED-S   PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        ADD I TO SUMA
    END-PERFORM

    MOVE SUMA TO ED-S
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL es **imperativo y estructurado**, y merece decirse que la
segunda mitad de esa frase se ganó a pulso: **el COBOL de 1959 no era estructurado**.

Hasta el estándar de 1985, el lenguaje no tenía `END-IF`, `END-PERFORM` ni `EVALUATE`. Un `IF`
terminaba con un punto, así que un punto de más partía la condición en dos y un punto de menos
absorbía el resto del párrafo. La estructura se construía con `GO TO` y `PERFORM THRU`, y el resultado
es el código que dio fama al lenguaje.

La transición está documentada en el propio `PERFORM VARYING` de este programa: **es un bucle de
verdad, con condición al principio y sin etiquetas**, y convive con la posibilidad de escribir
`GO TO`.

Y esta clase es buen sitio para situar a COBOL en el mapa de paradigmas con precisión, porque suele
caricaturizarse:

| Paradigma | En COBOL |
|---|---|
| Imperativo estructurado | **Sí**, desde 1985 y de forma completa |
| Modular | **Sí**: programas, `CALL` dinámico, `COMMON` |
| Orientado a objetos | **Sí**, desde 2002 — y casi nadie lo usa (clase 099) |
| Declarativo | **Parcialmente**: `SORT`, `MERGE`, `SEARCH ALL`, SQL incrustado |
| Funcional | No |
| Concurrente | No en el lenguaje: lo aporta el monitor transaccional |

La fila del `SORT` merece un momento. `SORT` en COBOL **no es una llamada a biblioteca**: es una
sentencia del lenguaje que ordena un fichero entero, con `INPUT PROCEDURE` y `OUTPUT PROCEDURE`
opcionales para filtrar antes y después.

```cobol
SORT FICHERO-TRABAJO
    ON ASCENDING KEY CLI-ID
    INPUT PROCEDURE IS FILTRAR
    OUTPUT PROCEDURE IS PROCESAR
```

Es declarativo —dices qué orden quieres, no cómo ordenar— y detrás hay una implementación externa
altamente optimizada. Es la misma relación que hoy hay entre SQL y un motor de base de datos, en
COBOL desde 1968.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program suman
   implicit none
   integer :: n, i

   read(*, *) n

   !  Estilo declarativo: se describe el conjunto, no el recorrido.
   write(*, '(A,I0)') 'suma=', sum([(i, i = 1, n)])
end program suman
```

**Lo que esta clase enseña en Fortran.** Este programa no tiene bucle, y esa es la observación: **la
aritmética de arreglos de Fortran 90 es programación declarativa**.

`sum([(i, i = 1, n)])` **describe un conjunto y una reducción**; no dice en qué orden sumar. Y por eso
el compilador puede vectorizarlo, paralelizarlo o mandarlo a una GPU — libertad que un bucle explícito
con un acumulador no le da, porque el orden de la suma quedaría fijado.

Fortran ha ido acumulando paradigmas de una forma muy visible, y merece verlo como línea temporal:

| Versión | Qué añadió | Paradigma |
|---|---|---|
| 1957 | `DO`, `GOTO`, subrutinas | imperativo |
| 1977 | `IF/THEN/ELSE`, sin `WHILE` | estructurado (a medias) |
| 1990 | módulos, aritmética de arreglos, `where` | modular y **declarativo** |
| 1995 | `forall`, `pure` | funcional (a medias) |
| 2003 | tipos con métodos, herencia, `class` | **objetos** |
| 2008 | `do concurrent`, **coarrays** | **paralelo** |
| 2018 | equipos, imágenes fallidas | paralelo tolerante a fallos |

Dos filas destacan.

**`pure`** (clase 084) es la única declaración de pureza **comprobada por el compilador** de todos los
lenguajes de esta página, y no se añadió por elegancia funcional: se añadió **para poder
paralelizar**.

**Los coarrays** de 2008 son el paradigma que hace único a Fortran hoy:

```fortran
real :: campo(100)[*]            ! un arreglo distribuido entre IMÁGENES
campo(:)[3] = campo(:)[1]        ! copiar de la imagen 1 a la 3
sync all
```

Ese `[*]` declara una variable **repartida entre procesos**, y `[3]` accede a la copia de otro
proceso **como si fuera memoria local**. Es paso de mensajes con sintaxis de arreglo, **en el
lenguaje**, sin MPI y sin biblioteca.

Es el paradigma de espacio de direcciones global particionado (PGAS), y Fortran es el único lenguaje
mayoritario que lo tiene integrado.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Suman is
   N    : Integer;
   Suma : Integer := 0;
begin
   Get (N);

   for I in 1 .. N loop
      Suma := Suma + I;
   end loop;

   Put ("suma=");
   Put (Suma, Width => 1);
   New_Line;
end Suman;
```

**Lo que esta clase enseña en Ada.** Ada es el lenguaje de esta página **diseñado deliberadamente
multiparadigma**, y esa palabra hay que tomarla en serio: el proceso de diseño de 1977-1983 partió de
un pliego de requisitos —los documentos *Strawman*, *Woodenman*, *Tinman*, *Ironman* y *Steelman* del
Departamento de Defensa— que enumeraba **qué debía poder expresar el lenguaje**, no cómo.

El resultado tiene cinco paradigmas de primera clase, y en tres de ellos **Ada llegó antes que
nadie**:

| Paradigma | En Ada | Nota |
|---|---|---|
| Estructurado | 1983 | heredado de Pascal |
| Modular | 1983 | **el paquete: el antepasado del módulo moderno** (clase 086) |
| Genérico | 1983 | **antes que las plantillas de C++** (clase 078) |
| Concurrente | 1983 | **tareas y citas EN EL LENGUAJE, no en biblioteca** |
| Orientado a objetos | 1995 | tipos etiquetados |
| Por contrato | 2012 | `Pre`, `Post`, `Type_Invariant` |

La fila de la concurrencia es la más notable. **En 1983, cuando C acababa de estandarizarse y no tenía
hilos, Ada ya tenía tareas, citas, entradas con colas y objetos protegidos** (clases 096 y 103) como
construcciones del lenguaje:

```ada
task Sensor;
task body Sensor is
begin
   loop
      delay until Proxima;         --  temporización de TIEMPO REAL
      Leer;
   end loop;
end Sensor;
```

`delay until` con un instante absoluto, en lugar de "espera 10 ms", es la diferencia entre un sistema
que deriva y uno que no. Ese nivel de detalle sobre el tiempo está en el lenguaje.

Y **la programación por contrato** de Ada 2012 es el paradigma que más ha crecido después:

```ada
function Raiz (X : Float) return Float
   with Pre  => X >= 0.0,
        Post => abs (Raiz'Result ** 2 - X) < 0.001;
```

Con **SPARK**, esas condiciones **se demuestran matemáticamente** antes de ejecutar nada. Es
verificación formal integrada en un lenguaje industrial, y es lo que se usa hoy en aviónica, en el
metro de París y en criptografía.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Suman;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I, Suma: Integer;

begin
  Read(N);

  Suma := 0;
  for I := 1 to N do
    Suma := Suma + I;

  WriteLn('suma=', IntToStr(Suma));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal **fue diseñado para enseñar un paradigma**, y es
probablemente el único lenguaje de esta página del que se puede decir eso.

Wirth lo creó en 1970 con un objetivo declarado: **enseñar programación estructurada**. Y esa
intención explica sus decisiones más criticadas:

- **Sin `return` anticipado**, sin `break` y sin `continue`: un bloque tiene una entrada y una salida.
- **El `for` solo cuenta de uno en uno** (clase 092): para cualquier otra cosa, `while`.
- **Declaraciones antes del código**, en un orden fijo: constantes, tipos, variables, procedimientos.
- **Tipos fuertes** sin conversiones implícitas.

Todo eso es **doctrina de Dijkstra convertida en sintaxis**. Su carta *Go To Statement Considered
Harmful* es de 1968, el debate estaba vivo, y Pascal fue el argumento en forma de compilador.

Funcionó: durante veinte años, **Pascal fue el lenguaje con el que se aprendía a programar** en medio
mundo, y la generación que hoy dirige la informática aprendió estructuras de datos en su sintaxis
(clase 097).

Y luego pasó lo interesante: **Pascal se volvió multiparadigma sin dejar de ser Pascal**.

| Paradigma | Cuándo |
|---|---|
| Estructurado | 1970, por diseño |
| Modular | 1987, las `unit` de Turbo Pascal |
| Orientado a objetos | 1989 `object`, 1995 `class` en Delphi |
| Dirigido por eventos | 1995 — **y esto es lo grande** |
| Genérico | 2004 en Free Pascal, 2009 en Delphi |
| Funcional | 2009, métodos anónimos |

**La fila de 1995 es la importante.** Delphi popularizó la programación dirigida por eventos con
diseño visual: arrastrar un botón, hacer doble clic y escribir el manejador. Ese modelo —controles con
propiedades, eventos como `of object` (clase 085) y un inspector que edita `published` (clase 087)—
lo copió Visual Basic, lo copió .NET con el mismo autor detrás, y es el antepasado directo de cómo se
construyen interfaces hoy.

Un lenguaje creado para enseñar disciplina acabó definiendo la programación de aplicaciones de
escritorio. No estaba en el plan.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "suma=~D~%" (loop for i from 1 to n sum i)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp es **el lenguaje más multiparadigma de esta página**,
y lo es por una razón estructural: **cualquiera puede añadirle un paradigma con macros**, sin tocar el
compilador.

De los paradigmas que hoy se enseñan, **Lisp inventó o estrenó una lista larga**:

| Idea | Lisp, año | Se generalizó |
|---|---|---|
| Funciones de primera clase | 1958 | años 90 |
| Recursión como herramienta central | 1958 | siempre |
| Recolección de basura | 1959 | Java, 1995 |
| Código como datos, macros | 1963 | sigue siendo raro |
| Tipado dinámico con tipos en los valores | 1958 | Python, Ruby |
| REPL y desarrollo interactivo | 1964 | Jupyter, 2014 |
| Excepciones con reinicios | 1984 | **sigue sin copiarse** |
| Despacho múltiple (CLOS) | 1988 | Julia, 2012 |
| Programación orientada a aspectos | MOP, 1991 | AspectJ, 2001 |

Y hay una demostración que resume el argumento: **CLOS, el sistema de objetos de Common Lisp, está
escrito en Common Lisp**. La orientación a objetos no es una característica del lenguaje: es una
biblioteca de macros y funciones genéricas que se puede leer, modificar y sustituir.

Lo mismo vale para el `loop` de este programa, que es un lenguaje de bucles completo implementado como
macro (clase 092); para `unwind-protect` y las macros `with-` (clase 103); y para las bibliotecas que
añaden emparejamiento de patrones, tipos algebraicos, listas por comprensión o programación lógica.

**Screamer** merece mención por lo extremo: es una biblioteca que añade a Common Lisp **búsqueda no
determinista con retroceso** —el motor de Prolog de la clase 118— sin cambiar el lenguaje.

Ese es el argumento de fondo por el que Lisp sigue apareciendo en cualquier discusión sobre
paradigmas: **no compite en la lista, la genera**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set suma 0
for {set i 1} {$i <= $n} {incr i} {
    incr suma $i
}

puts "suma=$suma"
```

**Lo que esta clase enseña en Tcl.** Tcl tiene la posición más peculiar de esta página: **su
paradigma es no tener paradigma**.

El lenguaje son doce reglas de sustitución (clase 041) y un intérprete de comandos. **Todo lo demás
—condicionales, bucles, procedimientos, objetos, espacios de nombres— son comandos**, no sintaxis. Y
como cualquiera puede definir comandos, **cualquiera puede añadir construcciones de control**:

```tcl
proc repetir {n cuerpo} {
    for {set i 0} {$i < $n} {incr i} {
        uplevel 1 $cuerpo          ;# ejecutar en el ámbito del LLAMANTE
    }
}

repetir 3 { puts "hola" }
```

Eso es una estructura de control nueva, definida por el usuario, indistinguible de las del lenguaje.
Es lo mismo que las macros de Lisp, conseguido por otro camino: **en Lisp porque el código es una
lista; en Tcl porque el código es una cadena**.

`uplevel` y `upvar` (clase 080) son las piezas que lo hacen posible, y explican por qué Tcl ha podido
adoptar paradigmas sin cambiar:

| Paradigma | Cómo llegó |
|---|---|
| Procedimental | en el núcleo, 1988 |
| Modular | `namespace`, 1997 |
| Dirigido por eventos | `after` y `fileevent`, **1990** (clase 096) |
| Orientado a objetos | incr Tcl y Snit como bibliotecas; TclOO en el núcleo en 2012 |
| Concurrente | corrutinas (8.6) e hilos con `Thread` |
| Empotrado | **desde el principio: era su propósito** |

Esa última fila es la clave para entender el lenguaje. **Tcl se diseñó para ser incrustado en otras
aplicaciones** como lenguaje de configuración y automatización, y por eso su API en C es minúscula y
por eso está dentro de tantas herramientas —Cisco IOS, Vivado, ns-3, Expect— que sus usuarios no
identifican como "programas Tcl".

Es un paradigma en sí mismo: **el lenguaje como componente**, y es el que después reprodujeron Lua,
JavaScript incrustado y los lenguajes de guion de los motores de videojuegos.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum);

my $n = <STDIN>;
chomp $n;

print "suma=", sum(1 .. $n), "\n";
```

**Lo que esta clase enseña en Perl.** Perl tiene una postura sobre los paradigmas que está escrita en
su lema: **TMTOWTDI**, *there's more than one way to do it*.

Es lo contrario del "hay una forma obvia de hacerlo" de Python, y es una decisión de diseño explícita
de Larry Wall, que era lingüista antes que informático. Su argumento: **los lenguajes naturales tienen
sinónimos y registros, y eso no es un defecto** — permite decir lo mismo de la forma que corresponde
al contexto.

Este mismo programa admite media docena de estilos idiomáticos:

```perl
sum(1 .. $n)                              # funcional, con biblioteca
my $s = 0; $s += $_ for 1 .. $n;           # imperativo con modificador de sentencia
$s += $_ foreach 1 .. $n;                   # lo mismo, otra palabra
reduce { $a + $b } 1 .. $n;                  # reducción explícita
$n * ($n + 1) / 2;                            # matemático
```

Y todos son "buen Perl" según el contexto.

Los paradigmas que Perl acumuló:

| Paradigma | Cuándo |
|---|---|
| Procedimental | 1987 |
| Modular | 1994, paquetes y CPAN |
| Orientado a objetos | 1994, `bless` (clase 099) |
| Funcional | 1994, referencias a subrutinas y clausuras |
| Genérico | por tipado dinámico, siempre |
| Orientado a aspectos | `Hook::LexWrap`, `Moose` con `around` |

La aportación duradera de Perl no es un paradigma sino algo transversal: **hizo del texto un
ciudadano de primera clase**. Las expresiones regulares integradas en la sintaxis (clase 093), el
contexto (clase 059) y el aplanamiento de listas hacen que procesar texto se parezca más a describirlo
que a programarlo.

Y su otra aportación es cultural: **CPAN** (clase 088), que estableció que **un lenguaje es también su
ecosistema**. Todo lo que vino después —PyPI, npm, crates.io— es esa idea.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::vector<int> v(static_cast<std::size_t>(n));
    std::iota(v.begin(), v.end(), 1);

    std::cout << "suma=" << std::accumulate(v.begin(), v.end(), 0) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ es el caso extremo de acumulación de paradigmas, y su propio
creador lo describe como un lenguaje **multiparadigma por diseño**, con una condición que lo explica
casi todo: **no pagar por lo que no usas**.

| Paradigma | Desde | Coste en ejecución |
|---|---|---|
| Procedimental (C) | 1972 | ninguno |
| Orientado a objetos | 1983 | una indirección **solo si usas `virtual`** |
| Genérico | 1991 | **ninguno**: se resuelve al compilar |
| Funcional | 2011, lambdas | ninguno si no usas `std::function` |
| Metaprogramación | 1994, por accidente | ninguno: pasa en compilación |
| Concurrente | 2011 | el del sistema |

Dos filas merecen comentario.

**La metaprogramación con plantillas se descubrió, no se diseñó.** En 1994, Erwin Unruh escribió un
programa cuyos **mensajes de error del compilador imprimían números primos**, demostrando que el
sistema de plantillas era Turing-completo sin que nadie lo hubiera planeado. De ahí salieron Boost,
las bibliotecas de álgebra con expresiones y todo el cálculo en tiempo de compilación.

Hoy eso se hace con **`constexpr`** y `consteval`, que son la versión civilizada:

```cpp
constexpr int suma(int n) { return n * (n + 1) / 2; }
static_assert(suma(5) == 15);        // se calcula al COMPILAR
```

**Y la genérica de C++ es la aportación de Alexander Stepanov**, que llegó con una convicción poco
habitual: los algoritmos deben escribirse contra **conceptos matemáticos** —qué operaciones admite un
tipo— y no contra jerarquías de clases. La STL de 1994 es esa idea, y es la razón de que `std::sort`
funcione igual sobre un arreglo de C, un `vector` y una estructura ajena.

C++20 formalizó por fin esos conceptos como característica del lenguaje:

```cpp
template <std::integral T> T doblar(T x) { return x * 2; }
```

Es la misma dirección que Ada tomó en 1983 con los genéricos y las restricciones, por un camino
distinto y con treinta y siete años de diferencia.

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

dcl-pi SUMAN;
  n int(10) const;
end-pi;

dcl-s i    int(10);
dcl-s suma int(20) inz(0);

for i = 1 to n;
  suma += i;
endfor;

dsply ('suma=' + %char(suma));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG tiene la historia de paradigmas más extraña de esta página,
porque **empezó siendo declarativo y se volvió imperativo**, que es el camino contrario al de todos
los demás.

El **RPG original de 1959** no era un lenguaje de programación en el sentido habitual: era un
**generador de informes**. El programador rellenaba unas hojas de codificación describiendo **qué
ficheros leer, qué campos comparar y qué imprimir**, y el sistema generaba el programa.

```text
FCLIENTES  IP  E             DISK
ICLIREG    01
C           SALDO     ADD    TOTAL     TOTAL
OINFORME   D    1     01
O                              NOMBRE      30
```

No hay bucle principal escrito: **el ciclo de RPG** lo aporta el compilador. Lee el registro
siguiente, evalúa los indicadores, dispara los niveles de ruptura y ejecuta los totales
correspondientes (clase 092). El programador **declara qué debe pasar en cada nivel**, no cuándo.

Eso es programación declarativa, en 1959, y es el mismo modelo mental que una hoja de cálculo o un
generador de informes moderno.

Y luego el lenguaje recorrió el camino inverso:

| Versión | Qué cambió | Paradigma |
|---|---|---|
| 1959 | hojas de codificación, ciclo automático | **declarativo** |
| 1978 (RPG III) | estructuras de control, subrutinas | estructurado |
| 1994 (RPG IV/ILE) | procedimientos, prototipos, módulos | **modular** |
| 2001 | formato libre en el cálculo | imperativo moderno |
| 2013 | **formato totalmente libre** | igual que cualquier lenguaje actual |
| 2018+ | `DATA-INTO`, `DATA-GEN`, SQL incrustado | declarativo **otra vez**, por SQL |

La última fila cierra el círculo: **el RPG moderno vuelve a ser declarativo**, pero por SQL. Un
programa de hoy no recorre ficheros con el ciclo: escribe `exec sql select ... group by ...` y deja
que el motor decida cómo.

Ese ir y venir entre "declara qué quieres" e "indica cómo hacerlo" es el mejor resumen de lo que esta
parte del curso va a mostrar quince veces.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 suman: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare suma fixed binary(31) initial(0);

    get list (n);

    do i = 1 to n;
       suma = suma + i;
    end;

    put skip list ('suma=' || trim(char(suma)));

 end suman;
```

**Lo que esta clase enseña en PL/I.** PL/I es **el primer intento serio de lenguaje multiparadigma de
la historia**, y su fracaso relativo es una de las lecciones de diseño mejor documentadas.

El objetivo de IBM en 1964 era explícito: **un solo lenguaje que sustituyera a Fortran y a COBOL**, y
que sirviera además para programación de sistemas. Y el resultado técnico fue notable — en este curso
ha ido apareciendo lo que PL/I tenía antes que nadie:

- Punteros y reserva dinámica (1964) — antes que C.
- Recursión, multitarea y manejo de condiciones con alcance dinámico.
- Cadenas de longitud variable (`varying`) — el antepasado de `VARCHAR`.
- Aritmética de arreglos — antes que Fortran 90.
- Decimales exactos como COBOL **y** coma flotante como Fortran.
- `select`/`when`/`otherwise` sin caída entre casos (clase 100).
- Un preprocesador con variables, bucles y procedimientos.

Y aun así no desplazó a ninguno de los dos. Las razones se citan en todas las historias del diseño de
lenguajes:

1. **Era demasiado grande.** El estándar completo era inabarcable, los compiladores costaban años y
   nadie usaba más de un tercio del lenguaje.
2. **Las reglas de conversión implícita eran impredecibles.** PL/I convertía casi cualquier cosa a
   casi cualquier otra, con reglas documentadas hasta el detalle y **imposibles de recordar**.
3. **No tenía palabras reservadas**, así que `IF IF = THEN THEN THEN = ELSE;` es legal. Facilitaba el
   código existente y complicaba los compiladores y la lectura.
4. **Cada comunidad lo usó como el lenguaje que ya conocía**: los científicos escribían PL/I con
   estilo Fortran; los de gestión, con estilo COBOL.

Ese cuarto punto es el más instructivo y conecta con el cierre de esta clase: **un paradigma no se
adopta porque el lenguaje lo permita, sino porque la comunidad lo practique**.

Dijkstra fue característicamente duro: dijo que usar PL/I le recordaba a intentar volar con un avión
que tuviera setenta y cinco mil botones en la cabina. La cita es injusta con sus aciertos técnicos y
acertada sobre el problema real.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SUMAN ; Que es un paradigma -- clase 107
 read n
 set suma = 0
 for i=1:1:n set suma = suma + i
 write "suma=", suma, !
 quit
```

**Lo que esta clase enseña en M.** M es el lenguaje **menos multiparadigma** de esta página, y esa
austeridad es deliberada y tiene una explicación de fecha: **1966, en un miniordenador PDP-7 con 8 KB
de memoria**, compartido por varios usuarios de un hospital.

Con esa restricción, el lenguaje que salió tiene:

- **Un tipo de dato**: la cadena.
- **Una estructura de datos**: el árbol disperso ordenado (clase 089).
- **Un modelo de persistencia**: el mismo árbol, con `^` delante.
- **Ninguna declaración**: ni tipos, ni variables, ni funciones.
- **Ningún ámbito** salvo `new` (clase 082).
- **Comandos de una letra** y postcondicionales para ahorrar caracteres.

Es programación imperativa en su forma más desnuda, y **no ha añadido paradigmas**: el estándar de M
de 1995 es esencialmente el de 1977 con retoques.

Lo que sí ha pasado —y es lo que esta sección documenta— es que **las implementaciones han añadido los
paradigmas por encima**:

- **InterSystems ObjectScript**: clases, herencia, propiedades, excepciones `try/catch`, literales
  JSON, y objetos que se ven a la vez como tablas SQL y como *globals* (clase 105).
- **YottaDB**: enlaces con Python, Node.js, Go, Rust y C, así que la lógica moderna se escribe fuera y
  los datos siguen en *globals*.

Y merece cerrar con la observación que hace justicia al lenguaje. Lo que hoy se llama **base de datos
NoSQL orientada a documentos, sin esquema, jerárquica y con transacciones ACID** describe con
precisión lo que M tenía en 1966.

M no se quedó atrás en paradigmas de programación porque nunca compitió ahí: **su paradigma es el
modelo de datos**, y ese sigue siendo actual. Es la razón exacta de que un lenguaje sin tipos, sin
ámbitos y sin módulos siga gestionando los historiales clínicos de decenas de millones de personas.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript
    show: 'suma=', ((1 to: n) inject: 0 into: [ :acc :cada | acc + cada ]) printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk **no es multiparadigma: es monoparadigma en su
forma más pura**, y esa pureza es su aportación.

La regla es una sola: **todo es un objeto, y lo único que ocurre es que los objetos se envían
mensajes**. Sin excepciones:

```smalltalk
3 + 4                       "un mensaje + enviado al objeto 3"
x > 0 ifTrue: [ ... ]        "un mensaje ifTrue: enviado a un Boolean"
1 to: 10 do: [ ... ]         "un mensaje enviado a un número"
[ ... ] ensure: [ ... ]      "un mensaje enviado a un bloque"
Object subclass: #Persona    "un mensaje enviado a una CLASE"
Integer superclass            "las clases son objetos y responden preguntas"
```

**No hay palabras clave de control, no hay operadores y no hay declaraciones**: hay envíos de
mensajes. El lenguaje entero cabe en una postal, y sus reglas se explican en un párrafo.

Ahí está el mérito y ahí está la influencia. De Smalltalk salieron, tal como se usan hoy:

| Aportación | Año | Dónde está hoy |
|---|---|---|
| El término *orientado a objetos* | Alan Kay, 1967-72 | en todas partes |
| Modelo-Vista-Controlador | 1979 | toda la interfaz de usuario |
| Interfaz gráfica con ventanas y ratón | 1973 | Macintosh, Windows |
| **Refactorización automática** | 1997 | todos los IDE (clase 098) |
| Programación extrema y TDD | Kent Beck, 1996 | metodologías ágiles |
| **SUnit → JUnit** | 1994 | todos los marcos de pruebas |
| Desarrollo sobre un sistema vivo | 1980 | REPL, *hot reload* |

Kent Beck escribió SUnit en Smalltalk y después lo portó a Java con Erich Gamma: **JUnit es SUnit
traducido**, y de ahí salieron NUnit, PyTest, RSpec y todos los demás.

Y hay una frase de Alan Kay que resume por qué esta clase le da a Smalltalk el último lugar de la
página: dijo que lamentaba haber acuñado el término "orientado a objetos", porque **la idea importante
no eran los objetos sino el paso de mensajes**. Casi todos los lenguajes que se dicen orientados a
objetos copiaron lo primero y no lo segundo.

---

## Y de vuelta a la clase

Lo transferible: **un paradigma no es una técnica, es un conjunto de cosas que dejas de decidir**. En
el imperativo decides el orden de los pasos; en el declarativo renuncias a decidirlo y ganas que otro
lo optimice. En objetos renuncias a saber qué código se ejecuta a cambio de poder añadir casos sin
tocar nada. Cada paradigma **cambia libertad por garantías**, y elegir bien es saber qué garantía
necesitas. Lo que verás en las quince clases siguientes es esa negociación, quince veces.

⏮️ [Volver a la clase 107](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
