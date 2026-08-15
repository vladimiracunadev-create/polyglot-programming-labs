# -*- coding: utf-8 -*-
"""Parte 8, lote C — clase 125. Ver `vivos_parte8.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 125 — Bytecode y máquinas virtuales
# ---------------------------------------------------------------------------
SPECS["125"] = dict(
    gancho="""
`3 4 +` en notación polaca inversa: apilar, apilar, operar. **Eso es literalmente una máquina de
pila**, que es como funcionan la JVM, el CLR, la VM de Python, la de Smalltalk y la de Tcl. Y aquí hay
dos casos que llegaron antes que Java: **UCSD Pascal con su p-code en 1977** y **RPG con la Machine
Interface de IBM en 1978**, que sigue funcionando y ha sobrevivido a un cambio de procesador.
""",
    porque="""
Aquí el concepto es la **máquina abstracta como objetivo de compilación**, y estos lenguajes lo enseñan
porque **inventaron la idea y la probaron dos décadas antes de que se hiciera famosa**. El argumento
de "compila una vez, ejecuta en cualquier sitio" es de UCSD Pascal, no de Java. Y **la MI de IBM i
demostró la versión fuerte del argumento**: sobrevivir a un cambio completo de arquitectura sin
recompilar y sin fuente.

Y **Smalltalk** aporta la otra mitad: su bytecode venía **con la especificación de la VM publicada en
un libro**, y de sus técnicas de ejecución salieron HotSpot y V8 (clase 124).
""",
    cierre="""
Lo transferible: **un bytecode es un contrato entre el compilador y el ejecutor, y su valor depende de
qué se pueda hacer con él**. Si solo se interpreta, es portabilidad y lentitud; si se compila al
vuelo, es portabilidad y velocidad; y si se traduce al instalar, es portabilidad sin coste de
calentamiento. Las tres opciones existen hoy —bytecode puro, JIT, imagen nativa— y todas se probaron
primero en los lenguajes de esta página.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. MAQPILA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  T1      PIC X(20).
01  T2      PIC X(20).
01  T-OP    PIC X(20).
01  PILA.
    05  CELDA  PIC S9(18) COMP-3 OCCURS 20 TIMES.
01  TOPE    PIC 9(4) COMP VALUE 0.
01  X       PIC S9(18) COMP-3.
01  Y       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO T1 T2 T-OP

    *> PUSH, PUSH
    ADD 1 TO TOPE
    COMPUTE CELDA(TOPE) = FUNCTION NUMVAL(T1)
    ADD 1 TO TOPE
    COMPUTE CELDA(TOPE) = FUNCTION NUMVAL(T2)

    *> POP, POP, operar, PUSH
    MOVE CELDA(TOPE) TO Y
    SUBTRACT 1 FROM TOPE
    MOVE CELDA(TOPE) TO X
    SUBTRACT 1 FROM TOPE

    EVALUATE FUNCTION TRIM(T-OP)
        WHEN "+"  COMPUTE X = X + Y
        WHEN "-"  COMPUTE X = X - Y
        WHEN "*"  COMPUTE X = X * Y
        WHEN OTHER MOVE 0 TO X
    END-EVALUATE

    ADD 1 TO TOPE
    MOVE X TO CELDA(TOPE)

    MOVE CELDA(TOPE) TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL **compila a código máquina nativo** (clase 124) y no tiene
máquina virtual — con dos excepciones que merecen conocerse.

**La primera es GnuCOBOL**, el compilador que este curso usa en CI: **traduce COBOL a C** y lo compila.
El "bytecode" es código C intermedio, y con eso hereda todas las plataformas de GCC.

**Y la segunda es la más interesante: COBOL sobre la JVM y sobre .NET.**

```text
Micro Focus Visual COBOL  →  bytecode de la JVM  o  CIL de .NET
IBM COBOL for Java (COBOL-JVM)
```

**Un programa COBOL compilado a bytecode de Java** puede llamar a clases Java, ser llamado desde ellas
y ejecutarse en un servidor de aplicaciones. Es la estrategia de migración de las clases 105 y 112 —
la modernización por los bordes— llevada al extremo: **el lenguaje no cambia, cambia el objetivo de
compilación**.

Y funciona porque, como se vio en la clase 110, **la orientación a objetos de COBOL 2002 se diseñó
para alinearse con Java**.

Y hay una relación entre COBOL y las máquinas de pila que esta clase permite señalar y que es
histórica: **la aritmética decimal de COBOL fue una de las razones de que la JVM y el CLR tengan tipos
decimales**.

`System.Decimal` de .NET y `java.math.BigDecimal` existen porque **el software de gestión necesita
decimales exactos** (clase 042), y ese requisito viene directamente del mundo COBOL. La primera es
incluso decimal de coma flotante con 96 bits de mantisa — diseñada para lo que hace un `PIC
S9(13)V99`.

Y para cerrar con el modelo de este programa: **una máquina de pila es exactamente lo que hace un
`COMPUTE`**. El compilador de COBOL convierte `COMPUTE A = B * C + D` en una secuencia de cargas,
operaciones y almacenamientos — que es lo mismo que este programa hace a mano con `CELDA` y `TOPE`.

Escribirlo así una vez es la mejor forma de entender qué hay debajo de una expresión.
"""),
        "fortran": ("""
program maqpila
   implicit none
   integer :: pila(20), tope, x, y, a, b, p1, p2
   character(len=200) :: linea
   character(len=1)   :: op

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(trim(linea), ' ')
   read(linea(1:p1-1), *) a
   p2 = index(trim(linea(p1+1:)), ' ') + p1
   read(linea(p1+1:p2-1), *) b
   op = linea(p2+1:p2+1)

   tope = 0
   tope = tope + 1;  pila(tope) = a        ! PUSH
   tope = tope + 1;  pila(tope) = b        ! PUSH

   y = pila(tope);  tope = tope - 1        ! POP
   x = pila(tope);  tope = tope - 1        ! POP

   select case (op)
   case ('+');   x = x + y
   case ('-');   x = x - y
   case ('*');   x = x * y
   case default; x = 0
   end select

   tope = tope + 1;  pila(tope) = x        ! PUSH

   write(*, '(A,I0)') 'resultado=', pila(tope)
end program maqpila
""", """
**Lo que esta clase enseña en Fortran.** Fortran **compila a nativo y no tiene máquina virtual**, y su
relación con esta clase es de las más curiosas de la página: **el hardware para el que se diseñó
Fortran NO tenía pila**.

El IBM 704 de 1957 no tenía instrucciones de pila ni registro de pila, y por eso el FORTRAN original
**no tenía recursión** (clase 097): las variables locales de cada subrutina se asignaban
estáticamente, en direcciones fijas.

Esa decisión —**variables estáticas en lugar de marco de pila**— es la que se comentó en la clase 082,
y aquí se ve su origen: **no había pila donde ponerlas**.

Y hay una consecuencia técnica de eso que sobrevivió décadas: **el retorno de subrutina se implementaba
modificando el código**. La instrucción de salto de vuelta **se escribía en tiempo de ejecución** con
la dirección del llamante — código automodificable, que era la práctica normal en 1957 y que la
existencia de una pila hizo innecesaria.

Hoy Fortran es completamente convencional en esto: marcos de pila, recursión y todo lo demás. Y hay
proyectos que lo llevan a máquinas virtuales:

- **LFortran** compila a **LLVM IR** —una representación intermedia que es, en la práctica, un bytecode
  para una máquina abstracta— y de ahí a nativo, a WebAssembly o a ejecución interactiva (clase 124).
- **Fortran a WebAssembly** con LFortran o Emscripten: código numérico de 1980 ejecutándose en un
  navegador.

Y esa última posibilidad conecta con la clase 162 del curso: **WebAssembly es una máquina de pila**, y
compilar Fortran para ella significa que los mismos algoritmos que corren en un superordenador pueden
correr en una página web.

Y merece cerrar con la observación de fondo: **una máquina de pila es una forma de organizar el
cálculo, no una tecnología moderna**. Este programa lo demuestra con veinte líneas de Fortran, y es lo
mismo que hace la JVM al ejecutar `iadd`.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Maqpila is
   Pila   : array (1 .. 20) of Integer := (others => 0);
   Tope   : Natural := 0;
   Linea  : String (1 .. 200);
   Ultimo : Natural;
   Pos    : Integer := 1;
   A, B, X, Y : Integer;
   Fin    : Positive;
   Op     : Character := ' ';
begin
   Get_Line (Linea, Ultimo);

   Get (Linea (Pos .. Ultimo), A, Fin);   Pos := Fin + 1;
   Get (Linea (Pos .. Ultimo), B, Fin);   Pos := Fin + 1;

   while Pos <= Ultimo and then Linea (Pos) = ' ' loop
      Pos := Pos + 1;
   end loop;
   Op := Linea (Pos);

   Tope := Tope + 1;  Pila (Tope) := A;      --  PUSH
   Tope := Tope + 1;  Pila (Tope) := B;      --  PUSH

   Y := Pila (Tope);  Tope := Tope - 1;      --  POP
   X := Pila (Tope);  Tope := Tope - 1;      --  POP

   case Op is
      when '+'    => X := X + Y;
      when '-'    => X := X - Y;
      when '*'    => X := X * Y;
      when others => X := 0;
   end case;

   Tope := Tope + 1;  Pila (Tope) := X;      --  PUSH

   Put ("resultado=");
   Put (Pila (Tope), Width => 1);
   New_Line;
end Maqpila;
""", """
**Lo que esta clase enseña en Ada.** Ada **compila a nativo** y no tiene una máquina virtual estándar, y
tiene algo que casi ningún lenguaje de esta página: **un formato intermedio definido y usado en la
industria**.

**DIANA** (*Descriptive Intermediate Attributed Notation for Ada*, 1981) fue una representación
intermedia estandarizada para Ada: un árbol sintáctico anotado con la información semántica, pensado
para que **las herramientas —compiladores, depuradores, analizadores, generadores de documentación—
compartieran la misma representación del programa**.

Es una idea que hoy se ha vuelto central con el **Protocolo de Servidor de Lenguaje (LSP)** y con las
representaciones intermedias de los compiladores modernos, y en Ada se intentó en 1981.

Y hay una segunda cosa, y es la que de verdad importa en el mundo de Ada: **los perfiles de runtime**.

```text
Runtime completo    → todo Ada: tareas, excepciones, biblioteca estándar
Ravenscar            → subconjunto de tiempo real certificable (clase 124)
ZFP (Zero FootPrint) → SIN runtime: para microcontroladores de kilobytes
```

**Con ZFP, un programa Ada se ejecuta directamente sobre el metal**, sin sistema operativo y sin
soporte de ejecución — no hay tareas, no hay excepciones y no hay reserva dinámica, y a cambio el
ejecutable puede caber en unos kilobytes.

Eso es exactamente lo contrario de una máquina virtual, y es la otra respuesta al problema de la
portabilidad: **en lugar de un ejecutor común, un compilador que genera para cada objetivo**.

Y hoy Ada llega también a los objetivos modernos de esta clase:

```bash
alr build --target=wasm32        # WebAssembly
```

**GNAT compila a WebAssembly**, con lo que un programa Ada verificado con SPARK puede ejecutarse en un
navegador. Es una combinación llamativa: **el lenguaje de la aviónica sobre la máquina virtual de la
web**.

Y para el ejercicio de esta clase, merece señalar que la pila de este programa lleva sus límites en el
tipo (clase 089): **si el índice se pasa, `Constraint_Error`**. Una máquina de pila escrita en Ada no
puede tener desbordamiento silencioso — que es exactamente el fallo que sí tienen las VM escritas en
C cuando se les cuela un bytecode malicioso.
"""),
        "pascal": ("""
program Maqpila;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Pila: array[1..20] of Integer;
  Tope, X, Y, A, B, P1, P2: Integer;
  Linea: string;
  Op: Char;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P1 := Pos(' ', Linea);
  A := StrToInt(Copy(Linea, 1, P1 - 1));
  P2 := Pos(' ', Copy(Linea, P1 + 1, Length(Linea))) + P1;
  B := StrToInt(Copy(Linea, P1 + 1, P2 - P1 - 1));
  Op := Linea[P2 + 1];

  Tope := 0;
  Inc(Tope); Pila[Tope] := A;         { PUSH }
  Inc(Tope); Pila[Tope] := B;         { PUSH }

  Y := Pila[Tope]; Dec(Tope);         { POP }
  X := Pila[Tope]; Dec(Tope);         { POP }

  case Op of
    '+': X := X + Y;
    '-': X := X - Y;
    '*': X := X * Y;
  else
    X := 0;
  end;

  Inc(Tope); Pila[Tope] := X;         { PUSH }

  WriteLn('resultado=', IntToStr(Pila[Tope]));
end.
""", """
**Lo que esta clase enseña en Pascal.** Aquí está el dato que abre esta clase, y merece contarse
entero: **Pascal inventó el argumento de "compila una vez, ejecuta en cualquier sitio", en 1977**.

El **p-code** de UCSD Pascal era el bytecode de una máquina de pila, y el **UCSD p-System** era el
entorno completo —compilador, editor, sistema de ficheros— portado a cada máquina. Compilar un
programa producía p-code, y ese p-code **se ejecutaba sin cambios en cualquier máquina con el
intérprete**.

Y funcionó a escala: el p-System corrió en Apple II, en PDP-11, en Z80, en el 68000 y **fue uno de los
tres sistemas operativos que IBM ofreció con el PC original en 1981** —junto con PC-DOS y CP/M-86—.

**Java hizo el mismo argumento dieciocho años después**, y sus diseñadores han reconocido la
influencia. La estructura es idéntica: máquina de pila, bytecode compacto, verificación al cargar,
intérprete portable.

La diferencia que hizo ganar a Java fue de contexto: **en 1977 la portabilidad no compensaba la
lentitud**, y Turbo Pascal, compilando a nativo, barrió al p-System (clase 123). En 1995, con la web y
con máquinas mil veces más rápidas, la ecuación cambió.

Y hay una segunda aportación de Pascal a esta clase, menos conocida: **Delphi compiló a bytecode
antes que a móviles**. Y hoy:

- **Free Pascal** genera nativo para veinte arquitecturas (clase 124).
- **Delphi** compila a LLVM para iOS y Android.
- **pas2js** compila Object Pascal a **JavaScript**, y hay proyectos que apuntan a **WebAssembly**.

Es decir: **el lenguaje que inventó el bytecode portable acabó compilando a nativo, y ahora compila
otra vez a máquinas virtuales** — las de la web.

Y para el ejercicio de este programa, una nota: `Pila: array[1..20] of Integer` con
`{$RANGECHECKS ON}` (clase 089) detecta el desbordamiento de pila. Sin esa opción, no — y ese es
exactamente el fallo de seguridad que ha aparecido varias veces en máquinas virtuales escritas en C.
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read))
       (op (symbol-name (read)))
       (pila '()))
  (push a pila)                      ; PUSH
  (push b pila)                       ; PUSH
  (let* ((y (pop pila))                ; POP
         (x (pop pila))                 ; POP
         (r (cond ((string= op "+") (+ x y))
                  ((string= op "-") (- x y))
                  ((string= op "*") (* x y))
                  (t 0))))
    (push r pila)
    (format t "resultado=~D~%" (first pila))))
""", """
**Lo que esta clase enseña en Common Lisp.** `push` y `pop` sobre una lista **son las operaciones de
una máquina de pila** (clase 096), así que este programa se escribe con las primitivas del lenguaje.

Y Lisp tiene con las máquinas virtuales una relación doble que merece contarse.

**Por un lado, las implementaciones.** Como se vio en la clase 124, **CLISP compila a bytecode** para
una máquina de pila, y ese bytecode es portable entre plataformas. **ECL traduce a C**. **SBCL y CCL
compilan a nativo**. El mismo lenguaje, tres modelos.

**Y por otro, y es lo importante: el bytecode de Lisp se puede escribir en Lisp.**

Como el código es una estructura de datos (clase 097), **escribir un compilador de Lisp a una máquina
de pila es un ejercicio de un par de páginas**, y aparece en todos los libros clásicos —SICP, *Lisp in
Small Pieces*, *Paradigms of AI Programming*—.

```lisp
(defun compilar (expr)
  (cond ((numberp expr) (list (list :push expr)))
        ((consp expr)
         (append (compilar (second expr))
                 (compilar (third expr))
                 (list (list :op (first expr)))))))

(compilar '(+ 3 4))     ; ((:PUSH 3) (:PUSH 4) (:OP +))
```

**Ocho líneas y ya hay un compilador a bytecode de pila.** Y como el bytecode resultante es una lista,
**se puede imprimir, guardar, transformar y ejecutar** con el mismo lenguaje.

Ese es el motivo por el que tantos lenguajes se prototipan en Lisp, y por el que la investigación en
compiladores lo ha usado tanto.

Y hay una historia de hardware que cierra la clase: **las máquinas Lisp** de Symbolics, LMI y Xerox
(1979-1990) **ejecutaban un bytecode de Lisp en el propio procesador**, con soporte de hardware para
etiquetas de tipo, comprobación de límites y recolección de basura.

Eran, literalmente, **una máquina virtual de Lisp implementada en silicio**. Desaparecieron cuando los
procesadores genéricos con buenos compiladores las superaron — que es la misma historia que las
máquinas Java de los noventa y por la misma razón.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b op

set pila {}
lappend pila $a                 ;# PUSH
lappend pila $b                  ;# PUSH

set y [lindex $pila end]; set pila [lrange $pila 0 end-1]   ;# POP
set x [lindex $pila end]; set pila [lrange $pila 0 end-1]   ;# POP

switch -exact -- $op {
    "+"     { set r [expr {$x + $y}] }
    "-"     { set r [expr {$x - $y}] }
    "*"     { set r [expr {$x * $y}] }
    default { set r 0 }
}

lappend pila $r
puts "resultado=[lindex $pila end]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl **compila a bytecode para una máquina de pila desde 1997**
(clases 123 y 124), y su bytecode se puede ver:

```tcl
tcl::unsupported::disassemble script {expr {3 + 4}}
```

Y el resultado es exactamente lo que hace este programa:

```text
push1 3
push1 4
add
done
```

**Ese `push, push, add` es el mismo que la JVM genera para `3 + 4` y el mismo que este programa
escribe a mano.** Todas las máquinas de pila se parecen porque el problema es el mismo.

Lo que hace peculiar al bytecode de Tcl es lo que ya se contó en la clase 124: **no todo se compila**.
El compilador tiene generadores específicos para unos setenta comandos del núcleo, y lo demás se
ejecuta invocando la implementación en C.

Eso da un bytecode **híbrido**: instrucciones de pila para lo compilable, y una instrucción
`invokeStk` genérica para llamar a cualquier otro comando.

```text
push1 "miProc"
push1 5
invokeStk 2          ;# llamada genérica: se resuelve en ejecución
```

Y esa instrucción es la razón de que Tcl sea extensible sin límite: **cualquier comando, definido en
Tcl o en C, se invoca igual**, y redefinir uno funciona inmediatamente (clase 109).

Tcl tiene además una propiedad relevante para esta clase: **el bytecode se invalida y se regenera**. Si
se redefine un procedimiento, el bytecode que lo llamaba **sigue siendo válido** —porque la llamada es
genérica— pero el del propio procedimiento se descarta.

Es la flexibilidad que exige un lenguaje donde todo se puede cambiar en marcha, y el precio que paga
en rendimiento frente a una VM que puede fijar más cosas.

Y para sistemas empotrados existe **Jim Tcl**, una implementación completa en 100 KB con su propio
bytecode — otra vez, el mismo lenguaje con implementaciones muy distintas.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a, $b, $op) = split ' ', $linea;

my @pila;
push @pila, $a;                # PUSH
push @pila, $b;                 # PUSH

my $y = pop @pila;               # POP
my $x = pop @pila;                # POP

my $r = $op eq '+' ? $x + $y
      : $op eq '-' ? $x - $y
      : $op eq '*' ? $x * $y
      :              0;

push @pila, $r;
print "resultado=$pila[-1]\\n";
""", """
**Lo que esta clase enseña en Perl.** `push` y `pop` son operaciones del lenguaje (clase 096), así que
la máquina de pila se escribe sola.

Y Perl es interesante en esta clase porque **su modelo de ejecución NO es una máquina de pila**: es un
**árbol de operaciones recorrido con punteros** (clase 124).

```bash
perl -MO=Concise -e '3 + 4'
```

El resultado no es `push push add`: es un árbol con un nodo `add` que tiene dos hijos `const`. El
intérprete **recorre el árbol siguiendo el puntero `op_next`**, y cada nodo es una función en C.

Esa diferencia es real y tiene consecuencias:

| | Máquina de pila | Árbol de operaciones |
|---|---|---|
| Representación | vector de bytes | estructuras enlazadas |
| Despacho | un salto por instrucción | un salto por nodo |
| Compacidad | **alta** | baja |
| Facilidad para optimizar | media | **alta para el análisis** |

Perl eligió el árbol porque su compilador hace **optimizaciones sobre él** —plegado de constantes,
eliminación de nodos, reconocimiento de idiomas frecuentes— y porque **el árbol conserva la estructura
del programa**, que es lo que `B::Deparse` necesita para reconstruir el fuente (clase 123).

Y Perl tiene, aun así, **una pila real y muy visible**: la pila de argumentos.

```perl
sub f { my @args = @_; ... }
```

**`@_` es literalmente la pila de argumentos del intérprete** (clase 079), con alias a los originales.
Y las operaciones de Perl trabajan sobre ella: cada nodo del árbol **saca sus operandos de la pila y
empuja el resultado**.

Es decir: **Perl tiene una máquina de pila para los datos y un árbol para el control**. Es un híbrido, y
conocerlo explica por qué `wantarray` funciona, por qué el contexto (clase 059) se propaga hacia abajo
y por qué `goto &funcion` (clase 108) puede sustituir un marco entero.

Y **Raku con MoarVM** sí tiene bytecode y JIT, con optimización especulativa. El mismo linaje, dos
arquitecturas.
"""),
        "cpp": ("""
#include <iostream>
#include <stack>
#include <string>

int main() {
    int a{}, b{};
    std::string op;
    if (!(std::cin >> a >> b >> op)) return 1;

    std::stack<int> pila;
    pila.push(a);                       // PUSH
    pila.push(b);                        // PUSH

    const int y = pila.top();  pila.pop();   // POP
    const int x = pila.top();  pila.pop();    // POP

    int r = 0;
    if      (op == "+") r = x + y;
    else if (op == "-") r = x - y;
    else if (op == "*") r = x * y;

    pila.push(r);
    std::cout << "resultado=" << pila.top() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ compila a nativo (clase 124), y esta clase permite señalar algo
que sí es una máquina virtual y que está en todas partes: **LLVM IR**.

```llvm
%1 = add nsw i32 3, 4
```

**LLVM IR es una representación intermedia con forma de ensamblador de una máquina abstracta** —de
registros, no de pila— y es el objetivo de compilación de Clang, Rust, Swift, Julia, Zig y decenas
más.

Y aunque normalmente sea un paso intermedio, **se puede guardar, transformar, distribuir y ejecutar**:

```bash
clang -emit-llvm -S prog.cpp -o prog.ll     # generar el IR
lli prog.ll                                   # EJECUTARLO con un intérprete/JIT
```

`lli` es un intérprete y JIT de LLVM IR, así que **C++ se puede ejecutar sobre una máquina virtual**
si se quiere — que es lo que hace Cling (clase 124).

Y de ahí sale el vínculo con el cierre de esta clase, que hoy es lo más relevante: **WebAssembly**.

```bash
emcc prog.cpp -o prog.html      # C++ → WebAssembly, vía LLVM
```

**WebAssembly es una máquina de pila** —igual que la JVM y que el p-code de Pascal de esta misma
página— con un bytecode compacto, verificación al cargar y ejecución en un espacio aislado.

Y su diseño aprendió de todos los anteriores: **es de pila para ser compacto**, tiene **tipos
explícitos para poder verificarse rápido**, y está pensado para **compilarse a nativo al cargar**, no
para interpretarse.

C++ es hoy uno de los principales lenguajes de origen para WebAssembly, y con eso se cierra un círculo
que esta clase recorre: **el argumento de UCSD Pascal en 1977 —compila una vez, ejecuta en cualquier
sitio— se cumple hoy con C++ en un navegador**.

Y la pila de este programa usa `std::stack`, que es un adaptador (clase 096): **quita las operaciones
que romperían la disciplina**. Escribir una VM con él da, gratis, la garantía de que nadie mira dentro
de la pila por medio.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi MAQPILA;
  a  int(10) const;
  b  int(10) const;
  op char(1) const;
end-pi;

dcl-s pila int(20) dim(20);
dcl-s tope int(10) inz(0);
dcl-s x    int(20);
dcl-s y    int(20);

tope += 1;  pila(tope) = a;        // PUSH
tope += 1;  pila(tope) = b;         // PUSH

y = pila(tope);  tope -= 1;          // POP
x = pila(tope);  tope -= 1;           // POP

select;
  when op = '+';  x = x + y;
  when op = '-';  x = x - y;
  when op = '*';  x = x * y;
  other;          x = 0;
endsl;

tope += 1;  pila(tope) = x;

dsply ('resultado=' + %char(pila(tope)));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Aquí está el segundo caso de esta clase que llegó antes que Java,
y es el más impresionante de los dos: **la Machine Interface de IBM i, de 1978** (clases 123 y 124).

La MI **no es una máquina de pila** al estilo de la JVM: es una **arquitectura virtual de alto nivel**
con instrucciones que manipulan objetos del sistema.

```text
CRTS   -- crear un espacio
SETSPPFP -- fijar un puntero a espacio
CPYBLA  -- copiar bloques
ADDN    -- sumar numéricos, con la precisión declarada
```

**Las instrucciones de la MI conocen los tipos de datos de alto nivel** —decimales empaquetados,
cadenas con longitud, punteros a objetos con autoridad— porque se diseñaron para el software de
gestión.

Y lo que la distingue de la JVM y del p-code es el momento de la traducción: **la MI se traduce a
código nativo al instalar o al primer uso, y el resultado se guarda dentro del objeto programa**.

| | JVM | p-code UCSD | **MI de IBM i** |
|---|---|---|---|
| Momento | JIT, en ejecución | interpretado | **al instalar** |
| Calentamiento | sí | — | **no** |
| Se guarda | no | — | **sí, en el objeto** |
| Sobrevivió a cambio de CPU | — | — | **sí, en 1995** |

Ese modelo es lo que hoy se persigue con **las imágenes nativas de GraalVM** y **el AOT de .NET**: la
portabilidad del bytecode sin el coste de calentamiento.

Y hay una consecuencia de la MI que va más allá del rendimiento y que define la plataforma: **los
punteros de IBM i son punteros con capacidades**, de 128 bits, gestionados por el sistema. **Un
programa no puede fabricar un puntero**: solo puede recibirlos del sistema, que comprueba la autoridad.

Eso hace que **el desbordamiento de búfer clásico sea imposible en el código MI**, y es una de las
razones por las que IBM i tiene un historial de seguridad notablemente bueno.

Es seguridad de memoria impuesta por la arquitectura, en 1978 — el problema que hoy se intenta
resolver con Rust y con CHERI.
"""),
        "pli": ("""
 maqpila: procedure options(main);

    declare pila(20) fixed binary(31);
    declare tope fixed binary(31) initial(0);
    declare linea char(80) varying;
    declare op char(1);
    declare (a, b, x, y, p1, p2) fixed binary(31);

    get edit (linea) (a(80));
    linea = trim(linea);

    p1 = index(linea, ' ');
    a  = substr(linea, 1, p1 - 1);
    p2 = index(substr(linea, p1 + 1), ' ') + p1;
    b  = substr(linea, p1 + 1, p2 - p1 - 1);
    op = substr(linea, p2 + 1, 1);

    tope = tope + 1;  pila(tope) = a;       /* PUSH */
    tope = tope + 1;  pila(tope) = b;        /* PUSH */

    y = pila(tope);  tope = tope - 1;         /* POP */
    x = pila(tope);  tope = tope - 1;          /* POP */

    select (op);
       when ('+') x = x + y;
       when ('-') x = x - y;
       when ('*') x = x * y;
       otherwise  x = 0;
    end;

    tope = tope + 1;  pila(tope) = x;

    put skip list ('resultado=' || trim(char(pila(tope))));

 end maqpila;
""", """
**Lo que esta clase enseña en PL/I.** PL/I compila a nativo y **no tiene máquina virtual**, y su
aportación a esta clase es de otro tipo: **PL/I fue el lenguaje del primer sistema operativo escrito
en alto nivel, y ese sistema definió ideas que hoy son universales**.

**Multics** (MIT, Bell Labs y General Electric, 1965-1969) se escribió en **EPL** y después en **PL/I**,
y de él salieron:

- **La memoria virtual segmentada y los ficheros mapeados en memoria.** En Multics, **un fichero se
  accedía como memoria**, sin `read` ni `write`. Es lo que hoy es `mmap`.
- **Los anillos de protección**, que están en el hardware de x86 desde entonces.
- **La jerarquía de directorios con rutas**, las listas de control de acceso y el enlace dinámico.
- **La idea de un sistema operativo como servicio público**, con usuarios simultáneos y facturación.

Y algo que conecta directamente con esta clase: **Multics tenía enlace dinámico de verdad**. Una
llamada a un procedimiento que aún no estaba cargado **provocaba un fallo que el sistema resolvía
buscándolo, cargándolo y enlazándolo en marcha**.

Eso es exactamente lo que hace la JVM al cargar una clase la primera vez, y lo que hacen las
bibliotecas dinámicas — **en 1969, sobre PL/I**.

Y hay una consecuencia irónica y muy conocida: **Unix nació como reacción a Multics**. Ken Thompson y
Dennis Ritchie habían trabajado en el proyecto, lo consideraron demasiado complejo, y escribieron algo
mucho más simple — con C, que es un descendiente lejano de BCPL, que a su vez venía del entorno de
CPL, emparentado con las ideas de Algol y PL/I.

**Multics fracasó comercialmente y sus ideas están en todos los sistemas operativos actuales.** Es el
mismo patrón que la clase 122 señalaba en PL/I: **las ideas se difundieron, el vehículo no**.

Y hay un detalle de seguridad que redondea la historia: **el informe de 1974 sobre la seguridad de
Multics** identificó los desbordamientos de búfer como clase de vulnerabilidad y recomendó lenguajes
con comprobación de límites. Cincuenta años después, seguimos ahí.
"""),
        "mumps": ("""
MAQPILA ; Bytecode y maquinas virtuales -- clase 125
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set op = $piece(linea, " ", 3)
 kill pila
 set tope = 0
 set tope = tope + 1, pila(tope) = a      ; PUSH
 set tope = tope + 1, pila(tope) = b      ; PUSH
 set y = pila(tope), tope = tope - 1      ; POP
 set x = pila(tope), tope = tope - 1      ; POP
 set r = 0
 if op = "+" set r = x + y
 if op = "-" set r = x - y
 if op = "*" set r = x * y
 set tope = tope + 1, pila(tope) = r
 write "resultado=", pila(tope), !
 quit
""", """
**Lo que esta clase enseña en M.** M **no tiene máquina virtual estandarizada**, y cada implementación
hace lo suyo: YottaDB compila a objeto nativo, IRIS a un bytecode propio con caché compartida (clase
124).

Lo que sí tiene M, y encaja perfectamente en esta clase, es **la pila de valores de `new`** (clase
096).

```mumps
 new i, x            ; APILA los valores actuales
 ...
 quit                 ; y los DESAPILA al salir
```

Esa pila es una estructura del intérprete, y **el programa la manipula con un comando del lenguaje**.
Es lo mismo que hace la instrucción de guardar registros de una máquina virtual, expuesto como
sintaxis.

Y hay una construcción de M que es literalmente una máquina virtual y que ya ha aparecido varias
veces: **la indirección** (clase 085).

```mumps
 set codigo = "set r = x + y"
 xecute codigo
```

**`xecute` ejecuta una cadena como código M.** Es `eval`, y en M es una primitiva del estándar de 1977,
no un añadido.

Con `xecute` y `$text` (clase 123), **M puede leer su propio código fuente, transformarlo y
ejecutarlo**. Es la homoiconicidad de Lisp por la vía del texto en lugar de la de las listas — más
frágil y con la misma capacidad.

Y eso tiene un uso real y masivo: **FileMan guarda código M en el diccionario de datos y lo ejecuta con
`xecute`** (clases 113 y 118). Las validaciones, los cálculos y los disparadores son cadenas guardadas
en *globals*.

Es una máquina virtual cuyo bytecode es texto M, cuyo programa está en la base de datos y cuyo
intérprete es el propio sistema.

Y merece cerrar con la advertencia que acompaña a todo esto y que esta parte del curso ha ido
repitiendo: **con `xecute` y la indirección, ningún análisis estático es posible**. Es el precio de la
flexibilidad total, pagado en la moneda de las herramientas.
"""),
        "smalltalk": ("""
| partes a b op pila y x r |

partes := stdin nextLine substrings.
a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.
op := partes at: 3.

pila := OrderedCollection new.
pila addLast: a.                     "PUSH"
pila addLast: b.                      "PUSH"

y := pila removeLast.                  "POP"
x := pila removeLast.                   "POP"

r := op = '+' ifTrue: [ x + y ] ifFalse: [
     op = '-' ifTrue: [ x - y ] ifFalse: [
     op = '*' ifTrue: [ x * y ] ifFalse: [ 0 ] ] ].

pila addLast: r.

Transcript show: 'resultado=', pila last printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk **ejecuta bytecode en una máquina de pila**, y este
programa hace a mano lo que su VM hace en cada expresión.

```smalltalk
(Integer >> #+) symbolic.
```

Eso devuelve el bytecode de un método, y para `x + y` se lee así:

```text
pushTemp: 0        "apilar x"
pushTemp: 1         "apilar y"
send: #+             "enviar el mensaje +"
returnTop             "devolver la cima"
```

**`pushTemp, pushTemp, send`** — la misma forma que la JVM, que Tcl y que este programa. Con una
diferencia que lo cambia todo: **`send` no es una operación aritmética, es un envío de mensaje** que
se resuelve en ejecución buscando el método.

Ahí está la dificultad que Smalltalk tuvo que resolver y que definió la tecnología de las VM
modernas: **si cada `+` es una búsqueda de método, el lenguaje es inaceptablemente lento**.

Las soluciones, en orden histórico, son las de la clase 124:

- **Bytecodes especiales para los mensajes frecuentes** —`+`, `-`, `at:`, `ifTrue:`— que la VM
  reconoce y ejecuta directamente si los operandos son del tipo esperado.
- **Cachés de método** globales, y después **cachés de línea polimórficas** (Self).
- **Compilación adaptativa** con integración especulativa y desoptimización.

Y la especificación del bytecode de Smalltalk-80 se publicó en el ***Blue Book*** (Goldberg y Robson,
1983), **con el código de la propia VM en Smalltalk**. Cualquiera podía implementarla, y mucha gente
lo hizo — es una de las primeras especificaciones de máquina virtual publicadas por completo.

Ese libro es el antepasado directo de la *Java Virtual Machine Specification* de 1997.

Y hay un detalle que resume el sistema entero: **la pila de ejecución de Smalltalk son objetos**
—`MethodContext`, clase 096— así que **la pila de la máquina virtual se puede inspeccionar, guardar y
reanudar desde el propio lenguaje**.

En casi todas las VM, la pila es una estructura interna. En Smalltalk, es un objeto más.
"""),
    },
)
