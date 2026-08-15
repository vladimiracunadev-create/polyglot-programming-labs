# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 136

> [⬅️ Volver a la clase 136](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Incrementar un contador `n` veces. Con un hilo es trivial; con dos, es el problema más sutil de la
informática concurrente. Y aquí hay un dato que ordena la página: **hasta C++11, ningún lenguaje de
uso general de esta lista tenía un modelo de memoria especificado** — Ada sí, con sus objetos
protegidos, y COBOL, RPG y M lo evitaron **no compartiendo memoria mutable**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **qué ve un hilo de lo que escribe otro**, y estos lenguajes lo enseñan porque
> muestran las dos únicas soluciones que funcionan. **Especificar el modelo**: C++11 lo hizo, y su
> trabajo lo adoptaron C11 y Rust. **O evitar el problema**: Ada con objetos protegidos donde el
> compilador genera la sincronización, y COBOL, RPG y M con procesos aislados y transacciones.
>
> Y el aviso que esta clase debe dar es serio: **una condición de carrera no es un fallo con síntomas —
> es un programa sin significado definido**, y el compilador puede optimizar suponiendo que no ocurre.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (número de incrementos) → stdout: `cuenta=<n>`
- **Regla:** `incrementar un contador n veces, con exclusión`

| stdin | esperado |
|---|---|
| `5` | `cuenta=5` |
| `0` | `cuenta=0` |
| `3` | `cuenta=3` |

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
PROGRAM-ID. CARRERA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(9) COMP.
01  I       PIC 9(9) COMP.
01  CUENTA  PIC 9(9) COMP VALUE 0.
01  ED-C    PIC Z(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        ADD 1 TO CUENTA
    END-PERFORM

    MOVE CUENTA TO ED-C
    DISPLAY "cuenta=" FUNCTION TRIM(ED-C)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene modelo de memoria porque no tiene hilos**, y sus
sistemas concurrentes evitan el problema por construcción: **cada transacción tiene su propia copia de
la `WORKING-STORAGE`** (clase 133).

Y donde sí hay estado compartido —los datos— la disciplina la impone el gestor de recursos:

```cobol
EXEC CICS READ FILE('CONTADOR') RIDFLD(CLAVE) UPDATE END-EXEC
ADD 1 TO CUENTA
EXEC CICS REWRITE FILE('CONTADOR') END-EXEC
EXEC CICS SYNCPOINT END-EXEC
```

**`UPDATE` bloquea el registro hasta el `SYNCPOINT`**, así que la secuencia leer-sumar-escribir es
atómica respecto a las demás transacciones. **Es exactamente la solución del cierre de esta clase:
protegerlo con exclusión**, con el gestor poniendo el bloqueo.

Y hay una construcción de COBOL que esta clase debe nombrar porque es donde sí puede haber carreras:
**el almacenamiento compartido**.

```cobol
01  CONTADOR  PIC 9(9) COMP EXTERNAL.
```

**`EXTERNAL` declara un dato compartido entre todos los programas de una unidad de ejecución**, y en un
entorno con hilos —COBOL for JVM, o CICS con TCB abiertos— **eso es memoria compartida sin
sincronización**.

Es una de las pocas formas de escribir una condición de carrera en COBOL, y es la razón de que las
guías desaconsejen `EXTERNAL` en programas que puedan ejecutarse en varios hilos.

Y merece cerrar con el dato que da la medida de la solución de esta plataforma: **DB2 y CICS ejecutan
millones de operaciones concurrentes sobre los mismos datos sin condiciones de carrera visibles para el
programador**, porque **la unidad de razonamiento es la transacción, no la instrucción**.

Es un nivel de abstracción por encima del modelo de memoria: en lugar de razonar sobre qué ve cada hilo
de cada escritura, se razona sobre **qué ve cada transacción del estado**, con los niveles de
aislamiento de SQL.

Esa abstracción es más fácil de usar correctamente, y es una de las razones por las que los sistemas de
gestión pudieron escalar en concurrencia sin que los programadores fueran expertos en modelos de
memoria.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program carrera
   implicit none
   integer :: n, i, cuenta

   read(*, *) n

   cuenta = 0
   do i = 1, n
      cuenta = cuenta + 1
   end do

   write(*, '(A,I0)') 'cuenta=', cuenta
end program carrera
```

**Lo que esta clase enseña en Fortran.** Fortran tiene un modelo de memoria **desde 2008**, y llegó con
los coarrays (clase 121) porque los necesitaban.

```fortran
integer :: contador[*]
sync all                       ! BARRERA: todo lo anterior es visible para todos
sync images ([2, 3])            ! barrera parcial
critical
   contador[1] = contador[1] + 1     ! SECCIÓN CRÍTICA: solo una imagen a la vez
end critical
```

**`sync all` es la barrera de memoria del lenguaje**: garantiza que todas las escrituras anteriores son
visibles para todas las imágenes.

Y Fortran 2018 añadió las operaciones atómicas, que son lo que esta clase pide:

```fortran
use iso_fortran_env
integer(atomic_int_kind) :: contador[*]

call atomic_add(contador[1], 1)              ! ATÓMICO: sin carrera
call atomic_fetch_add(contador[1], 1, viejo)  ! y devuelve el anterior
call atomic_cas(contador[1], comparar, nuevo, viejo)   ! comparar e intercambiar
```

**`atomic_cas` —comparar e intercambiar— es la primitiva sobre la que se construyen todas las
estructuras sin bloqueo**, y está en el estándar de Fortran desde 2018.

Y dentro de un nodo, con OpenMP, el problema clásico de esta clase aparece exactamente como se espera:

```fortran
!$omp parallel do
do i = 1, n
   cuenta = cuenta + 1        ! ¡CARRERA! varias hebras leen y escriben
end do

!$omp parallel do reduction(+:cuenta)
do i = 1, n
   cuenta = cuenta + 1         ! correcto: cada hebra acumula y se combina al final
end do
```

**`reduction` es la solución del cierre de esta clase por la vía de no compartir**: cada hilo tiene su
copia privada y se combinan al final.

Es la misma idea que los acumuladores por hilo de cualquier marco de trabajo de paralelismo de datos, y
es la razón de que `sum(v)` (clase 114) se pueda paralelizar sin sincronización.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Carrera is
   protected Contador is           --  exclusión mutua GENERADA por el compilador
      procedure Incrementar;
      function Valor return Integer;
   private
      C : Integer := 0;
   end Contador;

   protected body Contador is
      procedure Incrementar is
      begin
         C := C + 1;
      end Incrementar;

      function Valor return Integer is (C);
   end Contador;

   N : Integer;
begin
   Get (N);

   for I in 1 .. N loop
      Contador.Incrementar;         --  seguro aunque lo llamen varias tareas
   end loop;

   Put ("cuenta=");
   Put (Contador.Valor, Width => 1);
   New_Line;
end Carrera;
```

**Lo que esta clase enseña en Ada.** **Ada resolvió esta clase en 1983 sin necesitar un modelo de
memoria explícito**, y merece entender cómo: **eliminando la posibilidad de escribir la carrera**.

```ada
protected Contador is
   procedure Incrementar;     --  acceso EXCLUSIVO: el compilador lo garantiza
   function Valor return Integer;
private
   C : Integer := 0;           --  NADIE puede tocar C desde fuera
end Contador;
```

**El dato está en la parte privada del objeto protegido**, así que **no hay forma de acceder a él sin
pasar por una operación protegida**, y esas operaciones tienen exclusión mutua garantizada por el
runtime.

**La carrera no se evita: se hace inexpresable.** Es la misma filosofía que la clase 116 con los
subtipos —*hacer que los estados inválidos sean irrepresentables*— aplicada a la concurrencia.

Y Ada 2012 añadió lo que faltaba para el caso general: **los aspectos de datos compartidos**.

```ada
X : Integer with Volatile;              --  no se cachea en registros
Y : Integer with Atomic;                 --  lectura y escritura ATÓMICAS
Z : Integer with Independent;             --  no comparte palabra con vecinos
pragma Volatile_Components (Tabla);
```

**`Atomic`** garantiza que la lectura y la escritura son indivisibles; **`Volatile`** que no se
reordenan ni se cachean; y **`Independent`** que el compilador no la empaqueta con otras variables en
la misma palabra de memoria — un problema real que causa carreras invisibles cuando dos hilos escriben
campos vecinos.

Y para los sistemas de tiempo real, la restricción que cierra el problema:

```ada
pragma Profile (Ravenscar);
```

**Ravenscar** (clase 124) restringe la concurrencia a un subconjunto **analizable**: tareas fijas,
objetos protegidos con una sola entrada, sin colas dinámicas. **Sobre ese subconjunto se puede demostrar
la ausencia de interbloqueos y calcular los tiempos de respuesta.**

Es la respuesta más fuerte de esta página al problema de esta clase: **no detectar las carreras, sino
restringir el lenguaje hasta que no puedan existir y se pueda demostrar**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Carrera;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I, Cuenta: Integer;

begin
  Read(N);

  Cuenta := 0;
  for I := 1 to N do
    Inc(Cuenta);

  WriteLn('cuenta=', IntToStr(Cuenta));
end.
```

**Lo que esta clase enseña en Pascal.** Object Pascal **no tiene un modelo de memoria especificado**, y
depende del que provea la plataforma —el de C++11 en la práctica, porque comparte el hardware y el
sistema operativo.

Lo que sí tiene son las operaciones atómicas, en la clase `TInterlocked`:

```pascal
TInterlocked.Increment(Cuenta);
TInterlocked.Add(Cuenta, 5);
TInterlocked.CompareExchange(Destino, Nuevo, Comparando);
TInterlocked.Exchange(A, B);
```

**`TInterlocked.Increment` es un incremento atómico**, y es exactamente lo que el cierre de esta clase
recomienda para el contador: **hacerlo atómico**, sin bloqueo.

Y Delphi tiene una advertencia propia y muy conocida que ilustra el problema de esta clase mejor que
ningún ejemplo teórico: **el conteo de referencias de las cadenas**.

```pascal
var S: string;      { global, compartida entre hilos }
...
S := S + 'x';        { en dos hilos a la vez: CORRUPCIÓN }
```

**Las cadenas de Pascal llevan un contador de referencias** (clase 102), y **ese contador se incrementa
y decrementa sin sincronización** en las versiones antiguas. Dos hilos manipulando la misma cadena
pueden corromper el contador y liberar la memoria dos veces.

Free Pascal lo resolvió haciendo el conteo atómico **cuando `cthreads` está activa** (clase 133), y de
ahí la importancia de esa unidad: **sin ella, el runtime asume un solo hilo y usa operaciones no
atómicas**.

Es un ejemplo perfecto de lo que esta parte del curso quiere mostrar: **la concurrencia no es solo un
tema del código de usuario — el runtime entero tiene que ser seguro para hilos**, incluidos el gestor
de memoria, el de cadenas y el de excepciones.

Y de ahí el consejo práctico del ecosistema Delphi: **no compartir cadenas, arreglos dinámicos ni
interfaces entre hilos sin sincronizar**, porque su gestión automática de memoria es el punto de
carrera menos evidente.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read))
      (cuenta 0))
  (dotimes (i n)
    (incf cuenta))
  (format t "cuenta=~D~%" cuenta))
```

**Lo que esta clase enseña en Common Lisp.** El estándar **no dice nada sobre concurrencia** (clase
121), así que **no hay modelo de memoria**, y cada implementación define el suyo.

En SBCL:

```lisp
(sb-ext:atomic-incf (car celda))
(sb-ext:compare-and-swap (symbol-value 'contador) viejo nuevo)
(sb-thread:with-mutex (m) ...)
(sb-ext:atomic-push x (cdr lugar))
```

**`compare-and-swap` es la primitiva de la que se derivan todas las estructuras sin bloqueo**, y SBCL
la expone sobre lugares (clase 095) — sobre un `car`, sobre el valor de un símbolo, sobre un campo de
estructura.

Y Common Lisp tiene una propiedad que ayuda en esta clase y que viene de la clase 121: **las variables
especiales son por hilo**.

```lisp
(defvar *acumulador* 0)          ; cada hilo tiene su enlace
```

**El estado dinámico está aislado por defecto**, así que la carrera solo puede ocurrir sobre estructuras
explícitamente compartidas. Es una decisión que reduce mucho la superficie del problema.

Y merece señalar el peligro específico de un lenguaje con recolector y estructuras mutables:

```lisp
(push x lista)          ; NO es atómico: leer, construir, escribir
```

**`push` sobre una lista compartida entre hilos es una carrera clásica**, y puede perder elementos. La
versión segura es `sb-ext:atomic-push` o un cerrojo.

Y la conclusión es la de esta parte: **un lenguaje sin modelo de memoria especificado deja el
comportamiento concurrente en manos de la implementación**, y el código deja de ser portable.

Es exactamente el problema que C++ tenía antes de 2011, y la razón de que el estándar de C++11 sea la
contribución más importante de esa versión — más que las lambdas o el movimiento.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set cuenta 0
for {set i 0} {$i < $n} {incr i} {
    incr cuenta
}

puts "cuenta=$cuenta"
```

**Lo que esta clase enseña en Tcl.** **En Tcl no puede haber condiciones de carrera sobre variables**, y
esa afirmación fuerte se sostiene por la decisión de las clases 121 y 133: **cada hilo tiene su propio
intérprete y no comparte ninguna variable**.

```tcl
set contador 0        ;# esta variable es de ESTE intérprete y de nadie más
```

**No hay memoria compartida, así que no hay modelo de memoria que especificar.** El problema
desaparece por construcción.

Lo que sí se comparte, explícitamente, son las variables `tsv`:

```tcl
tsv::set compartido contador 0
tsv::incr compartido contador        ;# ATÓMICO: lo garantiza la implementación
tsv::lock compartido { ... }          ;# o exclusión explícita
```

**`tsv::incr` es atómico** y `tsv::lock` da exclusión sobre un conjunto de operaciones. La
sincronización está en el mecanismo de compartir, no en el lenguaje general.

Y esa arquitectura tiene una propiedad que el cierre de esta clase destaca: **para tener una carrera hay
que pedirla explícitamente**. En C++ o en Java, compartir es el defecto y aislar cuesta trabajo; en
Tcl es al revés.

Es el mismo diseño que los *web workers* de JavaScript, que los procesos de Erlang y que los
subintérpretes que Python está adoptando (clase 133).

Y merece cerrar con la comparación que esta clase permite hacer entre los tres lenguajes de guion que
se enfrentaron al problema en los noventa:

| | Decisión | Carreras posibles |
|---|---|---|
| **Tcl** | un intérprete por hilo | **solo con `tsv`, sincronizado** |
| **Perl** | copiar el intérprete | solo con `:shared`, y con `lock` |
| **Python** | un cerrojo global (GIL) | **sí, en el código Python** |

**El GIL de Python protege las estructuras internas del intérprete, no el código del usuario.** Un
`contador += 1` en dos hilos de Python **sí puede perder incrementos**, porque el GIL se libera entre
bytecodes.

Es un malentendido muy extendido, y esta comparación lo deja claro: **Tcl y Perl eligieron el
aislamiento; Python eligió proteger el intérprete y dejó la carrera en manos del programador**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $cuenta = 0;
$cuenta++ for 1 .. $n;

print "cuenta=$cuenta\n";
```

**Lo que esta clase enseña en Perl.** Con **iThreads**, Perl evita el problema como Tcl: **nada se
comparte salvo lo declarado** (clase 133).

```perl
use threads;
use threads::shared;

my $cuenta :shared = 0;

my @hilos = map { threads->create(sub {
    for (1 .. 1000) {
        lock($cuenta);          # SIN esto, hay carrera
        $cuenta++;
    }
}) } 1 .. 4;
$_->join for @hilos;
```

**`:shared` marca la variable como compartida y `lock` da exclusión mutua**, con la propiedad de que
**el bloqueo se suelta automáticamente al salir del ámbito** — es RAII (clase 132) aplicado al cerrojo.

Y sin `lock`, `$cuenta++` **es exactamente la carrera del cierre de esta clase**: leer, sumar,
escribir, con otro hilo en medio.

Perl documenta además una advertencia que esta clase debe recoger: **compartir una estructura anidada
requiere que cada nivel sea compartido**.

```perl
my %h :shared;
$h{a} = shared_clone({ x => 1 });     # hay que CLONAR a memoria compartida
```

**`shared_clone`** copia una estructura al espacio compartido, y olvidarlo produce errores confusos —
la referencia se comparte y el contenido no.

Es el mismo problema que en cualquier sistema con memoria segmentada, y la razón de que el modelo de
Perl sea tan poco usado en la práctica: **compartir es tan incómodo que la gente prefiere `fork`**
(clase 133).

Y ahí está la conclusión práctica de esta página, que Perl ilustra sin ambigüedad: **cuando compartir
memoria es caro e incómodo, la comunidad elige no compartir** — y ese resultado es exactamente el que
el cierre de esta clase recomienda.

A veces la mejor solución a un problema difícil es que la alternativa sea más cómoda.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <atomic>
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::atomic<int> cuenta{0};
    for (int i = 0; i < n; ++i) {
        cuenta.fetch_add(1, std::memory_order_relaxed);   // ATÓMICO
    }

    std::cout << "cuenta=" << cuenta.load() << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** **C++11 especificó el primer modelo de memoria de un lenguaje de
uso general**, y esa es una de las contribuciones más importantes de esta página a la informática —
más que cualquier característica sintáctica.

Antes de 2011, **el estándar no decía nada** sobre qué ve un hilo de lo que escribe otro. El código
concurrente dependía del compilador, del procesador y de la fase de la luna, y las bibliotecas de hilos
funcionaban por convención.

C++11 definió:

**La regla fundamental**: dos accesos concurrentes al mismo objeto, siendo uno de escritura y sin
sincronización, son **comportamiento indefinido**. No "un valor raro": **el programa no tiene
significado**.

**Y los órdenes de memoria**:

```cpp
std::memory_order_relaxed    // solo atomicidad; sin garantías de orden
std::memory_order_acquire    // las lecturas posteriores no se adelantan
std::memory_order_release     // las escrituras anteriores son visibles
std::memory_order_acq_rel
std::memory_order_seq_cst      // orden total: el defecto, el más caro
```

**`relaxed` es correcto para un contador** —solo hace falta que no se pierdan incrementos, no que se
ordene nada— y es notablemente más rápido que el defecto en ARM y en POWER.

Ese nivel de control es lo que permite escribir estructuras sin bloqueo correctas y portables, y **ese
trabajo lo adoptaron después C11, Rust y Java** —cuyo modelo de memoria de 2004 fue en realidad el
primero, y sirvió de base al de C++—.

Y las herramientas de esta clase son imprescindibles:

```bash
g++ -fsanitize=thread          # ThreadSanitizer: DETECTA carreras en ejecución
```

**ThreadSanitizer instrumenta cada acceso a memoria** y detecta accesos concurrentes sin
sincronización, aunque no fallen en esa ejecución. Es la única forma práctica de encontrar carreras, y
debería estar en las pruebas de cualquier proyecto concurrente.

Y merece cerrar con lo que C++20 añadió y que hacía falta:

```cpp
cuenta.wait(viejo);          // esperar sin condition_variable
cuenta.notify_all();
std::latch  std::barrier      // sincronización por fases
```

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

dcl-pi CARRERA;
  n int(10) const;
end-pi;

dcl-s i      int(10);
dcl-s cuenta int(10) inz(0);

for i = 1 to n;
  cuenta += 1;
endfor;

dsply ('cuenta=' + %char(cuenta));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG **no tiene modelo de memoria** porque su modelo de concurrencia
es multitrabajo (clases 121 y 133): **cada trabajo tiene su memoria y no comparte**.

Y donde sí hay estado compartido, la plataforma da mecanismos con sincronización incorporada:

```rpgle
in(e) contador;            // LEER un *DTAARA y bloquearlo
contador += 1;
out contador;               // escribir y liberar el bloqueo
```

**`in` y `out` sobre un espacio de datos toman y sueltan un bloqueo del sistema**, así que la secuencia
es atómica entre trabajos — y **persistente**.

Y para los contadores de verdad, Db2 for i da lo que corresponde:

```sql
CREATE SEQUENCE contador AS BIGINT START WITH 1;
VALUES NEXT VALUE FOR contador INTO :n;
```

**Una secuencia de base de datos es un contador atómico, persistente y compartido entre todos los
trabajos y todas las máquinas**, con caché para rendimiento.

Y aquí está el punto que esta clase quiere dejar sobre las plataformas de gestión: **el problema del
contador compartido está resuelto en la capa de datos desde hace décadas**, y con garantías que una
variable atómica en memoria no da — persistencia y participación en transacciones.

Donde RPG **sí** puede tener carreras es en el caso de la clase 087: **el estado estático de un módulo
en un programa de servicio con activación compartida**.

```rpgle
dcl-s cache int(10) dim(100) static;      // ¡compartido entre trabajos!
```

**Si el programa de servicio se activa en un grupo compartido, ese `static` lo ven varios trabajos**, y
sin ninguna sincronización.

Es la fuente de carreras más real de la plataforma, y la razón de la norma que ya se citó: **los
módulos de servicio, sin estado**.

Y merece señalar que ese fallo es especialmente insidioso porque **depende de la configuración de
activación, no del código**: el mismo programa es correcto en un grupo y tiene carreras en otro.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 carrera: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare cuenta fixed binary(31) initial(0);

    get list (n);

    do i = 1 to n;
       cuenta = cuenta + 1;
    end;

    put skip list ('cuenta=' || trim(char(cuenta)));

 end carrera;
```

**Lo que esta clase enseña en PL/I.** PL/I tuvo multitarea en 1964 (clase 121) y **no tuvo modelo de
memoria**, como ningún lenguaje hasta 2004.

Y esa combinación —concurrencia sin modelo— es exactamente el problema que esta clase describe: **con
tareas compartiendo `static` y `external` sin garantías especificadas, escribir código concurrente
correcto dependía del compilador y del hardware**.

Lo que PL/I ofrecía para sincronizar eran los eventos (clase 121):

```pli
 declare recurso event;
 wait(recurso);
 completion(recurso) = '0'b;       /* tomar */
 ...
 completion(recurso) = '1'b;        /* soltar */
```

**Un evento usado como semáforo binario**, con la advertencia de que **`completion` no es
necesariamente atómico** en todas las implementaciones — lo que hace de este idioma algo delicado.

Y en el z/OS de la época, la sincronización de verdad venía del sistema operativo:

```text
ENQ / DEQ    -- serialización de recursos con nombre, a nivel de sistema
Compare and Swap (CS)  -- instrucción atómica de la arquitectura, desde 1970
```

**La instrucción `CS` —comparar e intercambiar— está en la arquitectura de IBM desde el System/370 en
1970**, y fue una de las primeras primitivas atómicas de hardware de uso general. Se diseñó
específicamente para multiprocesadores.

Es un dato que da perspectiva a esta clase: **el hardware tuvo la primitiva atómica veinte años antes
de que los lenguajes tuvieran un modelo de memoria que la explicara**.

Y merece cerrar esta parte del curso desde PL/I con la observación que la recorre: **tuvo la
concurrencia antes que nadie y no tuvo cómo razonar sobre ella**, porque la teoría no existía. El
modelo de memoria de Java es de 2004 y el de C++ de 2011.

**Cuarenta años entre tener la capacidad y saber usarla correctamente** es un recordatorio útil de que
una característica sin la teoría que la sostiene es una trampa.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CARRERA ; Modelo de memoria y carreras -- clase 136
 read n
 set cuenta = 0
 for i=1:1:n set cuenta = cuenta + 1
 write "cuenta=", cuenta, !
 quit
```

**Lo que esta clase enseña en M.** M **no tiene modelo de memoria** y **no lo necesita para las
variables locales**: cada proceso tiene las suyas y no se comparten (clase 133).

Donde hay estado compartido —los *globals*— el problema es real, y M lo resuelve con lo de la clase
121: **`lock` y transacciones**.

```mumps
 lock +^CONTADOR:10
 if $test do
 . set ^CONTADOR = ^CONTADOR + 1
 . lock -^CONTADOR
```

Y M tiene una primitiva que resuelve esta clase concreta de forma directa y elegante: **`$increment`**.

```mumps
 set n = $increment(^CONTADOR)        ; ATÓMICO: incrementa y devuelve el nuevo valor
 set n = $increment(^CONTADOR, 5)      ; en 5
```

**`$increment` es atómico y no necesita `lock`**, y es exactamente lo que el cierre de esta clase
recomienda: **hacerlo atómico**.

Su implementación es lo interesante: **la hace el motor de base de datos**, con el bloqueo del bloque
de disco correspondiente, así que es atómica **entre todos los procesos del sistema y persistente**.

Comparada con un `std::atomic` de C++, tiene tres diferencias:

- **Es mucho más cara** —involucra la caché de bloques de la base de datos—.
- **Es persistente**: sobrevive al reinicio.
- **Y funciona entre procesos y entre máquinas** con ECP (clase 133).

Es la misma operación en un nivel de abstracción completamente distinto.

Y merece cerrar la Parte 8 desde M con la observación que la recorre: **este lenguaje evita la mayoría
de los problemas de esta parte moviendo el problema a la capa de datos**.

Sin punteros no hay punteros colgantes (clase 129); sin memoria compartida mutable no hay carreras
(clase 136); sin reserva explícita no hay fugas (clase 128). Y todo lo que sí es compartido está en una
base de datos transaccional que impone las reglas.

**Es un diseño coherente, tomado en 1966 y sostenido desde entonces** — y explica por qué un lenguaje
que parece primitivo sostiene sistemas que otros no podrían.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n cuenta |

n := stdin nextLine trimBoth asNumber.

cuenta := 0.
n timesRepeat: [ cuenta := cuenta + 1 ].

Transcript show: 'cuenta=', cuenta printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene una propiedad que hace esta clase mucho más
simple de lo que sería en otro sitio, y viene de la clase 133: **los procesos son cooperativos dentro
de cada prioridad**.

**Un proceso no cede el control hasta que se bloquea o llama a `yield`**, así que **dos procesos de la
misma prioridad no pueden interrumpirse en mitad de una operación**.

```smalltalk
cuenta := cuenta + 1.        "atómico respecto a los procesos de la misma prioridad"
```

**La carrera clásica del cierre de esta clase no puede ocurrir entre iguales**, porque no hay
desalojo.

Con procesos de prioridad distinta sí puede, y para eso está el mecanismo de siempre:

```smalltalk
| sem |
sem := Semaphore forMutualExclusion.
sem critical: [ cuenta := cuenta + 1 ].
```

Y hay una construcción que Smalltalk tiene y que responde a esta clase con precisión: **la sección
atómica del planificador**.

```smalltalk
[ ... ] valueUnpreemptively.        "no ceder el control durante esto"
Processor activeProcess priority: Processor highIOPriority.
```

Y como el planificador está escrito en Smalltalk (clase 121), **se puede leer exactamente qué garantiza**
— algo que con un planificador del sistema operativo es imposible.

Ahora, la limitación real, ya nombrada: **la máquina virtual de Pharo usa un solo hilo del sistema**, así
que **no hay paralelismo verdadero y por tanto no hay carreras a nivel de hardware**. El problema de
esta clase —qué ve un núcleo de lo que escribe otro— **no llega a plantearse**.

Y para el paralelismo real, el ecosistema usa varias imágenes con mensajes (clase 135), que es la
primera solución del cierre: **no compartir**.

Merece cerrar la Parte 8 con lo que Smalltalk ilustra mejor que ningún otro lenguaje de esta página:
**casi todos los problemas de las dieciséis clases de esta parte —compilación, memoria, pila,
recolección, concurrencia— son observables y modificables desde el propio lenguaje**.

La máquina virtual, el planificador, el recolector, el compilador y la pila **son objetos**. Cuando
alguien pregunta cómo funciona Smalltalk por dentro, la respuesta literal es la misma que la clase 121
daba sobre la concurrencia: **abre el navegador y léelo**.

---

## Y de vuelta a la clase

Lo transferible: **`contador++` no es una operación, son tres** —leer, sumar, escribir— y entre ellas
cabe otro hilo. Esa es la carrera clásica, y las soluciones son cuatro: **no compartir**, **hacerlo
atómico**, **protegerlo con exclusión** o **hacerlo inmutable**. Ninguna es gratis, y la peor decisión
es la que se toma sin darse cuenta: **compartir una variable entre hilos sin pensarlo**. Si dudas de si
un dato se comparte, ya tienes el problema.

⏮️ [Volver a la clase 136](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
