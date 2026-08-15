# -*- coding: utf-8 -*-
"""Parte 8, lote B — clase 124. Ver `vivos_parte8.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 124 — Compilador, intérprete y JIT
# ---------------------------------------------------------------------------
SPECS["124"] = dict(
    gancho="""
Contar dígitos. El programa da igual; lo que importa es **qué le pasa antes de ejecutarse**, y estos
doce lenguajes cubren el espectro completo: **cuatro compilan a código máquina** (COBOL, Fortran,
Ada, C++), **cuatro compilan a bytecode e interpretan** (Tcl, Perl, Lisp, Smalltalk), **uno traduce al
instalar** (RPG, con la Machine Interface de la clase 123), y **uno interpreta y es de los más rápidos
de su nicho** (M).
""",
    porque="""
Aquí el concepto es **cuándo se traduce el código**, y estos lenguajes lo enseñan porque desmontan la
división simplista entre compilado e interpretado. **Lisp lleva desde 1962 con las dos cosas a la
vez**: el mismo sistema interpreta en el REPL y compila funciones a código nativo, con
`compile-file` y `disassemble`. **Smalltalk tiene un JIT** con la tecnología que después fue HotSpot.
Y **Tcl y Perl compilan a una representación interna** que nadie llamaría intérprete puro.

Y **RPG** aporta el caso raro: **compilar a una arquitectura virtual y traducir a código nativo en la
instalación**, que es AOT diferido y le permitió sobrevivir a un cambio de procesador sin recompilar.
""",
    cierre="""
Lo transferible: **compilado e interpretado no son propiedades de un lenguaje, sino de una
implementación**. Hay C interpretado, Python compilado a nativo y JavaScript con uno de los mejores
compiladores del mundo. La pregunta útil no es "¿es compilado?" sino **"¿cuándo se toma cada
decisión?"**: los tipos, el destino de las llamadas, la disposición de la memoria. Cuanto más tarde se
decidan, más flexible es el lenguaje y más trabajo tiene que hacer en ejecución.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. DIGITOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(18) COMP-3.
01  D       PIC 9(4) COMP VALUE 0.
01  ED-D    PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    IF N = 0
        MOVE 1 TO D
    ELSE
        PERFORM UNTIL N = 0
            ADD 1 TO D
            COMPUTE N = FUNCTION INTEGER(N / 10)
        END-PERFORM
    END-IF

    MOVE D TO ED-D
    DISPLAY "digitos=" FUNCTION TRIM(ED-D)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL es **compilado a código máquina nativo**, y en z/OS lo es
con un compilador que merece conocerse porque es de los más optimizados que existen para su dominio.

**IBM Enterprise COBOL** comparte la infraestructura de optimización de los compiladores de C/C++ de
IBM, y sus opciones son reveladoras:

```text
OPT(2)              -- optimización agresiva
ARCH(12)            -- generar para z15 y usar SUS instrucciones
INLINE              -- integrar PERFORM en línea
NUMPROC(PFD)        -- suponer que los decimales están bien formados
SSRANGE             -- comprobar índices (clase 089): se DESACTIVA en producción
```

**`ARCH`** es interesante: los procesadores z tienen **instrucciones específicas para decimales
empaquetados** —el `COMP-3` de la clase 042— y para conversiones, así que una operación
`COMPUTE A = B + C` sobre decimales **es una sola instrucción de máquina**, no una emulación.

Eso explica una cosa que sorprende: **COBOL es más rápido que C para aritmética decimal exacta**, no
por el lenguaje sino porque **el hardware tiene esas operaciones y el compilador las usa**.

Y la relación con la máquina va más lejos: z/Architecture tiene instrucciones que existen básicamente
para lo que hace COBOL —`ED` y `EDMK` para el formateo con máscaras `PIC`, `TR` y `TRT` para
traducción y búsqueda de caracteres, `CLC` y `MVC` para bloques—.

**Es co-diseño de lenguaje y hardware**, sostenido durante sesenta años.

Y hay una segunda implementación que conviene nombrar porque cambia el cuadro: **GnuCOBOL**, el
compilador libre que este curso usa en CI, **traduce COBOL a C** y después lo compila con GCC. Es un
transpilador, y funciona bien: los programas de esta serie compilan y se ejecutan con él.

Esa es la prueba práctica del cierre de esta clase: **el mismo lenguaje, dos implementaciones
completamente distintas** — una que genera instrucciones z y otra que genera C.
"""),
        "fortran": ("""
program digitos
   implicit none
   integer :: n, d

   read(*, *) n

   if (n == 0) then
      d = 1
   else
      d = 0
      do while (n /= 0)
         d = d + 1
         n = n / 10
      end do
   end if

   write(*, '(A,I0)') 'digitos=', d
end program digitos
""", """
**Lo que esta clase enseña en Fortran.** Fortran es **compilado a nativo y con los mejores
optimizadores del mundo para código numérico**, y esta clase es el sitio para explicar por qué.

Un compilador de Fortran hace, de serie, transformaciones que en otros lenguajes son investigación:

```text
vectorización automática        (usar instrucciones SIMD)
desenrollado de bucles
intercambio de bucles           (cambiar el orden para la caché)
división en bloques              (tiling)
fusión y fisión de bucles
propagación de constantes entre procedimientos
integración en línea
paralelización automática
```

Y la razón de que pueda hacerlas ya se apuntó en la clase 123: **el modelo de aliasing**. En Fortran,
dos argumentos de una subrutina **no pueden solaparse**, y un `allocatable` no puede tener alias
(clase 090). Con esa garantía, el compilador **sabe** que reordenar es seguro.

En C, cualquier par de punteros puede apuntar al mismo sitio, así que el compilador debe suponer lo
peor — y por eso existe `restrict`, que es pedir a mano lo que Fortran da gratis.

Y hay una prueba histórica de esto que merece contarse: **durante décadas, los bancos de pruebas
numéricos mostraron que el mismo algoritmo era más rápido en Fortran que en C**, y la explicación no
era el lenguaje sino la información que el compilador tenía.

El ecosistema de compiladores es además de los más ricos que existen: **gfortran** (libre), **Intel
ifx**, **NVIDIA nvfortran** —que compila `do concurrent` a GPU—, **Cray**, **AMD flang**, **LFortran**
(basado en LLVM, con REPL incluido).

Y **LFortran** merece la mención final, porque desmonta el cierre de esta clase: es **un Fortran
interactivo**.

```text
$ lfortran
>>> integer :: i
>>> i = 42
>>> print *, i * 2
```

**Un REPL de Fortran**, con compilación incremental a LLVM y ejecución inmediata. Que el lenguaje más
asociado al compilado por lotes tenga hoy un intérprete interactivo es exactamente lo que dice el
cierre: **compilado o interpretado es una propiedad de la implementación**.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Digitos is
   N : Integer;
   D : Natural := 0;
begin
   Get (N);

   if N = 0 then
      D := 1;
   else
      while N /= 0 loop
         D := D + 1;
         N := N / 10;
      end loop;
   end if;

   Put ("digitos=");
   Put (D, Width => 1);
   New_Line;
end Digitos;
""", """
**Lo que esta clase enseña en Ada.** Ada es **compilado a nativo**, y su implementación de referencia
—**GNAT**— tiene una propiedad que explica buena parte de su historia reciente: **es una interfaz de
GCC**.

Robert Dewar y su equipo en la Universidad de Nueva York escribieron GNAT a principios de los noventa
con financiación del Departamento de Defensa, y la decisión de construirlo sobre GCC fue estratégica:
**Ada heredó de golpe todos los optimizadores y todas las arquitecturas de GCC**, y las sigue
heredando.

Por eso Ada compila hoy para ARM, RISC-V, x86-64, PowerPC y microcontroladores, **y para
WebAssembly**.

Y hay dos cosas de la compilación de Ada que son propias y que esta clase debe contar.

**La primera: las comprobaciones se pueden desactivar, y hay que hacerlo a propósito.**

```ada
pragma Suppress (All_Checks);          --  quitar TODAS las comprobaciones
pragma Suppress (Index_Check);          --  o solo las de índice
```

```bash
gnatmake -gnatp   # equivalente en la línea de órdenes
```

Por defecto, Ada comprueba índices, rangos, división por cero, desbordamiento y accesos nulos. Eso
cuesta, y el compilador **elimina la mayoría de las comprobaciones cuando puede demostrar que sobran**
— si un bucle va de `V'First` a `V'Last`, la comprobación de índice desaparece.

**Y con SPARK, se demuestran todas y se pueden quitar con garantías** (clase 118): es la única forma
honesta de tener seguridad y velocidad a la vez.

**La segunda: los perfiles restringidos.**

```ada
pragma Profile (Ravenscar);
```

**Ravenscar** es un subconjunto de las tareas de Ada, definido en 1997, pensado para sistemas de
tiempo real certificables: sin terminación de tareas, sin colas de entrada múltiples, sin
`select`... **Lo que queda se puede analizar temporalmente**, y de ahí que se pueda demostrar que un
sistema cumple sus plazos.

Con `pragma Profile (Ravenscar)`, **el compilador rechaza cualquier construcción fuera del perfil**, y
el runtime que se enlaza es una versión mínima y certificable.

Es una idea poco común y muy potente: **restringir el lenguaje para poder demostrar propiedades**, con
la restricción comprobada por el compilador.
"""),
        "pascal": ("""
program Digitos;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, D: Integer;

begin
  Read(N);

  if N = 0 then
    D := 1
  else
  begin
    D := 0;
    while N <> 0 do
    begin
      Inc(D);
      N := N div 10;
    end;
  end;

  WriteLn('digitos=', IntToStr(D));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal es **compilado a nativo** hoy, y su historia con esta
clase es de las mejores, porque **Pascal fue el lenguaje que popularizó el bytecode antes que Java**.

**UCSD Pascal** (Universidad de California en San Diego, 1977) compilaba a **p-code**, un bytecode para
una máquina virtual de pila, y distribuía el intérprete para cada máquina.

El resultado fue exactamente el argumento de Java veinte años después: **compila una vez, ejecuta en
cualquier sitio**. El sistema UCSD p-System corría en Apple II, en PDP-11, en el IBM PC original —era
uno de los tres sistemas operativos que IBM ofrecía con él— y en decenas de máquinas más.

Y su bytecode influyó directamente en el diseño de la JVM, cosa que sus autores reconocen.

Después llegó Turbo Pascal (clase 123) con compilación **directa a código máquina**, y ganó por
velocidad y por tamaño. El p-System desapareció.

Hoy, Free Pascal es un compilador nativo notable por su alcance:

```text
CPUs:  x86, x86-64, ARM, AArch64, RISC-V, PowerPC, MIPS, SPARC, m68k, AVR, Z80
SO:    Linux, Windows, macOS, FreeBSD, Android, iOS, DOS, OS/2, Amiga, Nintendo DS
```

**Un compilador mantenido por una comunidad pequeña que soporta más plataformas que casi cualquier
compilador comercial**, incluidas máquinas de los ochenta. Es uno de los ecosistemas de compilación
más versátiles que existen, y muy poco conocido fuera de su comunidad.

Y hay una peculiaridad de Free Pascal que conviene nombrar: **es un compilador auto-alojado escrito en
Pascal**, y su velocidad sigue la tradición de Turbo Pascal — compila el compilador entero en
segundos.

Delphi añade además la compilación cruzada a móviles con LLVM, así que el mismo código fuente produce
un ejecutable nativo para Windows, macOS, iOS y Android — que es lo que mantiene vivo el producto.
"""),
        "lisp": ("""
(let* ((n (read))
       (d (if (zerop n)
              1
              (loop with x = n
                    while (/= x 0)
                    count t
                    do (setf x (truncate x 10))))))
  (format t "digitos=~D~%" d))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp es **el desmentido más antiguo del cierre de esta
clase**: lleva desde 1962 siendo **compilado e interpretado a la vez, en el mismo sistema**.

```lisp
(defun f (x) (* x 2))        ; interpretada o compilada, según la implementación
(compile 'f)                  ; COMPILAR esta función, ahora, a código nativo
(disassemble 'f)               ; y ver el ensamblador
(compile-file "codigo.lisp")    ; compilar un fichero entero a FASL
```

**SBCL compila absolutamente todo a código máquina nativo**, incluido lo que se teclea en el REPL. No
hay intérprete: cuando escribes una expresión, **se compila y se ejecuta**. Y aun así el ciclo se
siente interactivo.

Otras implementaciones eligen distinto: **CLISP** compila a bytecode, **CCL** a nativo, **ECL** traduce
a C y lo compila con el compilador del sistema.

**El mismo lenguaje, cuatro estrategias.** Es el argumento del cierre en su forma más limpia.

Y Common Lisp da al programador un control sobre el compilador que casi ningún lenguaje ofrece:

```lisp
(declaim (optimize (speed 3) (safety 0) (debug 0)))
(declare (type (signed-byte 32) x))
(declare (inline f))
(the fixnum (+ a b))
```

**Las declaraciones de optimización son un vector de cinco cualidades** —velocidad, seguridad,
depuración, tamaño, velocidad de compilación— y se pueden fijar **por función o por bloque**.

Con `(safety 0)`, SBCL **quita las comprobaciones de tipo y de límites** y genera código comparable al
de C. Con `(safety 3)`, comprueba todo. **Y el programador decide dónde**, con la granularidad que
quiera.

Y SBCL hace algo que ayuda muchísimo y que casi nadie más hace: **avisa cuando no puede optimizar**.

```text
note: doing signed word to integer coercion, can't open code
note: forced to do GENERIC-+ (cost 10), unable to optimize due to type uncertainty
```

**Te dice por qué el código será lento y qué declaración de tipo lo arreglaría.** Es un diálogo con el
compilador, y es una de las razones por las que Lisp sigue siendo competitivo en rendimiento cuando se
usa bien.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

if {$n == 0} {
    set d 1
} else {
    set d 0
    while {$n != 0} {
        incr d
        set n [expr {$n / 10}]
    }
}

puts "digitos=$d"
""", """
**Lo que esta clase enseña en Tcl.** Tcl **compila a bytecode desde 1997** (clase 123), y su modelo de
ejecución tiene una particularidad que lo distingue de todos los demás bytecodes de esta página:
**la compilación es perezosa y por comando**.

Cuando el intérprete va a ejecutar un procedimiento por primera vez, **compila su cuerpo a bytecode y
lo guarda**. Y si el cuerpo cambia —porque se redefinió el procedimiento— **el bytecode se invalida**.

```tcl
tcl::unsupported::disassemble proc miProc
tcl::unsupported::disassemble script {set a 1}
```

Y aquí está lo interesante y lo que explica muchas cosas del rendimiento de Tcl: **no todos los
comandos se compilan**. El compilador tiene **generadores de código específicos** para los comandos
más usados —`set`, `if`, `while`, `foreach`, `incr`, `expr`, `lindex`— y el resto se ejecutan por la
vía general, invocando la implementación en C.

Por eso una operación aritmética con `expr {...}` es rápida y una con `expr $a + $b` no lo es: **la
primera se compila; la segunda construye una cadena y llama al analizador de expresiones**.

Y por eso las guías de rendimiento de Tcl insisten tanto en **usar los comandos del núcleo y con
llaves**: se traduce a "quédate en el camino compilado".

La otra mitad del rendimiento de Tcl es la de la clase 090: **la representación interna dual de los
valores**. Un valor lleva su forma textual y su forma interna —entero, lista, diccionario, bytecode— y
la conversión se hace una vez y se guarda.

**El *shimmering*** —alternar usos y forzar reconversiones— es la trampa correspondiente, y es la
causa más común de código Tcl inexplicablemente lento.

Y hay proyectos que van más allá: **TclQuadcode** compila procedimientos Tcl a LLVM, y las
implementaciones alternativas —Jim Tcl para sistemas empotrados, con 100 KB— demuestran otra vez lo
del cierre: **el mismo lenguaje admite implementaciones radicalmente distintas**.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;
$n += 0;

my $d = $n == 0 ? 1 : 0;
while ($n != 0) {
    $d++;
    $n = int($n / 10);
}

print "digitos=$d\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl **compila el programa entero a un árbol de operaciones y
después lo recorre** (clase 123). No es bytecode plano como el de Python o Java: es un **árbol de
estructuras enlazadas**, y el intérprete lo recorre siguiendo punteros.

```bash
perl -MO=Concise -e 'print 1+2'
```

Eso muestra los nodos: `const`, `add`, `print`, con sus enlaces. Y explica una característica de
rendimiento de Perl: **cada operación cuesta un salto indirecto**, así que Perl es rápido en las
operaciones grandes —expresiones regulares, ordenación, manejo de cadenas, todo implementado en C— y
lento en bucles aritméticos apretados.

Es exactamente el perfil contrario al de Fortran, y es coherente con para qué se usa cada uno.

Y Perl tiene una decisión de implementación que conviene conocer porque explica su consumo de memoria:
**cada valor es una estructura `SV`** —*scalar value*— con su tipo, sus banderas, su contador de
referencias y punteros a las representaciones que tenga.

Un entero en Perl no ocupa 8 bytes: ocupa **decenas**, porque lleva consigo la posibilidad de ser
también una cadena, una referencia o un número en coma flotante (clase 101).

Eso es lo que hace posible el tipado dinámico cómodo de Perl y lo que hace que un arreglo de un millón
de números consuma mucho más que en C. Para eso está **PDL** (clase 089), con arreglos compactos.

Hay además dos proyectos que ilustran el cierre de esta clase:

- **Perl con el compilador `B::CC`**, que traduce el árbol de operaciones a C. Nunca fue del todo
  fiable, y demostró que se puede.
- **Raku (Perl 6)** con **MoarVM**, que **sí tiene un JIT** y compila a código nativo las partes
  calientes, con optimización especulativa al estilo de las máquinas virtuales modernas.

Es el mismo lenguaje de la misma familia con dos modelos de ejecución completamente distintos.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    int d = 0;
    if (n == 0) {
        d = 1;
    } else {
        while (n != 0) {
            ++d;
            n /= 10;
        }
    }

    std::cout << "digitos=" << d << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ es el ejemplo canónico de **compilación anticipada a nativo**,
y esta clase es el sitio para explicar hasta dónde llega eso, porque va más lejos de lo que parece.

**Parte del programa se ejecuta al compilar**:

```cpp
constexpr int digitos(long long n) {          // clase 107
    int d = 0;
    if (n == 0) return 1;
    while (n) { ++d; n /= 10; }
    return d;
}
static_assert(digitos(12345) == 5);            // se calcula AL COMPILAR
consteval int obligatorio(int x) { ... }        // C++20: SIEMPRE al compilar
```

**`static_assert(digitos(12345) == 5)`** no genera ni una instrucción: el compilador ejecuta la función
y comprueba el resultado. Es un intérprete de C++ **dentro del compilador**, y desde C++20 admite casi
todo el lenguaje, incluida la reserva de memoria.

Y esa capacidad tiene un nombre que conviene tener claro: **C++ tiene dos "tiempos de ejecución"**, el
del compilador y el del programa, y `constexpr` decide en cuál puede correr algo.

Sobre la compilación propiamente dicha, las tres implementaciones principales toman decisiones
distintas y merece nombrarlas: **GCC**, **Clang/LLVM** —cuya representación intermedia se ha
convertido en la infraestructura de medio mundo, incluidos Rust, Swift y Julia— y **MSVC**.

Y C++ también desmiente el cierre de esta clase, y de dos formas:

- **Cling** es un intérprete de C++ construido sobre Clang, y es lo que hay debajo de los cuadernos de
  ROOT en el CERN: **se teclea C++ y se ejecuta**, con un REPL.
- **La compilación JIT con LLVM** se usa en producción en motores de bases de datos y en bibliotecas
  numéricas, que **generan y compilan C++ o LLVM IR en ejecución** para especializar una consulta o un
  núcleo de cálculo.

**Un lenguaje que se considera el ejemplo de lo compilado tiene un intérprete usado a diario en el
CERN.** Es el argumento del cierre, servido por el caso menos esperado.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi DIGITOS;
  n int(20) const;
end-pi;

dcl-s x int(20);
dcl-s d int(10) inz(0);

x = n;
if x = 0;
  d = 1;
else;
  dow x <> 0;
    d += 1;
    x = %div(x : 10);
  enddo;
endif;

dsply ('digitos=' + %char(d));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG es el caso más singular de esta clase, y ya se apuntó en la
123: **compila a una arquitectura virtual y traduce a código nativo al instalar**.

```text
CRTRPGMOD  →  *MODULE con código MI (Machine Interface)
CRTPGM     →  *PGM, todavía en MI
primera ejecución  →  el SLIC traduce MI a instrucciones Power y las guarda
```

**La MI es una arquitectura de máquina virtual diseñada en 1978**, con instrucciones de alto nivel —hay
una instrucción para "crear un objeto", otra para "resolver un puntero a un espacio"— y **la
traducción a código nativo la hace el sistema operativo**.

Esa decisión, llamada **independencia tecnológica**, dio un resultado que no tiene equivalente:

- **1988**: AS/400 con procesador CISC propietario.
- **1995**: cambio a PowerPC de 64 bits. **Los programas de los clientes siguieron funcionando sin
  recompilar y sin fuente**, retraducidos por el sistema.
- **Hoy**: Power10, y los mismos programas siguen ejecutándose.

**Treinta y ocho años de compatibilidad binaria a través de un cambio de arquitectura completo.**

Y hay un detalle que redondea la comparación con la JVM: **la traducción es AOT, no JIT**. Se hace una
vez, al instalar o al primer uso, y el resultado se guarda **en el propio objeto programa**. No hay
calentamiento y no hay reoptimización.

Es un punto intermedio poco frecuente: **la portabilidad del bytecode con el rendimiento del código
nativo compilado una vez**, que es exactamente lo que hoy buscan las imágenes nativas de Java y el AOT
de .NET.

Y sobre las opciones de compilación, RPG tiene una que conecta con la clase 089:

```text
CRTBNDRPG OPTION(*SRCSTMT) DBGVIEW(*SOURCE) OPTIMIZE(40)
```

`OPTIMIZE(40)` es el máximo, y **con optimización alta el depurador ya no puede mostrar valores
fiables** de las variables. Es el mismo compromiso que `-O2` y `-g` en GCC, y en IBM i está expuesto
como parámetro de la orden de compilación.
"""),
        "pli": ("""
 digitos: procedure options(main);

    declare n fixed binary(31);
    declare d fixed binary(31) initial(0);

    get list (n);

    if n = 0 then d = 1;
    else do while (n ^= 0);
       d = d + 1;
       n = divide(n, 10, 31);
    end;

    put skip list ('digitos=' || trim(char(d)));

 end digitos;
""", """
**Lo que esta clase enseña en PL/I.** PL/I es **compilado a nativo**, y su compilador es una pieza de
ingeniería con una historia relevante para esta clase: **el compilador de PL/I fue uno de los primeros
en hacer optimización global seria**.

El **PL/I Optimizing Compiler** de IBM (1971) y sobre todo el trabajo de **John Cocke** en IBM Research
sobre PL/I y sus sucesores dieron origen a técnicas que hoy están en todos los compiladores:

- **Numeración de valores** y eliminación de subexpresiones comunes.
- **Movimiento de código invariante** fuera de los bucles.
- **Reducción de fuerza** —sustituir multiplicaciones por sumas en bucles—.
- **Y la asignación de registros por coloreado de grafos**, de Chaitin, en IBM.

John Cocke recibió el Premio Turing en 1987 por ese trabajo, que además llevó a **RISC** — la idea de
que si el compilador es bueno, el procesador puede ser simple.

**La optimización moderna de compiladores nació, en buena medida, optimizando PL/I y Fortran en IBM.**

Y PL/I tiene una peculiaridad de compilación que hay que conocer: **la función `divide` del programa de
arriba**.

```pli
 d = n / 10;                    /* división que produce un resultado con DECIMALES */
 d = divide(n, 10, 31);          /* división ENTERA, con precisión declarada */
```

En PL/I, **`/` sobre enteros da un resultado con precisión calculada por reglas del estándar**, que
puede tener parte decimal y puede desbordar. `divide(a, b, precision)` **fija la precisión del
resultado explícitamente**.

Esa complejidad viene de la ambición del lenguaje: PL/I intenta que la aritmética "haga lo correcto"
combinando decimales fijos, binarios y flotantes, y las reglas de conversión ocupan decenas de páginas
del estándar (clase 101).

Es un ejemplo de lo que se dijo en la clase 107: **la potencia tuvo un coste en complejidad**, y esa
complejidad se paga en el compilador —que tardaba años en escribirse— y en el programador, que tiene
que conocer las reglas.
"""),
        "mumps": ("""
DIGITOS ; Compilador, interprete y JIT -- clase 124
 read n
 set d = 0
 if n = 0 set d = 1
 else  do
 . for  quit:n=0  set d = d + 1, n = n \\ 10
 write "digitos=", d, !
 quit
""", """
**Lo que esta clase enseña en M.** M es **interpretado**, y es de los lenguajes más rápidos de esta
página en lo suyo — que no es calcular, sino **mover datos entre memoria y disco**.

Las implementaciones modernas compilan las rutinas a una representación intermedia:

```text
MIRUT.m  →  MIRUT.o     (YottaDB: código objeto, cargado dinámicamente)
```

Y **InterSystems IRIS** va más lejos: compila ObjectScript a bytecode y tiene un caché de código
compilado en memoria compartida entre procesos.

Y aquí está lo que de verdad explica el rendimiento de M, y no tiene que ver con el intérprete: **el
acceso a los datos**.

En un lenguaje normal, leer un registro de base de datos implica: construir una consulta, enviarla por
un socket, que el motor la analice, la optimice, la ejecute, serialice el resultado, lo devuelva y el
cliente lo deserialice.

**En M, `set x = ^PAC(id, "nombre")` es una llamada a función que recorre un árbol B en memoria
compartida.** Sin consulta, sin socket, sin serialización y sin capa de red.

Es la razón, medida, de que los sistemas M ganen a arquitecturas mucho más modernas en cargas de
muchos accesos pequeños: **el coste no está en el lenguaje, está en las capas que M no tiene**.

Y hay un detalle de implementación que lo redondea: **los *globals* se cachean en memoria compartida
entre todos los procesos** del sistema. Un bloque de disco leído por un proceso está disponible para
los demás sin volver a leerlo, y las escrituras se agrupan.

Es una base de datos con arquitectura de memoria compartida, y el "intérprete" es una capa fina
encima.

Lo que M **no** hace bien es el cálculo: sin tipos, cada operación aritmética comprueba en ejecución si
el valor es numérico y lo convierte (clase 101). Para eso hay otros lenguajes, y las implementaciones
modernas permiten llamarlos — **YottaDB con C, Python, Go y Rust**, e IRIS con Java y .NET.

Es la conclusión sensata: **cada lenguaje es rápido donde su modelo le da ventaja**, y el de M es el
acceso a datos jerárquicos.
"""),
        "smalltalk": ("""
| n d |

n := stdin nextLine trimBoth asNumber.

d := n = 0
    ifTrue: [ 1 ]
    ifFalse: [ | x c | x := n. c := 0.
               [ x ~= 0 ] whileTrue: [ c := c + 1. x := x // 10 ].
               c ].

Transcript show: 'digitos=', d printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk **compila a bytecode y lo ejecuta en una máquina
virtual con JIT**, y su contribución a esta clase es enorme y poco reconocida: **buena parte de la
tecnología de las máquinas virtuales modernas salió de aquí**.

La línea es esta, y ya apareció en la clase 113:

- **Smalltalk-80** define un bytecode para una máquina de pila y una VM que cabía en un libro — el
  *Blue Book* incluía la especificación completa, y mucha gente la implementó.
- **Self** (1987) añade lo que faltaba para que un lenguaje totalmente dinámico fuera rápido: **cachés
  de línea polimórficas**, **compilación adaptativa** y **desoptimización** —volver a interpretar
  cuando una suposición falla—.
- **HotSpot** (1999), la VM de Java, la escribió **el mismo equipo**, con las mismas técnicas.
- **V8** (2008), la de JavaScript, y **Cog**, la de Pharo, siguen la misma línea.

**Cada vez que se ejecuta JavaScript en un navegador o Java en un servidor, se están usando ideas
desarrolladas para hacer rápido a Smalltalk.**

Y las técnicas son las que se necesitan cuando **todo se decide en ejecución**:

```text
caché de línea polimórfica  → recordar qué método se llamó la última vez desde este punto
compilación adaptativa       → compilar solo lo que se ejecuta mucho
integración especulativa      → suponer que el tipo será el mismo, y comprobarlo
desoptimización                → si la suposición falla, volver atrás sin romper nada
```

**La desoptimización es la más difícil y la más importante**: permite optimizar agresivamente
suponiendo cosas, porque siempre se puede deshacer.

En Pharo, todo eso es inspeccionable:

```smalltalk
(Integer >> #printString) symbolic.        "el bytecode del método"
Smalltalk vm parameterAt: 1.                "estadísticas de la VM"
```

Y **Cog** tiene además una propiedad rara: **la VM se genera a partir de código Smalltalk**. Se escribe
en un subconjunto llamado Slang, se traduce a C y se compila. Es decir, **la máquina virtual de
Smalltalk está escrita en Smalltalk** — coherente con todo lo demás del sistema.
"""),
    },
)
