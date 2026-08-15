# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 123

> [⬅️ Volver a la clase 123](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un intérprete mínimo: leer `3 + 4`, reconocerlo y evaluarlo. Escribirlo obliga a hacer a mano lo que
un compilador hace por ti, y estos lenguajes tienen las cadenas de compilación más elaboradas —y más
distintas— de esta página: **COBOL pasa por un precompilador, un compilador y un editor de enlaces
antes de existir; Ada tiene una fase que nadie más tiene, el *binder*; y Pascal se hizo famoso por
compilar en UNA sola pasada**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto son las **fases: análisis léxico, sintáctico, semántico, generación y enlace**, y
> estos lenguajes las enseñan porque en ellos **están separadas y son visibles**. En un lenguaje moderno
> se escribe un comando y aparece un ejecutable; aquí cada fase es un programa distinto, con su
> entrada, su salida y sus mensajes de error — y eso hace que se entiendan.
>
> Y aportan dos casos límite: **Pascal, diseñado a propósito para compilar en una pasada** —de ahí que
> las declaraciones vayan antes que el código y que Turbo Pascal fuera legendariamente rápido—, y
> **Ada, cuyo `binder` calcula el orden de inicialización de los paquetes** porque hacerlo mal es un
> fallo en ejecución.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a op b` (dos enteros y un operador +, -, *) → stdout: `resultado=<a op b>`
- **Regla:** `aplicar el operador a los dos operandos`

| stdin | esperado |
|---|---|
| `3 + 4` | `resultado=7` |
| `10 - 2` | `resultado=8` |
| `5 * 6` | `resultado=30` |

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
PROGRAM-ID. EVALUA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  T1      PIC X(20).
01  TOP     PIC X(20).
01  T2      PIC X(20).
01  A       PIC S9(9)  COMP-3.
01  B       PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO T1 TOP T2

    COMPUTE A = FUNCTION NUMVAL(T1)
    COMPUTE B = FUNCTION NUMVAL(T2)

    EVALUATE FUNCTION TRIM(TOP)
        WHEN "+"  COMPUTE R = A + B
        WHEN "-"  COMPUTE R = A - B
        WHEN "*"  COMPUTE R = A * B
        WHEN OTHER MOVE 0 TO R
    END-EVALUATE

    MOVE R TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** La cadena de compilación de COBOL en z/OS es la más larga de
esta página, y **cada fase es un programa distinto con su propio nombre y sus propios mensajes**:

```text
FUENTE
  → librarian: expande COPY                     (clase 088)
  → precompilador DB2: sustituye EXEC SQL       (clase 117)
  → traductor CICS: sustituye EXEC CICS         (clase 119)
  → COMPILADOR: produce un OBJETO
  → BINDER / editor de enlaces: produce un MÓDULO DE CARGA
  → y aparte: BIND del plan de DB2
```

Y esa lista explica cosas que de otro modo desconciertan:

- **Los números de línea de los errores no coinciden con el fuente**, porque el precompilador ha
  insertado código. Por eso los compiladores emiten un listado con el fuente expandido.
- **Un cambio en un copybook obliga a recompilar todo lo que lo use** (clase 088) — y hace falta una
  herramienta que sepa quién usa qué.
- **El `BIND` de DB2 es una fase aparte**: se compila el programa y **después** se "vincula" el plan de
  acceso a la base de datos, que es donde el optimizador decide los índices. Cambiar las estadísticas
  de una tabla y volver a hacer `BIND` **cambia el rendimiento sin tocar el programa**.

Y hay una decisión que define el ecosistema: **la unidad de enlace es el módulo de carga**, y el `CALL`
puede ser estático —resuelto por el editor de enlaces— o dinámico —resuelto al ejecutar (clase 085)—.

Esa elección es de arquitectura: con `CALL` dinámico, **corregir un subprograma no obliga a
reenlazar a sus miles de llamadores**. Es lo mismo que una biblioteca compartida, decidido llamada a
llamada.

Y una anécdota que explica la sintaxis del lenguaje: **COBOL se diseñó para compiladores de una
pasada en máquinas con memoria mínima**. De ahí las divisiones en orden fijo —identificación, entorno,
datos, procedimiento—: **cuando el compilador llega al código, ya conoce todos los datos**. La
estructura del lenguaje es la estructura del compilador de 1959.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program evalua
   implicit none
   character(len=200) :: linea
   character(len=1)   :: op
   integer :: a, b, r, p1

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(trim(linea), ' ')
   read(linea(1:p1-1), *) a
   op = linea(p1+1:p1+1)
   read(linea(p1+2:), *) b

   select case (op)
   case ('+');  r = a + b
   case ('-');  r = a - b
   case ('*');  r = a * b
   case default; r = 0
   end select

   write(*, '(A,I0)') 'resultado=', r
end program evalua
```

**Lo que esta clase enseña en Fortran.** La compilación de Fortran tiene una particularidad que ningún
otro lenguaje de esta página comparte y que domina la vida de cualquier proyecto grande: **el orden
de compilación importa**.

```bash
gfortran -c utiles.f90       # produce utiles.o Y utiles.mod
gfortran -c principal.f90    # NECESITA utiles.mod para compilar
gfortran utiles.o principal.o -o programa
```

**El fichero `.mod`** contiene la interfaz del módulo ya analizada —tipos, firmas, parámetros— y
**quien haga `use utiles` no compila hasta que exista**. Es lo mismo que la especificación de Ada, con
la diferencia de que **el `.mod` lo genera el compilador y su formato es propio de cada compilador y
de cada versión**.

Eso tiene tres consecuencias prácticas que sorprenden:

1. **Un `.mod` de gfortran no sirve para ifort**, ni siquiera entre versiones distintas de gfortran.
   **No hay ABI de módulos portable**, así que hay que recompilar todo con el mismo compilador.
2. **Calcular el orden de compilación de un proyecto con cientos de módulos es un problema real**, y
   de ahí `makedepf90` y las herramientas que analizan las dependencias.
3. **Cambiar una línea de un módulo obliga a recompilar todo lo que lo use**, en cascada.

Ese es el problema que **`fpm`** (clase 088) resolvió por fin en 2020: deduce el grafo, ordena y
compila.

Y Fortran tiene una fase que casi nadie ve y que es de las más avanzadas del mundo: **la
optimización**. Los compiladores de Fortran llevan sesenta años compitiendo en generar el código
numérico más rápido, y de ahí salen técnicas que después se aplicaron a todo: desenrollado de bucles,
intercambio de bucles, división en bloques para la caché, vectorización automática, análisis de
dependencias.

Y ahí está la razón de fondo de por qué Fortran sigue ganando en cálculo: **su modelo de aliasing es
más estricto que el de C**. Dos argumentos de una subrutina Fortran **no pueden solaparse** salvo que
se declare; en C, cualquier par de punteros puede apuntar al mismo sitio, y el compilador tiene que
suponer lo peor.

Es la característica que en C se pide con `restrict` y que en Fortran es el comportamiento por
defecto desde 1957.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Evalua is
   Linea  : String (1 .. 200);
   Ultimo : Natural;
   Pos    : Integer := 1;
   A, B   : Integer;
   Fin    : Positive;
   Op     : Character := ' ';
   R      : Integer := 0;
begin
   Get_Line (Linea, Ultimo);

   Get (Linea (Pos .. Ultimo), A, Fin);
   Pos := Fin + 1;

   while Pos <= Ultimo and then Linea (Pos) = ' ' loop
      Pos := Pos + 1;
   end loop;
   Op  := Linea (Pos);
   Pos := Pos + 1;

   Get (Linea (Pos .. Ultimo), B, Fin);

   case Op is
      when '+'    => R := A + B;
      when '-'    => R := A - B;
      when '*'    => R := A * B;
      when others => R := 0;
   end case;

   Put ("resultado=");
   Put (R, Width => 1);
   New_Line;
end Evalua;
```

**Lo que esta clase enseña en Ada.** Ada tiene **una fase que ningún otro lenguaje de esta página
tiene**, y merece conocerla: **el *binder***.

```bash
gcc -c programa.adb        # 1. COMPILAR
gnatbind programa.ali       # 2. BIND  <-- esta fase es propia de Ada
gnatlink programa.ali        # 3. ENLAZAR
# o todo junto:  gnatmake programa.adb
```

¿Qué hace el `binder`? Dos cosas que el enlazador de C no puede hacer:

**Primera: comprobar la consistencia entre unidades.** Ada exige que **todas las unidades del programa
se hayan compilado contra las mismas versiones de sus especificaciones**. Si se cambia un paquete y no
se recompila un cliente, **el binder lo detecta y falla**. En C, ese mismo caso enlaza y produce
corrupción de memoria (clase 088).

**Segunda, y es la interesante: calcular el ORDEN DE ELABORACIÓN.**

```ada
package Config is
   Tabla : constant Vector := Cargar_Tabla;    --  esto se EJECUTA al arrancar
end Config;
```

Los paquetes de Ada pueden tener código de inicialización, y **el orden en que se ejecutan importa**:
si `A` usa un valor que `B` inicializa, `B` tiene que elaborarse antes.

El `binder` **calcula ese orden analizando las dependencias**, y si hay un ciclo o una ambigüedad, lo
declara. Y el programador puede exigir garantías:

```ada
pragma Elaborate_All (Config);      --  elabora Config y todo lo suyo antes
pragma Preelaborate;                 --  este paquete NO tiene código de inicio
pragma Pure;                          --  además, no tiene estado
```

Ese problema es real en todos los lenguajes y casi ninguno lo resuelve: en C++ es el célebre **fiasco
del orden de inicialización estática**, donde dos objetos globales en ficheros distintos se
inicializan en un orden que el estándar no define, y el programa falla dependiendo de cómo se enlace.

**Ada lo detecta en la fase de bind. C++ lleva cuarenta años recomendando idiomas para esquivarlo.**

Y `gnatmake` y `gprbuild` cierran el cuadro: **calculan el grafo de dependencias solos** y recompilan
lo justo, como `fpm` en Fortran, y desde mucho antes.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Evalua;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, T1, T2: string;
  P1, P2, A, B, R: Integer;
  Op: Char;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P1 := Pos(' ', Linea);
  T1 := Copy(Linea, 1, P1 - 1);
  Op := Linea[P1 + 1];
  T2 := Trim(Copy(Linea, P1 + 3, Length(Linea)));

  A := StrToInt(T1);
  B := StrToInt(T2);

  case Op of
    '+': R := A + B;
    '-': R := A - B;
    '*': R := A * B;
  else
    R := 0;
  end;

  P2 := 0;                    { silencia el aviso de variable sin usar }
  if P2 = 1 then Exit;

  WriteLn('resultado=', IntToStr(R));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal es **el caso de estudio de esta clase**, porque su
sintaxis está diseñada para una propiedad concreta del compilador: **compilar en UNA SOLA PASADA**.

De ahí salen tres reglas del lenguaje que suelen atribuirse a la manía de Wirth y que son técnicas:

**Las declaraciones van antes del código**, en orden: `const`, `type`, `var`, procedimientos, y después
el cuerpo. Cuando el compilador llega a una expresión, **ya conoce todos los tipos**.

**Todo debe declararse antes de usarse**, de ahí `forward` para la recursión mutua:

```pascal
procedure B(X: Integer); forward;
procedure A(X: Integer); begin B(X) end;
procedure B(X: Integer); begin ... end;
```

**Y las unidades tienen `interface` e `implementation` separadas** (clase 086): compilar un cliente
solo requiere leer la interfaz, ya compilada en un `.ppu`.

Y el resultado fue espectacular: **Turbo Pascal 3.0 (1986) compilaba a velocidades que asombraban** —
miles de líneas por segundo en un PC de 4,77 MHz— y el compilador entero, editor incluido, **cabía en
39 KB**.

Anders Hejlsberg lo escribió en ensamblador y **el compilador no generaba código intermedio**: leía el
fuente y **escribía instrucciones máquina directamente**, sin árbol sintáctico y sin fases separadas.

Esa velocidad cambió cómo se programaba: **el ciclo editar-compilar-probar pasó de minutos a
segundos**, y de ahí salió la idea del entorno integrado que hoy es universal.

El precio es el que se ve en el lenguaje: **sin fases separadas no hay optimización global**. Turbo
Pascal generaba código correcto y no especialmente rápido, y los compiladores modernos —Free Pascal,
Delphi— sí tienen fases y optimizan, a costa de ser más lentos.

Es un compromiso explícito de diseño, y merece recordarlo cuando se critica la rigidez de la sintaxis
de Pascal: **cada una de esas reglas compraba velocidad de compilación en una máquina de 1970**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (op (symbol-name (read)))
       (b (read)))
  (format t "resultado=~D~%"
          (cond ((string= op "+") (+ a b))
                ((string= op "-") (- a b))
                ((string= op "*") (* a b))
                (t 0))))
```

**Lo que esta clase enseña en Common Lisp.** Este programa **no analiza nada**: `(read)` hace el
trabajo. Y ahí está la lección de esta clase en Lisp: **el analizador del lenguaje está disponible
como una función**.

```lisp
(read)                          ; lee UNA expresión de la entrada
(read-from-string "(+ 1 2)")     ; y devuelve una LISTA
(eval (read-from-string "(+ 1 2)"))   ; y la evalúa
```

En cualquier otro lenguaje de esta página, escribir un intérprete exige un analizador léxico y uno
sintáctico. **En Lisp, `read` devuelve directamente el árbol sintáctico**, porque el código **ES** una
estructura de datos (clase 097).

De ahí sale el ciclo de Lisp, que da nombre a algo que hoy usa todo el mundo:

```text
READ → EVAL → PRINT → LOOP     =     REPL
```

**El término REPL viene de aquí**, y las cuatro funciones son funciones normales del estándar que se
pueden llamar por separado.

Y las fases de compilación de Lisp son visibles y controlables como en ningún otro sitio:

```lisp
(compile-file "codigo.lisp")     ; produce un FASL (fast-load file)
(load "codigo.fasl")
(compile 'mi-funcion)             ; compilar UNA función, en marcha
(disassemble 'mi-funcion)          ; ver el CÓDIGO MÁQUINA generado
```

**`disassemble` sobre una función devuelve su ensamblador**, en el sistema vivo. Con eso se puede
comprobar si una declaración de tipo ha servido para algo, y es una herramienta de optimización que
la mayoría de los lenguajes no tiene a mano.

Y hay tres momentos distintos en los que puede ejecutarse código, y Lisp los distingue explícitamente:

```lisp
(eval-when (:compile-toplevel :load-toplevel :execute) ...)
```

**Al compilar, al cargar o al ejecutar** — y las macros (clase 092) se expanden en el primero. Esa
distinción es la que en C hace el preprocesador y en Rust las macros procedurales, y en Lisp está
explícita en una forma especial del estándar.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a op b

switch -exact -- $op {
    "+"     { set r [expr {$a + $b}] }
    "-"     { set r [expr {$a - $b}] }
    "*"     { set r [expr {$a * $b}] }
    default { set r 0 }
}

puts "resultado=$r"
```

**Lo que esta clase enseña en Tcl.** Tcl parece un intérprete puro y **no lo es desde 1997**: Tcl 8.0
introdujo un **compilador a bytecode**, y ese cambio es una de las historias de optimización más
instructivas de esta página.

Antes de 8.0, Tcl **reanalizaba cada comando cada vez que se ejecutaba**. Un bucle de un millón de
vueltas analizaba el cuerpo un millón de veces. Era brutalmente lento, y esa lentitud es la reputación
que el lenguaje arrastró durante años.

Tcl 8.0 compiló los guiones a bytecode para una máquina de pila, y **el rendimiento mejoró entre cinco
y diez veces**. Se puede ver:

```tcl
tcl::unsupported::disassemble proc miProc
```

Y ahí aparece la razón práctica de una regla que se ha repetido en varias clases: **hay que usar
llaves**.

```tcl
while {$i < 10} { ... }      ;# la condición se COMPILA una vez
while "$i < 10" { ... }       ;# se sustituye antes: NO se puede compilar
expr {$a + $b}                 ;# compilado a bytecode
expr $a + $b                    ;# se construye la expresión y se analiza CADA VEZ
```

**Con llaves, el compilador ve el texto literal y genera bytecode; sin ellas, ve una cadena construida
en ejecución y tiene que analizarla.** La diferencia puede ser de un orden de magnitud, y es la
optimización más importante que se puede hacer en Tcl.

Y esa dualidad —**un lenguaje cuya semántica es de sustitución textual, compilado a bytecode**— obliga
al intérprete a hacer algo curioso: **si el guion cambia en ejecución, hay que invalidar el bytecode**.
De ahí que `eval` sobre texto construido siga siendo lento, y que la representación interna de los
valores (clase 090) se guarde y se reutilice.

Tcl mantiene además el analizador expuesto, como Lisp:

```tcl
info complete $texto        ;# ¿es un comando completo? Lo usan los shells
subst $texto                 ;# aplicar las sustituciones sin ejecutar
```

**`info complete`** es lo que permite a un intérprete interactivo saber si debe pedir más líneas, y es
la razón de que los shells de Tcl gestionen bien los comandos multilínea.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a, $op, $b) = split ' ', $linea;

my $r = $op eq '+' ? $a + $b
      : $op eq '-' ? $a - $b
      : $op eq '*' ? $a * $b
      :              0;

print "resultado=$r\n";
```

**Lo que esta clase enseña en Perl.** Perl tiene una arquitectura de compilación peculiar que explica
varias de sus rarezas: **compila el programa entero a un árbol de operaciones —el *optree*— y después
lo ejecuta**.

```bash
perl -c programa.pl              # solo COMPILAR: comprobar la sintaxis
perl -MO=Deparse programa.pl      # descompilar: ver qué entendió Perl
perl -MO=Concise programa.pl       # ver el árbol de operaciones
```

**`-MO=Deparse` es una herramienta excelente y poco conocida**: reescribe el programa tal como Perl lo
ha interpretado, y resuelve de un vistazo las dudas sobre precedencia y sobre qué significa una línea
densa.

Y hay una peculiaridad que hace única la compilación de Perl: **las fases se entremezclan**.

```perl
BEGIN { ... }      # se ejecuta EN CUANTO se compila este bloque
UNITCHECK { ... }
CHECK { ... }       # al terminar la compilación
INIT { ... }         # justo antes de ejecutar
END { ... }           # al terminar el programa
```

**`BEGIN` ejecuta código durante la compilación**, y eso no es un detalle: **`use` es un `BEGIN`**
(clase 086).

```perl
use strict;         # equivale a  BEGIN { require strict; strict->import }
```

Por eso `use strict` afecta al resto del fichero: **se ha ejecutado antes de que se compile lo que
viene después**, y ha cambiado el comportamiento del compilador.

Esa capacidad —**código de usuario que se ejecuta durante la compilación y modifica cómo se compila lo
siguiente**— es lo que permite módulos como `Moose`, `Try::Tiny` y `Future::AsyncAwait` (clase 122),
que añaden sintaxis nueva desde CPAN.

Y también es lo que hace que **analizar Perl sea imposible en general**. Es un resultado conocido:
como un `BEGIN` puede cambiar el analizador —definiendo prototipos, o con `source filters`— **solo Perl
puede analizar Perl**, y hace falta ejecutarlo para saber qué significa. De ahí que las herramientas
de análisis estático de Perl sean aproximaciones.

Es el precio de la extensibilidad total, y está bien documentado por la propia comunidad.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    int a{}, b{};
    std::string op;
    if (!(std::cin >> a >> op >> b)) return 1;

    int r = 0;
    if      (op == "+") r = a + b;
    else if (op == "-") r = a - b;
    else if (op == "*") r = a * b;

    std::cout << "resultado=" << r << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** La cadena de C++ es la que más gente conoce a medias, y sus cuatro
fases se pueden ver por separado:

```bash
g++ -E prog.cpp -o prog.i     # 1. PREPROCESADOR: expande #include y macros
g++ -S prog.i -o prog.s        # 2. COMPILADOR: genera ENSAMBLADOR
as prog.s -o prog.o             # 3. ENSAMBLADOR: genera objeto
g++ prog.o -o prog               # 4. ENLAZADOR
```

**Mirar `prog.i` es instructivo**: un programa de veinte líneas que incluya `<iostream>` se convierte
en **decenas de miles de líneas**. Esa es, medida, la razón de que C++ compile lento y el problema que
los módulos de C++20 resuelven (clase 086).

Y el estándar define además **fases de traducción** con detalles que explican rarezas históricas:

```cpp
??=include <cstdio>      // TRIGRAFOS: ??= era #  (eliminados en C++17)
"cad" "ena"               // concatenación de literales adyacentes: es una FASE
```

C++ tiene además dos reglas de esta clase que son la causa de la mitad de los errores de enlace:

**La regla de una sola definición (ODR)**: una entidad puede declararse muchas veces y **definirse una
sola**. Violarla **no es un error que el compilador tenga que detectar**: es comportamiento indefinido,
y en la práctica produce errores de enlace o —peor— programas que funcionan mal en silencio.

**Y la separación entre declaración y definición**, con `inline`, `extern` y las plantillas, que
**deben estar completas en cada unidad que las use** — de ahí que las plantillas vivan en cabeceras.

Y hay una fase específica de C++ que no existe en C y que domina los tiempos de compilación: **la
instanciación de plantillas**. Cada `std::vector<int>` usado genera código, y el enlazador después
**elimina los duplicados** — de ahí los objetos enormes y los ejecutables que encogen al enlazar.

Sobre la optimización, C++ tiene la fase que el resto de esta página no: **la optimización en tiempo
de enlace**.

```bash
g++ -flto -O2 ...     # LTO: optimizar VIENDO TODO el programa a la vez
```

Con LTO, el compilador puede integrar en línea funciones de otras unidades de traducción. Es lo que
permite que C++ compita con Fortran en código numérico, y cuesta tiempo de compilación.

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

dcl-pi EVALUA;
  entrada char(80) const;
end-pi;

dcl-s texto varchar(80);
dcl-s p1    int(10);
dcl-s p2    int(10);
dcl-s a     int(10);
dcl-s b     int(10);
dcl-s op    char(1);
dcl-s r     int(20) inz(0);

texto = %trim(entrada);
p1 = %scan(' ' : texto);
a  = %int(%subst(texto : 1 : p1 - 1));
op = %subst(texto : p1 + 1 : 1);
p2 = %scan(' ' : texto : p1 + 2);
b  = %int(%subst(texto : p2 + 1 : %len(texto) - p2));

select;
  when op = '+';  r = a + b;
  when op = '-';  r = a - b;
  when op = '*';  r = a * b;
  other;          r = 0;
endsl;

dsply ('resultado=' + %char(r));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** La compilación en IBM i tiene una particularidad que no tiene
ninguna otra plataforma de esta página, y merece explicarla porque es de las cosas más singulares del
sistema: **el código máquina se genera al INSTALAR, no al compilar**.

```text
FUENTE → CRTRPGMOD → *MODULE  (contiene MI: Machine Interface, código INDEPENDIENTE del procesador)
       → CRTPGM    → *PGM     (enlaza módulos y programas de servicio)
       → al ejecutar por primera vez: el SLIC traduce MI a código del procesador
```

**La *Machine Interface* de IBM i es una arquitectura virtual**, diseñada en 1978 para el System/38. Un
programa compilado **no contiene instrucciones del procesador**: contiene MI, y el **SLIC** —la capa
que hay debajo del sistema operativo— lo traduce a código nativo la primera vez y guarda el resultado.

Y eso tiene una consecuencia extraordinaria y comprobada: **cuando IBM cambió de procesador CISC a
PowerPC en 1995, los programas de los clientes siguieron funcionando sin recompilar**. El sistema los
retradujo.

Un programa compilado en 1988 para un AS/400 con procesador propietario **se ejecuta hoy en un Power10
de 64 bits**, sin fuente y sin tocarlo. **No hay ningún otro ecosistema comercial que pueda decir
eso.**

Es la misma idea que el bytecode de la JVM (clase 125), diecisiete años antes y **en el sistema
operativo**.

Las fases visibles al programador son estas:

```text
CRTRPGMOD MODULE(MIBIB/UTILES)              -- compilar a módulo
CRTSRVPGM SRVPGM(MIBIB/UTILES) ...           -- programa de servicio (clase 086)
CRTPGM PGM(MIBIB/MIAPP) MODULE(...) BNDSRVPGM(...)   -- enlazar
CRTBNDRPG PGM(MIBIB/MIAPP)                    -- compilar y enlazar de una vez
```

Y la firma de los programas de servicio (clase 086) es lo que hace de esa cadena un sistema con
versionado de ABI comprobado al cargar.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 evalua: procedure options(main);

    declare linea char(80) varying;
    declare op    char(1);
    declare (a, b, r, p1, p2) fixed binary(31);

    get edit (linea) (a(80));
    linea = trim(linea);

    p1 = index(linea, ' ');
    a  = substr(linea, 1, p1 - 1);
    op = substr(linea, p1 + 1, 1);
    p2 = index(substr(linea, p1 + 2), ' ') + p1 + 1;
    b  = substr(linea, p2 + 1);

    select (op);
       when ('+') r = a + b;
       when ('-') r = a - b;
       when ('*') r = a * b;
       otherwise  r = 0;
    end;

    put skip list ('resultado=' || trim(char(r)));

 end evalua;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte la cadena de z/OS con COBOL —precompilador,
compilador, editor de enlaces— y tiene una fase propia que ya ha aparecido varias veces y que aquí es
el tema: **el preprocesador**.

```pli
 %declare depurar fixed;
 %depurar = 1;

 %do i = 1 to 10;
    campo_&i = 0;
 %end;

 %if depurar = 1 %then %do;
    put skip list ('traza');
 %end;
```

**El preprocesador de PL/I es un lenguaje completo** —con variables, condicionales, bucles y
procedimientos— que se ejecuta en tiempo de compilación y **genera texto fuente**. Es mucho más que
el `#define` de C, y es el antepasado directo de las macros y de la generación de código.

Su uso real es el que cabe esperar: **generar código repetitivo a partir de definiciones**. Un fuente
de quinientas líneas puede compilar cinco mil, y por eso los listados de compilación de PL/I incluyen
el fuente expandido.

Y ahí está el problema que esta clase debe señalar, porque se hereda hasta hoy: **el código que se
depura no es el que se escribió**. Los números de línea de los errores se refieren al texto
generado, las herramientas ven la expansión, y una macro mal escrita produce errores de sintaxis en
un sitio que no existe en el fuente.

Es exactamente lo que se le reprocha al preprocesador de C, que descendió de aquí — y la razón de que
Lisp con sus macros (clase 092) y Rust con las suyas trabajen sobre el **árbol sintáctico** en lugar
de sobre texto: **una macro que manipula estructura no puede producir texto inválido**.

PL/I tiene además una fase que COBOL no tiene y que es propia de su ambición: **el compilador hace un
análisis de flujo de datos bastante avanzado para su época**, y sus mensajes de aviso —variable usada
sin asignar, código inalcanzable, conversión implícita costosa— eran de los mejores de los años
setenta.

El listado de compilación de PL/I con todas las opciones activadas es un documento de decenas de
páginas: tabla de referencias cruzadas, mapa de almacenamiento, código ensamblador generado y
atributos de cada variable. Es la fase de diagnóstico convertida en documentación.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
EVALUA ; Fases de compilacion -- clase 123
 read linea
 set a = $piece(linea, " ", 1)
 set op = $piece(linea, " ", 2)
 set b = $piece(linea, " ", 3)
 set r = 0
 if op = "+" set r = a + b
 if op = "-" set r = a - b
 if op = "*" set r = a * b
 write "resultado=", r, !
 quit
```

**Lo que esta clase enseña en M.** M ocupa el extremo opuesto a COBOL en esta clase: **su modelo de
compilación es el más simple posible, y su código es un dato**.

En las implementaciones tradicionales, **una rutina se guarda en la base de datos**, no en un fichero:

```mumps
 ^ROUTINE("MIRUT", 0, 1) = "MIRUT ; una rutina"
 ^ROUTINE("MIRUT", 0, 2) = " write ""hola"",!"
```

**El fuente vive en un *global***, línea a línea. Y de ahí sale `$text` (clase 111), que **lee el
código fuente de un programa en ejecución**:

```mumps
 write $text(+2^MIRUT)          ; la línea 2 de la rutina MIRUT
 for i=1:1 quit:$text(+i^MIRUT)=""  write $text(+i^MIRUT),!   ; listarla entera
```

Esa capacidad —**el código como dato consultable en marcha**— es lo que hace posibles las herramientas
de VistA: el sistema de parcheo compara versiones leyendo `$text`, los analizadores recorren rutinas y
la documentación se genera del propio código.

Sobre la compilación, las implementaciones modernas **compilan la rutina a código objeto** la primera
vez que se ejecuta o al guardarla:

```text
MIRUT.m   → fuente
MIRUT.o   → objeto compilado (YottaDB)
```

Y el modelo de ejecución es el de la clase 088: **carga perezosa y automática**. No hay fase de
enlace, no hay ejecutable y **corregir una rutina afecta al sistema en la siguiente llamada** — sin
reiniciar y sin recompilar nada más.

Eso explica que los sistemas M lleven años sin reiniciarse y que el despliegue sea copiar una rutina.

Y hay una consecuencia de la indirección (clase 085) que esta clase debe cerrar: **no hay fase de
comprobación que valga**. Como el destino de una llamada se puede construir con texto en ejecución,
**ningún análisis previo puede garantizar que un programa M no falle por llamar a algo que no existe**.

La compilación de M es rápida, simple y no comprueba casi nada. Es coherente con todo lo demás del
lenguaje, y es la razón de que `$text` se use tanto: **si el compilador no puede decirte si algo
existe, pregúntaselo al sistema en marcha**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a op b r |

partes := stdin nextLine substrings.
a := (partes at: 1) asNumber.
op := partes at: 2.
b := (partes at: 3) asNumber.

r := op = '+' ifTrue: [ a + b ] ifFalse: [
     op = '-' ifTrue: [ a - b ] ifFalse: [
     op = '*' ifTrue: [ a * b ] ifFalse: [ 0 ] ] ].

Transcript show: 'resultado=', r printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** En Smalltalk **no hay fase de compilación separada**: se
compila **un método cada vez, al aceptarlo en el navegador**, y el resultado entra inmediatamente en el
sistema vivo (clase 041).

```smalltalk
Compiler evaluate: '3 + 4'.
(Number >> #printString) sourceCode.        "el fuente de un método"
(Number >> #printString) symbolic.           "su BYTECODE"
RBParser parseExpression: '3 + 4'.            "el árbol sintáctico"
```

**El compilador es un objeto del sistema, escrito en Smalltalk**, y se puede llamar, inspeccionar y
sustituir. `Compiler`, `RBParser`, `IRBuilder` y el generador de bytecode son clases normales.

Eso tiene tres consecuencias que definen el entorno:

1. **No hay tiempo de compilación separado del de ejecución.** Compilar un método es enviar un mensaje.
2. **El código fuente vive en la imagen**, junto con el bytecode, así que **cualquier método se puede
   leer y modificar en marcha** — como en M con `$text`, y con un modelo de objetos detrás.
3. **Se puede escribir un compilador nuevo** y hacer que el sistema lo use. Pharo lo ha hecho varias
   veces: el compilador actual, **Opal**, se escribió para exponer las fases intermedias como objetos.

Y el bytecode se ejecuta en una máquina virtual que hoy es notable por otra razón: **Cog**, la VM de
Pharo y Squeak, tiene un **JIT** basado en las técnicas de Self (clase 113) — cachés de línea
polimórficas y compilación adaptativa.

Es la misma tecnología que HotSpot, y por la misma línea genealógica: **Eliot Miranda, autor de Cog,
trabajó en las VM de Self y de Smalltalk comerciales**.

Y para cerrar, una peculiaridad que resume el modelo: **no hay `main`, no hay enlazador y no hay
ejecutable**. Un programa Smalltalk se distribuye como **una imagen**: el estado completo del sistema,
con sus objetos vivos. Ejecutarlo es reanudar donde se quedó.

Es el extremo opuesto a la cadena de COBOL de esta misma clase, y las dos llevan décadas funcionando.

---

## Y de vuelta a la clase

Lo transferible: **cuando algo falla, saber en qué fase falló ahorra la mitad del trabajo**. Un error
de sintaxis es el analizador; uno de tipos, el semántico; un *undefined symbol*, el enlazador; y un
fallo al arrancar, la inicialización. Son cuatro programas distintos con cuatro vocabularios
distintos, y confundirlos lleva a buscar donde no es. La clase 137 vuelve sobre esto con los errores;
aquí basta con quedarse con el mapa.

⏮️ [Volver a la clase 123](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
