# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 148

> [⬅️ Volver a la clase 148](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Anunciar una versión desplegada: `desplegado=v1.2.3`. El programa es un eco; lo que esta clase compara es
**lo que ocurre justo antes y justo después de esa línea**. Y aquí están los dos extremos absolutos de la
ingeniería: **CICS sustituye un programa en un sistema con miles de usuarios conectados, sin cortar
nada, y lo hace desde 1969**; y **una sonda espacial se actualiza a cientos de millones de kilómetros,
sin posibilidad de volver atrás si sale mal**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **puesta en producción y la reversión**, y estos lenguajes lo enseñan porque
> **operan sistemas que no pueden pararse**: bancos, hospitales, fábricas, aviones y satélites. Así que
> resolvieron hace décadas lo que hoy se llama despliegue sin cortes, y con mecanismos que siguen siendo
> más simples que los actuales: **cambiar el orden de una lista de bibliotecas**, **copiar un miembro**,
> **escribir una rutina en la base de datos**.
>
> Y aparece la pregunta que ordena la página: **¿cuánto cuesta deshacer?** Porque un despliegue sin
> reversión no es un despliegue: es una apuesta.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con una versión `mayor.menor.parche` → stdout: `desplegado=v<versión>`
- **Regla:** `prefijar la versión con 'v'`

| stdin | esperado |
|---|---|
| `1.2.3` | `desplegado=v1.2.3` |
| `0.9.0` | `desplegado=v0.9.0` |
| `2.1.5` | `desplegado=v2.1.5` |

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
PROGRAM-ID. DESPLIEG.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).

PROCEDURE DIVISION.
    ACCEPT LINEA
    DISPLAY "desplegado=v" FUNCTION TRIM(LINEA)
    STOP RUN.
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program despliegue
   implicit none
   character(len=40) :: linea

   read(*, '(A)') linea

   write(*, '(A)') 'desplegado=v' // trim(adjustl(linea))
end program despliegue
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Despliegue is
   Linea  : String (1 .. 40);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   Put_Line ("desplegado=v" & Linea (1 .. Ultimo));
end Despliegue;
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Despliegue;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;

begin
  ReadLn(Linea);
  WriteLn('desplegado=v', Trim(Linea));
end.
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((linea (string-trim '(#\Space #\Return) (read-line))))
  (format t "desplegado=v~A~%" linea))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

puts "desplegado=v[string trim $linea]"
```

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
send "configure terminal\r"
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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $version = <STDIN>;
chomp $version;

print "desplegado=v$version\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string version;
    if (!std::getline(std::cin, version)) return 1;

    std::cout << "desplegado=v" << version << '\n';
    return 0;
}
```

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

dcl-pi DESPLIEG;
  version char(40) const;
end-pi;

dsply ('desplegado=v' + %trim(version));

*inlr = *on;
return;
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 despliegue: procedure options(main);

    declare linea char(40) varying;

    get edit (linea) (a(40));

    put skip list ('desplegado=v' || trim(linea));

 end despliegue;
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DESPLIEG ; Anuncio de despliegue -- clase 148
 read version
 write "desplegado=v", version, !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| version |

version := stdin nextLine trimBoth.

Transcript show: 'desplegado=v', version; cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **el valor de un despliegue se mide por lo rápido que se deshace**, no por lo elegante
que sea. De ahí las tres propiedades que aparecen en toda esta página: **la versión anterior sigue
existiendo** —no se sobrescribe, se deja al lado—; **el cambio de una a otra es una operación pequeña y
atómica**; y **hay una forma de comprobar que la nueva funciona antes de dirigirle todo el tráfico**. Y
la cuarta, que casi nadie planea: **los datos**. El código vuelve atrás en segundos; una migración de
esquema, no — y por eso los cambios de datos se hacen compatibles en las dos direcciones antes de tocar
el código.

⏮️ [Volver a la clase 148](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
