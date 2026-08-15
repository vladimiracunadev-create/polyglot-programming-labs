# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 174

> [⬅️ Volver a la clase 174](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Nombrar una imagen: `imagen=app:1.2.3`. Un nombre y una etiqueta, que es como se identifica hoy una
unidad desplegable. Y esta página tiene las tres respuestas históricas a la misma pregunta —**¿qué es
exactamente lo que se despliega?**—: **un módulo de carga en una biblioteca** (COBOL y PL/I), **un fichero
de salvado con objetos completos** (RPG), y **una imagen con todo el sistema dentro** (Lisp y Smalltalk)
— esta última, cuarenta años antes de que se llamara así.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **unidad de despliegue**, y estos lenguajes la enseñan porque **cubren todo el
> rango de tamaños**: desde un binario estático de 200 KB (Pascal, Ada, C++) hasta una imagen de 200 MB
> (Lisp, Smalltalk), pasando por los que necesitan un intérprete y los que necesitan una plataforma
> entera.
>
> Y aparece la decisión que decide el coste operativo: **qué se mete dentro del artefacto y qué se espera
> encontrar fuera**. Cuanto más dentro, más grande y más autónomo; cuanto más fuera, más ligero y más
> frágil.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con una versión `mayor.menor.parche` → stdout: `imagen=app:<versión>`
- **Regla:** `construir el nombre de imagen app:version`

| stdin | esperado |
|---|---|
| `1.2.3` | `imagen=app:1.2.3` |
| `0.9.0` | `imagen=app:0.9.0` |
| `2.1.5` | `imagen=app:2.1.5` |

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
PROGRAM-ID. IMAGEN.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  VERSION PIC X(20).

PROCEDURE DIVISION.
    ACCEPT VERSION
    DISPLAY "imagen=app:" FUNCTION TRIM(VERSION)
    STOP RUN.
```

**COBOL y el empaquetado.** La unidad de despliegue del mainframe es **el módulo de carga en una
biblioteca particionada** (clase 144), y merece compararla con una imagen de contenedor porque los
paralelismos son exactos:

| Mainframe | Contenedores |
|---|---|
| **Módulo de carga** | el binario dentro de la imagen |
| **Biblioteca particionada (PDS)** | el registro de imágenes |
| **Grupos de datos generacionales** | las etiquetas de versión (clase 144) |
| **`STEPLIB` concatenado** | el orden de búsqueda |
| **`IEBCOPY` entre bibliotecas** | `docker push` / `pull` |
| **`IDENTIFY` con metadatos** | las etiquetas OCI de la imagen |

**Y la diferencia real está en una sola fila que no aparece ahí: el entorno.**

```text
Un módulo de carga NO lleva su entorno dentro.
Espera encontrar en el destino:
  - la versión correcta del Language Environment
  - las bibliotecas de DB2 y de CICS
  - los ficheros catalogados
  - y la configuración de la región
```

**Y por eso el despliegue del mainframe exige entornos iguales**, mientras que una imagen de contenedor
lleva sus dependencias dentro.

Es exactamente la regla del cierre de esta clase, y explica por qué los contenedores resolvieron un
problema que estos sistemas resolvían con disciplina operativa.

Y hoy, GnuCOBOL sí se empaqueta como cualquier cosa:

```dockerfile
FROM debian:12-slim AS construccion
RUN apt-get update && apt-get install -y gnucobol4
COPY src/ /src/
RUN cobc -x -free -O2 -o /app /src/programa.cob

FROM gcr.io/distroless/base-debian12
COPY --from=construccion /app /app
COPY --from=construccion /usr/lib/x86_64-linux-gnu/libcob.so.4 /usr/lib/
ENTRYPOINT ["/app"]
```

**Construcción en dos etapas** —la segunda práctica del cierre—: **el compilador se queda en la primera
imagen y no viaja**.

Y merece señalar el resultado: **una imagen de pocos megabytes con un programa COBOL dentro**, que se
despliega igual que cualquier otro servicio. Es lo que hace posible que la lógica de negocio validada
participe de una arquitectura moderna sin reescribirse (clase 164).

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program imagen
   implicit none
   character(len=20) :: version

   read(*, '(A)') version

   write(*, '(A)') 'imagen=app:' // trim(adjustl(version))
end program imagen
```

**Fortran y el empaquetado.** El cálculo científico tiene el problema de empaquetado más difícil de esta
página, y ya apareció en la clase 143: **el binario depende del compilador, de las bibliotecas y de la
arquitectura exacta**.

```text
Un ejecutable compilado con ifort 2021 + MKL + Intel MPI
NO funciona en un nodo con gfortran + OpenBLAS + OpenMPI.

Y con -march=native, ni siquiera en otro procesador (clase 144).
```

Y las tres soluciones que la comunidad usa merecen compararse porque cubren el eje del "por qué":

| Solución | Qué mete dentro |
|---|---|
| **Módulos de entorno** (clase 148) | **nada**: el entorno está en el clúster |
| **Spack** | compila todo, con un identificador por configuración |
| **Contenedores (Apptainer/Singularity)** | **el sistema operativo entero y las bibliotecas** |

**Y Apptainer merece la mención** porque es el contenedor del mundo científico y su diseño difiere de
Docker en cosas que importan aquí:

```text
- La imagen es UN FICHERO (.sif), no capas en un registro:
     se copia al clúster como cualquier otro dato
- Se ejecuta SIN privilegios de administrador:
     imprescindible en un superordenador compartido
- El usuario dentro es el mismo que fuera:
     los ficheros generados tienen el propietario correcto
- Y puede usar el MPI y la GPU del anfitrión
```

**La última fila es la que hace todo esto viable y merece explicarla**: **un contenedor completamente
aislado no puede usar la red de baja latencia del clúster ni las GPU**, así que **Apptainer deja pasar
esos recursos**.

Es la regla del cierre matizada por el dominio: **se mete dentro todo lo que no está garantizado, salvo lo
que es del hardware y no se puede llevar**.

Y merece cerrar con lo que esto resuelve y que la clase 154 llamaba la deuda de reproducibilidad:
**publicar el contenedor junto al artículo** hace que un resultado se pueda reproducir dentro de diez
años.

**Es la práctica que la comunidad está adoptando**, y es la aplicación más clara de la tercera regla del
cierre de esta clase.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Imagen is
   Linea  : String (1 .. 20);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   Put_Line ("imagen=app:" & Linea (1 .. Ultimo));
end Imagen;
```

**Ada y el empaquetado.** Ada produce binarios estáticos pequeños, así que el empaquetado es directo — y
esta clase es el sitio para el requisito de su dominio, que es más estricto que cualquier contenedor:
**el archivo del proyecto completo**.

```text
Lo que se archiva de un sistema certificado, por ley y por contrato:
  - el fuente, con su versión exacta
  - el compilador y todas las herramientas, en su versión exacta
  - la máquina de construcción, a veces como imagen de disco
  - los informes de análisis, cobertura y demostración (clase 147)
  - la trazabilidad requisito-código-prueba (clase 166)
  - y el binario resultante, con su suma de comprobación
```

**Y todo eso hay que conservarlo durante la vida operativa del producto** — que en un avión son **treinta
o cuarenta años**.

Y merece señalar el problema real que eso plantea y que las herramientas modernas empeoran: **¿cómo se
conserva una cadena de herramientas durante cuarenta años?**

```text
El compilador de 2026 no existirá como paquete instalable en 2060.
El sistema operativo tampoco.
Y el hardware, menos.
```

**Y la respuesta de esta clase es la de la regla del cierre llevada al extremo**: **archivar la imagen del
entorno completo**, y hoy eso significa **un contenedor o una máquina virtual con todo dentro**.

Es uno de los usos menos glamurosos y más valiosos de los contenedores: **congelar un entorno de
construcción para poder volver a él**.

Y para el despliegue en sí, Ada da lo que la clase 167 señalaba:

```bash
gnatmake -O2 -largs -static      # binario estático
ldd servicio                      # sin dependencias dinámicas
```

```dockerfile
FROM scratch
COPY servicio /servicio
ENTRYPOINT ["/servicio"]
```

**`FROM scratch` con un binario estático da una imagen que contiene exactamente un fichero** — que es el
límite inferior de la primera práctica del cierre y una superficie de ataque mínima (clase 153).

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Imagen;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Version: string;

begin
  ReadLn(Version);
  WriteLn('imagen=app:', Trim(Version));
end.
```

**Pascal y el empaquetado.** Free Pascal está en el mejor punto de esta página para esta clase, y merece
darlo con números:

```bash
fpc -O2 -XX -Xs servicio.pas     # -XX enlace inteligente, -Xs sin símbolos
ls -lh servicio                   # ~300 KB - 2 MB
ldd servicio                       # solo libc
```

```dockerfile
FROM alpine:3.20
COPY servicio /servicio
ENTRYPOINT ["/servicio"]
# → imagen total: unos 8 MB
```

**Y ese tamaño tiene consecuencias operativas concretas** que merecen enumerarse, porque suelen
subestimarse:

| Consecuencia | Detalle |
|---|---|
| **Despliegue rápido** | descargar 8 MB frente a 400 |
| **Arranque instantáneo** | escalar a cero y volver es viable |
| **Superficie de ataque mínima** | menos software, menos vulnerabilidades (clase 153) |
| **Y menos coste** | almacenamiento y tráfico del registro de imágenes |

**La tercera merece el detalle**, porque es la razón por la que las imágenes mínimas se han impuesto: **una
imagen basada en una distribución completa contiene cientos de paquetes que la aplicación no usa**, y
**cada uno puede tener una vulnerabilidad que un escáner reportará y alguien tendrá que atender**.

**Una imagen con un binario y nada más no tiene ese problema.**

Y la compilación cruzada de Free Pascal (clase 147) cierra el cuadro:

```bash
fpc -Tlinux -Px86_64 servicio.pas
fpc -Tlinux -Paarch64 servicio.pas    # ← ARM, desde la misma máquina
```

**Producir las imágenes para varias arquitecturas desde un solo corredor**, sin emulación ni cadenas
cruzadas — que es lo que hoy cuesta trabajo montar en la mayoría de los ecosistemas.

Y merece cerrar con la advertencia de la clase 144 aplicada aquí: **si el binario lleva la fecha de
compilación dentro** —con `{$I %DATE%}`— **la imagen no será reproducible**.

**La versión debe venir del control de versiones, no del reloj.**

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((version (string-trim '(#\Space #\Return) (read-line))))
  (format t "imagen=app:~A~%" version))
```

**Lisp y el empaquetado.** Aquí está una de las tres respuestas del gancho, y merece verla con perspectiva:
**Lisp lleva desplegando "imágenes" desde los años setenta**.

```lisp
(sb-ext:save-lisp-and-die "servicio"
                          :executable t
                          :toplevel #'main
                          :compression t)
```

**Y el paralelismo con una imagen de contenedor es notable**:

| Imagen de Lisp | Imagen de contenedor |
|---|---|
| Todo el sistema dentro | todo el sistema de ficheros dentro |
| Arranca en el estado guardado | arranca desde el estado de la imagen |
| Decenas o cientos de MB | ídem |
| Opaca: lo que hay es lo que había | ídem, salvo por las capas |
| **Y se construye desde una base + un guion** | ídem: `FROM` + instrucciones |

**Y la última fila es la práctica correcta en los dos casos** (clase 144): **construir desde una base
limpia con un guion**, no guardar la sesión de trabajo.

```bash
sbcl --non-interactive --load construir.lisp
```

```dockerfile
FROM clfoundation/sbcl:2.4 AS construccion
COPY . /src
WORKDIR /src
RUN sbcl --non-interactive --load construir.lisp

FROM debian:12-slim
COPY --from=construccion /src/servicio /servicio
ENTRYPOINT ["/servicio"]
```

**Construcción en dos etapas** —la segunda práctica del cierre— **con SBCL en la primera y solo el
ejecutable en la segunda**.

Y merece señalar la ventaja que Lisp aporta y que ningún contenedor da: **se puede precalcular estado**.

```lisp
(cargar-tablas-de-referencia)     ; leer, indexar, calentar cachés
(sb-ext:save-lisp-and-die "servicio" :executable t)
```

**El proceso desplegado arranca con las tablas ya construidas**, en milisegundos — cosa que en otros
lenguajes exige hacerlo en cada arranque.

Es una forma de "compilación anticipada del estado", y es la razón por la que un servicio Lisp puede tener
un arranque instantáneo con estructuras que tardarían minutos en montarse.

Y el coste, que es la regla del cierre: **la imagen incluye el compilador y el depurador** — potentísimo
en producción (clase 148) y **superficie de ataque** si el servicio está expuesto (clase 153).

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin version

puts "imagen=app:[string trim $version]"
```

**Tcl y el empaquetado.** Tcl tiene la respuesta de la clase 144 y merece verla aquí como lo que es: **un
contenedor de aplicación, veinte años antes**.

```bash
sdx wrap servicio.exe -runtime tclkit-linux-x86_64
```

**Y lo que produce un Starpack es**:

```text
Un ÚNICO fichero ejecutable que contiene:
  - el intérprete de Tcl
  - todos los paquetes que usa
  - los datos, plantillas e imágenes
  - y un sistema de ficheros virtual que los monta al arrancar
```

**Y el paralelismo con un contenedor es directo**: **el artefacto lleva dentro todo lo que no está
garantizado fuera** — que es la regla del cierre de esta clase.

Y merece la comparación honesta:

| | Starpack (2002) | Contenedor (2013) |
|---|---|---|
| Autocontenido | **sí** | sí |
| Tamaño | **5-20 MB** | 20-500 MB |
| Aislamiento | **ninguno** | procesos, red, ficheros |
| Límites de recursos | ninguno | sí |
| Multiplataforma | **un fichero por plataforma** | ídem, por arquitectura |
| Ecosistema | pequeño | **enorme** |

**Y las filas del aislamiento son las que explican por qué ganaron los contenedores**: **no resolvían el
empaquetado —eso ya estaba resuelto de varias formas— sino el aislamiento y los límites**.

Es una observación que merece extraerse porque se malinterpreta a menudo: **la aportación de los
contenedores no es meter cosas en un fichero, es que el sistema operativo garantice qué puede hacer ese
proceso** — que es el modelo de capacidades de las clases 153 y 162.

Y hoy Tcl se empaqueta de las dos maneras:

```dockerfile
FROM alpine:3.20
RUN apk add --no-cache tcl
COPY app/ /app/
ENTRYPOINT ["tclsh", "/app/servicio.tcl"]
```

**O con un Starpack dentro de una imagen `scratch`**, que da las dos propiedades a la vez: **un fichero y
aislamiento**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $version = <STDIN>;
chomp $version;

print "imagen=app:$version\n";
```

**Perl y el empaquetado.** Perl tiene el problema que la clase 143 explicó —**los módulos binarios están
atados a la construcción exacta del intérprete**— y la solución que la clase 148 nombró:

```dockerfile
FROM perl:5.38 AS construccion
COPY cpanfile cpanfile.snapshot /app/
WORKDIR /app
RUN cpanm --installdeps --notest .          # ← desde el FICHERO DE BLOQUEO
COPY . /app

FROM perl:5.38-slim
COPY --from=construccion /app /app
WORKDIR /app
CMD ["perl", "servicio.pl"]
```

**Y `cpanfile.snapshot` es la pieza que hace la imagen reproducible** (clase 143): **las mismas versiones
exactas, con sus sumas de comprobación**, en lugar de "lo que hubiera en CPAN ese día".

Es la tercera práctica del cierre, y merece subrayar que **sin fichero de bloqueo, dos construcciones de
la misma etiqueta producen imágenes distintas** — que es la irreproducibilidad de la clase 144 en su forma
más común y menos vigilada.

Y merece señalar la primera práctica del cierre, que en el ecosistema de contenedores tiene nombre
propio: **etiquetar por contenido**.

```bash
docker pull miapp:1.2.3                                  # ← una etiqueta se puede REESCRIBIR
docker pull miapp@sha256:3f2a...                          # ← esto identifica UN contenido
```

**Una etiqueta es un puntero mutable; el resumen es la identidad.** Y desplegar por etiqueta significa que
**dos despliegues de "1.2.3" pueden ser cosas distintas** si alguien reescribió la etiqueta.

Es exactamente el problema de las firmas de la clase 143, y la práctica correcta es la misma: **fijar por
contenido en producción**.

Y Perl tiene las alternativas al contenedor cuando no hay uno (clase 144):

```bash
fatpack pack servicio.pl > servicio-completo.pl    # módulos puros dentro del guion
pp -o servicio servicio.pl                          # ejecutable con intérprete dentro
carton bundle && carton install --deployment         # el árbol exacto, sin red
```

**`carton bundle` merece la mención** porque resuelve un caso real: **desplegar sin acceso a Internet**,
llevando las dependencias en el propio repositorio.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string version;
    if (!std::getline(std::cin, version)) return 1;

    std::cout << "imagen=app:" << version << '\n';
    return 0;
}
```

**C++ y el empaquetado.** C++ tiene el problema de la clase 148 —**las dependencias dinámicas y la versión
de glibc**— y esta clase es el sitio para las soluciones, ordenadas:

```dockerfile
# Construcción en varias etapas: el compilador NO viaja
FROM debian:12 AS construccion
RUN apt-get update && apt-get install -y g++ cmake ninja-build
COPY . /src
WORKDIR /build
RUN cmake -G Ninja /src -DCMAKE_BUILD_TYPE=Release && ninja

# Y la imagen final, mínima
FROM gcr.io/distroless/cc-debian12
COPY --from=construccion /build/servicio /servicio
ENTRYPOINT ["/servicio"]
```

**`distroless` merece la explicación** porque es la aplicación más pura de la regla del cierre: **una
imagen con las bibliotecas de ejecución de C y C++ y nada más**.

```text
Sin intérprete de órdenes, sin gestor de paquetes, sin utilidades.
  → una vulnerabilidad de ejecución remota no encuentra un shell que ejecutar
  → el escáner de vulnerabilidades no reporta cien paquetes irrelevantes
  → y la imagen ocupa unas decenas de MB
```

**Y la ausencia de intérprete de órdenes es una medida de seguridad real** (clase 153): **muchos exploits
dependen de poder ejecutar comandos**, y si no hay ninguno, la explotación se complica mucho.

Y el enlace estático lleva eso al límite:

```bash
g++ -O2 -static -o servicio servicio.cpp     # con musl, para evitar los avisos de glibc
```

```dockerfile
FROM scratch
COPY servicio /servicio
ENTRYPOINT ["/servicio"]
```

**Una imagen con un solo fichero.** Y las advertencias que hay que conocer y que casi nadie menciona:

| Advertencia | Detalle |
|---|---|
| **glibc estático rompe `dlopen` y NSS** | resolución de nombres y usuarios |
| **Sin `/etc/ssl/certs`** | **las conexiones TLS fallan**: hay que copiarlos |
| **Sin `/etc/passwd`** | el proceso corre con un UID sin nombre |
| **Sin zona horaria** | las fechas locales salen en UTC |

**La segunda es la que más tiempo hace perder**, y la solución es copiar el paquete de certificados desde
la etapa de construcción.

Y merece cerrar con la tercera práctica del cierre, que en C++ tiene herramientas: **la imagen
reproducible**.

```bash
SOURCE_DATE_EPOCH=1700000000 ...      # clase 144
docker buildx build --output type=oci,rewrite-timestamp=true
diffoscope imagen1.tar imagen2.tar     # ¿en qué difieren?
```

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

dcl-pi IMAGEN;
  version char(20) const;
end-pi;

dsply ('imagen=app:' + %trim(version));

*inlr = *on;
return;
```

**RPG y el empaquetado.** IBM i tiene la segunda respuesta del gancho, y merece verla con la regla del
cierre delante: **el fichero de salvado** (clase 144).

```text
CRTSAVF FILE(QGPL/ENTREGA)
SAVOBJ OBJ(*ALL) LIB(MIAPP) DEV(*SAVF) SAVF(QGPL/ENTREGA) TGTRLS(V7R3M0)
```

**Y lo que va dentro es más de lo que un contenedor lleva**:

| Dentro del SAVF | Nota |
|---|---|
| Los programas y programas de servicio | con sus firmas (clase 143) |
| **Las tablas, con o sin datos** | `DATA(*YES)` |
| **Los propietarios y las autoridades** | la seguridad viaja con el objeto |
| **Las descripciones y los metadatos** | de qué fuente salió cada objeto (clase 144) |
| **Y la vista de depuración** | se puede depurar en el destino (clase 141) |

**La tercera fila es la que ningún contenedor tiene**: **los permisos forman parte del artefacto**, no de
la configuración del destino.

Y merece decir con franqueza lo que esta plataforma **no** tiene y que es el tema de la clase: **IBM i no
se contenedoriza**.

```text
No hay una imagen de IBM i que se pueda ejecutar en un portátil.
El sistema operativo, la base de datos y la seguridad son inseparables (clase 164),
y la arquitectura es POWER.
```

**Y las consecuencias operativas son reales**: **no se puede levantar un entorno de pruebas desechable**
(clase 173), así que **la práctica es replicar bibliotecas dentro del mismo sistema** — que funciona y no
es lo mismo.

Y lo que la plataforma sí ofrece hoy y merece nombrarse:

| Pieza | Qué aporta |
|---|---|
| **Particiones lógicas (LPAR)** | varios sistemas aislados en una máquina |
| **PASE con contenedores** | Docker para lo que corre en el entorno AIX |
| **`ibmi-bob` + SAVF** | construcción y empaquetado reproducibles (clase 144) |
| **Y el entorno en la nube de IBM** | LPAR bajo demanda |

**La cuarta es el cambio de la última década**: **poder pedir un sistema IBM i por horas** acerca esta
plataforma a la práctica de entornos desechables que el resto del mundo da por supuesta.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 imagen: procedure options(main);

    declare version char(20) varying;

    get edit (version) (a(20));

    put skip list ('imagen=app:' || trim(version));

 end imagen;
```

**PL/I y el empaquetado.** PL/I comparte con COBOL el módulo de carga de esta página, y merece añadir el
mecanismo de versionado del mainframe que la clase 144 nombró, porque es la primera práctica del cierre
implementada en el sistema de ficheros: **los grupos de datos generacionales**.

```jcl
//SALIDA DD DSN=MI.PROD.LOADLIB(+1),DISP=(NEW,CATLG)   <-- la generación SIGUIENTE
//ACTUAL DD DSN=MI.PROD.LOADLIB(0),DISP=SHR             <-- la actual
//ANTES  DD DSN=MI.PROD.LOADLIB(-1),DISP=SHR             <-- la anterior
```

**El sistema conserva las últimas N generaciones automáticamente**, y `(0)`, `(-1)` y `(+1)` se refieren a
ellas de forma relativa.

Y merece señalar las dos propiedades que eso da y que son las del cierre:

**Una, la reversión es cambiar un número** (clase 148): desplegar es `(+1)` y revertir es apuntar a `(-1)`.

**Y dos, el historial existe sin gestionarlo**: **las versiones anteriores están ahí porque el sistema las
guarda**, no porque alguien se acordara.

Es la misma idea que las etiquetas de imagen y que las versiones de un registro, resuelta por el sistema
de ficheros en los años sesenta.

Y esta clase debe recoger la limitación que PL/I comparte con RPG y que la clase 162 explicó: **sin
implementación libre, no hay contenedor**.

```text
No existe una imagen con un compilador de PL/I que se pueda descargar.
Así que la construcción exige el mainframe (clase 147),
y el artefacto solo existe allí.
```

**Y por eso la modernización de estos sistemas pasa por conectar el mainframe al flujo moderno** —Zowe,
IBM DBB (clase 147)— **en lugar de traérselo a un contenedor**.

Es una diferencia práctica con COBOL que merece tenerse en cuenta al planificar, y es la razón por la que
los proyectos sobre PL/I tienden a la traducción (clase 165): **no es el lenguaje, es que no hay forma de
sacarlo de su plataforma**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
IMAGEN ; Empaquetado -- clase 174
 read version
 write "imagen=app:", version, !
 quit
```

**M y el empaquetado.** M tiene la unidad de despliegue más peculiar de esta página, y la clase 143 ya la
nombró: **el paquete KIDS es una global**.

```text
Un parche de VistA contiene:
  - las rutinas, como texto
  - las definiciones de fichero de FileMan y sus cambios
  - los requisitos previos, con números de parche
  - el código de instalación previa y posterior
  - y las sumas de comprobación de cada rutina (clase 144)
```

**Y se instala dentro de una transacción** (clase 148), así que **si algo falla, se deshace todo**.

Y merece la comparación con una imagen de contenedor, porque el contraste es instructivo:

| | KIDS | Imagen de contenedor |
|---|---|---|
| Qué contiene | **el cambio**: rutinas y migraciones | **el sistema entero** |
| Instalación | **incremental y transaccional** | sustitución completa |
| Estado de los datos | **los migra el propio paquete** | fuera del artefacto |
| Reversión | difícil si migró datos | **inmediata** |
| Y el destino | un sistema en marcha | un sistema nuevo |

**Y las dos primeras filas explican el modelo**: **un hospital no puede sustituir su sistema, tiene que
actualizarlo en marcha**, con los datos donde están.

Es la diferencia entre desplegar un servicio sin estado —donde la imagen completa es lo natural— y
actualizar un sistema con cuarenta años de datos, **donde el artefacto tiene que ser el cambio, no el
todo**.

Y esa distinción merece extraerse porque se aplica a cualquier sistema con base de datos: **el código se
sustituye entero; el esquema y los datos se migran** — y **el artefacto de despliegue tiene que incluir
las dos cosas y su orden** (clase 148).

Y hoy, las implementaciones modernas sí se empaquetan:

```dockerfile
FROM yottadb/yottadb-base:latest
COPY rutinas/ /data/r/
COPY globals.zwr /tmp/
RUN yottadb -run %XCMD 'do ^%GI' < /tmp/globals.zwr
```

**Una imagen con el motor, las rutinas y los datos iniciales** — que es lo que hace posible probar en un
corredor de la nube (clase 147) y lo que ha abierto este ecosistema en la última década.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| version |

version := stdin nextLine trimBoth.

Transcript show: 'imagen=app:', version; cr.
```

**Smalltalk y el empaquetado.** Y aquí está la tercera respuesta del gancho, y la más literal: **Smalltalk
llama "imagen" a su artefacto de despliegue desde 1980**.

```smalltalk
Smalltalk snapshot: true andQuit: true.
```

**Y merece poner los dos conceptos juntos, porque el paralelismo es casi exacto:**

| Imagen de Smalltalk (1980) | Imagen de contenedor (2013) |
|---|---|
| Contiene **todos los objetos del sistema** | contiene **todo el sistema de ficheros** |
| Se construye desde una **base + un guion** | `FROM base` + instrucciones |
| Arranca en el **estado guardado** | arranca en el estado de la imagen |
| **Opaca**: hay que confiar en cómo se hizo | ídem |
| Se reduce quitando lo que no se usa (clase 144) | imágenes mínimas |
| **Y no aísla nada** | **aísla procesos, red y ficheros** |

**Y esa última fila es, otra vez, la aportación real de los contenedores** — que la explicación de Tcl en
esta página ya señalaba.

Y el flujo moderno junta las dos:

```dockerfile
FROM pharo/pharo:11 AS construccion
COPY src/ /src/
RUN /pharo/pharo Pharo.image eval --save \
    "Metacello new baseline: 'MiApp'; repository: 'tonel:///src'; load."

FROM pharo/vm:11
COPY --from=construccion /pharo/Pharo.image /app/
ENTRYPOINT ["/pharo/pharo", "/app/Pharo.image", "servir"]
```

**Construcción en dos etapas, imagen construida desde una base limpia con un guion** (clase 144) — las
dos primeras prácticas del cierre.

Y merece cerrar esta clase con la observación que la página entera sostiene: **la idea de empaquetar el
estado completo en un artefacto opaco no la inventaron los contenedores**.

**La inventó Smalltalk, la practicó Lisp, la reprodujo Tcl con los Starkits y la formalizó el mainframe
con sus módulos de carga.** Lo que los contenedores añadieron fue **el aislamiento, los límites de
recursos y —sobre todo— un formato estándar que todos los proveedores implementan**.

Es la misma conclusión que la clase 162 sacaba sobre WebAssembly: **lo difícil no era la técnica, era el
acuerdo**.

---

## Y de vuelta a la clase

Lo transferible: **el artefacto debe contener todo lo que no está garantizado en el destino**. Esa es la
regla, y explica por qué los contenedores ganaron: no por aislar, sino porque **hacen imposible el "en mi
máquina funciona"**. Y las tres prácticas que la acompañan: **etiquetar por contenido y no solo por
versión** —una etiqueta que se puede reescribir no identifica nada—; **construir en varias etapas**, para
que lo que se despliega no lleve el compilador dentro; y **que la imagen sea reproducible** (clase 144),
porque un artefacto que nadie puede volver a construir es un artefacto que nadie puede verificar.

⏮️ [Volver a la clase 174](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
