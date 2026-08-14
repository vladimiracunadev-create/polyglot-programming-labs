# -*- coding: utf-8 -*-
"""Parte 7, lote N — clase 120. Ver `vivos_parte7.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 120 — Reactivo y flujos de datos
# ---------------------------------------------------------------------------
SPECS["120"] = dict(
    gancho="""
Filtrar los pares y doblarlos: **una tubería de transformaciones sobre un flujo**. La idea es de 1973
—las tuberías de Unix— y aquí tiene tres representantes de primera: **Tcl, cuyos canales unifican
ficheros, tuberías y sockets**; **Perl, cuyo `<>` con `-n` es un filtro de flujo en la línea de
órdenes**; y **COBOL, cuyo procesamiento por lotes ES un flujo** que lleva sesenta años moviendo datos
que no caben en memoria.
""",
    porque="""
Aquí el concepto es el **procesamiento incremental de una secuencia sin materializarla**, y estos
lenguajes lo enseñan porque lo llevan haciendo desde antes de que se llamara así. **Un programa COBOL
de lote lee un registro, lo transforma y lo escribe** — memoria constante, volumen ilimitado. Eso es
exactamente lo que hoy se vende como procesamiento de flujos.

Y **C++20 con las vistas perezosas** y **Fortran con `do concurrent`** enseñan la otra mitad: cuando
la tubería se declara en lugar de escribirse, **el compilador o el motor pueden fusionar las etapas y
paralelizarlas**.
""",
    cierre="""
Lo transferible: **lo que distingue un flujo de una lista es que no cabe**. Con una lista puedes
recorrerla dos veces, saber su tamaño y ordenarla; con un flujo, no. Esa restricción es la que obliga
a pensar en una pasada, con memoria acotada, y la que hace que las mismas operaciones —filtrar, mapear,
agregar por ventanas— aparezcan en Unix, en Spark, en Kafka y en un lote de COBOL. **Si tus datos
caben en memoria, no necesitas un flujo; si no caben, no tienes otra opción.**
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. FLUJO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2)  COMP VALUE 0.
01  I       PIC 9(4)  COMP.
01  L       PIC 9(4)  COMP.
01  VALOR   PIC S9(9) COMP-3.
01  SALIDA  PIC X(200) VALUE SPACES.
01  SPOS    PIC 9(4) COMP VALUE 1.
01  ED      PIC -(17)9.
01  TXT     PIC X(20).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    *> Una pasada: filtrar y transformar sobre la marcha
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM PROCESAR
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM PROCESAR

    COMPUTE L = SPOS - 1
    DISPLAY "stream=" SALIDA(1:L)
    STOP RUN.

PROCESAR.
    IF TLEN > 0
        COMPUTE VALOR = FUNCTION NUMVAL(TOKEN)
        IF FUNCTION MOD(VALOR, 2) = 0
            COMPUTE VALOR = VALOR * 2
            MOVE VALOR TO ED
            MOVE FUNCTION TRIM(ED) TO TXT
            MOVE 0 TO L
            INSPECT FUNCTION REVERSE(TXT) TALLYING L FOR LEADING SPACE
            COMPUTE L = 20 - L
            IF SPOS > 1
                MOVE "-" TO SALIDA(SPOS:1)
                ADD 1 TO SPOS
            END-IF
            MOVE TXT(1:L) TO SALIDA(SPOS:L)
            ADD L TO SPOS
        END-IF
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
""", """
**Lo que esta clase enseña en COBOL.** Este programa hace **una sola pasada** filtrando y transformando
sobre la marcha, y eso no es una casualidad de este ejercicio: **es la arquitectura del procesamiento
por lotes**.

```cobol
PERFORM UNTIL FIN-FICHERO
    READ ENTRADA AT END SET FIN-FICHERO TO TRUE
    NOT AT END
        IF CUMPLE-CRITERIO
            PERFORM TRANSFORMAR
            WRITE REG-SALIDA
        END-IF
    END-READ
END-PERFORM
```

**Memoria constante, volumen ilimitado.** Un programa así procesa cien millones de registros con los
mismos kilobytes que necesita para uno, porque **nunca tiene más de un registro en memoria**.

Y esa restricción es la del cierre de esta clase, aceptada desde el principio: **los datos nunca
cupieron**. En 1960 la memoria se medía en kilobytes y las cintas en millones de registros; **la única
arquitectura posible era el flujo**.

De ahí salen las técnicas que definen el oficio y que hoy tienen otros nombres:

- **Ordenar y procesar por grupos** (clase 098): el `GROUP BY` de un flujo.
- **El algoritmo de línea balanceada**: recorrer **dos ficheros ordenados a la vez** comparando claves,
  que es un `JOIN` de fusión en una pasada y con memoria constante.
- **Los puntos de control**: guardar el progreso cada N registros para poder reanudar tras un fallo.
  Es el **punto de comprobación** de Kafka y de Spark Streaming.
- **Las cadenas de trabajos** con JCL (clase 115): la salida de un paso es la entrada del siguiente.

Esa última es literalmente una tubería, escrita en JCL en lugar de con `|`, y con una diferencia
importante: **los pasos son secuenciales y el intermedio se guarda en disco**, así que se puede
reanudar desde el paso que falló.

Es el compromiso opuesto al de Unix —que encadena procesos en paralelo sin guardar nada— y es el
correcto cuando el proceso dura ocho horas y no se puede repetir entero.

Cuando alguien describe hoy una arquitectura de datos con etapas, particiones y puntos de control,
está describiendo la sala de máquinas de un banco de 1975.
"""),
        "fortran": ("""
program flujo
   implicit none
   integer, allocatable :: v(:), pares(:)
   integer :: n, ios, i
   character(len=400) :: linea, salida
   character(len=20)  :: buf

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      if (allocated(v)) deallocate(v)
      allocate(v(i))
      read(linea, *, iostat=ios) v
      if (ios /= 0) exit
      n = i
   end do
   if (allocated(v)) deallocate(v)
   allocate(v(n))
   read(linea, *) v

   !  la tubería, en una línea: filtrar y transformar
   pares = pack(v, mod(v, 2) == 0) * 2

   salida = ''
   do i = 1, size(pares)
      write(buf, '(I0)') pares(i)
      if (i == 1) then
         salida = trim(buf)
      else
         salida = trim(salida) // '-' // trim(buf)
      end if
   end do

   write(*, '(A)') 'stream=' // trim(salida)
end program flujo
""", """
**Lo que esta clase enseña en Fortran.** `pack(v, mod(v, 2) == 0) * 2` es **la tubería entera en una
expresión**: filtrar con `pack` y transformar con la aritmética de arreglos (clase 117).

Y aquí hay una diferencia importante con el resto de la página, que el cierre de esta clase pide
señalar: **eso NO es un flujo**. `pack` construye un arreglo nuevo con todos los elementos, en
memoria. Es procesamiento por lotes en el sentido de la palabra, no incremental.

Fortran no tiene evaluación perezosa ni generadores, y para su dominio eso es lo correcto: **los datos
de una simulación caben en memoria a propósito**, porque el objetivo es recorrerlos muchas veces a
toda velocidad, no una vez.

Donde Fortran sí hace algo que esta clase reconoce es en **el flujo de datos entre procesos**:

```fortran
real :: campo(1000)[*]                    ! coarray: distribuido entre imágenes
campo(:)[2] = campo(:)[1]                  ! enviar datos a otra imagen
sync images ([2, 3])                        ! sincronizar
```

Los **coarrays** de la clase 107 son intercambio de datos entre procesos con sintaxis de arreglo, y con
ellos se construyen las tuberías de los códigos de simulación: **cada imagen procesa una porción del
dominio y comunica sus bordes a las vecinas**.

Ese patrón —**descomposición del dominio con intercambio de halos**— es cómo funcionan los modelos
climáticos y los de fluidos, y **es procesamiento de flujos distribuido** con otro vocabulario: los
datos fluyen entre nodos en cada paso de tiempo, con memoria acotada por nodo.

Y `do concurrent` (clase 114) da la otra mitad:

```fortran
do concurrent (i = 1:n, mod(v(i), 2) == 0)     ! con MÁSCARA, Fortran 2008
   w(i) = v(i) * 2
end do
```

**Un bucle con filtro que el compilador puede repartir entre núcleos o mandar a una GPU.** Es la misma
tubería del programa de arriba, expresada de forma que la máquina la pueda dividir.

Es el argumento del cierre por el otro lado: **declarar la tubería permite que otro decida cómo
ejecutarla** — y en Fortran ese otro reparte entre 40.000 núcleos.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Flujo is
   Linea   : String (1 .. 400);
   Ultimo  : Natural;
   Pos     : Integer := 1;
   Valor   : Integer;
   Fin     : Positive;
   Primero : Boolean := True;
begin
   Get_Line (Linea, Ultimo);

   Put ("stream=");

   --  una sola pasada: filtrar y transformar sobre la marcha
   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      if Valor mod 2 = 0 then
         if not Primero then
            Put ("-");
         end if;
         Put (Valor * 2, Width => 1);
         Primero := False;
      end if;
      Pos := Fin + 1;
   end loop;

   New_Line;
end Flujo;
""", """
**Lo que esta clase enseña en Ada.** Ada no tiene vistas perezosas ni generadores, y **tiene el modelo
de flujos entre tareas más elaborado de esta página**, con una construcción hecha exactamente para
esto: **las colas sincronizadas**.

```ada
with Ada.Containers.Unbounded_Synchronized_Queues;

package Colas is new Ada.Containers.Unbounded_Synchronized_Queues (...);

task Productor;
task Filtro;
task Consumidor;

task body Filtro is
   X : Integer;
begin
   loop
      Entrada.Dequeue (X);              --  se BLOQUEA si está vacía
      if X mod 2 = 0 then
         Salida.Enqueue (X * 2);         --  se bloquea si está llena
      end if;
   end loop;
end Filtro;
```

**Cada etapa de la tubería es una tarea, y las colas las conectan.** `Dequeue` bloquea si no hay
datos, `Enqueue` bloquea si la cola acotada está llena — **eso es contrapresión**, el mecanismo que
impide que un productor rápido ahogue a un consumidor lento.

**La contrapresión es el problema central de los sistemas reactivos modernos** —es lo que definen las
especificaciones de Reactive Streams y lo que implementan Akka, RxJava y Project Reactor— y en Ada es
el comportamiento por defecto de una cola acotada, desde 2005.

Y para tiempo real, Ada tiene la variante con prioridades:

```ada
package Colas is new Ada.Containers.Bounded_Priority_Queues (...);
pragma Queuing_Policy (Priority_Queuing);
```

Con eso, **el elemento más urgente se atiende primero**, y la política de encolado es una directiva del
programa (clase 096).

Ese modelo —tareas conectadas por colas con contrapresión y prioridades— es la arquitectura clásica de
un sistema de control: **adquisición de datos, filtrado, decisión y actuación**, cada etapa con su
periodo y su prioridad. Y es lo que Ada lleva soportando en el lenguaje desde 1983, con `select` y
`delay until` (clase 107).

Es un buen recordatorio de que **lo reactivo no lo inventó la web**: lo inventaron los sistemas de
control, donde llegar tarde tiene consecuencias físicas.
"""),
        "pascal": ("""
program Flujo;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok, Salida: string;
  I, Valor: Integer;
  C: Char;

begin
  ReadLn(Linea);

  Salida := '';
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Valor := StrToInt(Tok);
        if Valor mod 2 = 0 then
        begin
          if Salida <> '' then Salida := Salida + '-';
          Salida := Salida + IntToStr(Valor * 2);
        end;
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('stream=', Salida);
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal no tiene flujos perezosos en el lenguaje, y **su
abstracción de flujo es una de las mejor diseñadas de su época**: la jerarquía `TStream`.

```pascal
TStream                        { la clase abstracta }
  TFileStream                   { un fichero }
  TMemoryStream                  { memoria }
  TStringStream                   { una cadena }
  TBufferedFileStream              { con búfer }
  TZDecompressionStream             { descompresión al vuelo }
  TCryptoStream                      { cifrado }
```

**Todas responden a `Read`, `Write`, `Seek` y `CopyFrom`**, así que se componen:

```pascal
Origen := TFileStream.Create('datos.gz', fmOpenRead);
Descomp := TDecompressionStream.Create(Origen);
Destino.CopyFrom(Descomp, 0);
```

Eso es **una tubería de flujos envueltos**: cada uno lee del anterior y transforma. Es exactamente el
modelo de `InputStream` de Java y de `Stream` de .NET, y es de 1995 — con el mismo autor detrás en el
caso de .NET (clase 073).

Y para el estilo reactivo con eventos, Delphi tiene lo que su modelo pide: **los eventos de progreso**.

```pascal
Descarga.OnProgress := procedure(Sender: TObject; Leidos: Int64)
                       begin ActualizarBarra(Leidos) end;
```

Un flujo largo **notifica su avance**, que es lo que un `Observable` hace con `onNext`.

Free Pascal moderno y Delphi tienen además `TTask` y `TParallel` para tuberías concurrentes:

```pascal
TParallel.For(1, N, procedure(I: Integer)
                    begin Procesar(I) end);
```

Y Spring4D trae la evaluación perezosa que falta:

```pascal
Resultado := TEnumerable.From<Integer>(Origen)
               .Where(EsPar)
               .Select(Doblar);       { PEREZOSO: no calcula hasta recorrer }
```

Esa pereza es lo que distingue una tubería de flujo de una cadena de transformaciones sobre listas: **sin
ella, cada etapa construye una colección intermedia completa**, que es lo que el cierre de esta clase
dice que no se puede permitir cuando los datos no caben.
"""),
        "lisp": ("""
(let ((salida '()))
  (loop for x = (read *standard-input* nil nil)
        while x
        when (evenp x)                     ; filtrar
          do (push (* 2 x) salida))         ; y transformar, en la misma pasada
  (format t "stream=~{~D~^-~}~%" (nreverse salida)))
""", """
**Lo que esta clase enseña en Common Lisp.** El `loop` con `when` hace **filtrado y transformación en
una sola pasada**, leyendo del flujo de entrada elemento a elemento — sin materializar la lista
completa.

Y Lisp tiene la construcción que define este paradigma y que no está en el estándar pero sí en su
tradición: **los flujos perezosos**.

*Structure and Interpretation of Computer Programs* (Abelson y Sussman, 1985) dedica su capítulo 3.5 a
construirlos, y la técnica es de una economía notable:

```lisp
(defmacro cons-flujo (a b)
  `(cons ,a (lambda () ,b)))          ; el resto es una FUNCIÓN sin evaluar

(defun flujo-resto (s) (funcall (cdr s)))

(defun enteros-desde (n)
  (cons-flujo n (enteros-desde (1+ n))))   ; una lista INFINITA
```

**`(enteros-desde 1)` es un flujo infinito** que ocupa dos celdas: el primer elemento y una promesa de
calcular el resto. Filtrar y transformar sobre él da otros flujos infinitos, y **solo se calcula lo que
se pide**.

Con eso, SICP construye la criba de Eratóstenes como un flujo infinito de primos y resuelve ecuaciones
diferenciales con series perezosas. Es uno de los capítulos más influyentes de la historia de la
enseñanza de la programación.

Y ahí está la conexión que esta clase quiere marcar: **los generadores de Python, los iteradores
perezosos de Rust, las vistas de C++20 y los `Observable` de RxJS son todos esa misma idea** — retrasar
el cálculo hasta que alguien pida el elemento siguiente.

En Common Lisp moderno, el ecosistema lo trae hecho:

```lisp
(ql:quickload :series)              ; series: tuberías FUSIONADAS al compilar
(ql:quickload :snakes)               ; generadores al estilo Python
```

**La biblioteca `series`** merece mención especial: sus tuberías se **fusionan en tiempo de
compilación** en un solo bucle, sin estructuras intermedias. Es exactamente lo que hacen las vistas de
C++20 y la fusión de flujos de Haskell — con macros, y en 1989.
"""),
        "tcl": ("""
gets stdin linea

set salida {}
foreach x [split [string trim $linea]] {
    if {$x % 2 == 0} {
        lappend salida [expr {$x * 2}]
    }
}

puts "stream=[join $salida -]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl no tiene flujos perezosos como valores, y **tiene la
abstracción de flujo más completa de esta página: los canales** (clase 104).

Un canal unifica **ficheros, tuberías a otros procesos, sockets TCP, dispositivos serie y memoria**
bajo la misma interfaz. Y desde Tcl 8.6 se pueden **apilar**:

```tcl
set c [open "datos.gz" rb]
zlib push gunzip $c                    ;# descomprimir al vuelo
fconfigure $c -encoding utf-8           ;# y decodificar
while {[gets $c linea] >= 0} { ... }
```

**`zlib push`** inserta una transformación **en el canal**, así que `gets` lee líneas de texto de un
fichero comprimido sin que el código lo sepa. Es exactamente la tubería de flujos envueltos de la
página de Pascal, hecha con un comando.

Y hay más transformaciones apilables: `tls import` para cifrado, y **canales definidos por el usuario**
con `chan create`:

```tcl
chan create {read write} miManejador     ;# un canal implementado en TCL
```

Un canal cuyo comportamiento lo define un procedimiento Tcl. Con eso se construyen canales que
transforman, que registran o que hablan un protocolo — **y el resto del programa los usa como
ficheros**.

Sobre lo reactivo, Tcl tiene la pieza que hace de todo esto un sistema: **`fileevent` sobre el bucle
de eventos** (clase 119).

```tcl
fconfigure $c -blocking 0
fileevent $c readable {
    if {[gets $c linea] >= 0} { procesar $linea }
}
vwait forever
```

**Entrada y salida no bloqueante dirigida por eventos, en 1990**, sobre canales que pueden ser ficheros
o sockets. Es la arquitectura de Node.js con quince años de antelación, y es la razón de que Tcl se
usara tanto para servidores y automatización de red.

Y `chan copy` cierra el cuadro:

```tcl
chan copy $origen $destino -command { ... }     ;# copia ASÍNCRONA, con callback
```

Copiar un flujo entero sin bloquear y avisar al terminar. Es `pipe()` de Node, en un comando.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

#  la tubería: filtrar y transformar
my @salida = map { $_ * 2 } grep { $_ % 2 == 0 } split ' ', $linea;

print "stream=", join('-', @salida), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `map { ... } grep { ... } split ...` **es una tubería escrita de
derecha a izquierda**, y encadenar `map`, `grep` y `sort` es el estilo idiomático de Perl desde 1987
(clase 117).

Con la salvedad que el cierre de esta clase pide: **eso construye listas intermedias completas**. Para
datos que no caben, Perl tiene la forma correcta y es la que lo hizo famoso:

```perl
while (my $linea = <$fh>) {          # UN registro a la vez
    next unless $linea =~ /ERROR/;    # filtrar
    print transformar($linea);         # transformar y emitir
}
```

**Memoria constante, fichero de cualquier tamaño.** Es el mismo bucle que el COBOL de esta página, en
cuatro líneas.

Y Perl lo lleva al extremo con las opciones de la línea de órdenes:

```bash
perl -ne 'print if /ERROR/' enorme.log
perl -lane 'print $F[2] if $F[1] > 100' datos.txt
cat a.log | perl -pe 's/viejo/nuevo/' | sort | uniq -c
```

**`-n`** envuelve el programa en un bucle de lectura; **`-p`** además imprime; **`-a`** parte cada
línea en `@F`; **`-l`** gestiona los saltos de línea. Con eso, **un filtro de flujo cabe en la línea de
órdenes**, y Perl se convierte en una etapa más de una tubería de Unix.

Esa es la aportación de Perl a esta clase, y es cultural más que técnica: **hizo que escribir un filtro
de flujo fuera tan barato como escribir un comando**. Durante veinte años, buena parte del
procesamiento de registros del mundo pasó por una de esas líneas.

Y Perl tiene además los **descriptores atados a procesos**, que son tuberías de verdad:

```perl
open(my $orden, '-|', 'ls -l') or die;     # LEER de otro proceso
open(my $envio, '|-', 'sort') or die;       # ESCRIBIR a otro proceso
```

Con eso se componen procesos externos como etapas, que es lo que hace `|` en el shell, con la
diferencia de que **aquí el filtro intermedio está escrito en Perl**.
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

int main() {
    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};

    std::string salida;
    for (int x : v) {
        if (x % 2 != 0) continue;         // filtrar
        if (!salida.empty()) salida += '-';
        salida += std::to_string(x * 2);   // transformar
    }

    std::cout << "stream=" << salida << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** El programa está escrito en C++17. **Con C++20, esta clase es una
tubería declarativa**:

```cpp
#include <ranges>

auto tuberia = v
    | std::views::filter([](int x) { return x % 2 == 0; })
    | std::views::transform([](int x) { return x * 2; });

for (int x : tuberia) { ... }
```

Y hay tres propiedades que hacen de esto un flujo de verdad, no una cadena de transformaciones sobre
listas:

1. **Es perezoso.** `tuberia` no calcula nada al construirse; cada elemento se procesa cuando el bucle
   lo pide.
2. **No hay contenedores intermedios.** El filtro y la transformación se aplican al mismo elemento
   antes de pasar al siguiente — **fusión de etapas**.
3. **El compilador lo integra todo en línea**, así que el bucle final compila a lo mismo que el bucle
   escrito a mano de arriba. **Coste cero.**

Esa tercera propiedad es lo que separa a C++ de casi todos: en Java o en Python, una tubería de
`Stream` tiene indirección en cada etapa.

Y C++20 añadió las vistas que hacen de esto un procesador de flujos:

```cpp
std::views::take(100)          std::views::drop(10)
std::views::take_while(pred)    std::views::chunk(4)      // C++23
std::views::iota(0)              std::views::split(',')
std::views::join                  std::views::zip           // C++23
```

**`std::views::iota(0)` es un flujo infinito**, y con `take(5)` se consumen cinco elementos. Es la
misma idea que los flujos perezosos de SICP de la página de Lisp, con tipos y sin coste.

Para flujos de verdad —datos que llegan por red, ficheros enormes— C++ usa **Boost.Asio** y las
corrutinas de C++20 (clase 122), y las bibliotecas de la comunidad como **RxCpp** implementan el modelo
reactivo completo con contrapresión.

Y `std::generator` (C++23) da por fin los generadores perezosos con sintaxis directa:

```cpp
std::generator<int> pares(int n) {
    for (int i = 0; i < n; ++i)
        if (i % 2 == 0) co_yield i * 2;
}
```
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi FLUJO;
  entrada char(200) const;
end-pi;

dcl-s texto  varchar(200);
dcl-s tok    varchar(20) inz('');
dcl-s c      char(1);
dcl-s i      int(10);
dcl-s valor  int(10);
dcl-s salida varchar(200) inz('');

texto = %trimr(entrada);

// una sola pasada: filtrar y transformar
for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      valor = %int(tok);
      if %rem(valor : 2) = 0;
        if salida <> '';
          salida += '-';
        endif;
        salida += %char(valor * 2);
      endif;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('stream=' + salida);

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Como COBOL, el RPG de producción **es procesamiento de flujos por
naturaleza**: leer un registro, decidir, escribir, siguiente. Y como en COBOL, la razón es que los
datos nunca cupieron.

Lo que RPG aporta a esta clase es lo que la plataforma pone encima, y son tres cosas que hoy tienen
nombres de moda.

**Las colas de datos como conectores de tubería** (clases 096 y 119):

```text
Programa A → [cola de datos] → Programa B → [cola] → Programa C
```

Cada programa es una etapa; las colas los conectan; **son persistentes y con reparto entre varios
consumidores**. Es una arquitectura de microservicios con mensajería, montada con objetos del sistema
operativo, desde los años ochenta.

**El registro de diario como flujo de eventos** (clase 114):

```text
STRJRNPF FILE(CLIENTES) IMAGES(*BOTH)
```

**Cada cambio de cada fila queda registrado en orden**, con la imagen anterior y la posterior. Y ese
diario **se puede leer como un flujo**:

```sql
SELECT * FROM TABLE(QSYS2.DISPLAY_JOURNAL('MIBIB', 'QSQJRN'))
```

Leer los cambios de una base de datos como una secuencia ordenada de eventos **es exactamente lo que
hoy se llama *change data capture***, y es lo que hacen Debezium con PostgreSQL y los conectores de
Kafka. En IBM i está desde 1988, y la replicación de alta disponibilidad de la plataforma —MIMIX,
iTera— **funciona leyendo ese diario y reproduciéndolo en otra máquina**.

**Y los ficheros lógicos**, que son vistas materializadas mantenidas por el sistema:

```text
CRTLF FILE(CLIENTES_VIP)   -- una vista con su propio orden y selección
```

Un fichero lógico **se actualiza solo** cuando cambia el físico, y un programa lo lee como si fuera un
fichero normal. Es una vista con índice mantenido en tiempo real, y encaja con lo que esta clase
describe: **una transformación declarada una vez que el sistema aplica a cada dato que llega**.
"""),
        "pli": ("""
 flujo: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare (i, valor) fixed binary(31);
    declare salida char(200) varying initial('');

    get edit (linea) (a(200));
    linea = trim(linea);

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             valor = tok;
             if mod(valor, 2) = 0 then do;
                if salida ^= '' then salida = salida || '-';
                salida = salida || trim(char(valor * 2));
             end;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('stream=' || salida);

 end flujo;
""", """
**Lo que esta clase enseña en PL/I.** PL/I comparte con COBOL la arquitectura de flujo del
procesamiento por lotes, y tiene dos cosas propias que encajan en esta clase.

**La primera es `locate`** (clase 104), que es procesamiento de flujo sin copias:

```pli
 locate reg file(salida);      /* posiciona la estructura EN EL BÚFER del fichero */
 reg.campo = valor;             /* se escribe directamente ahí */
```

En lugar de construir el registro en una variable y copiarlo al búfer, **`locate` hace que la
estructura viva en el búfer**. Es entrada y salida sin copia intermedia, en 1964, y es exactamente lo
que hoy se persigue con `mmap` y con los búferes directos de Java NIO.

En una tubería que mueve millones de registros, **eliminar una copia por registro es la mitad del
trabajo**.

**La segunda es la multitarea con eventos** de la clase 119:

```pli
 declare listo(3) event;
 call etapa1(datos) task(t1) event(listo(1));
 call etapa2(datos) task(t2) event(listo(2));
 wait(listo);                          /* esperar a TODAS */
 wait(listo) (1);                        /* o a la PRIMERA que termine */
```

Con eso se puede montar una tubería con etapas concurrentes: cada `task` es una etapa, y los eventos
sincronizan. Es el modelo productor-consumidor con espera selectiva, y `wait(listo)(1)` —esperar a que
termine **una cualquiera**— es `Promise.race`.

Y merece la nota honesta que esta sección exige: **la multitarea de PL/I estuvo muy poco implementada**
y muy poco usada. Los compiladores completos la traían y los programas de producción rara vez la
tocaban, porque en un mainframe **el paralelismo lo daba el sistema ejecutando varios trabajos a la
vez**, no el lenguaje dentro de uno.

Es un patrón que se repite: **PL/I tenía la característica, y la plataforma resolvía el problema por
otra vía, así que la característica no arraigó**.
"""),
        "mumps": ("""
FLUJO ; Reactivo y flujos -- clase 120
 read linea
 set salida = ""
 ; una sola pasada: filtrar y transformar
 for i=1:1:$length(linea, " ") do
 . set x = $piece(linea, " ", i)
 . quit:x#2'=0
 . if salida '= "" set salida = salida _ "-"
 . set salida = salida _ (x * 2)
 write "stream=", salida, !
 quit
""", """
**Lo que esta clase enseña en M.** El `quit:x#2'=0` del programa es el postcondicional de la clase 108
haciendo de `continue`: **si el número no es par, se sale del bloque de esta iteración**.

Y M tiene una propiedad que lo convierte en un procesador de flujos natural, y ya ha aparecido varias
veces: **`$order` recorre estructuras que no caben en memoria**.

```mumps
 set id = ""
 for  set id = $order(^PACIENTE(id))  quit:id=""  do procesar(id)
```

Ese bucle **recorre diez millones de pacientes en disco, en orden, con memoria constante**. No hay
consulta, no hay cursor y no hay carga: es un recorrido de índice expresado como bucle del lenguaje
(clase 092).

Es exactamente lo que esta clase describe: **una pasada, memoria acotada, volumen ilimitado**.

Y M tiene además un mecanismo de flujo entre procesos que es de los más elegantes de esta página:
**los globals como cola**.

```mumps
 ; productor
 set ^COLA($increment(^COLA)) = mensaje

 ; consumidor
 for  set n = $order(^COLA(""))  quit:n=""  do
 . set msg = ^COLA(n)
 . kill ^COLA(n)
 . do procesar(msg)
```

**`$increment` es atómico**, así que varios productores pueden encolar a la vez sin bloqueos. Y como el
*global* es persistente y transaccional, **la cola sobrevive a una caída del sistema** y los mensajes
no se pierden.

Es una cola de mensajes durable construida con la estructura de datos del lenguaje, y es el patrón que
usan los sistemas M para comunicar procesos desde siempre.

Y la modernización, como en las clases 105 y 119, va por ahí: **IRIS Interoperability** es un motor de
integración con productores, procesos de negocio y operaciones conectados por mensajes persistentes,
con reintentos y trazabilidad. Es donde entran los mensajes HL7 y FHIR de un hospital, y por debajo
son *globals*.

**Un bus de eventos empresarial sobre un modelo de datos de 1966.**
"""),
        "smalltalk": ("""
| v salida |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

"select: y collect: encadenados: la tubería"
salida := (v select: [ :cada | cada even ]) collect: [ :cada | cada * 2 ].

Transcript
    show: 'stream=', ((salida collect: [ :cada | cada printString ])
        inject: '' into: [ :acc :cada |
            acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ]);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `select:` seguido de `collect:` es la tubería, y con la
salvedad de siempre: **construye una colección intermedia**. Para flujos, Smalltalk tiene su propia
jerarquía, y es de las más antiguas que existen.

```smalltalk
ReadStream on: coleccion
WriteStream on: String new
ReadWriteStream on: ...
```

Un `Stream` **es una posición sobre una secuencia**, con `next`, `peek`, `atEnd`, `upTo:` y
`skipSeparators`. Y como se dijo en la clase 106, **funciona igual sobre una colección en memoria que
sobre un fichero**.

Su uso más idiomático es construir texto sin concatenar (clase 093):

```smalltalk
String streamContents: [ :flujo |
    coleccion do: [ :cada | flujo print: cada ]
              separatedBy: [ flujo nextPut: $- ] ]
```

Y Pharo tiene la evaluación perezosa que esta clase pide, con un nombre que la describe:

```smalltalk
(1 to: 1000000) readStream
    select: [ :x | x even ];
    collect: [ :x | x * 2 ];
    next: 5                          "solo se calculan CINCO"
```

Con `Iterator` y las colecciones perezosas de Pharo, las etapas se fusionan y no hay colecciones
intermedias.

Y hay una construcción de Smalltalk que esta clase debe nombrar porque es reactividad en su forma
más pura: **el proceso como flujo**.

```smalltalk
| cola productor consumidor |
cola := SharedQueue new.
productor := [ 1 to: 100 do: [ :i | cola nextPut: i ] ] fork.
consumidor := [ [ true ] whileTrue: [ procesar: cola next ] ] fork.
```

**`fork` sobre un bloque crea un proceso ligero**, y `SharedQueue` los conecta con bloqueo. Es la
misma arquitectura que las colas sincronizadas de Ada de esta página, con la diferencia de que **en
Smalltalk los procesos son objetos que se pueden inspeccionar, suspender y depurar en marcha**.

Y eso lleva al hecho que resume el lenguaje: **el planificador de procesos de Smalltalk está escrito en
Smalltalk**. `Processor` es un objeto, las prioridades son constantes de clase, y se puede escribir un
planificador propio. Cuando todo es un objeto, la concurrencia también lo es.
"""),
    },
)
