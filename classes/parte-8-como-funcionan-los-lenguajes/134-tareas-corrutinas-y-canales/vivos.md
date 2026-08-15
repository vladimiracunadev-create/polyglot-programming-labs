# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 134

> [⬅️ Volver a la clase 134](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Encontrar el máximo. La pregunta de esta clase es **cómo se suspende y se reanuda algo sin bloquear un
hilo**, y su respuesta más antigua está aquí: **Melvin Conway acuñó "corrutina" en 1958**, describiendo
un compilador de COBOL. Y en esta página hay dos implementaciones vivas: **las corrutinas de Tcl
(2012)** y **la cita de Ada (1983)**, que es un canal síncrono con otro nombre.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **suspensión sin bloqueo**: guardar el estado de una ejecución y reanudarla
> después. Estos lenguajes lo enseñan porque contienen el origen —el término es de 1958, describiendo
> cómo se comunicaban las fases de un compilador— y porque tienen las dos formas modernas.
>
> **El canal síncrono**: la cita de Ada, donde emisor y receptor se encuentran y se bloquean el uno por
> el otro. **Y la corrutina**: Tcl, con `yield` y reanudación por nombre, sin colorear funciones (clase
> 122). Los dos resuelven lo mismo desde lados opuestos —**la sincronización por encuentro y la
> suspensión explícita**— y los dos preceden a Go en décadas.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `max=<el mayor>`
- **Regla:** `enviar los valores por un canal; el consumidor guarda el máximo`

| stdin | esperado |
|---|---|
| `3 1 4` | `max=4` |
| `5` | `max=5` |
| `10 20 5` | `max=20` |

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
PROGRAM-ID. TAREAS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2)  COMP VALUE 0.
01  I       PIC 9(4)  COMP.
01  VALOR   PIC S9(9) COMP-3.
01  MAXIMO  PIC S9(9) COMP-3.
01  HAY     PIC X VALUE "N".
01  ED-M    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM CERRAR
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM CERRAR

    MOVE MAXIMO TO ED-M
    DISPLAY "max=" FUNCTION TRIM(ED-M)
    STOP RUN.

CERRAR.
    IF TLEN > 0
        COMPUTE VALOR = FUNCTION NUMVAL(TOKEN)
        IF HAY = "N" OR VALOR > MAXIMO
            MOVE VALOR TO MAXIMO
            MOVE "S" TO HAY
        END-IF
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** Aquí está el dato que abre esta clase, y es de los mejores de
toda la sección: **el término "corrutina" lo acuñó Melvin Conway en 1958, en un artículo sobre el
diseño de un compilador de COBOL**.

*Design of a Separable Transition-Diagram Compiler* (Conway, 1963) describía un compilador organizado
en **fases que se pasaban el control mutuamente**, sin que ninguna fuera la principal: el analizador
léxico produce un símbolo y **cede el control**; el sintáctico lo consume y **cede de vuelta**.

Ese es exactamente el patrón productor-consumidor que hoy se escribe con generadores, y Conway lo
describió **para un compilador de COBOL, en 1958**.

Y el mismo Conway es el autor de la observación que hoy se llama **ley de Conway** —las organizaciones
diseñan sistemas que copian su estructura de comunicación—, formulada en el mismo contexto.

En el COBOL del lenguaje, lo más cercano a una corrutina son las construcciones de la clase 107:

```cobol
SORT FICHERO
    INPUT PROCEDURE IS FILTRAR
    OUTPUT PROCEDURE IS PROCESAR
```

**`INPUT PROCEDURE` y `OUTPUT PROCEDURE` son corrutinas de verdad**: el `SORT` llama a `FILTRAR` para
pedir el registro siguiente, `FILTRAR` hace `RELEASE` de uno y **devuelve el control**; después el
`SORT` llama a `PROCESAR`, que hace `RETURN` de los ordenados.

```cobol
FILTRAR SECTION.
    PERFORM UNTIL FIN
        READ ENTRADA AT END SET FIN TO TRUE
        NOT AT END RELEASE REG-ORDENAR FROM REG-ENTRADA
        END-READ
    END-PERFORM.
```

**`RELEASE` produce y `RETURN` consume**, y el control va y viene entre el `SORT` y los procedimientos.
Es un canal con el ordenador en medio, en COBOL desde 1968.

Es la corrutina de Conway, en el lenguaje sobre el que la describió.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program tareas
   implicit none
   integer :: v(100), n, ios, i

   character(len=400) :: linea

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   write(*, '(A,I0)') 'max=', maxval(v(1:n))
end program tareas
```

**Lo que esta clase enseña en Fortran.** **Fortran no tiene corrutinas ni canales**, y su modelo es el
de la clase 133: procesos con mensajes o hilos con memoria compartida.

Lo que sí tiene, y encaja en esta clase, son **los eventos de Fortran 2018**:

```fortran
use iso_fortran_env
type(event_type) :: listo[*]

if (this_image() == 1) then
   ! producir datos
   event post (listo[2])            ! avisar a la imagen 2
else if (this_image() == 2) then
   event wait (listo)                ! esperar el aviso
   ! consumir
end if
```

**`event post` y `event wait` son señalización entre imágenes**, y con ellos se construye un canal de
capacidad uno: el productor avisa, el consumidor espera.

Y Fortran 2018 añadió además los **equipos** y la sincronización parcial, que son las piezas para
tuberías distribuidas:

```fortran
sync images ([2, 3])              ! sincronizar solo con esas imágenes
form team (color, mi_equipo)       ! dividir las imágenes en subgrupos
change team (mi_equipo)
   ...                              ! aquí num_images() es el del EQUIPO
end team
```

**Los equipos permiten dividir un cálculo en fases con topologías distintas** —unos procesos hacen la
física, otros la entrada/salida—, que es la arquitectura de tuberías de esta clase a escala de
superordenador.

Y merece decir con claridad lo que Fortran no tiene y por qué no le hace falta: **`async`/`await` y las
corrutinas sirven para no bloquear un hilo mientras se espera entrada/salida** (clase 122), y **un
programa Fortran no espera: calcula**.

Su problema no es la latencia, es el rendimiento agregado, y para eso la respuesta es el paralelismo de
datos, no la concurrencia.

Es un buen recordatorio de que **una característica ausente no siempre es una carencia**: a veces es
que el problema que resuelve no aparece en ese dominio.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Tareas is
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
   Maximo : Integer := Integer'First;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      if Valor > Maximo then
         Maximo := Valor;
      end if;
      Pos := Fin + 1;
   end loop;

   Put ("max=");
   Put (Maximo, Width => 1);
   New_Line;
end Tareas;
```

**Lo que esta clase enseña en Ada.** **La cita de Ada es un canal síncrono**, y esa equivalencia merece
explicarse porque es exacta.

```ada
task Productor is
   entry Dar (X : out Integer);
end Productor;

--  El consumidor llama:
Productor.Dar (Valor);        --  se BLOQUEA hasta que el productor haga accept
```

En Go se escribiría así:

```go
valor := <-canal        // se bloquea hasta que alguien envíe
```

**Son la misma operación.** Un canal sin búfer en Go es un encuentro: emisor y receptor se esperan
mutuamente. La cita de Ada es exactamente eso, con la diferencia de que **el "canal" tiene nombre y
pertenece a una tarea**.

Y Ada llega más lejos en dos aspectos:

**Primero, `select` con guardas** (clase 119), que es el `select` de Go **con condiciones**:

```ada
select
   when Cola_No_Llena =>
      accept Poner (X : Integer) do ... end Poner;
or
   when Cola_No_Vacia =>
      accept Sacar (X : out Integer) do ... end Sacar;
or
   delay 5.0;
   Put_Line ("inactivo");
end select;
```

**`when` delante de cada alternativa** hace que una rama solo esté disponible si la condición se
cumple. En Go hay que simular eso poniendo un canal a `nil`, que es un idioma conocido y menos claro.

**Y segundo, las colas con contrapresión y prioridad** (clase 120), que Go no tiene en el lenguaje.

Y desde Ada 2022 hay además **corrutinas por biblioteca** y **paralelismo estructurado**:

```ada
parallel do
   Tarea_A;
and
   Tarea_B;
end do;
```

**`parallel ... and ... end` de Ada 2022 lanza bloques en paralelo y espera a todos**, con la
sintaxis del propio lenguaje. Es concurrencia estructurada (clase 121) con soporte sintáctico, y muy
pocos lenguajes la tienen así.

Es el mismo camino que Ada lleva recorriendo desde 1983: **poner en la gramática lo que otros dejan a
la biblioteca**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Tareas;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Valor, Maximo: Integer;
  C: Char;
  Hay: Boolean;

begin
  ReadLn(Linea);

  Hay := False;
  Maximo := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Valor := StrToInt(Tok);
        if (not Hay) or (Valor > Maximo) then
        begin
          Maximo := Valor;
          Hay := True;
        end;
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('max=', IntToStr(Maximo));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal **no tiene corrutinas** en el lenguaje, y su historia
contiene una de las mejores implementaciones de la idea: **los `iterator` de Turbo Pascal para
Windows**... que en realidad no existieron.

Lo que sí existió, y es relevante, son **las corrutinas de Modula-2**, el lenguaje siguiente de Wirth:

```text
NEWPROCESS(P, espacio, tamaño, corrutina);
TRANSFER(actual, siguiente);        (* ceder el control explícitamente *)
```

**`TRANSFER` cambia de corrutina guardando el contexto actual**, y era la primitiva sobre la que
Modula-2 construía su concurrencia. Wirth la eligió deliberadamente en lugar de hilos: **una primitiva
mínima sobre la que construir lo demás**.

Es exactamente el modelo de las corrutinas simétricas, y precede a las de Lua y a las de Tcl en
décadas.

En Object Pascal, lo que hay son las capas de la clase 122 —tareas, futuros, `Synchronize`— y **las
funciones anónimas** que permiten escribir el patrón productor-consumidor:

```pascal
Cola := TThreadedQueue<Integer>.Create(100, INFINITE, INFINITE);
TTask.Run(procedure begin
  for var I := 1 to 100 do Cola.PushItem(I);      { productor }
end);
while Cola.PopItem(Valor) = wrSignaled do ...      { consumidor }
```

**`TThreadedQueue<T>` es un canal con capacidad**: `PushItem` bloquea si está llena y `PopItem` si está
vacía. Es contrapresión (clase 120), con la misma forma que las colas sincronizadas de Ada.

Y Free Pascal tiene además algo que se le acerca desde otro lado: **los generadores implementados con
hilos**, y la extensión experimental de corrutinas en algunas ramas.

Merece cerrar señalando la conexión que esta clase revela: **Wirth eligió corrutinas y transferencia
explícita; Hoare y Ada eligieron el encuentro; Hansen eligió el monitor** (clase 121). Los tres
trabajaban a la vez, en los setenta, sobre el mismo problema — y las tres ideas siguen vivas.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((maximo nil))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (when (or (null maximo) (> x maximo))
             (setf maximo x)))
  (format t "max=~D~%" maximo))
```

**Lo que esta clase enseña en Common Lisp.** **Common Lisp no tiene corrutinas en el estándar**, y tiene
la primitiva de la que se derivan todas: **las continuaciones** — aunque no en el estándar, sino en
Scheme.

`call/cc` de Scheme captura **el resto del cálculo como un valor**, y con eso se implementan corrutinas,
generadores, retroceso (clase 118) y `async`/`await`. Es la primitiva más general de control que
existe.

Common Lisp no la tiene —el comité la consideró demasiado costosa de implementar con eficiencia— y el
ecosistema lo resuelve por otras vías:

```lisp
(ql:quickload :cl-cont)              ; continuaciones por transformación de código
(cl-cont:with-call/cc ...)

(ql:quickload :snakes)                ; generadores al estilo Python
(defgenerator contar (n)
  (loop for i from 1 to n do (yield i)))

(ql:quickload :bordeaux-threads)       ; y los hilos, para lo demás
```

**`cl-cont`** merece la explicación porque es un ejemplo excelente de lo que las macros permiten:
**transforma el código a estilo de paso de continuaciones en tiempo de compilación**, con lo que
`call/cc` funciona dentro de su ámbito.

Eso es lo que hace un compilador con `async`/`await` (clase 122) —transformar la función en una máquina
de estados— **escrito como biblioteca**.

Y Lisp tiene una construcción del estándar que da el efecto de un generador en muchos casos, y que ya
apareció en la clase 120: **las macros `with-` con un bloque**.

```lisp
(do-lineas (linea "fichero.txt")     ; una macro propia
  (procesar linea))
```

**El "generador" es una macro que recorre y llama al cuerpo**, que es iteración interna (clase 097) — la
misma solución que Smalltalk con `do:`.

Es la diferencia de fondo de esta clase: **un generador da el control al consumidor; la iteración
interna lo deja en el productor**. Y para la mayoría de los casos, la segunda basta y es más simple.

Cuando no basta —recorrer dos secuencias a la vez, entrelazar— hace falta la corrutina, y ahí Lisp
recurre a las bibliotecas.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc maximizar {} {
    set m ""
    while 1 {
        set x [yield]
        if {$x eq ""} { return $m }
        if {$m eq "" || $x > $m} { set m $x }
    }
}

gets stdin linea

coroutine acum maximizar             ;# se ejecuta hasta el primer yield
foreach x [split [string trim $linea]] {
    acum $x                           ;# ENVIAR un valor a la corrutina
}

puts "max=[acum {}]"
```

**Lo que esta clase enseña en Tcl.** Este programa usa **una corrutina como consumidor**: `yield`
devuelve el control **y el valor que se le envíe al reanudarla**.

```tcl
set x [yield]         ;# suspende, y al reanudar recibe el argumento
acum $x                ;# reanudar, pasando un valor
```

**Eso es un canal**: la corrutina espera datos, el llamante los envía. Y es exactamente la equivalencia
del cierre de esta clase — **una corrutina que recibe por `yield` es el extremo receptor de un canal
de capacidad cero**.

Las corrutinas de Tcl 8.6 tienen tres propiedades que las hacen de las mejores de esta página:

**Primera: no colorean funciones** (clase 122). Cualquier procedimiento llamado desde una corrutina
puede hacer `yield`, sin declarar nada.

**Segunda: `yieldto` permite ceder a otra corrutina directamente**, sin pasar por el llamante:

```tcl
yieldto otraCorrutina $datos      ;# corrutinas SIMÉTRICAS
```

Eso son las corrutinas simétricas —el `TRANSFER` de Modula-2 de esta misma clase— y muy pocos lenguajes
las ofrecen: Python y JavaScript solo tienen las asimétricas, donde `yield` siempre vuelve al llamante.

**Y tercera: se integran con el bucle de eventos** (clase 119), que es lo que las hace útiles para
entrada/salida:

```tcl
yieldto fileevent $canal readable [info coroutine]
```

Y todo eso fue posible por el cambio de implementación de la clase 127: **NRE**, que sacó la pila del
intérprete de la pila de C.

Y Tcl 8.7 añade lo que faltaba para depurarlas:

```tcl
coroprobe $nombre { info level }     ;# ejecutar código DENTRO de una corrutina suspendida
coroinject $nombre { ... }            ;# inyectarle código
```

**Inspeccionar una corrutina suspendida** es un problema conocido en todos los entornos asíncronos, y
Tcl lo resolvió con dos comandos.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(max);

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

print "max=", max(@v), "\n";
```

**Lo que esta clase enseña en Perl.** Perl **no tiene corrutinas ni canales en el núcleo**, y el
ecosistema los ha construido de tres formas distintas, que ilustran bien las opciones de esta clase.

**Primera: con hilos y colas** —el modelo directo—:

```perl
use threads;
use Thread::Queue;
my $cola = Thread::Queue->new;
threads->create(sub { while (defined(my $x = $cola->dequeue)) { ... } });
$cola->enqueue(1, 2, 3);
$cola->end;
```

**`Thread::Queue` es un canal con bloqueo**, con la advertencia de la clase 121: los hilos de Perl son
caros.

**Segunda: con clausuras, que dan generadores sin corrutinas**:

```perl
sub contador {
    my $n = 0;
    return sub { return $n++ };       # cada llamada avanza el estado
}
my $g = contador();
$g->(); $g->();                        # 0, 1
```

**Una clausura con estado es un generador limitado**: puede producir valores, y **no puede suspenderse
en medio de un bucle**. Para lo segundo hace falta una corrutina de verdad.

**Y tercera: `Coro`**, una biblioteca de CPAN que implementa corrutinas reales manipulando la pila de C:

```perl
use Coro;
use Coro::Channel;
my $canal = Coro::Channel->new(4);      # canal con CAPACIDAD
async { $canal->put($_) for 1 .. 10 };
async { while (defined(my $x = $canal->get)) { ... } };
cede;
```

**`Coro::Channel` con capacidad es exactamente un canal de Go**, con contrapresión (clase 120), y
`async` crea una corrutina.

`Coro` es una obra de ingeniería notable —cambia pilas de C a mano— y por eso es frágil entre versiones
de Perl, lo que ilustra el problema de fondo: **añadir corrutinas a un intérprete que no las previó
exige tocar su núcleo**.

Es exactamente lo que Tcl tuvo que hacer con NRE (clase 127), y lo que Perl no ha hecho en el núcleo.
Por eso hoy el camino recomendado es `IO::Async` con futuros y `Future::AsyncAwait` (clase 122), que
transforman el código en lugar de manipular la pila.

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
    if (v.empty()) return 1;

    std::cout << "max=" << *std::max_element(v.begin(), v.end()) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** **C++20 añadió corrutinas**, y su diseño es el más peculiar de esta
página: **el lenguaje aporta la transformación y no aporta los tipos** (clase 122).

```cpp
generator<int> contar(int n) {
    for (int i = 0; i < n; ++i)
        co_yield i;              // suspende y produce un valor
}
```

Tres palabras clave —`co_await`, `co_yield`, `co_return`— y **el compilador transforma la función en
una máquina de estados** con su marco guardado.

Y ahí está la propiedad que hace especiales a las corrutinas de C++: **la elisión del marco**.

Si el compilador puede demostrar que el marco de la corrutina no sobrevive al llamante, **puede
colocarlo en la pila y evitar la reserva de memoria**. En el mejor caso, **una corrutina cuesta lo
mismo que un bucle escrito a mano**.

Es la promesa de C++ de siempre —abstracción sin coste— aplicada a la concurrencia.

El precio es la complejidad: **para usar `co_yield` hace falta un tipo `generator` con su
`promise_type`**, y escribirlo a mano es notoriamente difícil. C++23 añadió por fin
`std::generator`, y para el resto están cppcoro, Boost.Asio y libunifex.

Y sobre canales, C++ **no tiene ninguno en el estándar**, lo cual sorprende. La construcción se hace a
mano:

```cpp
std::queue<T> cola;
std::mutex m;
std::condition_variable cv;      // el trío clásico
```

O con bibliotecas: `boost::fibers::buffered_channel`, las colas concurrentes de TBB, `moodycamel`.

**La propuesta de ejecutores —`std::execution`, prevista para C++26—** traerá por fin el modelo
completo: planificadores, remitentes y receptores, con los que se componen operaciones asíncronas de
forma tipada.

Es un buen ejemplo de cómo evoluciona C++: **primero el mecanismo de coste cero, y las políticas
después**.

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

dcl-pi TAREAS;
  entrada char(200) const;
end-pi;

dcl-s texto  varchar(200);
dcl-s tok    varchar(20) inz('');
dcl-s c      char(1);
dcl-s i      int(10);
dcl-s valor  int(10);
dcl-s maximo int(10);
dcl-s hay    ind inz(*off);

texto = %trimr(entrada);

for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      valor = %int(tok);
      if not hay or valor > maximo;
        maximo = valor;
        hay = *on;
      endif;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('max=' + %char(maximo));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG no tiene corrutinas, y **la plataforma tiene el canal**: las
colas de datos de las clases 096, 119 y 122.

```text
Trabajo A → [cola de datos] → Trabajo B
```

Y merece comparar esa cola con un canal de Go, porque las diferencias son instructivas:

| | Canal de Go | Cola de datos de IBM i |
|---|---|---|
| Ámbito | dentro de un proceso | **entre trabajos, y entre máquinas** |
| Persistencia | no | **sí, opcional** |
| Sobrevive a un fallo | no | **sí** |
| Disciplina | FIFO | **FIFO, LIFO o por CLAVE** |
| Coste por operación | nanosegundos | microsegundos |
| Contrapresión | por capacidad | por tamaño máximo |

**La cola de datos es un canal persistente y distribuido**, tres órdenes de magnitud más cara y con
garantías que un canal en memoria no puede dar.

Y la disciplina **por clave** es la que no tiene equivalente: permite que varios consumidores esperen
en la misma cola y **cada uno reciba solo los mensajes con su clave** — que es lo que hace falta para
el patrón petición-respuesta de la clase 122.

Y RPG tiene además la construcción que se acerca a un generador, aunque no se llame así: **el ciclo de
lectura de un fichero**.

```rpgle
setll (*loval) MOVIMIENTOS;
dow *on;
  reade MOVIMIENTOS;
  if %eof(MOVIMIENTOS);
    leave;
  endif;
  // procesar
enddo;
```

**`reade` produce el registro siguiente sin cargar el fichero**, manteniendo la posición en el índice —
que es exactamente lo que hace un generador: **estado suspendido entre invocaciones**.

Es la conclusión que esta parte del curso repite: **los conceptos de esta clase existen en las
plataformas de gestión con otros nombres y a otra escala**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 tareas: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare (i, valor, maximo) fixed binary(31);
    declare hay bit(1) initial('0'b);

    get edit (linea) (a(200));
    linea = trim(linea);

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             valor = tok;
             if ^hay | valor > maximo then do;
                maximo = valor;
                hay = '1'b;
             end;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('max=' || trim(char(maximo)));

 end tareas;
```

**Lo que esta clase enseña en PL/I.** PL/I no tiene corrutinas ni canales, y tiene las piezas de la
clase 119 con las que se construye el patrón:

```pli
 declare listo(4) event;
 call productor(datos) task(t1) event(listo(1));
 call consumidor(datos) task(t2) event(listo(2));
 wait(listo);
```

Y una construcción que se acerca a un canal más de lo que parece: **la multitarea con `event` como
señal de disponibilidad**.

Con un búfer compartido, un evento de "hay datos" y otro de "hay hueco", **se construye un canal con
contrapresión** — que es exactamente cómo se implementa un canal por debajo en cualquier runtime.

Lo interesante de esta clase en PL/I es otra cosa, y conecta con COBOL de esta misma página: **PL/I y
COBOL son los dos lenguajes sobre los que se describieron las corrutinas**.

Conway describió el concepto en 1958 para un compilador de COBOL, y el mismo patrón se usó en los
compiladores de PL/I: **fases que se pasan el control produciendo y consumiendo símbolos**.

Y hay un uso de corrutinas en el mundo del mainframe que sigue vivo y que casi nadie llama así: **las
salidas de usuario de las utilidades de ordenación**.

```text
DFSORT con EXIT E15 (entrada) y E35 (salida)
```

**El programa de salida E15 se llama para cada registro de entrada**, decide si lo pasa, lo modifica o
lo descarta, y devuelve el control. **E35 hace lo mismo con la salida.**

Es la misma estructura que el `SORT` de COBOL de esta página, y es exactamente el patrón de Conway: **el
control va y viene entre la utilidad y el código del usuario**, sin que ninguno sea el programa
principal.

Y ese patrón —**el marco de trabajo llama a tu código, no al revés**— es la inversión de control de la
clase 119, y estaba en las utilidades de ordenación de los años sesenta.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
TAREAS ; Tareas, corrutinas y canales -- clase 134
 read linea
 set maximo = ""
 for i=1:1:$length(linea, " ") do
 . set x = $piece(linea, " ", i)
 . if maximo = "" set maximo = x quit
 . if x > maximo set maximo = x
 write "max=", maximo, !
 quit
```

**Lo que esta clase enseña en M.** M **no tiene corrutinas ni canales**, y tiene la construcción que en
la práctica hace de generador y que ya ha aparecido en varias clases: **`$order`**.

```mumps
 set id = ""
 for  set id = $order(^PACIENTE(id))  quit:id=""  do procesar(id)
```

**`$order` devuelve el subíndice siguiente y mantiene la posición implícita en el argumento**, así que
el bucle recorre diez millones de registros **sin cargar nada y sin cursor** (clase 120).

Eso es un generador: **estado suspendido entre invocaciones, un elemento cada vez, memoria constante**.
Y funciona igual sobre memoria y sobre disco.

Y para el canal, M usa lo de la clase 120: **un *global* como cola**.

```mumps
 ; productor
 set ^COLA($increment(^COLA)) = mensaje

 ; consumidor
 for  set n = $order(^COLA(""))  quit:n=""  do
 . set msg = ^COLA(n)
 . kill ^COLA(n)
 . do procesar(msg)
```

**`$increment` es atómico**, así que varios productores no colisionan, y el *global* es persistente y
transaccional.

Comparado con un canal de Go, tiene las mismas diferencias que las colas de IBM i de esta página:
**mucho más caro y con garantías que un canal en memoria no puede dar** — sobrevive a la caída del
consumidor, se puede inspeccionar desde otro proceso y participa en transacciones.

Y para la espera, M tiene `lock` con tiempo límite (clase 121) y `hang`:

```mumps
 for  quit:$data(^COLA)  hang 0.1        ; sondeo
 lock +^COLA:5                            ; o esperar el bloqueo
```

**El sondeo es la forma tradicional**, y es una carencia real: **M no tiene una primitiva de espera
sobre un *global***. Las implementaciones modernas la añaden —eventos en IRIS, y en YottaDB se usan
mecanismos del sistema— pero el lenguaje base obliga a sondear.

Es de las pocas cosas de esta parte donde M queda claramente por detrás, y merece decirlo.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

Transcript show: 'max=', (v inject: v first into: [ :a :b | a max: b ]) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk **puede implementar corrutinas dentro del propio
lenguaje**, y esa capacidad viene de lo que la clase 127 explicaba: **el contexto de pila es un
objeto**.

```smalltalk
| ctx |
ctx := thisContext.               "el marco actual, como objeto"
ctx suspend.                       "guardarlo"
ctx resume: valor.                  "y reanudarlo después"
```

**Guardar un contexto y reanudarlo es exactamente una corrutina**, y en Smalltalk no hace falta soporte
del compilador ni palabras clave: **es manipulación de objetos**.

Sobre eso, Pharo implementa generadores en una clase de biblioteca:

```smalltalk
| g |
g := Generator on: [ :salida |
        1 to: 10 do: [ :i | salida yield: i ] ].
g next.                            "1"
g next.                             "2"
g do: [ :cada | ... ].
```

**`Generator` está escrito en Smalltalk**, usando `Process` y semáforos por debajo, y es un buen
ejemplo del argumento de la clase 107: **lo que en otros lenguajes es sintaxis, aquí es una clase**.

Y para los canales, la biblioteca tiene `SharedQueue` (clases 120 y 121):

```smalltalk
| cola |
cola := SharedQueue new.
[ 1 to: 100 do: [ :i | cola nextPut: i ] ] fork.
[ [ true ] whileTrue: [ procesar: cola next ] ] fork.
```

**`cola next` bloquea si está vacía**, que es la mitad de un canal; con `SharedQueue2` y capacidad
limitada se obtiene la contrapresión.

Y merece cerrar esta clase con la observación que la recorre entera, y que Smalltalk ilustra mejor que
nadie: **corrutina, canal, generador, continuación y excepción reanudable son todos la misma
capacidad** —guardar y reanudar un estado de ejecución— **vista desde ángulos distintos**.

En Smalltalk, las cinco se construyen sobre la misma pieza: **el contexto como objeto**. Y por eso el
depurador puede reanudar desde un marco (clase 127), las excepciones pueden `resume:` (clase 116) y los
generadores son una clase de biblioteca.

**Una primitiva, cinco características.** Es el mejor argumento a favor de exponer el mecanismo en
lugar de las políticas.

---

## Y de vuelta a la clase

Lo transferible: **un canal y una corrutina son la misma idea vista desde dos sitios**. Una corrutina
que hace `yield` de un valor a otra es, de hecho, un canal de capacidad cero; y un canal con un
productor y un consumidor es un par de corrutinas. Lo que cambia es quién controla el flujo: con
corrutinas lo controla el código; con canales, la disponibilidad de los datos. Cuando diseñes,
pregúntate **qué debe esperar a qué**, y la elección se decide sola.

⏮️ [Volver a la clase 134](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
