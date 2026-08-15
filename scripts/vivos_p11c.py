# -*- coding: utf-8 -*-
"""Parte 11, lote C — clases 171 a 173. Ver `vivos_parte11.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 171 — Componente de automatización
# ---------------------------------------------------------------------------
SPECS["171"] = dict(
    gancho="""
Ejecutar N tareas y decir que terminaron: `tareas=5 estado=completado`. Es un orquestador reducido a lo
esencial, y esta clase trata del componente que ningún diagrama dibuja y sin el cual no funciona nada.
Y aquí hay una precedencia clara: **el JCL, de 1964, es un lenguaje de orquestación de trabajos con
dependencias, condiciones y asignación de recursos** — y lo que hoy hacen Airflow, Argo o GitHub Actions
tiene una forma sorprendentemente parecida.
""",
    porque="""
Aquí el concepto es la **automatización como componente de primera clase**, y estos lenguajes la enseñan
porque **tienen los lenguajes de orquestación más antiguos y más probados**: JCL en z/OS, CL en IBM i, y
las herramientas que crecieron alrededor —Expect, Perl, Tcl— para automatizar lo que no tenía interfaz.

Y aparece la propiedad que separa una automatización que aguanta de una que se rompe cada semana: **la
idempotencia** — que ejecutarla dos veces dé el mismo resultado que ejecutarla una.
""",
    cierre="""
Lo transferible: **una automatización que no se puede volver a ejecutar sin miedo no está terminada**. De
ahí las tres propiedades que hay que buscar: **idempotencia**, para poder reintentar; **reanudabilidad**,
para no repetir lo caro cuando falla el paso siete; y **registro de lo que hizo**, porque una
automatización silenciosa es imposible de diagnosticar (clase 142). Y la advertencia que más caro sale
ignorar: **el código de automatización es código de producción** — se versiona, se revisa y se prueba,
porque es lo que despliega, borra y mueve datos.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. AUTOMAT.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED
    DISPLAY "tareas=" FUNCTION TRIM(ED) " estado=completado"
    STOP RUN.
""", """
**COBOL y la automatización.** Aquí está el dato del gancho, y merece verlo con la lista de propiedades
del cierre delante: **el JCL es un lenguaje de orquestación** (clase 077).

```jcl
//NOCTURNO JOB CLASS=B,MSGCLASS=X,RESTART=PASO3
//PASO1 EXEC PGM=EXTRAER
//SALIDA  DD DSN=&&TEMP,DISP=(NEW,PASS)
//PASO2 EXEC PGM=VALIDAR,COND=(0,LT,PASO1)
//PASO3 EXEC PGM=CALCULAR,COND=(8,LE)
//PASO4 EXEC PGM=INFORMAR,COND=EVEN
```

Y las tres propiedades del cierre están ahí:

**`RESTART=PASO3` es la reanudabilidad**: **el trabajo se relanza desde el paso que falló**, sin repetir
los anteriores.

**`COND=` es el control de flujo**: cada paso se ejecuta o se salta según los códigos de retorno de los
anteriores (clase 167). **`COND=EVEN` significa "ejecuta aunque algo haya fallado"** — el paso de
limpieza.

**Y el registro es automático** (clase 142): el registro del trabajo recoge cada paso, su código, su
consumo y sus mensajes.

Y hay una cuarta propiedad que el JCL tiene y que las herramientas modernas suelen no tener, y merece
destacarse: **la declaración de recursos**.

```jcl
//SALIDA DD DSN=MI.FICHERO,DISP=(NEW,CATLG),SPACE=(CYL,(100,50)),
//          UNIT=SYSDA,VOL=SER=WORK01
```

**El trabajo declara cuánto espacio necesita y qué ficheros va a usar, ANTES de arrancar**, y **el
planificador puede negarse a lanzarlo si no hay sitio**.

**Eso evita el fallo más frustrante de un proceso largo: reventar a las cuatro horas por falta de
espacio.**

Es una idea que los orquestadores modernos han recuperado con las peticiones de recursos de los
contenedores, y por la misma razón.

Y sobre los planificadores, merece nombrarlos porque son el componente real de esta clase en estos
sistemas: **Control-M, CA-7, TWS** — herramientas que gestionan **decenas de miles de trabajos al día con
dependencias entre sí**, calendarios, ventanas y avisos.

**Es Airflow, con cuarenta años y a otra escala.**
"""),
        "fortran": ("""
program automat
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A)') 'tareas=', n, ' estado=completado'
end program automat
""", """
**Fortran y la automatización.** El cálculo científico tiene su propio orquestador, y merece conocerlo
porque su modelo es distinto: **el planificador del clúster**.

```bash
#!/bin/bash
#SBATCH --job-name=simulacion
#SBATCH --nodes=64
#SBATCH --ntasks-per-node=48
#SBATCH --time=24:00:00
#SBATCH --dependency=afterok:12345      # ← ¡dependencias entre trabajos!
#SBATCH --array=1-100                    # ← 100 variantes del mismo trabajo

srun ./simulacion --caso $SLURM_ARRAY_TASK_ID
```

**SLURM, PBS y LSF** reparten un superordenador entre cientos de usuarios, y merece señalar lo que
resuelven:

| Capacidad | Detalle |
|---|---|
| **Cola con prioridades y cuotas** | quién entra antes, y cuánto puede consumir |
| **Reserva de recursos** | 64 nodos durante 24 horas, garantizados |
| **Dependencias** | `afterok`, `afterany`: el JCL de esta página |
| **Arreglos de trabajos** | **cien variantes con una sola línea** |
| **Y límite de tiempo duro** | el trabajo se mata al agotarlo |

**La cuarta fila es la que resuelve el problema de la clase 167**: un barrido de parámetros **es
`--array`**, siempre que el programa acepte el caso por la línea de comandos.

Y la quinta trae la propiedad del cierre que este dominio necesita más que ninguno: **la
reanudabilidad**.

```text
Un cálculo de 200 horas no cabe en un límite de 24.
Así que el programa GUARDA PUNTOS DE CONTROL y se relanza:
   - cada N pasos escribe su estado completo
   - y al arrancar, si encuentra un punto de control, continúa desde ahí
```

**Y esa capacidad hay que diseñarla dentro del programa**: no la puede añadir el planificador.

Es la segunda propiedad del cierre, y en este dominio es un requisito de arquitectura del componente de
cálculo, no una comodidad — porque **sin ella, cualquier fallo cuesta la ejecución entera**.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Automat is
   N : Integer;
begin
   Get (N);

   Put_Line ("tareas=" & Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both) &
             " estado=completado");
end Automat;
""", """
**Ada y la automatización.** Ada no es un lenguaje de guiones, y esta clase es el sitio para lo que sí
aporta a este componente: **la automatización de la construcción y la verificación** (clase 147).

```bash
gprbuild -P proyecto.gpr -XMODO=produccion
gnatcheck -P proyecto.gpr
gnattest -P proyecto.gpr && ./obj/test_runner
gnatprove -P proyecto.gpr --level=2
gnatcoverage --level=stmt+mcdc
```

**Y en un proyecto certificado, esa secuencia no es una comodidad: es parte del expediente** — cada
ejecución se archiva con su resultado, porque **hay que demostrar ante un auditor que se hizo** (clase
144).

Y merece señalar lo que eso impone y que es la tercera propiedad del cierre llevada al extremo: **la
automatización tiene que dejar constancia**.

```text
No basta con que la construcción pase.
Hay que conservar:
  - qué versión exacta del fuente se usó
  - qué versión de cada herramienta
  - qué opciones
  - y los informes completos, firmados
```

Es la lista de materiales de la clase 144, producida por la automatización y conservada durante la vida
del producto — que en aviación son **treinta años o más**.

Y hay una propiedad de Ada que merece nombrarse porque hace la automatización mucho más fiable y que la
clase 149 explicó: **el fichero de proyecto es la única fuente de la configuración**.

```ada
project Proyecto is
   type Modo_Tipo is ("desarrollo", "produccion");
   Modo : Modo_Tipo := external ("MODO", "desarrollo");

   package Compiler is
      case Modo is
         when "desarrollo" => for Default_Switches ("Ada") use ("-g", "-gnata");
         when "produccion"  => for Default_Switches ("Ada") use ("-O2");
      end case;
   end Compiler;
end Proyecto;
```

**Las opciones no están repartidas entre un guion, un Makefile y la memoria de alguien**: están
declaradas, con las variantes explícitas.

Y eso resuelve el problema de reproducibilidad más común (clase 144): **que el binario dependa de cómo lo
compiló quien lo compiló**.
"""),
        "pascal": ("""
program Automat;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('tareas=', IntToStr(N), ' estado=completado');
end.
""", """
**Pascal y la automatización.** Free Pascal es una buena elección para el componente de automatización por
la razón de la clase 167: **produce herramientas pequeñas, rápidas y sin dependencias**.

```pascal
uses Process, SysUtils;

function Ejecutar(const Cmd: string; const Args: array of string;
                  out Salida: string): Integer;
begin
  Result := -1;
  with TProcess.Create(nil) do
  try
    Executable := Cmd;
    Parameters.AddStrings(Args);            { ← lista, no cadena (clase 153) }
    Options := [poWaitOnExit, poUsePipes];
    Execute;
    Salida := ...;
    Result := ExitStatus;                    { ← el código de retorno }
  finally
    Free;
  end;
end;
```

**`Parameters` como lista y no como cadena** es la defensa contra la inyección de comandos, igual que en
Perl (clase 161).

Y merece dedicar el resto a la primera propiedad del cierre, porque es la que menos se aplica y la que
más problemas evita: **la idempotencia**.

```pascal
{ ✗ no idempotente: al reintentar, duplica }
AppendFile(Registro, Linea);

{ ✓ idempotente: comprobar antes de actuar }
if not FileExists(Destino) then CopyFile(Origen, Destino);
if not DirectoryExists(Ruta) then ForceDirectories(Ruta);
```

**Y la forma general, que sirve en cualquier lenguaje: escribir a un temporal y renombrar.**

```pascal
Guardar(Destino + '.tmp');
RenameFile(Destino + '.tmp', Destino);     { ← atómico en el mismo sistema de ficheros }
```

**El renombrado es atómico**, así que **el fichero de destino nunca existe a medias** — y si el proceso
muere a mitad, **no deja un fichero corrupto, deja un temporal que se puede borrar**.

Es el mismo patrón del enlace simbólico del despliegue (clase 148), y es probablemente **la técnica más
rentable de toda esta clase**: convierte una operación que puede dejar el sistema en un estado
intermedio en una que no.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "tareas=~D estado=completado~%" n))
""", """
**Lisp y la automatización.** Lisp tiene, para este componente, una capacidad que su modelo hace natural:
**la automatización puede ser código de primera clase, no cadenas**.

```lisp
(defparameter *plan*
  '((:extraer  :de "origen" :a "temp")
    (:validar  :sobre "temp" :requiere (:extraer))
    (:calcular :sobre "temp" :requiere (:validar))
    (:informar :requiere (:calcular) :siempre t)))

(ejecutar-plan *plan*)
```

**El plan es una estructura de datos**, así que se puede **inspeccionar, validar, transformar y
visualizar** antes de ejecutarlo — cosa que un guion de shell no permite.

Y esa propiedad merece destacarse porque es la que separa un orquestador de un guion: **un plan
declarado se puede analizar**.

```lisp
(detectar-ciclos *plan*)          ; ¿hay dependencias circulares?
(orden-topologico *plan*)          ; ¿en qué orden hay que ejecutarlo?
(que-falta-si-falla :validar)       ; ¿qué se salta?
```

**Es exactamente lo que Airflow y Make hacen con su grafo**, y en Lisp la estructura ya es un dato.

Y el ecosistema para el componente práctico:

| Herramienta | Notas |
|---|---|
| **UIOP** | `run-program`, rutas, variables de entorno — portable |
| **ASDF** | el sistema de construcción, con dependencias (clase 143) |
| **Roswell** | guiones ejecutables con `#!` |
| **`cl-cron` / hilos** | tareas periódicas dentro de un servicio |

Y merece cerrar con la propiedad de Lisp que hace la automatización más segura y que la clase 132
explicó: **`unwind-protect`**.

```lisp
(unwind-protect
     (progn (bloquear-recurso) (procesar))
  (liberar-recurso))        ; ← se ejecuta SIEMPRE, aunque haya error o interrupción
```

**Una automatización que reserva algo —un bloqueo, un directorio temporal, una conexión— tiene que
liberarlo pase lo que pase**, y **la mitad de los guiones de shell no lo hacen** porque hay que escribir
un `trap`.

Es la tercera propiedad del cierre vista desde otro lado: **una automatización que falla debe dejar el
sistema en un estado conocido**, no en el que estuviera.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

puts "tareas=$n estado=completado"
""", """
**Tcl y la automatización.** Este es **el componente de Tcl por excelencia** (clases 155 y 165), y esta
clase es el sitio para juntar lo que las anteriores han ido nombrando.

```tcl
# Ejecutar con control de errores y de tiempo
proc ejecutar {cmd args} {
    set salida ""
    set codigo [catch {exec {*}$cmd {*}$args} salida opciones]
    if {$codigo} {
        set info [dict get $opciones -errorcode]
        if {[lindex $info 0] eq "CHILDSTATUS"} {
            return -code error "falló con estado [lindex $info 2]: $salida"
        }
        return -code error $salida
    }
    return $salida
}
```

**`-errorcode` con `CHILDSTATUS` da el código de salida del proceso hijo**, distinguiendo "el programa
devolvió error" de "no se pudo ejecutar" — que son dos fallos distintos y casi ningún guion los separa.

Y **Expect** (clase 147) sigue siendo la respuesta cuando no hay API:

```tcl
package require Expect
set timeout 30
spawn ssh operador@equipo
expect {
    "password:"    { send "$::env(CLAVE)\\r"; exp_continue }
    "$ "            { send "reiniciar servicio\\r" }
    timeout         { error "sin respuesta del equipo" }
}
```

**Y la lección de Expect que la clase 147 anticipó es la primera propiedad del cierre aplicada a las
esperas**: **esperar por un evento, no por un tiempo**.

```tcl
# ✗ frágil: depende de la carga de la máquina
after 5000
# ✓ robusto: espera a que ocurra algo, con un límite
esperarPuerto 8080 -timeout 30
```

Y merece cerrar señalando la propiedad que hace de Tcl un buen orquestador y que la clase 161 explicó:
**el bucle de eventos**.

```tcl
# Lanzar cinco tareas EN PARALELO y esperar a todas
foreach t $tareas {
    set canal [open "|./tarea $t" r]
    fconfigure $canal -blocking 0
    fileevent $canal readable [list recogerSalida $canal]
    incr pendientes
}
vwait pendientes
```

**Paralelismo real sin hilos y sin bloquear**, que es lo que un orquestador necesita: **lanzar muchas
cosas, recoger sus salidas y saber cuándo han terminado todas**.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "tareas=$n estado=completado\\n";
""", """
**Perl y la automatización.** Perl fue **la herramienta de automatización de sistemas durante veinte
años**, y su ecosistema para este componente sigue siendo excelente:

```perl
use IPC::Run qw(run timeout);
use Try::Tiny;
use File::Temp qw(tempdir);
use Path::Tiny;

my $dir = tempdir(CLEANUP => 1);            # ← se borra solo al salir

try {
    run \\@comando, \\undef, \\my $salida, \\my $error, timeout(300)
        or die "falló ($?): $error";
} catch {
    warn "reintentando: $_";
    ...
};
```

**`tempdir(CLEANUP => 1)` y `timeout(300)`** son las dos piezas que más veces faltan en una
automatización: **limpiar siempre** y **no esperar para siempre**.

Y Perl aporta a esta clase la herramienta de automatización que definió una categoría entera y merece
nombrarse: **rsync no, pero sí `cfengine` y sus descendientes**.

```text
La gestión de configuración —describir el estado deseado
en lugar de los pasos para llegar— nació en los años noventa,
y su idea central es la primera propiedad del cierre de esta clase.
```

```perl
# ✗ imperativo: los pasos. No es idempotente.
system('useradd', 'app');
system('mkdir', '/opt/app');

# ✓ declarativo: el estado deseado. Idempotente por construcción.
asegurar_usuario('app');
asegurar_directorio('/opt/app', modo => 0755);
```

**Y "asegurar" es la palabra clave**: **comprueba y actúa solo si hace falta**, así que **ejecutar dos
veces no cambia nada**.

Es exactamente el modelo de Ansible, Puppet, Chef y Terraform, y **es la aportación conceptual más
importante de esta clase**: **describir el destino, no el camino**.

Y merece cerrar con la advertencia del cierre que Perl ilustra bien, porque su facilidad la provoca: **un
guion de automatización crece hasta ser un sistema** (clase 165).

**Y en cuanto despliega, borra o mueve datos de producción, es código de producción**: con pruebas, con
revisión y con un modo de simulación.

```perl
GetOptions('dry-run' => \\my $simular);
...
if ($simular) { say "haría: borrar $ruta" } else { unlink $ruta }
```

**El modo de simulación es la característica más valiosa de una herramienta de automatización**, y la que
permite revisar un cambio grande antes de ejecutarlo.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "tareas=" << n << " estado=completado" << '\\n';
    return 0;
}
""", """
**C++ y la automatización.** C++ no se usa para escribir guiones, y esta clase es el sitio para lo que sí
aporta: **es el lenguaje de las herramientas que la automatización usa**.

```text
Sistemas de construcción:  Ninja, CMake, Bazel (C++ y Java)
Contenedores:               containerd, runc (Go), pero el núcleo es C
Orquestación:                Kubernetes (Go), Envoy (C++)
Y las herramientas rápidas: ripgrep, fd (Rust), jq (C)
```

Y la razón es la de la clase 167: **el tiempo de arranque**.

```text
Un sistema de construcción invoca herramientas MILES de veces.
Con 30 ms de arranque por invocación, 10.000 invocaciones son 5 minutos
de puro arranque.
```

**Por eso las herramientas del camino crítico están compiladas**, y por eso Ninja —escrito en C++ y
diseñado para hacer una sola cosa— desplazó a Make en proyectos grandes.

Y C++ aporta a esta clase la biblioteca que la clase 147 agradece y que merece nombrar: **`std::filesystem`
(C++17)**, que hizo portables las operaciones de ficheros.

```cpp
#include <filesystem>
namespace fs = std::filesystem;

fs::create_directories(destino);              // idempotente por definición
fs::copy_file(a, b, fs::copy_options::overwrite_existing);
for (const auto& e : fs::recursive_directory_iterator(raiz)) { ... }

std::error_code ec;
fs::remove_all(temporal, ec);                  // sin excepción: con código
```

**`create_directories` no falla si ya existe**, que es la primera propiedad del cierre integrada en la
API — y merece señalarlo porque es la diferencia entre una API que empuja a la idempotencia y una que no.

Y la sobrecarga con `std::error_code` merece la mención por la tercera propiedad: **en una automatización,
un fallo esperado —el fichero no está— no debería lanzar**; y uno inesperado, sí.

**Distinguir los dos es lo que hace que el registro sea útil** en lugar de una lista de excepciones donde
no se sabe cuál importaba.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi AUTOMAT;
  n int(10) const;
end-pi;

dsply ('tareas=' + %char(n) + ' estado=completado');

*inlr = *on;
return;
""", """
**RPG y la automatización.** IBM i tiene su propio lenguaje de orquestación, hermano del JCL y bastante
más agradable: **CL, el *Control Language***.

```cl
PGM
   DCL VAR(&FECHA) TYPE(*CHAR) LEN(8)

   MONMSG MSGID(CPF0000) EXEC(GOTO CMDLBL(ERROR))     /* ← manejo de errores GLOBAL */

   RTVSYSVAL SYSVAL(QDATE) RTNVAR(&FECHA)
   CALL PGM(EXTRAER) PARM(&FECHA)
   CALL PGM(CALCULAR) PARM(&FECHA)
   SBMJOB CMD(CALL PGM(INFORMAR)) JOB(INFORME)         /* ← en segundo plano */
   RETURN

ERROR:
   SNDMSG MSG('Falló el proceso nocturno') TOUSR(*SYSOPR)
   MONMSG MSGID(CPF0000)
ENDPGM
```

Y merece destacar tres cosas porque son las propiedades del cierre:

**`MONMSG` es manejo de errores declarado para todo el programa** —o para el comando anterior— y **eso
hace que un guion CL no siga adelante en silencio tras un fallo**, que es el problema clásico de los
guiones de shell sin `set -e`.

**`SBMJOB` envía trabajo al planificador**, con su cola, su prioridad y su descripción — así que **la
ejecución en segundo plano es del sistema**, con su registro (clase 142).

**Y el planificador del sistema** —`ADDJOBSCDE`— **da las tareas periódicas**, con calendario y con
control de si el trabajo anterior sigue corriendo.

Y esta clase debe recoger la propiedad que esta plataforma da y que hace la automatización mucho más
segura: **el registro completo de cada trabajo** (clase 142).

```text
DSPJOBLOG del trabajo nocturno:
  cada comando ejecutado, sus parámetros, sus mensajes y su resultado.
Sin instrumentar nada.
```

**Es la tercera propiedad del cierre resuelta por la plataforma**, y hace que diagnosticar un proceso
nocturno que falló a las 3:40 sea mirar un registro, en lugar de deducirlo de lo que quedó a medias.
"""),
        "pli": ("""
 automat: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('tareas=' || trim(char(n)) || ' estado=completado');

 end automat;
""", """
**PL/I y la automatización.** PL/I comparte el JCL con COBOL en esta página, y esta clase es el sitio para
la pieza que hace de orquestador de verdad en estos sistemas: **el planificador de trabajos**.

```text
Control-M, CA-7, IBM Workload Scheduler gestionan:
  - decenas de miles de trabajos al día
  - con dependencias entre ellos, entre sistemas y entre máquinas
  - calendarios: laborables, fin de mes, festivos por país
  - ventanas de ejecución y recursos exclusivos
  - reintentos automáticos y escalado de avisos
  - y una vista del plan completo del día
```

**Y esa lista es, casi palabra por palabra, la de un orquestador moderno** — con dos diferencias que
merecen señalarse porque van en direcciones opuestas:

**A favor de los antiguos**: **el calendario de negocio**. Un planificador de mainframe sabe qué es "el
tercer día hábil del mes", "el cierre trimestral" y "los festivos de cada país donde opera el banco" — y
eso, que suena trivial, **es la mitad de la lógica de un proceso financiero** y las herramientas modernas
lo suelen dejar al usuario.

**A favor de los modernos**: **el plan está en el repositorio**. Un DAG de Airflow o un fichero de
GitHub Actions **se versiona, se revisa y se despliega** (clase 145); la definición en un planificador
clásico **vive en su propia base de datos**, se edita por pantalla y **no está en git**.

Y esa segunda diferencia es exactamente la advertencia del cierre de esta clase: **la automatización es
código de producción**.

**Cuando el plan de ejecución de mil trabajos vive fuera del control de versiones, nadie sabe quién lo
cambió ni por qué** — y es una de las deudas técnicas más caras y menos reconocidas de estos sistemas
(clase 154).

Y la práctica que lo corrige y que varias organizaciones han adoptado: **exportar las definiciones del
planificador a ficheros y versionarlas**, aunque la herramienta no lo haga sola.
"""),
        "mumps": ("""
AUTOMAT ; Componente de automatizacion -- clase 171
 read n
 write "tareas=", n, " estado=completado", !
 quit
""", """
**M y la automatización.** VistA tiene un planificador propio dentro del sistema, y merece conocerlo
porque su diseño encaja con el modelo de M: **TaskMan**.

```mumps
 ; Programar una tarea
 set ZTRTN = "PROCESAR^MIRUT"
 set ZTDTH = $horolog                    ; cuándo
 set ZTDESC = "Proceso nocturno de altas"
 set ZTSAVE("VAR*") = ""                  ; qué variables se le pasan
 do ^%ZTLOAD
```

**Y la propiedad que lo distingue es la de la clase 161: la cola de tareas es una global**.

```text
Consecuencias:
  - la tarea programada es PERSISTENTE: sobrevive a un reinicio
  - se puede consultar, cancelar y reprogramar con SQL... o con $order
  - y la programación participa de la TRANSACCIÓN que la creó
```

**La tercera merece el detalle**: si una transacción crea una tarea y luego se deshace, **la tarea
tampoco se crea**.

Es el problema de la doble escritura de la clase 161 resuelto de raíz, y es una propiedad que un
planificador externo **no puede tener**.

Y `ZTSAVE` merece la mención porque resuelve algo específico de M: **el ámbito global por defecto** (clase
146). La tarea se ejecuta en otro proceso, con otro espacio de variables, así que **hay que declarar
explícitamente qué se le lleva**.

**Y eso, que parece una molestia, es exactamente la primera propiedad del cierre**: **la tarea recibe todo
lo que necesita y no depende del estado del proceso que la creó**, así que **se puede reejecutar**.

Y esta clase debe recoger la práctica de este dominio que la criticidad impone y que merece transferirse:
**la automatización clínica avisa a personas**.

```text
Un proceso que falla no escribe solo en un registro:
  - envía un mensaje a la cola del operador
  - y si es crítico, activa un aviso que alguien tiene que reconocer
```

**Una automatización que falla en silencio es peor que no tenerla**, porque **todo el mundo cree que se
está haciendo** — y esa es la forma más peligrosa de la tercera propiedad del cierre incumplida.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'tareas=', n printString, ' estado=completado'; cr.
""", """
**Smalltalk y la automatización.** Smalltalk tiene, para este componente, una capacidad que su modelo hace
natural: **la tarea programada es un objeto vivo dentro del sistema**.

```smalltalk
"Una tarea periódica, dentro de la imagen"
tarea := [ [ true ] whileTrue: [
              self procesarPendientes.
              (Delay forSeconds: 60) wait ] ] newProcess.
tarea name: 'procesador'; priority: Processor userBackgroundPriority.
tarea resume.
```

**Y la propiedad interesante es la de la Parte 8: se puede inspeccionar en marcha** (clase 141).

```smalltalk
Processor    "todos los procesos, su estado y su prioridad"
tarea suspend. tarea resume. tarea terminate.
tarea suspendedContext    "¡y ver DÓNDE está parada!"
```

**Poder mirar dónde está bloqueada una tarea programada, en producción, sin haberlo previsto** es algo que
en la mayoría de los sistemas requiere volcados y suerte.

Y el ecosistema tiene lo que falta:

| Herramienta | Notas |
|---|---|
| **TaskIt** | tareas con conjunto de trabajadores y futuros |
| **`Delay` / `Process`** | lo básico, en el sistema |
| **OSSubprocess / LibC** | lanzar procesos externos |
| **Iceberg + guiones Pharo** | automatizar la construcción (clase 147) |

Y merece cerrar esta clase con la advertencia que el modelo de imagen impone y que es la primera
propiedad del cierre en su versión más difícil: **una tarea dentro de la imagen comparte su destino**.

```text
Si la imagen se reinicia, las tareas programadas DESAPARECEN
—salvo que se vuelvan a crear al arrancar—.
Y si una tarea corrompe el estado, lo corrompe para todos.
```

**Así que la programación tiene que reconstruirse al arrancar**, desde una descripción persistente:

```smalltalk
Smalltalk at: #Programacion put: (OrderedCollection new).
"y en el arranque de la imagen:"
Programacion do: [ :cada | cada iniciar ].
```

Es la misma conclusión que M en esta página, con otro vocabulario: **la definición de lo que hay que hacer
tiene que sobrevivir al proceso que lo hace** — y eso significa que vive en un almacén persistente, no en
la memoria del que lo ejecuta.
"""),
    },
)

# ---------------------------------------------------------------------------
# 172 — Persistencia y almacenamiento
# ---------------------------------------------------------------------------
SPECS["172"] = dict(
    gancho="""
Guardar un par nombre-valor: `guardado=x=5`. Es la operación más simple de persistir, y esta clase trata
de lo que hay detrás de esa palabra: **que el dato siga ahí después**. Y "después" incluye un corte de
luz a mitad de la escritura, que es donde casi todos los sistemas descubren que no habían pensado en
ello. Y aquí hay una respuesta que merece el titular: **el diario, la técnica que hace posible sobrevivir
a eso, es de los años setenta y viene de estos sistemas**.
""",
    porque="""
Aquí el concepto es la **durabilidad**, y estos lenguajes la enseñan porque **operan sistemas donde
perder datos no es una opción**: bancos, hospitales, seguros. Y de ahí salieron las técnicas que hoy usan
todas las bases de datos: **el registro de escritura anticipada, los puntos de control, la confirmación
en dos fases y el diario de imágenes anterior y posterior** (clase 140).

Y aparece la pregunta que casi nadie se hace hasta que es tarde: **¿qué pasa si el proceso muere entre
estas dos líneas?**
""",
    cierre="""
Lo transferible: **escribir no es persistir**. Entre `write` y el plato del disco hay al menos tres
búferes —el de la biblioteca, el del sistema operativo y el del propio disco— y **solo `fsync` cierra el
trato**. De ahí las tres reglas: **escribir a un temporal y renombrar**, porque el renombrado es atómico
y evita ficheros a medias; **`fsync` antes de dar algo por confirmado**, y saber que cuesta; y **no
inventar formatos de almacenamiento transaccional** — si hacen falta transacciones, se usa una base de
datos, porque los detalles que hay que acertar son muchos y llevan cuarenta años acertados.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. GUARDAR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  C-NOM   PIC X(20).
01  C-VAL   PIC X(20).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-NOM C-VAL
    END-UNSTRING

    DISPLAY "guardado=" FUNCTION TRIM(C-NOM)
            "=" FUNCTION TRIM(C-VAL)
    STOP RUN.
""", """
**COBOL y la persistencia.** COBOL tiene el catálogo de organizaciones de fichero más completo del
lenguaje, y merece verlo porque cada una responde a un patrón de acceso (clase 170):

```cobol
       SELECT CLIENTES ASSIGN TO "CLIENTES"
           ORGANIZATION IS INDEXED           *> VSAM KSDS: acceso por clave
           ACCESS MODE IS DYNAMIC             *> secuencial Y aleatorio
           RECORD KEY IS CLI-ID
           ALTERNATE RECORD KEY IS CLI-NIF WITH DUPLICATES
           FILE STATUS IS WS-ESTADO.
```

| Organización | Acceso | Uso |
|---|---|---|
| **SEQUENTIAL** | de principio a fin | lote (clase 152) |
| **RELATIVE** | por número de registro | acceso directo por posición |
| **INDEXED** (VSAM KSDS) | **por clave, con índices alternativos** | maestro de datos |
| **LINE SEQUENTIAL** | texto con saltos de línea | intercambio |

**`ALTERNATE RECORD KEY` merece la mención**: **VSAM mantiene índices secundarios automáticamente** —lo
que M tiene que hacer a mano (clase 170)— y es de 1973.

Y la durabilidad, que es el tema del cierre:

```cobol
           EXEC CICS SYNCPOINT END-EXEC          *> confirmar
           EXEC CICS SYNCPOINT ROLLBACK END-EXEC  *> o deshacer
```

**Y debajo está la técnica del gancho**: **el registro de escritura anticipada**.

```text
Antes de modificar un dato, el sistema escribe en un REGISTRO SECUENCIAL
lo que va a hacer, y se asegura de que ESE registro está en disco.
Solo entonces modifica el dato.

Si el sistema cae, al arrancar recorre el registro:
  - lo confirmado y no aplicado, se aplica
  - lo no confirmado, se deshace
```

**Ese algoritmo —conocido como ARIES, formalizado por IBM en 1992— es la base de la recuperación de
prácticamente todas las bases de datos actuales**: DB2, Oracle, SQL Server, PostgreSQL y SQLite.

Y su idea central es la primera regla del cierre generalizada: **escribir la intención antes que el
cambio**, porque **un registro secuencial se puede escribir de forma atómica y una modificación en su
sitio, no**.
"""),
        "fortran": ("""
program guardar
   implicit none
   character(len=60) :: linea
   character(len=20) :: nombre, valor
   integer :: p1

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, ' ')
   nombre = linea(1:p1-1)
   valor  = adjustl(linea(p1+1:))

   write(*, '(A)') 'guardado=' // trim(nombre) // '=' // trim(valor)
end program guardar
""", """
**Fortran y la persistencia.** El cálculo científico tiene un problema de durabilidad propio y muy
concreto: **escribir terabytes desde miles de procesos a la vez**.

```fortran
! Cada proceso escribe su trozo del mismo fichero, en paralelo
call MPI_File_open(MPI_COMM_WORLD, 'salida.dat', MPI_MODE_CREATE + MPI_MODE_WRONLY, &
                   MPI_INFO_NULL, fh)
call MPI_File_write_at_all(fh, desplazamiento, datos, n, MPI_DOUBLE_PRECISION, estado)
call MPI_File_close(fh)
```

**MPI-IO coordina la escritura de miles de procesos sobre un sistema de ficheros paralelo** —Lustre,
GPFS— y **agrupa las escrituras pequeñas en grandes**, que es lo único que hace viable ese caudal.

Y la técnica de durabilidad de este dominio es la de la clase 171: **los puntos de control**.

```fortran
! Cada N pasos: escribir el estado completo, y hacerlo BIEN
write(nombre, '(A,I6.6,A)') 'ckpt_', paso, '.h5.tmp'
call escribir_estado(nombre)
call flush_y_sincronizar(nombre)
call rename(nombre, 'ckpt_ultimo.h5')     ! ← temporal y renombrado (cierre, regla 1)
```

**Y el renombrado al final es lo que evita el desastre clásico**: **caer mientras se escribe el punto de
control y quedarse sin el nuevo y sin el viejo**.

Y merece nombrar la técnica que este dominio ha desarrollado para el mismo problema a otra escala: **los
puntos de control multinivel**.

```text
Nivel 1: en memoria local o en el nodo vecino    → rapidísimo, sobrevive a fallo de proceso
Nivel 2: en el disco local del nodo                → sobrevive a fallo de nodo
Nivel 3: en el sistema de ficheros paralelo         → sobrevive a todo, y es lento
```

**Se escribe el nivel 1 a menudo y el nivel 3 pocas veces**, porque **la mayoría de los fallos son
locales**.

Es la misma jerarquía que las réplicas de una base de datos —memoria, disco local, otro centro— y la misma
lógica: **la durabilidad se paga en latencia, y conviene comprar solo la que hace falta**.

Es la regla del cierre matizada con datos: **`fsync` cuesta, y saber cuánta durabilidad se necesita en
cada punto es una decisión de ingeniería, no un absoluto**.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Guardar is
   Linea  : String (1 .. 60);
   Ultimo : Natural;
   Sep    : Natural;
begin
   Get_Line (Linea, Ultimo);
   Sep := Ada.Strings.Fixed.Index (Linea (1 .. Ultimo), " ");

   Put_Line ("guardado=" & Linea (1 .. Sep - 1) & "=" &
             Ada.Strings.Fixed.Trim (Linea (Sep + 1 .. Ultimo), Ada.Strings.Both));
end Guardar;
""", """
**Ada y la persistencia.** Ada tiene entrada y salida con tipos en el estándar, y su diseño merece
señalarse porque es distinto del habitual:

```ada
with Ada.Sequential_IO;
with Ada.Direct_IO;
with Ada.Streams.Stream_IO;

package Registro_IO is new Ada.Direct_IO (Registro);   --  ¡genérico sobre EL TIPO!

F : Registro_IO.File_Type;
Registro_IO.Open (F, Registro_IO.Inout_File, "datos.bin");
Registro_IO.Read (F, R, Positive_Count (Indice));       --  acceso directo por índice
```

**`Direct_IO` se instancia con el tipo del registro**, así que **el fichero es de registros de ese tipo y
solo de ese tipo** — el compilador impide leer una cosa donde se guardó otra.

Es una comprobación que casi ningún lenguaje de esta página hace sobre ficheros binarios, y evita el fallo
de la clase 106.

Y el dominio de Ada trae un requisito de persistencia que merece contarse porque es extremo: **la memoria
no volátil en sistemas embarcados**.

```ada
type Parametros is record ... end record;
for Parametros'Alignment use 4;

--  Escritura en EEPROM o FRAM, con verificación
procedure Guardar_Parametros (P : Parametros) is
   Copia : Parametros := P;
begin
   Copia.Suma := Calcular_Suma (P);       --  ← suma de comprobación EN el registro
   Escribir_Fisico (Copia);
   if Leer_Fisico /= Copia then           --  ← releer y comparar
      raise Error_Escritura;
   end if;
end Guardar_Parametros;
```

**Y las dos técnicas de ahí son la respuesta de este dominio al gancho de esta clase**:

**La suma de comprobación dentro del registro** permite detectar una escritura interrumpida al leerlo.

**Y releer y comparar** confirma que el medio aceptó el dato — porque **en una memoria con celdas
desgastadas, la escritura puede fallar en silencio**.

Y la variante completa, para cuando no se puede perder nada: **dos copias alternadas**.

```text
Se escribe siempre en la copia que NO está en uso, con su contador y su suma.
Al arrancar, se leen las dos y se usa la más reciente que sea VÁLIDA.
```

**Y así, un corte de luz a mitad de escritura deja intacta la copia anterior** — que es la primera regla
del cierre de esta clase, implementada sin sistema de ficheros.
"""),
        "pascal": ("""
program Guardar;
{$MODE OBJFPC}{$H+}
uses SysUtils, StrUtils;

var
  Linea, Nombre, Valor: string;
  P: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P := Pos(' ', Linea);
  Nombre := Copy(Linea, 1, P - 1);
  Valor  := Trim(Copy(Linea, P + 1, Length(Linea)));

  WriteLn('guardado=', Nombre, '=', Valor);
end.
""", """
**Pascal y la persistencia.** Pascal tiene un tipo que merece destacarse porque es una idea de 1970 muy
buena y poco imitada: **el fichero tipado**.

```pascal
type
  TRegistro = record
    Id: Integer;
    Nombre: string[50];        { cadena corta: tamaño FIJO, apta para fichero }
    Saldo: Currency;
  end;

var
  F: file of TRegistro;         { ← un fichero DE ESE TIPO }
  R: TRegistro;

begin
  Assign(F, 'datos.dat');
  Reset(F);
  Seek(F, 10);                  { al registro 10 }
  Read(F, R);
  R.Saldo := R.Saldo + 100;
  Seek(F, 10);
  Write(F, R);
  Close(F);
end;
```

**`file of TRegistro` es acceso directo por número de registro, con el tipo comprobado** —lo mismo que
`Direct_IO` de Ada en esta página— y **es de Pascal original**.

Y la advertencia que hay que dar y que la clase 157 explica: **`file of` guarda la representación en
memoria del registro**, así que **el fichero depende de la alineación, del tamaño de los tipos y del orden
de bytes**.

```pascal
{$PACKRECORDS 1}     { sin relleno: el fichero es portable... si todos usan esto }
```

**Un fichero escrito por la versión de 32 bits puede no leerse con la de 64** — que es exactamente el
problema de la migración de la clase 150.

Y sobre durabilidad, el ecosistema Pascal da lo necesario y merece verlo junto porque es la receta
completa del cierre:

```pascal
{ 1. escribir a un temporal }
AssignFile(F, Destino + '.tmp');
Rewrite(F);
...
{ 2. vaciar y sincronizar }
Flush(F);
FileFlush(TFileRec(F).Handle);        { fsync }
CloseFile(F);
{ 3. y renombrar, que es atómico }
RenameFile(Destino + '.tmp', Destino);
```

**Los tres pasos, en ese orden**, y merece subrayar el segundo porque es el que casi siempre falta:
**`Flush` vacía el búfer de la biblioteca al sistema operativo; `FileFlush` obliga al sistema operativo a
llevarlo al disco**.

**Son dos búferes distintos, y solo el segundo sobrevive a un corte de luz.**
"""),
        "lisp": ("""
(let* ((linea (read-line))
       (sep (position #\\Space linea))
       (nombre (subseq linea 0 sep))
       (valor (string-trim '(#\\Space #\\Return) (subseq linea (1+ sep)))))
  (format t "guardado=~A=~A~%" nombre valor))
""", """
**Lisp y la persistencia.** Lisp tiene la persistencia más cómoda de esta página y una de las más
peligrosas, y merece ver las dos caras.

**La cómoda, que la clase 159 explicó:**

```lisp
(with-open-file (f "estado.lisp" :direction :output :if-exists :supersede)
  (let ((*print-readably* t) (*print-circle* t))
    (print *estado* f)))

(with-open-file (f "estado.lisp") (read f))
```

**Guardar y cargar una estructura arbitraria son dos líneas** — y `*print-circle*` maneja las referencias
compartidas y los ciclos.

**Y la peligrosa es la del cierre de esta clase**, porque ese código tiene un fallo que casi nadie ve:

```lisp
:if-exists :supersede
```

**`:supersede` trunca el fichero al abrirlo.** Así que **si el proceso muere a mitad de la escritura, el
fichero anterior ya no existe y el nuevo está incompleto** — se pierden las dos versiones.

Y la forma correcta es la primera regla del cierre:

```lisp
(let ((temp (merge-pathnames "estado.tmp" destino)))
  (with-open-file (f temp :direction :output :if-exists :supersede)
    (print *estado* f)
    (finish-output f))                       ; ← vaciar
  (rename-file temp destino))                 ; ← atómico
```

**`finish-output` antes de renombrar** es imprescindible: **sin él, el renombrado puede ocurrir antes de
que los datos lleguen al fichero**.

Y Lisp tiene una forma de persistencia que ningún otro de esta página comparte y que la clase 144
explicó: **la imagen**.

```lisp
(sb-ext:save-lisp-and-die "estado.core")
```

**Guardar el sistema entero, con todos sus objetos vivos** — que es persistencia total y sin código de
serialización.

**Y su límite hay que decirlo**: **no es incremental ni transaccional**. Guardar una imagen de 200 MB para
persistir un cambio pequeño no es una opción, y **si el proceso muere entre dos guardados, se pierde
todo lo intermedio**.

Es un buen ejemplo de la tercera regla del cierre: **para persistencia con garantías, una base de datos**.
La imagen es excelente para arrancar rápido y para congelar un estado conocido, no para ser el almacén.
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] nombre valor

puts "guardado=$nombre=$valor"
""", """
**Tcl y la persistencia.** Tcl tiene la escritura de ficheros integrada en su modelo de canales (clase
161), y esta clase es el sitio para las opciones que deciden la durabilidad:

```tcl
set f [open "datos.txt.tmp" w]
fconfigure $f -encoding utf-8 -translation lf -buffering full
puts $f $contenido
flush $f                      ;# ← vacía el búfer de Tcl al sistema operativo
close $f
file rename -force "datos.txt.tmp" "datos.txt"    ;# ← atómico
```

**Y merece explicar la diferencia entre `flush` y `close`**, porque es la que produce corrupciones:
**`close` vacía y cierra, pero ninguno de los dos garantiza que el dato esté en el disco físico** — para
eso hace falta `fsync`, que Tcl expone en versiones recientes o vía TclX.

Es la segunda regla del cierre, y **Tcl la deja explícita** en lugar de esconderla.

Y merece señalar `-translation lf`, porque es la trampa de la clase 145: **por defecto, Tcl traduce los
fines de línea según la plataforma**, así que **un fichero escrito en Windows y leído en Linux puede
diferir** — y para datos binarios hay que poner `-translation binary`.

Y Tcl trae dos almacenes en la distribución que merecen conocerse:

| Almacén | Notas |
|---|---|
| **`array set` / `array get`** | serializar un arreglo asociativo a una lista y volver |
| **Metakit / VFS** | el sistema de ficheros virtual de los Starkits (clase 144) |
| **`tdbc::sqlite3`** | **SQLite, con transacciones de verdad** |

**Y la tercera es la aplicación directa de la tercera regla del cierre**: cuando hace falta que un
conjunto de cambios sea todo o nada, **la respuesta es SQLite y no un fichero propio**.

```tcl
db transaction {
    db allrows {UPDATE cuentas SET saldo = saldo - :importe WHERE id = :origen}
    db allrows {UPDATE cuentas SET saldo = saldo + :importe WHERE id = :destino}
}
```

**Esas dos actualizaciones ocurren las dos o ninguna**, y sobrevive a un corte de luz — porque SQLite
implementa el registro de escritura anticipada de la explicación de COBOL en esta página.

**Reimplementar eso a mano es la forma más eficaz de perder datos**, y es lo que la tercera regla del
cierre quiere evitar.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($nombre, $valor) = split ' ', $linea;

print "guardado=$nombre=$valor\\n";
""", """
**Perl y la persistencia.** Perl tiene todo el arsenal de esta clase, y esta es la ocasión para la receta
completa, que es la del cierre:

```perl
use Path::Tiny;
use Fcntl qw(:flock O_WRONLY O_CREAT O_EXCL);

# 1. temporal + fsync + renombrado, en una llamada
path("datos.json")->spew_utf8($json);        # Path::Tiny ya hace temporal y renombrado

# 2. o a mano, con control:
open(my $fh, '>', "$destino.tmp") or die $!;
print $fh $contenido;
$fh->flush;                                   # búfer de Perl → sistema operativo
$fh->sync;                                     # → disco   (IO::Handle)
close $fh;
rename("$destino.tmp", $destino) or die $!;    # atómico
```

**Y la línea `$fh->sync` es la del cierre**: sin ella, **el renombrado puede completarse y el contenido
no estar**, lo que deja un fichero de tamaño cero — un fallo real y muy desconcertante.

Y Perl aporta a esta clase el mecanismo de exclusión que una automatización necesita (clase 171):

```perl
open(my $lock, '>', "/var/run/miapp.lock") or die;
flock($lock, LOCK_EX | LOCK_NB) or die "ya hay otra instancia\\n";
```

**`flock` con `LOCK_NB` es la forma correcta de impedir dos ejecuciones simultáneas** — y merece la
advertencia: **es consultivo** (clase 161), y **no funciona bien en sistemas de ficheros de red**.

Y los almacenes del ecosistema, ordenados por lo que garantizan:

| Almacén | Durabilidad |
|---|---|
| **Fichero de texto o JSON** | lo que el programa haga |
| **`Storable`** | binario propio de Perl (clase 159) |
| **`DB_File` / `BerkeleyDB`** | clave-valor con transacciones opcionales |
| **`DBD::SQLite`** | **ACID completo** |
| **PostgreSQL, MySQL** | ACID, con réplicas |

**Y la lección del cierre está en el salto entre la primera y la cuarta**: **entre "escribir un fichero" y
"garantizar que un conjunto de cambios es atómico y durable" hay cuarenta años de ingeniería**, y no se
recorren en una tarde.

Es la razón por la que SQLite está en todos los teléfonos: **es la forma más barata de tener esa
garantía**.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string nombre, valor;
    if (!(std::cin >> nombre >> valor)) return 1;

    std::cout << "guardado=" << nombre << '=' << valor << '\\n';
    return 0;
}
""", """
**C++ y la persistencia.** C++ es donde se implementan los almacenes de esta página, y esta clase es el
sitio para los detalles que hay que acertar y que casi nadie conoce.

**Los tres búferes del cierre, con sus llamadas:**

```cpp
std::ofstream f("datos.tmp");
f << contenido;
f.flush();                              // 1. búfer de la biblioteca → sistema operativo
// pero eso NO basta:
int fd = ::open("datos.tmp", O_WRONLY);
::fsync(fd);                             // 2. sistema operativo → disco
::close(fd);
::rename("datos.tmp", "datos");           // 3. renombrado atómico
// ¡y falta uno!
int dir = ::open(".", O_RDONLY);
::fsync(dir);                              // 4. ← ¡sincronizar el DIRECTORIO!
::close(dir);
```

**El cuarto paso merece la explicación porque es el que casi todo el mundo olvida**: **el renombrado
modifica el directorio, y esa modificación también está en un búfer**.

Sin `fsync` del directorio, **puede ocurrir que el fichero exista con su contenido y que la entrada de
directorio se pierda** — el fichero desaparece.

**Es un fallo real, documentado, y es la razón por la que las bases de datos serias sincronizan el
directorio.**

Y hay más detalles que merecen conocerse porque han causado pérdidas de datos famosas:

| Detalle | Consecuencia |
|---|---|
| **`fsync` puede fallar y no se puede reintentar** | en Linux, un `fsync` fallido marca las páginas como limpias: **el dato se pierde y el segundo `fsync` dice que todo bien** |
| **`write` puede escribir menos bytes de los pedidos** | hay que comprobar el valor devuelto y repetir |
| **La caché del disco puede mentir** | discos baratos que confirman antes de escribir |
| **`O_DIRECT` salta la caché del sistema** | lo usan las bases de datos, con alineación estricta |

**La primera fila es el llamado "fsyncgate" de 2018**, que obligó a PostgreSQL a cambiar su estrategia de
recuperación: **si `fsync` falla, la única respuesta segura es abortar el proceso**.

Y todo esto es exactamente la tercera regla del cierre de esta clase: **la lista de cosas que hay que
acertar para tener durabilidad es larga, poco conocida y llena de detalles del sistema operativo**.

**Y por eso la recomendación no es aprenderlos todos: es usar una base de datos que ya los haya
acertado.**
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi GUARDAR;
  linea char(60) const;
end-pi;

dcl-s texto  varchar(60);
dcl-s pos    int(10);
dcl-s nombre varchar(20);
dcl-s valor  varchar(20);

texto = %trim(linea);
pos = %scan(' ' : texto);

nombre = %subst(texto : 1 : pos - 1);
valor  = %trim(%subst(texto : pos + 1));

dsply ('guardado=' + nombre + '=' + valor);

*inlr = *on;
return;
""", """
**RPG y la persistencia.** IBM i tiene la persistencia integrada en el sistema, y esta clase es el sitio
para la pieza que la hace segura y que la clase 140 ya nombró: **el diario**.

```text
STRJRNPF FILE(CLIENTES) JRN(MIJRN) IMAGES(*BOTH)
```

**Y con eso, cada cambio de cada fila queda registrado** con la imagen anterior y la posterior, el
trabajo, el usuario, el programa y la marca de tiempo.

Y merece enumerar lo que eso da, porque es más de lo que parece:

| Capacidad | Cómo |
|---|---|
| **Recuperación tras caída** | se aplican los cambios confirmados del diario |
| **Control de compromiso** | transacciones sobre varios ficheros |
| **`RMVJRNCHG`** | **deshacer los cambios hasta un instante** (clase 148) |
| **Replicación** | el diario se envía a otra máquina: alta disponibilidad |
| **Auditoría** | quién cambió qué y cuándo (clase 142) |
| **Y captura de cambios** | alimentar un almacén analítico |

**La cuarta fila merece destacarse** porque es la base de las soluciones de alta disponibilidad de esta
plataforma: **enviar el diario a un sistema de respaldo que lo aplica** — que es exactamente la
replicación por registro de escritura anticipada de PostgreSQL y de MySQL, y es de los años noventa.

Y el control de compromiso, que es la parte de transacciones:

```rpgle
exec sql SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
...
exec sql COMMIT;      // o ROLLBACK
```

**O con el acceso nativo, `COMMIT` y `ROLLBACK` como operaciones de RPG** sobre ficheros con diario.

Y merece cerrar con la observación que esta plataforma permite y que conecta con el cierre de esta clase:
**aquí la durabilidad no es una decisión del programa, es una propiedad del objeto**.

**Se activa el diario sobre una tabla con un comando, y a partir de ahí todos los programas que la usen
están cubiertos** — sin cambiar ni una línea.

Es la diferencia entre una garantía que hay que implementar en cada sitio y una que se configura una vez,
y explica por qué en esta plataforma la pérdida de datos por un fallo de programación es rara.
"""),
        "pli": ("""
 guardar: procedure options(main);

    declare linea  char(60) varying;
    declare nombre char(20) varying;
    declare valor  char(20) varying;
    declare p      fixed binary(31);

    get edit (linea) (a(60));
    linea = trim(linea);

    p = index(linea, ' ');
    nombre = substr(linea, 1, p - 1);
    valor = trim(substr(linea, p + 1));

    put skip list ('guardado=' || nombre || '=' || valor);

 end guardar;
""", """
**PL/I y la persistencia.** PL/I tiene el catálogo de organizaciones de fichero de COBOL y añade un
concepto propio que merece explicarse porque es de los pocos de esta página: **el área**.

```pli
 declare zona area(100000);
 declare p pointer;
 declare nodo based(p),
           2 valor fixed binary(31),
           2 siguiente pointer;

 allocate nodo in (zona) set (p);      /* reservar DENTRO del área */
 ...
 write file(f) from (zona);             /* ¡y GUARDAR EL ÁREA ENTERA! */
```

**Un `AREA` es un montón autocontenido con punteros relativos a su base**, así que **una estructura
enlazada construida dentro de un área se puede escribir a disco y volver a leer** — con los punteros
intactos.

Es **persistencia de estructuras con punteros**, resuelta en 1964, y merece señalar por qué es difícil:
**los punteros normales son direcciones absolutas y no sirven al recargar en otra dirección** (clase
161).

**Y la solución de PL/I —punteros relativos a un área— es la misma que hoy usan los formatos de
serialización sin copia** como FlatBuffers y Cap'n Proto (clase 159), y la misma que la memoria compartida
entre procesos necesita.

Y merece la comparación con el resto de esta página:

```text
La mayoría:  serializar → escribir → leer → deserializar
Con AREA:     escribir el bloque → leerlo → usarlo directamente
```

**Sin coste de conversión**, que es exactamente el argumento de FlatBuffers.

Y sobre durabilidad, PL/I vive en el mismo mundo de COBOL de esta página: **el registro de escritura
anticipada de DB2 e IMS, el control de compromiso y la confirmación en dos fases** (clase 161).

Y merece cerrar con la observación general que estas columnas permiten y que el cierre de esta clase
defiende: **las garantías de durabilidad que hoy se dan por supuestas en cualquier base de datos son el
resultado de cuarenta años de acertar detalles**, muchos de ellos aprendidos perdiendo datos de verdad —
y esa es la razón para no reimplementarlas.
"""),
        "mumps": ("""
GUARDAR ; Persistencia -- clase 172
 read linea
 new nombre, valor
 set nombre = $piece(linea, " ", 1)
 set valor = $piece(linea, " ", 2)
 write "guardado=", nombre, "=", valor, !
 quit
""", """
**M y la persistencia.** M tiene la persistencia más simple de esta página, y merece verla con la lista
del cierre delante:

```mumps
 set ^CONFIG("x") = 5
```

**Esa línea está en disco, es transaccional, sobrevive al reinicio y es visible para todos los procesos**
(clase 161).

**Y no hay que abrir, ni cerrar, ni vaciar, ni sincronizar, ni serializar.**

Y merece explicar cómo se consigue, porque debajo está exactamente la técnica del gancho: **el diario**.

```text
Una escritura en una global:
  1. se escribe en el DIARIO (secuencial, rápido)
  2. y se modifica la base de datos en memoria
  3. los bloques modificados se llevan a disco después, en bloque

Si el sistema cae, al arrancar se recorre el diario y se recupera.
```

**Es el registro de escritura anticipada de COBOL en esta página**, y M lo tiene desde sus primeras
implementaciones porque su público —hospitales— no podía perder datos.

Y las transacciones:

```mumps
 tstart
 set ^CUENTA(origen) = ^CUENTA(origen) - importe
 set ^CUENTA(destino) = ^CUENTA(destino) + importe
 tcommit
```

**Todo o nada**, y **junto con cualquier otra cosa que la transacción haga** — incluida encolar un mensaje
(clase 161), que es lo que resuelve el problema de la doble escritura.

Y merece cerrar con la comparación que hace M valiosa en esta clase y que la clase 170 anticipó:

```text
En casi todos los lenguajes de esta página:
   variable en memoria  ≠  dato persistente
   y entre las dos hay una capa: ficheros, SQL, mapeador, serialización.

En M:
   ^dato  es  dato persistente
   y la única diferencia con una variable local es un carácter.
```

**Esa ausencia de capa es la propiedad más valiosa del lenguaje**, y es la razón por la que sistemas
escritos en él llevan cuarenta años sin perder datos: **hay muchísimo menos código entre el programa y el
disco, y por tanto muchos menos sitios donde equivocarse**.
"""),
        "smalltalk": ("""
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

Transcript
    show: 'guardado=', (partes at: 1), '=', (partes at: 2);
    cr.
""", """
**Smalltalk y la persistencia.** Smalltalk tiene tres formas de persistir, y compararlas cierra bien esta
clase porque cubren todo el espectro.

**Una, la imagen** (clase 144):

```smalltalk
Smalltalk snapshot: true andQuit: false.
```

**Guarda todos los objetos vivos.** Total, y ni incremental ni transaccional — el mismo límite que la
imagen de Lisp en esta página.

**Dos, la serialización** (clase 159):

```smalltalk
FLSerializer serialize: unGrafo toFileNamed: 'estado.fuel'.
```

**Rápida y completa**, y con la receta del cierre por delante: **temporal, sincronizar y renombrar**.

**Y tres, GemStone**, que es la que merece el espacio porque resuelve lo que las otras dos no:

```smalltalk
System beginTransaction.
cuenta saldo: cuenta saldo - importe.
otra saldo: otra saldo + importe.
System commitTransaction.        "ACID sobre el grafo de objetos"
```

**Los objetos viven en un repositorio transaccional compartido**, y **modificar un objeto es modificar la
base de datos**.

Y merece explicar lo que eso implica, porque es lo mismo que M en esta página conseguido con objetos:

```text
Sin: mapeo objeto-relacional, serialización, consultas, ni "guardar".
Con: transacciones, detección de conflictos, y objetos compartidos entre máquinas.
```

**Y la detección de conflictos merece la mención** porque es la parte difícil: **si dos procesos modifican
el mismo objeto, la confirmación del segundo falla y hay que reintentar** — que es control de concurrencia
optimista, y es lo que permite escalar sin bloqueos largos.

Y esta clase debe cerrar con la observación que las tres formas dejan clara: **el eje real de la
persistencia no es el formato, es la granularidad de la garantía**.

```text
Imagen:     todo o nada, y solo cuando alguien la guarda.
Serializar: un grafo, con la durabilidad que el programa implemente.
GemStone / base de datos: una transacción, garantizada por el sistema.
```

**Y elegir es decidir qué se puede perder**: en un editor, el trabajo desde el último guardado; en un
sistema de pagos, nada.

Es la pregunta que el gancho de esta clase planteaba —**¿qué pasa si el proceso muere entre estas dos
líneas?**— y la respuesta correcta es siempre la misma: **depende de qué haya entre ellas**.
"""),
    },
)

# ---------------------------------------------------------------------------
# 173 — Pruebas de extremo a extremo
# ---------------------------------------------------------------------------
SPECS["173"] = dict(
    gancho="""
Comprobar el sistema entero con una entrada y una salida esperada: `e2e=pasa`. Es lo que hace el
verificador de este curso desde la clase 040, y lo que hacen las pruebas de extremo a extremo de
cualquier sistema. Y estos lenguajes aportan aquí la técnica más antigua y más eficaz que existe para
esto: **preparar unos ficheros de entrada, ejecutar el sistema y comparar la salida con una guardada** —
que es de los años sesenta y sigue siendo insuperable.
""",
    porque="""
Aquí el concepto es la **prueba del sistema completo**, y estos lenguajes la enseñan porque **sus
sistemas no se pueden probar de otra manera**: un lote de veinte pasos, una transacción que toca cuatro
programas y dos bases de datos, o un cálculo que corre en mil procesos. Y de ahí salieron las técnicas
que esta parte del curso ha ido nombrando: **la comparación de salidas** (clase 140), **la ejecución en
paralelo** y **Expect** para lo que no tiene API (clase 147).

Y aparece la tensión que define esta clase: **estas pruebas son las más valiosas y las más frágiles**.
""",
    cierre="""
Lo transferible: **una prueba de extremo a extremo comprueba lo que de verdad importa y falla por lo que
no**. De ahí las tres reglas que la hacen sostenible: **pocas y bien elegidas** —cubrir los caminos
críticos, no todos los casos, que ya están cubiertos abajo (clase 139)—; **con datos propios y
desechables**, porque una prueba que depende del estado que dejó otra falla de forma intermitente; y
**esperando por eventos, no por tiempos** (clase 171), que es la causa número uno de pruebas
intermitentes. Y la regla que sostiene todo: **una prueba que falla a veces y se reintenta hasta que pasa
ya no prueba nada** — y enseña al equipo a ignorar el rojo.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. E2E.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  C-A     PIC X(15).
01  C-B     PIC X(15).
01  C-E     PIC X(15).
01  A       PIC S9(9) COMP.
01  B       PIC S9(9) COMP.
01  ESPER   PIC S9(9) COMP.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-A C-B C-E
    END-UNSTRING

    COMPUTE A     = FUNCTION NUMVAL(C-A)
    COMPUTE B     = FUNCTION NUMVAL(C-B)
    COMPUTE ESPER = FUNCTION NUMVAL(C-E)

    IF A + B = ESPER
        DISPLAY "e2e=pasa"
    ELSE
        DISPLAY "e2e=falla"
    END-IF
    STOP RUN.
""", """
**COBOL y las pruebas de extremo a extremo.** El mundo del lote inventó la técnica del gancho, y merece
verla completa porque es más elaborada de lo que parece:

```jcl
//PRUEBA JOB
//COPIAR  EXEC PGM=IEBGENER          <-- preparar los datos de entrada conocidos
//SISUT1   DD DSN=PRUEBA.ENTRADA.CASO01,DISP=SHR
//SISUT2   DD DSN=&&ENTRADA,DISP=(NEW,PASS)
//EJECUTA EXEC PROC=MIPROCESO         <-- ejecutar el sistema completo
//COMPARA EXEC PGM=ISRSUPC            <-- comparar la salida con la esperada
//NEWDD    DD DSN=&&SALIDA,DISP=SHR
//OLDDD    DD DSN=PRUEBA.ESPERADA.CASO01,DISP=SHR
//OUTDD    DD SYSOUT=*
```

**`ISRSUPC` —SuperC— es el comparador de IBM**, y es lo que hace esta técnica práctica, porque tiene una
capacidad que un `diff` normal no tiene:

```text
CMPCOLM 1:60,80:100      <-- comparar SOLO estas columnas
DPLINE '2026-'            <-- IGNORAR las líneas que contengan una fecha
```

**Poder excluir columnas y líneas es lo que hace usable la comparación de salidas**, porque **toda salida
real contiene cosas que cambian en cada ejecución**: fechas, horas, números de trabajo, contadores.

Es exactamente lo que `Test::Deep` con `ignore()` hace en Perl (clase 140), con cuarenta años de
adelanto.

Y merece señalar la segunda regla del cierre aplicada a este mundo, porque es donde falla: **los datos de
prueba**.

```text
✗ Ejecutar la prueba contra la base de datos de desarrollo compartida.
   → otro equipo cambia un cliente y la prueba falla mañana.

✓ Cada caso restaura sus propias tablas antes de ejecutarse,
   desde un juego de datos versionado.
```

**Y esa restauración es lo que hace que las pruebas de lote sean reproducibles**, y es la práctica
estándar en los sistemas serios: **juegos de datos de prueba tratados como código** (clase 145),
versionados y con dueño.
"""),
        "fortran": ("""
program e2e
   implicit none
   integer :: a, b, esperado

   read(*, *) a, b, esperado

   if (a + b == esperado) then
      write(*, '(A)') 'e2e=pasa'
   else
      write(*, '(A)') 'e2e=falla'
   end if
end program e2e
""", """
**Fortran y las pruebas de extremo a extremo.** El cálculo científico tiene la versión más difícil de esta
clase, y ya apareció en la clase 140: **la salida nunca es idéntica**.

```text
Comparar dos ejecuciones de una simulación:
  - con distinto compilador → el último dígito cambia
  - con distinto número de procesos → el orden de las sumas cambia
  - con la misma máquina y la misma versión → normalmente sí coincide
```

**Así que la comparación byte a byte no sirve**, y la técnica de este dominio es de tres niveles y merece
verla porque es un buen modelo:

**Nivel 1 — pruebas de regresión con tolerancia:**

```text
Caso pequeño, resultado guardado, y comparación con tolerancia RELATIVA
justificada por el análisis del error (clase 140), no por lo que hizo falta.
```

**Nivel 2 — magnitudes conservadas:**

```fortran
! La masa total, la energía y el momento DEBEN conservarse
if (abs(masa_final - masa_inicial) / masa_inicial > 1e-12_dp) error stop
```

**Esas comprobaciones no dependen del valor exacto**, así que **son robustas frente al compilador y al
paralelismo** — y detectan la mayoría de los errores reales.

**Nivel 3 — soluciones analíticas:**

```text
Para unos pocos casos existe la solución exacta (una onda plana, un flujo laminar).
Comparar contra ella verifica el MÉTODO, no solo la ausencia de cambios.
```

**Y la diferencia entre el nivel 1 y el nivel 3 es la de esta clase**: **el nivel 1 detecta que algo
cambió; el nivel 3 detecta que algo está mal**.

Y merece cerrar con la práctica que este dominio ha adoptado y que es la primera regla del cierre: **la
pirámide de casos**.

```text
En cada cambio:      casos de segundos, con 2 procesos
Cada noche:           casos de minutos, con varias combinaciones
Antes de publicar:     el caso de producción, en el clúster (clase 147)
```

**Y lo importante es que el nivel de arriba exista y se ejecute alguna vez**, porque **es el único que
prueba lo que de verdad se usa** — y muchos proyectos se quedan solo en el primero.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure E2e is
   A, B, Esperado : Integer;
begin
   Get (A);
   Get (B);
   Get (Esperado);

   if A + B = Esperado then
      Put_Line ("e2e=pasa");
   else
      Put_Line ("e2e=falla");
   end if;
end E2e;
""", """
**Ada y las pruebas de extremo a extremo.** En los dominios de Ada, esta clase tiene un nombre formal y un
peso enorme: **la verificación del sistema integrado**.

```text
Niveles de prueba en un proyecto certificado:
  1. Unitaria         → cada subprograma, con cobertura MC/DC (clase 139)
  2. Integración      → los componentes entre sí
  3. Hardware-software → el software sobre el hardware REAL
  4. Sistema          → el equipo completo, en banco de pruebas
  5. Y vuelo o campo   → el sistema en su entorno
```

**Y cada nivel tiene sus requisitos trazados** (clase 166): **cada requisito de alto nivel se verifica en
el nivel que le corresponde**, y una herramienta comprueba que no falte ninguno.

Y este dominio aporta a esta clase la técnica que hace posible probar lo que no se puede ejecutar de
verdad, y merece explicarla: **la prueba con hardware simulado en el bucle**.

```text
El sistema real ejecuta su software, y en lugar de sensores y actuadores
tiene conectado un SIMULADOR que:
  - le da lecturas de sensor como si volara
  - recibe sus órdenes de actuador
  - y simula la física del vehículo en tiempo real
```

**Y así se prueban situaciones que no se pueden provocar de verdad**: un fallo de motor, una ráfaga
extrema, un sensor que miente.

Es la versión física de los objetos simulados de la clase 139, y su valor es el mismo: **poder ejercitar
los caminos de error**.

Y merece señalar la propiedad que la tercera regla del cierre pide y que este mundo consigue mejor que
nadie: **el determinismo**.

```text
Con Ravenscar (clase 146) y sin reserva dinámica,
el sistema es determinista: la misma entrada da la misma secuencia de ejecución.

Y eso hace que una prueba que falla se pueda REPRODUCIR.
```

**Una prueba de extremo a extremo reproducible es una herramienta; una intermitente es un impuesto** — y
la diferencia, en gran parte, viene de las decisiones de diseño de la clase 135, no de la prueba.
"""),
        "pascal": ("""
program E2e;
{$MODE OBJFPC}{$H+}

var
  A, B, Esperado: Integer;

begin
  Read(A, B, Esperado);

  if A + B = Esperado then
    WriteLn('e2e=pasa')
  else
    WriteLn('e2e=falla');
end.
""", """
**Pascal y las pruebas de extremo a extremo.** El ecosistema Delphi tiene el problema de esta clase en su
forma clásica: **probar una aplicación de escritorio con interfaz gráfica**.

```pascal
{ Automatización de la interfaz: TestComplete, Ranorex, o la API de Windows }
FindWindow('TForm1', 'Mi aplicación');
SendMessage(Handle, WM_COMMAND, ...);
```

**Y merece decir con franqueza que esas pruebas son las más frágiles que existen**: dependen de
posiciones, de nombres de control, de la velocidad de la máquina y del tema visual.

Y la lección de esta clase, que vale para cualquier interfaz gráfica o web, es la primera regla del
cierre: **pocas y bien elegidas**.

```text
✗ Probar cada formulario y cada validación por la interfaz.
   → miles de pruebas lentas y frágiles.

✓ Probar la LÓGICA por debajo (clase 139),
   y por la interfaz solo unos pocos caminos completos:
   "entrar, crear un pedido, cobrarlo, imprimir el ticket".
```

**Y para que eso sea posible, la lógica tiene que estar separada de la interfaz** (clase 149) — que es,
otra vez, buena arquitectura y comprobabilidad siendo lo mismo.

Y el ecosistema tiene una técnica que merece nombrarse y que resuelve la segunda regla del cierre: **la
base de datos en memoria o en fichero temporal**.

```pascal
{ Cada prueba arranca con su propia base, creada desde un guion }
FDConnection.Params.Database := TempDir + 'prueba_' + GUID + '.fdb';
EjecutarGuion('esquema.sql');
EjecutarGuion('datos_de_prueba.sql');
```

**Una base por prueba, creada y destruida**, elimina de golpe las pruebas intermitentes por estado
compartido — y con SQLite o Firebird embebido cuesta milisegundos.

Es la aplicación más directa de "datos propios y desechables", y merece señalar que **la mayoría de los
equipos que sufren pruebas intermitentes no han probado esto**.
"""),
        "lisp": ("""
(let ((a (read))
      (b (read))
      (esperado (read)))
  (format t "e2e=~A~%" (if (= (+ a b) esperado) "pasa" "falla")))
""", """
**Lisp y las pruebas de extremo a extremo.** Lisp aporta a esta clase una técnica que su modelo hace fácil
y que merece destacarse porque ataca la fragilidad del cierre: **grabar y reproducir**.

```lisp
;; Envolver una función para GRABAR sus llamadas y sus resultados en producción
(defun grabar (nombre fn)
  (lambda (&rest args)
    (let ((r (apply fn args)))
      (push (list nombre args r) *grabacion*)
      r)))

;; Y luego reproducir: la misma secuencia, sin el sistema externo
```

**Grabar las interacciones reales con los sistemas externos y reproducirlas** convierte una prueba de
extremo a extremo —lenta, dependiente de la red y frágil— **en una prueba rápida y determinista**.

Es la técnica que en otros ecosistemas se llama *VCR* o *cassettes*, y que Lisp permite montar en veinte
líneas porque **redefinir una función es una operación normal** (clase 139).

Y la advertencia que va con ella y merece decirse: **una prueba con grabación deja de detectar cambios en
el sistema externo**.

**Así que hacen falta las dos**: la mayoría con grabación —rápidas y estables— y **unas pocas contra el
sistema real**, ejecutadas menos veces (clase 147).

Y el ecosistema para esta clase:

```lisp
(asdf:test-system "mi-sistema")
(uiop:run-program (list "./servicio" "--puerto" "8080") :wait nil)
(dex:get "http://localhost:8080/pedidos/1")
```

**`uiop:run-program` con `:wait nil` lanza el sistema en segundo plano**, y el guion de prueba puede
esperar, ejercitar y parar — que es el patrón de la clase 165.

Y merece cerrar con la aportación de Lisp que la Parte 8 hace posible y que en esta clase es muy valiosa:
**cuando una prueba de extremo a extremo falla, se puede entrar**.

```lisp
;; La prueba falla → el depurador se abre CON el estado vivo (clase 141)
;; y se puede inspeccionar el sistema entero en el punto del fallo
```

**Diagnosticar un fallo de una prueba de sistema sin reproducirlo a mano** es lo que más tiempo ahorra en
esta clase, y es exactamente lo que un depurador sobre el proceso vivo permite.
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] a b esperado

puts "e2e=[expr {$a + $b == $esperado ? {pasa} : {falla}}]"
""", """
**Tcl y las pruebas de extremo a extremo.** Este es **el componente de Tcl por excelencia** en esta parte
(clase 165), y merece juntar aquí la receta completa con las tres reglas del cierre.

```tcl
package require tcltest
namespace import ::tcltest::*

# 1. Datos propios y desechables (regla 2)
proc arrancarSistema {} {
    set ::dir [file tempdir]
    exec sqlite3 $::dir/prueba.db < esquema.sql
    set ::api [exec ./api --db $::dir/prueba.db --puerto 0 --puertofile $::dir/p &]
    esperarFichero $::dir/p -timeout 10          ;# 2. esperar EVENTOS (regla 3)
    set ::puerto [leerFichero $::dir/p]
}

proc pararSistema {} {
    exec kill $::api
    file delete -force $::dir
}

test flujo-completo-1.1 {crear un pedido y cobrarlo} -setup {
    arrancarSistema
} -body {
    set id [crearPedido $::puerto {items {A1 2}}]
    cobrar $::puerto $id
    dict get [consultar $::puerto $id] estado
} -cleanup {
    pararSistema
} -result {cobrado}

cleanupTests
```

**Y tres detalles de ese guion merecen destacarse porque son las decisiones que hacen la prueba
sostenible:**

**`--puerto 0` y un fichero con el puerto real.** **Pedir un puerto fijo es la causa clásica de pruebas
que fallan al ejecutarse en paralelo** (clase 147): **que el sistema elija y lo publique** permite
ejecutar veinte a la vez.

**`esperarFichero` en lugar de dormir** (clase 171). **Nunca `after 3000`**.

**Y `-cleanup` que se ejecuta siempre**, incluso si el cuerpo falla — que es la propiedad que evita que
una prueba rota deje procesos y directorios por todas partes.

Y Tcl aporta lo que la clase 147 ya señaló y que aquí es la herramienta para lo que no tiene API:
**Expect**.

**Probar de extremo a extremo una aplicación de terminal, un instalador o un equipo de red** es algo que
solo Expect hace bien, y sigue siendo la respuesta treinta y cinco años después.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1, $esperado) = split ' ', $linea;

print "e2e=", ($a1 + $b1 == $esperado ? 'pasa' : 'falla'), "\\n";
""", """
**Perl y las pruebas de extremo a extremo.** Perl tiene el ecosistema más completo de esta página para
esta clase, y merece verlo porque cubre las tres reglas del cierre:

```perl
use Test::More;
use Test::TCP;              # ← puerto libre y arranque de servidor
use Test::PostgreSQL;        # ← ¡una base de datos temporal por prueba!
use Test::Deep;               # comparación con comodines (clase 140)

my $pg = Test::PostgreSQL->new;               # arranca su propio PostgreSQL
test_tcp(
    server => sub {
        my $puerto = shift;
        exec './api', '--dsn', $pg->dsn, '--puerto', $puerto;
    },
    client => sub {
        my $puerto = shift;
        my $r = pedir("http://127.0.0.1:$puerto/pedidos", {items => 2});
        cmp_deeply($r, {
            id     => ignore(),                # cambia en cada ejecución
            creado => re(qr/^\\d{4}-/),
            total  => num(24.20, 0.01),
        }, 'el pedido creado cumple el contrato');
    },
);
done_testing();
```

**`Test::PostgreSQL` merece destacarse** porque resuelve la segunda regla del cierre de la forma más
limpia: **arranca una instancia de PostgreSQL propia, en un directorio temporal, y la destruye al
terminar**.

**Cada prueba tiene su base de datos entera, aislada**, y **se pueden ejecutar en paralelo sin
coordinación**.

Es una idea excelente y sorprendentemente poco usada: **el coste de arrancar una base vacía es de
segundos, y el de depurar pruebas que se pisan es de días**.

**Y `Test::TCP`** resuelve el problema del puerto igual que Tcl en esta página: **busca uno libre y se lo
pasa al servidor**.

Y merece cerrar con la observación que la clase 147 anticipó y que en esta clase es la regla que sostiene
todo: **una prueba intermitente hay que arreglarla o borrarla**.

```perl
# ✗ lo que NO hay que hacer, y todo el mundo acaba haciendo
$ENV{REINTENTOS} = 3;
```

**Reintentar hasta que pase convierte la suite en un generador de ruido**, y a partir de ahí **nadie mira
el rojo** — que es exactamente lo que la integración continua existía para evitar.

Y la causa suele ser una de tres: **espera por tiempo, estado compartido, o dependencia del orden**. Las
tres tienen solución conocida, y ninguna es el reintento.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long a{}, b{}, esperado{};
    if (!(std::cin >> a >> b >> esperado)) return 1;

    std::cout << "e2e=" << (a + b == esperado ? "pasa" : "falla") << '\\n';
    return 0;
}
""", """
**C++ y las pruebas de extremo a extremo.** C++ aporta a esta clase una técnica que la clase 141 nombró y
que aquí es la respuesta al problema más difícil: **el fallo que solo ocurre a veces**.

```bash
rr record ./sistema_completo --caso 42
# ...falla una vez de cada cincuenta...
rr replay                       # ← la MISMA ejecución, exactamente
```

**`rr` graba una ejecución completa y la reproduce de forma determinista**, incluidas las condiciones de
carrera.

**Y eso convierte una prueba intermitente en un fallo reproducible** — que es la diferencia entre poder
arreglarlo y no poder.

Es la mejor herramienta que existe para la tensión del "por qué" de esta clase, y merece conocerse aunque
solo se use dos veces al año.

Y las otras técnicas de C++ para esta clase, ordenadas por lo que cazan:

| Técnica | Qué caza |
|---|---|
| **ThreadSanitizer en la prueba de sistema** | carreras que se manifiestan una vez de cada mil (clase 136) |
| **AddressSanitizer** | corrupción de memoria bajo carga real |
| **Fuzzing con `libFuzzer`** | entradas que nadie pensó |
| **Pruebas basadas en propiedades** | invariantes, con casos generados (clase 140) |
| **`rr`** | reproducir lo irreproducible |

**El fuzzing merece la mención** porque en un sistema que procesa entradas externas es la prueba de
extremo a extremo más rentable que existe:

```bash
./api_fuzzer corpus/ -max_total_time=3600
```

**Se generan millones de entradas aleatorias y mutadas, guiadas por cobertura**, y **cada caída se guarda
como caso de prueba reproducible**.

**Y encuentra cosas que ninguna persona escribiría**: cadenas vacías, números en los límites, secuencias
UTF-8 inválidas, anidamientos de mil niveles.

Y para el proyecto de esta parte, la recomendación concreta es la primera regla del cierre aplicada con
criterio: **pocas pruebas de extremo a extremo, y en cambio fuzzing continuo sobre las fronteras** —
porque es donde llegan los datos hostiles (clase 153) y donde una persona escribiendo casos nunca va a
competir con una máquina.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi E2E;
  a        int(10) const;
  b        int(10) const;
  esperado int(10) const;
end-pi;

if a + b = esperado;
  dsply 'e2e=pasa';
else;
  dsply 'e2e=falla';
endif;

*inlr = *on;
return;
""", """
**RPG y las pruebas de extremo a extremo.** IBM i tiene un mecanismo que resuelve la segunda regla del
cierre mejor que cualquier otra plataforma de esta página, y ya apareció en la clase 139: **la lista de
bibliotecas**.

```text
CRTLIB PRUEBA$$$
CRTDUPOBJ OBJ(*ALL) FROMLIB(PRODDATOS) OBJTYPE(*FILE) TOLIB(PRUEBA$$$) DATA(*YES)
CHGLIBL LIBL(PRUEBA$$$ MIAPP QGPL)
   ... ejecutar las pruebas ...
DLTLIB PRUEBA$$$
```

**Copiar el esquema y los datos a una biblioteca temporal y redirigir el trabajo hacia ella** da a cada
ejecución de pruebas **su propia copia completa de la base de datos**, sin tocar nada.

**Y es una operación del sistema, no de la aplicación**: los programas **no saben** que están usando otras
tablas.

Es inyección de dependencias a nivel de sistema operativo (clase 139), y resuelve de raíz la fuente número
uno de pruebas intermitentes.

Y las otras dos reglas del cierre tienen respuesta en la plataforma:

**Los datos deterministas**: `CRTDUPOBJ` desde un juego de datos versionado, y **el diario** (clase 172)
permite volver al estado inicial con `RMVJRNCHG` en lugar de recrear.

**Y el diagnóstico**: **si una prueba falla, el registro del trabajo tiene todo** (clase 142) — cada
mensaje, con su programa y su número de sentencia.

Y merece cerrar con la práctica de este mundo que la primera regla del cierre recomienda y que aquí es
natural: **probar por la interfaz de programa, no por la pantalla**.

```rpgle
// La prueba llama al procedimiento del programa de servicio,
// no simula pulsaciones en una pantalla 5250
aEqual(120.50 : calcularTotal(pedidoDePrueba) : 'total con IVA');
```

**Y para el flujo completo, un guion CL que encadena los programas** (clase 171) y compara los ficheros
resultantes con los esperados — que es, otra vez, la técnica de COBOL de esta página.
"""),
        "pli": ("""
 e2e: procedure options(main);

    declare (a, b, esperado) fixed binary(31);

    get list (a, b, esperado);

    if a + b = esperado then
       put skip list ('e2e=pasa');
    else
       put skip list ('e2e=falla');

 end e2e;
""", """
**PL/I y las pruebas de extremo a extremo.** PL/I aporta a esta clase la versión más ambiciosa que existe,
y la clase 140 ya la nombró: **la ejecución en paralelo**.

```text
Durante SEIS MESES:
  - el sistema viejo y el nuevo procesan las MISMAS entradas reales
  - solo el viejo tiene efectos
  - y un proceso compara TODAS las salidas, todos los días
  - cada discrepancia se investiga y se documenta
```

**Es una prueba de extremo a extremo con datos de producción reales, ejecutada millones de veces.**

Y merece explicar por qué se hace así y no con casos escritos, porque el argumento es fuerte: **nadie
puede escribir los casos que un sistema de treinta años ha visto**.

```text
Las discrepancias que aparecen son casi siempre:
  - clientes con configuraciones que ya no se dan de alta
  - contratos con excepciones aprobadas hace veinte años
  - casos que el sistema viejo maneja mal y de los que alguien depende
```

**Y ninguno de esos estaría en un juego de casos de prueba**, porque nadie sabe que existen.

Es la lección más importante de esta clase para cualquier reescritura: **los datos de producción son la
única especificación completa del sistema actual**.

Y la técnica que lo hace posible y que merece nombrarse: **la captura y reproducción de entradas**.

```text
Se instrumenta el sistema viejo para guardar cada entrada
—cada mensaje, cada fichero, cada petición—
y se reproduce contra el nuevo, fuera de línea.
```

**Y eso permite ejecutar seis meses de tráfico real en unas horas**, cuantas veces haga falta.

Y es la aportación de esta columna a la primera regla del cierre, con un matiz: **aquí las pruebas no son
pocas y bien elegidas — son todas las que ocurrieron**.

Y la razón es que **el objetivo no es comprobar que el sistema funciona, sino que es equivalente** (clase
140), y para eso **la cobertura de casos reales vale más que cualquier diseño de pruebas**.
"""),
        "mumps": ("""
E2E ; Prueba de extremo a extremo -- clase 173
 read linea
 new a, b, esperado
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set esperado = $piece(linea, " ", 3)
 write "e2e=", $select(a + b = esperado : "pasa", 1 : "falla"), !
 quit
""", """
**M y las pruebas de extremo a extremo.** M tiene, para esta clase, una capacidad que su modelo de datos
hace posible y que es más fuerte que comparar salidas: **comparar el estado de la base**.

```mumps
 ; 1. copiar el estado inicial a un espacio temporal
 merge ^||INICIAL = ^PACIENTE(dfn)

 ; 2. ejecutar el flujo completo
 do procesarAlta^ADT(dfn, datos)

 ; 3. y comparar el resultado con el esperado
 write $$comparar^UTIL($name(^PACIENTE(dfn)), $name(^ESPERADO(caso)))
```

**`merge` copia un subárbol entero de una global a otra en una operación** — que es la forma de M de
capturar un estado.

Y merece explicar por qué comparar el estado es mejor que comparar la salida, porque es la lección de esta
explicación y ya apareció en la clase 140:

```text
Comparar la SALIDA detecta lo que el sistema dijo.
Comparar el ESTADO detecta lo que el sistema HIZO.

Y un fallo típico —actualizar mal un índice, dejar un registro huérfano,
no borrar algo temporal— no se ve en la salida y sí en el estado.
```

**Y esa es la clase de fallo que aparece meses después**, cuando alguien consulta por ese índice.

Y las dos reglas del cierre que este dominio resuelve bien:

**Los datos propios**: `^||` da globals temporales privadas del proceso (clase 139), y **las
implementaciones modernas permiten regiones de base de datos desechables**.

**Y el determinismo**: la trampa clásica de este mundo es **la fecha**.

```mumps
 ; ✗ una prueba que usa DT (la fecha de hoy) falla el 1 de enero
 if $$edad^UTIL(fechaNac, DT) > 65 ...

 ; ✓ la fecha se INYECTA
 if $$edad^UTIL(fechaNac, fechaReferencia) > 65 ...
```

**Depender del reloj es la segunda causa de pruebas intermitentes**, después del estado compartido — y en
un dominio donde casi todo se calcula respecto a hoy, es un problema constante.

**Y la defensa es de diseño**: **el tiempo es un parámetro, no una variable global** — que es una de las
recomendaciones más rentables de toda esta parte del curso.
"""),
        "smalltalk": ("""
| linea partes a b esperado |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.
esperado := (partes at: 3) asNumber.

Transcript
    show: 'e2e=', (a + b = esperado ifTrue: [ 'pasa' ] ifFalse: [ 'falla' ]);
    cr.
""", """
**Smalltalk y las pruebas de extremo a extremo.** Smalltalk, que inventó las pruebas unitarias (clase
139), aporta a esta clase dos capacidades que vienen de su modelo.

**La primera: la imagen como estado de prueba.**

```smalltalk
"Preparar el sistema en un estado concreto y GUARDARLO"
self cargarDatosDePrueba.
Smalltalk snapshot: true andQuit: true.
```

**Una imagen con los datos ya cargados arranca en el estado exacto que la prueba necesita** — lo que
resuelve la segunda regla del cierre sin base de datos temporal ni guiones de carga.

Es la misma idea que una instantánea de contenedor (clase 174), disponible desde 1980.

**Y la segunda: el fallo se puede examinar entero.**

```smalltalk
[ self ejecutarFlujoCompleto ] on: Error do: [ :e |
    "Guardar el CONTEXTO del error para abrirlo después (clase 141)"
    FLSerializer serialize: e signalerContext toFileNamed: 'fallo.fuel' ]
```

**Y ese fichero se abre en el depurador en otra máquina**, con la pila viva y los objetos.

**Es la respuesta al problema más caro de esta clase**: una prueba de sistema que falla en la integración
continua y no se reproduce en local. Aquí **el fallo viaja**.

Y merece cerrar esta clase con la observación que Smalltalk permite hacer y que resume la parte: **las
pruebas de extremo a extremo son caras porque el sistema no se deja preguntar**.

```text
Si el sistema puede decir en qué estado está,
si el fallo se puede capturar entero,
y si el entorno se puede recrear exactamente,
entonces la prueba de extremo a extremo es barata y estable.

Y si no, se compensa con esperas, reintentos y capturas de pantalla.
```

**La fragilidad de estas pruebas es, casi siempre, un síntoma del sistema y no de la prueba** — y las
propiedades que las abaratan son las mismas que esta parte del curso viene defendiendo: **fronteras
claras, estado inspeccionable, entorno reproducible y tiempo inyectado**.
"""),
    },
)
