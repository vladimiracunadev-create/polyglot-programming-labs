# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 126

> [⬅️ Volver a la clase 126](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Calcular 2ⁿ. Un cálculo tan pequeño que **la mitad de estos lenguajes lo resuelven antes de ejecutar
nada**: C++ con `constexpr`, Lisp con macros, PL/I con su preprocesador y Ada con expresiones
estáticas. Y aquí hay un caso que no encaja en la división AOT/JIT y que la industria está
redescubriendo: **RPG traduce al instalar** —ni antes ni durante— y con eso sobrevivió a un cambio de
procesador.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **cuándo se paga la traducción**, y estos lenguajes lo enseñan porque cubren las
> cuatro posiciones. **AOT clásico**: COBOL, Fortran, Ada, Pascal, C++, con tiempos de compilación
> largos y arranque instantáneo. **JIT**: Smalltalk, y Lisp según la implementación. **Traducción al
> instalar**: RPG con la Machine Interface (clase 125). **Y evaluación en compilación**: `constexpr`,
> macros y preprocesadores, que es AOT llevado al extremo — **el resultado ya está en el ejecutable**.
>
> Y todos comparten el mismo compromiso: **cuanto antes se decide, más rápido arranca y menos se puede
> adaptar a los datos reales**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (0 <= n <= 60) → stdout: `resultado=<2^n>`
- **Regla:** `2 elevado a n`

| stdin | esperado |
|---|---|
| `3` | `resultado=8` |
| `0` | `resultado=1` |
| `5` | `resultado=32` |

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
PROGRAM-ID. POTENCIA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4) COMP.
01  I       PIC 9(4) COMP.
01  R       PIC S9(18) COMP-3 VALUE 1.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE R = R * 2
    END-PERFORM

    MOVE R TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL es **AOT puro**: se compila una vez y el módulo de carga
contiene instrucciones máquina (clase 124). Y su ecosistema lleva la idea al extremo por una razón
operativa muy concreta: **en producción no se compila nada**.

Un módulo de carga se prueba en un entorno, se promociona a otro y se instala en producción **sin
volver a compilar**. La gestión de cambios —Endevor, Changeman— controla que **el binario que corre es
exactamente el que se probó**.

Esa disciplina hace inaceptable cualquier traducción en ejecución: **un JIT introduciría una variable
que nadie ha auditado**.

Y COBOL tiene la optimización guiada por perfil, que es lo que un AOT puede hacer para acercarse al
JIT:

```text
PGO en z/OS: ejecutar con instrumentación, recoger el perfil, recompilar con él
```

Con eso el compilador **coloca las ramas más frecuentes juntas**, mejora la localidad de la caché de
instrucciones y decide qué integrar en línea. Es lo mismo que hacen `-fprofile-use` en GCC y la
optimización guiada por perfil de .NET.

Y hay una decisión de arquitectura de COBOL que es el equivalente exacto del compromiso de esta clase:
**`CALL` estático frente a `CALL` dinámico** (clase 085).

| | `CALL` literal | `CALL` con variable |
|---|---|---|
| Resolución | al enlazar | **en cada llamada** |
| Coste | ninguno | búsqueda en la biblioteca |
| Cambiar el subprograma | **reenlazar a todos** | copiar el módulo y ya |

**Es AOT frente a JIT en miniatura**: uno decide pronto y va más rápido; el otro decide tarde y permite
cambiar sin tocar a nadie.

Y en un sistema con miles de programas, esa flexibilidad vale más que los ciclos: **corregir un módulo
de cálculo de comisiones a las tres de la mañana sin reenlazar cuatrocientos programas** es la razón de
que el `CALL` dinámico exista.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program potencia
   implicit none
   integer :: n, i
   integer(kind=8) :: r

   read(*, *) n

   r = 1_8
   do i = 1, n
      r = r * 2_8
   end do

   write(*, '(A,I0)') 'resultado=', r
end program potencia
```

**Lo que esta clase enseña en Fortran.** Fortran es **AOT puro y con los compiladores más agresivos de
esta página** (clase 124), y esta clase permite señalar lo que eso significa en la práctica.

El `2_8` del programa es el sufijo de **especie** (*kind*): `2_8` es el literal 2 en un entero de 8
bytes. Sin él, `r * 2` con `r` de 64 bits y `2` de 32 podría dar sorpresas de conversión — y `2**60`
en enteros de 32 bits **desborda en silencio**.

Y Fortran tiene la evaluación en compilación desde siempre, con los **parámetros**:

```fortran
integer, parameter :: n = 20
integer, parameter :: tabla(n) = [(i*i, i = 1, n)]     ! calculado AL COMPILAR
real, parameter :: pi = 4.0 * atan(1.0)                 ! y esto también
```

**Una expresión de inicialización de `parameter` se evalúa en tiempo de compilación**, incluidas las
funciones intrínsecas. Es lo mismo que `constexpr` en C++, y en Fortran no hace falta declararlo: **el
contexto lo exige**.

Y sobre AOT frente a JIT, el mundo del cálculo científico tiene una respuesta propia que merece
contarse, porque es la aplicación más pura del cierre de esta clase: **la generación de código
especializado en ejecución**.

Bibliotecas como **ATLAS**, **FFTW** y **OpenBLAS** hacen algo llamativo: **prueban varias
implementaciones al instalarse o al arrancar, miden cuál es más rápida en esa máquina concreta, y usan
esa**.

```text
FFTW: "planificar" la transformada -> mide variantes -> guarda el plan -> ejecuta
```

Eso es exactamente lo que hace un JIT —**decidir con información que solo existe en ejecución**— sin
generar código, eligiendo entre versiones precompiladas.

Y hay quien sí genera código: **LFortran** (clase 124) compila a LLVM y puede hacer JIT, y los marcos
de trabajo modernos como **Julia** —muy influida por Fortran en su dominio— apostaron directamente por
la compilación en ejecución con especialización por tipos.

Es la misma disyuntiva de esta clase, resuelta distinto por dos comunidades que hacen lo mismo.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;              use Ada.Text_IO;
with Ada.Long_Long_Integer_Text_IO; use Ada.Long_Long_Integer_Text_IO;
with Ada.Integer_Text_IO;      use Ada.Integer_Text_IO;

procedure Potencia is
   N : Integer;
   R : Long_Long_Integer := 1;
begin
   Get (N);

   for I in 1 .. N loop
      R := R * 2;
   end loop;

   Put ("resultado=");
   Put (R, Width => 1);
   New_Line;
end Potencia;
```

**Lo que esta clase enseña en Ada.** Ada es **AOT**, y su ecosistema tiene una razón para serlo que va
más allá del rendimiento: **la certificación**.

Un sistema de aviónica certificado bajo **DO-178C** exige demostrar la trazabilidad entre el código
fuente, el objeto y los requisitos, y **verificar el código objeto generado**. Un JIT hace eso
imposible: **el código que se ejecuta no existía cuando se auditó**.

Por eso, en los sectores donde Ada vive, **la traducción en ejecución está descartada por norma**, no
por preferencia.

Y Ada tiene una capacidad de evaluación en compilación notable y poco conocida: **las expresiones
estáticas**.

```ada
N : constant := 2 ** 40;                     --  entero SIN TIPO, exacto
Tabla : constant array (1 .. 5) of Integer := (1, 4, 9, 16, 25);
type Grados is delta 0.01 range 0.0 .. 360.0;
```

**Los números literales de Ada no tienen tipo y su aritmética en compilación es exacta y de precisión
arbitraria.** `2 ** 40` como constante **no desborda**, aunque `Integer` sea de 32 bits, porque el
cálculo lo hace el compilador con precisión ilimitada y solo después comprueba si cabe donde se use.

Es una diferencia real con C y C++, donde una constante entera tiene tipo y desborda.

Y Ada añade la posibilidad de **exigir** que algo se evalúe en compilación:

```ada
pragma Assert (2 ** 10 = 1024);
X : constant Integer := Calcular (5) with Static;   --  Ada 2022
```

Y para el otro lado del compromiso, Ada tiene lo que a un sistema empotrado le interesa: **control
sobre el tamaño y el tiempo**.

```bash
gnatmake -O2 -gnatn        # -gnatn: integración en línea entre unidades
```

```ada
pragma Restrictions (No_Implicit_Heap_Allocations);
pragma Profile (Ravenscar);        --  runtime mínimo y analizable (clase 124)
```

**Con el perfil ZFP** (clase 125), un ejecutable Ada puede caber en kilobytes y arrancar en
microsegundos. Es el extremo opuesto de un JIT, y es exactamente lo que pide un controlador de motor.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Potencia;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I: Integer;
  R: Int64;

begin
  Read(N);

  R := 1;
  for I := 1 to N do
    R := R * 2;

  WriteLn('resultado=', IntToStr(R));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal es **AOT**, y su historia contiene los dos extremos de
esta clase, ya vistos en las clases 123 y 125: **el p-code interpretado de UCSD (1977)** y **la
compilación directa a nativo de Turbo Pascal (1983)**.

Y el resultado de esa competencia es la mejor ilustración del cierre de esta clase: **en 1983, con
máquinas de 4,77 MHz, la portabilidad no compensaba la lentitud, y ganó el nativo**. En 1995, con la
web, la ecuación se invirtió y ganó Java.

**La misma decisión técnica, dos veredictos opuestos, según el contexto.**

Pascal tiene además la evaluación en compilación en su forma clásica:

```pascal
const
  Tam = 1024;
  Doble = Tam * 2;                   { evaluado al compilar }
  Mensaje = 'Version ' + '2.0';       { concatenación en compilación }

{$IF Tam > 512}
  {$MESSAGE WARN 'buffer grande'}
{$IFEND}
```

**Las constantes de Pascal se evalúan al compilar**, y las directivas `{$IF}` permiten compilación
condicional sobre ellas. No llega al nivel de `constexpr` —no se pueden ejecutar funciones— y cubre
lo habitual.

Y hay una capacidad de Free Pascal que encaja de lleno en el compromiso de esta clase: **las
optimizaciones específicas de procesador**.

```bash
fpc -O3 -CpCOREAVX2 -OpCOREAVX2 programa.pas
```

`-Cp` fija el conjunto de instrucciones y `-Op` la microarquitectura para la que optimizar. Es lo mismo
que `ARCH` en COBOL de z/OS y `-march` en GCC, y tiene el compromiso conocido: **el binario va más
rápido y solo corre en máquinas modernas**.

Un JIT no tiene ese problema —**ve el procesador real y genera para él**— y esa es una de sus ventajas
menos citadas y más reales.

Y para móviles, Delphi compila con LLVM a nativo (clase 124), porque **iOS prohíbe la generación de
código en ejecución**: en esa plataforma, el JIT no es una opción técnica sino una decisión de
política de Apple, que dejó fuera a los lenguajes que dependían de él.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (r (expt 2 n)))                  ; enteros de precisión arbitraria
  (format t "resultado=~D~%" r))
```

**Lo que esta clase enseña en Common Lisp.** `(expt 2 n)` funciona para cualquier `n` porque **Common
Lisp tiene enteros de precisión arbitraria en el estándar** (clase 042): `(expt 2 1000)` da el número
completo.

Y Lisp es, otra vez, el lenguaje que rompe la dicotomía de esta clase, y de tres formas.

**Primera: compila cuando quiere.** SBCL compila todo a nativo, incluso lo tecleado en el REPL (clase
124). Es AOT aplicado a cada expresión, con lo que **el arranque es instantáneo y no hay
calentamiento**.

**Segunda: la evaluación en compilación es explícita y total.**

```lisp
(defmacro potencia-fija (n) (expt 2 n))     ; se calcula AL EXPANDIR la macro
(potencia-fija 10)                           ; el compilador ve el literal 1024

#.(expt 2 10)                                 ; macro de LECTURA: se evalúa al LEER
(eval-when (:compile-toplevel) ...)            ; código en tiempo de compilación
```

**`#.`** es especialmente llamativo: evalúa la expresión **durante la lectura del fuente**, así que el
compilador nunca ve el cálculo — ve el resultado. Es lo que la clase 104 señalaba como el riesgo de
`read` sobre datos no fiables, y aquí es su uso legítimo.

**Y tercera: puede generar y compilar código en ejecución.**

```lisp
(let ((f (compile nil `(lambda (x) (* x ,factor)))))
  (funcall f 10))
```

**`compile` sobre una lista construida en marcha genera código nativo**, y `funcall` lo ejecuta. Eso es
un JIT escrito por el programador: se puede especializar una función para un valor concreto que solo
se conoce en ejecución.

Ese patrón se usa de verdad en bibliotecas de Lisp de alto rendimiento: **generar una rutina
especializada para el tamaño de matriz o el formato de datos que llega**, compilarla una vez y
reutilizarla.

Es exactamente lo que hacen los motores de bases de datos modernos con LLVM y lo que hace Julia con
cada combinación de tipos — **y en Lisp es una función del estándar de 1984**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set r 1
for {set i 0} {$i < $n} {incr i} {
    set r [expr {$r * 2}]
}

puts "resultado=$r"
```

**Lo que esta clase enseña en Tcl.** Tcl **compila a bytecode y lo interpreta** (clase 125), sin JIT en
la implementación de referencia. Está en el punto intermedio: **arranque rápido y ejecución más lenta
que el nativo**.

Y ese perfil encaja exactamente con para qué se usa: **guiones de configuración, automatización y
pegamento**, donde el proceso vive segundos y arrancar rápido importa más que el rendimiento
sostenido.

Es el caso que el cierre de esta clase señala: **para un comando de línea de órdenes, un JIT es una
desventaja** — el calentamiento nunca se amortiza.

Tcl tiene además una propiedad relevante y poco conocida: **los enteros son de precisión arbitraria
desde Tcl 8.5**.

```tcl
expr {2 ** 1000}          ;# el número completo, sin desbordar
```

Como en Lisp y en Python, **el desbordamiento no existe**: cuando un valor no cabe en 64 bits, la
implementación cambia a enteros grandes (usa libtommath). Cuesta rendimiento y elimina una clase
entera de errores.

Y hay proyectos que exploran el otro lado:

- **TclQuadcode** compila procedimientos Tcl a **LLVM**, con análisis de tipos para especializar. Es un
  compilador AOT para un lenguaje sin tipos, y su dificultad ilustra el problema: **hay que demostrar
  qué tipos puede tener cada variable**, y en Tcl casi nunca se puede saber con certeza.
- **Jim Tcl** va en la dirección contraria: una implementación completa en 100 KB para sistemas
  empotrados, donde el tamaño importa más que la velocidad.

Y la optimización práctica de Tcl no es de compilación, es de idioma (clases 123 y 124): **usar
llaves, usar los comandos del núcleo y evitar el *shimmering***. En un lenguaje interpretado, **la
diferencia entre el camino compilado y el genérico es mayor que cualquier opción del compilador**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $r = 1;
$r *= 2 for 1 .. $n;

print "resultado=$r\n";
```

**Lo que esta clase enseña en Perl.** Perl **compila a un árbol de operaciones y lo recorre** (clase
124), sin JIT. Arranque rápido, ejecución modesta — el mismo perfil que Tcl y por las mismas razones
de uso.

Y hay un detalle numérico que esta clase obliga a mirar: **`$r *= 2` sesenta veces da 2⁶⁰**, y eso cabe
en el entero de 64 bits de Perl. Con `2 ** 60`, el operador de potencia **devuelve un número en coma
flotante**, y a partir de 2⁵³ perdería precisión.

Es un detalle real: **`**` en Perl siempre calcula en coma flotante**, y para potencias enteras
grandes hay que multiplicar o usar `bigint`:

```perl
use bigint;
print 2 ** 1000;          # el número completo, con enteros grandes
```

Y Perl tiene una capacidad de tiempo de compilación que ya se explicó en la clase 123 y que aquí encaja
como evaluación anticipada:

```perl
use constant DOBLE => 2 * 512;     # se integra EN LÍNEA al compilar
BEGIN { $tabla = calcular() }        # se ejecuta durante la compilación
```

**`use constant` define una subrutina de aridad cero que el compilador integra en línea**, así que la
constante desaparece del código generado. Es la forma que tiene Perl de evaluar en compilación.

Y para el rendimiento de verdad, la respuesta del ecosistema es la que se ha repetido en varias clases:
**bajar a C**.

```perl
use Inline C => 'int doblar(int x) { return x * 2; }';    # ¡C dentro del fuente Perl!
```

**`Inline::C`** compila el código C incrustado la primera vez, **guarda el objeto** y lo reutiliza en
ejecuciones posteriores. Es AOT diferido y guardado — el mismo modelo que la Machine Interface de IBM i
de esta clase, a escala de módulo.

Y `XS`, la interfaz nativa de Perl, es cómo están escritos los módulos rápidos de CPAN: **el 20% del
código que consume el 80% del tiempo, en C**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

constexpr long long potencia(int n) {      // puede evaluarse AL COMPILAR
    long long r = 1;
    for (int i = 0; i < n; ++i) r *= 2;
    return r;
}

static_assert(potencia(10) == 1024);        // comprobado sin ejecutar nada

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "resultado=" << potencia(n) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Este programa contiene **las dos cosas a la vez**, y esa es la
lección: `potencia` **es la misma función**, y

- `static_assert(potencia(10) == 1024)` **la ejecuta en el compilador**;
- `potencia(n)` con `n` leído de la entrada **la ejecuta en el programa**.

**`constexpr` no significa "siempre en compilación": significa "puede".** Y `consteval` (C++20)
significa "obligatoriamente".

Esa distinción es de las mejores ideas recientes de C++, porque permite escribir **una sola versión** de
un algoritmo que sirve para las dos fases.

Y desde C++20, `constexpr` admite casi todo: bucles, condicionales, `new` y `delete` —si se libera
dentro—, `std::vector` y `std::string` en tiempo de compilación. Es un intérprete de C++ dentro del
compilador (clase 124).

Sobre AOT frente a JIT, C++ está firmemente en el primero, y su ecosistema tiene las herramientas para
acercarse al segundo:

```bash
g++ -O3 -march=native                # generar para ESTA máquina
g++ -flto                             # optimizar viendo TODO el programa (clase 123)
g++ -fprofile-generate ... && g++ -fprofile-use    # optimización guiada por PERFIL
```

**La optimización guiada por perfil (PGO)** es la respuesta del AOT al JIT: ejecutar el programa con
datos reales, recoger qué ramas se toman y qué funciones son calientes, y recompilar con esa
información.

Con PGO, un compilador AOT obtiene **lo que un JIT sabe de serie**: el comportamiento real. La
diferencia es que **hay que hacerlo a mano y con datos representativos**, mientras que el JIT lo hace
solo y se adapta si el patrón cambia.

Y hay un tercer camino que C++ usa en producción: **generar y compilar código en ejecución con LLVM**,
como hacen los motores de bases de datos para especializar una consulta.

Es exactamente lo que hace el `compile` de Lisp de esta misma clase, con más maquinaria.

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

dcl-pi POTENCIA;
  n int(10) const;
end-pi;

dcl-s i int(10);
dcl-s r int(20) inz(1);

for i = 1 to n;
  r = r * 2;
endfor;

dsply ('resultado=' + %char(r));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG es **el caso que no encaja en la dicotomía de esta clase**, y
ya se ha contado en las clases 123, 124 y 125 — aquí toca ponerlo en su sitio del compromiso.

```text
AOT clásico:   fuente → nativo → se ejecuta
JIT:           fuente → bytecode → nativo EN EJECUCIÓN, cada vez
IBM i:         fuente → MI → nativo AL INSTALAR, guardado en el objeto
```

Ese tercer modelo tiene, medido contra los otros dos:

| | AOT | JIT | **MI de IBM i** |
|---|---|---|---|
| Arranque | **instantáneo** | lento (calentamiento) | **instantáneo** |
| Rendimiento sostenido | alto | **muy alto** (especializa) | alto |
| Portabilidad del binario | ninguna | **total** | **total** |
| Aprovecha el procesador nuevo | no, hay que recompilar | **sí** | **sí, al retraducir** |
| Auditable | **sí** | difícil | **sí** |

Es, en la práctica, **casi todas las ventajas de los dos**, y el motivo de que la industria esté
volviendo a ese punto con las **imágenes nativas de GraalVM** y el **AOT de .NET**: compilar el
bytecode a nativo antes de desplegar, para tener portabilidad de distribución y arranque instantáneo.

Lo que RPG no obtiene, y es lo que el cierre de esta clase señala, es **la especialización con datos
reales**: la traducción MI ocurre antes de ejecutar, así que no sabe qué ramas se toman ni qué tipos
llegan.

Y hay una capacidad de la plataforma que la acerca: **la retraducción**.

```text
CHGPGM PGM(MIAPP) OPTIMIZE(*FULL)
```

Un programa se puede **retraducir con más optimización sin recompilar el fuente**, porque el MI sigue
guardado en el objeto. Se puede desplegar con optimización baja para depurar y subirla después, sobre
el mismo objeto.

Es una flexibilidad que ningún ejecutable nativo tiene, y viene de haber guardado la representación
intermedia.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 potencia: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare r fixed binary(63) initial(1);

    get list (n);

    do i = 1 to n;
       r = r * 2;
    end;

    put skip list ('resultado=' || trim(char(r)));

 end potencia;
```

**Lo que esta clase enseña en PL/I.** PL/I es **AOT**, con la misma disciplina de producción que COBOL
(clase 126, apartado COBOL): **el binario que corre es el que se auditó**.

Y PL/I tiene **la evaluación en compilación más potente de esta página**, ya nombrada en las clases 088
y 115: **su preprocesador es un lenguaje completo**.

```pli
 %declare tam fixed;
 %tam = 2 ** 10;                   /* CALCULADO en tiempo de compilación */

 %if tam > 512 %then %do;
    declare buffer char(1024);
 %end;
 %else %do;
    declare buffer char(256);
 %end;
```

**El preprocesador tiene aritmética, variables, condicionales, bucles y procedimientos propios**, así
que puede calcular tablas, generar declaraciones y decidir qué código se compila.

Es lo que en C++ hacen `constexpr` y las plantillas, y en Rust las macros procedurales — con una
diferencia importante y ya señalada en la clase 123: **trabaja sobre texto, no sobre estructura**, y
por eso el código que se depura no es el que se escribió.

Y esta clase permite añadir un dato de rendimiento que suele sorprender: **el compilador de PL/I fue
donde nacieron varias técnicas de optimización que hoy son universales** (clase 124) — la eliminación
de subexpresiones comunes, el movimiento de código invariante y la asignación de registros por
coloreado de grafos, todo en IBM Research trabajando sobre PL/I y Fortran.

**John Cocke recibió el Turing por eso, y de ese trabajo salió RISC**: la observación de que si el
compilador es lo bastante bueno, el procesador no necesita instrucciones complejas.

Es una conexión que cierra bien esta clase: **la calidad de la compilación anticipada fue tan buena que
cambió el diseño de los procesadores**. La discusión AOT contra JIT presupone compiladores que ya son
extraordinariamente buenos, y buena parte de eso se construyó aquí.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
POTENCIA ; AOT frente a JIT -- clase 126
 read n
 set r = 1
 for i=1:1:n set r = r * 2
 write "resultado=", r, !
 quit
```

**Lo que esta clase enseña en M.** M es **interpretado con compilación a objeto** (clase 124), y su
posición en el compromiso de esta clase es peculiar: **el coste de traducción es irrelevante porque el
tiempo se va en otro sitio**.

Un programa M típico pasa la mayor parte de su tiempo **recorriendo árboles B en memoria compartida y
en disco**, no ejecutando aritmética. Optimizar el intérprete un 30% no cambia nada si el 90% del
tiempo está en el acceso a datos.

Es un recordatorio útil del cierre de esta clase: **la pregunta "¿AOT o JIT?" solo importa si el cuello
de botella es la ejecución de código**.

Y hay un detalle numérico que esta clase obliga a mirar en M: **la precisión**. El estándar de M exige
**al menos 15 dígitos significativos** en la aritmética, y las implementaciones tradicionales usan
**decimal de coma fija** —no coma flotante binaria— precisamente por su origen: **cantidades de
medicamento, importes y dosis**.

```mumps
 write 0.1 + 0.2        ; .3   -- exacto, porque es DECIMAL
```

Ese resultado sorprende a quien viene de C o Java, y es la misma decisión que el `COMP-3` de COBOL
(clase 042): **cuando el dominio es sanitario o financiero, el decimal exacto no es negociable**.

Y para 2⁶⁰, las implementaciones difieren: **YottaDB e IRIS manejan enteros grandes** hasta el límite
de su precisión decimal, y el resultado de este programa es exacto.

Sobre la modernización, las implementaciones actuales sí hacen trabajo de compilación serio: **IRIS
compila ObjectScript a bytecode con caché compartida entre procesos**, y las rutinas más usadas quedan
en memoria para todos.

Es una decisión coherente con el modelo del sistema: **compartir lo caro entre procesos**, que es lo
mismo que hace con los datos.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n r |

n := stdin nextLine trimBoth asNumber.

r := 2 raisedTo: n.        "enteros de precisión arbitraria"

Transcript show: 'resultado=', r printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** `2 raisedTo: n` da el resultado exacto para cualquier `n`
porque **Smalltalk tiene enteros de precisión arbitraria desde 1980**: `SmallInteger` y
`LargePositiveInteger`, con **promoción automática** cuando el valor deja de caber.

```smalltalk
(2 raisedTo: 1000) class.       "LargePositiveInteger"
1073741823 class.                "SmallInteger"
(1073741823 + 1) class.           "LargePositiveInteger -- promoción automática"
```

Y Smalltalk es **el representante del JIT** en esta página (clase 124), con la tecnología que después
fue HotSpot.

La ventaja del JIT se ve en el perfil de uso de Smalltalk: **una imagen que lleva horas o días
funcionando**, con el mismo código ejecutándose millones de veces. Ahí el calentamiento se amortiza
enseguida y la especialización con datos reales gana.

Y la desventaja se ve igual de claro: **arrancar una imagen de Pharo tarda**, y para un guion de línea
de órdenes eso es inaceptable. Es exactamente el compromiso del cierre de esta clase.

Lo que hace especial al JIT de Smalltalk, y lo que lo distingue de un compilador AOT, es que **puede
optimizar suponiendo cosas que podrían dejar de ser ciertas**:

```text
"este envío de + siempre ha sido a un SmallInteger" → integrar la suma en línea
"pero si un día llega un Fraction"                   → DESOPTIMIZAR y volver al caso general
```

**La desoptimización es lo que permite ser agresivo**, y es imposible en AOT: un compilador que no
puede deshacer una suposición no puede permitirse hacerla.

Y en Smalltalk esa maquinaria es visible desde el propio lenguaje:

```smalltalk
Smalltalk vm parameterAt: 46.        "número de métodos compilados por el JIT"
Smalltalk vm statisticsReport.
```

**El programa puede consultar las estadísticas de su propio JIT en marcha.** Es coherente con todo lo
demás de esta serie: cuando todo es un objeto, la máquina virtual también lo es.

---

## Y de vuelta a la clase

Lo transferible: **el JIT gana cuando sabe algo que el compilador no podía saber**. Un compilador AOT
ve el código; un JIT ve **los datos reales, los tipos que de verdad llegan y qué ramas se toman**, y
puede especializar. Por eso un JIT bien afinado supera a veces al AOT en programas de larga duración,
y por eso pierde siempre en arranque. Cuando elijas —imagen nativa, AOT, JIT, optimización guiada por
perfil— la pregunta es **cuánto vive el proceso**: un comando de línea de órdenes y un servidor de
ocho meses necesitan lo contrario.

⏮️ [Volver a la clase 126](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
