# -*- coding: utf-8 -*-
"""Parte 11, lote D — clases 174 a 176. Ver `vivos_parte11.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 174 — Empaquetado, contenedores y despliegue
# ---------------------------------------------------------------------------
SPECS["174"] = dict(
    gancho="""
Nombrar una imagen: `imagen=app:1.2.3`. Un nombre y una etiqueta, que es como se identifica hoy una
unidad desplegable. Y esta página tiene las tres respuestas históricas a la misma pregunta —**¿qué es
exactamente lo que se despliega?**—: **un módulo de carga en una biblioteca** (COBOL y PL/I), **un fichero
de salvado con objetos completos** (RPG), y **una imagen con todo el sistema dentro** (Lisp y Smalltalk)
— esta última, cuarenta años antes de que se llamara así.
""",
    porque="""
Aquí el concepto es la **unidad de despliegue**, y estos lenguajes la enseñan porque **cubren todo el
rango de tamaños**: desde un binario estático de 200 KB (Pascal, Ada, C++) hasta una imagen de 200 MB
(Lisp, Smalltalk), pasando por los que necesitan un intérprete y los que necesitan una plataforma
entera.

Y aparece la decisión que decide el coste operativo: **qué se mete dentro del artefacto y qué se espera
encontrar fuera**. Cuanto más dentro, más grande y más autónomo; cuanto más fuera, más ligero y más
frágil.
""",
    cierre="""
Lo transferible: **el artefacto debe contener todo lo que no está garantizado en el destino**. Esa es la
regla, y explica por qué los contenedores ganaron: no por aislar, sino porque **hacen imposible el "en mi
máquina funciona"**. Y las tres prácticas que la acompañan: **etiquetar por contenido y no solo por
versión** —una etiqueta que se puede reescribir no identifica nada—; **construir en varias etapas**, para
que lo que se despliega no lleve el compilador dentro; y **que la imagen sea reproducible** (clase 144),
porque un artefacto que nadie puede volver a construir es un artefacto que nadie puede verificar.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. IMAGEN.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  VERSION PIC X(20).

PROCEDURE DIVISION.
    ACCEPT VERSION
    DISPLAY "imagen=app:" FUNCTION TRIM(VERSION)
    STOP RUN.
""", """
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
"""),
        "fortran": ("""
program imagen
   implicit none
   character(len=20) :: version

   read(*, '(A)') version

   write(*, '(A)') 'imagen=app:' // trim(adjustl(version))
end program imagen
""", """
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
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;

procedure Imagen is
   Linea  : String (1 .. 20);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   Put_Line ("imagen=app:" & Linea (1 .. Ultimo));
end Imagen;
""", """
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
"""),
        "pascal": ("""
program Imagen;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Version: string;

begin
  ReadLn(Version);
  WriteLn('imagen=app:', Trim(Version));
end.
""", """
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
"""),
        "lisp": ("""
(let ((version (string-trim '(#\\Space #\\Return) (read-line))))
  (format t "imagen=app:~A~%" version))
""", """
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
"""),
        "tcl": ("""
gets stdin version

puts "imagen=app:[string trim $version]"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $version = <STDIN>;
chomp $version;

print "imagen=app:$version\\n";
""", """
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
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string version;
    if (!std::getline(std::cin, version)) return 1;

    std::cout << "imagen=app:" << version << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi IMAGEN;
  version char(20) const;
end-pi;

dsply ('imagen=app:' + %trim(version));

*inlr = *on;
return;
""", """
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
"""),
        "pli": ("""
 imagen: procedure options(main);

    declare version char(20) varying;

    get edit (version) (a(20));

    put skip list ('imagen=app:' || trim(version));

 end imagen;
""", """
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
"""),
        "mumps": ("""
IMAGEN ; Empaquetado -- clase 174
 read version
 write "imagen=app:", version, !
 quit
""", """
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
"""),
        "smalltalk": ("""
| version |

version := stdin nextLine trimBoth.

Transcript show: 'imagen=app:', version; cr.
""", """
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
RUN /pharo/pharo Pharo.image eval --save \\
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 175 — Documentación y defensa de las decisiones de lenguaje
# ---------------------------------------------------------------------------
SPECS["175"] = dict(
    gancho="""
Contar las secciones de un documento: `documentado=5 secciones`. Es lo más aburrido de esta parte y lo
que más se agradece dentro de tres años. Y estos lenguajes son la mejor prueba de por qué: **todos ellos
fueron, en su momento, una decisión razonable** — y hoy, quien se encuentra ese código sin explicación
suele concluir que alguien se equivocó. **Lo que falta casi nunca es el código: es el porqué** (clase
154).
""",
    porque="""
Aquí el concepto es la **decisión documentada**, y estos lenguajes lo enseñan porque **son decisiones que
han sobrevivido a sus autores**. Un sistema COBOL de 1985, un modelo Fortran de 1978 o un paquete VistA
de 1990 llevan décadas ejecutándose, y **la pregunta que todo el mundo hace al llegar es la misma: ¿por
qué está esto así?**

Y aparece el formato que la industria ha encontrado para responderla: **el registro de decisión de
arquitectura**, corto, con contexto, alternativas y consecuencias.
""",
    cierre="""
Lo transferible: **documenta las decisiones, no el código**. El código dice qué hace; lo que se pierde es
**qué se consideró, qué se descartó y por qué** — y sin eso, quien llegue después solo puede suponer que
fue un error. De ahí el formato que funciona y que cabe en una página: **contexto** (qué problema había y
qué restricciones), **decisión** (qué se eligió), **alternativas** (qué más se miró y por qué no), y
**consecuencias** (qué se gana, qué se pierde y qué habría que revisar si cambia el contexto). Y la regla
que lo hace sostenible: **las decisiones se escriben cuando se toman**, porque reconstruirlas después es
imposible.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. DOCUMEN.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED
    DISPLAY "documentado=" FUNCTION TRIM(ED) " secciones"
    STOP RUN.
""", """
**La decisión, escrita: COBOL.** Así se vería el registro de decisión que casi nunca se escribió y que hoy
haría falta:

```text
DECISIÓN 001 — Mantener el motor de cálculo de intereses en COBOL
Estado: aceptada (2024), revisada desde la original de 1987

CONTEXTO
  - 240.000 líneas de COBOL implementan las reglas de cálculo,
    incluidas 30 años de normativa acumulada y sus excepciones.
  - No existe especificación escrita: el código ES la especificación (clase 154).
  - El sistema procesa el cierre diario en una ventana de 4 horas.
  - La aritmética es decimal exacta y auditada por el regulador (clase 072).

DECISIÓN
  Mantener el motor en COBOL y exponerlo como servicio (clases 149 y 160).
  Todo lo nuevo se escribe fuera.

ALTERNATIVAS CONSIDERADAS
  - Reescritura completa a Java: descartada. Las reescrituras de sistemas
    sin especificación fracasan con frecuencia documentada (clase 150),
    y el coste de reproducir el redondeo decimal exacto es alto (clase 140).
  - Traducción automática: descartada. Produce código que nadie entiende
    y hereda la deuda sin las personas que la conocen.
  - Estrangulamiento por partes: ACEPTADA para las funciones que cambien.

CONSECUENCIAS
  + La lógica validada no se toca; el riesgo regulatorio no aumenta.
  + Lo nuevo se escribe con tecnología actual.
  - Dependencia de un perfil escaso, con relevo generacional urgente (clase 154).
  - Y hay que mantener la capa de fachada.

REVISAR SI
  - se pierde el conocimiento del equipo actual
  - o cambia la normativa de forma que obligue a tocar el núcleo
```

**Y el apartado "revisar si" merece destacarse**, porque es el que convierte un documento en una
herramienta: **una decisión correcta depende de un contexto, y decir cuál permite saber cuándo dejó de
serlo** (clase 154).

Sin él, la decisión se hereda como dogma — y es exactamente lo que le pasó al estilo abreviado de M
(clase 154) y a tantas otras.
"""),
        "fortran": ("""
program documen
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A)') 'documentado=', n, ' secciones'
end program documen
""", """
**La decisión, escrita: Fortran.**

```text
DECISIÓN 007 — El núcleo numérico se mantiene en Fortran moderno

CONTEXTO
  - El solver tiene 80.000 líneas, validado contra datos experimentales
    y contra soluciones analíticas durante 20 años (clase 173).
  - Se ejecuta en clústeres con MPI, hasta 4.000 procesos.
  - Depende de LAPACK y de FFTW, y su rendimiento está optimizado
    para el orden de acceso por columnas (clases 149 y 152).
  - El equipo son físicos, no ingenieros de software.

DECISIÓN
  Mantener Fortran para el núcleo, y Python para todo lo demás:
  preparación de datos, orquestación, análisis y gráficas (clase 155).

ALTERNATIVAS CONSIDERADAS
  - C++ con Eigen: rendimiento equivalente. Descartada porque el equipo
    no lo domina y porque reescribir invalidaría 20 años de validación.
  - Julia: atractiva; descartada por madurez del ecosistema MPI
    y por el coste de migrar. REVISAR en 3 años.
  - Todo en Python con NumPy: descartada. Los bucles anidados con
    dependencias no se vectorizan bien.

CONSECUENCIAS
  + Se conserva la validación y el rendimiento.
  + La capa de Python permite trabajar a quien no sabe Fortran.
  - Hay que mantener la frontera con f2py (clase 158).
  - Y hay que invertir en lo que al código le falta:
    pruebas (clase 139), construcción reproducible (clase 144) y un dueño.

REVISAR SI
  - Julia o Rust alcanzan paridad de ecosistema en HPC
  - o si el equipo cambia lo bastante como para no poder mantenerlo
```

**Y la línea de las consecuencias sobre lo que "hay que invertir" es la más útil de este documento**,
porque nombra la deuda de forma explícita (clase 154).

**Una decisión que reconoce lo que deja pendiente es una decisión honesta**; una que solo lista ventajas
es publicidad.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Documen is
   N : Integer;
begin
   Get (N);

   Put_Line ("documentado=" &
             Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both) & " secciones");
end Documen;
""", """
**La decisión, escrita: Ada.** En el dominio de Ada, este documento **no es opcional**: forma parte del
expediente de certificación, y merece verlo con ese peso.

```text
DECISIÓN 002 — Ada/SPARK para el software de control de vuelo

CONTEXTO
  - Requisito DO-178C nivel A: un fallo es catastrófico.
  - Hay que demostrar cobertura MC/DC (clase 139) y ausencia de
    errores de ejecución.
  - Vida operativa prevista: 30 años.
  - Restricciones: memoria acotada, plazos duros, sin sistema operativo.

DECISIÓN
  Ada 2012 con perfil Ravenscar y subconjunto SPARK para los módulos
  de nivel A (clases 135 y 146).

ALTERNATIVAS CONSIDERADAS
  - C con MISRA-C: viable y usado en el sector. Descartada porque
    exige herramientas externas para lo que Ada da en el lenguaje,
    y la evidencia de análisis es más costosa de producir.
  - Rust: seguridad de memoria comparable. Descartada HOY por falta de
    cadena de herramientas cualificada y de precedente ante el regulador
    (clase 164). REVISAR en cada nuevo programa.
  - Generación desde modelo (SCADE): ACEPTADA para las leyes de control;
    el código generado es Ada.

CONSECUENCIAS
  + gnatprove demuestra la ausencia de errores de ejecución (clase 118).
  + El perfil Ravenscar permite demostrar los plazos (clase 152).
  - Contratación difícil: hay que formar internamente (clase 154).
  - Ecosistema pequeño: casi todo se escribe en casa.
  - Y la cadena de herramientas queda CONGELADA durante el programa (clase 174).

REVISAR SI
  - la certificación de una cadena Rust madura
  - o si el coste de contratación se vuelve prohibitivo
```

**Y merece señalar lo que este dominio hace y que el resto debería copiar**: **las alternativas se
documentan aunque se descarten**, y **se dice qué las haría ganar**.

Es la diferencia entre "elegimos Ada" y "elegimos Ada, y esto es lo que tendría que pasar para elegir otra
cosa" — la segunda es una decisión de ingeniería; la primera, una preferencia.
"""),
        "pascal": ("""
program Documen;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('documentado=', IntToStr(N), ' secciones');
end.
""", """
**La decisión, escrita: Object Pascal.**

```text
DECISIÓN 015 — Mantener el terminal de punto de venta en Delphi

CONTEXTO
  - 4.200 terminales instalados en tiendas, con hardware específico:
    balanza, cajón, impresora fiscal, lector (clase 165).
  - Deben funcionar SIN RED: una caída de línea no puede parar la caja.
  - Aplicación de 350.000 líneas, 18 años de evolución.
  - Actualización remota, sin técnico en tienda (clase 148).

DECISIÓN
  Mantener Delphi para el terminal. La lógica de negocio ya está
  separada en unidades sin interfaz (clase 149) y se prueba con DUnitX.

ALTERNATIVAS CONSIDERADAS
  - Aplicación web: descartada. No funciona sin red y el acceso al
    hardware local exige un agente nativo igualmente.
  - Electron o similar: descartada. Arranque lento y consumo alto
    para el hardware instalado, que tiene 8 años.
  - .NET o Java: viable técnicamente. Descartada por el coste de
    reescribir la integración con hardware, que es la parte cara.

CONSECUENCIAS
  + Binario autocontenido, arranque instantáneo, sin dependencias (clase 174).
  + La inversión en integración de hardware se conserva.
  - Licencias de Delphi y contratación difícil (clase 164).
  - Y el ecosistema encoge: hay que asumir mantener más cosas en casa.

REVISAR SI
  - se renueva el parque de terminales
  - o si aparece una necesidad de movilidad que el escritorio no cubra
```

**Y la fila de "no funciona sin red" merece destacarse** porque es el tipo de restricción que suele
faltar en estas discusiones y que decide el resultado.

**Las decisiones de tecnología casi nunca las gana el lenguaje mejor**: las gana **la restricción que
elimina más opciones** — y escribirla es lo que hace que la discusión sea corta y la decisión, defendible.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "documentado=~D secciones~%" n))
""", """
**La decisión, escrita: Common Lisp.**

```text
DECISIÓN 021 — El motor de reglas de tarificación en Common Lisp

CONTEXTO
  - Las reglas de precio las definen los actuarios, cambian cada mes
    y tienen interacciones complejas entre sí.
  - Intentos previos con tablas de configuración se quedaron cortos:
    acabaron necesitando condicionales, y luego variables (clase 163).
  - El equipo son 3 personas, con experiencia en Lisp.

DECISIÓN
  Motor en Common Lisp, con un lenguaje de dominio definido con macros
  (clase 149), aislado tras una API (clase 160).

ALTERNATIVAS CONSIDERADAS
  - Motor de reglas comercial: descartado por coste y por rigidez
    del modelo de reglas frente a lo que el dominio necesita.
  - Python con un DSL: viable. Descartada porque las macros permiten
    que la regla se lea como la escribe el actuario, y eso reduce
    los errores de traducción.
  - Reglas en la base de datos: descartada por lo que enseña VistA
    (clase 151): la lógica deja de ser revisable y versionable.

CONSECUENCIAS
  + Las reglas se escriben en el vocabulario del dominio.
  + El ciclo de prueba es de segundos (clase 124).
  - RIESGO PRINCIPAL: un solo dueño. Mitigación obligatoria:
    documentar el porqué (clase 154), macros solo cuando una función
    no baste (clase 150), y pruebas que sirvan de especificación (clase 139).
  - Contratación muy difícil.
  - Y la API es la frontera: si hay que reescribirlo, se reescribe
    solo este componente (clase 165).

REVISAR SI
  - el equipo baja de dos personas que lo dominen
  - o si el ritmo de cambio de las reglas se estabiliza
```

**Y la línea del riesgo principal es la que hace útil este documento**: **nombra el peligro y escribe la
mitigación**.

**Una decisión que no dice cómo puede salir mal no está terminada** — y en tecnologías minoritarias, el
riesgo casi siempre es el mismo y casi nunca se escribe.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

puts "documentado=$n secciones"
""", """
**La decisión, escrita: Tcl.**

```text
DECISIÓN 009 — Tcl como lenguaje de guion de la herramienta

CONTEXTO
  - La herramienta es un motor de simulación en C++ (clase 165).
  - Los usuarios son ingenieros que necesitan automatizar flujos
    y componer análisis, no programar el motor.
  - El sector ya usa Tcl en las herramientas equivalentes (clase 149):
    los usuarios lo conocen.
  - Los flujos que escriban durarán más que varias versiones del producto.

DECISIÓN
  Incrustar Tcl como lenguaje de comandos, con una API de comandos
  registrados explícitamente (clase 163).

ALTERNATIVAS CONSIDERADAS
  - Lua: más pequeño y más rápido. Descartada porque los usuarios
    del sector ya escriben Tcl y sus flujos existentes se podrían reusar.
  - Python incrustado: más popular en general. Descartada por el peso
    del intérprete y por la fragmentación de versiones del entorno.
  - Un lenguaje propio: DESCARTADA explícitamente. Es el error que
    Ousterhout describió al crear Tcl (clase 155) y siempre acaba
    siendo un lenguaje mal diseñado sin herramientas.

CONSECUENCIAS
  + Los usuarios son productivos desde el primer día.
  + Safe-Tcl permite ejecutar guiones de terceros con capacidades
    acotadas y límites de recursos (clases 153 y 163).
  - Compromiso de compatibilidad: los guiones de los clientes
    NO se pueden romper entre versiones (clase 160).
  - Y la comunidad de Tcl es pequeña: menos bibliotecas de terceros.

REVISAR SI
  - el perfil de usuario cambia hacia gente que espera Python
```

**Y la alternativa descartada explícitamente —inventar un lenguaje propio— merece estar escrita**, porque
es la que siempre vuelve.

**Documentar por qué NO se hizo algo evita repetir la discusión cada dos años** — y es, probablemente, el
valor más subestimado de este tipo de documento.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "documentado=$n secciones\\n";
""", """
**La decisión, escrita: Perl.**

```text
DECISIÓN 033 — El proceso de integración de ficheros sigue en Perl

CONTEXTO
  - 47 proveedores envían ficheros en 31 formatos distintos, algunos
    definidos hace 20 años y ninguno negociable a corto plazo.
  - El proceso tiene 6.000 líneas y 12 años (clase 165).
  - Se ejecuta cada noche y es crítico: si falla, no hay facturación.
  - Tiene 0 % de cobertura de pruebas.

DECISIÓN
  Mantenerlo en Perl, y ANTES de cualquier cambio:
    1. pruebas de caracterización con ficheros reales (clase 150)
    2. un contrato declarado para la entrada y la salida (clase 160)
    3. un dueño identificado

ALTERNATIVAS CONSIDERADAS
  - Reescribir en Python: descartada de momento. Sin pruebas,
    una reescritura no se puede verificar (clase 140).
  - Herramienta ETL comercial: descartada. Los formatos irregulares
    exigen lógica que las herramientas gráficas expresan mal.
  - Dejarlo como está: DESCARTADA. Es el estado actual y ya ha
    provocado dos incidentes.

CONSECUENCIAS
  + El proceso sigue funcionando mientras se estabiliza.
  + Con pruebas y contrato, la reescritura futura será verificable.
  - Perl es hoy una elección minoritaria: la contratación cuesta.
  - Y hay que invertir en lo que debió hacerse hace años.

REVISAR SI
  - los pasos 1 a 3 están completos: entonces la reescritura
    pasa a ser una decisión de coste, no de riesgo
```

**Y ese último apartado es lo mejor que puede tener un documento de este tipo**: **convierte "algún día
habrá que hacer algo" en una condición concreta**.

Es la diferencia entre una deuda que se arrastra y una que tiene un plan (clase 154) — y la condición
escrita es lo que permite volver a la conversación con datos en lugar de con opiniones.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "documentado=" << n << " secciones" << '\\n';
    return 0;
}
""", """
**La decisión, escrita: C++.**

```text
DECISIÓN 004 — C++ para el motor de procesado, con frontera en C

CONTEXTO
  - El motor procesa 2 millones de eventos por segundo con un
    presupuesto de 50 µs en el percentil 99 (clase 152).
  - Depende de bibliotecas de terceros que solo existen en C++.
  - Lo consumen componentes en Python y en Go (clase 155).

DECISIÓN
  Motor en C++20, expuesto con una interfaz en C y punteros opacos
  (clase 156). Aislado en su propio proceso (clase 165).

ALTERNATIVAS CONSIDERADAS
  - Rust: rendimiento equivalente y seguridad de memoria (clase 164).
    Descartada HOY por las bibliotecas de terceros. Se ha ACEPTADO
    escribir los componentes NUEVOS en Rust, con frontera en C.
  - Go: descartada por las pausas del recolector frente al presupuesto
    de latencia del percentil 99.
  - Java: ídem.

CONSECUENCIAS
  + Se cumple el presupuesto de latencia.
  + La interfaz en C sirve para cualquier lenguaje cliente (clase 157).
  - RIESGO: seguridad de memoria. Mitigaciones OBLIGATORIAS:
    desinfectantes en toda la suite (clase 147), fuzzing continuo
    de las fronteras (clase 173), y proceso aislado para que un
    fallo no comprometa el resto (clase 153).
  - Y el proyecto acumulará varias generaciones del lenguaje: hay
    que fijar el estándar y un formateador desde el día uno (clase 146).

REVISAR SI
  - las bibliotecas críticas tienen equivalente en Rust
  - o si el análisis de incidentes muestra que las mitigaciones no bastan
```

**Y las mitigaciones marcadas como obligatorias son lo que distingue una decisión responsable de una
imprudente.**

Elegir C++ sabiendo el riesgo y poniendo las defensas es ingeniería; elegirlo sin nombrarlo es lo que
produce el 70 % de las vulnerabilidades de la clase 153.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi DOCUMEN;
  n int(10) const;
end-pi;

dsply ('documentado=' + %char(n) + ' secciones');

*inlr = *on;
return;
""", """
**La decisión, escrita: RPG e IBM i.**

```text
DECISIÓN 012 — Permanecer en IBM i, con RPG modernizado

CONTEXTO
  - ERP propio de 1,2 millones de líneas, 28 años, en producción
    con 900 usuarios y disponibilidad del 99,98 %.
  - La plataforma aporta base de datos, seguridad, colas,
    planificación y observabilidad integradas (clases 142 y 164).
  - Coste operativo actual: 2 personas de sistemas.
  - Edad media del equipo de desarrollo: 54 años (clase 154).

DECISIÓN
  Permanecer. Y ejecutar un plan de modernización EN la plataforma:
    - conversión a formato totalmente libre (clase 150)
    - extracción de lógica a programas de servicio (clase 149)
    - SQL en lugar de acceso registro a registro (clase 152)
    - fuentes en git, en el IFS (clase 145) y CI con ibmi-bob (clase 147)
    - y APIs REST con IWS para lo nuevo (clase 160)

ALTERNATIVAS CONSIDERADAS
  - Migrar a un ERP de mercado: descartada. El ajuste funcional
    cubre el 60 %; el resto habría que reimplementarlo igualmente.
  - Reescribir en Java sobre Linux: descartada por coste y riesgo
    (clase 150), y porque habría que reconstruir lo que la plataforma
    da de fábrica: 2 personas de sistemas pasarían a ser un equipo.
  - No hacer nada: DESCARTADA. El riesgo de relevo es inmediato.

CONSECUENCIAS
  + Se conserva la lógica validada y el coste operativo bajo.
  + Lo nuevo se escribe con tecnología actual, sobre la misma máquina.
  - Dependencia de un único proveedor.
  - Y hay que resolver el relevo: contratación, formación y captura
    del conocimiento de las reglas, con urgencia (clase 154).

REVISAR SI
  - el relevo generacional no se resuelve en 3 años
  - o si el coste de licencias cambia significativamente
```

**Y la última consecuencia con la palabra "urgencia" es la más importante del documento**, porque es la
única con plazo.

**Una decisión que identifica un riesgo sin fecha es una decisión que lo aplaza** — y este es el caso
donde eso sale más caro.
"""),
        "pli": ("""
 documen: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('documentado=' || trim(char(n)) || ' secciones');

 end documen;
""", """
**La decisión, escrita: PL/I.**

```text
DECISIÓN 018 — Migrar el sistema actuarial de PL/I, por fases

CONTEXTO
  - 600.000 líneas de PL/I, cálculo de reservas técnicas, 35 años.
  - NO hay implementación libre del lenguaje (clase 162): no se puede
    compilar ni probar fuera del mainframe (clase 147).
  - El equipo que lo conoce son 3 personas; 2 se jubilan en 4 años.
  - La normativa de solvencia obliga a cambios frecuentes.

DECISIÓN
  Migración por estrangulamiento (clase 150), no reescritura completa:
    1. fachada de servicios sobre el sistema actual (clase 160)
    2. verificador de equivalencia con datos reales, en paralelo (clase 140)
    3. traducción función a función, verificada contra el original
    4. y apagado del componente viejo solo cuando el nuevo lleve
       6 meses coincidiendo

ALTERNATIVAS CONSIDERADAS
  - Reescritura completa: descartada. 600.000 líneas sin especificación
    y con un plazo de 4 años es el escenario clásico de fracaso.
  - Traducción automática PL/I → Java: descartada como solución única.
    Produce código sintácticamente correcto e ilegible, y hereda
    la deuda sin las personas. Se usará como PUNTO DE PARTIDA de cada
    función, con refactorización posterior.
  - Permanecer: descartada por el riesgo de relevo y por la
    imposibilidad de montar una CI moderna.

CONSECUENCIAS
  + Cada paso es reversible y el sistema funciona todo el tiempo.
  + El verificador de equivalencia da evidencia ante el regulador.
  - Es lento: 4 a 6 años.
  - Y exige mantener los dos sistemas durante la transición.

REVISAR SI
  - el ritmo de traducción se desvía más de un 30 % del plan
```

**Y la decisión de usar la traducción automática como punto de partida y no como resultado merece
destacarse**, porque es el matiz que suele faltar: **la herramienta ahorra la parte mecánica y no sustituye
al criterio**.
"""),
        "mumps": ("""
DOCUMEN ; Documentar decisiones -- clase 175
 read n
 write "documentado=", n, " secciones", !
 quit
""", """
**La decisión, escrita: M.**

```text
DECISIÓN 026 — Conservar el núcleo clínico en M, sobre YottaDB

CONTEXTO
  - Historia clínica de 40 años, con lógica clínica validada
    y usada por 12.000 profesionales.
  - El modelo de datos —árboles ordenados, transaccionales,
    sin impedancia (clase 170)— encaja con el dominio.
  - El lenguaje es indefendible con criterios actuales: sin
    declaraciones, con ámbito global por defecto, con indirección
    imposible de analizar (clases 146 y 150).
  - Un error clínico puede causar daño a un paciente.

DECISIÓN
  Separar las dos cosas:
    - CONSERVAR el motor de datos (YottaDB) y la lógica clínica en M
    - ESCRIBIR todo lo nuevo en otros lenguajes, contra las mismas
      globals con los envoltorios oficiales (clase 156)
    - EXPONER el sistema con FHIR, no con estructuras internas (clase 160)

ALTERNATIVAS CONSIDERADAS
  - Migrar a un sistema comercial: descartada por coste y porque
    la lógica local acumulada se perdería.
  - Migrar los datos a PostgreSQL: descartada. El modelo jerárquico
    encaja mejor con la historia clínica que el relacional, y la
    migración pondría en riesgo 40 años de datos.
  - Reescribir la lógica clínica: descartada por riesgo asistencial.

CONSECUENCIAS
  + El dato y su lógica validada no se tocan.
  + Lo nuevo se escribe con tecnología actual y personal contratable.
  + FHIR permite integrar aplicaciones de terceros (clase 169).
  - Sigue habiendo código M que mantener, con relevo difícil.
  - Y hay una deuda pendiente: el código dentro del diccionario de
    datos es ejecución sin límites (clases 151 y 163). Plan: sustituirlo
    por extensiones acotadas.

REVISAR SI
  - la deuda del código en el diccionario provoca un incidente
  - o si aparece un motor con el mismo modelo y mejor ecosistema
```

**Y la separación entre "el lenguaje" y "el motor" es lo que hace defendible esta decisión** (clase 164).

**Sin ese matiz, la discusión se reduce a "M es antiguo" y se pierde lo único que importa: que el modelo
de datos es bueno y los datos son irremplazables.**
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'documentado=', n printString, ' secciones'; cr.
""", """
**La decisión, escrita: Smalltalk.**

```text
DECISIÓN 030 — Smalltalk para el modelo de dominio del sistema de seguros

CONTEXTO
  - El dominio tiene 400 tipos de cobertura con interacciones,
    y cambia varias veces al año.
  - El equipo trabaja con los actuarios en sesiones de modelado.
  - Requisito: poder explorar reglas nuevas en horas, no en semanas.
  - El resto del sistema —web, integración— usa tecnología convencional.

DECISIÓN
  Modelo de dominio en Pharo, con persistencia en GemStone (clase 172),
  expuesto por API REST (clase 160). Todo lo demás, fuera.

ALTERNATIVAS CONSIDERADAS
  - Java o C# con un ORM: viable y descartada por el ciclo de
    exploración: el modelado con objetos vivos es mucho más rápido
    para este dominio (clase 124).
  - Motor de reglas comercial: descartado por rigidez.
  - Python: buen ciclo, y descartada por la persistencia de objetos:
    GemStone elimina el mapeo objeto-relacional por completo.

CONSECUENCIAS
  + Ciclo de modelado de minutos; los actuarios participan directamente.
  + Sin impedancia entre el modelo y el almacenamiento (clase 170).
  - Comunidad pequeña; contratación muy difícil (clase 164).
  - El modelo de imagen exige disciplina con git (clase 145) y con
    la construcción reproducible (clase 174). Mitigación: Tonel,
    Metacello con versiones fijas, e imagen construida desde cero en CI.
  - Y GemStone es comercial: dependencia de proveedor.

REVISAR SI
  - el equipo que lo domina baja de tres personas
  - o si el ritmo de cambio del dominio se estabiliza y el ciclo
    rápido deja de compensar sus costes
```

**Y merece cerrar esta clase con la observación que las doce decisiones de esta página comparten**: **en
ninguna gana el lenguaje "mejor"**.

Gana **el que encaja con el contexto**: la validación acumulada, el modelo de datos, el equipo, la
restricción dura, el horizonte temporal.

**Y todas las decisiones dicen bajo qué condición habría que revisarlas** — que es lo único que impide que
una decisión razonable de hoy se convierta en el "¿por qué está esto así?" de dentro de veinte años, que
es exactamente lo que estos doce lenguajes llevan escuchando toda su vida.
"""),
    },
)

# ---------------------------------------------------------------------------
# 176 — Cierre: retrospectiva y transferencia a nuevos lenguajes
# ---------------------------------------------------------------------------
SPECS["176"] = dict(
    gancho="""
La última clase: contar las lecciones y afirmar que son transferibles. Y esta página cierra 136 clases de
lenguajes vivos con la pregunta que las justifica todas: **¿para qué sirve haber mirado COBOL, Fortran,
Ada, Pascal, Lisp, Tcl, Perl, C++, RPG, PL/I, M y Smalltalk?** La respuesta no es para usarlos —aunque
varios se sigan usando— sino porque **en ellos están las decisiones originales, con sus razones
intactas**, y reconocerlas en cualquier lenguaje nuevo es lo que convierte aprender en reconocer.
""",
    porque="""
Aquí el concepto es la **transferencia**, y estos doce lenguajes son el mejor material posible porque
**cada uno lleva una decisión al extremo**: la aritmética exacta, los arreglos, la seguridad demostrada,
la legibilidad, el código como dato, el texto como código, la expresividad, el control total, la
plataforma integrada, la ambición, el dato persistente, y todo como objeto.

Y las decisiones extremas se ven; las moderadas se confunden con lo natural. **Por eso se aprende más de
un lenguaje raro que de uno cómodo.**
""",
    cierre="""
Lo transferible —y es lo último de esta serie—: **un lenguaje es un conjunto de decisiones, y todas se
pagan**. Lo que un lenguaje te da, se lo quita a otra cosa: la seguridad cuesta ceremonia, la
flexibilidad cuesta análisis, el rendimiento cuesta control manual, la abstracción cuesta previsibilidad.
Y por eso la pregunta útil ante cualquier lenguaje nuevo no es si es bueno, sino **qué decidió, contra
qué, y si eso encaja con lo que tienes delante**. Quien sabe hacer esa pregunta aprende un lenguaje nuevo
en semanas; quien no, lleva veinte años aprendiendo el primero.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CIERRE.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED
    DISPLAY "lecciones=" FUNCTION TRIM(ED) " transferible=si"
    STOP RUN.
""", """
**Lo que se lleva de COBOL.** Tres cosas, y ninguna es sintaxis.

**Una, que los números decimales no son coma flotante** (clase 072). COBOL lo tuvo claro en 1959 porque
su dominio era el dinero, y **cualquier lenguaje moderno tiene un tipo decimal** —`BigDecimal`,
`decimal`, `Decimal`— **que casi nadie usa hasta que llega el primer céntimo descuadrado**.

**Reconocerlo**: en cuanto un programa maneje dinero, cantidades exactas o porcentajes que se suman, la
pregunta es cuál es el tipo decimal del lenguaje y por qué no se está usando.

**Dos, que la legibilidad es una decisión de diseño con coste** (clase 146). COBOL se diseñó para que lo
leyera gente de negocio, y **por eso es verboso**. Hoy nadie diseñaría así, y **la intención sigue siendo
correcta**: **el código se lee muchas más veces de las que se escribe** (clase 154).

**Y tres, que un sistema puede sobrevivir a todos sus autores** (clase 175). COBOL es la prueba de que el
software dura mucho más de lo que su autor imagina, y de que **lo que se pierde no es el código: es el
porqué**.

**Reconocerlo**: cada vez que alguien pregunte "¿por qué está esto así?" y nadie sepa la respuesta, ahí
hay una decisión que no se documentó (clase 154).

Y merece cerrar con la lección incómoda que COBOL enseña mejor que ningún otro de esta página: **el
software que funciona vale más que el software elegante**.

Doscientos mil millones de líneas ejecutando el sistema financiero mundial son un argumento — y quien
trabaje alguna vez en un sistema así descubrirá que **la pregunta no es cómo reescribirlo, sino cómo
respetarlo mientras se construye lo siguiente al lado** (clase 150).
"""),
        "fortran": ("""
program cierre
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A)') 'lecciones=', n, ' transferible=si'
end program cierre
""", """
**Lo que se lleva de Fortran.** Tres cosas que se aplican en cualquier lenguaje.

**Una, que el rendimiento moderno es un problema de memoria, no de aritmética** (clases 128 y 152). La
lección de LAPACK —**diez veces más rápido sin cambiar el algoritmo, solo el orden de acceso**— es la más
transferible de este curso.

**Reconocerlo**: ante un bucle lento, la primera pregunta no es cuántas operaciones hace, sino **cuántos
datos trae de memoria y si los aprovecha**. El orden de los bucles, la disposición de los datos y la
localidad importan más que el número de instrucciones.

**Dos, que la coma flotante no es igualdad** (clases 073 y 140). Comparar reales con `==`, esperar que dos
ejecuciones den lo mismo, o suponer que la suma es asociativa: los tres son errores, y **están en todos
los lenguajes**.

**Y tres, que declarar más permite optimizar más.** `intent`, `pure`, los arreglos que no se solapan: cada
declaración es información que el compilador usa (clase 164).

**Reconocerlo**: `const`, `final`, `readonly`, `noexcept`, los tipos inmutables — **todo lo que restringe
lo que el programa puede hacer permite que la herramienta razone mejor**. La ceremonia que parece
burocracia suele ser información.

Y merece cerrar con lo que Fortran enseña sobre la vida del software y que la clase 154 desarrolló: **el
código científico está mejor validado y peor mantenido que casi ningún otro**.

Y la conclusión no es que los científicos escriban mal: es que **la validación del resultado y la calidad
del software son cosas distintas**, y **un programa puede ser correcto y a la vez imposible de
modificar**.

Es una distinción útil en cualquier dominio.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Cierre is
   N : Integer;
begin
   Get (N);

   Put_Line ("lecciones=" & Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both) &
             " transferible=si");
end Cierre;
""", """
**Lo que se lleva de Ada.** Es, probablemente, el lenguaje de esta página con más lecciones
transferibles, y merece elegir tres.

**Una, que un tipo puede llevar el dominio dentro** (clase 124).

```ada
subtype Porcentaje is Integer range 0 .. 100;
type Metros is new Float;      --  y NO se puede sumar a Pies
```

**Reconocerlo**: en cualquier lenguaje, **cada vez que se escribe una comprobación de rango en varios
sitios, ahí falta un tipo**. Los tipos envoltorio, los enumerados y los tipos con validación en el
constructor hacen lo mismo — y **convierten una comprobación repetida en una garantía**.

**Dos, que un contrato escrito puede comprobarse** (clase 118). Precondiciones, postcondiciones e
invariantes existen en Ada, y **su equivalente existe en todos los lenguajes**: aserciones, `assert`,
tipos refinados, o simplemente una prueba que documenta la expectativa (clase 139).

**Reconocerlo**: cuando un comentario dice "este parámetro no puede ser nulo", **eso es una precondición
que no se comprueba** — y hay una forma de escribirla para que sí.

**Y tres, que renunciar a características compra propiedades** (clases 146 y 152). Ravenscar, `pragma
Restrictions` y SPARK son eso: **quitar la mitad del lenguaje para poder demostrar cosas sobre la otra
mitad**.

**Reconocerlo**: es lo mismo que hacen `strict mode`, los subconjuntos de un lenguaje, las reglas de
estilo que prohíben construcciones (clase 146), y **la programación funcional al renunciar al estado
mutable**.

**Lo que un lenguaje prohíbe es lo que permite a sus herramientas prometer.**

Y esa es, quizá, la idea más importante de todo este curso, y por eso Ada la lleva al extremo: **la
libertad y las garantías son el mismo recurso, repartido de otra manera**.
"""),
        "pascal": ("""
program Cierre;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('lecciones=', IntToStr(N), ' transferible=si');
end.
""", """
**Lo que se lleva de Pascal.** Tres lecciones, y las tres son de diseño.

**Una, que un lenguaje pequeño es una decisión, no una carencia** (clase 164). Wirth hizo Pascal, luego
Modula-2 y luego Oberon, **cada uno más pequeño que el anterior**, con un criterio explícito: **una
característica solo entra si su beneficio supera el coste de que todos tengan que aprenderla y leerla**.

**Reconocerlo**: ante cualquier lenguaje o biblioteca que crece, la pregunta es si cada adición se paga —
y **PL/I en esta misma página es el experimento contrario, con su resultado** (clase 155).

**Dos, que la herramienta forma el estilo** (clase 149). El diseñador visual de Delphi hacía facilísimo
poner la lógica en el manejador del botón, **y por eso millones de líneas la tienen ahí**.

**Reconocerlo**: **la arquitectura por defecto de una herramienta será la del 90 % del código**, por mucho
que el documento diga otra cosa. Si se quiere otra estructura, **hay que hacer que el camino correcto sea
el más fácil**: plantillas, generadores, comprobaciones automáticas (clase 147).

**Y tres, que la compilación rápida cambia cómo se trabaja** (clase 123). Turbo Pascal compilaba en
segundos cuando lo normal eran minutos, y eso **no fue una mejora de comodidad: cambió el ciclo**.

**Reconocerlo**: cualquier cosa que acorte el ciclo —compilación incremental, recarga en caliente,
pruebas rápidas (clase 147)— **rinde mucho más de lo que su descripción sugiere**, porque **cambia cuántas
veces al día se experimenta**.

Y merece cerrar con lo que Pascal enseña sobre este curso entero: **fue diseñado para enseñar**, y sigue
haciéndolo bien porque **hace visible lo que otros lenguajes esconden** — la diferencia entre asignar y
comparar, entre declarar y usar, entre valor y referencia.

**Y ver esas diferencias es exactamente lo que permite reconocerlas en cualquier otro sitio.**
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "lecciones=~D transferible=si~%" n))
""", """
**Lo que se lleva de Common Lisp.** Lisp es el lenguaje del que más cosas han salido, y la lista de la
clase 164 lo resume: **la recolección de basura, los cierres, el REPL, las excepciones, las macros, el
tipado dinámico y buena parte de los IDE**.

Y tres lecciones para llevarse:

**Una, que el código puede ser un dato** (clases 122 y 123). Es la idea más radical de esta página, y su
consecuencia práctica es que **un lenguaje puede extenderse hacia el problema** (clase 149).

**Reconocerlo**: las macros de Rust, los decoradores de Python, los constructores de consultas (clase
170), JSX, y **cualquier cosa que genere código a partir de una declaración** — todos son la misma idea,
más limitada.

**Y su coste también es transferible**: **lo que se genera es difícil de analizar y de depurar** (clase
150), así que la regla de Lisp vale en todas partes: **si una función basta, no uses una macro**.

**Dos, que el ciclo corto es una capacidad, no una comodidad** (clase 124). El REPL de Lisp permite probar
una idea en segundos, y eso **cambia qué problemas se pueden atacar**: los mal definidos, donde hay que
explorar.

**Reconocerlo**: los cuadernos, la recarga en caliente y las pruebas rápidas persiguen lo mismo — y
**merece invertir en el ciclo antes que en casi cualquier otra cosa**.

**Y tres, que el manejo de errores puede ofrecer más que abortar** (clase 116). Los reinicios de Lisp
—**decidir cómo continuar desde donde se sabe qué hacer**— siguen siendo superiores a `try`/`catch`, y
casi ningún lenguaje los tiene.

**Reconocerlo**: cada vez que un manejador de errores tenga que reconstruir el contexto que se perdió al
propagar, **ahí falta lo que Lisp tenía**.

Y merece cerrar con lo que Lisp enseña sobre este curso: **es un lenguaje de 1958 del que la industria
sigue extrayendo ideas**, y eso debería bastar para desconfiar de la palabra "moderno".
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

puts "lecciones=$n transferible=si"
""", """
**Lo que se lleva de Tcl.** Tres lecciones, y la primera es de arquitectura.

**Una, la tesis de los dos lenguajes** (clase 155): **un sistema se construye mejor con uno de sistemas
para los componentes y uno de guion para unirlos**, porque **el 90 % de los cambios ocurre en el
pegamento**.

**Reconocerlo**: está en todas partes —los complementos de un editor, los guiones de un motor de juego, la
configuración programable de una herramienta (clase 163)— y **la pregunta útil en cualquier sistema es
qué capa cambia todos los días y si está hecha del material adecuado**.

**Dos, que la uniformidad es una propiedad valiosa** (clases 081 y 161). En Tcl **todo es una cadena y
todo es un canal**, y eso hace que **el mismo código sirva para un fichero, una tubería y un socket**.

**Reconocerlo**: cada vez que una API trata de forma distinta cosas que son conceptualmente iguales,
**está pidiendo que su usuario aprenda una distinción que no aporta nada** — y `everything is a file` de
Unix es la misma idea con el mismo beneficio.

**Y tres, que ejecutar código ajeno es un problema de capacidades, no de listas negras** (clase 153).
Safe-Tcl, de 1993, **quitó todo y concedió puertas concretas** — y ese modelo es hoy el de WebAssembly,
el de los contenedores y el de los permisos móviles (clase 162).

**Reconocerlo**: ante cualquier complemento, guion de usuario o dependencia de terceros, la pregunta
correcta no es qué prohibir, sino **qué necesita de verdad y cómo dárselo solo a eso**.

Y merece cerrar con lo que Tcl enseña sobre el éxito: **su idea principal ganó tan completamente que hoy
es invisible**, y casi nadie sabe que hubo que defenderla.

**Es la mejor forma de éxito que puede tener una idea**, y también la razón por la que conviene conocer
de dónde vienen las cosas: **lo que hoy parece obvio fue una decisión, y tuvo alternativas**.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "lecciones=$n transferible=si\\n";
""", """
**Lo que se lleva de Perl.** Perl es el lenguaje del que la industria copió más infraestructura sin
citarlo, y la lista de la clase 164 lo resume: **CPAN, TAP, CPAN Testers, el modo taint, POD, las
severidades de perlcritic y las expresiones regulares tal como todos las usan**.

Y tres lecciones:

**Una, que el ecosistema vale más que el lenguaje** (clase 164). CPAN, en 1995, **inventó el archivo de
paquetes** y con él la forma de trabajar de todos los ecosistemas posteriores.

**Reconocerlo**: al evaluar cualquier tecnología, **la pregunta que más pesa no es cómo es el lenguaje,
sino qué hay ya escrito para tu problema** — y las clases 143 y 164 lo repiten desde varios ángulos.

**Dos, que "hay más de una forma de hacerlo" tiene un precio** (clases 146 y 154). Perl es libertad total,
y **su fama de ilegible es la factura**.

**Reconocerlo**: cualquier lenguaje o biblioteca con muchas formas de hacer lo mismo **acaba con un
dialecto por persona**, y la respuesta es la de la clase 146: **un estándar de estilo comprobado
automáticamente**, no la disciplina individual.

**Y tres, que marcar el dato que viene de fuera es una idea excelente** (clase 153). El modo taint de
1989 —**los datos externos están marcados y no se pueden usar en operaciones peligrosas hasta validarlos
explícitamente**— sigue siendo poco imitado y muy sensato.

**Reconocerlo**: es lo que persiguen el análisis de flujo de datos, los tipos "validado" frente a "sin
validar" y **la disciplina de validar en la frontera**. Y la regla que queda es simple: **toda entrada es
hostil hasta que se demuestre lo contrario, y demostrarlo es comprobar contra una lista de lo permitido**.

Y merece cerrar con lo que Perl enseña sobre las modas: **su declive no fue técnico**. Perl 5 siguió
mejorando todo el tiempo; lo que cambió fue la percepción, y quince años de espera por una versión que
acabó siendo otro lenguaje.

**La suerte de una tecnología depende de cosas que no son su calidad** — y saberlo ayuda a juzgar las de
hoy.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "lecciones=" << n << " transferible=si" << '\\n';
    return 0;
}
""", """
**Lo que se lleva de C++.** Tres lecciones, y las tres se aplican a lenguajes que no se parecen en nada a
él.

**Una, que la gestión de recursos es un patrón, no una característica** (clase 132). RAII —**atar la vida
de un recurso a la de un objeto**— es la mejor solución que existe al problema de liberar lo que se
reserva, y **su equivalente está en todos los lenguajes**: `with` en Python, `try-with-resources` en Java,
`defer` en Go, `using` en C#, `unwind-protect` en Lisp (clase 171).

**Reconocerlo**: cada vez que haya un `abrir` sin un `cerrar` garantizado, **falta el mecanismo del
lenguaje que lo garantiza** — y todos lo tienen.

**Dos, que el comportamiento indefinido es una categoría distinta de "error"** (clase 136). Un programa
con comportamiento indefinido **no hace algo incorrecto: deja de tener significado**, y puede funcionar
durante años y romperse al cambiar de compilador.

**Reconocerlo**: las carreras de datos en cualquier lenguaje, el orden de evaluación no especificado, y
todo lo que la documentación llame "no especificado" o "depende de la implementación" — **son promesas que
nadie hizo, y apoyarse en ellas es deuda invisible**.

**Y tres, que la seguridad de memoria no se consigue con disciplina** (clases 153 y 164). El 70 % de las
vulnerabilidades graves de los sistemas grandes son de esa familia, **escritas por equipos excelentes con
revisión y herramientas**.

**Reconocerlo**: es el argumento más fuerte que existe a favor de que **la garantía la dé la herramienta y
no la persona** — y se aplica más allá de la memoria: **a los tipos, a la concurrencia, a los contratos y
al formato del código** (clase 146).

Y merece cerrar con lo que C++ enseña sobre la evolución: **es un lenguaje que ha cambiado
profundamente cuatro veces sin romper nada**, y esa compatibilidad —que es su gran virtud— **es también
por qué un proyecto real contiene cuatro generaciones a la vez** (clase 154).

**Todo lo que se promete mantener, hay que mantenerlo.**
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CIERRE;
  n int(10) const;
end-pi;

dsply ('lecciones=' + %char(n) + ' transferible=si');

*inlr = *on;
return;
""", """
**Lo que se lleva de RPG e IBM i.** Tres lecciones, y ninguna es del lenguaje.

**Una, que la integración de plataforma tiene un valor que no aparece en las comparativas** (clase 164).
Base de datos, seguridad, colas, planificación, registro y observabilidad **en un solo sistema
coherente** dan una productividad operativa que un montaje de veinte piezas no alcanza — y **dos personas
de sistemas mantienen lo que en otra arquitectura serían diez**.

**Reconocerlo**: al comparar arquitecturas, **contar las piezas que hay que integrar, versionar, vigilar y
parchear** es tan importante como comparar las capacidades.

**Dos, que la compatibilidad comprobada es mejor que la prometida** (clases 143 y 160). La firma de un
programa de servicio —**calculada sobre las exportaciones y verificada al arrancar**— hace lo que el
versionado semántico intenta expresar con un número.

**Reconocerlo**: `abi-compliance-checker`, `buf breaking`, las pruebas de contrato (clase 160) — **todo lo
que convierte una promesa en una comprobación automática** merece el esfuerzo, porque **las promesas se
rompen sin querer**.

**Y tres, que la observabilidad puede ser una propiedad del sistema y no un producto** (clase 142). En
IBM i, **cada trabajo lleva su registro con la pila y el número de sentencia, sin instrumentar nada**.

**Reconocerlo**: la pregunta correcta ante cualquier sistema es **"¿qué puedo saber de lo que pasó sin
haberlo previsto?"** — y la respuesta suele ser "poco", porque la observabilidad se añade después y solo
donde alguien se acordó.

Y merece cerrar con lo que esta plataforma enseña sobre el software y las personas, que es la lección más
seria de esta parte: **un sistema puede ser técnicamente sólido y estar en riesgo por completo**.

**El relevo generacional de estos sistemas no es un problema de tecnología** (clase 154), y **no se
resuelve modernizando el código**: se resuelve capturando el porqué de las reglas antes de que se vaya
quien lo sabe.
"""),
        "pli": ("""
 cierre: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('lecciones=' || trim(char(n)) || ' transferible=si');

 end cierre;
""", """
**Lo que se lleva de PL/I.** PL/I es el lenguaje de esta página que menos se usa y del que más se aprende
sobre diseño, y merece tres lecciones.

**Una, que un lenguaje que lo permite todo no puede prometer casi nada** (clase 155). PL/I quiso sustituir
a Fortran y a COBOL a la vez, **y perdió contra los dos** — porque **el compilador de un lenguaje
especializado puede suponer más**, y suponer es lo que permite optimizar y verificar.

**Reconocerlo**: es la misma idea que Ada lleva al extremo en esta página, vista desde el otro lado. **Cada
característica que un lenguaje añade le quita garantías**, y la ambición tiene un precio que se paga
siempre.

**Dos, que el tamaño es un coste de mantenimiento** (clase 154). Un lenguaje que nadie domina entero
**produce un dialecto por persona**, y un sistema con cinco dialectos internos es cinco veces más caro de
entender.

**Reconocerlo**: se aplica a los lenguajes, a los marcos y a las bibliotecas internas — y la defensa es la
de la clase 146: **un subconjunto acordado y comprobado**.

**Y tres, la más práctica y la más dura: sin implementación libre, un lenguaje no llega a las plataformas
nuevas** (clase 162).

**Reconocerlo**: al elegir cualquier tecnología con horizonte largo, **la pregunta sobre quién la mantiene
y bajo qué licencia pesa más que casi cualquier característica** — porque decide si dentro de quince años
seguirá habiendo un camino hacia adelante.

Y merece cerrar con lo que PL/I aporta a la memoria de la disciplina: **tenía en 1964 el manejo de
excepciones con reanudación, la concurrencia en el lenguaje, el decimal exacto y un preprocesador
programable** (clases 116 y 163).

**Muchas de las ideas que hoy parecen recientes tienen sesenta años y ya se probaron.**

Y saberlo cambia cómo se leen las novedades: **no todas lo son, y las que no lo son vienen con su
historia de por qué no funcionaron la primera vez**.
"""),
        "mumps": ("""
CIERRE ; Retrospectiva -- clase 176
 read n
 write "lecciones=", n, " transferible=si", !
 quit
""", """
**Lo que se lleva de M.** M es el lenguaje de esta página que más rechazo produce a primera vista y el
que más ideas valiosas esconde, y merece tres.

**Una, que el desajuste entre el lenguaje y la base de datos no es inevitable** (clase 170). En M **la
variable persistente y la variable local se diferencian en un carácter**, y con eso desaparecen el
mapeo objeto-relacional, la serialización y media capa de infraestructura.

**Reconocerlo**: cada vez que un sistema tenga tres representaciones del mismo dato —el objeto, la fila y
el JSON—, **ahí hay una traducción que cuesta código y produce fallos** (clases 159 y 170). No siempre se
puede evitar, y saber que es una decisión y no una ley ayuda a elegir.

**Dos, que un modelo de datos jerárquico y ordenado es una buena idea que se abandonó y volvió** (clases
099 y 170). Las globals de M son árboles ordenados, persistentes y transaccionales — **y las bases de
clave y valor las redescubrieron cuarenta años después, casi siempre sin las transacciones**.

**Reconocerlo**: el modelo de datos se elige por los patrones de acceso, y **lo jerárquico gana cuando el
acceso se conoce de antemano** — igual que IMS en la clase 170.

**Y tres, la más incómoda de este curso: una tecnología se juzga por su arquitectura, no por su
sintaxis** (clase 164).

**M tiene una sintaxis indefendible con criterios actuales y un modelo de datos excelente.** Y quien se
quede en lo primero **no verá lo segundo**, y concluirá que los sistemas construidos sobre él son un error
— cuando llevan cuarenta años sin perder datos de pacientes.

**Reconocerlo**: es un sesgo constante en las discusiones de tecnología, y **la pregunta que lo corrige es
la del cierre de esta clase**: **¿qué decidió esto, contra qué, y por qué?**

Y merece cerrar con lo que M enseña sobre las decisiones heredadas: **su estilo abreviado fue una decisión
correcta cuando la memoria era cara, y sobrevivió a su motivo** (clase 154).

**Y ese es el patrón general**: **casi ninguna decisión antigua fue estúpida cuando se tomó**. Lo que
suele fallar no es la decisión: **es que nadie escribió su contexto** — que es exactamente el argumento de
la clase 175 y de este curso entero.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'lecciones=', n printString, ' transferible=si'; cr.
""", """
**Lo que se lleva de Smalltalk.** Y con esto cierran las 136 clases de esta serie.

Smalltalk es el lenguaje de esta página con menos usuarios y más descendencia, y la clase 164 hizo la
lista: **la interfaz gráfica, MVC, el Observador, las pruebas unitarias, TDD, la refactorización
automática, la deuda técnica, las cachés de envío que hacen posible todo JIT moderno, y buena parte de lo
ágil**.

Y tres lecciones para llevarse:

**Una, que la uniformidad conceptual tiene poder.** En Smalltalk **todo es un objeto y todo es un envío de
mensaje** —incluidos el `if`, el bucle y la clase (clase 151)—, y de esa única decisión salen la
reflexión, el depurador vivo, la refactorización automática y el navegador.

**Reconocerlo**: cuando un lenguaje o un sistema tiene pocos conceptos aplicados con consistencia,
**aprende más rápido y compone mejor** — y cuando tiene muchos casos especiales, cada uno hay que
recordarlo.

**Dos, que un sistema que se puede preguntar es un sistema que se puede gobernar** (clases 138, 150 y
165). Smalltalk puede responder qué clases tiene, quién llama a qué, qué no usa nadie y dónde está parado
un proceso.

**Reconocerlo**: **cada pregunta que un sistema no puede responder sobre sí mismo se acaba respondiendo
con arqueología** — y las herramientas de análisis, los registros estructurados y las trazas existen para
recuperar parte de esa capacidad.

**Y tres, que las mejores ideas no vienen de la tecnología más usada.** Una comunidad pequeña, trabajando
en un lenguaje minoritario, produjo la forma en que hoy trabaja todo el sector.

**Y esa es la razón de haber recorrido estos doce lenguajes.**

No para usarlos —aunque varios se sigan usando, y con buenas razones (clase 164)— sino porque **cada uno
llevó una decisión al extremo y por eso se ve**: la aritmética exacta, la memoria, la demostración, la
legibilidad, el código como dato, el texto como código, el texto como especialidad, el control, la
plataforma, la ambición, el dato persistente, y el objeto.

**Y todas esas decisiones están, más discretas, en el lenguaje que uses mañana.**

Reconocerlas es lo que convierte aprender un lenguaje nuevo en **reconocer un reparto conocido de
compromisos** — y esa es la única habilidad de este curso que no caduca.
"""),
    },
)
