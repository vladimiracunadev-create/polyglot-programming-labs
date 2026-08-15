# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 171

> [⬅️ Volver a la clase 171](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Ejecutar N tareas y decir que terminaron: `tareas=5 estado=completado`. Es un orquestador reducido a lo
esencial, y esta clase trata del componente que ningún diagrama dibuja y sin el cual no funciona nada.
Y aquí hay una precedencia clara: **el JCL, de 1964, es un lenguaje de orquestación de trabajos con
dependencias, condiciones y asignación de recursos** — y lo que hoy hacen Airflow, Argo o GitHub Actions
tiene una forma sorprendentemente parecida.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **automatización como componente de primera clase**, y estos lenguajes la enseñan
> porque **tienen los lenguajes de orquestación más antiguos y más probados**: JCL en z/OS, CL en IBM i, y
> las herramientas que crecieron alrededor —Expect, Perl, Tcl— para automatizar lo que no tenía interfaz.
>
> Y aparece la propiedad que separa una automatización que aguanta de una que se rompe cada semana: **la
> idempotencia** — que ejecutarla dos veces dé el mismo resultado que ejecutarla una.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (número de tareas) → stdout: `tareas=<n> estado=completado`
- **Regla:** `procesar n tareas y confirmar`

| stdin | esperado |
|---|---|
| `5` | `tareas=5 estado=completado` |
| `0` | `tareas=0 estado=completado` |
| `3` | `tareas=3 estado=completado` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program automat
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A)') 'tareas=', n, ' estado=completado'
end program automat
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Automat;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('tareas=', IntToStr(N), ' estado=completado');
end.
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "tareas=~D estado=completado~%" n))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

puts "tareas=$n estado=completado"
```

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
    "password:"    { send "$::env(CLAVE)\r"; exp_continue }
    "$ "            { send "reiniciar servicio\r" }
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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "tareas=$n estado=completado\n";
```

**Perl y la automatización.** Perl fue **la herramienta de automatización de sistemas durante veinte
años**, y su ecosistema para este componente sigue siendo excelente:

```perl
use IPC::Run qw(run timeout);
use Try::Tiny;
use File::Temp qw(tempdir);
use Path::Tiny;

my $dir = tempdir(CLEANUP => 1);            # ← se borra solo al salir

try {
    run \@comando, \undef, \my $salida, \my $error, timeout(300)
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
GetOptions('dry-run' => \my $simular);
...
if ($simular) { say "haría: borrar $ruta" } else { unlink $ruta }
```

**El modo de simulación es la característica más valiosa de una herramienta de automatización**, y la que
permite revisar un cambio grande antes de ejecutarlo.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "tareas=" << n << " estado=completado" << '\n';
    return 0;
}
```

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

dcl-pi AUTOMAT;
  n int(10) const;
end-pi;

dsply ('tareas=' + %char(n) + ' estado=completado');

*inlr = *on;
return;
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 automat: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('tareas=' || trim(char(n)) || ' estado=completado');

 end automat;
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
AUTOMAT ; Componente de automatizacion -- clase 171
 read n
 write "tareas=", n, " estado=completado", !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'tareas=', n printString, ' estado=completado'; cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **una automatización que no se puede volver a ejecutar sin miedo no está terminada**. De
ahí las tres propiedades que hay que buscar: **idempotencia**, para poder reintentar; **reanudabilidad**,
para no repetir lo caro cuando falla el paso siete; y **registro de lo que hizo**, porque una
automatización silenciosa es imposible de diagnosticar (clase 142). Y la advertencia que más caro sale
ignorar: **el código de automatización es código de producción** — se versiona, se revisa y se prueba,
porque es lo que despliega, borra y mueve datos.

⏮️ [Volver a la clase 171](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
