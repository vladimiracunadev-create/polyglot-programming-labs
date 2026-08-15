# -*- coding: utf-8 -*-
"""Parte 9, lote C — clases 147 a 150. Ver `vivos_parte9.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 147 — Integración continua multi-lenguaje
# ---------------------------------------------------------------------------
SPECS["147"] = dict(
    gancho="""
Una línea de ceros y unos: si todos son uno, la integración está verde. Es el resumen exacto de lo que
hace una integración continua, y esta clase existe porque **el "todos" es la parte difícil cuando hay
doce lenguajes**. Y aquí hay un dato que cambia la historia habitual: **CPAN Testers lleva desde 1998
compilando y probando cada versión publicada en cientos de combinaciones de sistema y compilador** — es
integración continua distribuida, y es anterior al término.
""",
    porque="""
Aquí el concepto es la **verificación automática y continua**, y estos lenguajes lo enseñan porque
tienen los casos más incómodos. **Fortran necesita el clúster para probarse de verdad.** **RPG y COBOL
necesitan una máquina que no está en la nube.** **C++ tiene una explosión combinatoria de compiladores,
versiones y opciones.** **Y Ada tiene que certificar la propia cadena de herramientas.**

Y aparece la tensión que decide si una integración continua sirve: **entre lo rápido que se ejecuta y
lo mucho que comprueba**. Cada lenguaje de esta página la resuelve en un punto distinto.
""",
    cierre="""
Lo transferible: **la integración continua no encuentra fallos, encuentra el momento en que se
introdujeron** — y eso es lo valioso, porque un fallo localizado en un cambio de veinte líneas se
arregla en minutos y el mismo fallo descubierto tres meses después cuesta días. De ahí las dos reglas
que atraviesan la página: **que sea rápida**, porque una comprobación que tarda una hora se ignora; y
**que sea fiable**, porque una prueba que falla a veces enseña al equipo a ignorar el rojo, y a partir
de ahí la integración continua ya no protege de nada.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let ((linea (read-line))
      (verde t))
  (loop for c across linea
        do (when (char= c #\\0) (setf verde nil)))
  (format t "ci=~A~%" (if verde "verde" "rojo")))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene una particularidad en integración continua que
se deriva de la Parte 8 y que merece explicarse: **hay que forzar la construcción desde cero**.

El flujo normal de desarrollo en Lisp es incremental sobre una imagen viva (clase 124), y eso significa
que **el estado de la imagen puede contener cosas que no están en los ficheros** (clase 145).

De ahí que la canalización empiece siempre igual:

```bash
sbcl --non-interactive \\
     --eval '(asdf:load-system "mi-proyecto" :force t)' \\
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
"""),
        "tcl": ("""
gets stdin linea

set verde 1
foreach v [split [string trim $linea]] {
    if {$v eq "0"} { set verde 0 }
}

puts "ci=[expr {$verde ? {verde} : {rojo}}]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl tiene con esta clase una relación que merece contarse, porque
**es el lenguaje con el que se automatizó buena parte de la industria antes de que existieran las
herramientas actuales**.

Y la pieza clave tiene nombre: **Expect**, escrito por Don Libes en 1990.

```tcl
package require Expect

spawn ssh servidor
expect "password:"
send "$::env(CLAVE)\\r"
expect "$ "
send "make test\\r"
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my $verde = !grep { $_ eq '0' } split ' ', $linea;

print "ci=", ($verde ? 'verde' : 'rojo'), "\\n";
""", """
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
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string v;
    bool verde = true;

    while (std::cin >> v)
        if (v == "0") verde = false;

    std::cout << "ci=" << (verde ? "verde" : "rojo") << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
CIVERDE ; Estado de la integracion -- clase 147
 read linea
 new i, verde
 set verde = 1
 for i = 1:1:$length(linea, " ") do
 . if $piece(linea, " ", i) = "0" set verde = 0
 write "ci=", $select(verde : "verde", 1 : "rojo"), !
 quit
""", """
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
"""),
        "smalltalk": ("""
| linea verde |

linea := stdin nextLine trimBoth.
verde := (linea substrings: ' ') noneSatisfy: [ :t | t = '0' ].

Transcript show: 'ci=', (verde ifTrue: [ 'verde' ] ifFalse: [ 'rojo' ]); cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 148 — Entrega y despliegue
# ---------------------------------------------------------------------------
SPECS["148"] = dict(
    gancho="""
Anunciar una versión desplegada: `desplegado=v1.2.3`. El programa es un eco; lo que esta clase compara es
**lo que ocurre justo antes y justo después de esa línea**. Y aquí están los dos extremos absolutos de la
ingeniería: **CICS sustituye un programa en un sistema con miles de usuarios conectados, sin cortar
nada, y lo hace desde 1969**; y **una sonda espacial se actualiza a cientos de millones de kilómetros,
sin posibilidad de volver atrás si sale mal**.
""",
    porque="""
Aquí el concepto es la **puesta en producción y la reversión**, y estos lenguajes lo enseñan porque
**operan sistemas que no pueden pararse**: bancos, hospitales, fábricas, aviones y satélites. Así que
resolvieron hace décadas lo que hoy se llama despliegue sin cortes, y con mecanismos que siguen siendo
más simples que los actuales: **cambiar el orden de una lista de bibliotecas**, **copiar un miembro**,
**escribir una rutina en la base de datos**.

Y aparece la pregunta que ordena la página: **¿cuánto cuesta deshacer?** Porque un despliegue sin
reversión no es un despliegue: es una apuesta.
""",
    cierre="""
Lo transferible: **el valor de un despliegue se mide por lo rápido que se deshace**, no por lo elegante
que sea. De ahí las tres propiedades que aparecen en toda esta página: **la versión anterior sigue
existiendo** —no se sobrescribe, se deja al lado—; **el cambio de una a otra es una operación pequeña y
atómica**; y **hay una forma de comprobar que la nueva funciona antes de dirigirle todo el tráfico**. Y
la cuarta, que casi nadie planea: **los datos**. El código vuelve atrás en segundos; una migración de
esquema, no — y por eso los cambios de datos se hacen compatibles en las dos direcciones antes de tocar
el código.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. DESPLIEG.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).

PROCEDURE DIVISION.
    ACCEPT LINEA
    DISPLAY "desplegado=v" FUNCTION TRIM(LINEA)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Aquí está el primer extremo del gancho, y merece desarrollarse
porque es una capacidad que sorprende: **CICS puede sustituir un programa mientras hay miles de usuarios
usándolo**.

```text
CEMT SET PROGRAM(MIPGM) NEWCOPY
CEMT SET PROGRAM(MIPGM) PHASEIN
```

**`NEWCOPY` carga la versión nueva; las transacciones que empiecen a partir de ahí usan la nueva.**

**Y `PHASEIN` va más lejos**: carga la nueva **mientras las transacciones que ya están en curso terminan
con la vieja**. Las dos versiones conviven en memoria hasta que la última transacción antigua acaba.

**Eso es un despliegue sin cortes, con drenaje de conexiones, en un solo comando** — y es de una época en
la que "sin cortes" no era un término de marketing sino el requisito de un sistema de cajeros.

Y el despliegue de lotes es igual de simple, y ya apareció en la clase 144:

```jcl
//COPIA EXEC PGM=IEBCOPY        <-- copiar el miembro de QA a PROD
```

**Y la reversión es copiar el anterior de vuelta**, que se conserva automáticamente en los grupos de
datos generacionales.

Y hay una técnica del mundo mainframe que merece conocerse porque es la respuesta a la cuarta propiedad
del cierre —**los datos**— y tiene nombre: **la ejecución en paralelo previa** (clase 140).

```text
Semanas 1-8:  el sistema nuevo se ejecuta EN PARALELO, sin efectos, comparando salidas
Semana 9:     el nuevo pasa a producción; el viejo sigue ejecutándose, ahora sin efectos
Semana 12:    se apaga el viejo
```

**Durante semanas, los dos sistemas funcionan y solo uno tiene efectos.** La vuelta atrás es cambiar
cuál de los dos escribe.

Es lo mismo que hoy se llama despliegue en oscuridad y lanzamiento por bandera, y su motivo es idéntico:
**separar el despliegue del código de la activación del comportamiento**.

Y merece cerrar con la propiedad organizativa, porque es la parte que las herramientas no dan: en estos
sistemas **hay una ventana de cambio autorizada, un plan de vuelta atrás escrito, y un responsable de
decidir**.

No es burocracia gratuita: es la constatación de que **un despliegue es una operación de riesgo**, y de
que el momento de pensar cómo se deshace **no es cuando ya ha salido mal**.
"""),
        "fortran": ("""
program despliegue
   implicit none
   character(len=40) :: linea

   read(*, '(A)') linea

   write(*, '(A)') 'desplegado=v' // trim(adjustl(linea))
end program despliegue
""", """
**Lo que esta clase enseña en Fortran.** El despliegue en cálculo científico tiene una forma propia que
merece explicarse, porque casi nadie fuera del dominio la conoce: **los módulos de entorno**.

```bash
module avail                          # qué versiones hay instaladas
module load fortran/gcc-13.2 openmpi/4.1.5 hdf5/1.14
module swap openmpi/4.1.5 openmpi/5.0.1     # cambiar de versión
module list
```

**En un clúster hay decenas de versiones de cada compilador y de cada biblioteca instaladas a la vez**, y
`module load` **ajusta las variables de entorno** —`PATH`, `LD_LIBRARY_PATH`, `MANPATH`— para elegir
una combinación.

Y eso es exactamente el modelo de despliegue que esta clase describe:

- **Todas las versiones coexisten**, no se sobrescriben.
- **Cambiar de una a otra es una operación instantánea.**
- **Y la vuelta atrás es `module swap`.**

Es lo mismo que la lista de bibliotecas de IBM i y la concatenación de `STEPLIB` de z/OS en esta página,
resuelto con variables de entorno.

Y el despliegue del programa propio sigue el mismo patrón:

```bash
/opt/miapp/2.3.1/bin/simular       # instalación versionada
/opt/miapp/actual -> 2.3.1          # un ENLACE SIMBÓLICO
```

**Cambiar el enlace simbólico es el despliegue, y devolverlo es la reversión** — la técnica más simple y
más eficaz de esta página, y la misma que usan Capistrano, los despliegues de Nix y media industria.

Y hay una consideración propia del dominio que merece señalarse y que conecta con la clase 140: **la
reproducibilidad de los resultados publicados**.

Un artículo científico cita resultados producidos con una versión concreta del código, del compilador y
de las bibliotecas. **Si esa combinación deja de estar disponible, el resultado no se puede
reproducir.**

De ahí que los centros de cálculo **conserven versiones antiguas durante años** y que la comunidad haya
adoptado los contenedores —Singularity/Apptainer— para congelar el entorno completo junto con el
artículo.

Es la cuarta propiedad del cierre aplicada a un caso peculiar: **aquí lo que hay que poder revertir no
es el servicio, es la capacidad de reproducir un resultado de hace cinco años**.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;

procedure Despliegue is
   Linea  : String (1 .. 40);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   Put_Line ("desplegado=v" & Linea (1 .. Ultimo));
end Despliegue;
""", """
**Lo que esta clase enseña en Ada.** Aquí está el segundo extremo del gancho, y es el caso límite de esta
clase entera: **desplegar software donde no se puede volver atrás y no se puede tocar la máquina**.

La NASA lo ha hecho muchas veces, y merece conocer cómo:

**La Voyager**, lanzada en 1977 y todavía funcionando, **ha recibido actualizaciones de software a más
de veinte mil millones de kilómetros**. En 2023, tras un fallo de memoria en el ordenador de vuelo, el
equipo **reubicó el código afectado a otra zona de memoria** — enviando la actualización con **22 horas
de retardo en cada sentido**.

**El *Mars Reconnaissance Orbiter* y los róveres** funcionan con software escrito en C y Ada, y reciben
actualizaciones completas de versión.

Y las propiedades que hacen posible ese despliegue son exactamente las tres del cierre de esta clase,
llevadas al extremo:

**Uno, la versión anterior sigue existiendo**: hay **memoria redundante con la imagen antigua**, y un
temporizador de vigilancia que **restaura la anterior si la nueva no confirma que está viva** en un
plazo.

**Dos, el cambio es atómico**: la imagen nueva se transmite entera, **se verifica con una suma de
comprobación**, y solo entonces se conmuta.

**Y tres, hay validación previa**: existe **un gemelo del vehículo en tierra** —hardware idéntico— donde
la actualización se ensaya primero, tantas veces como haga falta.

Ese último punto merece pensarse, porque es la versión más honesta del entorno de preproducción: **una
copia física exacta del sistema de producción**, mantenida durante décadas.

Y las características del lenguaje que sostienen esto son las de la Parte 8:

```ada
pragma Restrictions (No_Allocators);       --  sin montón: memoria predecible
pragma Restrictions (No_Recursion);         --  pila acotada
pragma Profile (Ravenscar);                  --  concurrencia analizable (clase 146)
```

**Sin reserva dinámica y sin recursión, el consumo de memoria se conoce en tiempo de compilación** — y
eso es lo que permite garantizar que la versión nueva cabe y no agotará nada.

Y hay una técnica de Ada específica para esta clase que merece nombrarse: **el parcheo en caliente con
`pragma Linker_Section`**, que permite colocar código en direcciones concretas para poder sustituir
bloques individuales en lugar de la imagen entera — porque **el ancho de banda hacia Marte se mide en
kilobits por segundo**.
"""),
        "pascal": ("""
program Despliegue;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;

begin
  ReadLn(Linea);
  WriteLn('desplegado=v', Trim(Linea));
end.
""", """
**Lo que esta clase enseña en Pascal.** El ecosistema Pascal vive el problema del despliegue en su forma
más incómoda, y merece nombrarla porque casi todo lo demás de esta página la evita: **el software se
instala en máquinas que no controlas**.

Un servidor se despliega y se revierte en segundos. **Una aplicación de escritorio instalada en 4.000
puestos, no.**

Y de ahí las técnicas que el mundo Delphi desarrolló, y que hoy se reconocen en cualquier aplicación de
escritorio:

**El instalador con desinstalación y reparación:**

```text
Inno Setup, InstallShield, NSIS
  - detectan la versión instalada
  - hacen copia de seguridad de lo que sustituyen
  - registran para poder desinstalar
  - y ofrecen "reparar" reinstalando lo que falte
```

**La actualización automática:**

```pascal
{ el patrón clásico: el programa comprueba, descarga y se relanza }
if HayVersionNueva(URLManifiesto) then
begin
  DescargarA(TempDir + 'actualizador.exe');
  ExecuteProcess(TempDir + 'actualizador.exe', ['/silent', '/pid=' + IntToStr(GetProcessID)]);
  Halt;      { el actualizador espera a que muera, sustituye y relanza }
end;
```

**El detalle de que un programa no puede sustituirse a sí mismo mientras se ejecuta** es lo que obliga a
ese baile del proceso auxiliar, y es un problema real de esta clase en cualquier sistema operativo que
bloquee los ejecutables en uso.

**Y el despliegue por copia**, que Pascal permite porque su binario es autocontenido (clase 144):

```text
xcopy deployment: copiar el .exe y funciona
```

**Sin instalador, sin registro y sin dependencias**, que es lo que hizo tan popular a Delphi para
herramientas internas.

Y merece cerrar con la técnica que resuelve el problema de fondo y que conecta con la clase 142: **la
telemetría de fallos**.

Cuando no se puede revertir a voluntad, **lo que hace falta es enterarse rápido**. Y por eso el
ecosistema desarrolló madExcept y EurekaLog (clases 141 y 142): **el informe automático de excepción
llega al desarrollador el mismo día del despliegue**, con la pila y el contexto.

Es la aplicación de la tercera propiedad del cierre —**comprobar antes de dirigir todo el tráfico**— a un
mundo donde el tráfico no se dirige: **se despliega por fases, a un grupo pequeño primero, y se mira la
telemetría antes de continuar**.
"""),
        "lisp": ("""
(let ((linea (string-trim '(#\\Space #\\Return) (read-line))))
  (format t "desplegado=v~A~%" linea))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene la forma de despliegue más radical de esta página,
y viene directamente del modelo de la Parte 8: **se puede cambiar el código de un sistema en producción
sin pararlo, función a función**.

```lisp
;; conectado por red a un servidor EN PRODUCCIÓN (clase 138)
(swank:create-server :port 4005)

;; y desde el editor, en la máquina de desarrollo:
(defun calcular-descuento (pedido)
  ...)                             ; C-c C-c: recompila ESA función, en el servidor vivo
```

**La siguiente llamada usa la definición nueva; las que estén en curso terminan con la vieja** (clase
124).

Es exactamente lo que `PHASEIN` de CICS hace en esta página, con una diferencia enorme: **la granularidad
es la función, no el programa**, y **no hace falta ninguna infraestructura**.

Y merece decir con claridad las dos caras de esto:

**A favor**, resuelve el caso más difícil de la depuración: **un fallo que solo ocurre en producción,
con datos que no se pueden reproducir**. Se puede instrumentar la función, mirar, corregir y seguir, sin
perder el estado.

**En contra**, y hay que decirlo igual de claro: **la imagen en producción deja de corresponderse con
ningún commit**. Nadie sabe qué código está ejecutándose. Y si el proceso se reinicia, **el arreglo
desaparece**.

De ahí la disciplina que el ecosistema recomienda y que es la lección de esta explicación: **la
redefinición en caliente es para diagnosticar, no para desplegar**. El arreglo se lleva al repositorio,
pasa la integración continua y se despliega como cualquier otro; lo que se hizo en caliente fue ganar
tiempo.

Y el despliegue normal de Lisp usa lo de la clase 144:

```lisp
(sb-ext:save-lisp-and-die "miapp" :executable t :toplevel #'main)
```

**Una imagen ejecutable, versionada, desplegada por copia**, con el patrón de enlace simbólico de
Fortran en esta página.

Y hay una capacidad que merece cerrar, porque es el despliegue de estado y casi ningún lenguaje lo
tiene: **la imagen se puede guardar con las cachés ya calientes**.

```lisp
(precargar-tablas)                 ; leer la base, construir índices, calentar cachés
(sb-ext:save-lisp-and-die "miapp" :executable t)
```

**El proceso desplegado arranca con todo eso ya hecho**, en milisegundos. Es la razón por la que un
servicio Lisp puede tener un arranque instantáneo con estructuras que tardarían minutos en construirse.
"""),
        "tcl": ("""
gets stdin linea

puts "desplegado=v[string trim $linea]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl tiene, gracias a los Starkits de la clase 144, el despliegue más
simple de esta página: **la aplicación es un fichero**.

```bash
scp miapp.kit servidor:/opt/miapp/miapp-1.2.3.kit
ssh servidor "ln -sfn /opt/miapp/miapp-1.2.3.kit /opt/miapp/actual && systemctl restart miapp"
```

**Y la reversión es reapuntar el enlace simbólico**, que es la primera propiedad del cierre en su forma
más pura: **la versión anterior sigue ahí, intacta**.

Y Tcl aporta a esta clase dos capacidades propias que merecen conocerse.

**La primera es la actualización en caliente por `source`**, hermana de la de Lisp en esta página:

```tcl
# un servidor Tcl puede recargar un fichero de procedimientos sin reiniciar
proc recargar {} {
    source /opt/miapp/handlers.tcl      ;# las proc se REDEFINEN
    return "recargado"
}
```

**`proc` redefine si ya existe**, así que recargar un fichero actualiza los procedimientos que define.
Es el mismo mecanismo que hace funcionar la recarga de módulos de muchos servidores modernos.

Y la advertencia que va con ello es la misma que en Lisp: **sirve para el código, no para el estado**. Si
una variable global cambió de forma, recargar los procedimientos deja el sistema en un estado
incoherente.

**Y la segunda es la que conecta con la clase 147: Expect para el despliegue.**

```tcl
package require Expect
spawn ssh operador@router
expect "# "
send "configure terminal\\r"
...
```

**Automatizar el despliegue en equipos que no tienen API** sigue siendo un problema real —routers,
conmutadores, controladores industriales, sistemas antiguos con menús de texto— y Expect sigue siendo la
respuesta.

Y merece cerrar con una observación práctica sobre la tercera propiedad del cierre: **el archivo único
hace trivial la validación previa**.

```bash
# comprobar que el artefacto arranca ANTES de cambiar el enlace
/opt/miapp/miapp-1.2.3.kit --autocomprobar || exit 1
ln -sfn ...
```

**Ejecutar la versión nueva en modo de comprobación antes de dirigirle tráfico** es la mitad barata de
un despliegue canario, y no requiere nada más que un artefacto que se pueda ejecutar dos veces.
"""),
        "perl": ("""
use strict;
use warnings;

my $version = <STDIN>;
chomp $version;

print "desplegado=v$version\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl fue durante veinte años **el lenguaje con el que se
desplegaba**, y de ahí salieron patrones que hoy están en todas las herramientas.

El más importante es **el despliegue por directorio versionado con enlace simbólico**, que popularizó
Capistrano —escrito en Ruby, pero heredero directo de los guiones de despliegue en Perl de los años
noventa—:

```text
/srv/miapp/
  releases/
    2024-03-15-093012/     <-- cada despliegue, en su directorio
    2024-03-14-171040/
    2024-03-12-104533/
  shared/
    log/  uploads/  config/    <-- lo que sobrevive entre versiones
  current -> releases/2024-03-15-093012
```

Y las propiedades que lo hacen bueno son literalmente las tres del cierre de esta clase:

- **Las versiones anteriores siguen ahí** —normalmente las cinco últimas—.
- **El cambio es un `ln -sfn`, que es atómico** en un sistema POSIX.
- **Y se puede comprobar el directorio nuevo antes de conmutar.**

**La atomicidad del enlace simbólico merece el detalle**, porque es la razón técnica de que el patrón
funcione: `ln -sfn` sobre un enlace existente hace **rename**, que es atómico. **No hay un instante en
que `current` no exista**, así que ningún proceso ve un estado intermedio.

Y el despliegue de dependencias, con lo de la clase 143:

```bash
carton install --deployment      # exactamente lo del cpanfile.snapshot, nada más
```

**`--deployment` se niega a resolver nada**: instala las versiones exactas del fichero de bloqueo o
falla. Es lo que hay que usar en producción, y es la diferencia entre un despliegue reproducible y uno
que depende de qué había en el índice ese día.

Y Perl aporta a esta clase la advertencia sobre la cuarta propiedad del cierre —**los datos**— que es la
que más despliegues estropea:

```perl
# ✗ MAL: el código nuevo necesita la columna nueva
#    → durante el despliegue, los procesos viejos y nuevos conviven y unos fallan
# ✓ BIEN: en tres pasos
#   1. añadir la columna, NULL permitido; desplegar código que la escribe pero no la exige
#   2. rellenar los datos históricos
#   3. desplegar código que la exige, y solo entonces ponerla NOT NULL
```

**Ese patrón —expandir, migrar, contraer— es la respuesta general**, y su motivo es el que casi nadie
anticipa: **durante un despliegue gradual, las dos versiones del código funcionan a la vez sobre la
misma base de datos**.

Cualquier cambio de esquema que no sea compatible en las dos direcciones **hace imposible la vuelta
atrás**, que es exactamente lo que esta clase quiere evitar.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string version;
    if (!std::getline(std::cin, version)) return 1;

    std::cout << "desplegado=v" << version << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ está en el lado bueno del despliegue por una razón simple: **un
binario enlazado estáticamente es un fichero que se copia y funciona**.

Y en el lado malo por otra igual de simple: **cuando no está enlazado estáticamente, depende de
bibliotecas del sistema con reglas de compatibilidad propias** (clase 143).

```bash
ldd ./miapp
        libstdc++.so.6 => /usr/lib/libstdc++.so.6
        libc.so.6 => /usr/lib/libc.so.6 (GLIBC_2.34)
```

**Ese `GLIBC_2.34` es la trampa clásica**: un binario compilado en un sistema moderno **no arranca en uno
más antiguo**, con un mensaje desconcertante:

```text
./miapp: /lib/libc.so.6: version `GLIBC_2.34' not found
```

Y las soluciones, todas usadas en la práctica:

| Estrategia | Coste |
|---|---|
| **Compilar en el sistema más antiguo que se soporte** | necesita esa máquina o contenedor |
| **Enlace estático con musl** | binario grande, sin `dlopen` ni NSS |
| **AppImage / Flatpak** | empaqueta las bibliotecas |
| **Contenedores** | la solución dominante hoy |
| **`-static-libstdc++ -static-libgcc`** | evita el problema de C++ y deja el de libc |

Y C++ tiene una capacidad de despliegue propia que merece explicarse porque es de las pocas formas de
actualizar sin reiniciar en un lenguaje compilado: **la carga dinámica de complementos**.

```cpp
void* h = dlopen("/opt/miapp/plugins/reglas-v2.so", RTLD_NOW);
auto crear = reinterpret_cast<Reglas*(*)()>(dlsym(h, "crear_reglas"));
```

**Se puede cargar una versión nueva de un módulo mientras el proceso corre**, y descargar la vieja
cuando nadie la use.

Y las trampas hay que decirlas porque son severas: **los objetos creados por la versión vieja tienen
punteros a tablas de métodos virtuales de la biblioteca vieja**, así que **descargarla mientras existan
esos objetos es una caída segura**.

De ahí que el patrón exija **contar referencias y descargar solo cuando llega a cero**, o directamente
**no descargar nunca** — que es lo que hacen la mayoría de los sistemas en producción.

Y merece cerrar con lo que la industria hace hoy y que aplica las tres propiedades del cierre: **el
despliegue azul-verde y el canario**.

```text
azul-verde:  dos entornos completos; el balanceador apunta a uno; conmutar es instantáneo
canario:     el 1 % del tráfico a la versión nueva; se miran las métricas; se amplía o se revierte
```

**El canario es la tercera propiedad del cierre en su forma completa**: no "comprobar antes de dirigir el
tráfico", sino **dirigir un poco de tráfico real y medir**, porque hay fallos que solo aparecen con
carga y datos de verdad.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi DESPLIEG;
  version char(40) const;
end-pi;

dsply ('desplegado=v' + %trim(version));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i tiene, con diferencia, **el mecanismo de despliegue y reversión
más simple de esta página**, y ya apareció en las clases 139 y 140: **la lista de bibliotecas**.

```text
CHGLIBL LIBL(NUEVO PROD COMUN)      <-- desplegar: NUEVO tiene prioridad
CHGLIBL LIBL(PROD COMUN)             <-- revertir: quitar una entrada
```

**El sistema busca cada objeto recorriendo la lista en orden**, así que **poner una biblioteca delante
sustituye programas, tablas y todo lo demás, sin tocar ningún objeto**.

Y las propiedades que eso da son exactamente las del cierre de esta clase:

- **La versión anterior sigue existiendo**, intacta, en su biblioteca.
- **El cambio es un comando y es instantáneo.**
- **Y se puede probar por usuario**: la lista de bibliotecas **es propia de cada trabajo**.

**Esa última es la que merece destacarse**, porque es un despliegue canario sin infraestructura:

```text
Para el usuario de pruebas:   LIBL(NUEVO PROD COMUN)
Para todos los demás:          LIBL(PROD COMUN)
```

**Diez usuarios pueden estar usando la versión nueva mientras mil siguen con la vieja**, en la misma
máquina, sin balanceador, sin contenedores y sin coordinación.

Y la plataforma añade la capacidad que resuelve el problema del despliegue en caliente:

```text
El objeto programa puede SUSTITUIRSE mientras hay trabajos ejecutándolo:
  - los trabajos que ya lo activaron siguen con la versión activada
  - los nuevos usan la nueva
```

Es el `PHASEIN` de CICS de esta página, con la misma semántica.

Y sobre la cuarta propiedad del cierre —**los datos**—, IBM i tiene un mecanismo que merece conocerse
porque casi ningún sistema lo tiene: **la salvaguarda con el diario**.

```text
STRJRNPF  ...          <-- el diario registra cada cambio (clase 140)
APYJRNCHG / RMVJRNCHG   <-- APLICAR o RETIRAR cambios del diario
```

**`RMVJRNCHG` deshace los cambios de datos hasta un instante concreto.** Así que **la vuelta atrás de los
datos existe como operación del sistema**, no como restauración de una copia de seguridad de hace ocho
horas.

Es la respuesta más completa de esta página a la parte del despliegue que casi nadie planifica, y explica
por qué en esta plataforma la pregunta "¿y si sale mal?" tiene una respuesta corta.
"""),
        "pli": ("""
 despliegue: procedure options(main);

    declare linea char(40) varying;

    get edit (linea) (a(40));

    put skip list ('desplegado=v' || trim(linea));

 end despliegue;
""", """
**Lo que esta clase enseña en PL/I.** PL/I comparte el mundo de COBOL en esta página y aporta un
mecanismo del lenguaje que es directamente el tema de la clase: **`FETCH` y `RELEASE`** (clase 143).

```pli
 fetch reglas;              /* cargar el módulo AHORA, por nombre */
 call reglas(datos);
 release reglas;             /* y descargarlo */
```

**Un módulo se carga por nombre en tiempo de ejecución**, así que **desplegar una versión nueva es
sustituir el módulo en la biblioteca**: la siguiente ejecución que haga `FETCH` carga la nueva.

Es la carga dinámica de complementos de C++ en esta página, expresada como sentencia del lenguaje y sin
la trampa de las tablas de métodos, porque PL/I no tiene objetos con tablas virtuales.

Y el despliegue por concatenación es el mecanismo estructural, y es el mismo patrón que la lista de
bibliotecas de IBM i:

```jcl
//STEPLIB  DD DSN=PRUEBAS.LOADLIB,DISP=SHR     <-- primero aquí
//         DD DSN=PROD.LOADLIB,DISP=SHR         <-- y si no, aquí
```

**Añadir una línea al JCL despliega; quitarla revierte.** Y como el JCL es del trabajo, **se puede
desplegar a un trabajo concreto** — el canario por trabajo, igual que RPG en esta página lo hace por
usuario.

Y merece dedicar el cierre a la propiedad organizativa que este mundo aporta y que la industria moderna
está redescubriendo: **la ventana de cambio**.

```text
Ventana autorizada: domingo 02:00-05:00
  - plan de despliegue escrito y aprobado
  - plan de VUELTA ATRÁS escrito, con el tiempo estimado
  - criterio de decisión: qué medida obliga a revertir, y quién decide
  - y un ensayo previo en el entorno de preproducción
```

**El "criterio de decisión" es la parte que más se echa en falta hoy**: decidir **de antemano** qué señal
obliga a revertir, y **quién tiene la autoridad para hacerlo sin consultar**.

Sin eso, lo que ocurre en un despliegue que va mal es lo conocido: **se pasan cuarenta minutos
investigando la causa mientras el servicio está degradado**, cuando la acción correcta era revertir en
el minuto dos y investigar después.

Es una lección que no viene de la tecnología sino de operar sistemas donde el minuto de parada tiene
precio, y es tan válida hoy como en 1985.
"""),
        "mumps": ("""
DESPLIEG ; Anuncio de despliegue -- clase 148
 read version
 write "desplegado=v", version, !
 quit
""", """
**Lo que esta clase enseña en M.** M tiene el despliegue más peculiar de esta página, y es la consecuencia
directa de la clase 145: **el código es un dato, así que desplegar es escribir en la base de datos**.

Y eso da propiedades que ningún despliegue de ficheros tiene:

**Primera, es transaccional** (clase 144):

```mumps
 tstart
 ; cargar rutinas nuevas, migrar datos, actualizar definiciones de FileMan
 tcommit
```

**Si algo falla a mitad, `trollback` deshace el despliegue entero** —código y datos a la vez—, que es
justamente la cuarta propiedad del cierre de esta clase resuelta de raíz.

**Segunda, es en caliente por naturaleza.** Sustituir una rutina es una escritura; **los procesos que ya
la tenían cargada siguen con la vieja y los nuevos toman la nueva** — el mismo comportamiento que
`PHASEIN` de CICS y que la sustitución de objetos en IBM i.

**Y tercera, el despliegue va acompañado de sus datos**, porque un parche KIDS (clase 143) incluye las
definiciones de fichero y el código de migración en el mismo paquete.

Y el contexto de este mundo merece decirse, porque explica el nivel de cuidado: **VistA se despliega en
cientos de hospitales que no pueden pararse**. Un fallo en el módulo de farmacia no es una página de
error: es una dosis.

De ahí las prácticas del sistema de parches:

```text
- número de parche secuencial y global, con requisitos previos verificados
- suma de comprobación de cada rutina antes y después (clase 144)
- entorno de pruebas obligatorio antes de producción
- código de instalación previo y posterior, ejecutado en la misma transacción
- y un procedimiento de vuelta atrás documentado, con las rutinas anteriores
```

Y merece cerrar con la advertencia sobre lo que M **no** resuelve, porque es honesta: **la reversión del
código es fácil y la de los datos migrados no siempre lo es**.

Si el parche transformó el formato de un millón de fichas de pacientes, **`trollback` funciona durante
la instalación, pero no tres días después**.

Es exactamente el problema del patrón expandir-migrar-contraer de Perl en esta página, y la respuesta es
la misma: **los cambios de datos se diseñan para ser compatibles con la versión anterior del código**,
y la eliminación de lo viejo se hace en un parche posterior, cuando ya no hay vuelta atrás que temer.
"""),
        "smalltalk": ("""
| version |

version := stdin nextLine trimBoth.

Transcript show: 'desplegado=v', version; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene, junto con Lisp, la capacidad de esta página
que más se aleja del modelo habitual: **el sistema en producción se puede modificar mientras funciona**,
y con más granularidad todavía.

```smalltalk
"Conectado a la imagen en producción:"
Pedido compile: 'calcularTotal
    ^ items inject: 0 into: [ :a :b | a + b precio ]'.
```

**Compilar un método sustituye ese método en el sistema vivo** (clase 124). Las llamadas en curso
terminan con el código viejo; las siguientes usan el nuevo.

Y el despliegue formal usa lo de la clase 144: **la imagen como artefacto**.

```bash
# construir la imagen nueva en la integración continua
./pharo Pharo.image eval "Metacello new baseline: 'MiApp';
    repository: 'github://org/miapp:v1.2.3'; load."
./pharo Pharo.image save miapp-1.2.3

# desplegar: copiar y conmutar
scp miapp-1.2.3.image servidor:/opt/miapp/
ssh servidor "ln -sfn miapp-1.2.3.image actual.image && systemctl restart miapp"
```

Y aquí aparece **el problema específico de esta clase en un sistema con imagen**, y merece explicarse
porque es distinto de todo lo demás de la página: **la imagen contiene estado, no solo código**.

Una imagen desplegada trae **los objetos que existían al guardarla**. Así que:

- **No se puede simplemente sustituir la imagen de producción por la nueva**, porque se perdería el
  estado acumulado —sesiones, cachés, colas—.
- **Y no se puede conservar el estado viejo con el código nuevo** sin más, porque los objetos
  existentes pueden tener la forma antigua.

Y la solución que el ecosistema usa es la que cualquier sistema con estado acaba adoptando: **el estado
importante no vive en la imagen**.

```smalltalk
"El estado va a una base de datos o a un almacén de objetos:"
GemStone, Voyage/MongoDB, o simplemente PostgreSQL
```

**La imagen queda como código puro y se puede sustituir entera**, que es lo que hace posible el
despliegue azul-verde.

Y hay una excepción que merece nombrarse porque es una tecnología notable: **GemStone/S**, un Smalltalk
con **una base de datos de objetos transaccional integrada**, donde **los objetos persisten
automáticamente y las transacciones son del lenguaje**.

Ahí el problema desaparece por diseño: **el estado vive en el repositorio de objetos, compartido entre
todas las máquinas virtuales**, y desplegar código nuevo es actualizar clases en ese repositorio, con
transacción y con vuelta atrás.

Es la respuesta más completa de esta página al problema de desplegar código y datos juntos, y lleva
funcionando en sistemas financieros desde los años noventa.
"""),
    },
)

# ---------------------------------------------------------------------------
# 149 — Diseño y arquitectura comparada
# ---------------------------------------------------------------------------
SPECS["149"] = dict(
    gancho="""
Contar capas: `web api datos` son tres. Es la abstracción más repetida de la industria, y esta clase la
pone frente a las alternativas que estos lenguajes practican. Y hay un dato que conviene tener presente
al hablar de arquitectura: **el patrón Modelo-Vista-Controlador se inventó en Smalltalk-80**, lo
describió Trygve Reenskaug en Xerox PARC en 1979, y **todo lo que hoy se llama arquitectura de
aplicaciones interactivas desciende de ahí**.
""",
    porque="""
Aquí el concepto es la **arquitectura como reparto de responsabilidades**, y estos lenguajes lo enseñan
porque **practican arquitecturas distintas de la de tres capas**, y todas siguen funcionando. **COBOL y
JCL: la canalización de lotes**, donde cada paso es un programa y el acoplamiento es un fichero.
**Fortran: capas numéricas**, con BLAS y LAPACK como ejemplo canónico de biblioteca en niveles. **M:
arquitectura centrada en los datos**, donde el esquema es el sistema. **Y Smalltalk: MVC y objetos**.

Y aparece la pregunta de fondo: **¿qué decide dónde va cada cosa?** Porque toda arquitectura es una
respuesta a esa pregunta, y las respuestas difieren mucho más de lo que el vocabulario común sugiere.
""",
    cierre="""
Lo transferible: **una arquitectura es un conjunto de decisiones difíciles de cambiar, y su valor está
en qué cambios hace fáciles**. De ahí la prueba que conviene aplicar a cualquier propuesta: **nombrar los
tres cambios más probables del próximo año y ver si la estructura los facilita o los estorba**. Y la
segunda regla, que es la que más se incumple: **las capas solo sirven si la dependencia va en un solo
sentido**; en cuanto la capa de datos conoce a la de presentación, hay tres capas en el diagrama y una
sola en la práctica.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CAPAS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  CNT     PIC 9(4) COMP VALUE 0.
01  ENPAL   PIC 9      VALUE 0.
01  ED      PIC -(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            MOVE 0 TO ENPAL
        ELSE
            IF ENPAL = 0
                MOVE 1 TO ENPAL
                ADD 1 TO CNT
            END-IF
        END-IF
    END-PERFORM

    MOVE CNT TO ED
    DISPLAY "capas=" FUNCTION TRIM(ED)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El mundo del lote practica una arquitectura que merece conocerse
porque es excelente y porque la industria la reinventó dos veces: **la canalización de pasos**.

```jcl
//PASO1 EXEC PGM=EXTRAER      <-- lee la base, escribe un fichero
//PASO2 EXEC PGM=SORT           <-- ordena
//PASO3 EXEC PGM=VALIDAR         <-- lee, valida, escribe válidos y rechazos
//PASO4 EXEC PGM=CALCULAR         <-- lee válidos, calcula, escribe resultados
//PASO5 EXEC PGM=INFORMAR          <-- lee resultados, imprime
```

Y sus propiedades son las que hoy se buscan en cualquier sistema de procesamiento de datos:

- **Cada paso es un programa independiente**, con una entrada y una salida.
- **El acoplamiento es un fichero con formato declarado**, no una llamada.
- **Cada paso se puede reejecutar solo**, si falla, sin repetir los anteriores.
- **Se puede insertar un paso nuevo en medio** sin tocar los demás.
- **Y cada paso se prueba dando un fichero de entrada y comparando la salida** (clase 139).

**Eso es la arquitectura de tuberías y filtros**, y es la misma que Unix adoptó con `|`, la que
MapReduce popularizó, y la que hoy tienen Airflow, Spark y cualquier orquestador de datos.

Y merece señalar la diferencia con la arquitectura de tres capas que el gancho nombra: **aquí no hay
capas, hay etapas**. El eje no es "presentación / lógica / datos" sino "paso 1 / paso 2 / paso 3".

Es una arquitectura orientada al flujo, no a la responsabilidad, y para procesamiento por lotes es
mejor.

Y el mismo mundo tiene la otra arquitectura, la transaccional, que sí es en capas:

```text
Terminal 3270  →  CICS (control de transacción)  →  Programa COBOL  →  DB2
                        ↑                              ↑
                  presentación (BMS)            lógica de negocio
```

Y el problema arquitectónico clásico de estos sistemas es exactamente el de la segunda regla del cierre:
**los programas COBOL de los años ochenta mezclaban las tres capas**, con `EXEC CICS SEND MAP` —
presentación— y `EXEC SQL` —datos— en el mismo párrafo que el cálculo.

Y de ahí que la modernización de estos sistemas consista, casi siempre, en **separar la lógica de
negocio de la presentación** para poder exponerla como servicio.

Es la misma operación que la clase 150 llamará refactorización, hecha a escala de millones de líneas, y
es la razón por la que "extraer la lógica a un programa llamable" es la tarea número uno de cualquier
proyecto de modernización de COBOL.
"""),
        "fortran": ("""
program capas
   implicit none
   character(len=200) :: linea
   integer :: i, cnt
   logical :: en_palabra

   read(*, '(A)') linea
   cnt = 0
   en_palabra = .false.

   do i = 1, len_trim(linea)
      if (linea(i:i) == ' ') then
         en_palabra = .false.
      else if (.not. en_palabra) then
         en_palabra = .true.
         cnt = cnt + 1
      end if
   end do

   write(*, '(A,I0)') 'capas=', cnt
end program capas
""", """
**Lo que esta clase enseña en Fortran.** El cálculo científico tiene una arquitectura en capas propia, y
es probablemente **el ejemplo más exitoso de arquitectura por niveles de toda la historia del
software**: **BLAS y LAPACK**.

```text
Aplicación del usuario
      ↓
LAPACK      -- resolución de sistemas, valores propios, descomposiciones
      ↓
BLAS nivel 3 -- operaciones MATRIZ-matriz  (gemm)
BLAS nivel 2  -- matriz-VECTOR             (gemv)
BLAS nivel 1   -- vector-vector            (axpy, dot)
      ↓
la implementación optimizada de CADA fabricante
```

Y el motivo por el que esto funcionó tan extraordinariamente bien merece explicarse, porque es una
lección de arquitectura de primer orden:

**BLAS es una especificación de interfaz, no una implementación.** Define exactamente qué hace `dgemm`
—multiplicar matrices de dobles— y con qué argumentos, **y nada más**.

Y entonces:

- **Intel, AMD, NVIDIA, IBM y ARM escriben su propia implementación**, optimizada hasta el último ciclo
  para su hardware.
- **LAPACK se escribió encima**, expresando todos sus algoritmos **en términos de BLAS nivel 3**.
- **Y cualquier programa que use LAPACK se acelera automáticamente** al enlazar con la BLAS del
  fabricante.

**La decisión clave fue expresarlo todo en operaciones matriz-matriz**, porque son las que permiten
aprovechar la caché (clase 128): una multiplicación de matrices hace muchas operaciones por cada dato
leído de memoria, y una operación vector-vector hace una.

**Esa reescritura de LINPACK a LAPACK, en los años ochenta, multiplicó por diez el rendimiento sin
cambiar ningún algoritmo** — solo reorganizando el código para que usara la capa correcta.

Es la mejor demostración de la primera regla del cierre: **la arquitectura correcta hizo fácil un cambio
que de otro modo habría sido imposible**, porque nadie va a reescribir sesenta años de código numérico
para cada procesador nuevo.

Y el ecosistema moderno sigue el patrón:

| Capa | Ejemplos |
|---|---|
| Aplicación | modelos climáticos, CFD, dinámica molecular |
| **Marcos** | PETSc, Trilinos, deal.II |
| **Solvers** | LAPACK, ScaLAPACK, MUMPS, SuperLU |
| **Núcleo** | BLAS (OpenBLAS, MKL, BLIS), FFTW |
| **Comunicación** | MPI |
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Capas is
   Linea      : String (1 .. 200);
   Ultimo     : Natural;
   Cnt        : Natural := 0;
   En_Palabra : Boolean := False;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         En_Palabra := False;
      elsif not En_Palabra then
         En_Palabra := True;
         Cnt := Cnt + 1;
      end if;
   end loop;

   Put_Line ("capas=" & Ada.Strings.Fixed.Trim (Cnt'Image, Ada.Strings.Both));
end Capas;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene una construcción que es **arquitectura expresada en el
lenguaje**, y merece ser el centro de esta explicación: **las unidades hijas**.

```ada
package Banco is ...                    --  el paquete raíz
package Banco.Cuentas is ...             --  hijo público
package Banco.Cuentas.Interes is ...      --  nieto
private package Banco.Interno is ...       --  hijo PRIVADO
```

Y las reglas de visibilidad son exactamente las de una arquitectura en capas, **y las comprueba el
compilador**:

**Un hijo ve la parte privada de su padre.** Es decir: `Banco.Cuentas` puede acceder a los detalles
internos de `Banco`, pero **nadie de fuera puede**.

**Y un paquete hijo privado solo es visible dentro del árbol del padre.** `Banco.Interno` **no se puede
usar desde fuera de `Banco`**, y el compilador rechaza el `with`.

**Eso es control de dependencias arquitectónicas impuesto por el compilador**, y es lo que en otros
lenguajes hay que conseguir con herramientas externas —ArchUnit en Java, reglas de `import` en
analizadores— o con disciplina y esperanza.

Y Ada tiene una segunda construcción que resuelve la segunda regla del cierre de forma directa: **las
restricciones de dependencia en el fichero de proyecto**.

```ada
project Dominio is
   for Source_Dirs use ("src/dominio");
   --  y NO depende de nada de infraestructura
end Dominio;

project Infraestructura is
   for Source_Dirs use ("src/infra");
   --  este SÍ depende de Dominio
end Infraestructura;
```

**Un proyecto declara de qué otros proyectos depende, y `gprbuild` se niega a compilar si alguien
importa hacia el lado equivocado.**

Es la arquitectura hexagonal —o de puertos y adaptadores— **verificada por la construcción**, que es la
única forma de que sobreviva a dos años de prisas.

Y merece cerrar con la arquitectura que Ada practica en su dominio y que es distinta de las tres capas:
**el sistema de tiempo real como conjunto de tareas periódicas**.

```ada
task Sensor with Priority => 20;      --  cada 10 ms
task Control with Priority => 15;      --  cada 50 ms
task Registro with Priority => 5;       --  cuando sobre tiempo
```

**El eje de descomposición aquí no es la responsabilidad funcional: es el plazo temporal** (clase 135).
Y con el perfil Ravenscar (clase 146), **se puede demostrar que el conjunto cumple sus plazos**.

Es una arquitectura donde la propiedad que se garantiza no es la mantenibilidad: es el tiempo.
"""),
        "pascal": ("""
program Capas;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I, Cnt: Integer;
  EnPalabra: Boolean;

begin
  ReadLn(Linea);
  Cnt := 0;
  EnPalabra := False;

  for I := 1 to Length(Linea) do
    if Linea[I] = ' ' then
      EnPalabra := False
    else if not EnPalabra then
    begin
      EnPalabra := True;
      Inc(Cnt);
    end;

  WriteLn('capas=', IntToStr(Cnt));
end.
""", """
**Lo que esta clase enseña en Pascal.** El ecosistema Delphi aporta a esta clase un caso de estudio muy
valioso, porque **su arquitectura por defecto era mala y la comunidad tardó años en salir de ella**.

El modelo original de Delphi era la **programación orientada a eventos con doble clic**: se dibujaba el
formulario, se hacía doble clic en un botón y **se escribía ahí la lógica**.

```pascal
procedure TForm1.Button1Click(Sender: TObject);
begin
  Query1.SQL.Text := 'SELECT * FROM clientes WHERE id = ' + Edit1.Text;
  Query1.Open;
  Label1.Caption := Query1.FieldByName('nombre').AsString;
end;
```

**Ahí están las tres capas en cinco líneas**: presentación, lógica y acceso a datos, con inyección SQL
de regalo (clase 153).

Y eso no era un accidente: **era el modelo que el producto promovía**, porque hacía espectacular la
demostración de dos minutos.

Y la salida de ahí es la historia de esta clase en el ecosistema:

**Primero, los módulos de datos** —`TDataModule`—: un contenedor **sin interfaz visual** donde poner los
componentes de acceso a datos, compartido entre formularios. **Es la primera separación real**, y es de
Delphi 2.

**Después, la separación en unidades por responsabilidad**, con la regla que hoy es evidente: **la
unidad del formulario no debe contener lógica de negocio**.

**Y hoy, el ecosistema moderno**: contenedores de inversión de control (Spring4D), interfaces para las
dependencias, y arquitectura por capas verificada.

Y merece extraer la lección general, porque es la más útil de esta página: **la arquitectura por defecto
de una herramienta es la que tendrá el 90 % del código**.

Si la forma más fácil de hacer algo mezcla las capas, **la mayoría del código las mezclará** — por
mucho que el documento de arquitectura diga otra cosa.

De ahí que la decisión arquitectónica más eficaz no sea escribir un diagrama, sino **hacer que el camino
correcto sea el más fácil**: una plantilla de proyecto, un generador, una comprobación en la integración
continua.

Es la aplicación práctica de la segunda regla del cierre: **una capa que no está impuesta por algo no
es una capa, es una intención**.
"""),
        "lisp": ("""
(let ((linea (read-line))
      (cnt 0)
      (en-palabra nil))
  (loop for c across linea
        do (if (char= c #\\Space)
               (setf en-palabra nil)
               (unless en-palabra
                 (setf en-palabra t)
                 (incf cnt))))
  (format t "capas=~D~%" cnt))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp practica una arquitectura que no aparece en ningún
diagrama de tres capas y que merece explicarse, porque es la más característica del lenguaje:
**construir un lenguaje hasta el problema**.

La idea, formulada por Paul Graham y practicada desde los años setenta:

> En lugar de escribir el programa en el lenguaje, **se extiende el lenguaje hacia el problema** hasta
> que el programa se pueda escribir en una página.

```lisp
;; capa 4: el problema, escrito en el vocabulario del dominio
(definir-flujo procesar-pedido
  (validar :contra esquema-pedido)
  (calcular-impuestos :segun pais)
  (reservar-stock :con-reintentos 3)
  (emitir-evento :pedido-confirmado))

;; capa 3: las macros que hacen que eso sea código válido
;; capa 2: las funciones de dominio
;; capa 1: Common Lisp
```

**`definir-flujo` no existe en Lisp: se define con `defmacro`** (clase 122), y a partir de ahí es
sintaxis del lenguaje.

Y las consecuencias arquitectónicas son reales, en los dos sentidos:

**A favor**, la capa superior es **legible por alguien del dominio** y muy densa: cada línea significa
mucho. Y los cambios habituales —añadir un paso, cambiar una regla— se hacen ahí, sin tocar nada más.

**En contra**, y hay que decirlo: **cada proyecto acaba con su propio lenguaje**, que nadie más conoce.
La curva de entrada de un desarrollador nuevo es alta, y **las herramientas genéricas no entienden ese
código**.

Es exactamente el compromiso que la clase 122 planteaba, aquí a escala de sistema.

Y Lisp tiene una segunda aportación arquitectónica de primer orden que merece nombrarse: **CLOS y el
protocolo de metaobjetos** (clase 111).

```lisp
(defgeneric calcular-precio (producto cliente))
(defmethod calcular-precio ((p Libro) (c ClienteVIP)) ...)
(defmethod calcular-precio ((p Digital) (c Cualquiera)) ...)
```

**El despacho múltiple cambia la arquitectura**: no hay que decidir si el método "pertenece" al producto
o al cliente, porque **pertenece a la relación entre ambos**.

En un lenguaje con despacho simple, esa decisión fuerza patrones —visitante, doble despacho— que existen
**solo para compensar la limitación**. Es un buen recordatorio de que **muchos patrones de diseño son
parches a carencias del lenguaje**, que es lo que la clase 151 desarrolla.
"""),
        "tcl": ("""
gets stdin linea

set capas [llength [split [string trim $linea]]]

puts "capas=$capas"
""", """
**Lo que esta clase enseña en Tcl.** `llength [split ...]` cuenta en un comando lo que las demás columnas
construyen a mano, y ese contraste es la arquitectura de Tcl en miniatura: **es un lenguaje de
pegamento, y su papel arquitectónico es unir cosas escritas en otros**.

Y esa arquitectura tiene nombre y una justificación explícita de su autor. **John Ousterhout la
formuló en 1998**:

> Los sistemas se construyen mejor con **dos lenguajes**: uno de sistemas —C, C++— para los componentes
> que necesitan rendimiento, y uno de guion —Tcl, Python— para **unirlos y configurarlos**.

**Y la métrica que daba es la clave del argumento**: el código de pegamento es **de cinco a diez veces
más corto** en un lenguaje de guion, y **el 90 % de los cambios de un sistema ocurren en el pegamento,
no en los componentes**.

Es la primera regla del cierre de esta clase con datos: **la arquitectura correcta es la que hace fácil
lo que se cambia a menudo**.

Y Tcl se diseñó para ese papel desde el primer día:

```c
/* Un componente en C expone comandos a Tcl */
Tcl_CreateObjCommand(interp, "simular", SimularCmd, NULL, NULL);
```

```tcl
# y el sistema se compone, se configura y se prueba en Tcl
simular -pasos 1000 -modelo $modelo -salida resultados.dat
```

**El componente pesado en C; la composición, los parámetros y el flujo en Tcl.**

Y esa arquitectura es la que domina en un sector entero que merece nombrarse, porque es el mayor éxito
del lenguaje: **el diseño de circuitos integrados**.

```tcl
# el flujo de síntesis de un chip, en Tcl
read_verilog diseno.v
set_clock_period 2.5
compile_ultra
report_timing
write_verilog netlist.v
```

**Synopsys, Cadence, Xilinx y Mentor exponen sus herramientas como comandos de Tcl**, y los flujos de
diseño —que son programas de decenas de miles de líneas— están escritos en él.

Es la arquitectura de aplicación embebible en su forma más pura: **el programa principal no es el
guion, es la herramienta; el guion es el que decide qué hace**.

Y la clase 163 volverá sobre esto — **el lenguaje embebido como decisión de arquitectura** — porque es
la razón por la que Lua está en los videojuegos y Tcl en el diseño de circuitos.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @capas = split ' ', $linea;

print "capas=", scalar(@capas), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl es el caso de estudio de esta página sobre **qué pasa cuando
un lenguaje no impone ninguna arquitectura**, y su historia merece contarse porque tiene las dos mitades.

**La primera mitad: el guion que creció.**

Perl fue diseñado para guiones de una página, y su lema —"hay más de una forma de hacerlo"— es lo
contrario de una arquitectura. El resultado, en los años noventa, fueron sistemas enteros escritos como
guiones CGI de tres mil líneas, sin módulos, con variables globales y HTML mezclado con SQL.

**Ese código es el origen de la mala fama del lenguaje**, y es justo reconocer que la culpa no era del
lenguaje sino de que **nada empujaba hacia otra cosa** — el mismo diagnóstico que Pascal en esta página.

**Y la segunda mitad: la comunidad construyó la arquitectura por encima.**

| Pieza | Qué aportó |
|---|---|
| **Moose** (2006) | **un sistema de objetos completo**: roles, atributos, tipos, modificadores |
| **Plack / PSGI** | la interfaz común servidor-aplicación (como WSGI y Rack) |
| **DBIx::Class** | mapeo objeto-relacional |
| **Catalyst / Dancer / Mojolicious** | marcos MVC |
| **Try::Tiny** | manejo de excepciones sano |

**Moose merece el detalle**, porque es de las mejores implementaciones de un concepto arquitectónico que
esta clase debe nombrar: **los roles**.

```perl
package Nadador;
use Moose::Role;
requires 'mover';                    # quien tome este rol DEBE tener 'mover'
sub nadar { ... }

package Pato;
use Moose;
with 'Nadador', 'Volador';            # COMPONER comportamientos
```

**Un rol es un conjunto de métodos que se compone en una clase, con requisitos declarados** — y a
diferencia de la herencia múltiple, **los conflictos son errores en tiempo de composición**, no
resoluciones silenciosas por orden (clase 111).

Es la solución al problema que la herencia múltiple plantea, la misma que adoptaron los *traits* de
Scala y de Rust, y viene de la investigación en Smalltalk de 2003.

Y la lección de esta página es la que el ecosistema Perl demostró: **la arquitectura se puede añadir
después**, con bibliotecas y disciplina, incluso a un lenguaje que no la fomenta. Cuesta más, y funciona.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string capa;
    int cnt = 0;
    while (std::cin >> capa) ++cnt;

    std::cout << "capas=" << cnt << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ tiene una restricción arquitectónica que ningún otro lenguaje de
esta página comparte con la misma fuerza, y es la que de verdad decide la estructura de un proyecto
grande: **las dependencias de compilación son físicas, no lógicas**.

```cpp
// cliente.hpp
#include "pedido.hpp"      // ← quien incluya cliente.hpp compila TAMBIÉN pedido.hpp
class Cliente { Pedido ultimo_; };
```

**Incluir una cabecera es depender de ella en tiempo de compilación**, y eso se propaga: un proyecto mal
estructurado acaba con **cada fichero compilando medio sistema**, y **una construcción de una hora**.

De ahí que la arquitectura de C++ tenga un vocabulario propio, y merece conocerlo porque es real:

**Declaración adelantada** en lugar de inclusión, cuando basta con un puntero o una referencia:

```cpp
class Pedido;                    // no hace falta la definición completa
class Cliente { Pedido* ultimo_; };
```

**El patrón *pimpl***, que oculta la implementación entera:

```cpp
class Cliente {
public:
    Cliente(); ~Cliente();
    void procesar();
private:
    struct Impl;
    std::unique_ptr<Impl> p_;    // los detalles están en el .cpp
};
```

**Con `pimpl`, cambiar los miembros privados no obliga a recompilar a los clientes** — y además **no
cambia el ABI** (clase 143), lo que permite actualizar una biblioteca compartida sin recompilar lo que
la usa.

Es la única forma en C++ de conseguir lo que Ada tiene de serie con la separación de especificación y
cuerpo (clase 143).

Y el vocabulario arquitectónico de la comunidad, que John Lakos formalizó en *Large-Scale C++ Software
Design* (1996):

| Concepto | Qué significa |
|---|---|
| **Niveles** | el grafo de dependencias debe ser **acíclico**, y cada componente tiene un nivel |
| **Componente** | un par `.hpp` / `.cpp`: **la unidad física de diseño** |
| **Insulation** | ocultar la implementación para romper dependencias de compilación |
| **Escalable** | una jerarquía en la que se puede probar de abajo arriba |

**"El grafo debe ser acíclico" es la segunda regla del cierre de esta clase**, y en C++ tiene una
consecuencia física inmediata: **un ciclo de dependencias entre componentes hace imposible probarlos por
separado y multiplica el tiempo de compilación**.

Y las herramientas modernas lo comprueban:

```bash
include-what-you-use *.cpp        # cada fichero incluye lo que usa, y nada más
cpp-dependencies --graph          # el grafo de dependencias, para ver los ciclos
```
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CAPAS;
  linea char(200) const;
end-pi;

dcl-s i     int(10);
dcl-s cnt   int(10);
dcl-s enpal ind;

cnt = 0;
enpal = *off;

for i = 1 to %len(%trimr(linea));
  if %subst(linea : i : 1) = ' ';
    enpal = *off;
  elseif not enpal;
    enpal = *on;
    cnt += 1;
  endif;
endfor;

dsply ('capas=' + %char(cnt));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** El mundo IBM i tiene una evolución arquitectónica en tres etapas que
es la historia de esta clase contada en una plataforma, y merece verla completa.

**Etapa 1 — el programa monolítico (1988-2000):**

```text
Un programa RPG que:
  - dibuja la pantalla 5250   (especificaciones O y ficheros de pantalla)
  - lee y escribe la base      (acceso registro a registro)
  - y calcula                   (en medio de todo lo anterior)
```

**Las tres capas en un objeto**, exactamente como Delphi y COBOL en esta página.

**Etapa 2 — el programa de servicio (2000-2015):**

```rpgle
// La lógica sale a procedimientos exportados
dcl-proc calcularDescuento export;
  dcl-pi *n packed(9:2);
    cliente char(10) const;
    importe packed(9:2) const;
  end-pi;
  ...
end-proc;
```

**Y con eso llegó todo lo demás**: pruebas unitarias (clase 139), reutilización entre programas,
versionado por firma (clase 143) y la posibilidad de que un programa Java llamara a la misma lógica.

**Es la separación que hizo posible modernizar sin reescribir**, y sigue siendo la recomendación número
uno de la plataforma.

**Etapa 3 — la API (2015-hoy):**

```rpgle
// El mismo procedimiento, expuesto como servicio web con IWS
// o consumido desde una aplicación web moderna
exec sql SELECT ... ;                    // acceso por conjuntos, no por registro
```

| Pieza | Qué permite |
|---|---|
| **IWS** (*Integrated Web Services*) | **convertir un programa RPG en un servicio REST**, sin código |
| **`YAJL` / `DATA-INTO` / `DATA-GEN`** | JSON nativo en RPG (clase 105) |
| **Db2 for i con SQL** | conjuntos en vez de bucles registro a registro |
| **Node.js / Python en PASE** | la capa web moderna, en la misma máquina |

**`DATA-INTO` merece la mención** porque es la pieza que faltaba: **analiza JSON o XML directamente a
una estructura de datos RPG**, con una sola instrucción.

Y la arquitectura resultante es la que la plataforma recomienda hoy y que responde a la primera regla
del cierre: **la lógica de negocio en programas de servicio, estable y probada; la presentación en
cualquier tecnología, sustituible**.

Es la arquitectura hexagonal, alcanzada por evolución en una plataforma de 1988, y con una ventaja
concreta sobre las reescrituras: **la lógica de negocio de treinta años, que funciona y está validada,
no se toca**.
"""),
        "pli": ("""
 capas: procedure options(main);

    declare linea  char(200) varying;
    declare i      fixed binary(31);
    declare cnt    fixed binary(31) initial(0);
    declare enpal  bit(1) initial('0'b);

    get edit (linea) (a(200));

    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then
          enpal = '0'b;
       else if ^enpal then
          do;
             enpal = '1'b;
             cnt = cnt + 1;
          end;
    end;

    put skip list ('capas=' || trim(char(cnt)));

 end capas;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tiene una construcción que es directamente una decisión
arquitectónica del lenguaje y que merece explicarse, porque casi ningún lenguaje moderno la tiene: **los
procedimientos anidados con alcance léxico**.

```pli
 sistema: procedure options(main);
    declare estado fixed binary(31);        /* visible en TODO lo de dentro */

    contabilidad: procedure;
       declare saldo fixed decimal(11,2);    /* visible solo aquí y en sus hijos */

       calcular: procedure;
          saldo = saldo + estado;             /* ve las dos */
       end calcular;

    end contabilidad;
 end sistema;
```

**El anidamiento define la arquitectura**: lo que está dentro ve lo de fuera, y lo de fuera **no ve lo de
dentro**.

Es encapsulación por estructura léxica, y tiene una propiedad interesante para esta clase: **la
arquitectura está en la forma del fichero, no en un documento aparte**.

Y sus límites también merecen decirse, porque explican por qué el modelo no ganó: **el anidamiento es un
árbol**, y **las arquitecturas reales son grafos**. Cuando dos ramas del árbol necesitan compartir algo,
hay que subirlo al tronco — y el tronco crece hasta contenerlo todo.

Es exactamente el problema que los módulos con importación explícita resuelven, y por eso Ada, Modula-2
y todos los posteriores fueron por ahí.

Y PL/I aporta la arquitectura que su mundo practica, y que es la de COBOL en esta página: **la
canalización de pasos de lote y el sistema transaccional en capas**.

Con una particularidad propia que conviene conocer: **PL/I se usó mucho para programación de sistemas**
—Multics, el precursor de Unix, está escrito casi entero en PL/I— y ahí practicó una arquitectura que
merece nombrarse: **los anillos de protección**.

```text
Anillo 0: núcleo
Anillo 1-3: servicios del sistema
Anillo 4-7: aplicaciones de usuario
```

**Un anillo interior puede llamar al exterior, pero no al revés sin una puerta controlada.** Es la
segunda regla del cierre de esta clase —**la dependencia en un solo sentido**— implementada en el
hardware, en 1969.

Y de Multics salieron, además de Unix, la idea de sistema de ficheros jerárquico, la memoria virtual
segmentada y buena parte del vocabulario de la seguridad informática. **PL/I fue el lenguaje en que se
escribió todo eso**, y es una parte de su historia que suele olvidarse.
"""),
        "mumps": ("""
CAPAS ; Contar capas -- clase 149
 read linea
 new i, cnt, p
 set cnt = 0
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" set cnt = cnt + 1
 write "capas=", cnt, !
 quit
""", """
**Lo que esta clase enseña en M.** M practica una arquitectura que casi no aparece en los libros y que es
la que sostiene VistA: **la arquitectura centrada en los datos**, donde **el esquema es el sistema**.

Y la pieza que la implementa merece explicarse en detalle, porque es una de las construcciones más
interesantes de esta página: **FileMan**.

**FileMan es una base de datos y un generador de aplicaciones escrito en M**, de 1979, y su idea central
es esta:

```text
El "diccionario de datos" describe cada fichero:
  - los campos, su tipo, su validación y su ayuda
  - los índices
  - las relaciones con otros ficheros
  - los permisos de lectura y escritura POR CAMPO
  - y las reglas de negocio, como código M asociado al campo
```

Y a partir de ese diccionario, **FileMan genera las pantallas de entrada, los informes, las búsquedas y
las validaciones** — sin escribir código para cada una.

```mumps
 do ^DIC       ; buscar en cualquier fichero: la interfaz sale del diccionario
 do ^DIE        ; editar: los campos, las validaciones y la ayuda salen del diccionario
 do ^DIP         ; imprimir: el informe se define, no se programa
```

**Eso es una arquitectura dirigida por metadatos**, y sus propiedades son las que hoy se buscan en
cualquier plataforma de bajo código:

- **Añadir un campo a una ficha de paciente actualiza las pantallas, los informes y las búsquedas**, sin
  tocar programas.
- **Las reglas de validación viven junto al dato**, no repartidas por la aplicación.
- **Y los permisos son por campo**, que en sanidad no es un lujo.

Y el coste hay que decirlo con la misma claridad: **el sistema entero depende del diccionario**, y un
cambio mal hecho ahí afecta a todo. Además, **la lógica escrita como código M dentro de los metadatos es
difícil de versionar y de revisar** (clase 145).

Es el mismo compromiso que cualquier plataforma dirigida por metadatos —Salesforce, SAP, los ERP en
general— y merece reconocerlo: **la flexibilidad de configurar en lugar de programar se paga con
opacidad**.

Y la lección para el cierre de esta clase: **la arquitectura de VistA hace facilísimo el cambio que su
dominio necesita todos los días** —añadir un campo, un informe, una validación clínica— **y difícil casi
todo lo demás**. Que es, exactamente, lo que se espera de una buena decisión arquitectónica.
"""),
        "smalltalk": ("""
| linea |

linea := stdin nextLine trimBoth.

Transcript show: 'capas=', (linea substrings: ' ') size printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Aquí está el dato del gancho, y merece desarrollarse porque es
el origen de casi todo el vocabulario de esta clase: **MVC se inventó en Smalltalk-80**.

**Trygve Reenskaug lo describió en Xerox PARC en 1979**, y el reparto original era este:

```text
Modelo       -- los datos y las reglas del dominio. NO sabe que existen las vistas.
Vista         -- cómo se presenta. Observa al modelo.
Controlador   -- interpreta la entrada del usuario (ratón, teclado) y actúa sobre el modelo.
```

Y **la pieza que lo hace funcionar es el mecanismo de dependencias**, que en Smalltalk-80 estaba en la
clase `Object`:

```smalltalk
modelo addDependent: unaVista.       "la vista se suscribe"
...
modelo changed: #saldo.               "y el modelo AVISA sin saber a quién"
```

**El modelo no conoce a las vistas: publica que algo cambió.** Eso es el patrón Observador (clase 120), y
está en la raíz de la jerarquía de clases desde 1980.

Y merece señalar una precisión histórica, porque el término se ha desdibujado: **el MVC original no es
el MVC de los marcos web**.

| Smalltalk-80 (1979) | Marcos web actuales |
|---|---|
| El controlador maneja **la entrada física** (ratón, teclado) | El controlador maneja **la petición HTTP** |
| La vista **observa** al modelo y se actualiza sola | La vista se **renderiza** una vez por petición |
| Hay **un trío por cada widget** de la pantalla | Hay un trío por **página** |

**En el MVC original, cada botón y cada campo tenía su propio trío**, y la composición de la interfaz era
la composición de esos tríos.

Lo que hoy más se parece al MVC original no son los marcos web clásicos: **son los marcos reactivos de
componentes** —donde cada componente observa su estado y se actualiza solo— que redescubrieron el modelo
treinta años después.

Y Smalltalk aporta a esta clase una segunda idea arquitectónica que merece nombrarse: **la arquitectura
es la jerarquía de clases y sus protocolos**.

```smalltalk
"Un 'protocolo' es un conjunto de mensajes que un objeto entiende.
 No hay declaración: si responde a los mensajes, sirve."
```

**El tipado por comportamiento** (clase 112) hace que la arquitectura se defina por **qué mensajes se
envían entre partes**, no por qué clases hay.

Y eso tiene una consecuencia práctica que conecta con el cierre de esta clase: **la frontera entre capas
es un conjunto de mensajes**, y se puede sustituir cualquier objeto por otro que responda a los mismos.

Es inyección de dependencias sin marco, objetos simulados sin biblioteca, y arquitectura hexagonal sin
interfaces declaradas — **porque el acoplamiento nunca fue al tipo, sino al comportamiento**.
"""),
    },
)

# ---------------------------------------------------------------------------
# 150 — Refactorización segura
# ---------------------------------------------------------------------------
SPECS["150"] = dict(
    gancho="""
Duplicar un número y afirmar que el resultado es equivalente. Es el contrato de toda refactorización:
**cambiar cómo, sin cambiar qué**. Y esta página tiene el origen de la disciplina: **el Refactoring
Browser, escrito en Smalltalk por John Brant y Don Roberts a mediados de los noventa, fue la primera
herramienta de refactorización automática de la historia**, y los ejemplos del libro de Martin Fowler
que popularizó el término salieron de ese entorno.
""",
    porque="""
Aquí el concepto es el **cambio de estructura sin cambio de comportamiento**, y estos lenguajes lo
enseñan porque **tienen el código más viejo del mundo y no pueden reescribirlo**. Un sistema COBOL de
1985 en producción no se tira: se transforma poco a poco, con red. Y la red es lo que esta página
compara: **el compilador** (Ada, C++), **las pruebas de caracterización** (COBOL, PL/I), **el
verificador de equivalencia** (clase 140), **y las herramientas que refactorizan sobre el árbol
sintáctico en lugar de sobre el texto**.

Y aparece el límite que nadie puede saltarse: **lo que se puede refactorizar con seguridad depende de lo
que se pueda analizar**.
""",
    cierre="""
Lo transferible: **refactorizar sin red no es refactorizar, es reescribir con esperanza**. La secuencia
que funciona es siempre la misma: **primero conseguir una red** —pruebas de caracterización que capturen
el comportamiento actual, aunque sea el equivocado—; **después cambiar en pasos pequeños y reversibles**,
comprobando después de cada uno; **y no mezclar nunca la refactorización con un cambio de
comportamiento**, porque si algo se rompe hay que saber cuál de las dos cosas fue. Y la regla que evita
la mayoría de los desastres: **si no se puede volver atrás en cinco minutos, el paso era demasiado
grande**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. REFACT.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  R       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM DOBLAR

    MOVE R TO ED
    DISPLAY "equivalente=true resultado=" FUNCTION TRIM(ED)
    STOP RUN.

DOBLAR.
    COMPUTE R = N * 2.
""", """
**Lo que esta clase enseña en COBOL.** El programa extrae el cálculo a un párrafo y lo invoca con
`PERFORM` — que es **la refactorización más básica y más útil de COBOL: extraer párrafo** (clase 084).

Y COBOL es el lenguaje donde esta clase tiene más consecuencias económicas del mundo, porque **hay
cientos de miles de millones de líneas en producción y casi ninguna se puede reescribir**.

Y el método que funciona lo formalizó Michael Feathers en *Working Effectively with Legacy Code* (2004),
con una definición que merece citarse porque es incómoda y exacta:

> **Código heredado es código sin pruebas.**

Y su técnica central es la que esta página necesita: **las pruebas de caracterización**.

```text
1. Se ejecuta el programa actual con entradas reales y se GUARDA la salida.
2. Esa salida se declara "lo esperado" —aunque contenga errores conocidos—.
3. Se refactoriza.
4. Si la salida cambia, el cambio rompió algo.
```

**El paso 2 es el que cuesta aceptar**: no se prueba que el programa sea correcto, **se prueba que sigue
haciendo exactamente lo mismo**, errores incluidos.

Y es lo correcto, porque **los errores de un sistema de treinta años forman parte de su
comportamiento**: hay procesos aguas abajo que dependen de ellos (clase 140).

Y COBOL tiene una técnica propia para el problema más difícil de esta clase —**cómo se prueba un
programa que solo funciona con CICS y DB2**— que Feathers llamó *seam* y aquí es literal:

```cobol
      *> Antes: la lógica está pegada a la infraestructura
       EXEC SQL SELECT SALDO INTO :WS-SALDO ... END-EXEC
       COMPUTE WS-NUEVO = WS-SALDO * WS-TASA
       EXEC CICS SEND MAP('PANTALLA') END-EXEC

      *> Después: la lógica es un programa llamable y PROBABLE
       CALL 'CALCINT' USING WS-SALDO WS-TASA WS-NUEVO
```

**Extraer el cálculo a un programa que solo recibe y devuelve datos** es la operación que hace probable
el 90 % de la lógica de negocio, y es la tarea número uno de cualquier modernización (clase 149).

Y las herramientas del mundo COBOL para esto son sustanciales y merecen nombrarse:

| Herramienta | Qué hace |
|---|---|
| **Micro Focus Enterprise Analyzer** | grafo de llamadas y de datos de todo el sistema |
| **CAST Imaging** | análisis de impacto entre lenguajes y tecnologías |
| **IBM ADDI** | análisis de aplicaciones y descubrimiento de reglas de negocio |
| **cobol-check** | pruebas unitarias insertadas en una copia del programa (clase 139) |

**El análisis de impacto es lo que hace viable el paso pequeño del cierre de esta clase**: antes de
tocar un campo, saber **exactamente qué programas lo usan** — que en un sistema de treinta millones de
líneas no es una pregunta que se pueda responder leyendo.
"""),
        "fortran": ("""
program refact
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0)') 'equivalente=true resultado=', doblar(n)

contains

   pure integer function doblar(x)
      integer, intent(in) :: x
      doblar = 2 * x
   end function doblar

end program refact
""", """
**Lo que esta clase enseña en Fortran.** El programa usa `contains` con una función **`pure`**, y esa
palabra es la refactorización de esta página: **`pure` declara que la función no tiene efectos
secundarios**, y el compilador lo comprueba.

Es documentación verificada, y además **permite al compilador optimizar y paralelizar**.

Y Fortran tiene el problema de esta clase en su forma más pesada, porque el código heredado científico
tiene características muy concretas:

```fortran
      COMMON /ESTADO/ X(1000), Y(1000), NPTS, ITER
      EQUIVALENCE (BUF(1), X(1))
      GOTO (10, 20, 30), MODO
      ENTRY ALTERNATIVA
```

**`COMMON` es estado global compartido por nombre y por posición** (clase 088): dos rutinas pueden
declarar el mismo bloque con distintos nombres y tipos, **y funciona**. Es imposible saber quién toca
qué sin leerlo todo.

**`EQUIVALENCE` hace que dos nombres sean la misma memoria.** **`GOTO` calculado** salta según un índice.
Y **`ENTRY`** da varios puntos de entrada al mismo procedimiento.

Y la refactorización canónica de Fortran es la que resuelve todo eso a la vez, y merece describirse en
orden porque el orden importa:

**Paso 1 — capturar el comportamiento**: guardar entradas y salidas de casos reales (clase 140), con
tolerancia numérica justificada.

**Paso 2 — `implicit none`**, fichero a fichero. Rompe la compilación de todo lo que dependía de tipos
implícitos, y **cada rotura es un error latente encontrado** (clase 137).

**Paso 3 — `COMMON` a `module`**:

```fortran
module estado
   implicit none
   integer, parameter :: dp = kind(1.0d0)
   real(dp), allocatable :: x(:), y(:)
   integer :: npts, iter
end module
```

**Con eso, el compilador comprueba los tipos** y `use estado, only: x, npts` **documenta qué usa cada
rutina**.

**Paso 4 — interfaces explícitas**: mover los procedimientos sueltos a módulos activa la comprobación de
argumentos (clase 109), que es donde aparecen los fallos silenciosos de décadas.

**Y paso 5 — `intent` en todo argumento**, que documenta la dirección y la hace comprobar.

Y las herramientas:

```bash
findent -ofree                 # formato fijo a libre (clase 145)
fprettify                       # formateo
plusFORT / SPAG                  # reestructuración automática: quita GOTO, analiza COMMON
```

**plusFORT merece la mención** porque hace algo raro: **reestructura el flujo de control
automáticamente**, convirtiendo marañas de `GOTO` en bucles y condicionales — con demostración de
equivalencia.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Refact is

   function Doblar (X : Integer) return Integer is (2 * X);

   N : Integer;
begin
   Get (N);

   Put ("equivalente=true resultado=");
   Put (Doblar (N), Width => 1);
   New_Line;
end Refact;
""", """
**Lo que esta clase enseña en Ada.** `function Doblar (X : Integer) return Integer is (2 * X);` es una
**función de expresión** de Ada 2012: el cuerpo es una única expresión, sin `begin` ni `end`.

Y es relevante para esta clase por un motivo concreto: **una función de expresión es visible para el
demostrador**, así que `gnatprove` puede razonar sobre ella en las llamadas — cosa que con un cuerpo
normal no siempre puede.

Y Ada tiene la mejor red de esta página para refactorizar, y merece enumerarla porque el conjunto es
inusual:

**Primera, el sistema de tipos como red.** Renombrar un tipo, cambiar un rango, mover un campo: **el
compilador señala todos los sitios afectados**. En un lenguaje sin tipos fuertes, eso es una búsqueda de
texto con esperanza.

**Segunda, la comprobación de coherencia entre unidades** (clase 143): si se cambia una especificación y
algo no se recompila, **el enlace falla**. No hay forma de acabar con la mitad del sistema usando la
interfaz vieja.

**Tercera, los contratos como afirmación de equivalencia** (clase 140):

```ada
function Nueva_Version (X : Integer) return Integer
   with Post => Nueva_Version'Result = Vieja_Version (X);
```

**Se declara literalmente que la nueva debe dar lo mismo que la vieja**, y se comprueba en cada llamada
durante el periodo de transición.

**Y cuarta, la demostración formal**: `gnatprove` puede demostrar que la versión refactorizada **no
introduce errores de ejecución**, y en algunos casos que es equivalente.

Y las herramientas de refactorización asistida:

| Herramienta | Qué hace |
|---|---|
| **GNAT Studio** | renombrar, extraer subprograma, extraer variable, **sobre el árbol sintáctico** |
| **`gnatstub`** | generar el esqueleto del cuerpo desde la especificación |
| **`gnattest`** | regenerar las pruebas al cambiar la interfaz (clase 139) |
| **libadalang** | biblioteca de análisis: **escribir refactorizaciones propias** |

**libadalang merece el detalle**, porque es la respuesta al límite que el "por qué" de esta clase
enunciaba: **da acceso al árbol sintáctico y a la información semántica de un proyecto Ada completo**,
desde Python o Ada.

```python
for nodo in unidad.root.findall(lal.CallExpr):
    if nodo.f_name.p_referenced_decl() == decl_obsoleta:
        ...   # reescritura SEGURA: se sabe a qué se refiere cada nombre
```

**"Se sabe a qué se refiere cada nombre" es toda la diferencia** entre una refactorización y un
`sed -i`.
"""),
        "pascal": ("""
program Refact;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

function Doblar(X: Integer): Integer;
begin
  Result := 2 * X;
end;

begin
  Read(N);
  WriteLn('equivalente=true resultado=', IntToStr(Doblar(N)));
end.
""", """
**Lo que esta clase enseña en Pascal.** El ecosistema Delphi tiene un caso de refactorización a gran
escala que merece contarse, porque es el más doloroso de esta página y enseña una lección general: **la
migración a Unicode de Delphi 2009**.

**Hasta Delphi 2007, `string` era `AnsiString`: un byte por carácter.** A partir de Delphi 2009,
**`string` pasó a ser `UnicodeString`: UTF-16** (clase 093).

Y eso rompió, de golpe, todo el código que suponía "un carácter, un byte":

```pascal
Length(S)                  { ahora cuenta unidades de código de 16 bits }
SizeOf(Char)                { pasó de 1 a 2 }
BlockRead(F, S[1], N)        { lee bytes en una cadena de caracteres anchos: BASURA }
PChar(S)                      { ahora es PWideChar }
Move(Origen, Destino, Longitud)  { ¿longitud en bytes o en caracteres? }
```

**El código que trataba cadenas como memoria dejó de funcionar**, y a menudo **sin error de
compilación** — que es el peor caso posible.

Y la forma en que la comunidad lo resolvió es exactamente la del cierre de esta clase:

**Paso 1 — hacer explícito lo implícito.** Antes de migrar, sustituir `string` por `AnsiString` **donde
de verdad se querían bytes** y por `string` donde se querían caracteres. Eso se hace **en la versión
vieja**, donde nada cambia de comportamiento, y **es refactorización pura**.

**Paso 2 — introducir `RawByteString` y `TBytes`** para los datos binarios, que es lo que había estado
viajando en cadenas por comodidad.

**Paso 3 — migrar**, con el compilador señalando lo que queda.

Y la lección general merece destacarse porque se aplica a cualquier migración grande: **la
refactorización se hace ANTES del cambio, en el sistema que todavía funciona**.

Preparar el código para el cambio y hacer el cambio son dos operaciones distintas, y hacerlas a la vez
es lo que convierte una migración en un desastre — que es la tercera regla del cierre de esta clase.

Y las herramientas del ecosistema:

| Herramienta | Qué hace |
|---|---|
| **Refactorizaciones del IDE** | renombrar, extraer método, declarar variable, cambiar firma |
| **Pascal Analyzer** | variables sin usar, ámbitos, dependencias, complejidad |
| **ModelMaker Code Explorer** | refactorización avanzada y navegación |
| **DUnitX + Delphi-Mocks** | la red de pruebas (clase 139) |
"""),
        "lisp": ("""
(defun doblar (x) (* 2 x))

(let ((n (read)))
  (format t "equivalente=true resultado=~D~%" (doblar n)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene, para esta clase, una ventaja estructural que
merece explicarse: **el programa ya es un árbol sintáctico** (clase 123), así que **una refactorización
es una transformación de listas**.

```lisp
;; Un refactorizador en Lisp es un programa que recorre código como datos
(defun sustituir-llamada (forma vieja nueva)
  (cond ((atom forma) forma)
        ((eq (car forma) vieja) (cons nueva (cdr forma)))
        (t (mapcar (lambda (f) (sustituir-llamada f vieja nueva)) forma))))
```

**No hace falta un analizador**, porque no hay texto que analizar. Es la misma propiedad que hace
posibles las macros (clase 122), aplicada a las herramientas.

Y Lisp tiene una capacidad de refactorización que ningún lenguaje compilado de esta página iguala, y
viene de la Parte 8: **se puede refactorizar con el sistema en marcha y comprobar cada paso al
instante**.

```lisp
(defun calcular (x) ...)      ; C-c C-c: recompila y ya está activa
(calcular 42)                  ; comprobar inmediatamente
```

**El ciclo de un paso de refactorización dura segundos**, que es lo que hace practicable la segunda regla
del cierre: **pasos pequeños comprobados uno a uno**.

Y las herramientas del ecosistema:

| Herramienta | Qué hace |
|---|---|
| **SLIME** | `M-.` ir a la definición, `M-?` quién la llama, recompilar función |
| **`who-calls` / `who-references`** | el grafo de llamadas, desde la imagen viva |
| **`trace`** | comprobar que el comportamiento no cambió (clase 141) |
| **`lisp-critic`** | sugerencias de idiomas más limpios (clase 146) |
| **Paredit / Lispy** | **edición estructural**: mover y envolver expresiones, no texto |

**Paredit merece la mención final**, porque es refactorización a nivel de tecleo: **las operaciones son
"envolver esta expresión", "sacar esta expresión del padre", "partir este nodo"** — nunca "insertar un
paréntesis".

El resultado es que **el código nunca queda con los paréntesis desequilibrados**, ni siquiera a mitad de
una edición.

Es lo mismo que las refactorizaciones de un IDE hacen para lenguajes con sintaxis, y en Lisp llega hasta
el movimiento del cursor.

Y merece cerrar con el límite honesto, que es el del "por qué" de esta clase: **la potencia de Lisp
también dificulta el análisis**. `eval`, `funcall` con símbolos construidos, `intern` de nombres
calculados y las macros que generan definiciones **hacen que "quién llama a esto" no siempre tenga
respuesta exacta**.

Es el mismo compromiso de siempre, aquí en la caja de herramientas: **lo que es dinámico es difícil de
analizar, y lo que es difícil de analizar es difícil de refactorizar con garantías**.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

proc doblar {x} { return [expr {2 * $x}] }

puts "equivalente=true resultado=[doblar $n]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl está en el extremo difícil de esta clase, y merece decirlo con
claridad porque es una consecuencia directa de su diseño: **en Tcl, casi nada se puede analizar
estáticamente** (clase 123).

```tcl
set comando "procesar"
$comando $datos                  ;# ¿quién llama a "procesar"? imposible saberlo
eval $codigoConstruido
uplevel 1 $fragmento
namespace eval $nombreVariable { ... }
```

**Una búsqueda de "procesar" no encuentra esa llamada**, y ninguna herramienta puede garantizar que ha
encontrado todas.

Y de ahí que la red en Tcl sea **necesariamente dinámica**:

**Primera, las pruebas** (clase 139) con `tcltest`, que en Tcl son más importantes que en ningún otro
lenguaje de esta página por lo que se acaba de decir.

**Segunda, `trace` para verificar la equivalencia** (clase 141):

```tcl
# antes de refactorizar: grabar todas las llamadas y sus resultados
trace add execution procesar leave {apply {{cmd code res op} {
    puts $::grabacion "[lrange $cmd 1 end] -> $res"
}}}
```

**Grabar el comportamiento real en producción y usarlo como pruebas de caracterización** es la aplicación
directa de la técnica de COBOL de esta página, y en Tcl se monta en cinco líneas sin tocar el código.

**Y tercera, `nagelfar`**, que es lo más parecido a un análisis estático que Tcl tiene: comprueba
aridades, nombres de comando y citación (clase 137).

Y Tcl aporta a esta clase una refactorización propia que merece conocerse, porque es un mecanismo de
sustitución que otros lenguajes no tienen:

```tcl
# Sustituir gradualmente una implementación por otra, midiendo la equivalencia
rename ::procesar ::procesar_viejo
proc ::procesar {args} {
    set viejo [::procesar_viejo {*}$args]
    set nuevo [::procesar_nuevo {*}$args]
    if {$viejo ne $nuevo} { puts stderr "DIFIERE: $args" }
    return $viejo          ;# de momento, se sirve el viejo
}
```

**Las dos implementaciones se ejecutan, se comparan, y se sirve la vieja mientras dure la
verificación.**

Eso es el patrón que Martin Fowler llamó *Branch by Abstraction* con verificación —y GitHub popularizó
como *Scientist*— **implementado en Tcl con un `rename` y una `proc`**, sin bibliotecas y sin modificar
a los llamadores.

Es la mejor demostración de esta página de que **la refactorización segura depende más de tener un punto
donde interceptar que de las herramientas**.
"""),
        "perl": ("""
use strict;
use warnings;

sub doblar { my ($x) = @_; return 2 * $x }

my $n = <STDIN>;
chomp $n;

print "equivalente=true resultado=", doblar($n), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl comparte el límite de Tcl en esta página —**el análisis
estático es difícil**— y por una razón célebre: **solo Perl puede analizar Perl**.

La frase es de Larry Wall y es literalmente cierta: **la gramática de Perl depende del código que ya se
ha compilado**, porque los prototipos de subrutina y los `use` pueden cambiar cómo se analiza lo que
viene después.

```perl
sub mifuncion($$);      # el prototipo cambia el análisis de las llamadas
use Try::Tiny;           # y esto añade sintaxis nueva
```

Y de ahí que exista una herramienta muy interesante que merece explicarse: **PPI**.

**PPI —*Parse Perl Isolated*— analiza Perl sin ejecutarlo**, aceptando que el resultado es
**aproximado**. Es la base de `Perl::Critic` (clase 146) y de las herramientas de refactorización del
ecosistema.

```perl
my $doc = PPI::Document->new('modulo.pm');
for my $sub ($doc->find('PPI::Statement::Sub')->@*) {
    print $sub->name, "\\n";
}
```

**Y el compromiso que representa es la lección de esta página**: PPI da un árbol sintáctico útil para el
99 % del código real, **y no puede garantizar nada** para el 1 % que hace magia.

Y las herramientas del ecosistema:

| Herramienta | Qué hace |
|---|---|
| **PPI** | árbol sintáctico aproximado, sin ejecutar |
| **Perl::Critic** | reglas de estilo y patrones peligrosos |
| **Devel::Cover** | cobertura: **qué cubre la red antes de tocar nada** |
| **App::perlimports** | limpiar y explicitar las importaciones |
| **Test::Deep / Test::Differences** | comparar salidas antes y después (clase 140) |

**`Devel::Cover` merece el primer puesto en esta clase**, y es una recomendación general: **antes de
refactorizar, medir qué cubren las pruebas**.

```bash
cover -test -report html
```

**Refactorizar una zona con el 20 % de cobertura es trabajar sin red**, por muchas pruebas que tenga el
resto del proyecto. Y la respuesta correcta no es refactorizar con cuidado: **es escribir pruebas de
caracterización de esa zona primero**.

Es la primera regla del cierre de esta clase, y la que más se salta por prisa.

Y Perl aporta una técnica que su dinamismo permite y que resuelve el mismo problema que el `rename` de
Tcl en esta página:

```perl
use Test::MockModule;
my $mod = Test::MockModule->new('Pedido');
$mod->redefine('calcular', sub { ... });     # sustituir para probar
```

**Sustituir cualquier función de cualquier módulo durante una prueba**, sin que el código lo haya
previsto — que es lo que permite poner una red alrededor de código heredado que no fue diseñado para
probarse.
"""),
        "cpp": ("""
#include <iostream>

constexpr long long doblar(long long x) { return 2 * x; }

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "equivalente=true resultado=" << doblar(n) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `constexpr` declara que la función **se puede evaluar en tiempo de
compilación** (clase 122), y aquí es también una refactorización: convertir una función normal en
`constexpr` **no cambia el comportamiento** y permite que el compilador la evalúe cuando los argumentos
son constantes.

Y C++ tiene, en herramientas de refactorización, una de las mejores infraestructuras que existen, y
merece explicar por qué: **Clang expone su propio análisis**.

```bash
clang-tidy --fix --checks='modernize-*' *.cpp    # reescribe el código
clang-rename -offset=1234 -new-name=calcularTotal archivo.cpp
clangd                                             # el servidor de lenguaje del editor
```

**Y la diferencia con una búsqueda y sustitución merece subrayarse**: `clang-rename` **sabe a qué se
refiere cada nombre**, así que renombrar un método `procesar` **no toca los `procesar` de otras clases,
ni los de los comentarios, ni los de las cadenas** — y sí toca las llamadas que llegan por una
referencia a la clase base.

Es la diferencia entre una operación semántica y una textual, y es lo que hace que la refactorización sea
segura.

Y las refactorizaciones que `modernize-*` aplica automáticamente son sustanciales:

```cpp
// antes                              // después
NULL                                → nullptr
typedef int Entero;                  → using Entero = int;
for (auto it = v.begin(); ...)        → for (const auto& x : v)
new Foo()                              → std::make_unique<Foo>()
virtual void f() { }                    → void f() override { }
```

**Aplicar eso a un millón de líneas es un comando**, y es la respuesta a la objeción de que un estándar
nuevo no se puede aplicar a código existente (clase 146).

Y C++ aporta a esta clase su propia red, que es distinta de la de los demás:

| Red | Qué caza |
|---|---|
| **El compilador con `-Wall -Wextra -Werror`** | tipos, conversiones, sombras de nombres |
| **Los desinfectantes** | comportamiento indefinido introducido al refactorizar |
| **`abi-compliance-checker`** | **si la refactorización rompió el ABI** (clase 143) |
| **Pruebas + cobertura (`gcov`, `llvm-cov`)** | la red clásica |
| **`csmith` / comparación de binarios** | equivalencia a nivel de compilador (clase 140) |

**La tercera fila es específica de C++ y fácil de olvidar**: mover un miembro de sitio, añadir un campo
privado o cambiar el orden de las funciones virtuales **cambia el ABI**, así que **una refactorización
"interna" puede romper a todos los que usan la biblioteca ya compilados**.

Es la razón de existir del patrón `pimpl` (clase 149), y un buen ejemplo de que **en C++ hay
refactorizaciones que no son transparentes aunque no cambien el comportamiento del código**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi REFACT;
  n int(10) const;
end-pi;

dcl-proc doblar;
  dcl-pi *n int(20);
    x int(10) const;
  end-pi;
  return 2 * x;
end-proc;

dsply ('equivalente=true resultado=' + %char(doblar(n)));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG ha vivido **la refactorización a mayor escala de esta página**,
y es la que la clase 146 describía: **la conversión de formato fijo a formato totalmente libre**.

```text
     C                   EVAL      TOTAL = PRECIO * CANTIDAD
```

```rpgle
total = precio * cantidad;
```

Y lo interesante para esta clase es que **existen herramientas que lo hacen automáticamente y de forma
verificable**:

| Herramienta | Qué hace |
|---|---|
| **ARCAD Transformer RPG** | conversión de fijo a libre, con equivalencia comprobada |
| **CVTRPGSRC / RDi** | conversión asistida, con revisión |
| **Linoma / Fresche** | modernización de fuentes y de interfaces |

**Y el método es el del cierre de esta clase**: se convierte, **se compila, y se compara el objeto
resultante** — porque **si la conversión es realmente equivalente, el código generado debe ser el
mismo**.

Es un verificador de equivalencia a nivel de compilador (clase 140), y es una red mucho más fuerte que
un conjunto de pruebas.

Y la segunda gran refactorización de esta plataforma, que ya apareció en la clase 149, merece verse como
una secuencia porque es un ejemplo modélico de pasos pequeños:

```text
1. Extraer el cálculo a una SUBRUTINA dentro del mismo programa    (sin riesgo)
2. Convertir la subrutina en un PROCEDIMIENTO con parámetros        (elimina globales)
3. Mover el procedimiento a un módulo aparte                          (compila igual)
4. Enlazar el módulo en un PROGRAMA DE SERVICIO                        (ahora es reutilizable)
5. Escribir pruebas unitarias con RPGUnit                               (¡ya hay red!)
6. Y ahora sí: cambiar la implementación                                 (con red)
```

**Los pasos 1 a 4 no cambian el comportamiento y cada uno se puede desplegar por separado.** El paso 5
es el que crea la red, y solo entonces empieza el cambio real.

Es la secuencia del cierre de esta clase aplicada literalmente, y es la razón por la que la
modernización de IBM i tiene una tasa de éxito notablemente mejor que las reescrituras completas.

Y merece cerrar con el dato que lo justifica: **las reescrituras completas de sistemas heredados fracasan
con mucha más frecuencia de lo que la industria admite**, y el motivo es siempre el mismo — **el
comportamiento real del sistema viejo no está documentado en ninguna parte más que en su propio código**,
y en los treinta años de casos particulares que ha ido acumulando.
"""),
        "pli": ("""
 refact: procedure options(main);

    declare n fixed binary(31);

    doblar: procedure (x) returns (fixed binary(31));
       declare x fixed binary(31);
       return (2 * x);
    end doblar;

    get list (n);

    put skip list ('equivalente=true resultado=' || trim(char(doblar(n))));

 end refact;
""", """
**Lo que esta clase enseña en PL/I.** El programa declara `doblar` como **procedimiento anidado** (clase
149), que es la unidad de extracción natural del lenguaje.

Y PL/I aporta a esta clase la perspectiva del sistema que **no se puede refactorizar del todo**, y merece
tratarla con seriedad porque es la situación real de mucho software crítico.

Los factores que lo hacen difícil son concretos:

**Primero, no queda quien lo escribió.** Un sistema de 1975 tiene autores jubilados, y **la
documentación es el código**.

**Segundo, el lenguaje permite construcciones que impiden el análisis:**

```pli
 declare p pointer;
 declare estructura based(p);           /* la forma depende de lo que apunte */
 declare texto char(100) defined(otro);  /* dos nombres, una memoria */
 goto etiqueta_variable;                  /* salto a una etiqueta CALCULADA */
```

**`goto` a una variable de etiqueta** es especialmente duro: **el destino se decide en ejecución**, así
que el grafo de flujo no se puede construir.

**Y tercero, las reglas de conversión implícita** (clase 140): cualquier cambio de tipo puede alterar
resultados de formas sutiles.

Y la estrategia que la industria aplica en estos casos merece conocerse, porque es distinta de
refactorizar y es legítima: **encapsular en lugar de transformar**.

```text
1. NO se toca el sistema viejo.
2. Se le pone una fachada: un servicio que lo llama y expone una interfaz moderna.
3. Todo lo NUEVO se escribe fuera, contra esa interfaz.
4. Y las funciones se van sacando de una en una, cuando hay razón para tocarlas.
```

**Eso es el patrón del *estrangulador***, que Martin Fowler nombró y que es la técnica de referencia para
sistemas que no se pueden reescribir: **el sistema nuevo crece alrededor del viejo hasta que el viejo se
puede apagar**, en un plazo de años.

Y su propiedad más valiosa es la del cierre de esta clase: **cada paso es pequeño y reversible**, y **el
sistema funciona en todo momento**.

Frente a la alternativa —**la reescritura completa**, que exige dos años sin entregar nada y termina
compitiendo contra un original que mientras tanto ha seguido cambiando— la diferencia en tasa de éxito
está bien documentada, y es grande.
"""),
        "mumps": ("""
REFACT ; Refactorizacion segura -- clase 150
 read n
 write "equivalente=true resultado=", $$doblar(n), !
 quit
 ;
doblar(x) ; devuelve el doble
 quit x * 2
""", """
**Lo que esta clase enseña en M.** El programa extrae el cálculo a una **función extrínseca** —`$$doblar`,
con el doble símbolo de dólar— que es la unidad de extracción de M y la refactorización básica del
lenguaje.

Y M está en el extremo más difícil de esta página, y conviene ser explícito sobre por qué: **la
indirección hace imposible el análisis estático completo** (clase 123).

```mumps
 do @rutina             ; el nombre de la rutina es una VARIABLE
 set @nombre = valor     ; el nombre de la variable es una variable
 xecute codigo            ; código construido en marcha
 do @("EN^" _ paquete)     ; llamada compuesta con concatenación
```

**"¿Quién llama a esta rutina?" no tiene respuesta fiable**, y en VistA —donde la indirección se usa de
verdad— eso es una limitación real.

Y las redes que sí funcionan en este mundo:

**Primera, las sumas de comprobación de rutina** (clase 144): **detectan cualquier modificación**, lo
que permite saber exactamente qué cambió.

**Segunda, las pruebas de caracterización sobre globals** (clase 140): **ejecutar antes y después y
comparar el estado de la base de datos**, que en M captura todos los efectos porque **todo el estado
importante está ahí**.

```mumps
 ; grabar el estado antes, ejecutar, comparar después
 do copiar^UTIL("^PACIENTE", "^ANTES")
 do procesar^MIRUT(caso)
 write $$comparar^UTIL("^PACIENTE", "^ESPERADO")
```

**Y esa es una red más fuerte que la de la mayoría de los lenguajes de esta página**, porque **compara el
efecto completo, no solo el valor devuelto**.

Es la misma idea que el diario de IBM i de la clase 140, y viene del mismo sitio: **cuando el estado vive
en la base de datos, la equivalencia se comprueba sobre el estado**.

**Y tercera, el prefijo de paquete como frontera** (clase 146): las convenciones de nombres de VistA
hacen que **el ámbito de un cambio sea identificable** aunque el análisis automático falle.

Y merece cerrar con la refactorización más valiosa que se puede hacer en M, y que es aplicable a
cualquier lenguaje con estado global: **añadir `new`**.

```mumps
procesar(caso) ;
 new i, j, temporal, resultado      ; ← esta línea
 ...
```

**Declarar como locales las variables que la rutina usa** convierte una rutina que puede corromper el
estado de quien la llama en una que no puede — **sin cambiar lo que hace**.

Es la definición exacta de una refactorización, cuesta una línea, y es la primera que el estándar de
VistA exige (clase 146) precisamente porque es la que más fallos elimina por unidad de esfuerzo.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript
    show: 'equivalente=true resultado=', (n * 2) printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Aquí está el origen del gancho, y merece contarse completo
porque es la historia de esta disciplina: **el Refactoring Browser fue la primera herramienta de
refactorización automática**.

**John Brant y Don Roberts lo escribieron en la Universidad de Illinois a mediados de los noventa**,
dirigidos por Ralph Johnson —uno de los cuatro autores del libro de patrones de diseño—. Y ofrecía, ya
entonces:

```text
Renombrar clase, método, variable, argumento
Extraer método   /  Insertar método (inline)
Extraer variable temporal  /  Insertar
Mover método a otra clase
Subir método a la superclase  /  Bajarlo a las subclases
Añadir y quitar parámetros
Convertir variable temporal en instancia
Abstraer variable de instancia (crear accesores y usarlos)
```

**Esa lista es, prácticamente, el menú "Refactor" de cualquier IDE actual**, y es de hace treinta años.

Y **`Refactoring` de Martin Fowler (1999)**, el libro que dio nombre a la disciplina, **usa Java en los
ejemplos pero nació de este entorno**: Ralph Johnson y Don Roberts firman capítulos, y las técnicas se
habían practicado y automatizado en Smalltalk antes.

Y merece explicar **por qué la herramienta apareció aquí y no en otro sitio**, porque la respuesta es la
de la Parte 8:

**Primero, el código es un objeto.** No hay que analizar texto: **el sistema ya tiene el árbol
sintáctico de cada método**, accesible como objetos.

**Segundo, `allCallsOn:` responde de verdad** (clase 138): se puede recorrer todo el sistema preguntando
qué método envía qué mensaje.

**Y tercero, el ciclo es instantáneo**: recompilar un método son milisegundos, y las pruebas —con SUnit,
inventado en el mismo entorno (clase 139)— se ejecutan en el acto.

**Las tres condiciones que la segunda regla del cierre de esta clase necesita —pasos pequeños,
comprobados, rápidos— estaban dadas.**

Y el límite honesto también hay que decirlo, y es el mismo que en Lisp y Tcl en esta página: **el
dinamismo**.

```smalltalk
objeto perform: (nombre , 'Total') asSymbol.     "el selector se construye"
```

**Un mensaje enviado con `perform:` y un selector calculado es invisible para el analizador.** El
Refactoring Browser **avisa** cuando detecta `perform:` cerca de lo que se está renombrando, pero no
puede garantizarlo.

Y esa advertencia es la conclusión más útil de esta página entera: **ninguna herramienta de
refactorización es completamente segura en un lenguaje dinámico**, y el que las inventó lo sabía y lo
decía. La red final siguen siendo las pruebas.
"""),
    },
)
