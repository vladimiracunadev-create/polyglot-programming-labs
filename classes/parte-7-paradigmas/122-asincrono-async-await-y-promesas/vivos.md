# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 122

> [⬅️ Volver a la clase 122](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Lanzar un trabajo y esperar su resultado sin bloquear. `async`/`await` parece de 2012, y sus dos
piezas son mucho más viejas: **la promesa la describieron Baker y Hewitt en 1977 en un artículo sobre
Lisp**, y **la corrutina la nombró Conway en 1958**. Aquí hay tres lenguajes que las tienen de verdad:
**Tcl con corrutinas desde 2012, Ada con la cita desde 1983 y C++ con `co_await` desde 2020**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **suspender y reanudar sin bloquear el hilo**, y estos lenguajes lo enseñan porque
> muestran que `async`/`await` no es una idea nueva sino **una sintaxis para una idea vieja**. La
> **cita de Ada** —`entry` y `accept`— es exactamente un `await`: quien llama se suspende hasta que el
> otro esté listo, y el planificador aprovecha el hueco. Las **corrutinas de Tcl** dan lo mismo sin
> sintaxis nueva, porque `yield` ya es suspender.
>
> Y **COBOL y RPG** enseñan la versión de la plataforma: `EXEC CICS START` y las colas de datos son
> **invocación asíncrona con recogida posterior del resultado**, que es una promesa con otro nombre.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `resultado=<2n>`
- **Regla:** `await doble(n) = 2n`

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `6` | `resultado=12` |

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
PROGRAM-ID. ASINC.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  RESULT  PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    *> COBOL no tiene async: aquí la llamada es directa
    PERFORM CALCULAR

    MOVE RESULT TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.

CALCULAR.
    COMPUTE RESULT = N * 2.
```

**Lo que esta clase enseña en COBOL.** COBOL no tiene `async`/`await`, y **CICS tiene invocación
asíncrona con recogida de resultados desde hace décadas** — que es una promesa con otro nombre.

**La forma clásica, con `START`:**

```cobol
EXEC CICS START TRANSID('CALC')
    FROM(DATOS) LENGTH(100)
    RTRANSID('RECOGE') RTERMID(MITERM)
END-EXEC
*> el programa SIGUE; la transacción CALC se ejecuta aparte
```

**`START` lanza otra transacción y devuelve el control inmediatamente.** `RTRANSID` indica qué
transacción atenderá la respuesta. Es lanzar un trabajo y registrar quién recogerá el resultado —
exactamente un `then`.

**Y la moderna, con la API asíncrona de CICS TS 5.2 (2014):**

```cobol
EXEC CICS RUN TRANSID('CALC') CHILD(TOKEN) ASYNCHRONOUS END-EXEC
*> ... hacer otras cosas mientras tanto ...
EXEC CICS FETCH CHILD(TOKEN) INTO(RESULTADO) END-EXEC
*> FETCH se bloquea hasta que el hijo termina: eso es AWAIT
```

Mira las palabras: **`CHILD(TOKEN)` es la promesa, `RUN ... ASYNCHRONOUS` es el `async`, y `FETCH` es
el `await`**. Y hay más:

```cobol
EXEC CICS FETCH ANY(TOKEN) ... END-EXEC     *> el PRIMERO que termine: Promise.race
EXEC CICS FREE CHILD(TOKEN) END-EXEC         *> cancelar
```

**`FETCH ANY`** espera al primero que acabe, que es `Promise.race`. Y lanzando varios hijos y
recogiéndolos todos se tiene `Promise.all`.

Eso es un modelo de promesas completo, en un monitor transaccional, para programas COBOL. Se
introdujo en 2014 con un motivo muy concreto: **las aplicaciones de mainframe empezaron a tener que
llamar a varios servicios web y no podían hacerlo en serie**.

Es la modernización por los bordes de la clase 105, aplicada a la concurrencia: **el lenguaje no
cambia; el entorno le da lo que necesita para hablar con el mundo de hoy**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program asinc
   implicit none
   integer :: n, resultado

   read(*, *) n

   !  Fortran no tiene async/await: la llamada es directa
   resultado = doblar(n)

   write(*, '(A,I0)') 'resultado=', resultado

contains

   pure function doblar(x) result(r)
      integer, intent(in) :: x
      integer :: r
      r = x * 2
   end function doblar

end program asinc
```

**Lo que esta clase enseña en Fortran.** **Fortran no tiene nada asíncrono para código**, y merece
explicar por qué no le hace falta: `async`/`await` sirve para **aprovechar el tiempo de espera de la
entrada/salida**, y un programa Fortran típico **no espera: calcula**.

Cuando el cuello de botella es la CPU, la respuesta no es la asincronía sino el paralelismo — que
Fortran tiene de sobra (clase 121).

Y sin embargo, Fortran **sí tiene entrada/salida asíncrona en el estándar**, desde Fortran 2003, y es
poco conocida:

```fortran
open(unit=10, file='enorme.dat', asynchronous='yes')

read(10, asynchronous='yes', id=peticion) datos      ! LANZAR la lectura
call calcular_otra_cosa()                             ! trabajar mientras llega
wait(unit=10, id=peticion)                             ! AWAIT
```

**`asynchronous='yes'` con `id=` y `wait`** es exactamente el patrón de esta clase: lanzar, seguir
trabajando y esperar cuando haga falta el dato. **`id` es la promesa y `wait` es el `await`.**

Y su motivación es la de los superordenadores: **escribir un volcado de estado de decenas de gigabytes
mientras la simulación sigue calculando el paso siguiente**. Sin eso, un modelo climático pasaría una
fracción importante de su tiempo esperando al disco.

El atributo **`asynchronous`** también se aplica a las variables, y es una declaración al compilador:

```fortran
real, asynchronous :: buffer(1000000)
```

Le dice que **ese arreglo puede cambiar por debajo mientras se ejecuta el código**, así que no puede
mantenerlo en registros ni reordenar accesos. Es el `volatile` de C con un propósito más preciso.

Y con los coarrays (clase 121), Fortran 2018 añadió las operaciones **atómicas** y los **eventos**:

```fortran
event post (listo[2])                ! avisar a otra imagen
event wait (listo)                    ! esperar el aviso
```

`event post` y `event wait` son señalización asíncrona entre procesos, con la misma forma que las
promesas de PL/I de la clase 119 y `Promise` de JavaScript.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Asinc is
   N : Integer;
begin
   Get (N);

   declare
      task Trabajo is
         entry Arranca (X : Integer);
         entry Resultado (R : out Integer);
      end Trabajo;

      task body Trabajo is
         Valor : Integer;
      begin
         accept Arranca (X : Integer) do
            Valor := X;
         end Arranca;

         Valor := Valor * 2;             --  "el trabajo largo"

         accept Resultado (R : out Integer) do
            R := Valor;
         end Resultado;
      end Trabajo;

      R : Integer;
   begin
      Trabajo.Arranca (N);               --  lanzar: NO bloquea al terminar la cita
      --  ... aquí se podría hacer otra cosa ...
      Trabajo.Resultado (R);              --  AWAIT: se suspende hasta que esté
      Put ("resultado=");
      Put (R, Width => 1);
      New_Line;
   end;
end Asinc;
```

**Lo que esta clase enseña en Ada.** `Trabajo.Resultado (R)` **es un `await`**, y lleva siéndolo desde
1983.

La **cita** (*rendezvous*) de Ada funciona así: quien llama a una entrada **se suspende hasta que la
tarea llamada ejecute su `accept`**, y mientras tanto **el planificador ejecuta otras tareas**. Eso es
exactamente lo que hace `await`: liberar el hilo mientras se espera.

La diferencia con `async`/`await` es de sintaxis y de modelo, y merece verla:

| | `async`/`await` | Cita de Ada |
|---|---|---|
| Qué se espera | una promesa | **otra tarea** |
| Quién decide cuándo | el planificador de tareas | **la tarea llamada, con `accept`** |
| Color de función | **sí**: `async` se propaga | **no** |
| Cancelación | por `token` | `select ... then abort` |

Esa fila del **color de las funciones** es la importante, y es el problema que menciona el cierre de
esta clase: en Ada **cualquier subprograma puede llamar a una entrada**, no hace falta declararlo
`async` ni propagar nada.

Y Ada tiene las construcciones que en JavaScript son métodos de `Promise`:

```ada
select
   Trabajo.Resultado (R);
or
   delay 5.0;                       --  TIMEOUT: Promise.race con un temporizador
   Put_Line ("tardó demasiado");
end select;

select
   Trabajo.Resultado (R);
else
   Put_Line ("todavía no");          --  comprobar sin esperar
end select;

select
   Trabajo.Resultado (R);
then abort
   Calcular_Aproximacion;             --  hacer esto MIENTRAS, y ABORTARLO si llega
end select;
```

Esa última —**`then abort`**— no tiene equivalente en ningún lenguaje de esta página: **ejecuta un
bloque mientras se espera y lo cancela en cuanto la espera termina**. Es cálculo especulativo con
cancelación, en la gramática.

Y con `delay until` (clase 107) para instantes absolutos y `pragma Queuing_Policy` para la disciplina
de las colas (clase 096), Ada tiene un modelo asíncrono completo y **con garantías temporales**, que
es lo que ningún `async`/`await` moderno ofrece.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Asinc;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, Resultado: Integer;

begin
  Read(N);

  { Pascal estándar no tiene async: la llamada es directa }
  Resultado := N * 2;

  WriteLn('resultado=', IntToStr(Resultado));
end.
```

**Lo que esta clase enseña en Pascal.** El Pascal clásico no tiene nada asíncrono, y **Delphi y Free
Pascal modernos tienen el modelo completo**, llegado por la puerta de las aplicaciones móviles.

**Las tareas y los futuros** (Delphi XE7, 2014):

```pascal
uses System.Threading;

var T: ITask;
begin
  T := TTask.Run(procedure begin TrabajoLargo end);
  T.Wait;                                    { await }

  var F := TTask.Future<Integer>(function: Integer
                                 begin Result := Calcular end);
  Valor := F.Value;                           { await con resultado }
end;
```

**`IFuture<T>` es una promesa**, y `.Value` es el `await`: bloquea hasta que esté listo. Y hay
`TTask.WaitForAll` y `TTask.WaitForAny`, que son `Promise.all` y `Promise.race`.

Y la pieza que resuelve el problema clásico de las interfaces (clase 121):

```pascal
TTask.Run(procedure
begin
  Datos := DescargarTodo;                    { en un hilo secundario }
  TThread.Synchronize(nil, procedure
  begin
    Rejilla.Actualizar(Datos);                { de vuelta al hilo de la INTERFAZ }
  end);
end);
```

**`Synchronize` encola el bloque al hilo principal**, que es lo que hacen `invokeLater` en Swing,
`Dispatcher.Invoke` en WPF y `DispatchQueue.main` en iOS. Sin eso, tocar un control desde otro hilo
corrompe la interfaz.

Y hay una capacidad menos conocida y muy útil que Delphi tiene: **`TThread.ForceQueue`** y las
**funciones anónimas como continuaciones**, con las que se escriben cadenas de trabajo asíncrono sin
bloquear:

```pascal
Descargar(URL,
  procedure(const Datos: string)
  begin
    Procesar(Datos);
  end);
```

Eso es una retrollamada de finalización, y anidar varias reproduce el problema del cierre de la clase
119 —el infierno de las retrollamadas—, que es exactamente lo que `async`/`await` vino a resolver.

Free Pascal y Delphi **no tienen `async`/`await` como sintaxis**, y esa es la carencia real de esta
clase en Pascal: hay futuros, hay tareas y hay sincronización, y **la forma secuencial hay que
escribirla a mano**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       ;;  una "promesa" hecha a mano: un cálculo diferido
       (promesa (lambda () (* n 2))))
  ;;  "await": forzar la promesa
  (format t "resultado=~D~%" (funcall promesa)))
```

**Lo que esta clase enseña en Common Lisp.** Aquí está el origen histórico que abre esta clase: **el
término *promise* y el concepto de futuro vienen de la comunidad Lisp**.

**Daniel Friedman y David Wise (1976)** describieron los *promises*, y **Henry Baker y Carl Hewitt
(1977)**, en *The Incremental Garbage Collection of Processes*, describieron los **futuros** — un
valor que todavía no está calculado y que el consumidor espera automáticamente si lo necesita.

Y **Multilisp** (Halstead, 1985) los llevó a un lenguaje real:

```lisp
(future (calcular-algo))       ; devuelve INMEDIATAMENTE una promesa
```

En Multilisp, **usar un futuro que aún no está resuelto suspende al que lo usa automáticamente**. Sin
`await`: el compilador insertaba la comprobación. Es lo que hoy se llama *futuros transparentes*, y
elimina el problema del color de las funciones del cierre de esta clase.

Common Lisp **tiene una versión perezosa en el estándar**, aunque sin concurrencia:

```lisp
(defparameter p (delay (calculo-caro)))     ; en Scheme; en CL:
(defparameter p (lambda () (calculo-caro)))
(funcall p)                                   ; forzar
```

Y el ecosistema moderno trae los futuros de verdad:

```lisp
(ql:quickload :lparallel)
(let ((f (lparallel:future (calcular))))
  (lparallel:force f))                        ; await

(lparallel:pmap 'list #'procesar datos)        ; map paralelo
(lparallel:pdotimes (i n) ...)
```

**lparallel** da futuros, promesas explícitas, canales, colas de tareas y operaciones paralelas, con
una API que se lee declarativa.

Y hay algo que Lisp puede hacer y casi nadie: **implementar `async`/`await` con macros**, sin tocar el
compilador.

```lisp
(defmacro async (&body cuerpo) `(lparallel:future ,@cuerpo))
(defmacro await (f) `(lparallel:force ,f))
```

Dos líneas. Y con continuaciones —`cl-cont`— se puede llegar más lejos y transformar código secuencial
en estilo de paso de continuaciones automáticamente, que es exactamente lo que hace el compilador de
un lenguaje con `async`/`await`.

Es, una vez más, el argumento de la clase 107: **lo que otros lenguajes añaden al núcleo, Lisp lo
añade como biblioteca**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc trabajo {n} {
    yield                       ;# suspender: aquí se devuelve el control
    return [expr {$n * 2}]
}

gets stdin linea
set n [string trim $linea]

coroutine tarea trabajo $n     ;# crear la corrutina (llega hasta el yield)
set resultado [tarea]           ;# reanudarla: devuelve su valor

puts "resultado=$resultado"
```

**Lo que esta clase enseña en Tcl.** Este programa usa **corrutinas de verdad**: `coroutine` crea una,
`yield` la suspende devolviendo el control, y llamarla por su nombre la reanuda.

**Las corrutinas llegaron en Tcl 8.6 (2012)**, y su combinación con el bucle de eventos de 1990 (clase
119) da exactamente lo que `async`/`await` da en otros lenguajes — **sin sintaxis nueva y sin colorear
funciones**:

```tcl
coroutine cliente apply {{} {
    set canal [socket -async servidor 80]
    yieldto fileevent $canal writable [info coroutine]    ;# esperar sin bloquear
    puts $canal "GET / HTTP/1.0\n"
    set respuesta [read $canal]
}}
```

**`yieldto` con `fileevent`** suspende la corrutina y registra su reanudación como manejador de un
evento. Mientras tanto, **el bucle de eventos sigue atendiendo a los demás**.

Eso es `await` sobre entrada/salida, y hay dos cosas que lo hacen mejor que `async`/`await`:

1. **No hay color de función.** Una corrutina puede llamar a cualquier procedimiento, y ese
   procedimiento puede hacer `yield`. No hay que declarar nada ni propagar `async` por toda la pila —
   el problema del cierre de esta clase.
2. **`[info coroutine]`** devuelve el nombre de la corrutina actual, así que **se puede pasar como
   retrollamada** y reanudarse desde cualquier sitio.

Es lo mismo que hacen las **fibras** y lo que Java 21 eligió con los **hilos virtuales**, precisamente
para evitar colorear funciones. Tcl lo tiene desde 2012 y el modelo entero desde 1990.

Y Tcl 8.7 añade `coroinject` y `coroprobe`, que permiten **inyectar código dentro de una corrutina
suspendida** y examinarla — depuración de código asíncrono, que en la mayoría de los entornos es un
problema conocido.

El paquete **`tcl::async`** y las utilidades de Tcllib completan el cuadro con promesas y combinadores
al estilo `Promise.all`.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

#  una "promesa" mínima: un cálculo diferido en una clausura
my $promesa = sub { return $n * 2 };

print "resultado=", $promesa->(), "\n";
```

**Lo que esta clase enseña en Perl.** Perl **no tiene `async`/`await` en el núcleo**, y su ecosistema
tiene el modelo completo desde hace más de una década.

**`Future`** es la biblioteca de referencia, y su vocabulario es el de las promesas:

```perl
use Future;

my $f = Future->new;
$f->done(42);                          # resolver
$f->fail("error");                      # rechazar

$f->then(sub { ... })                    # encadenar
  ->else(sub { ... })                     # capturar el error
  ->on_ready(sub { ... });                 # finally

Future->wait_all(@futuros);                # Promise.all
Future->wait_any(@futuros);                 # Promise.race
Future->needs_all(@futuros);                 # all, fallando si alguno falla
```

Y **`IO::Async`** —del mismo autor, Paul Evans— da el bucle de eventos, con `Future` como moneda de
cambio:

```perl
my $bucle = IO::Async::Loop->new;
$bucle->connect(host => '...')->then(sub { ... })->get;
```

Y hay una historia que merece contarse porque es reciente y muestra cómo evoluciona un lenguaje vivo:
**Paul Evans, autor de `Future`, escribió `Future::AsyncAwait`**, un módulo que **añade la sintaxis
`async` y `await` a Perl**:

```perl
use Future::AsyncAwait;

async sub descargar {
    my $datos = await http_get($url);
    return procesar($datos);
}
```

Eso **no es una función de biblioteca: es sintaxis nueva**, implementada con la API de análisis
sintáctico de Perl. Y funcionó tan bien que **sus ideas se están incorporando al núcleo**, junto con
las firmas de subrutina y la palabra clave `class` (clase 110).

Es un patrón muy propio de Perl y que esta sección debe destacar: **el lenguaje se extiende desde
CPAN, y lo que demuestra su valor acaba en el núcleo**. `Try::Tiny` llevó a `try`/`catch` nativo en
5.34; `Moose` llevó a `class`; `Future::AsyncAwait` va por el mismo camino.

Y para el paralelismo real, la respuesta sigue siendo `fork` (clase 121): **asincronía con un bucle de
eventos, paralelismo con procesos**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <future>
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    //  std::async devuelve un FUTURO: la promesa de un valor
    std::future<int> f = std::async(std::launch::async, [n] { return n * 2; });

    //  .get() es el await: se bloquea hasta que esté listo
    std::cout << "resultado=" << f.get() << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::future` y `std::async` llegaron en **C++11**, y son la
promesa clásica: lanzar un trabajo y recoger el valor después.

```cpp
std::future<int> f = std::async(std::launch::async, tarea);
f.get();                      // await, BLOQUEANTE
f.wait_for(std::chrono::seconds(1));   // esperar con límite
std::promise<int> p;  auto f = p.get_future();  p.set_value(42);
std::packaged_task<int()> t{tarea};
```

Con dos limitaciones importantes que conviene conocer:

1. **`get()` bloquea el hilo.** No hay continuaciones: no existe `f.then(...)` en el estándar. Se
   propuso y no entró.
2. **El futuro de `std::async` con `launch::async` tiene un destructor que ESPERA**, lo que sorprende:
   `std::async(...);` sin guardar el resultado **se comporta como una llamada síncrona**.

**C++20 trajo las corrutinas**, que son la solución de verdad:

```cpp
task<int> descargar(std::string url) {
    auto datos = co_await http_get(url);      // suspende SIN bloquear el hilo
    co_return procesar(datos);
}
```

Y el diseño de las corrutinas de C++ es característico: **el lenguaje aporta la maquinaria —`co_await`,
`co_yield`, `co_return` y la transformación a máquina de estados— y NO aporta los tipos**.

No hay `task`, no hay `generator` —hasta C++23— y no hay planificador. **Hay que escribirlos o usar una
biblioteca**: cppcoro, Boost.Asio, libunifex.

Esa decisión es puro C++: **dar el mecanismo de coste cero y dejar la política al usuario**. Con la
consecuencia previsible: las corrutinas de C++20 son difíciles de usar directamente y magníficas
cuando alguien ha construido la capa de encima.

Y **son de coste cero de verdad**: el compilador transforma la función en una máquina de estados y, si
el marco no escapa, **puede evitar la reserva de memoria por completo**. Es la misma promesa de C++
para todo: la abstracción no cuesta si no la usas.

C++23 añadió `std::generator`, y la propuesta de ejecutores —`std::execution`, en C++26— aportará por
fin los planificadores estándar que faltan.

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

dcl-pi ASINC;
  n int(10) const;
end-pi;

// RPG no tiene async/await: la llamada es directa
dsply ('resultado=' + %char(doblar(n)));

*inlr = *on;
return;

dcl-proc doblar;
  dcl-pi *n int(20);
    x int(10) const;
  end-pi;
  return x * 2;
end-proc;
```

**Lo que esta clase enseña en RPG.** RPG no tiene `async`/`await`, y la plataforma tiene el patrón
completo con las piezas de las clases 096 y 119: **colas de datos como promesas**.

```rpgle
// LANZAR: enviar la petición a un trabajo servidor
callp enviarDatos('PETICIONES' : 'MIBIB' : %len(peticion) : peticion);

// ... hacer otras cosas ...

// AWAIT: esperar la respuesta, con tiempo límite
callp recibirDatos('RESPUESTAS' : 'MIBIB' : longitud : respuesta : 30);
```

**El trabajo se lanza escribiendo en una cola y el resultado se recoge leyendo de otra**, con un tiempo
de espera. Es exactamente una promesa: **la petición lleva un identificador y la respuesta lo
devuelve**.

Y con **colas por clave**, el emparejamiento es directo:

```text
CRTDTAQ DTAQ(RESPUESTAS) SEQ(*KEYED) KEYLEN(16)
```

Una cola con clave permite **recibir solo la respuesta que lleve MI identificador**, mientras otras
respuestas para otros esperan en la misma cola. **Eso es exactamente lo que hace un correlador de
mensajes**, y está en el sistema desde los años ochenta.

Con eso se montan las tres operaciones de esta clase:

- **`await`**: leer con clave y tiempo de espera.
- **`Promise.all`**: lanzar N peticiones y leer N respuestas.
- **`Promise.race`**: leer de la cola sin clave, el primero que llegue.

Y la plataforma da además dos formas más de asincronía:

```text
SBMJOB CMD(CALL PGM(PROCESA))              -- lanzar un trabajo (clase 121)
```

```sql
CALL QSYS2.HTTP_GET_VERBOSE(...)            -- llamadas HTTP desde SQL
```

Y para el mundo moderno, **IBM i Access y los servicios REST** permiten que un programa RPG sea a la
vez cliente y servidor de servicios web, con las colas gestionando la concurrencia.

Es la conclusión que se repite en toda la Parte 7 con estas plataformas: **lo que en un lenguaje
moderno es sintaxis, aquí es un objeto del sistema operativo** — más verboso, y persistente,
transaccional y observable.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 asinc: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    /* PL/I no tiene async/await; ver la nota sobre task y event */
    put skip list ('resultado=' || trim(char(n * 2)));

 end asinc;
```

**Lo que esta clase enseña en PL/I.** PL/I **tenía las dos mitades de `async`/`await` en 1964**, y ya
aparecieron en las clases 119 y 121. Aquí es donde encajan del todo:

```pli
 declare listo event;
 declare resultado fixed binary(31);

 call calcular(n, resultado) task(t) event(listo);   /* ASYNC: lanzar */

 call otra_cosa();                                    /* seguir trabajando */

 wait(listo);                                          /* AWAIT: esperar */
 put list (resultado);
```

**`task` es el `async`, `event` es la promesa y `wait` es el `await`.** La correspondencia es exacta, y
el vocabulario de PL/I incluso es más claro: un `event` **es** un objeto que representa "algo que
ocurrirá".

Y las operaciones sobre eventos cubren lo que en JavaScript son métodos de `Promise`:

```pli
 wait(listo);                  /* await */
 wait(e);                       /* Promise.all sobre un arreglo de eventos */
 wait(e) (1);                    /* Promise.race: el primero de ellos */
 completion(listo)               /* ¿ya está? -- comprobar sin esperar */
 status(listo)                    /* con qué resultado terminó */
```

**`completion` y `status` como pseudovariables** permiten consultar y fijar el estado de un evento, con
lo que un evento sirve también de semáforo (clase 121).

Es un modelo de promesas completo, cuarenta y ocho años antes de que `async`/`await` llegara a C# en
2012.

Y la conclusión honesta es la de las clases 120 y 121: **casi nadie lo usó**. Los compiladores lo
implementaron parcialmente, la documentación advertía del coste, y el paralelismo del mainframe venía
de ejecutar muchos trabajos a la vez.

Merece cerrar esta parte del curso con la observación que se ha ido acumulando: **PL/I tuvo
concurrencia, promesas, excepciones con reanudación, cadenas de longitud variable, aritmética de
arreglos y punteros antes que nadie, y ninguna de esas ideas se difundió desde PL/I**.

Se difundieron después, desde otros lenguajes, redescubiertas. La lección no es que PL/I fuera
adelantado: es que **una buena idea no se propaga por ser buena, sino por llegar en un lenguaje que la
gente adopta**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ASINC ; Asincrono -- clase 122
 read n
 ; M no tiene async/await: la llamada es directa
 write "resultado=", $$doblar(n), !
 quit
 ;
doblar(x) quit x * 2
```

**Lo que esta clase enseña en M.** M **no tiene `async`/`await`, ni promesas, ni corrutinas**, y tiene
la primitiva que lanza trabajo en paralelo:

```mumps
 job procesar^INFORME(id)
 job procesar^INFORME(id):(priority=5):10      ; con parámetros y tiempo de espera
```

**`job` lanza un proceso independiente** y devuelve el control inmediatamente. Es el `async`, y no
tiene `await`: el proceso hijo **no puede devolver un valor**.

La forma de recoger el resultado es la que cabe esperar en M y es la que se usa: **por un *global***.

```mumps
 ; lanzar
 set id = $increment(^PETICION)
 set ^PETICION(id, "datos") = entrada
 job procesar^TRABAJO(id)

 ; "await": esperar a que aparezca la respuesta
 for  quit:$data(^PETICION(id, "resultado"))  hang 0.1
 set resultado = ^PETICION(id, "resultado")
```

Eso es **una promesa implementada como un nodo de la base de datos**: el hijo escribe ahí cuando
termina, y el padre espera a que aparezca. Con `hang` para no consumir CPU.

Es rudimentario, y tiene tres propiedades que ninguna promesa en memoria tiene: **es persistente**
—sobrevive a que el padre muera—, **es observable** —cualquier proceso puede consultar el estado— y
**es transaccional**.

Las implementaciones modernas dan la versión civilizada. **YottaDB** tiene enlaces con Node.js, Python
y Go, así que **la capa asíncrona se escribe en el lenguaje que la tenga** y los datos siguen en
*globals*. Y **IRIS** tiene `%SYSTEM.WorkMgr`, un gestor de trabajos con colas y espera:

```objectscript
Set queue = ##class(%SYSTEM.WorkMgr).%New()
Do queue.Queue("##class(Mi.Clase).Procesar", id)
Do queue.WaitForComplete()
```

Y con eso cierra la Parte 7 desde el lenguaje más antiguo de la página, con la observación que la
recorre entera: **M no adoptó ningún paradigma de los dieciséis de esta parte**. Sigue siendo
imperativo, sin tipos, sin ámbitos y sin objetos.

Y sostiene los historiales clínicos de decenas de millones de personas, porque **su paradigma nunca fue
de programación: fue de datos**, y ese sigue siendo actual.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n promesa |

n := stdin nextLine trimBoth asNumber.

"un bloque no evaluado es una promesa mínima"
promesa := [ n * 2 ].

Transcript show: 'resultado=', promesa value printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Un bloque no evaluado **es una promesa mínima**: un cálculo
diferido que se fuerza con `value`. Y con `fork` (clase 121), la promesa se vuelve concurrente.

Pharo trae el modelo completo:

```smalltalk
| p |
p := [ calculoLargo ] promise.          "lanza en un proceso y devuelve una promesa"
p wait.                                   "await"
p value.                                   "el resultado"
p isResolved.

Promise all: { p1. p2. p3 }.              "Promise.all"
[ ... ] future.                             "otra forma, según el dialecto"
```

Y hay una construcción de Smalltalk que va más allá de las promesas y que merece cerrar esta parte:
**los `Future` y los proxies transparentes**.

```smalltalk
resultado := servidor calcularAlgo.      "devuelve un PROXY inmediatamente"
...
resultado + 1                              "AQUÍ se espera, si aún no llegó"
```

**Un proxy transparente parece el valor real**, y **solo se bloquea cuando alguien le envía un
mensaje**. Es lo mismo que hacía Multilisp con los futuros transparentes (la página de Lisp de esta
clase), y en Smalltalk se implementa **sin tocar la máquina virtual**, con `doesNotUnderstand:` (clase
051): el proxy no entiende ningún mensaje, así que lo intercepta, espera el valor y lo reenvía.

Eso **elimina el color de las funciones** del cierre de esta clase: no hay que declarar nada `async`,
porque el consumidor no sabe que está esperando.

Y esa idea es la base de **los objetos remotos** de Smalltalk: en sistemas distribuidos escritos en él,
un objeto de otra máquina se usa igual que uno local, y el proxy se ocupa de la red.

Con eso cierra la Parte 7, y merece decirlo con claridad: **Smalltalk lleva desde 1980 con un modelo
donde los objetos, los procesos, los contextos de pila, las clases y el planificador son todos objetos
del mismo sistema, inspeccionables y modificables en marcha**.

Casi todos los paradigmas de esta parte se pueden implementar dentro de él **sin cambiar el lenguaje**,
y varios —MVC, TDD, la refactorización automática, los traits— se inventaron ahí.

No es el lenguaje más usado de esta página. Probablemente sea el más influyente.

---

## Y de vuelta a la clase

Lo transferible: **`async`/`await` no da paralelismo, da concurrencia sin bloquear**. Un solo hilo que
atiende mil conexiones no calcula más rápido: **aprovecha el tiempo que pasaría esperando**. Por eso
sirve para entrada/salida y no para cálculo, y por eso ponerle `await` a algo que consume CPU no
mejora nada. Y trae su propio problema —**el color de las funciones**: una función `async` solo se
puede esperar desde otra `async`, y esa restricción se propaga por todo el programa. Las corrutinas de
Tcl y las fibras no lo tienen, y por eso Java 21 eligió ese camino con los hilos virtuales.

⏮️ [Volver a la clase 122](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
