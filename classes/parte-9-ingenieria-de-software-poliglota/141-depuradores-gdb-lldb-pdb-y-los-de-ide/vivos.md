# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 141

> [⬅️ Volver a la clase 141](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una traza: las sumas acumuladas de 1 a n, unidas por guiones. Es un programa que **se explica a sí
mismo mientras corre**, que es la técnica de depuración más antigua y más usada del mundo. Y esta clase
la pone en su sitio: **`print` no es la alternativa pobre al depurador — es la alternativa correcta
cuando el fallo no se reproduce**, y todos los lenguajes de esta página tienen algo mejor que `print`
para hacerlo.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **depurador como herramienta y sus límites**, y estos lenguajes lo enseñan
> porque cubren los dos extremos. **Ada, C++ y Fortran usan GDB**, el depurador externo que lee símbolos
> y controla el proceso. **Lisp, Smalltalk, Tcl y M llevan el depurador dentro**, escrito en el propio
> lenguaje. **Perl trae el suyo en el intérprete.** Y **COBOL y RPG tienen depuradores del sistema
> operativo**, capaces de entrar en un trabajo ajeno que ya está corriendo.
>
> Y el eje que los separa es el de la clase 138: **si el programa sigue vivo, se dialoga; si no, se hace
> arqueología**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (n >= 1) → stdout: `traza=<sumas acumuladas 1..n unidas por ->`
- **Regla:** `traza[i] = 1 + 2 + ... + i`

| stdin | esperado |
|---|---|
| `3` | `traza=1-3-6` |
| `1` | `traza=1` |
| `4` | `traza=1-3-6-10` |

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
PROGRAM-ID. TRAZA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP.
01  I       PIC S9(9) COMP.
01  ACUM    PIC S9(9) COMP.
01  ED      PIC -(8)9.
01  SALIDA  PIC X(200).
01  POSIC   PIC 9(4) COMP VALUE 1.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE "traza=" TO SALIDA
    MOVE 7 TO POSIC
    MOVE 0 TO ACUM

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE ACUM = ACUM + I
        MOVE ACUM TO ED
        IF I > 1
            MOVE "-" TO SALIDA(POSIC:1)
            COMPUTE POSIC = POSIC + 1
        END-IF
        STRING FUNCTION TRIM(ED) DELIMITED BY SIZE
            INTO SALIDA WITH POINTER POSIC
        END-STRING
    END-PERFORM

    DISPLAY FUNCTION TRIM(SALIDA)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El programa usa `STRING ... WITH POINTER`, que es la forma
idiomática de COBOL de ir concatenando: **`POSIC` avanza sola** conforme se escribe, y es un puntero de
escritura dentro del campo.

Y sobre depuradores, el mundo COBOL tiene dos que merecen conocerse por lo distintos que son de lo
habitual.

**IBM Debug Tool / z/OS Debugger**, el interactivo, con una capacidad que sorprende:

```text
AT ENTRY MIPGM PERFORM
   LIST WS-CLIENTE;
   IF WS-IMPORTE > 10000 THEN GO TO ETIQUETA;
END-PERFORM;
```

**Los puntos de ruptura ejecutan comandos**, incluidos condicionales, listados y **cambios de flujo**.
Es un lenguaje de guion dentro del depurador, y permite instrumentar sin recompilar.

Y hay dos capacidades específicas del mainframe que no tienen equivalente:

**`AT CHANGE`**, que detiene el programa **cuando un campo cambia de valor** — el punto de vigilancia
de datos, resuelto por el sistema:

```text
AT CHANGE WS-SALDO PERFORM LIST WS-SALDO; LIST %LINE; END-PERFORM;
```

**Y CEDF para CICS** (clase 138), que intercepta cada comando de una transacción viva en producción y
**permite modificar los datos antes de que se ejecute**.

Y GnuCOBOL, en el lado libre:

```bash
cobc -x -g -fsource-location prog.cob     # -g: símbolos; y el fuente en el ejecutable
gdb ./prog
```

**`-fsource-location` hace que el ejecutable conserve fichero y línea**, para que un aborto informe de
dónde ocurrió — que es lo que la clase 137 señalaba como la diferencia entre un diagnóstico y un
volcado.

Y merece cerrar con la técnica que sigue siendo la más usada en producción, y que este programa
ilustra: **la traza escrita**. En un lote nocturno **no hay nadie para pulsar "continuar"**, así que lo
que sirve es que el programa deje escrito por dónde pasó.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program traza
   implicit none
   integer :: n, i, acum
   character(len=400) :: salida
   character(len=20)  :: pieza

   read(*, *) n

   salida = 'traza='
   acum = 0

   do i = 1, n
      acum = acum + i
      write(pieza, '(I0)') acum
      if (i > 1) salida = trim(salida) // '-'
      salida = trim(salida) // trim(pieza)
   end do

   write(*, '(A)') trim(salida)
end program traza
```

**Lo que esta clase enseña en Fortran.** El `write(pieza, '(I0)')` del programa es **escritura interna**
(clase 093): escribir a una cadena en lugar de a un fichero, que es el `sprintf` de Fortran y la forma
idiomática de convertir números a texto.

Y sobre depuración, Fortran tiene una particularidad que define su relación con las herramientas: **el
depurador tiene que entender los arreglos**.

```text
(gdb) print matriz
$1 = (( 1, 2, 3) ( 4, 5, 6))
(gdb) print vector(3:7)          # una SECCIÓN
(gdb) print vector(3)@5           # 5 elementos desde el 3
(gdb) ptype matriz                 # tipo, forma y límites
```

**Un depurador que no sabe imprimir un arreglo multidimensional con sus límites es inútil en Fortran**,
y esa es la razón de que el soporte de GDB para Fortran haya recibido tanto trabajo.

Y hay dos problemas de depuración que son específicos de este lenguaje y que merecen conocerse:

**Primero, los arreglos asumidos y los descriptores.** Un arreglo `dimension(:,:)` pasado a un
procedimiento **no es un puntero: es un descriptor** con la dirección, los límites y los saltos. Si el
depurador no lo interpreta, muestra basura. Es lo mismo que la clase 129 explicaba sobre punteros
gordos.

**Y segundo, la depuración de código paralelo**, que en Fortran es la norma:

```bash
mpirun -np 4 xterm -e gdb ./prog          # cuatro depuradores, uno por proceso
mpirun -np 4 ./prog --wait-for-debugger    # y engancharse con gdb -p
```

**Lanzar un depurador por proceso deja de funcionar pasados unos pocos**, y por eso existen TotalView y
Arm DDT (clase 138), que **agrupan los procesos por comportamiento**.

Y hay una técnica de bajo coste que la comunidad usa mucho y que este programa ilustra:

```fortran
if (mi_rango == 0) write(*, *) 'paso', i, 'residuo', residuo
flush(6)                                     ! ¡IMPORTANTE!
```

**`flush` es la parte crítica**: sin él, la salida está en el búfer y **si el programa aborta, se
pierde justo lo que interesa** — el último mensaje antes del fallo.

Es una lección transferible a cualquier lenguaje: **una traza sin vaciado no sirve para diagnosticar un
aborto**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Traza is
   N, Acum : Integer;
   Salida  : Unbounded_String := To_Unbounded_String ("traza=");
begin
   Get (N);
   Acum := 0;

   for I in 1 .. N loop
      Acum := Acum + I;
      if I > 1 then
         Append (Salida, "-");
      end if;
      Append (Salida,
              Ada.Strings.Fixed.Trim (Integer'Image (Acum), Ada.Strings.Both));
   end loop;

   Put_Line (To_String (Salida));
end Traza;
```

**Lo que esta clase enseña en Ada.** El programa usa `Unbounded_String` (clase 093) y `'Image` con
`Trim`, que es la conversión de número a texto idiomática de Ada: **`'Image` de un entero positivo
lleva un espacio delante** —reservado para el signo—, y por eso hay que recortarlo.

Y sobre depuración, Ada tiene la posición coherente con toda su filosofía: **cuando el lenguaje detecta
tanto, el depurador se usa menos** — pero cuando se usa, GDB habla el vocabulario de Ada.

```text
(gdb) print Mi_Registro
$1 = (nombre => "Ana       ", edad => 30, activo => true)
(gdb) print Vector
$2 = (1 => 10, 2 => 20, 3 => 30)
(gdb) print Mi_Enum
$3 = Rojo
(gdb) catch exception Constraint_Error      <-- ¡detener AL LANZARSE!
(gdb) info tasks
(gdb) task 2                                  <-- cambiar de tarea
```

**`catch exception` merece destacarse**: detiene el programa **en el punto donde se lanza la excepción,
antes de que se propague** — con la pila todavía intacta.

Es la diferencia entre ver dónde se capturó y ver dónde se produjo, y en un lenguaje con propagación de
excepciones eso lo es todo.

**Y `info tasks` con `task N`** (clase 138) permite cambiar de tarea y mirar su pila, con el estado en
vocabulario de Ada: *Runnable*, *Waiting on entry call*, *Accept*, *Delay*.

Y la aportación propia de Ada a esta clase es la instrumentación integrada:

```ada
pragma Debug (Poner_Traza ("acum = " & Acum'Image));
```

**`pragma Debug` ejecuta una llamada solo si la compilación tiene `-gnata`.** Es una traza que **no
cuesta nada en producción** y que **el compilador comprueba igualmente** —tipos incluidos— aunque no la
genere.

Es superior a un `#ifdef` de C por eso mismo: **el código de depuración no se pudre**, porque siempre
se compila aunque no se ejecute.

Y `'Image` sobre cualquier tipo (Ada 2022 lo extendió a todos, incluidos registros y arreglos) da una
representación legible sin escribir el formateador:

```ada
Put_Line (Mi_Registro'Image);      --  (NOMBRE => "Ana", EDAD => 30)
```

Es lo que Lisp tiene con `print` y Smalltalk con `printString`, llegado a Ada por la vía de los
atributos.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Traza;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I, Acum: Integer;
  Salida: string;

begin
  Read(N);

  Salida := 'traza=';
  Acum := 0;

  for I := 1 to N do
  begin
    Acum := Acum + I;
    if I > 1 then Salida := Salida + '-';
    Salida := Salida + IntToStr(Acum);
  end;

  WriteLn(Salida);
end.
```

**Lo que esta clase enseña en Pascal.** Pascal tiene el mérito histórico de esta clase, ya adelantado en
la clase 138: **Turbo Pascal integró el depurador en el editor en 1987**.

Antes de eso, depurar era **compilar, ejecutar un depurador aparte, y traducir a mano las direcciones
de memoria a nombres de variable**. Turbo Pascal puso F7, F8 y una ventana de vigilancia **en el mismo
programa donde se escribía el código**, en un ordenador de 640 KB.

Ese modelo —editor, compilador y depurador en uno— es el de todos los IDE actuales, y su influencia es
mayor que la del lenguaje.

Hoy, el ecosistema:

```bash
fpc -g -gl -gw3 prog.pas       # símbolos + números de línea + DWARF 3
gdb ./prog
```

Y en Lazarus, todo eso está integrado con puntos de ruptura condicionales, vigilancia y evaluación de
expresiones.

Y hay dos herramientas del ecosistema que resuelven bien el problema de la clase:

**El registro de excepciones con pila**, que es la solución para el fallo que ocurre en la máquina del
cliente:

```pascal
uses SysUtils;

try
  Procesar;
except
  on E: Exception do
    WriteLn(E.ClassName, ': ', E.Message, LineEnding, BackTraceStrFunc(...));
end;
```

**Y `heaptrc`** (clase 138), con `-gh`, que informa al terminar de cada bloque no liberado **con la
pila de dónde se reservó**.

Y una técnica propia del mundo Delphi que merece nombrarse porque anticipa la telemetría moderna:
**madExcept** y **EurekaLog** capturan cualquier excepción no manejada y **componen un informe con la
pila simbolizada, las variables, la versión, el sistema y una captura de pantalla**, listo para
enviar.

Eso resuelve el caso más difícil del cierre de esta clase —**el fallo que ocurre donde no puedes
mirar**— y lo hace por la vía correcta: **no intentando depurar en remoto, sino recogiendo suficiente
contexto para no tener que hacerlo**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read))
      (acum 0)
      (piezas '()))
  (dotimes (i n)
    (incf acum (1+ i))
    (push (format nil "~D" acum) piezas))
  (format t "traza=~{~A~^-~}~%" (nreverse piezas)))
```

**Lo que esta clase enseña en Common Lisp.** El programa usa **`~{~A~^-~}`**, una directiva de `format`
que merece explicarse porque es de las más útiles del lenguaje:

- **`~{ ... ~}`** itera sobre una lista.
- **`~A`** imprime el elemento.
- **`~^`** significa **"si no quedan más elementos, sal aquí"**.

**El resultado es "unir con guiones sin guion final"** — el `join` de otros lenguajes, expresado como
directiva de formato. `format` de Common Lisp es un lenguaje completo dentro del lenguaje, con
iteración, condicionales y recursión.

Y sobre depuración, Lisp tiene lo que la clase 138 detalló, y aquí conviene añadir la herramienta más
característica para el problema concreto de esta clase —**seguir la ejecución**:

```lisp
(trace factorial)
(factorial 4)
  0: (FACTORIAL 4)
    1: (FACTORIAL 3)
      2: (FACTORIAL 2)
        3: (FACTORIAL 1)
        3: FACTORIAL returned 1
      2: FACTORIAL returned 2
    1: FACTORIAL returned 6
  0: FACTORIAL returned 24
```

**`trace` da exactamente lo que este programa construye a mano**, y sin tocar el código: **la traza
completa de llamadas con indentación por profundidad y el valor de retorno de cada una**.

Y admite condiciones:

```lisp
(trace factorial :break t)                    ; entrar al depurador en cada llamada
(trace foo :condition (> (car args) 100))      ; solo si el argumento pasa de 100
(trace foo :report :graph)
```

**Poder activar la traza sobre una función ya cargada, con una condición, sin recompilar y sin haberlo
previsto** es la ventaja concreta del modelo de la Parte 8.

Y merece cerrar con `step` y `inspect`:

```lisp
(step (factorial 4))       ; ejecución paso a paso por FORMAS, no por líneas
(inspect *objeto*)          ; inspector interactivo y navegable
(describe 'factorial)        ; su definición, argumentos, documentación y tipo
```

**`step` avanza por formas**, no por líneas de texto, que es lo coherente en un lenguaje donde el
programa es un árbol (clase 123) — y es más preciso que una línea, porque una línea puede contener
varias formas anidadas.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set acum 0
set piezas {}
for {set i 1} {$i <= $n} {incr i} {
    incr acum $i
    lappend piezas $acum
}

puts "traza=[join $piezas -]"
```

**Lo que esta clase enseña en Tcl.** `join $piezas -` resuelve en un comando lo que otros lenguajes de
esta página construyen a mano, y es coherente con la clase 090: **en Tcl toda lista sabe unirse**.

Y sobre depuración, Tcl tiene el mecanismo más elegante de esta página para el problema concreto de la
clase, y ya apareció en la clase 138: **`trace add execution`**.

```tcl
proc calcular {n} { ... }

trace add execution calcular enter {apply {{cmd op} {
    puts "-> $cmd"
}}}
trace add execution calcular leave {apply {{cmd code res op} {
    puts "<- $res"
}}}
```

**Eso produce la traza de llamadas de `trace` de Lisp**, con dos comandos y sin tocar el procedimiento.

Y **`enterstep`** va más allá que cualquier otro lenguaje de esta página:

```tcl
trace add execution calcular enterstep {apply {{cmd op} { puts "  $cmd" }}}
```

**Imprime CADA comando que se ejecuta dentro del procedimiento**, con sus argumentos ya sustituidos. Es
un `set -x` de shell aplicado a un procedimiento concreto, activable en marcha.

Y para el problema clásico —**"¿quién cambió esta variable?"**—:

```tcl
trace add variable ::config write {apply {{n1 n2 op} {
    puts "config cambió a $::config desde [info level -1]"
}}}
```

**`info level -1` da la llamada del llamante**, así que el mensaje dice **quién** hizo el cambio, no
solo que se hizo.

Eso responde en tres líneas a lo que en C++ requiere un punto de vigilancia de hardware (clase 138) y
en la mayoría de los lenguajes no tiene respuesta directa.

Y el ecosistema completa el cuadro:

| Herramienta | Qué hace |
|---|---|
| **TclDebugger** | depurador gráfico con puntos de ruptura |
| **tclsh + `-errorinfo`** | la pila con el texto de cada comando (clase 137) |
| **nagelfar** | análisis estático |
| **`coroprobe`** (8.7) | inspeccionar una corrutina suspendida |
| **tkcon** | consola interactiva sobre una aplicación en marcha |

**tkcon** merece la mención final: **se puede inyectar en una aplicación Tk en ejecución** y da una
consola sobre ella, con acceso a todas sus variables y procedimientos.

Es el `swank` de Lisp de la clase 138: **una puerta al programa vivo**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my ($acum, @piezas) = (0);
for my $i (1 .. $n) {
    $acum += $i;
    push @piezas, $acum;
}

print "traza=", join('-', @piezas), "\n";
```

**Lo que esta clase enseña en Perl.** Perl trae **un depurador completo en el intérprete**, sin instalar
nada y en cualquier máquina donde haya Perl — que durante veinte años fue todas.

```bash
perl -d prog.pl
```

Los comandos que conviene conocer:

```text
n / s          siguiente línea / entrar en la función
c 42            continuar hasta la línea 42
b 15 $x > 100    punto de ruptura CONDICIONAL
w $variable       vigilar: parar cuando cambie
x $estructura      volcar una estructura anidada
T                   la pila
r                    ejecutar hasta salir de la función
R                     reiniciar
|m $objeto             los métodos disponibles, paginados
```

**`x` es el comando central**, y hace lo que `Data::Dumper` pero interactivamente y con profundidad
controlable: `x 2 $estructura` limita a dos niveles.

Y el depurador de Perl tiene una propiedad poco conocida que ilustra bien la filosofía del lenguaje:
**está escrito en Perl**, en el fichero `perl5db.pl`, y **se puede sustituir por otro**.

De ahí toda la familia `Devel::`:

```bash
perl -d:NYTProf prog.pl      # el perfilador de referencia
perl -d:Trace prog.pl         # traza de cada línea ejecutada
perl -d:ptkdb prog.pl          # depurador gráfico en Tk
```

**Todos usan el mismo gancho**: `-d:Foo` carga `Devel::Foo` como depurador, y el intérprete le entrega
el control en cada sentencia.

Es una arquitectura de complementos para la depuración, y es la razón de que Perl tenga un perfilador
tan bueno sin que el intérprete tenga que soportarlo específicamente.

Y para el caso del cierre de esta clase —**el fallo que no se puede depurar en vivo**—:

```perl
use Carp;
$SIG{__DIE__} = sub { Carp::confess(@_) };     # cualquier muerte, CON pila
$SIG{ALRM}   = sub { Carp::cluck("colgado") }; # y un aviso con pila si se cuelga
alarm 30;
```

**Convertir toda muerte en una muerte con pila completa** es una línea, y es lo primero que conviene
poner en un programa que va a correr sin supervisión.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::string salida = "traza=";
    long long acum = 0;

    for (long long i = 1; i <= n; ++i) {
        acum += i;
        if (i > 1) salida += '-';
        salida += std::to_string(acum);
    }

    std::cout << salida << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene el depurador más potente de esta página y el más
laborioso de usar, y esta clase es el sitio para las técnicas que de verdad rinden.

**Puntos de ruptura condicionales y con acción**, para no parar mil veces:

```text
(gdb) break procesar if id == 4711
(gdb) break archivo.cpp:42
(gdb) commands
> print estado
> continue
> end
```

**Ese `commands` con `continue` es un `printf` sin recompilar**: imprime y sigue, tantas veces como
haga falta, sobre un binario que ya existe.

**Puntos de vigilancia de hardware**, para "¿quién escribió aquí?":

```text
(gdb) watch *ptr
(gdb) rwatch variable       # cuando se LEE
(gdb) awatch variable        # lectura o escritura
```

El procesador tiene registros de depuración —cuatro en x86— que **detienen la ejecución en el acceso**,
sin coste. Es la respuesta a la corrupción de memoria, y es lo que Tcl hace con `trace add variable`
por software.

**La pila y los marcos**:

```text
(gdb) bt              # la pila
(gdb) frame 3          # subir al marco 3
(gdb) info locals       # sus variables (clase 127)
(gdb) finish             # ejecutar hasta volver
```

**Impresión bonita de la biblioteca estándar**, que hay que activar y que cambia la experiencia:

```text
(gdb) print v
$1 = std::vector of length 3, capacity 4 = {10, 20, 30}
```

Sin los *pretty printers* de GCC, eso se ve como tres punteros. **Es lo primero que hay que comprobar
al montar un entorno de C++.**

Y **rr**, que merece cerrar porque cambia lo que se puede preguntar:

```bash
rr record ./prog
rr replay
(gdb) watch -l saldo
(gdb) reverse-continue      # hacia ATRÁS hasta la última escritura
```

**Grabar una ejecución y recorrerla hacia atrás desde el fallo hasta la causa.** Con carreras
incluidas, porque `rr` serializa los hilos y **reproduce exactamente la misma intercalación**.

Es la respuesta más directa al cierre de esta clase: **convierte un fallo intermitente en un fallo
determinista**, y a partir de ahí es un problema normal.

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

dcl-pi TRAZA;
  n int(10) const;
end-pi;

dcl-s i     int(10);
dcl-s acum  int(10);
dcl-s salida varchar(200);

salida = 'traza=';
acum = 0;

for i = 1 to n;
  acum += i;
  if i > 1;
    salida += '-';
  endif;
  salida += %char(acum);
endfor;

dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** IBM i tiene, para esta clase, una capacidad que ningún otro sistema
de esta página iguala: **se puede depurar un trabajo ajeno que ya está corriendo, sin haberlo previsto**
(clase 138).

```text
STRSRVJOB JOB(123456/USUARIO/OTROTRABAJO)     <-- "servir" otro trabajo
STRDBG PGM(MIBIB/MIPGM) UPDPROD(*YES)
BREAK 42                                        <-- punto de ruptura
```

**Ese trabajo puede ser una sesión de un usuario que está reportando un problema en ese momento, o un
lote nocturno a mitad de proceso.** No hay que reiniciarlo, ni configurarlo, ni compilarlo distinto.

Y funciona sin tener el fuente en la máquina, porque **la vista de depuración se guarda dentro del
objeto programa**:

```text
CRTBNDRPG PGM(MIPGM) DBGVIEW(*ALL)
```

`DBGVIEW(*SOURCE)` guarda el fuente original; `*LIST` guarda el listado con las copias expandidas;
`*ALL`, todo. **El objeto lleva su propio código dentro**, y por eso se puede depurar un programa de
hace quince años cuyo fuente se perdió.

Es una decisión de diseño de plataforma que resuelve el problema más frecuente del mantenimiento de
legado, y merece pensarse: **el ejecutable como contenedor de su propia información de depuración** es
lo que hoy hacen los formatos con símbolos embebidos, y aquí es de 1988.

Y el resto del arsenal:

| Herramienta | Qué hace |
|---|---|
| **`STRDBG` / `STRISDB`** | depurador de sistema, con `EVAL`, `WATCH` y `STEP` |
| **`WATCH`** | punto de vigilancia sobre una variable o dirección |
| **`DSPJOBLOG`** | el registro completo con pila (clase 138) |
| **`QSYS2.STACK_INFO`** | la pila de cualquier trabajo, **por SQL** |
| **RDi / Code4i** | depuración gráfica desde Eclipse o VS Code |
| **`dsply`** | el `print` de RPG, que este programa usa |

Y merece cerrar señalando lo que esto significa para el cierre de la clase: **en IBM i la distinción
entre "depurar en vivo" y "hacer arqueología" casi desaparece**, porque el trabajo sigue vivo y el
registro conserva la historia.

Es la excepción de esta página, y viene de una decisión de plataforma, no de lenguaje.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 traza: procedure options(main);

    declare n         fixed binary(31);
    declare i         fixed binary(31);
    declare acum      fixed binary(31) initial(0);
    declare salida    char(200) varying initial('traza=');

    get list (n);

    do i = 1 to n;
       acum = acum + i;
       if i > 1 then
          salida = salida || '-';
       salida = salida || trim(char(acum));
    end;

    put skip list (salida);

 end traza;
```

**Lo que esta clase enseña en PL/I.** PL/I trae la instrumentación **en el lenguaje**, con un mecanismo
que ningún otro de esta página tiene igual: **las condiciones de depuración `CHECK` y `SUBSCRIPTRANGE`
activadas por prefijo**.

```pli
 (check(acum, i)):
 calcular: procedure;
    ...
 end calcular;

 on check(acum) put skip list ('acum ahora vale', acum);
```

**`CHECK` dispara un manejador cada vez que una variable cambia de valor.** Es el punto de vigilancia de
datos —el `watch` de GDB, el `AT CHANGE` de COBOL, el `trace add variable` de Tcl— **integrado en el
lenguaje y activable por ámbito con un prefijo**.

Y como es una condición normal, el manejador es código PL/I: puede imprimir, contar, comparar o abortar.

Es de 1964, y es una idea que la mayoría de los lenguajes modernos delegan por completo en herramientas
externas.

El resto del repertorio de esta clase:

```pli
 put data;                        /* volcar TODAS las variables (clase 138) */
 on error snap put data;           /* al fallar: pila + volcado */
 put skip list ('en ' || onloc()); /* dónde estamos */
```

**`snap` imprime la traza de la pila**, y `onloc()` da el nombre del procedimiento donde ocurrió la
condición.

Y para depuración interactiva, el mundo z/OS usa el mismo **z/OS Debugger** que COBOL en esta página,
con las mismas capacidades: puntos de ruptura con guion, `AT CHANGE` y depuración de programas en
ejecución.

Y merece cerrar con la observación que atraviesa la columna de la izquierda de esta página: **COBOL,
PL/I y Fortran resolvieron la depuración con instrumentación declarada en el propio programa**, porque
en su época **no había una consola donde sentarse a mirar**.

La consecuencia es que su instrumentación **sobrevive al despliegue**: está en el código, se activa con
una opción de compilación, y funciona igual en producción que en desarrollo.

Es exactamente lo que la observabilidad moderna redescubrió cincuenta años después, y que la clase 142
desarrolla.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
TRAZA ; Traza acumulada -- clase 141
 read n
 new i, acum, salida
 set acum = 0, salida = "traza="
 for i = 1:1:n do
 . set acum = acum + i
 . if i > 1 set salida = salida _ "-"
 . set salida = salida _ acum
 write salida, !
 quit
```

**Lo que esta clase enseña en M.** El programa usa `_` para concatenar —el operador de concatenación de
M— y el bucle `for i = 1:1:n` con el punto de anidamiento, que son los idiomas del lenguaje (clases 083
y 090).

Y sobre depuración, M tiene la propiedad que la clase 138 detalló y que aquí conviene aplicar al
problema concreto de esta clase: **el código es texto accesible en ejecución**, así que **una traza
puede imprimir el propio código**.

```mumps
 set $etrap = "do TRAZA^ERRLOG"
 ...
TRAZA ;
 new i
 for i = $stack(-1):-1:1 do
 . write $stack(i, "PLACE"), "  ", $stack(i, "MCODE"), !
 quit
```

**Ese bucle imprime la pila con el código fuente de cada nivel**, sin depurador, sin símbolos y sin
haber compilado de forma especial.

Y el depurador interactivo del entorno, con las extensiones `$Z`:

```mumps
 zbreak procesar^MIRUT             ; punto de ruptura
 zbreak procesar^MIRUT:"n>100"      ; condicional
 zstep into / zstep over / zstep outof
 zshow "V"                            ; todas las variables locales
 zshow "S"                             ; la pila
 zwrite                                  ; volcado del espacio de variables
```

**`zwrite` sin argumentos vuelca todas las variables locales con todos sus subíndices**, que en M —donde
una variable local puede ser un árbol entero (clase 099)— es mucha información en un comando.

Y merece cerrar con la capacidad que se deriva del modelo de datos y que resuelve el caso difícil del
cierre de la clase:

```mumps
 set ^LOG($job, $horolog, $increment(^LOG("N"))) = "paso " _ i _ " acum " _ acum
```

**Escribir la traza a una global es escribirla a la base de datos**: es persistente, transaccional,
indexada por trabajo y por tiempo, **y consultable desde otro proceso mientras el programa sigue
corriendo**.

Eso es exactamente lo que un sistema de registro estructurado moderno hace con mucha más maquinaria, y
en M **es una asignación**.

Es la ventaja de tener la base de datos dentro del lenguaje, y la clase 142 la retoma.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n acum piezas |

n := stdin nextLine trimBoth asNumber.

acum := 0.
piezas := OrderedCollection new.

1 to: n do: [ :i |
    acum := acum + i.
    piezas add: acum printString ].

Transcript show: 'traza=', (piezas inject: '' into: [ :a :b |
    a isEmpty ifTrue: [ b ] ifFalse: [ a, '-', b ] ]); cr.
```

**Lo que esta clase enseña en Smalltalk.** El programa une con `inject:into:` —el pliegue de la clase
115— porque en Smalltalk incluso unir cadenas es un mensaje sobre una colección.

Y sobre depuración, aquí está el extremo de esta página y lo que la clase 138 ya adelantó: **el
depurador de Smalltalk no controla un proceso desde fuera; ES parte del sistema, escrito en Smalltalk,
y opera sobre objetos vivos**.

Las consecuencias que importan para esta clase:

**Primera, `halt` en cualquier sitio, sin recompilar el mundo:**

```smalltalk
Calculadora >> sumar: a con: b
    self halt.               "abre el depurador AQUÍ"
    ^ a + b
```

Aceptar ese método recompila solo ese método (clase 124), en milisegundos, con el sistema corriendo.

**Segunda, el depurador se puede abrir sin que haya error:**

```smalltalk
[ self calcular ] fork.                       "en otro proceso"
Processor activeProcess suspend.               "y mirarlo"
thisContext                                     "el marco actual como OBJETO"
```

**Tercera, y es la que no tiene equivalente: se puede modificar el programa y continuar.** Escribir el
método que falta, corregir el que está mal, cambiar el valor de una variable, **volver a un marco
anterior de la pila y reejecutar desde ahí**.

```text
[Proceed] [Restart] [Into] [Over] [Through] [Full Stack] [Where is?]
```

**`Restart` reinicia el marco seleccionado** — no el programa: **ese marco**, con el método ya
corregido.

Y cuarta, para el caso difícil del cierre de esta clase: **la depuración remota**. Como el depurador es
un objeto y la pila es un objeto, **se pueden serializar y enviar**:

```smalltalk
"En producción: capturar el contexto del error y mandarlo"
[ self procesar ] on: Error do: [ :e |
    self enviarInforme: e signalerContext copy ]
```

**Lo que viaja no es un texto con la pila: es la pila**, con sus objetos, y se puede **abrir en el
depurador en la máquina del desarrollador**.

Es la conclusión de esta clase llevada al límite: **cuando todo es un objeto, el estado de un fallo es
un dato que se puede guardar, enviar y volver a examinar** — y la distinción entre depurar en vivo y
hacer arqueología deja de existir.

---

## Y de vuelta a la clase

Lo transferible: **el depurador responde "¿qué está pasando ahora?", y esa no siempre es la pregunta**.
Para un fallo que ocurre una vez de cada mil, o de madrugada, o en la máquina de un cliente, la
pregunta es "¿qué pasó?", y para esa sirven los registros, las trazas y la grabación reversible. La
habilidad que hay que desarrollar no es manejar un depurador: es **decidir rápido de qué tipo es el
fallo**, porque eso determina la herramienta y el 90 % del tiempo que costará.

⏮️ [Volver a la clase 141](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
