# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 147

> [⬅️ Volver a la clase 147](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una línea de ceros y unos: si todos son uno, la integración está verde. Es el resumen exacto de lo que
hace una integración continua, y esta clase existe porque **el "todos" es la parte difícil cuando hay
doce lenguajes**. Y aquí hay un dato que cambia la historia habitual: **CPAN Testers lleva desde 1998
compilando y probando cada versión publicada en cientos de combinaciones de sistema y compilador** — es
integración continua distribuida, y es anterior al término.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **verificación automática y continua**, y estos lenguajes lo enseñan porque
> tienen los casos más incómodos. **Fortran necesita el clúster para probarse de verdad.** **RPG y COBOL
> necesitan una máquina que no está en la nube.** **C++ tiene una explosión combinatoria de compiladores,
> versiones y opciones.** **Y Ada tiene que certificar la propia cadena de herramientas.**
>
> Y aparece la tensión que decide si una integración continua sirve: **entre lo rápido que se ejecuta y
> lo mucho que comprueba**. Cada lenguaje de esta página la resuelve en un punto distinto.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con 0 y 1 (resultado de cada paso; 1 = pasó) → stdout: `ci=<verde|rojo>`
- **Regla:** `verde si todos los pasos son 1`

| stdin | esperado |
|---|---|
| `1 1 1` | `ci=verde` |
| `1 0 1` | `ci=rojo` |
| `1 1` | `ci=verde` |

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
PROGRAM-ID. CIVERDE.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  ESTADO  PIC X(5) VALUE "verde".

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = "0"
            MOVE "rojo" TO ESTADO
        END-IF
    END-PERFORM

    DISPLAY "ci=" FUNCTION TRIM(ESTADO)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El mundo mainframe tuvo integración continua antes del nombre, y
merece explicar en qué consistía porque la forma es reconocible: **la compilación nocturna**.

```jcl
//NOCTURNO JOB CLASS=B,MSGCLASS=X
//COMPILA  EXEC PROC=COBCOMP,MEMBER=TODOS
//PRUEBAS  EXEC PGM=EJECUTOR,COND=(0,LT,COMPILA)
//COMPARA  EXEC PGM=SUPERC       <-- comparar salidas con las esperadas
//INFORME  EXEC PGM=IEBGENER,COND=EVEN
```

**Todo el sistema se compilaba de noche, se ejecutaba con juegos de datos de prueba y se comparaban las
salidas con las esperadas** (clase 140). Por la mañana había un informe.

Y el motivo por el que era nocturno y no continuo es el que define la época: **el tiempo de máquina
costaba dinero y se facturaba** (clase 142). No se compilaba "por si acaso".

Y el paso de promoción entre entornos de Endevor (clase 143) añadía la parte de puerta:

```text
Para promover de QA a PROD:
  - la compilación debe estar limpia
  - las pruebas de regresión deben haber pasado
  - y alguien distinto al autor debe aprobar
```

**Eso es exactamente una regla de protección de rama con revisión obligatoria y comprobaciones
requeridas**, en un sistema de 1985.

Y hoy, el mundo COBOL se ha conectado a la integración continua moderna, y merece conocer cómo:

| Pieza | Qué hace |
|---|---|
| **Zowe** | API REST sobre z/OS: lanzar trabajos y leer resultados desde fuera |
| **IBM Dependency Based Build (DBB)** | construcción con grafo de dependencias, desde Groovy |
| **GnuCOBOL en el corredor** | compilar y probar la lógica sin mainframe, para lo portable |
| **Ejecutores autoalojados** | un corredor de GitHub Actions dentro del centro de datos |
| **Micro Focus / Rocket** | COBOL en Linux y Windows, para probar en la nube |

**La estrategia mixta es la que suele funcionar**: **la lógica de negocio pura se compila y prueba con
GnuCOBOL en el corredor de la nube, en segundos**, y **solo lo que necesita CICS, DB2 o VSAM se lanza
contra el mainframe**.

Es la aplicación directa de la primera regla del cierre de esta clase —**que sea rápida**— a un entorno
donde la máquina de verdad es lenta y cara: **separar lo que se puede comprobar barato de lo que
necesita el sistema real**, y ejecutar lo barato en cada cambio.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program civerde
   implicit none
   character(len=200) :: linea
   integer :: i
   logical :: verde

   read(*, '(A)') linea
   verde = .true.

   do i = 1, len_trim(linea)
      if (linea(i:i) == '0') verde = .false.
   end do

   if (verde) then
      write(*, '(A)') 'ci=verde'
   else
      write(*, '(A)') 'ci=rojo'
   end if
end program civerde
```

**Lo que esta clase enseña en Fortran.** Fortran tiene el problema más difícil de esta página, y merece
enunciarlo con claridad: **el programa de verdad no cabe en un corredor de integración continua**.

Un código de simulación se ejecuta en **cientos o miles de núcleos, durante horas**, con MPI y con
bibliotecas específicas del clúster. Un corredor de la nube tiene dos núcleos y siete minutos de
paciencia.

Y la respuesta de la comunidad es una estrategia por niveles que es transferible a cualquier proyecto
con pruebas caras:

**Nivel 1 — en cada cambio, en el corredor (minutos):**

```bash
gfortran -std=f2018 -Wall -Werror -fcheck=all -c src/*.f90    # ¿compila limpio?
fpm test                                                        # pruebas unitarias
mpirun -np 2 ./prog_test                                         # MPI con 2 procesos
```

**Nivel 2 — cada noche, en un ejecutador propio (horas):**

```bash
# casos de referencia pequeños, con comparación numérica tolerante (clase 140)
# y la matriz de compiladores: gfortran, ifx, nvfortran, flang
```

**Nivel 3 — antes de cada versión, en el clúster (días):**

```bash
# el caso de producción completo, con 1.000 procesos
# comparado contra los resultados publicados de la versión anterior
```

**Y el nivel 1 es el que aporta el 80 % del valor**, porque caza lo que de verdad se rompe a diario:
errores de compilación, interfaces incompatibles y fallos de lógica en las rutinas pequeñas.

Y hay dos comprobaciones baratas que merecen destacarse porque cazan mucho:

**Primera, la matriz de compiladores.** Cada compilador de Fortran acepta un subconjunto distinto de
extensiones, así que **compilar con dos compiladores distintos detecta el código no estándar** — que es
la principal causa de que un programa no sea portable.

**Y segunda, `-fcheck=all` con `-ffpe-trap`** (clase 138), que convierte comportamientos silenciosos en
errores localizados.

Y una advertencia de la segunda regla del cierre, específica de este dominio: **las pruebas numéricas
con tolerancia son la fuente número uno de pruebas intermitentes**. Una tolerancia demasiado ajustada
falla según el compilador y la máquina, y el equipo aprende a reintentar hasta que pase.

La disciplina que lo evita: **la tolerancia se justifica por el análisis del error, no por lo que hizo
falta para que pasara**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Civerde is
   Linea  : String (1 .. 200);
   Ultimo : Natural;
   Verde  : Boolean := True;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = '0' then
         Verde := False;
      end if;
   end loop;

   if Verde then
      Put_Line ("ci=verde");
   else
      Put_Line ("ci=rojo");
   end if;
end Civerde;
```

**Lo que esta clase enseña en Ada.** Ada tiene la integración continua más exigente de esta página, y es
porque **en sus dominios la comprobación no es una buena práctica: es un requisito con auditor**.

Una canalización típica de un proyecto certificado:

```yaml
- gprbuild -j0 -p                     # construir con las opciones exactas del proyecto
- gnatcheck -rules -from=proyecto.rules    # estándar de codificación (clase 146)
- gnattest --harness-only && ./run_tests    # pruebas generadas y ejecutadas
- gnatcoverage --level=stmt+mcdc            # cobertura MC/DC (clase 139)
- gnatprove --level=2 --report=all           # DEMOSTRACIÓN formal
- gnatmetric                                  # métricas de complejidad
- trazabilidad: requisito -> código -> prueba  # y que no falte ninguno
```

**El paso de `gnatprove` es el que no existe en ningún otro ecosistema de esta página**: no ejecuta
nada, **intenta demostrar matemáticamente que no hay errores de ejecución** —desbordamiento, índices
fuera de rango, división por cero— **para todas las entradas posibles** (clase 118).

Y en integración continua eso tiene una propiedad interesante: **el resultado es una cuenta**.

```text
Summary of SPARK analysis
  flow analysis: 1240 checks, 1240 proved
  proof:         3871 checks, 3862 proved, 9 NOT PROVED
```

**Esos 9 sin demostrar son la lista de trabajo pendiente**, y la regla del proyecto suele ser que **no
puede crecer**. Es una métrica de calidad objetiva, y encaja perfectamente en una puerta de integración
continua.

Y el paso de trazabilidad merece explicarse, porque es un tipo de comprobación que casi nadie hace fuera
de estos sectores: **una herramienta verifica que cada requisito tiene código que lo implementa y
pruebas que lo cubren, y que cada línea de código responde a algún requisito**.

**Código sin requisito asociado es un hallazgo**, igual que un requisito sin código.

Es la versión estricta de la cobertura, y su motivo es concreto: en un sistema certificado, **código que
nadie pidió es código que nadie ha analizado**.

Y sobre la primera regla del cierre —que sea rápida— Ada tiene el problema de esta página en su forma
más cruda: **`gnatprove` puede tardar horas**. La estrategia es la misma que Fortran: **las
demostraciones rápidas en cada cambio y las lentas por la noche**, con la lista de comprobaciones no
demostradas como estado compartido.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Civerde;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I: Integer;
  Verde: Boolean;

begin
  ReadLn(Linea);
  Verde := True;

  for I := 1 to Length(Linea) do
    if Linea[I] = '0' then Verde := False;

  if Verde then
    WriteLn('ci=verde')
  else
    WriteLn('ci=rojo');
end.
```

**Lo que esta clase enseña en Pascal.** Free Pascal tiene una característica que lo hace excepcionalmente
cómodo en integración continua y que merece destacarse: **compila para casi cualquier destino desde
cualquier máquina**.

```bash
fpc -Twin64 -Px86_64 prog.pas      # ejecutable de Windows... desde Linux
fpc -Tlinux -Parm prog.pas          # ARM
fpc -Tdarwin -Paarch64 prog.pas      # macOS Apple Silicon
```

**Compilación cruzada nativa, sin contenedores ni emulación**, porque el compilador está escrito en
Pascal y se compila a sí mismo para cada plataforma.

Y en integración continua eso significa que **una sola tarea puede producir los binarios de todas las
plataformas**, en lugar de necesitar un corredor por sistema operativo.

Es una ventaja considerable frente a C++ en esta página, donde compilar para Windows desde Linux exige
montar una cadena de herramientas cruzada completa.

Y la canalización típica del ecosistema:

```yaml
- fpc -Sew -vw -O2 src/*.pas        # -Sew: los AVISOS son errores
- ./pruebas/ejecutar_fpcunit         # FPCUnit, con salida en XML de JUnit
- fpc -gh ./pruebas/fugas             # heaptrc: detectar fugas (clase 138)
- lazbuild proyecto.lpi                # construir un proyecto de Lazarus
```

**`-Sew` merece la mención** porque es la aplicación de la regla del cierre: **si el aviso no rompe la
compilación, se acumula hasta ser ruido**. Un proyecto con 400 avisos es un proyecto sin avisos útiles.

Y hay una comprobación específica del ecosistema Delphi que conviene conocer porque es cara de descubrir
de otra forma: **la compilación en las dos arquitecturas**.

```text
Un proyecto que compila en Win32 puede fallar en Win64 por:
  - Integer(Puntero): truncamiento (clase 140)
  - código ensamblador en línea: NO existe en Win64 con la misma sintaxis
  - Extended de 80 bits que pasa a 64: resultados distintos
```

**Poner las dos arquitecturas en la matriz de integración continua** es lo que evita descubrir eso en la
migración, tres años después.

Y es la lección general de esta página: **la matriz de la integración continua debe cubrir todos los
destinos que se prometen**, porque lo que no está en la matriz no está comprobado — y se descubrirá en
el peor momento.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((linea (read-line))
      (verde t))
  (loop for c across linea
        do (when (char= c #\0) (setf verde nil)))
  (format t "ci=~A~%" (if verde "verde" "rojo")))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene una particularidad en integración continua que
se deriva de la Parte 8 y que merece explicarse: **hay que forzar la construcción desde cero**.

El flujo normal de desarrollo en Lisp es incremental sobre una imagen viva (clase 124), y eso significa
que **el estado de la imagen puede contener cosas que no están en los ficheros** (clase 145).

De ahí que la canalización empiece siempre igual:

```bash
sbcl --non-interactive \
     --eval '(asdf:load-system "mi-proyecto" :force t)' \
     --eval '(asdf:test-system "mi-proyecto")'
```

**`:force t` recompila todo desde cero**, y es lo que convierte la integración continua en una
comprobación de verdad: **si el sistema no se puede cargar desde los ficheros en una imagen limpia, está
roto**, aunque funcione en la máquina de quien lo escribió.

Y Lisp tiene una propiedad que hace su integración continua muy informativa, y es la de la clase 137:
**los avisos del compilador son un analizador estático**.

```lisp
(handler-bind ((warning (lambda (c)
                          (format *error-output* "~A~%" c)
                          (setf *hubo-avisos* t))))
  (asdf:load-system "mi-proyecto" :force t))
(when *hubo-avisos* (sb-ext:exit :code 1))     ; los avisos ROMPEN la construcción
```

**Convertir los avisos de SBCL en fallo de construcción** es la práctica recomendada, porque SBCL avisa
de conflictos de tipos deducidos, variables sin usar y código inalcanzable — cosas que en otros
lenguajes requieren un analizador aparte.

Y el ecosistema:

| Herramienta | Notas |
|---|---|
| **`asdf:test-system`** | el punto de entrada estándar de las pruebas |
| **FiveAM / Parachute** | marcos con salida en formatos consumibles |
| **`sb-cover`** | cobertura de SBCL, con informe HTML |
| **`qlot`** | fijar versiones por proyecto (clase 143) |
| **`roswell`** | gestor de implementaciones: probar en SBCL, CCL, ECL, ABCL |

**Roswell merece la mención final** porque resuelve la matriz de esta página en Lisp: **probar en varias
implementaciones a la vez**.

Y eso importa más de lo que parece: **el estándar de Common Lisp deja muchas cosas al criterio de la
implementación** —el tamaño de los enteros nativos, el comportamiento de los flujos, las extensiones de
hilos—, así que **código que funciona en SBCL puede fallar en CCL**.

Es exactamente el mismo argumento que la matriz de compiladores de Fortran de esta página: **probar en
más de una implementación es lo que separa el código portable del que solo funciona aquí**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set verde 1
foreach v [split [string trim $linea]] {
    if {$v eq "0"} { set verde 0 }
}

puts "ci=[expr {$verde ? {verde} : {rojo}}]"
```

**Lo que esta clase enseña en Tcl.** Tcl tiene con esta clase una relación que merece contarse, porque
**es el lenguaje con el que se automatizó buena parte de la industria antes de que existieran las
herramientas actuales**.

Y la pieza clave tiene nombre: **Expect**, escrito por Don Libes en 1990.

```tcl
package require Expect

spawn ssh servidor
expect "password:"
send "$::env(CLAVE)\r"
expect "$ "
send "make test\r"
expect {
    "PASSED" { exit 0 }
    "FAILED" { exit 1 }
    timeout  { puts "sin respuesta"; exit 2 }
}
```

**Expect automatiza programas interactivos**: espera un texto, responde, y decide según lo que llega.

Y su importancia histórica es grande: **antes de que las herramientas tuvieran modo no interactivo,
Expect era la única forma de automatizarlas**. Se usó —y se usa— para configurar routers, instalar
sistemas, probar terminales y lanzar compilaciones en máquinas remotas.

Es el antepasado directo de cualquier automatización de interfaces sin API, y sigue siendo la respuesta
cuando algo no tiene otra.

Y Tcl aporta a esta clase el papel que sigue teniendo hoy: **el lenguaje de los guiones de
construcción**.

```tcl
# comprobar los 12 lenguajes de este curso, en paralelo
foreach lang {cobol fortran ada pascal lisp tcl perl cpp} {
    set pid [exec ./verificar.sh $lang &]
    lappend pids $lang $pid
}
```

Y en la industria de diseño de circuitos, **Tcl es el lenguaje de guion de todas las herramientas
principales** —Synopsys, Cadence, Xilinx—, así que **la integración continua de un chip está escrita en
Tcl**.

Y merece cerrar con la observación que conecta con la segunda regla de esta clase: **Expect enseñó el
problema de los tiempos de espera**.

Un guion de Expect con un `timeout` demasiado corto **falla a veces y pasa a veces**, según la carga de
la máquina. Es la prueba intermitente en su forma original, y la solución que Expect propuso hace treinta
y cinco años sigue siendo la correcta: **esperar por un evento concreto, no por un tiempo**.

Toda prueba que contiene una espera fija es una prueba intermitente esperando a manifestarse.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my $verde = !grep { $_ eq '0' } split ' ', $linea;

print "ci=", ($verde ? 'verde' : 'rojo'), "\n";
```

**Lo que esta clase enseña en Perl.** `grep` en contexto booleano devuelve cuántos elementos cumplen la
condición, así que `!grep {...}` es "ninguno cumple" — un idioma compacto y muy de Perl.

Y aquí está el dato del gancho de esta clase, que merece desarrollarse: **CPAN Testers es integración
continua distribuida desde 1998**.

El funcionamiento es tan simple como eficaz:

```text
1. Alguien sube una versión a CPAN.
2. Cientos de voluntarios tienen máquinas que descargan lo nuevo automáticamente.
3. Cada una lo compila y ejecuta sus pruebas en SU combinación:
   Linux/Perl 5.36, FreeBSD/5.32, Windows/Strawberry, AIX, Solaris, ARM...
4. Y envía el informe a una base de datos pública.
```

**El resultado es una matriz de compatibilidad que ningún proyecto podría permitirse construir**, con
sistemas operativos y arquitecturas que el autor no tiene ni conoce.

Y su valor práctico es directo: **antes de instalar un módulo, se ve si pasa en tu plataforma exacta**;
y **al publicar, llegan informes de fallo en sistemas que nunca has tocado**.

Es un modelo que casi nadie ha reproducido —requiere una comunidad dispuesta a donar cómputo— y merece
conocerse porque resuelve el problema más caro de la matriz de esta página: **cubrir plataformas que no
tienes**.

Y el resto del ecosistema de Perl en integración continua:

```bash
cpanm --installdeps --notest .
prove -lr --jobs 4 t/            # el corredor de TAP, en paralelo
cover -test -report html          # Devel::Cover
perlcritic --severity 3 lib/       # el estándar (clase 146)
```

**`prove --jobs 4`** ejecuta los ficheros de prueba en paralelo, que es la aplicación directa de la
primera regla del cierre.

Y merece cerrar con la advertencia sobre la segunda regla, porque el paralelismo la provoca: **las
pruebas que comparten un fichero temporal, un puerto o una base de datos fallan de forma intermitente
al paralelizar**.

Y la disciplina que lo evita es la misma en todos los lenguajes: **cada prueba crea y destruye su propio
estado**, con un nombre único —`File::Temp`, un puerto efímero, un esquema con sufijo aleatorio—. Es
más trabajo al escribirla y es lo que permite ejecutar en paralelo sin miedo.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string v;
    bool verde = true;

    while (std::cin >> v)
        if (v == "0") verde = false;

    std::cout << "ci=" << (verde ? "verde" : "rojo") << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene el problema de la matriz en su forma más severa, y merece
verlo en números.

**Las dimensiones reales de un proyecto C++ serio:**

```text
compilador:   gcc, clang, msvc, icx            (4)
versión:      3 versiones soportadas de cada    (3)
estándar:     C++17, C++20, C++23                (3)
tipo:         Debug, Release, RelWithDebInfo      (3)
plataforma:   Linux, Windows, macOS               (3)
arquitectura: x86-64, arm64                        (2)
desinfectante: ninguno, ASan+UBSan, TSan            (3)
                                            = 1.944 combinaciones
```

**Nadie ejecuta 1.944 construcciones en cada cambio.** Así que la práctica real de esta página es
elegir:

```yaml
# en CADA cambio: rápido, y las combinaciones que más cazan
- gcc-13   Release  C++20  Linux      # la principal
- clang-17 Debug    C++20  Linux + ASan/UBSan   # detecta comportamiento indefinido
- msvc     Release  C++20  Windows      # otro compilador, otras reglas

# cada noche: la matriz amplia, TSan, y los compiladores antiguos
# antes de publicar: todo
```

**La segunda línea es la que más rinde y merece justificarse**: `-fsanitize=address,undefined` **detecta
en ejecución lo que el lenguaje no detecta** (clase 137), y un cambio que introduce un acceso fuera de
límites falla en el acto en lugar de dentro de seis meses.

Y sobre la primera regla del cierre —que sea rápida—, C++ tiene herramientas específicas porque el
problema es suyo:

| Herramienta | Qué ahorra |
|---|---|
| **ccache / sccache** | no recompilar lo que no cambió, entre ejecuciones |
| **ninja** | planificador de construcción rápido, frente a `make` |
| **Unity builds** | juntar `.cpp` para pagar las cabeceras una vez |
| **`-fsyntax-only`** | comprobar sintaxis sin generar código |
| **Módulos (C++20)** | atacan la raíz: no repetir el texto de las cabeceras |
| **`include-what-you-use`** | quitar inclusiones innecesarias: menos recompilación |

**`ccache` con la caché compartida entre ejecuciones de la integración continua** es, en la práctica, lo
que más tiempo ahorra en un proyecto C++ grande: **construcciones de cuarenta minutos bajan a tres**.

Y la advertencia que va con ello, y conecta con la clase 144: **una caché de compilación tiene que
tener en cuenta todo lo que afecta al resultado** —opciones, versión del compilador, contenido de las
cabeceras— o produce binarios incorrectos.

`ccache` lo hace bien, y es la razón por la que se usa esa herramienta y no un guion casero.

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

dcl-pi CIVERDE;
  linea char(200) const;
end-pi;

dcl-s i     int(10);
dcl-s verde ind;

verde = *on;

for i = 1 to %len(%trimr(linea));
  if %subst(linea : i : 1) = '0';
    verde = *off;
  endif;
endfor;

if verde;
  dsply 'ci=verde';
else;
  dsply 'ci=rojo';
endif;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** IBM i tiene el problema práctico de esta clase en su forma más
concreta: **no hay un corredor de IBM i en la nube**. El sistema es propietario, la arquitectura es
POWER, y no existe un contenedor con él dentro.

Y la solución que la comunidad adoptó merece conocerse porque es la respuesta general al mismo problema
en cualquier plataforma cerrada: **el ejecutador autoalojado**.

```yaml
# .github/workflows/ci.yml
jobs:
  construir:
    runs-on: [self-hosted, ibmi]      # un corredor DENTRO del centro de datos
    steps:
      - uses: actions/checkout@v4
      - run: makei build              # ibmi-bob (clase 144)
      - run: makei check               # RPGUnit (clase 139)
```

**Se instala un corredor de GitHub Actions o de GitLab en el propio IBM i** —el sistema tiene PASE, un
entorno AIX, con Git, Python y Node— **y las tareas se ejecutan ahí**, contra el sistema real.

Y la canalización típica:

```text
1. Compilar todos los objetos afectados     (ibmi-bob resuelve el grafo)
2. Ejecutar RPGUnit sobre los programas de servicio
3. Comprobar las FIRMAS de los programas de servicio (clase 143)
4. Crear un fichero de salvado con los objetos    (clase 144)
5. Y publicarlo como artefacto para el despliegue (clase 148)
```

**El paso 3 merece destacarse** porque es una comprobación que solo esta plataforma puede hacer:
**verificar que la firma no cambió de forma incompatible** es una puerta de integración continua que
detecta una rotura de interfaz binaria **antes de desplegar**.

En otros ecosistemas eso requiere herramientas específicas —`abi-compliance-checker` en C++, `japicmp`
en Java— y aquí es una propiedad del objeto.

Y hay un detalle práctico del ejecutador autoalojado que merece la advertencia, porque es un problema
real de seguridad (clase 153): **un corredor autoalojado ejecuta el código de cualquier cambio
propuesto**.

En un repositorio público, eso significa que **cualquiera puede ejecutar código arbitrario dentro del
centro de datos** enviando una propuesta de cambio.

La configuración correcta es conocida y hay que aplicarla: **los ejecutadores autoalojados solo para
repositorios privados, o con aprobación manual obligatoria de las propuestas externas** — y con un
usuario del sistema con los permisos mínimos.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 civerde: procedure options(main);

    declare linea  char(200) varying;
    declare i      fixed binary(31);
    declare verde  bit(1) initial('1'b);

    get edit (linea) (a(200));

    do i = 1 to length(linea);
       if substr(linea, i, 1) = '0' then verde = '0'b;
    end;

    if verde then
       put skip list ('ci=verde');
    else
       put skip list ('ci=rojo');

 end civerde;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte el mundo de COBOL en esta página, y aporta la
perspectiva de qué significa la integración continua cuando **la máquina de construcción es un recurso
compartido y facturado**.

En un mainframe, lanzar una compilación no es gratis: **consume unidades de servicio que se cobran al
departamento** (clase 142). Y de ahí una práctica que en el mundo de los corredores efímeros suena
extraña: **la compilación se planifica**.

```jcl
//CIDIARIO JOB CLASS=C,MSGCLASS=X,NOTIFY=&SYSUID
//*  CLASS=C: cola de baja prioridad, se ejecuta cuando hay hueco
```

**Las clases de trabajo y las colas de prioridad** son un mecanismo del sistema para repartir una
máquina cara entre trabajos de distinta urgencia, y son la respuesta de esta plataforma a la primera
regla del cierre: **no "que sea rápido", sino "que no estorbe a lo que importa"**.

Es un enfoque distinto y merece pensarse, porque el problema vuelve a aparecer hoy con otro nombre: **el
coste de la integración continua en la nube**. Un proyecto grande puede gastar más en corredores que en
servidores, y la respuesta —priorizar, cachear, no ejecutar todo en cada cambio— es la misma.

Y la parte moderna, que conecta el mainframe con el flujo actual:

| Pieza | Qué aporta |
|---|---|
| **Zowe CLI** | `zowe jobs submit` desde cualquier corredor: lanzar y esperar |
| **z/OSMF** | API REST de gestión: trabajos, ficheros, despliegue |
| **IBM DBB** | construcción con dependencias desde Groovy |
| **IDz / VS Code** | edición y compilación remota |

```bash
zowe jobs submit local-file "compila.jcl" --wait-for-output --rff retcode
```

**Ese comando lanza un trabajo en el mainframe desde un corredor de la nube y devuelve el código de
retorno**, con lo que un `if` normal decide si la construcción pasa.

Es todo lo que hacía falta para conectar los dos mundos, y es de la última década.

Y merece cerrar con la observación que atraviesa esta columna: **la integración continua no es una
herramienta, es una disciplina** —construir a menudo, probar automáticamente y no dejar que lo roto se
acumule— y estos sistemas la practicaban con planificadores de trabajos y listados impresos mucho antes
de que hubiera un tablero web que se pusiera verde.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CIVERDE ; Estado de la integracion -- clase 147
 read linea
 new i, verde
 set verde = 1
 for i = 1:1:$length(linea, " ") do
 . if $piece(linea, " ", i) = "0" set verde = 0
 write "ci=", $select(verde : "verde", 1 : "rojo"), !
 quit
```

**Lo que esta clase enseña en M.** M tiene el problema de esta clase con una vuelta de tuerca que se
deriva de la clase 145: **el código vive en la base de datos, así que "construir" no significa lo mismo**.

No hay compilación separada, no hay enlace y no hay artefacto: **cargar una rutina es escribir un dato**.

Y por eso la integración continua en M consiste en tres cosas distintas:

**Primera, cargar el código en un entorno limpio.** Y "limpio" aquí significa **una base de datos
nueva**, porque el código y los datos viven juntos:

```bash
# YottaDB: crear una base vacía y cargar las rutinas
export ydb_dir=/tmp/ci_$$
mumps -run ^%RI < rutinas.ro       # importar
```

**Segunda, ejecutar las pruebas** (clase 139), con MUnit o con los marcos modernos.

**Y tercera, y es la específica de este mundo: comprobar las sumas de comprobación de rutina** (clase
144), para detectar modificaciones no declaradas.

Y el ecosistema moderno ha cambiado bastante y merece conocerse:

| Pieza | Qué aporta |
|---|---|
| **YottaDB en Docker** | **una base de datos M en un contenedor**: corredores de la nube normales |
| **`ydbtest` / MUnit** | marcos de prueba |
| **InterSystems IRIS + `%UnitTest`** | canalizaciones con contenedores oficiales |
| **VistA en contenedores** (*vista-docker*) | el sistema completo, reproducible |

**La primera fila es el cambio importante de la última década**: **que exista una implementación de M
libre y en contenedor** convirtió a este ecosistema, que era el más cerrado de esta página, en uno que
se puede probar en un corredor público igual que cualquier otro.

Es exactamente lo que a IBM i y a z/OS todavía les falta, y explica por qué esas plataformas dependen de
ejecutadores autoalojados.

Y merece cerrar con una observación sobre la segunda regla del cierre, porque en M es especialmente
delicada: **las pruebas que escriben en globals persistentes se contaminan entre sí**.

```mumps
 set ^||TMP("caso", 1) = valor      ; global TEMPORAL, privada del proceso
```

**El prefijo `^||`** (clase 139) da aislamiento por proceso, y es la forma correcta. Una prueba que use
una global normal **deja rastro para la siguiente**, y el resultado es el fallo intermitente clásico:
**pasa sola y falla en el conjunto**, o al revés.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea verde |

linea := stdin nextLine trimBoth.
verde := (linea substrings: ' ') noneSatisfy: [ :t | t = '0' ].

Transcript show: 'ci=', (verde ifTrue: [ 'verde' ] ifFalse: [ 'rojo' ]); cr.
```

**Lo que esta clase enseña en Smalltalk.** `noneSatisfy:` dice literalmente lo que se quiere comprobar,
y es un ejemplo de la convención de la clase 146: **el selector se lee como la frase**.

Y sobre integración continua, Smalltalk tiene la misma peculiaridad que Lisp en esta página, agravada:
**el artefacto es una imagen** (clase 144), así que **la canalización tiene que construirla desde cero**.

```bash
# Pharo: descargar imagen base + cargar el proyecto + probar
curl -L https://get.pharo.org/64/110+vm | bash
./pharo Pharo.image eval --save "
    Metacello new
        baseline: 'MiProyecto';
        repository: 'tonel://./src';
        load."
./pharo Pharo.image test --junit-xml-output "MiProyecto.*"
```

**`--junit-xml-output` genera el formato XML de JUnit**, que cualquier sistema de integración continua
sabe leer — y es un buen ejemplo de lo que la clase 145 concluía: **el ecosistema minoritario se adapta
al formato del mayoritario para poder participar**.

Y hay una capacidad de esta canalización que es propia de Smalltalk y merece destacarse: **el análisis
estático corre sobre el sistema vivo**.

```smalltalk
"En la imagen recién construida, con TODO el código cargado:"
(RBCompositeLintRule allRules) runOnEnvironment: MiProyecto asRBEnvironment.
"y también:"
SystemNavigation default allUnsentMessages.      "métodos que nadie llama"
SystemNavigation default allUnimplementedCalls.   "llamadas a métodos que no existen"
```

**`allUnimplementedCalls` merece la explicación**, porque hace en Smalltalk lo que la clase 137 decía que
un lenguaje dinámico no puede hacer: **encuentra envíos de mensajes que ninguna clase implementa**.

No es una comprobación completa —un selector construido en marcha con `perform:` se le escapa— pero
caza la inmensa mayoría de los errores de nombre, que son los que un lenguaje sin tipos estáticos no
detecta hasta ejecutar.

**Y `allUnsentMessages` da la lista de código muerto**, que la clase 154 retomará.

Y merece cerrar con la observación general: **la integración continua de Smalltalk es más lenta de
arrancar** —hay que construir una imagen entera— **y más rica una vez arrancada**, porque el sistema
cargado puede responder preguntas sobre sí mismo que en otros lenguajes requieren herramientas externas
que reimplementan el análisis del lenguaje.

Es, una vez más, el compromiso que la Parte 8 mostró en cada clase.

---

## Y de vuelta a la clase

Lo transferible: **la integración continua no encuentra fallos, encuentra el momento en que se
introdujeron** — y eso es lo valioso, porque un fallo localizado en un cambio de veinte líneas se
arregla en minutos y el mismo fallo descubierto tres meses después cuesta días. De ahí las dos reglas
que atraviesan la página: **que sea rápida**, porque una comprobación que tarda una hora se ignora; y
**que sea fiable**, porque una prueba que falla a veces enseña al equipo a ignorar el rojo, y a partir
de ahí la integración continua ya no protege de nada.

⏮️ [Volver a la clase 147](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
