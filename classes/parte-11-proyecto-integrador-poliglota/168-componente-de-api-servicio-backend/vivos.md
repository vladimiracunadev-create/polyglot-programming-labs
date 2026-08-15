# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 168

> [⬅️ Volver a la clase 168](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una respuesta de servicio: `respuesta=200 datos=5`. Un código de estado y un cuerpo, que es la forma que
ha tomado casi toda la comunicación entre sistemas. Y estos lenguajes tienen aquí una perspectiva que
conviene: **el servidor de aplicaciones no lo inventó la web**. **CICS es de 1969**, y ya hacía lo que un
servidor moderno: recibir peticiones, mantener un conjunto de procesos, gestionar transacciones,
controlar el acceso y responder — con miles de terminales conectados.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **servicio como componente**, y estos lenguajes lo enseñan porque **han sido
> servidores durante décadas y con modelos muy distintos**: transacciones cortas con estado externo
> (CICS), procesos por conexión (CGI), hilos con conjunto reutilizable (AOLserver), bucle de eventos
> (Tcl), y continuaciones (Seaside).
>
> Y aparece la pregunta que decide la arquitectura de un servicio: **¿dónde vive el estado entre una
> petición y la siguiente?** Porque de eso dependen la escala, el reparto de carga y lo que pasa cuando un
> proceso muere.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (el dato solicitado) → stdout: `respuesta=200 datos=<n>`
- **Regla:** `responder 200 con el dato`

| stdin | esperado |
|---|---|
| `5` | `respuesta=200 datos=5` |
| `0` | `respuesta=200 datos=0` |
| `42` | `respuesta=200 datos=42` |

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
PROGRAM-ID. SERVICIO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED
    DISPLAY "respuesta=200 datos=" FUNCTION TRIM(ED)
    STOP RUN.
```

**COBOL como componente de servicio.** Aquí está el dato del gancho, y merece desarrollarlo porque el
paralelismo con un servidor moderno es casi exacto: **CICS, de 1969, es un monitor de transacciones**.

```text
Lo que hace CICS:
  - recibe peticiones y las asigna a una TAREA
  - mantiene un conjunto de programas cargados y reutilizados
  - gestiona la transacción: confirma o deshace (clase 161)
  - controla el acceso por transacción y por recurso (clase 153)
  - y limita la concurrencia y el tiempo de cada tarea
```

**Y el modelo de estado de CICS es exactamente el del cierre de esta clase**, y merece subrayarlo porque
lo resolvió antes que nadie:

```text
Una transacción CICS es CORTA y SIN ESTADO en memoria.
  - lo que hay que recordar entre pantallas va a la COMMAREA (clase 160)
  - o a una cola temporal, o a la base de datos
  - y el programa puede ejecutarse en OTRA región o en OTRA MÁQUINA la vez siguiente
```

**Eso es "sin estado en el proceso" con cincuenta años de adelanto**, y por la misma razón: **para poder
repartir la carga entre varias regiones y sobrevivir a que una caiga**.

Y merece la comparación completa, porque hace evidente que el problema no cambió:

| CICS (1969) | Web moderna |
|---|---|
| Transacción (código de 4 letras) | punto de acceso de la API |
| **COMMAREA** | cuerpo de la petición y de la respuesta |
| Cola temporal | caché de sesión (Redis) |
| **Región CICS** | proceso o contenedor |
| CICSPlex, reparto entre regiones | balanceador y réplicas |
| `EXEC CICS SYNCPOINT` | confirmación de la transacción |
| **Límite de tiempo por tarea** | tiempo máximo de petición |
| RACF por transacción | autorización por punto de acceso |

Y hoy, la fila que falta la pone z/OS Connect (clase 158): **el programa COBOL se expone como REST**, y el
código de estado HTTP lo genera la capa de fachada a partir del código de retorno.

Es la aplicación de la tercera regla del cierre: **el error forma parte del contrato**, y traducir un
`SQLCODE` a un 404 o a un 409 **es una decisión de diseño de la API**, no un detalle de implementación.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program servicio
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0)') 'respuesta=200 datos=', n
end program servicio
```

**Fortran como componente de servicio.** Fortran no es un lenguaje de servidores, y esta clase es el sitio
para explicar **cómo se expone entonces un cálculo como servicio**, que es un problema real y frecuente.

**La arquitectura habitual, y es la correcta:**

```text
Cliente HTTP
   ↓
API en Python / Go / Node          ← maneja HTTP, autenticación, colas, límites
   ↓
►  Cálculo en Fortran               ← una biblioteca, o un proceso trabajador
```

**Y la decisión concreta es cómo se conecta esa flecha**, con las tres opciones de la clase 155:

| Opción | Cuándo |
|---|---|
| **Biblioteca cargada en el proceso** (f2py, ctypes) | cálculos de milisegundos |
| **Proceso trabajador con cola** | cálculos de minutos u horas |
| **Trabajo enviado al planificador del clúster** | cálculos de días |

**Y la segunda y la tercera son las habituales**, porque un cálculo científico **no cabe en el tiempo de
una petición HTTP**.

Y de ahí el patrón que esta clase debe nombrar porque es el correcto para trabajos largos y se aplica muy
mal muy a menudo: **la petición asíncrona con recurso de estado**.

```text
POST /simulaciones        → 202 Accepted, y devuelve un identificador
GET  /simulaciones/{id}    → 200 con estado: "en cola", "ejecutando", "terminada"
GET  /simulaciones/{id}/resultado → 200 con los datos, o 404 si aún no está
```

**El código 202 y el recurso de estado son la forma correcta**, y evitan el error clásico: **mantener la
conexión HTTP abierta durante veinte minutos**, que falla en cuanto hay un balanceador o un proxy de por
medio.

Y esta clase debe recoger la restricción que Fortran impone a este componente y que hay que diseñar
alrededor: **el estado global**.

```fortran
module estado
   real(dp), allocatable :: malla(:,:)     ! ← compartido por TODO el programa
end module
```

**Un módulo con variables es estado global**, así que **dos peticiones concurrentes en el mismo proceso se
pisan** (clase 136).

Y la solución práctica, que además es la del cierre de esta clase: **un proceso por cálculo**. Es más
caro y es simple, aislado y correcto — y para trabajos de minutos, el coste de arrancar un proceso es
irrelevante.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Servicio is
   N : Integer;
begin
   Get (N);

   Put_Line ("respuesta=200 datos=" &
             Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both));
end Servicio;
```

**Ada como componente de servicio.** Ada tiene, para esta clase, una capacidad que ningún otro de esta
página trae en el lenguaje: **el control de la concurrencia y del tiempo, declarado** (clase 135).

```ada
task type Trabajador is
   entry Atender (P : Peticion; R : out Respuesta);
end Trabajador;

Conjunto : array (1 .. 16) of Trabajador;      --  un conjunto FIJO de trabajadores
```

**Un número fijo de tareas es una decisión declarada**, no un parámetro de configuración que alguien
ajusta a ojo.

Y la segunda regla del cierre —**cada petición con un plazo**— está en el lenguaje:

```ada
select
   Trabajador.Atender (P, R);
or
   delay 2.0;                                  --  ← el plazo, en la sentencia
   R := Respuesta_Tiempo_Agotado;
end select;
```

**`select ... or delay` es una llamada con tiempo límite integrada en la sintaxis** — que en la mayoría de
los lenguajes de esta página requiere una biblioteca y disciplina.

Y merece señalar por qué eso importa tanto en un servicio y no solo en tiempo real: **sin plazo, un
cliente lento o un recurso bloqueado agota los trabajadores**, y el servicio deja de responder a todos.

Es el fallo en cascada clásico, y **el plazo por petición es la defensa más barata**.

Y Ada tiene el mecanismo que evita el otro fallo clásico y que merece nombrarse: **el objeto protegido con
cola de entrada acotada**.

```ada
protected Cola is
   entry Poner (P : Peticion) when Longitud < Maximo;    --  ← rechaza si está llena
   entry Sacar (P : out Peticion) when Longitud > 0;
   ...
end Cola;
```

**Una cola con límite ejerce contrapresión**: cuando el servicio va saturado, **rechaza rápido en lugar de
acumular** — que es lo que convierte una sobrecarga en una caída.

Es una idea que la industria ha ido adoptando con nombres nuevos —*backpressure*, *load shedding*,
*circuit breaker*— y que en Ada es una guarda en una entrada.

Y para el componente de API en sí, el ecosistema tiene servidores HTTP —AWS de AdaCore, Gnoga—, aunque
merece la honestidad: **Ada rara vez es el componente de API**. Su sitio es lo que hay detrás, y la
frontera se pone donde empieza el requisito de determinismo.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Servicio;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('respuesta=200 datos=', IntToStr(N));
end.
```

**Pascal como componente de servicio.** El ecosistema Pascal tiene servidores HTTP competentes, y uno
merece destacarse por sus decisiones de diseño: **mORMot**.

```pascal
type
  ICalculo = interface(IInvokable)
    ['{...}']
    function Sumar(A, B: Integer): Integer;
  end;

  TCalculo = class(TInjectableObjectRest, ICalculo)
  public
    function Sumar(A, B: Integer): Integer;
  end;

Servidor.ServiceDefine(TCalculo, [ICalculo], sicShared);
```

**Y la propiedad que merece explicarse es `sicShared`**, porque es exactamente la pregunta del "por qué"
de esta clase: **dónde vive el estado**.

```text
sicSingle      → una instancia por LLAMADA. Sin estado. Lo más escalable.
sicShared       → una instancia compartida por todos. Hay que sincronizar.
sicClientDriven  → una instancia por CLIENTE, con estado de sesión en el servidor.
sicPerSession     → por sesión
sicPerThread       → por hilo
```

**El modelo de instancia se declara al registrar el servicio**, y **esa declaración es la decisión de
arquitectura del cierre de esta clase**, hecha explícita.

Es un buen diseño: **obliga a elegir conscientemente** en lugar de que el estado se acumule por descuido
(clase 163).

Y el resto del ecosistema:

| Herramienta | Notas |
|---|---|
| **mORMot** | ORM, servicios, JSON rápido, autenticación; muy completo |
| **fpWeb / Brook** | servidores HTTP de Free Pascal |
| **Indy** | veterano, con sockets y protocolos |
| **DataSnap** | el de Embarcadero |
| **Horse** | minimalista, al estilo de Express |

Y merece señalar la ventaja de este componente en Pascal para el proyecto de esta parte, y es la de la
clase 164: **el binario es autocontenido y arranca al instante**.

```bash
./miapi &          # un fichero, sin runtime que instalar, ~3 MB
```

**En un contenedor** (clase 174) **eso significa una imagen de pocos megabytes** —frente a los cientos de
una con máquina virtual o intérprete— y **un arranque en milisegundos**, que es lo que hace viable
escalar a cero y volver.

Es una ventaja real y poco reconocida de los lenguajes compilados nativos en la arquitectura de servicios
actual.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "respuesta=200 datos=~D~%" n))
```

**Lisp como componente de servicio.** Lisp tiene servidores HTTP maduros, y uno de ellos ilustra bien la
pregunta del "por qué" de esta clase: **Hunchentoot**.

```lisp
(hunchentoot:define-easy-handler (obtener :uri "/pedidos") (id)
  (setf (hunchentoot:content-type*) "application/json")
  (yason:with-output-to-string* ()
    (yason:encode (buscar-pedido (parse-integer id)))))

(hunchentoot:start (make-instance 'hunchentoot:easy-acceptor :port 8080))
```

**Y el modelo de concurrencia de Hunchentoot es un hilo por conexión** — sencillo, y con el límite de
escala conocido.

Y merece contrastar con el otro modelo del ecosistema, porque son las dos familias de esta clase:

| Servidor | Modelo | Escala |
|---|---|---|
| **Hunchentoot** | un hilo por conexión | miles |
| **Woo** (sobre libev) | **bucle de eventos** | decenas de miles |
| **Clack** | abstracción común sobre los dos | la del servidor elegido |

**Clack merece la mención** porque es el PSGI de Perl y el WSGI de Python (clase 149): **una interfaz
común entre servidor y aplicación**, así que la aplicación no depende del servidor.

Es la segunda regla de la clase 166 —**interfaces estrechas**— aplicada al punto más crítico de un
servicio.

Y Lisp aporta a esta clase una capacidad que su modelo hace posible y que la clase 148 ya nombró, y que
aquí merece verse como decisión de arquitectura:

```lisp
(swank:create-server :port 4005)      ; en el servicio EN PRODUCCIÓN
```

**Un servicio Lisp puede diagnosticarse y corregirse en marcha**, sin reiniciar y sin perder el estado que
causó el problema.

**Y esa capacidad choca de frente con la primera regla del cierre de esta clase.**

Porque un servicio que se puede modificar en marcha **es un servicio con estado no reproducible**: dos
copias del mismo servicio pueden tener código distinto, y **la que se reinicie perderá el arreglo**.

Y la conclusión razonable, que es la de la clase 148: **usarlo para diagnosticar, no para desplegar** —y
tratarlo como lo que es: una herramienta excepcional para el peor momento, no una práctica normal.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

puts "respuesta=200 datos=$n"
```

**Tcl como componente de servicio.** Tcl tiene aquí una historia que merece contarse porque fue pionera y
casi nadie la conoce: **AOLserver**.

**A mediados de los noventa, America Online servía uno de los sitios con más tráfico del mundo**, y lo
hacía con un servidor web **con Tcl incrustado** (clase 163).

Y sus decisiones de diseño, en 1995, eran las que hoy se consideran buenas prácticas:

| Decisión de AOLserver | Hoy se llama |
|---|---|
| **Multihilo con conjunto de hilos** | *thread pool* |
| **Intérprete Tcl por hilo, reutilizado** | evitar el arranque por petición |
| **Conjunto de conexiones a base de datos persistente** | *connection pooling* |
| **Caché en memoria compartida entre hilos** | caché de proceso |
| **Guiones recargables sin reiniciar** | recarga en caliente (clase 148) |

**Y el contraste con lo que hacía todo el mundo entonces es lo que lo hace notable: CGI.**

```text
CGI (1993):  cada petición ARRANCA UN PROCESO NUEVO
             que carga el intérprete, conecta a la base, responde y muere.

AOLserver:   hilos reutilizados, intérpretes ya arrancados,
             conexiones ya abiertas.
```

**La diferencia de rendimiento era de dos órdenes de magnitud**, y es la razón por la que aparecieron
`mod_perl`, FastCGI y todos los servidores de aplicaciones que vinieron después.

Y merece señalar el detalle que resuelve la primera regla del cierre y que AOLserver hacía bien: **cada
hilo tiene su propio intérprete, que se limpia entre peticiones**.

```tcl
ns_register_proc GET /pedidos manejadorPedidos
# El intérprete del hilo se reinicializa: las variables de una petición
# NO llegan a la siguiente
```

**Es exactamente la lección de `mod_perl`** (clase 163): **el intérprete se reutiliza, el estado no**.

Y hoy, Tcl sigue teniendo servidores —**NaviServer**, el descendiente vivo de AOLserver, y **tclhttpd**—
y **el sitio de código abierto más grande escrito en Tcl es OpenACS**, que sigue en producción en
universidades.

Es un componente que se elige poco hoy, y su diseño de hace treinta años sigue siendo un buen modelo de lo
que esta clase pide.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "respuesta=200 datos=$n\n";
```

**Perl como componente de servicio.** Perl vivió la evolución completa de esta clase, y contarla es contar
la historia de los servicios web:

```text
1993  CGI            → un proceso por petición. Simple y lentísimo.
1996  mod_perl        → el intérprete DENTRO de Apache (clase 163). Rápido y con estado peligroso.
1996  FastCGI          → procesos persistentes, separados del servidor web
2009  PSGI/Plack        → la INTERFAZ común entre aplicación y servidor
hoy   Starman, Mojolicious, Dancer2
```

**Y PSGI merece el detalle**, porque resolvió un problema de arquitectura que la clase 166 llamaría de
manual:

```perl
# Una aplicación PSGI es una función: recibe un entorno, devuelve una respuesta
my $app = sub {
    my $env = shift;
    return [ 200, ['Content-Type' => 'application/json'], ['{"datos":5}'] ];
};
```

**Tres cosas: código, cabeceras y cuerpo.** Y con eso:

- **La aplicación no depende del servidor**: funciona con Starman, con uWSGI, con Apache o con el servidor
  de desarrollo.
- **Y se puede envolver**: los *middleware* de Plack —registro, compresión, sesiones, autenticación— **son
  funciones que envuelven a la función**.

Es el patrón Decorador (clase 151) aplicado a la petición entera, y es el modelo que hoy tienen Rack,
WSGI, ASGI y los marcos de Go.

Y esta clase debe recoger la lección que `mod_perl` enseñó y que es la primera regla del cierre, porque se
pagó cara (clase 163):

```perl
# ✗ variable de fichero en un intérprete persistente: sobrevive entre peticiones
my $usuario_actual;

# ✓ todo lo de la petición, dentro de la petición
sub manejar { my ($env) = @_; my $usuario = autenticar($env); ... }
```

**El estado que sobrevive a la petición sin quererlo es una fuga entre usuarios**, y en un servicio con
autenticación es un fallo de seguridad grave.

Y el ecosistema moderno lo previene con la forma misma de PSGI: **la aplicación es una función que recibe
todo lo que necesita** — que es, otra vez, buena arquitectura y seguridad siendo la misma propiedad.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "respuesta=200 datos=" << n << '\n';
    return 0;
}
```

**C++ como componente de servicio.** C++ es **el suelo de casi todos los servidores del mundo** —Nginx,
Envoy, HAProxy y los motores de bases de datos— y también se usa directamente cuando la latencia es el
requisito.

```cpp
#include <drogon/drogon.h>          // o Crow, Pistache, Beast, oat++

drogon::app()
    .registerHandler("/pedidos/{id}",
        [](const drogon::HttpRequestPtr& req,
           std::function<void(const drogon::HttpResponsePtr&)>&& cb,
           int id) {
            Json::Value j;
            j["datos"] = id;
            cb(drogon::HttpResponse::newHttpJsonResponse(j));
        })
    .setThreadNum(8)
    .run();
```

**`std::function<void(...)>&& cb` es lo interesante**: la respuesta se entrega por retrollamada, **no se
devuelve** — porque el manejador puede terminar antes de que la respuesta esté lista.

Es el modelo asíncrono, y **es la decisión de arquitectura de esta clase**, así que merece la tabla:

| Modelo | Cómo escala | Coste |
|---|---|---|
| **Proceso por petición** | mal | máximo aislamiento |
| **Hilo por conexión** | miles | 1-8 MB de pila por hilo |
| **Conjunto de hilos + cola** | decenas de miles | complejidad de sincronización |
| **Bucle de eventos** (epoll, io_uring) | **cientos de miles** | código asíncrono, difícil de leer |
| **Corrutinas** (C++20) | como el anterior | **con aspecto síncrono** (clase 134) |

**La última fila es la novedad**, y merece explicarla: **las corrutinas permiten escribir código que
parece secuencial y se ejecuta sobre un bucle de eventos**.

```cpp
drogon::Task<> manejar(HttpRequestPtr req) {
    auto fila = co_await db->execSqlCoro("SELECT ... WHERE id=$1", id);
    co_return respuesta(fila);
}
```

**`co_await` suspende la corrutina sin bloquear el hilo**, así que un solo hilo atiende miles de
peticiones concurrentes **sin que el código parezca asíncrono**.

Es el mismo modelo que Go, Rust con `async`, Python con `asyncio` y Node — y llegó a C++ en 2020.

Y merece cerrar con la advertencia que la clase 153 exige en este componente: **un servicio en C++ expuesto
a Internet procesa entradas hostiles**.

**Cada análisis de cabecera, cada búfer y cada índice es una superficie de ataque**, y por eso los
servidores serios se compilan con desinfectantes en las pruebas, se fuzzean sistemáticamente y se ejecutan
con privilegios mínimos.

Es el componente donde la elección entre C++ y un lenguaje con seguridad de memoria (clase 164) tiene la
consecuencia más directa.

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

dcl-pi SERVICIO;
  n int(10) const;
end-pi;

dsply ('respuesta=200 datos=' + %char(n));

*inlr = *on;
return;
```

**RPG como componente de servicio.** IBM i convierte un programa en servicio sin escribir código de red, y
merece verlo porque el reparto es limpio (clases 158 y 160):

```text
IWS (Integrated Web Services):
   1. se elige un programa o un procedimiento
   2. el asistente lee su PROTOTIPO
   3. y genera el servicio REST, con su OpenAPI
```

**Y el modelo de estado de esta plataforma es el que el cierre de esta clase pide**, por diseño:

```rpgle
*inlr = *on;      // ← al terminar, el programa LIBERA todo su estado
```

**`*INLR` activado hace que el programa cierre ficheros y libere almacenamiento al volver**, así que **la
siguiente llamada empieza limpia**.

Y merece explicar la alternativa, porque es una decisión real que se toma en cada programa:

```text
*INLR = *ON   → estado liberado. Llamada siguiente: arranque completo.
                Más lento por llamada, y SIN estado residual.

*INLR = *OFF  → el programa queda ACTIVO con sus ficheros abiertos.
                Llamadas siguientes rapidísimas.
                Y el estado sobrevive: hay que saber lo que se hace.
```

**Es exactamente el compromiso de `mod_perl` de esta página**, expresado como un indicador del lenguaje —y
en el mundo IBM i **se elige conscientemente**, porque es la diferencia entre un programa de lote y uno de
servicio.

Y la plataforma da el resto de lo que un servicio necesita, sin montarlo:

| Necesidad | Lo da |
|---|---|
| Conjunto de trabajos | los **subsistemas** y los trabajos preiniciados |
| Límite de concurrencia | la definición del subsistema |
| Transacciones | el control de compromiso, integrado (clase 161) |
| Autorización | por objeto y por perfil (clase 153) |
| Registro y métricas | el registro del trabajo y los datos de rendimiento (clase 142) |

**Los trabajos preiniciados merecen la mención** porque son el conjunto de procesos de esta clase: **el
subsistema arranca N trabajos ya listos**, y cada petición toma uno, se ejecuta y lo devuelve — **sin
pagar el arranque**.

Es un conjunto de trabajadores del sistema operativo, configurado con un comando, y es de 1988.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 servicio: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('respuesta=200 datos=' || trim(char(n)));

 end servicio;
```

**PL/I como componente de servicio.** PL/I comparte con COBOL el mundo de CICS e IMS, y esta clase es el
sitio para nombrar el otro monitor de transacciones del mainframe, porque su modelo es distinto y merece
conocerse: **IMS/TM**.

```text
IMS Transaction Manager:
  - el cliente pone un MENSAJE en una cola
  - una REGIÓN DE MENSAJE toma el mensaje y ejecuta el programa
  - el programa lee el mensaje, procesa y pone la respuesta en otra cola
  - y termina
```

**Y esa arquitectura es de paso de mensajes con colas, no de llamada síncrona** — lo que la clase 161
señalaba como la forma más robusta.

Y sus propiedades merecen destacarse porque son las que hoy se buscan:

- **Desacoplamiento**: el cliente no espera a que haya una región libre; el mensaje espera en la cola.
- **Contrapresión natural**: si la cola crece, se ve y se puede actuar (clase 168, Ada).
- **Y recuperación**: si la región cae a mitad, **el mensaje sigue en la cola** y se vuelve a procesar.

**La tercera es la que distingue una arquitectura de colas de una de llamadas**, y es la razón de que los
sistemas que no pueden perder trabajo la usen.

Y el programa PL/I en ese modelo es **sin estado por construcción**:

```pli
 call plitdli(tres, 'GU      ', pcb_io, mensaje);   /* leer el mensaje */
 /* ... procesar ... */
 call plitdli(tres, 'ISRT    ', pcb_io, respuesta);  /* poner la respuesta */
```

**El programa lee, procesa y termina**, y **todo lo que hay que recordar está en la base de datos** — que
es la primera regla del cierre de esta clase, impuesta por el modelo.

Y merece cerrar con la observación general que estas dos columnas del mainframe permiten: **las dos
arquitecturas de servicio que la industria usa hoy —la síncrona con conjunto de procesos y la asíncrona
con colas— existían en 1970 y se llamaban CICS e IMS**.

Y la elección entre ellas se hacía con los mismos criterios que hoy: **latencia y acoplamiento frente a
robustez y desacoplamiento**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SERVICIO ; Componente de API -- clase 168
 read n
 write "respuesta=200 datos=", n, !
 quit
```

**M como componente de servicio.** El mundo M tiene un modelo de servicio propio y muy longevo, y esta
clase es el sitio para verlo con ojos de arquitectura: **el RPC Broker de VistA** (clase 155).

```text
El cliente abre un SOCKET al servidor M.
El servidor arranca UN PROCESO M por conexión.
Ese proceso se queda vivo mientras dure la sesión,
y atiende las RPC que el cliente pida.
```

**Y eso es un proceso por cliente con estado en el proceso** — exactamente lo que la primera regla del
cierre de esta clase desaconseja.

Y merece explicar por qué funcionó de todos modos durante veinticinco años, porque la razón es
instructiva:

```text
El "estado" del proceso M no es realmente estado:
  las variables locales duran poco, y TODO lo importante está en globals.

Así que un proceso que muere pierde muy poco,
y el cliente reconecta y sigue.
```

**Cuando el estado vive en la base de datos** (clase 161), **el modelo de proceso importa mucho menos** —
que es, dicho al revés, la primera regla del cierre confirmada.

Y la evolución moderna de este componente merece nombrarse porque es hacia donde va el ecosistema:

| Capa | Notas |
|---|---|
| **RPC Broker** | el histórico: socket, protocolo propio, proceso por cliente |
| **VistA FHIR / VX-API** | REST con contratos estándar (clase 160) |
| **YottaDB + Go/Python** | **el servicio se escribe fuera y usa las globals** (clase 156) |
| **IRIS con REST nativo** | servicios definidos en el propio entorno |

**Y la tercera fila es el cambio de fondo**: el componente de API deja de estar en M.

```text
Antes:  M es el lenguaje, la base de datos y el servidor.
Hoy:    M es la base de datos; el servicio lo escribe Go o Python;
        y la lógica clínica sigue en M, llamada desde ahí.
```

**Es el patrón del estrangulador** (clase 150) **aplicado por capas**: primero salió la presentación,
después la API, y la lógica clínica —que es lo validado— se queda.

Y esa secuencia es transferible a cualquier sistema heredado: **se moderniza de fuera hacia dentro**,
porque lo de fuera cambia más y arriesga menos.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'respuesta=200 datos=', n printString; cr.
```

**Smalltalk como componente de servicio.** Smalltalk aportó a esta clase una de las ideas más originales
de la historia de la web, y merece contarla porque plantea la pregunta del "por qué" desde el otro lado:
**Seaside**.

**El problema que Seaside atacó** es real y conocido: **la web rompe el flujo de control**.

```text
Un formulario de tres pasos en un servidor sin estado obliga a:
  - guardar en qué paso está el usuario
  - reconstruir el contexto en cada petición
  - manejar el botón "atrás" y las ventanas duplicadas
  - y todo eso convierte una función en una máquina de estados
```

**Y la solución de Seaside fue usar continuaciones** (clase 127):

```smalltalk
| nombre direccion confirmado |
nombre := self request: '¿Cómo te llamas?'.
direccion := self request: '¿Dirección?'.
confirmado := self confirm: 'Enviar a ', direccion, '?'.
confirmado ifTrue: [ self enviar ].
```

**Ese código parece un programa de consola y es una aplicación web de cuatro páginas.**

Y funciona porque **`self request:` captura la continuación** —el resto del cálculo, que en Smalltalk es
un objeto (clase 127)— **la guarda asociada a una URL, y la reanuda cuando llega la respuesta**.

Y merece señalar las dos consecuencias, porque son exactamente el compromiso de esta clase:

**A favor**: **el botón atrás y las ventanas duplicadas funcionan solos**, porque cada URL tiene su propia
continuación. Es algo que la mayoría de las aplicaciones web sigue resolviendo mal.

**En contra**: **el estado está en el proceso** —las continuaciones viven en memoria—, así que **el
reparto de carga exige sesiones pegajosas** y **reiniciar el servidor tira todas las sesiones**.

Es la primera regla del cierre de esta clase incumplida a propósito, y con los ojos abiertos: **se cambia
escalabilidad por una programación mucho más simple**.

Y merece la valoración justa: **para una aplicación interna con cientos de usuarios es un intercambio
excelente**; para un servicio público con millones, no.

Y su influencia fue real: **las continuaciones web aparecieron después en Rails, en Racket y en varios
marcos de investigación**, y el problema que Seaside identificó —**que la web obliga a invertir el flujo
de control**— sigue siendo la razón de la complejidad de las aplicaciones web modernas.

---

## Y de vuelta a la clase

Lo transferible: **un servicio bien hecho no guarda estado de sesión en el proceso**. Esa única decisión
es la que permite arrancar más copias, reiniciar una sin que nadie lo note, y desplegar por fases (clase
148). El estado va a la base de datos, a una caché compartida o al propio cliente, firmado. Y las otras
dos reglas que aparecen en toda esta página: **cada petición es una unidad de trabajo con un límite de
tiempo**, porque sin plazo un cliente lento agota el servicio; y **todo lo que se responde está en el
contrato** (clase 160), incluidos los errores — que son parte de la API y no un accidente.

⏮️ [Volver a la clase 168](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
