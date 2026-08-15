# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 131

> [⬅️ Volver a la clase 131](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Crear `n` objetos temporales y dejar que desaparezcan. Aquí hay una fecha que es la raíz de todo:
**John McCarthy inventó la recolección de basura para Lisp en 1959**, y el término es suyo. Y hay un
contraste que ordena la página: **cuatro de estos lenguajes tienen recolector, tres tienen conteo de
referencias y cinco no tienen nada** — y esos cinco llevan sesenta años en producción sin fugas
relevantes.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **liberación automática**, y estos lenguajes lo enseñan porque tienen las tres
> respuestas y las tres funcionan. **Recolector de trazado**: Lisp desde 1959 y Smalltalk desde 1980,
> donde se inventó casi toda la tecnología que hoy usan Java, .NET y Go. **Conteo de referencias**: Perl,
> Tcl y las interfaces de Delphi, con liberación determinista y el problema de los ciclos. **Y nada**:
> COBOL, Fortran, Ada, RPG y PL/I, que lo resuelven **no reservando** o **liberando por región** (clases
> 128 y 130).
>
> Y el dato incómodo es que **la tercera opción es la que gobierna los sistemas más críticos**, porque
> una pausa impredecible es inaceptable donde el tiempo importa.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (número de objetos temporales) → stdout: `creados=<n> estado=recolectado`
- **Regla:** `crear n objetos temporales; al perder la referencia, se recolectan`

| stdin | esperado |
|---|---|
| `5` | `creados=5 estado=recolectado` |
| `0` | `creados=0 estado=recolectado` |
| `3` | `creados=3 estado=recolectado` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Recolec;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TTemporal = class
    Valor: Integer;
  end;

var
  N, I: Integer;
  T: TTemporal;

begin
  Read(N);

  for I := 1 to N do
  begin
    T := TTemporal.Create;       { sin recolector: hay que liberar a mano }
    T.Valor := I;
    T.Free;
  end;

  WriteLn('creados=', IntToStr(N), ' estado=recolectado');
end.
```

**Lo que esta clase enseña en Pascal.** El programa libera a mano con `Free` porque **una clase normal
de Pascal no tiene gestión automática**. Y esa es la mitad de la historia: Pascal tiene **conteo de
referencias, y solo para tres cosas**: cadenas largas, arreglos dinámicos e **interfaces**.

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (dotimes (i n)
    (let ((temporal (make-array 100)))     ; objeto efímero
      (setf (aref temporal 0) i)))
  ;; nadie libera: el recolector se ocupa
  (format t "creados=~D estado=recolectado~%" n))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

for {set i 0} {$i < $n} {incr i} {
    set temporal [lrepeat 100 $i]      ;# objeto efímero
    unset temporal                       ;# la referencia desaparece: se libera
}

puts "creados=$n estado=recolectado"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

for my $i (1 .. $n) {
    my $temporal = [ (0) x 100 ];      # se libera al salir de la vuelta
}

print "creados=$n estado=recolectado\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
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

    std::cout << "creados=" << n << " estado=recolectado\n";
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
RECOLEC ; Recoleccion de basura -- clase 131
 read n
 for i=1:1:n do
 . new temporal
 . set temporal(1) = i
 . ; `new` restaura el valor anterior al salir del bloque
 write "creados=", n, " estado=recolectado", !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
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
```

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

---

## Y de vuelta a la clase

Lo transferible: **el recolector no elimina las fugas, cambia su forma**. Ya no se olvida un `free`: se
olvida quitar una entrada de una caché, o un oyente de una lista, y el objeto vive para siempre porque
**algo lo referencia**. Por eso los lenguajes con recolector tienen referencias débiles y por eso la
pregunta ante una fuga cambia de "¿dónde falta el `free`?" a **"¿quién sigue apuntando a esto?"**.

⏮️ [Volver a la clase 131](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
