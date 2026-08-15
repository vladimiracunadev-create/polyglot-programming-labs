# -*- coding: utf-8 -*-
"""Parte 8, lote H — clases 131 y 132. Ver `vivos_parte8.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 131 — Recolección de basura
# ---------------------------------------------------------------------------
SPECS["131"] = dict(
    gancho="""
Crear `n` objetos temporales y dejar que desaparezcan. Aquí hay una fecha que es la raíz de todo:
**John McCarthy inventó la recolección de basura para Lisp en 1959**, y el término es suyo. Y hay un
contraste que ordena la página: **cuatro de estos lenguajes tienen recolector, tres tienen conteo de
referencias y cinco no tienen nada** — y esos cinco llevan sesenta años en producción sin fugas
relevantes.
""",
    porque="""
Aquí el concepto es la **liberación automática**, y estos lenguajes lo enseñan porque tienen las tres
respuestas y las tres funcionan. **Recolector de trazado**: Lisp desde 1959 y Smalltalk desde 1980,
donde se inventó casi toda la tecnología que hoy usan Java, .NET y Go. **Conteo de referencias**: Perl,
Tcl y las interfaces de Delphi, con liberación determinista y el problema de los ciclos. **Y nada**:
COBOL, Fortran, Ada, RPG y PL/I, que lo resuelven **no reservando** o **liberando por región** (clases
128 y 130).

Y el dato incómodo es que **la tercera opción es la que gobierna los sistemas más críticos**, porque
una pausa impredecible es inaceptable donde el tiempo importa.
""",
    cierre="""
Lo transferible: **el recolector no elimina las fugas, cambia su forma**. Ya no se olvida un `free`: se
olvida quitar una entrada de una caché, o un oyente de una lista, y el objeto vive para siempre porque
**algo lo referencia**. Por eso los lenguajes con recolector tienen referencias débiles y por eso la
pregunta ante una fuga cambia de "¿dónde falta el `free`?" a **"¿quién sigue apuntando a esto?"**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. RECOLEC.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4) COMP.
01  I       PIC 9(4) COMP.
01  PTR     USAGE POINTER.
01  ED-N    PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    *> COBOL no tiene recolector: se reserva y se libera, o no se reserva
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        CONTINUE
    END-PERFORM

    MOVE N TO ED-N
    DISPLAY "creados=" FUNCTION TRIM(ED-N) " estado=recolectado"
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene recolector de basura**, y sus sistemas no tienen
fugas. La contradicción aparente se resuelve con lo que ya explicaron las clases 128 y 130: **la
memoria es estática y la liberación es por región**.

Y hay una razón por la que un recolector sería **inaceptable** en el entorno donde COBOL vive, y merece
decirla con precisión: **las pausas**.

Un sistema transaccional bancario tiene acuerdos de nivel de servicio del tipo "el 99,9 % de las
transacciones en menos de 200 ms". Un recolector que pare el mundo 300 ms **rompe ese acuerdo**, y no
se puede predecir cuándo lo hará.

Esa es la razón —no la antigüedad— por la que la gestión automática de memoria tardó tanto en llegar a
los sistemas de misión crítica, y por la que Java necesitó recolectores de baja latencia —ZGC,
Shenandoah— para entrar en ese mercado.

Y cuando COBOL sí convive con un recolector, es en la frontera con Java:

```cobol
CLASS-ID. MiClase INHERITS FROM Base.       *> COBOL orientado a objetos (clase 110)
```

En **COBOL for JVM**, los objetos COBOL **son objetos Java y los recoge el recolector de la JVM**. Y
ahí aparece un problema de interoperabilidad que esta clase debe nombrar: **los datos de la
`WORKING-STORAGE` no los ve el recolector**, así que un objeto Java referenciado solo desde memoria
COBOL nativa **puede ser recogido mientras se usa**.

Es el mismo problema que tienen JNI en Java y las referencias globales, y se resuelve declarando las
referencias explícitamente.

Merece cerrar con la observación de fondo: **COBOL no adoptó el recolector, y su ecosistema resolvió el
problema por otra vía** — la misma conclusión que esta parte del curso repite con las plataformas de
gestión.
"""),
        "fortran": ("""
program recolec
   implicit none
   integer :: n, i
   integer, allocatable :: temporal(:)

   read(*, *) n

   do i = 1, n
      block
         integer, allocatable :: efimero(:)
         allocate(efimero(100))
         efimero = i
      end block                       ! se libera AQUÍ, sin recolector
   end do

   write(*, '(A,I0,A)') 'creados=', n, ' estado=recolectado'
end program recolec
""", """
**Lo que esta clase enseña en Fortran.** **Fortran no tiene recolector**, y este programa muestra su
alternativa, que la clase 130 ya presentaba: **la liberación por ámbito con `block` y `allocatable`**.

```fortran
block
   integer, allocatable :: efimero(:)
   allocate(efimero(100))
end block                       ! liberado, salga por donde salga
```

Y el motivo por el que Fortran nunca añadió un recolector es el mismo que el de COBOL, aplicado a otro
dominio: **la predecibilidad**.

Un cálculo que corre ocho horas en 40.000 núcleos **no puede permitirse una pausa global**: en un
programa con coarrays (clase 121), si una imagen se detiene para recolectar, **las demás se quedan
esperando en el `sync all`**. El efecto se amplifica con el número de procesos, y es lo que se llama
*jitter* del sistema — uno de los problemas más estudiados de la computación de alto rendimiento.

Los centros de supercomputación llegan a **desactivar servicios del sistema operativo** en los nodos de
cálculo por esa razón. Un recolector sería impensable.

Y el modelo de Fortran encaja perfectamente con eso: **`allocatable` libera de forma determinista, en un
punto conocido del programa**, sin ningún hilo de fondo y sin pausas.

Es una decisión de diseño, no una carencia — y es exactamente el mismo argumento que hoy usa Rust
frente a Go.

Fortran sí tiene una construcción que se acerca a la finalización automática, y ya apareció en la clase
103: **`final`**.

```fortran
type :: recurso
contains
   final :: limpiar          ! se ejecuta al morir el objeto
end type
```

Con el aviso de aquella clase: **es la característica peor soportada del estándar de 2003**, y el
idioma que sí funciona es `allocatable`.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Finalization;

procedure Recolec is
   type Temporal is new Ada.Finalization.Controlled with null record;
   --  Finalize se llamaría aquí al salir de cada ámbito

   N : Integer;
begin
   Get (N);

   for I in 1 .. N loop
      declare
         T : Temporal;          --  nace y muere en cada vuelta
      begin
         null;
      end;                       --  Finalize automático (clase 103)
   end loop;

   Put ("creados=");
   Put (N, Width => 1);
   Put_Line (" estado=recolectado");
end Recolec;
""", """
**Lo que esta clase enseña en Ada.** **El estándar de Ada PERMITE la recolección de basura y ninguna
implementación seria la hace.**

Eso está escrito en el estándar: un compilador puede implementar un recolector, y `pragma
Controlled (T)` sirve para **desactivarlo** sobre un tipo concreto. La previsión estaba desde 1983.

Y no se usó, por la razón de esta página: **Ada vive donde una pausa impredecible es un fallo**.

Lo que Ada ofrece en su lugar son las tres estrategias de la clase 130, y las tres son deterministas:

**Los tipos controlados** (clase 103), que es lo que usa este programa: `Finalize` se ejecuta al salir
del ámbito, **siempre y en un punto conocido**.

**Los *storage pools*** (clase 128), con los que se implementa una arena que libera de golpe.

**Y no reservar**, con `pragma Restrictions (No_Allocators)`.

Y merece contar el detalle que hace de Ada un caso interesante en esta clase: **es el único lenguaje de
esta página cuyo estándar contempla explícitamente las dos opciones y deja la elección al
implementador**.

La razón está documentada en la justificación del lenguaje: el comité no quiso **excluir** a los
sistemas que sí podrían beneficiarse de un recolector —herramientas, compiladores, aplicaciones de
escritorio— pero tampoco imponerlo a los empotrados.

El mercado decidió: **prácticamente todo el código Ada del mundo está en sistemas donde el
determinismo manda**, y ningún compilador comercial invirtió en un recolector.

Es un buen ejemplo de que **una característica opcional en un estándar tiende a no existir**, porque
nadie puede depender de ella.

Y para las estructuras compartidas, Ada tiene desde 2005 los contenedores con `Indefinite_` y los tipos
controlados que implementan conteo de referencias a mano — que es lo que en C++ es `shared_ptr`.
"""),
        "pascal": ("""
program Recolec;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  ITemporal = interface
    ['{B2C3D4E5-0000-0000-0000-000000000002}']
  end;

  TTemporal = class(TInterfacedObject, ITemporal)
  end;

var
  N, I: Integer;

begin
  Read(N);

  for I := 1 to N do
  begin
    var T: ITemporal := TTemporal.Create;   { conteo de referencias }
    { al salir de la vuelta, T se libera SOLA }
  end;

  WriteLn('creados=', IntToStr(N), ' estado=recolectado');
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal tiene **conteo de referencias, y solo para tres cosas**:
cadenas largas, arreglos dinámicos e **interfaces**.

```pascal
S: string;              { contada por referencia, con copia al escribir }
A: array of Integer;     { contada por referencia, SIN copia al escribir (clase 102) }
I: IInterfaz;             { contada por referencia: se libera sola }
O: TObjeto;                { NO: hay que llamar a Free }
```

**Esa asimetría es lo que hay que tener claro en Delphi**, y es la razón de que tantas clases se
diseñen con interfaces: **para no escribir `try/finally`** (clase 103).

Y esta clase permite contar un episodio instructivo del ecosistema: **ARC en Delphi para móviles**.

Entre 2013 y 2019, Delphi aplicó **conteo automático de referencias a TODOS los objetos** en iOS y
Android, no solo a las interfaces. La idea era razonable —iOS no permite recolectores y Objective-C
había hecho lo mismo— y el resultado fue malo:

- **El código dejó de ser portable**: el mismo fuente se comportaba distinto en escritorio y en móvil.
- **Los ciclos seguían sin liberarse**, y ahora aparecían en sitios donde nadie los esperaba.
- **`Free` pasó a significar algo distinto** según la plataforma.

**Embarcadero lo retiró en Delphi 10.4 (2020)** y volvió al modelo manual en todas las plataformas.

Es uno de los pocos casos documentados de un lenguaje maduro que **añade gestión automática de memoria
y la deshace**, y la lección es la del cierre de esta clase: **cambiar el modelo de memoria de un
lenguaje con treinta años de código es casi imposible**, porque el código existente depende del
comportamiento anterior.

Y sobre los ciclos, Delphi tiene lo esperable:

```pascal
[weak] FPadre: IPadre;         { referencia débil }
[unsafe] FOtro: IOtro;          { sin contar, sin comprobar }
```

**`[weak]`** es el `weaken` de Perl y el `weak_ptr` de C++, y es obligatorio en cualquier estructura con
enlaces al padre.
"""),
        "lisp": ("""
(let ((n (read)))
  (dotimes (i n)
    (let ((temporal (make-array 100)))     ; objeto efímero
      (setf (aref temporal 0) i)))
  ;; nadie libera: el recolector se ocupa
  (format t "creados=~D estado=recolectado~%" n))
""", """
**Lo que esta clase enseña en Common Lisp.** Aquí está el origen: **John McCarthy inventó la recolección
de basura para Lisp en 1959**, y el término *garbage collection* es suyo.

La razón fue de necesidad: **Lisp construye y descarta *conses* constantemente**, y pedir al
programador que liberara cada uno habría hecho el lenguaje inutilizable.

Y esta clase es el sitio para contar de dónde viene la tecnología que hoy usan Java, .NET, Go y
JavaScript, porque **casi toda se desarrolló en Lisp y en Smalltalk**:

| Técnica | Origen |
|---|---|
| Marcado y barrido | McCarthy, Lisp, 1959 |
| Recolección por copia | Cheney, 1970 |
| **Hipótesis generacional** | medida en Lisp y Smalltalk, años 80 |
| Barreras de escritura | Lisp Machines |
| Recolección incremental | Baker, Lisp, 1978 |
| Conservadora (Boehm) | para C, inspirada en Lisp |

**La hipótesis generacional** —*la mayoría de los objetos mueren jóvenes*— es la observación empírica
que sostiene todos los recolectores modernos, y **se midió estudiando programas Lisp y Smalltalk**.

Y en SBCL, el recolector es observable y ajustable:

```lisp
(room t)                                  ; uso de memoria por generación
(sb-ext:gc :full t)                        ; recolección completa
(sb-ext:gc :gen 0)                          ; solo la generación joven
(sb-ext:bytes-consed-between-gcs)            ; cada cuánto recolectar
(sb-ext:generation-number-of-gcs-before-promotion 0)
```

**`(time ...)` informa de los bytes reservados además del tiempo** (clase 128), lo que hace visible el
coste de reservar en cada expresión.

Y Common Lisp tiene lo que el cierre de esta clase pide, y desde hace décadas:

```lisp
(sb-ext:make-weak-pointer objeto)         ; referencia DÉBIL
(sb-ext:weak-pointer-value wp)             ; nil si ya fue recogido
(sb-ext:finalize objeto (lambda () ...))    ; finalizador
(make-hash-table :weakness :key)             ; caché que no retiene
```

Con el aviso de la clase 103: **los finalizadores se ejecutan cuando el recolector quiere, o nunca**.
Para cerrar ficheros está `unwind-protect`, no la finalización.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

for {set i 0} {$i < $n} {incr i} {
    set temporal [lrepeat 100 $i]      ;# objeto efímero
    unset temporal                       ;# la referencia desaparece: se libera
}

puts "creados=$n estado=recolectado"
""", """
**Lo que esta clase enseña en Tcl.** Tcl usa **conteo de referencias sobre valores inmutables**, y esa
combinación tiene una propiedad que ningún otro lenguaje de esta página comparte: **no puede haber
ciclos**.

Un valor de Tcl es inmutable desde el punto de vista del programa, y **una lista no puede contenerse a
sí misma**, así que el grafo de referencias **es siempre acíclico**.

**Por eso Tcl no necesita recolector de basura y no lo tiene.** Es el único lenguaje de esta página del
que se puede decir que el conteo de referencias es una solución **completa** y no parcial.

Comparado con Perl, que tiene el mismo mecanismo y sí necesita `weaken` (clase 130), la diferencia está
en la mutabilidad: **las estructuras mutables de Perl pueden apuntarse entre sí; los valores inmutables
de Tcl, no**.

Y esa propiedad tiene un coste conocido, el de la clase 102: **modificar una estructura compartida
implica copiarla**.

```tcl
set b $a          ;# O(1)
lset b 0 99        ;# copia la lista entera
```

Es el compromiso: **sin ciclos y con liberación determinista, a cambio de copiar al escribir**.

Donde Tcl sí puede tener fugas es **en los objetos y en los recursos con nombre**, que no llevan
contador:

```tcl
Persona new                    ;# crea un comando que vive HASTA que se destruya
set c [open fichero]            ;# un canal abierto
after 1000 { ... }               ;# un temporizador pendiente
```

**Un objeto TclOO no desaparece cuando nadie lo referencia**: es un comando global, y hay que llamar a
`$obj destroy` (clase 103). Es la misma situación que Java antes de `try-with-resources`.

Y para los intérpretes secundarios, Tcl tiene la liberación por región de la clase 130:

```tcl
interp delete $i        ;# todo lo que vivía dentro desaparece
```

Es la respuesta más limpia del lenguaje a esta clase: **si un subsistema puede fugar, dale su propio
intérprete y bórralo entero**.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

for my $i (1 .. $n) {
    my $temporal = [ (0) x 100 ];      # se libera al salir de la vuelta
}

print "creados=$n estado=recolectado\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl usa **conteo de referencias puro**, sin recolector de trazado
de respaldo, y esa decisión define sus virtudes y su único defecto grave.

**La virtud**: liberación **determinista e inmediata** (clases 103 y 128). En cuanto la última
referencia desaparece, el objeto se destruye y `DESTROY` se ejecuta. Por eso los objetos de Perl pueden
cerrar ficheros con fiabilidad.

**El defecto**: **los ciclos no se liberan nunca**.

```perl
my $a = {};  my $b = {};
$a->{otro} = $b;
$b->{otro} = $a;          # ciclo: los dos viven para siempre
```

Y aquí está la comparación que esta clase permite hacer, porque tres lenguajes de esta página usan
conteo de referencias con resultados distintos:

| | Perl | Tcl | Delphi (interfaces) |
|---|---|---|---|
| Estructuras mutables compartidas | **sí** | no | sí |
| ¿Puede haber ciclos? | **sí** | **no** | sí |
| Solución | `weaken` | no hace falta | `[weak]` |

**Tcl se libra porque sus valores son inmutables** (clase 131, apartado Tcl); Perl y Delphi no.

Y Perl tiene un detalle que conviene conocer sobre el final del programa: **al terminar, Perl hace una
recolección global** que destruye todo, incluidos los ciclos, en orden no especificado.

```perl
END { ... }                    # bloque de fin de programa
$obj->DESTROY                   # puede ejecutarse en un orden extraño en la salida
```

De ahí un aviso clásico: **no confiar en `DESTROY` durante la destrucción global**. Perl expone incluso
una variable para detectarlo:

```perl
sub DESTROY {
    return if ${^GLOBAL_PHASE} eq 'DESTRUCT';   # estamos en la salida
    ...
}
```

Ese idioma aparece en módulos serios de CPAN, y es un buen ejemplo de la clase de detalle que solo se
descubre cuando el modelo de memoria se filtra al código de usuario.
"""),
        "cpp": ("""
#include <iostream>
#include <memory>
#include <vector>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    for (int i = 0; i < n; ++i) {
        auto temporal = std::make_unique<std::vector<int>>(100, i);
        // se destruye al final de la vuelta: RAII, sin recolector
    }

    std::cout << "creados=" << n << " estado=recolectado\\n";
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** **C++ no tiene recolector de basura**, y esa fue una decisión
consciente y muy defendida por Bjarne Stroustrup: **RAII y los destructores deterministas hacen
innecesario el recolector para la memoria, y además sirven para los demás recursos**.

Ese último punto es el argumento fuerte, y ya apareció en la clase 103: **un recolector gestiona
memoria y no gestiona ficheros, conexiones ni bloqueos**. Por eso Java necesitó
`try-with-resources` y Python los gestores de contexto — **el recolector resuelve la mitad del
problema**.

Y sin embargo el estándar de C++ **sí contempló la recolección de basura**: C++11 añadió una interfaz
para un recolector conservador, con `std::declare_reachable` y `std::undeclare_reachable`. **Nadie la
implementó, y C++23 la eliminó del estándar.**

Es exactamente lo mismo que pasó con Ada en esta misma clase: **una característica opcional que nadie
podía usar acabó desapareciendo**.

Lo que C++ sí tiene es el conteo de referencias como herramienta explícita:

```cpp
std::unique_ptr<T>     // propiedad ÚNICA: cero coste
std::shared_ptr<T>      // conteo de referencias: coste ATÓMICO en cada copia
std::weak_ptr<T>         // observador que no cuenta: rompe los ciclos
```

Y la guía moderna es tajante: **`unique_ptr` por defecto; `shared_ptr` solo cuando la propiedad es de
verdad compartida**. Un `shared_ptr` cuesta:

- **Un bloque de control** aparte, con dos contadores atómicos.
- **Incrementos y decrementos atómicos** en cada copia y destrucción, que son caros en sistemas
  multinúcleo.
- **Y el problema de los ciclos**, el mismo de Perl y Delphi de esta página.

Y existe la opción de un recolector para C++, poco conocida: **el recolector conservador de Boehm**.

```cpp
#include <gc/gc.h>
int* p = (int*) GC_MALLOC(sizeof(int) * 100);   // y no se libera nunca
```

**Es conservador**: como no sabe qué es un puntero, **trata cualquier valor que parezca una dirección
como si lo fuera**. Eso lo hace usable desde C y C++ sin cambiar el lenguaje, y a cambio **puede
retener memoria por falsos positivos**.

Se usa en producción —en el propio Mono, y en compiladores— y es la prueba de que el recolector es
posible en C++ y de que la comunidad prefirió RAII.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi RECOLEC;
  n int(10) const;
end-pi;

dcl-s i int(10);
dcl-s p pointer;

// RPG no tiene recolector: se reserva y se libera
for i = 1 to n;
  p = %alloc(400);
  dealloc p;
endfor;

dsply ('creados=' + %char(n) + ' estado=recolectado');

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG no tiene recolector, y la plataforma resuelve el problema con
lo de las clases 128 y 130: **liberación por grupo de activación**.

Y esta clase permite explicar por qué eso es, en la práctica, mejor que un recolector para su dominio:

```text
Un trabajo IBM i:  arranca → procesa N transacciones → termina → RCLACTGRP libera todo
```

**La memoria de un trabajo se recupera entera al terminar**, y los trabajos de un servidor
transaccional son cortos. Es el mismo argumento que la clase 130 hacía con CICS: **si la unidad de
trabajo tiene un final, la fuga tiene fecha de caducidad**.

Y donde IBM i sí convive con recolectores es en la parte Java de la plataforma, que es considerable:
**la JVM de IBM i ejecuta aplicaciones WebSphere junto a programas RPG**, en la misma máquina y a menudo
en el mismo trabajo.

De ahí una capacidad de observabilidad que merece nombrarse, porque es la clase 142 anticipada:

```sql
SELECT * FROM QSYS2.ACTIVE_JOB_INFO(...) WHERE JOB_TYPE = 'BATCH';
SELECT * FROM QSYS2.SYSTEM_STATUS_INFO;
```

**El uso de memoria de cada trabajo, incluidos los que ejecutan Java, se consulta con SQL** — y con eso
se detecta un trabajo que crece.

Y RPG tiene una particularidad de gestión de memoria que esta clase debe recordar y que viene de la
clase 087: **el almacenamiento estático de un programa de servicio con activación compartida se
comparte entre trabajos**.

Eso significa que **una estructura que crece en un módulo de servicio no se libera al terminar un
trabajo**: vive mientras viva el grupo de activación, que puede ser el del sistema.

Es la fuga más real que puede tener un sistema RPG moderno, y la razón de la norma de la plataforma:
**los módulos de servicio, sin estado**.
"""),
        "pli": ("""
 recolec: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare p pointer;
    declare temporal(100) fixed binary(31) based(p);

    get list (n);

    /* PL/I no tiene recolector: allocate y free */
    do i = 1 to n;
       allocate temporal set(p);
       free temporal;
    end;

    put skip list ('creados=' || trim(char(n)) || ' estado=recolectado');

 end recolec;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **no tiene recolector**, y su respuesta a esta clase es la
mejor de los lenguajes sin él, y ya se contó en las clases 128 y 130: **las áreas**.

```pli
 declare mi_area area(100000);
 allocate nodo in(mi_area) set(p);
 ...
 free mi_area;               /* TODO lo de dentro, de golpe */
```

**Liberar el área libera todo lo reservado dentro**, sin recorrer nada. Es un *arena allocator* con
sintaxis del lenguaje, en 1964, y para el patrón "muchos objetos con la misma vida" es **más rápido que
cualquier recolector**: la liberación es O(1).

Ese patrón es hoy la técnica recomendada en Rust, en Zig y en C++ con `pmr` (clase 128) para
compiladores, servidores de peticiones y videojuegos — **exactamente los casos donde un recolector
molesta**.

Y PL/I añade la otra estrategia de la clase 130: **`controlled` como pila de generaciones**, donde la
liberación se empareja por construcción.

Lo que PL/I **no** tiene, y es la carencia real de esta clase, es **detección de fugas**. Sin recolector
y sin herramientas del lenguaje, una fuga en un programa PL/I de larga duración es un problema de
análisis manual.

En z/OS eso se mitiga con lo mismo que en COBOL: **los programas de transacción son efímeros**, y el
gestor de recursos libera al terminar la unidad de trabajo.

Y merece cerrar la página con una observación sobre PL/I que esta parte del curso ha ido acumulando:
**tuvo casi todas las ideas antes que nadie, y no tuvo la que más falta hacía en su época**.

En 1964, con memoria medida en kilobytes, un recolector era impensable. Cuando dejó de serlo —en los
noventa—, PL/I ya había dejado de evolucionar (clase 110). Es la misma historia que la orientación a
objetos, y por la misma causa: **el calendario**.
"""),
        "mumps": ("""
RECOLEC ; Recoleccion de basura -- clase 131
 read n
 for i=1:1:n do
 . new temporal
 . set temporal(1) = i
 . ; `new` restaura el valor anterior al salir del bloque
 write "creados=", n, " estado=recolectado", !
 quit
""", """
**Lo que esta clase enseña en M.** **M no tiene recolector de basura** y **tampoco tiene reserva
explícita** (clase 128): el intérprete gestiona el árbol y el programador solo asigna y borra.

Y M tiene dos mecanismos de liberación automática que ya han aparecido y que aquí se ven juntos:

**`new`**, que apila y restaura al salir del ámbito (clases 096 y 127):

```mumps
 new temporal          ; al hacer quit, vuelve el valor anterior
```

**Y `kill`**, que borra un subárbol entero.

Lo que M no tiene es la propiedad que esta clase discute: **liberación de lo que ya nadie usa**. Como
no hay referencias (clase 129), **no hay nada que rastrear**: un dato existe mientras su nombre exista,
y desaparece cuando se hace `kill` o cuando el `new` lo restaura.

Es el modelo más simple posible, y con una consecuencia interesante: **el concepto de "basura" no
existe en M**. No hay objetos inalcanzables, porque todo es alcanzable por su nombre.

Donde sí hay algo parecido a un problema de recolección es en la capa de datos:

```mumps
 kill ^DATOS(id)        ; borra el nodo, pero el BLOQUE de disco queda libre DENTRO del fichero
```

**Los ficheros de base de datos de M no encogen al borrar**: los bloques quedan disponibles para
reutilizar, y recuperar el espacio exige una reorganización — el equivalente de la compactación de un
recolector, a escala de disco y ejecutada manualmente.

Y esa operación tiene los mismos compromisos que un recolector: **cuesta tiempo, hay que programarla en
una ventana de mantenimiento y las implementaciones modernas la hacen en línea**, sin parar el sistema.

Es una simetría curiosa que esta clase permite señalar: **los problemas de la gestión automática de
memoria reaparecen, con otros nombres y otra escala, en la gestión del almacenamiento de una base de
datos** — fragmentación, compactación, pausas y ventanas de mantenimiento.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

1 to: n do: [ :i |
    | temporal |
    temporal := Array new: 100.
    temporal at: 1 put: i ].

Smalltalk garbageCollect.

Transcript
    show: 'creados=', n printString, ' estado=recolectado';
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk **tiene recolector desde 1980**, y junto con Lisp
es donde se desarrolló casi toda la tecnología moderna (clase 128).

Y esta clase permite contar el papel concreto de Smalltalk, que es enorme y poco citado: **la
recolección generacional se propuso y midió aquí**.

David Ungar publicó en 1984 *Generation Scavenging: A Non-disruptive High Performance Storage
Reclamation Algorithm*, trabajando en Smalltalk en Berkeley. La observación central era la **hipótesis
generacional**, y la implementación —espacios de supervivientes, promoción por edad, barreras de
escritura— **es reconociblemente la de la JVM y la de .NET**.

Y la motivación era la de esta página: **Smalltalk es interactivo**, y una pausa de un segundo al mover
el ratón es inaceptable. El título del artículo lo dice: *no disruptivo*.

En Pharo, el recolector es observable y ajustable:

```smalltalk
Smalltalk garbageCollect.                    "completa"
Smalltalk garbageCollectMost.                 "solo la joven: rápida"
Smalltalk vmParameterAt: 7.                    "tamaño del espacio de supervivientes"
Smalltalk vmParameterAt: 7 put: 4000000.        "y se puede CAMBIAR en marcha"
```

**Ajustar el recolector desde el propio lenguaje, con el sistema funcionando.**

Y las herramientas de diagnóstico de fugas son las mejores de esta página, y responden exactamente a
la pregunta del cierre de esta clase:

```smalltalk
MiClase allInstances size.        "¿cuántas hay?"
objeto chasePointers.              "¿QUIÉN me retiene?"
objeto inspect.
```

**`chasePointers` recorre el montón y muestra quién referencia a un objeto.** Es la respuesta a "¿por
qué esto no se recoge?", y en Java exige un volcado del montón y una herramienta aparte.

Y las referencias débiles cierran el cuadro:

```smalltalk
WeakArray with: objeto.
WeakKeyDictionary new.          "caché que no retiene (clase 095)"
objeto toFinalizeSend: #cerrar to: self.
```

Con el aviso de siempre: **la finalización no es determinista**, y para cerrar recursos está `ensure:`
(clase 103).
"""),
    },
)

# ---------------------------------------------------------------------------
# 132 — RAII, propiedad y préstamos
# ---------------------------------------------------------------------------
SPECS["132"] = dict(
    gancho="""
Un recurso que se adquiere, se usa y se libera solo. Es RAII, y esta clase cierra el arco de la Parte
8 con la conclusión que las clases 128 a 131 han ido preparando: **la gestión automática de memoria no
la inventó el recolector, la inventó el ÁMBITO**. Y aquí hay dos lenguajes que llegaron antes que C++:
**Ada con los tipos controlados en 1983** y **Pascal con `try/finally`**, que resuelve el mismo
problema desde el otro lado.
""",
    porque="""
Aquí el concepto es la **propiedad: quién es responsable de liberar y cuándo**, y estos lenguajes lo
enseñan porque tienen todas las piezas de las que Rust hizo un sistema de tipos. **`Finalize` de Ada
es el destructor**; **`allocatable` de Fortran es propiedad única sin alias**; **`limited` de Ada es
un tipo que no se puede copiar**; **`unique_ptr` de C++ es propiedad única con movimiento** (clase
081).

Rust no inventó esas ideas: **las juntó y las hizo comprobables en compilación**. Ver las piezas
sueltas en los lenguajes donde nacieron explica de dónde viene el préstamo mejor que cualquier
introducción.
""",
    cierre="""
Lo transferible: **RAII es una respuesta a una pregunta más general que la memoria — ¿quién limpia?**.
Ficheros, bloqueos, conexiones, transacciones y bloques de memoria comparten el problema, y todos se
resuelven igual: **atar la liberación a la muerte de algo que muere seguro**. Cuando escribas código
con recursos, la pregunta útil no es "¿dónde libero?" sino **"¿de quién es esto y qué lo va a
enterrar?"** — y si la respuesta es "de nadie en concreto", ahí está el fallo futuro.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PROPIED.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM ADQUIRIR
    PERFORM USAR
    PERFORM LIBERAR

    MOVE R TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.

ADQUIRIR.
    CONTINUE.

USAR.
    COMPUTE R = N * 2.

LIBERAR.
    CONTINUE.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene RAII, ni destructores, ni propiedad**, y sus
sistemas gestionan recursos con una fiabilidad que muchos lenguajes modernos envidiarían.

La razón es la que esta parte del curso ha repetido: **la propiedad está en la transacción, no en el
objeto**.

```cobol
EXEC CICS READ FILE('CLIENTES') RIDFLD(ID) UPDATE END-EXEC
*> el registro queda BLOQUEADO
EXEC CICS SYNCPOINT END-EXEC
*> se confirma y se sueltan TODOS los bloqueos y recursos
```

**El monitor es el dueño de todo**: bloqueos de registro, memoria de `GETMAIN`, colas, conexiones. Y
cuando la transacción termina —bien o mal— **libera todo lo suyo**.

Eso es RAII con la unidad puesta en la transacción en lugar del ámbito léxico, y tiene una propiedad
que RAII no tiene: **funciona aunque el programa se caiga**. Un destructor de C++ no se ejecuta si el
proceso muere; un `SYNCPOINT` deshecho por el monitor, sí.

Dentro del programa, COBOL tiene lo que la clase 103 describía:

```cobol
DECLARATIVES.
ERROR-FICHERO SECTION.
    USE AFTER STANDARD ERROR PROCEDURE ON CLIENTES.
```

**Un manejador declarativo que el sistema invoca al fallar una operación** — y que se usa para cerrar y
registrar.

Y hay una construcción de COBOL-2002 que se parece más a lo de esta clase de lo que suele reconocerse:
**los programas anidados con `LOCAL-STORAGE`** (clase 127).

```cobol
PROGRAM-ID. SUB RECURSIVE.
LOCAL-STORAGE SECTION.
01  BUFFER  PIC X(1000).      *> se reserva al entrar, se libera al salir
```

**`LOCAL-STORAGE` es un recurso atado al ámbito de la invocación**, y eso es exactamente la idea de
RAII aplicada a la memoria.

Lo que falta es el gancho: **no hay forma de ejecutar código al salir**. Es la mitad del mecanismo, y
la otra mitad la pone el monitor.
"""),
        "fortran": ("""
program propied
   implicit none
   integer :: n, r

   read(*, *) n

   block
      integer, allocatable :: recurso(:)
      allocate(recurso(100))          ! adquirir
      recurso = n
      r = recurso(1) * 2               ! usar
   end block                            ! LIBERAR: automático, salga por donde salga

   write(*, '(A,I0)') 'resultado=', r
end program propied
""", """
**Lo que esta clase enseña en Fortran.** **`allocatable` es propiedad única con liberación por ámbito**,
y esa frase describe exactamente lo que Rust llama *ownership*.

Y las tres propiedades que lo hacen equivalente son las de la clase 128:

1. **No puede tener alias.** Solo un nombre posee el arreglo.
2. **Se libera al salir del ámbito**, siempre.
3. **`move_alloc` transfiere la propiedad** sin copiar (clase 081) — que es el `std::move` de C++ y el
   movimiento de Rust.

```fortran
call move_alloc(origen, destino)      ! origen queda SIN ASIGNAR
```

**Después de `move_alloc`, `origen` está desasignado** — igual que una variable movida en Rust queda
inutilizable. Es la misma semántica, expresada con una subrutina en lugar de con el sistema de tipos.

Y Fortran 2003 completó el modelo con **componentes `allocatable` en tipos derivados**:

```fortran
type :: matriz
   real, allocatable :: datos(:,:)      ! el tipo POSEE sus datos
end type
```

**Al morir una `matriz`, sus datos se liberan automáticamente**, en cascada — que es exactamente lo que
hace `unique_ptr` dentro de una clase en C++ (clase 128).

Lo que a Fortran le falta para ser RAII completo es el gancho de la clase 103: **`final`**, que existe
desde 2003 y es la característica peor soportada del estándar.

```fortran
type :: fichero
   integer :: unidad
contains
   final :: cerrar          ! DEBERÍA ejecutarse al morir el objeto
end type
```

**Con `final` funcionando bien, Fortran tendría RAII para cualquier recurso.** Sin él, la memoria se
libera sola y los ficheros hay que cerrarlos a mano.

Es un caso claro de lo que esta clase quiere mostrar: **las piezas de RAII estaban repartidas por
varios lenguajes, y hacía falta juntarlas**.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Finalization;

procedure Propied is
   package Recursos is
      type Recurso is new Ada.Finalization.Limited_Controlled with record
         Valor : Integer := 0;
      end record;

      overriding procedure Initialize (R : in out Recurso);
      overriding procedure Finalize   (R : in out Recurso);
   end Recursos;

   package body Recursos is
      overriding procedure Initialize (R : in out Recurso) is
      begin
         null;                    --  adquirir
      end Initialize;

      overriding procedure Finalize (R : in out Recurso) is
      begin
         null;                    --  LIBERAR: automático al salir del ámbito
      end Finalize;
   end Recursos;

   use Recursos;

   N, R : Integer;
begin
   Get (N);

   declare
      Rec : Recurso;              --  Initialize aquí
   begin
      Rec.Valor := N;
      R := Rec.Valor * 2;
   end;                            --  Finalize aquí, pase lo que pase

   Put ("resultado=");
   Put (R, Width => 1);
   New_Line;
end Propied;
""", """
**Lo que esta clase enseña en Ada.** **Ada tenía RAII completo en 1983**, once años antes de que
Stroustrup le pusiera nombre, y este programa lo demuestra con las tres piezas juntas.

**Primera: `Limited_Controlled`.** El tipo es a la vez:

- **`Controlled`**: tiene `Initialize` y `Finalize`, que el runtime ejecuta al crear y al destruir.
- **`Limited`**: **no se puede copiar ni asignar** (clase 101).

Esa segunda mitad es lo que Rust expresa no implementando `Copy` y C++ borrando el constructor de
copia. **En Ada es una palabra en la declaración del tipo.**

**Segunda: `Finalize` se ejecuta siempre.** Al salir del bloque, por `return`, por `goto` y **por una
excepción que se propague**. Es la garantía que hace utilizable el mecanismo.

**Y tercera: la comprobación de accesibilidad** (clase 083), que impide guardar una referencia a algo
que vive menos. **Eso es el préstamo con comprobación en compilación**, y Ada lo tiene desde el
principio para los tipos de acceso.

Y Ada 2012 añadió lo que faltaba para acercarse todavía más a Rust: **los aspectos de propiedad**.

```ada
type Puntero is not null access Recurso
   with Ownership;                        --  SPARK: propiedad comprobada
```

**En SPARK, `Ownership` hace que el análisis siga quién posee cada recurso** y rechace usar algo tras
moverlo o liberarlo — **con comprobación estática, como Rust**.

Es la conclusión de esta clase: **las piezas del sistema de propiedad de Rust existían repartidas —
destructores en Ada y C++, propiedad única en Fortran, tipos no copiables en Ada— y lo que hizo Rust
fue hacerlas comprobables por el compilador en un solo modelo coherente**.

Y merece decir lo que Ada hace mejor incluso hoy: **`Finalize` se ejecuta también al abortar una
tarea** (clase 121), y la combinación de tipos controlados con objetos protegidos garantiza la
liberación en escenarios concurrentes que en otros lenguajes exigen cuidado manual.
"""),
        "pascal": ("""
program Propied;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TRecurso = class
    Valor: Integer;
    constructor Create(V: Integer);
    destructor Destroy; override;
  end;

constructor TRecurso.Create(V: Integer);
begin
  inherited Create;
  Valor := V;                    { adquirir }
end;

destructor TRecurso.Destroy;
begin
  inherited Destroy;              { liberar }
end;

var
  N, R: Integer;
  Rec: TRecurso;

begin
  Read(N);

  Rec := TRecurso.Create(N);
  try
    R := Rec.Valor * 2;
  finally
    Rec.Free;                     { SIEMPRE se ejecuta }
  end;

  WriteLn('resultado=', IntToStr(R));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal resuelve esta clase **desde el otro lado**: no con
destructores automáticos, sino con **`try...finally`**, que garantiza la ejecución de la limpieza.

Y esa diferencia merece explicarse, porque es la elección que hicieron Java, C# y Python:

| | RAII (C++, Ada, Rust) | `try/finally` (Pascal, Java) |
|---|---|---|
| Quién libera | **el destructor del objeto** | **el bloque de código** |
| Se escribe | una vez, en el tipo | **en cada uso** |
| Se puede olvidar | no | **sí** |
| Funciona con excepciones | sí | sí |

**La ventaja de RAII es que se escribe una vez y no se puede olvidar**; la de `try/finally` es que no
exige destructores automáticos ni semántica de valor.

Y el mundo Pascal ha ido convergiendo hacia RAII por tres vías:

**Las interfaces con conteo de referencias** (clases 103 y 131), que liberan solas y que se usan a
menudo **solo por eso**.

**Los registros gestionados** de Free Pascal 3.2 (clase 130), que sí son RAII completo:

```pascal
type
  TRecurso = record
    class operator Initialize(var R: TRecurso);   { constructor automático }
    class operator Finalize(var R: TRecurso);      { DESTRUCTOR automático }
  end;

procedure P;
var R: TRecurso;        { Initialize aquí }
begin
  ...
end;                     { Finalize aquí, pase lo que pase }
```

**Eso es exactamente RAII**, llegado a Pascal en 2020.

**Y los helpers y las clausuras**, con los que se construye el patrón de "recurso con bloque":

```pascal
ConRecurso(procedure(const R: TRecurso)
           begin ... end);          { la función adquiere, llama y libera }
```

Es el `with-open-file` de Lisp (clase 103) escrito con métodos anónimos, y es lo que hacen hoy muchas
bibliotecas de Delphi.

Merece cerrar señalando que **el `try/finally` de Delphi es de 1995 y precede a `try-with-resources`
de Java (2011) en dieciséis años** — y que la crítica que se le hace hoy —que hay que acordarse de
escribirlo— es exactamente la que motivó RAII.
"""),
        "lisp": ("""
(let* ((n (read))
       (r 0))
  ;; unwind-protect: la limpieza se ejecuta pase lo que pase (clase 103)
  (unwind-protect
       (setf r (* n 2))
    nil)                              ; aquí iría la liberación
  (format t "resultado=~D~%" r))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp resuelve esta clase con **`unwind-protect`** y con las
macros `with-` que se construyen sobre él (clase 103), y esa solución tiene una propiedad que la
distingue de RAII: **la limpieza está en el sitio de uso, no en el tipo**.

```lisp
(with-open-file (f "datos.txt")       ; adquirir
  (leer f))                            ; usar; y al salir, cerrar
```

Y como se dijo en la clase 103, **eso no es una característica del lenguaje: es una macro**, y
cualquiera puede escribir la suya:

```lisp
(defmacro with-recurso ((var arg) &body cuerpo)
  `(let ((,var (adquirir ,arg)))
     (unwind-protect (progn ,@cuerpo)
       (liberar ,var))))
```

**Diez líneas y el patrón queda disponible para todo el proyecto**, con la limpieza garantizada y
escrita una sola vez — que es la ventaja de RAII conseguida con macros.

Es la diferencia entre los dos enfoques: **RAII lo ata al tipo; las macros lo atan a la forma de
uso**. Y para recursos que no son objetos —una transacción, un bloqueo global, un cambio temporal de
configuración— **la macro encaja mejor**.

Y Lisp tiene un tercer mecanismo que ningún otro lenguaje de esta página tiene y que resuelve casos que
RAII no cubre: **el enlace dinámico** (clase 082).

```lisp
(let ((*print-base* 16))
  (print 255))              ; FF -- y al salir, *print-base* vuelve a 10
```

**Cambiar una variable especial dentro de un `let` la restaura al salir**, automáticamente y
respetando las excepciones. Es RAII aplicado a la configuración, sin objetos y sin macros.

Es el mismo mecanismo que `local` en Perl (clase 096), `new` en M y `controlled` en PL/I — cuatro
lenguajes que llegaron a lo mismo.

Y la conclusión de esta clase en Lisp es la de la clase 107: **el problema de la propiedad se resuelve
con las herramientas que el lenguaje ya tiene**, y en Lisp esas herramientas son la macro y el ámbito.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

try {
    set recurso [expr {$n * 2}]       ;# adquirir y usar
    puts "resultado=$recurso"
} finally {
    # liberar: se ejecuta pase lo que pase
}
""", """
**Lo que esta clase enseña en Tcl.** Tcl resuelve esta clase con `try...finally` (Tcl 8.6) y con los
mecanismos de la clase 103, y su modelo de memoria hace que la propiedad casi no sea un problema:
**los valores son inmutables y se liberan solos** (clase 131).

Lo que sí tiene dueño en Tcl son **los recursos con nombre**: canales, objetos, ventanas, temporizadores
e intérpretes. Y para ellos hay tres patrones:

```tcl
try { ... } finally { close $canal }              ;# explícito
trace add variable v unset { close $canal }        ;# atado a una VARIABLE
oo::class create R { destructor { close $canal } }  ;# atado a un objeto
```

**El segundo es el más parecido a RAII y el menos conocido**: `trace ... unset` engancha código a la
desaparición de una variable, **incluida la salida del procedimiento**.

```tcl
proc procesar {} {
    set canal [open datos.txt]
    trace add variable canal unset [list apply {{c args} { close $c }} $canal]
    ...
}                                     ;# al salir, `canal` desaparece y se cierra
```

Eso es **un destructor construido con las piezas del lenguaje**, y funciona aunque haya `return` o
error.

Y Tcl tiene la liberación por región de la clase 130, que es la respuesta más contundente:

```tcl
set i [interp create]
$i eval $codigo_no_confiable
interp delete $i                ;# TODO lo suyo desaparece
```

**Un intérprete secundario es una arena**: sus variables, sus procedimientos, sus canales y sus objetos
mueren con él.

Y eso conecta con la clase 153, porque es también el mecanismo de aislamiento de Tcl: **un intérprete
seguro (*safe interp*) tiene comandos restringidos y se destruye entero**, con lo que ejecutar código
ajeno no puede dejar residuos.

Es una idea que hoy reaparece en los aislamientos de WebAssembly y en los espacios de nombres de los
contenedores: **dar un mundo pequeño y borrarlo entero**.
"""),
        "perl": ("""
use strict;
use warnings;

package Guardia;
sub new { my ($c, $cb) = @_; return bless { cb => $cb }, $c }
sub DESTROY { $_[0]{cb}->() }          # se ejecuta al morir el objeto

package main;

my $n = <STDIN>;
chomp $n;

my $r;
{
    my $g = Guardia->new(sub { });     # "adquirir": la limpieza va en el guardia
    $r = $n * 2;
}                                        # aquí muere $g y se ejecuta DESTROY

print "resultado=$r\\n";
""", """
**Lo que esta clase enseña en Perl.** Este programa implementa **RAII en Perl**, y funciona por la
propiedad de la clase 131: **el conteo de referencias da destrucción determinista**.

`$g` muere al salir del bloque, `DESTROY` se ejecuta **en ese instante**, y la limpieza ocurre.

Ese patrón tiene nombre en la comunidad —**el objeto guardián**— y CPAN lo empaqueta:

```perl
use Scope::Guard;
my $g = Scope::Guard->new(sub { close $fh });

use Guard;
scope_guard { limpiar() };            # sintaxis más limpia
```

Y esta clase permite señalar por qué Perl puede hacer esto y Java no: **la diferencia entre conteo de
referencias y recolector de trazado**.

| | Conteo (Perl, Tcl, Delphi) | Trazado (Java, Lisp, Smalltalk) |
|---|---|---|
| Cuándo se destruye | **en el instante exacto** | **cuando el recolector quiera** |
| Sirve para RAII | **sí** | no |
| Ciclos | problema | resueltos |
| Coste | en cada copia | en las pausas |

**Esa primera fila es la que decide**: RAII necesita saber **cuándo** muere el objeto, y un recolector
de trazado no lo garantiza. Por eso Java necesitó `try-with-resources` y Python, pese a tener conteo de
referencias en CPython, documenta que no hay que depender de él.

Y Perl tiene además `local` (clases 082 y 096), que es RAII para variables globales:

```perl
{
    local $/ = undef;        # cambia el separador de registro
    $todo = <$fh>;
}                             # y se RESTAURA al salir, pase lo que pase
```

**`local` guarda el valor anterior en una pila interna y lo restaura al salir del ámbito**, incluidas
las salidas por excepción. Es exactamente el enlace dinámico de Lisp de esta misma clase.

Cuatro lenguajes de esta página —Perl, Lisp, PL/I y M— tienen ese mecanismo, y ninguno de los cuatro lo
llamó RAII.
"""),
        "cpp": ("""
#include <iostream>

class Recurso {
    int valor_;
public:
    explicit Recurso(int v) : valor_(v) {}      // adquirir
    ~Recurso() = default;                        // liberar: automático
    Recurso(const Recurso&) = delete;             // NO copiable: propiedad única
    Recurso& operator=(const Recurso&) = delete;
    int valor() const { return valor_; }
};

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    int r = 0;
    {
        const Recurso rec{n};        // nace
        r = rec.valor() * 2;
    }                                 // muere: destructor, pase lo que pase

    std::cout << "resultado=" << r << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Este programa tiene las tres piezas de la propiedad, y merece
verlas por separado:

```cpp
explicit Recurso(int v) : valor_(v) {}         // 1. ADQUIRIR en el constructor
~Recurso() = default;                           // 2. LIBERAR en el destructor
Recurso(const Recurso&) = delete;                // 3. NO COPIABLE: dueño único
```

**La tercera es la que convierte RAII en propiedad.** Sin ella, dos objetos podrían creerse dueños del
mismo recurso y liberarlo dos veces. `= delete` (C++11) es la forma moderna de expresarlo; antes se
declaraba privado y sin definir.

Y con el movimiento (clase 081), la propiedad se puede **transferir**:

```cpp
Recurso(Recurso&&) noexcept;                    // constructor de MOVIMIENTO
Recurso& operator=(Recurso&&) noexcept;
```

**Eso es exactamente el modelo de Rust**: un dueño, transferible, no copiable.

Y aquí está la comparación que cierra esta clase y esta parte del curso:

| | C++ | Rust |
|---|---|---|
| Propiedad única | por convención (`unique_ptr`) | **en el sistema de tipos** |
| Usar tras mover | compila; el objeto queda "válido pero indeterminado" | **no compila** |
| Referencia colgante | compila; comportamiento indefinido | **no compila** |
| Dos referencias mutables | compila | **no compila** |
| Coste en ejecución | ninguno | ninguno |

**Las ideas son las mismas; la diferencia es quién las comprueba.** Los autores de Rust lo dicen
explícitamente: **RAII de C++ es el antepasado directo de la propiedad de Rust**, y el préstamo es la
formalización de lo que las guías de C++ recomiendan de palabra.

Y C++ ha ido en esa dirección con las herramientas:

```cpp
[[nodiscard]] Recurso crear();          // avisa si se ignora el resultado
gsl::owner<T*>                            // marcar quién posee, en las Core Guidelines
clang-tidy --checks=cppcoreguidelines-*   // comprobación estática de las reglas
```

**Las C++ Core Guidelines de Stroustrup y Sutter son, en buena medida, el modelo de Rust escrito como
recomendaciones** — con analizadores que comprueban parte de ellas.

Es un buen final para la Parte 8: **el problema de "quién limpia" recorre sesenta años de diseño de
lenguajes, y la respuesta ha ido pasando del programador a la biblioteca y de la biblioteca al
compilador**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi PROPIED;
  n int(10) const;
end-pi;

dcl-s p pointer;
dcl-s r int(20);

monitor;
  p = %alloc(100);           // adquirir
  r = n * 2;                  // usar
on-error;
  // manejar el error
endmon;

dealloc(n) p;                 // liberar: tambien si hubo error

dsply ('resultado=' + %char(r));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG no tiene destructores ni propiedad, y tiene las dos piezas que
la plataforma pone en su lugar y que ya han aparecido en las clases 103, 130 y 131.

**Primera: `monitor`/`on-error`/`endmon`**, el manejo de errores de RPG, con el que se construye el
patrón de esta clase.

```rpgle
monitor;
  p = %alloc(1000);
  procesar(p);
on-error;
  // limpiar y relanzar
endmon;
dealloc(n) p;
```

Con la advertencia del cierre de esta clase: **eso hay que escribirlo bien en cada uso**, y `on-error`
no cubre todos los caminos si hay `return` dentro.

**Y segunda, la que de verdad resuelve el problema: el grupo de activación** (clase 130).

```text
CRTPGM ... ACTGRP(MIAPP)
RCLACTGRP ACTGRP(MIAPP)      -- libera TODO: memoria, ficheros, transacciones
```

**El dueño de los recursos es el grupo de activación**, no el objeto ni el ámbito. Y su final libera
todo lo suyo, aunque el programa haya fallado.

Es la misma arquitectura que CICS en COBOL de esta clase: **la propiedad está en la unidad de trabajo**.

Y RPG tiene además el `*INLR` de la clase 103, que es propiedad a nivel de programa:

```rpgle
*inlr = *on;      // al terminar: cerrar ficheros, liberar estático, descargar
```

Merece cerrar esta página con la observación que la Parte 8 ha ido construyendo: **las plataformas de
gestión resolvieron el problema de "quién limpia" antes que los lenguajes, y lo resolvieron a una
escala mayor**.

RAII ata la limpieza a un ámbito léxico; CICS y los grupos de activación la atan a **una unidad de
trabajo que puede abarcar varios programas y sobrevivir a un fallo**. Son soluciones al mismo problema
en niveles distintos, y las dos siguen siendo necesarias.
"""),
        "pli": ("""
 propied: procedure options(main);

    declare n fixed binary(31);
    declare r fixed binary(31);
    declare p pointer;
    declare recurso(100) fixed binary(31) based(p);

    get list (n);

    on error begin;                  /* manejador con alcance dinamico */
       put skip list ('error');
    end;

    allocate recurso set(p);          /* adquirir */
    r = n * 2;                         /* usar */
    free recurso;                       /* liberar */

    put skip list ('resultado=' || trim(char(r)));

 end propied;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **no tiene RAII**, y tiene las tres piezas sueltas repartidas
por el lenguaje, que es exactamente el punto de esta clase.

**El almacenamiento `automatic`** (clase 127) es propiedad por ámbito para la memoria de pila: se
reserva al entrar y se libera al salir.

**Las áreas** (clases 128 y 130) son propiedad por región: liberar el área libera todo lo de dentro.

**Y `controlled`** (clase 096) es una pila de generaciones donde el emparejamiento es estructural.

Lo que falta es **el gancho**: no hay forma de ejecutar código al salir de un ámbito. Un procedimiento
PL/I no tiene destructor.

Y sin embargo PL/I tiene la construcción que más se le acerca de esta página, y que ya se ha mencionado
varias veces: **`on finish`**.

```pli
 on finish begin;
    call cerrar_todo();      /* se ejecuta al TERMINAR el programa, normal o no */
 end;
```

Y con manejadores de alcance dinámico (clase 103), un procedimiento puede establecer un manejador que
cubra **todo lo que llame**, y limpiar desde ahí.

Merece cerrar la página de PL/I en esta parte con el balance que se ha ido acumulando: **PL/I tuvo
punteros, reserva dinámica, áreas, multitarea, promesas, excepciones reanudables y aritmética de
arreglos antes que nadie**.

Lo que no tuvo fue **el destructor automático**, que es la pieza que convierte todas las demás en un
sistema. C++ la añadió en 1985, Ada en 1983, y esa pieza es la que hizo posible RAII.

Es una lección de diseño que esta clase deja clara: **un lenguaje no es la suma de sus
características, sino cómo encajan**. PL/I tenía más piezas que casi nadie y le faltó la que las unía.
"""),
        "mumps": ("""
PROPIED ; RAII, propiedad y prestamos -- clase 132
 read n
 new recurso                        ; "adquirir": apila el valor anterior
 set recurso = n * 2
 write "resultado=", recurso, !
 quit                                ; al salir, `new` restaura: liberacion automatica
""", """
**Lo que esta clase enseña en M.** M no tiene destructores ni propiedad, y tiene **`new`**, que es lo
más parecido a RAII que ofrece el lenguaje y que ya ha aparecido en las clases 096, 127 y 131.

```mumps
 new recurso          ; guarda el valor anterior en una pila
 ...
 quit                  ; y lo RESTAURA al salir, pase lo que pase
```

**`new` ata la restauración al final de la rutina**, incluida la salida por error. Es exactamente
`local` de Perl y el enlace dinámico de Lisp de esta misma clase.

Y para los recursos de verdad —bloqueos y transacciones—, M tiene la propiedad atada al **proceso** y a
la **transacción**:

```mumps
 lock +^PACIENTE(id)
 ...
 lock -^PACIENTE(id)
```

Con una garantía que ningún destructor da: **si el proceso muere, el sistema suelta sus bloqueos**. Es
la misma propiedad que la clase 121 destacaba de las transacciones frente a los mutex.

```mumps
 tstart
 ...
 tcommit               ; o si el proceso muere: TROLLBACK automático
```

**El dueño de la transacción es el proceso, y su muerte la deshace.**

Y merece cerrar la Parte 8 desde M con la observación que la recorre entera: **M no tiene ninguna de
las construcciones de esta parte** —ni pila de marcos con destructores, ni montón explícito, ni
recolector, ni propiedad— **y sostiene sistemas con miles de usuarios concurrentes sobre datos
compartidos**.

Lo hace porque **movió el problema de sitio**: la gestión de memoria es del intérprete, la
persistencia es del modelo de datos, la concurrencia es de las transacciones y la limpieza es del
proceso.

No es que M resolviera estos problemas mejor. Es que **eligió un modelo donde la mayoría no aparecen**,
y pagó el precio en todo lo demás — sin tipos, sin ámbitos, sin módulos y sin objetos.

Es, probablemente, la lección más útil de esta parte del curso: **la mitad de los problemas de un
lenguaje vienen de decisiones que podrían no haberse tomado**.
"""),
        "smalltalk": ("""
| n r |

n := stdin nextLine trimBoth asNumber.

r := [ n * 2 ]                    "usar"
    ensure: [ nil ].               "liberar: se ejecuta pase lo que pase"

Transcript show: 'resultado=', r printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk resuelve esta clase con **`ensure:`** y
**`ifCurtailed:`** (clase 103), y no con destructores: **tiene recolector de basura**, así que la
memoria no necesita propiedad, y para los demás recursos usa bloques.

```smalltalk
[ ... ] ensure: [ ... ]              "limpiar SIEMPRE"
[ ... ] ifCurtailed: [ ... ]          "limpiar solo si termina ANORMALMENTE"
'f.txt' asFileReference readStreamDo: [ :s | ... ]   "el patrón with-"
```

Y esa distinción entre `ensure:` e `ifCurtailed:` —limpiar siempre frente a limpiar solo si algo falló—
es más fina que la de casi todos los lenguajes de esta página, y es útil: **deshacer una transacción es
`ifCurtailed:`; cerrar un fichero es `ensure:`**.

Lo que Smalltalk no tiene es propiedad, y no la necesita: **el recolector se ocupa, y las referencias
débiles cubren las cachés** (clase 131).

Y merece cerrar la Parte 8 con la observación que la recorre desde el lado de Smalltalk: **este sistema
tomó la decisión contraria a la de C++ en cada una de las dieciséis clases de esta parte**.

| | C++ | Smalltalk |
|---|---|---|
| Compilación | AOT a nativo | bytecode con JIT |
| Memoria | manual y RAII | **recolector** |
| Referencias | punteros crudos | **solo referencias, sin direcciones** |
| Pila | estructura interna | **objetos inspeccionables** |
| Tipos | estáticos | dinámicos |
| Errores | excepciones que desenrollan | **excepciones REANUDABLES** |

**Y los dos funcionan.** C++ mueve los sistemas donde el rendimiento y el control mandan; Smalltalk
influyó en cómo se programa todo lo demás — y sus técnicas de máquina virtual son las que hacen rápido
a JavaScript y a Java hoy.

Es la conclusión honesta de esta parte del curso: **no hay un conjunto correcto de decisiones sobre
cómo funciona un lenguaje**. Hay compromisos, y cada uno abre unas puertas y cierra otras.
"""),
    },
)
