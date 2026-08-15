# -*- coding: utf-8 -*-
"""Parte 11, lote B — clases 168 a 170. Ver `vivos_parte11.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 168 — Componente de API: servicio backend
# ---------------------------------------------------------------------------
SPECS["168"] = dict(
    gancho="""
Una respuesta de servicio: `respuesta=200 datos=5`. Un código de estado y un cuerpo, que es la forma que
ha tomado casi toda la comunicación entre sistemas. Y estos lenguajes tienen aquí una perspectiva que
conviene: **el servidor de aplicaciones no lo inventó la web**. **CICS es de 1969**, y ya hacía lo que un
servidor moderno: recibir peticiones, mantener un conjunto de procesos, gestionar transacciones,
controlar el acceso y responder — con miles de terminales conectados.
""",
    porque="""
Aquí el concepto es el **servicio como componente**, y estos lenguajes lo enseñan porque **han sido
servidores durante décadas y con modelos muy distintos**: transacciones cortas con estado externo
(CICS), procesos por conexión (CGI), hilos con conjunto reutilizable (AOLserver), bucle de eventos
(Tcl), y continuaciones (Seaside).

Y aparece la pregunta que decide la arquitectura de un servicio: **¿dónde vive el estado entre una
petición y la siguiente?** Porque de eso dependen la escala, el reparto de carga y lo que pasa cuando un
proceso muere.
""",
    cierre="""
Lo transferible: **un servicio bien hecho no guarda estado de sesión en el proceso**. Esa única decisión
es la que permite arrancar más copias, reiniciar una sin que nadie lo note, y desplegar por fases (clase
148). El estado va a la base de datos, a una caché compartida o al propio cliente, firmado. Y las otras
dos reglas que aparecen en toda esta página: **cada petición es una unidad de trabajo con un límite de
tiempo**, porque sin plazo un cliente lento agota el servicio; y **todo lo que se responde está en el
contrato** (clase 160), incluidos los errores — que son parte de la API y no un accidente.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
program servicio
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0)') 'respuesta=200 datos=', n
end program servicio
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
program Servicio;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('respuesta=200 datos=', IntToStr(N));
end.
""", """
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
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "respuesta=200 datos=~D~%" n))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

puts "respuesta=200 datos=$n"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "respuesta=200 datos=$n\\n";
""", """
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
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "respuesta=200 datos=" << n << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SERVICIO;
  n int(10) const;
end-pi;

dsply ('respuesta=200 datos=' + %char(n));

*inlr = *on;
return;
""", """
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
"""),
        "pli": ("""
 servicio: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('respuesta=200 datos=' || trim(char(n)));

 end servicio;
""", """
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
"""),
        "mumps": ("""
SERVICIO ; Componente de API -- clase 168
 read n
 write "respuesta=200 datos=", n, !
 quit
""", """
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
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'respuesta=200 datos=', n printString; cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 169 — Componente web (frontend)
# ---------------------------------------------------------------------------
SPECS["169"] = dict(
    gancho="""
Un contador de elementos y un `render=ok`. Es lo que hace un frontal: **coger datos y pintarlos**. Y esta
clase tiene una premisa que conviene decir de entrada: **ninguno de estos doce lenguajes es hoy la
elección para el componente web, y todos han pintado interfaces**. Unos generando HTML desde el servidor,
otros con bibliotecas gráficas propias, y varios —de forma sorprendente— **ejecutándose dentro del
navegador** (clase 162).
""",
    porque="""
Aquí el concepto es la **capa de presentación como componente**, y estos lenguajes la enseñan porque
**vivieron todas las generaciones**: pantallas de bloques (3270, 5250), interfaces de escritorio (Tk,
VCL), HTML generado en el servidor (CGI, mod_perl), y hoy WebAssembly. Y esa historia deja una lección
que la moda oculta: **cada generación resolvió los mismos problemas** —estado, validación, navegación,
rendimiento— **y las soluciones se parecen mucho más de lo que su vocabulario sugiere**.

Y aparece la decisión de siempre: **cuánta lógica vive en el cliente**.
""",
    cierre="""
Lo transferible: **la validación del cliente es comodidad; la del servidor es la única real** (clase 153).
Todo lo que se comprueba en el navegador se puede saltar, así que **se comprueba dos veces o no se
comprueba**. Y las otras dos reglas que atraviesan la página: **el frontal no debe conocer la estructura
interna del sistema**, sino un contrato (clase 160), porque es el componente que más cambia y no puede
arrastrar a los demás; y **el estado de la interfaz es del cliente y el de negocio es del servidor** —
mezclarlos es el origen de la mayoría de los fallos difíciles de una aplicación web.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. FRONTAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED
    DISPLAY "items=" FUNCTION TRIM(ED) " render=ok"
    STOP RUN.
""", """
**COBOL y la capa de presentación.** COBOL tiene una historia con las interfaces que merece contarse
porque **inventó el formulario y la validación declarativa**: **las pantallas BMS de CICS**.

```text
MAPA    DFHMSD TYPE=MAP,MODE=INOUT,LANG=COBOL,TIOAPFX=YES
PANT1   DFHMDI SIZE=(24,80)
NOMBRE  DFHMDF POS=(3,10),LENGTH=20,ATTRB=(UNPROT,IC),
               INITIAL='                    '
IMPORTE DFHMDF POS=(5,10),LENGTH=9,ATTRB=(UNPROT,NUM),PICIN='9(7)V99'
MENSAJE DFHMDF POS=(23,1),LENGTH=79,ATTRB=(PROT,BRT)
```

**Ese fichero define la pantalla**, y de él se genera **una estructura COBOL con un campo por control**.

Y merece enumerar lo que ya hacía, porque es exactamente lo que un formulario web necesita:

| Atributo | Qué hace |
|---|---|
| **`UNPROT` / `PROT`** | editable o solo lectura |
| **`NUM`** | **el terminal solo acepta dígitos**: validación en el cliente |
| **`IC`** | dónde va el cursor al abrir |
| **`BRT` / `DRK`** | resaltado, y **campos ocultos para contraseñas** |
| **`PICIN` / `PICOUT`** | formato de entrada y de salida |
| **`MDT`** | **marca de campo modificado**: solo se transmite lo que cambió |

**La última merece destacarse** porque es una optimización que la web redescubrió: **el terminal 3270
envía solo los campos modificados**, no la pantalla entera.

**Es exactamente la idea del DOM virtual y de las actualizaciones parciales**, en un protocolo de 1972 y
por la misma razón: **el ancho de banda era caro**.

Y la arquitectura de aquello es la del cierre de esta clase, y conviene verla:

```text
El terminal valida el TIPO (NUM impide letras).
El programa valida TODO lo demás en el servidor.
El estado de la conversación va en la COMMAREA, no en el terminal (clase 168).
```

**Validación doble, estado en el servidor, y el terminal sin lógica de negocio** — las tres reglas del
cierre, cincuenta años antes de que hubiera navegadores.

Y hoy, el frontal de un sistema COBOL es web o móvil, y habla con él por una API (clase 160). **La
lección que queda es que la pantalla vieja hacía bien lo que muchas aplicaciones nuevas hacen mal**:
tenía un contrato declarado, generado y comprobado.
"""),
        "fortran": ("""
program frontal
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A)') 'items=', n, ' render=ok'
end program frontal
""", """
**Fortran y la capa de presentación.** Fortran no pinta interfaces, y merece decirlo sin rodeos — y a
cambio, esta clase es el sitio para hablar de lo que sí produce: **visualización científica**.

```text
El "frontal" de un cálculo Fortran no es una interfaz de usuario:
  es una visualización de campos escalares y vectoriales en tres dimensiones,
  con millones de celdas y con evolución temporal.
```

Y la arquitectura habitual es la de la clase 155, con la frontera en el fichero:

```text
Fortran  →  NetCDF / HDF5 (clase 159)  →  ParaView / VisIt / VTK  →  imagen
                                        →  Python + matplotlib
                                        →  y hoy: navegador con WebGL
```

**Y esa separación es un buen ejemplo de la segunda regla del cierre**: **el visualizador no conoce el
programa que generó los datos** — solo el formato, que es autodescriptivo (clase 159).

Y por eso **el mismo ParaView visualiza salidas de decenas de códigos distintos**, y por eso un resultado
de hace quince años se puede volver a mirar.

Y hay una técnica de este dominio que merece nombrarse porque resuelve un problema que la web también
tiene: **la visualización *in situ***.

```text
Problema: una simulación genera 10 TB de datos por ejecución.
          Escribirlos y luego visualizarlos es inviable.

Solución: el visualizador se ENLAZA con el código de simulación
          y genera las imágenes MIENTRAS se calcula (Catalyst, Ascent).
```

**Es mover el cálculo hacia el dato en lugar del dato hacia el cálculo**, y es la misma idea que el
renderizado en el servidor y que los cálculos en el borde.

Y para el proyecto de esta parte, la aportación de esta columna es una recomendación concreta: **el
componente de cálculo no debe generar la presentación**.

Debe **emitir datos con un formato declarado**, y que el frontal —web, cuaderno o herramienta de
visualización— decida cómo se ven. Es la separación de la clase 149, y aquí tiene una consecuencia
práctica inmediata: **la misma salida sirve para la gráfica, para el informe y para el análisis
posterior**.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Frontal is
   N : Integer;
begin
   Get (N);

   Put_Line ("items=" & Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both) &
             " render=ok");
end Frontal;
""", """
**Ada y la capa de presentación.** Ada tiene interfaces gráficas —GtkAda, Gnoga, AWS con web— y merece
plantear la pregunta que su dominio hace inevitable y que esta clase debe recoger: **¿qué pasa cuando la
interfaz es crítica?**

```text
Una pantalla de cabina de avión, un panel de control de una central
o el display de un desfibrilador NO son "frontales":
  son componentes con requisitos de seguridad.
```

Y las reglas que esos sistemas aplican merecen conocerse, porque son la versión extrema del cierre de
esta clase:

| Regla | Motivo |
|---|---|
| **La interfaz no decide nada** | solo muestra y transmite; la lógica está detrás |
| **Todo dato mostrado tiene una marca de frescura** | un valor congelado es peor que ninguno |
| **Los estados se pintan de forma inequívoca** | nada de depender solo del color |
| **La entrada se confirma en el sistema, no en la pantalla** | la validación real está detrás |
| **Y la interfaz no puede bloquear al control** | particiones de tiempo (clase 165) |

**La segunda merece el detalle**, porque es un fallo real y de los peores: **una pantalla que sigue
mostrando el último valor recibido cuando el sensor ha dejado de enviar** hace creer que todo va bien.

**La defensa es que el dato lleve su instante y que la pantalla lo marque como obsoleto** — y es
transferible a cualquier panel de control, incluidos los de un sistema informático normal.

Y hay una norma que este mundo tiene y que el resto no: **ARINC 661**, que **separa la definición de la
interfaz de la aplicación**.

```text
Un fichero de definición describe los widgets de la pantalla.
Un "servidor de cabina" certificado los pinta.
Y la aplicación solo ENVÍA DATOS y RECIBE EVENTOS.
```

**Es la separación de la primera regla del cierre llevada al extremo**: la aplicación **no puede** pintar
nada que no esté en la definición, y esa definición se certifica por separado.

Y merece la observación general: **es lo mismo que un contrato de API entre frontal y servicio** (clase
160), con la diferencia de que aquí **el sistema lo hace cumplir** — y en una aplicación normal lo hace
cumplir la disciplina.
"""),
        "pascal": ("""
program Frontal;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('items=', IntToStr(N), ' render=ok');
end.
""", """
**Pascal y la capa de presentación.** Aquí Pascal tiene mucho que decir, porque **Delphi definió cómo se
construyen las interfaces de escritorio** y su modelo sigue vivo en varias herramientas.

```pascal
{ El diseñador visual, el inspector de objetos y los eventos }
procedure TForm1.Button1Click(Sender: TObject);
begin
  Label1.Caption := IntToStr(ListBox1.Items.Count) + ' items';
end;
```

**Y las tres ideas que Delphi popularizó merecen nombrarse** porque están en todas partes:

**Una, el componente visual con propiedades editables** en un inspector —y persistidas en el `.dfm`
(clase 159)—.

**Dos, la programación dirigida por eventos con métodos de objeto** (clase 151), gracias a `of object`
que hace que el manejador lleve su formulario consigo.

**Y tres, el enlace de datos**: un control conectado a un origen de datos que **se actualiza solo**.

```pascal
DBGrid1.DataSource := DataSource1;
DataSource1.DataSet := Query1;
```

**Ese enlace bidireccional entre datos e interfaz es lo que hoy hacen Vue, Angular y todos los marcos
reactivos** (clase 120) — y en Delphi es de 1995.

Y el ecosistema Pascal llega hoy a la web por los dos caminos de la clase 162:

| Camino | Notas |
|---|---|
| **`pas2js`** | Pascal **a JavaScript**, con acceso al DOM |
| **WebAssembly** | `fpc -Twasi -Pwasm32`, con generador propio |
| **TMS Web Core** | marco comercial: diseñador visual que produce web |
| **Lazarus + LCL** | escritorio nativo, multiplataforma |

**TMS Web Core merece la mención** porque persigue lo mismo que Delphi en 1995: **arrastrar controles y
que salga una aplicación**, ahora en el navegador.

Y esta clase debe recoger la advertencia que ese modelo trae y que la clase 149 ya señaló: **el diseñador
visual empuja a poner la lógica en el manejador del botón**.

**Y en un frontal eso choca con la segunda regla del cierre**: la lógica de negocio en el cliente **se
duplica, se desincroniza y se puede saltar** (clase 153). El manejador debe llamar a un servicio, no
calcular.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "items=~D render=ok~%" n))
""", """
**Lisp y la capa de presentación.** Lisp llega al navegador por varios caminos, y esta clase es el sitio
para una idea suya que la industria adoptó sin saberlo: **generar el marcado con el propio lenguaje**.

```lisp
(cl-who:with-html-output-to-string (s)
  (:div :class "pedidos"
    (:h1 "Pedidos")
    (:ul
      (dolist (p pedidos)
        (:li (str (pedido-nombre p)))))))
```

**El HTML se escribe como estructuras de Lisp**, así que:

- **No hay lenguaje de plantillas que aprender**: es el mismo lenguaje.
- **Se puede componer con funciones**: un fragmento es un valor.
- **Y es imposible generar marcado mal formado**, porque la estructura es un árbol.

**Y esa última propiedad merece destacarse porque resuelve un fallo de seguridad real**: **la inyección de
HTML** (clase 153). Si el marcado se construye concatenando cadenas, **un dato con `<script>` se ejecuta**;
si se construye como árbol, **la biblioteca escapa el texto**.

Es el mismo argumento que las consultas parametrizadas frente al SQL concatenado (clase 163), aplicado a
la presentación — y es la razón por la que JSX, Hiccup y los constructores de elementos ganaron a las
plantillas de texto.

Y los caminos de Lisp al navegador:

| Vía | Notas |
|---|---|
| **cl-who / Spinneret** | generación de HTML desde el servidor |
| **Parenscript** | **escribe JavaScript con sintaxis de Lisp** |
| **JSCL / Clasp** | Common Lisp en el navegador (clase 162) |
| **ClojureScript** | el caso de éxito real: Lisp compilado a JavaScript |
| **Hoot (Guile)** | Scheme a WebAssembly con WasmGC |

**ClojureScript merece la mención** porque es el único de esta lista con adopción industrial, y **de él
salió una idea que el resto del mundo web adoptó**: **el estado de la aplicación como un único valor
inmutable**, del que la interfaz es una función.

```text
interfaz = f(estado)
```

**Esa formulación —que Re-frame y Redux popularizaron— es la tercera regla del cierre de esta clase**:
**separar el estado del pintado** hace que la interfaz sea predecible y depurable, porque **se puede
reconstruir a partir del estado**.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

puts "items=$n render=ok"
""", """
**Tcl y la capa de presentación.** Tcl tiene aquí un mérito histórico que merece contarse: **Tk, de 1991,
fue el primer kit de interfaces gráficas verdaderamente multiplataforma y fácil**.

```tcl
package require Tk

label .titulo -text "Pedidos"
listbox .lista
button .cerrar -text "Cerrar" -command exit

pack .titulo .lista .cerrar -fill both -expand 1
```

**Cuatro líneas y hay una ventana funcionando en Linux, Windows y macOS.**

Y merece explicar por qué eso fue tan influyente en su momento: **en 1991, hacer una interfaz gráfica
significaba escribir cientos de líneas de C con Xlib o con la API de Windows**, distintas en cada
plataforma.

**Tk lo redujo a un lenguaje declarativo con gestores de disposición**, y su influencia fue enorme:

```text
Tkinter (Python), Perl/Tk, Ruby/Tk, Tcl/Tk en R...
Tk se convirtió en el kit gráfico "por defecto" de media docena de lenguajes.
```

**Y sigue siéndolo**: `tkinter` viene con Python, y es con lo que se hacen decenas de miles de
herramientas internas.

Y las dos ideas de Tk que merecen destacarse porque son de diseño y siguen vigentes:

**Los gestores de disposición**: `pack`, `grid` y `place` — **la posición no se fija en píxeles, se
declara una relación** —"esto se expande, aquello se pega arriba"—.

**Es exactamente lo que hacen Flexbox y Grid en CSS**, treinta años después, y por la misma razón: **las
ventanas cambian de tamaño y las pantallas son distintas**.

**Y la variable enlazada**:

```tcl
entry .campo -textvariable ::nombre
# cambiar ::nombre actualiza el campo, y escribir en el campo actualiza ::nombre
```

**Enlace bidireccional entre una variable y un control**, igual que Delphi en esta página y que los
marcos reactivos actuales.

Y merece cerrar con lo que esta clase debería concluir: **los problemas de las interfaces no han cambiado**
—disposición adaptable, enlace de datos, eventos, validación— y **cada generación los ha resuelto con el
mismo puñado de ideas**, redescubiertas con vocabulario nuevo.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "items=$n render=ok\\n";
""", """
**Perl y la capa de presentación.** Perl fue **el lenguaje con el que se construyó la primera web
dinámica**, y esta clase debe contarlo porque de ahí salen varias cosas que seguimos usando.

```perl
#!/usr/bin/perl
use CGI;
my $q = CGI->new;
print $q->header('text/html'),
      $q->start_html('Pedidos'),
      $q->h1('Pedidos'),
      $q->ul(map { $q->li($_) } @pedidos),
      $q->end_html;
```

**CGI.pm, de Lincoln Stein (1995), fue durante una década el módulo más usado de CPAN**, y con él se
hicieron los primeros formularios, buscadores, foros y tiendas de la web.

Y merece nombrar lo que aquella generación estableció y que sigue vigente:

| Idea | Sigue |
|---|---|
| **Formularios HTML con `POST`** | igual |
| **Cookies de sesión** | igual |
| **Parámetros con codificación de URL** | igual |
| **Cabeceras de tipo de contenido** | igual |
| **Y la validación en el servidor, siempre** | **la primera regla del cierre** |

Y también lo que se hizo mal y que costó años corregir, porque es la lección de esta clase:

```perl
# ✗ el fallo de seguridad más común de aquella web
print "<p>Hola, $nombre</p>";       # si $nombre contiene <script>, se EJECUTA
```

**Eso es *cross-site scripting***, y fue —y sigue siendo— una de las vulnerabilidades más extendidas.

**Y la defensa es la que la explicación de Lisp de esta página describe**: **escapar por defecto**, que es
lo que hacen las plantillas modernas.

```perl
use Template;                       # Template Toolkit
# [% nombre | html %]  ← el filtro de escape, explícito

# Y los marcos modernos:
use Mojolicious::Lite;
get '/pedidos' => sub { $_[0]->render(json => \\@pedidos) };
```

**Mojolicious escapa por defecto** y hay que pedir explícitamente lo contrario — que es la forma correcta
de una API insegura: **que lo peligroso sea lo que hay que escribir**.

Y merece cerrar con la observación sobre la evolución del papel de este componente, que Perl vivió entera:

```text
1995: el servidor genera TODO el HTML. El navegador solo pinta.
2005: AJAX. El navegador pide trozos y actualiza partes.
2015: el navegador tiene la aplicación; el servidor solo da JSON.
2020: y vuelta parcial al servidor, por rendimiento y por accesibilidad.
```

**El péndulo ha ido y vuelto**, y lo que no ha cambiado en treinta años es la primera regla del cierre:
**la validación del servidor es la única que cuenta**.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "items=" << n << " render=ok" << '\\n';
    return 0;
}
""", """
**C++ y la capa de presentación.** C++ es, otra vez, **el suelo**: los navegadores, los motores de
renderizado y los kits gráficos están escritos en él.

```text
Chromium / Blink   →  C++
WebKit              →  C++
Gecko                →  C++ y Rust
Skia (el renderizador de Chrome y Android)  →  C++
Qt, wxWidgets, GTK (C)  →  los kits de escritorio
```

**Así que cuando esta clase habla del componente web, C++ está debajo aunque no aparezca.**

Y C++ sí llega al navegador directamente por la vía de la clase 162, con casos que merecen recordarse:
**Figma, AutoCAD web, Google Earth y los motores de juego**.

Y hay un modelo de interfaz que merece explicarse porque viene de los juegos y ha influido mucho: **la
interfaz de modo inmediato**.

```cpp
// Dear ImGui: la interfaz se DECLARA cada fotograma
if (ImGui::Begin("Pedidos")) {
    ImGui::Text("items=%d", (int)pedidos.size());
    if (ImGui::Button("Recargar")) recargar();
    ImGui::End();
}
```

**No hay objetos de widget que crear, guardar y destruir**: **cada fotograma se dice qué debe haber en
pantalla**, y la biblioteca lo pinta y devuelve los eventos.

Y merece señalar el parecido con la web moderna, porque es exactamente el mismo modelo:

```text
Modo inmediato (ImGui):  interfaz = f(estado), redibujada cada fotograma
React:                     interfaz = f(estado), reconciliada cada cambio
```

**Los dos parten de la misma observación: mantener sincronizados un árbol de objetos de interfaz y un
estado es la fuente de la mayoría de los fallos**, y es más simple **volver a declarar la interfaz
entera** y dejar que algo optimice la diferencia.

Es la tercera regla del cierre de esta clase —**separar el estado del pintado**— convertida en modelo de
programación, y aparece de forma independiente en dos mundos que apenas se hablan.

Y la contrapartida es la misma en los dos: **hay que redibujar o reconciliar**, y eso cuesta — que es la
razón de que existan el DOM virtual, los memos y los `shouldComponentUpdate`.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi FRONTAL;
  n int(10) const;
end-pi;

dsply ('items=' + %char(n) + ' render=ok');

*inlr = *on;
return;
""", """
**RPG y la capa de presentación.** IBM i tiene su propia generación de pantallas —**los ficheros de
pantalla 5250**, hermanos de los mapas BMS de COBOL en esta página— y su modernización es un caso de
estudio de esta clase.

```text
     A          R PANTALLA1
     A                                  1  30'Pedidos'
     A            CLIENTE       10A  B  5 10CHECK(ME)
     A            IMPORTE        9Y 2B  7 10EDTCDE(J)
     A                                     ERRMSG('Cliente no válido' 51)
```

**Y de nuevo, la validación básica la hace el terminal** —`CHECK(ME)` obliga a rellenar, `EDTCDE` da el
formato— **y la de negocio, el programa**.

Y la modernización de esas pantallas ha pasado por tres fases que merecen conocerse porque el patrón se
repite en cualquier sistema heredado:

| Fase | Qué hace | Valoración |
|---|---|---|
| **1. Refaceado automático** | traduce la pantalla 5250 a HTML al vuelo | rápido, y **es la misma aplicación con otra piel** |
| **2. Reescribir la interfaz** | una web nueva que llama al programa por API | correcto, y **exige separar la lógica** (clase 149) |
| **3. Web nativa desde el principio** | lo nuevo se escribe web | lo ideal para lo que no existe |

**Y la fase 1 merece la advertencia**, porque es la tentación: **el refaceado no moderniza nada**. La
navegación sigue siendo por pantallas, el flujo sigue siendo el del terminal, y **el resultado suele
gustar menos que la pantalla verde** a quien ya sabía usarla.

**Y su único valor real es de transición**: permite enseñar algo mientras se hace la fase 2.

Y la fase 2 es la que esta parte del curso defiende, y su requisito previo es el de la clase 149:
**separar la lógica de la presentación** para poder llamarla desde otro sitio.

```rpgle
// La lógica, en un procedimiento exportado: la usan la pantalla 5250 Y la web
dcl-proc crearPedido export;
```

**Y con eso, las dos interfaces coexisten** durante los años que dure la transición — que es la propiedad
que hace la migración posible sin apagar nada, y es la segunda regla del cierre de esta clase: **el
frontal no conoce el sistema, conoce un contrato**.
"""),
        "pli": ("""
 frontal: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('items=' || trim(char(n)) || ' render=ok');

 end frontal;
""", """
**PL/I y la capa de presentación.** PL/I comparte el mundo de las pantallas de bloques con COBOL en esta
página, y esta clase es el sitio para explicar una propiedad de aquella arquitectura que merece
rescatarse, porque hoy se echa de menos: **la interacción por bloques**.

```text
Terminal 3270:
  - el usuario rellena TODA la pantalla
  - pulsa ENTER
  - y se transmite UNA vez, solo los campos modificados
  - el servidor procesa y devuelve la pantalla siguiente
```

**Y eso hacía que la aplicación fuera utilizable con 300 milisegundos de latencia** — porque **no había
comunicación mientras se teclea**.

Y merece comparar con lo que ocurre hoy:

```text
Un formulario web moderno puede hacer:
  - una petición por pulsación (autocompletado)
  - una validación por campo al salir de él
  - una comprobación de disponibilidad en tiempo real
  - y varias más para telemetría
```

**Y cada una es un viaje de ida y vuelta que puede fallar.**

Es una observación honesta: **la interfaz por bloques era menos agradable y mucho más robusta**, y la
gente que trabajaba con ella todo el día **era rapidísima**, porque **no había esperas intermedias ni
elementos que se movían**.

Y la lección transferible, que es una de las más útiles de esta clase: **la interactividad tiene un
coste, y conviene decidirlo en lugar de heredarlo**.

Un formulario que valida al enviar es más simple, más rápido de rellenar con teclado y **no deja al
usuario a medias si se cae la red**. Uno que valida campo a campo es más amable para quien no conoce el
dominio.

**Las dos son decisiones legítimas, y depende de quién lo use y cuántas veces al día.**

Y merece cerrar con el dato que lo confirma y que este mundo conoce bien: **en aplicaciones de uso
intensivo** —un centro de atención telefónica, una mesa de contratación, una consulta médica— **los
usuarios expertos prefieren teclado y pantallas densas**, y las modernizaciones que las sustituyen por
interfaces amables con muchos clics **suelen empeorar la productividad**.

Es la primera pregunta que un componente de frontal debería hacerse: **¿quién lo va a usar, y cuántas
horas al día?**
"""),
        "mumps": ("""
FRONTAL ; Componente web -- clase 169
 read n
 write "items=", n, " render=ok", !
 quit
""", """
**M y la capa de presentación.** El mundo VistA vivió la transición de esta clase de forma muy visible, y
merece contarla porque las tres generaciones conviven hoy en los mismos hospitales.

```text
1980s  Terminal de texto, con menús de FileMan  ← todavía en uso
2000s  CPRS: cliente Delphi, hablando por el RPC Broker (clase 168)
2010s+ Web y móvil, sobre FHIR (clase 160)
```

**Y la observación que merece hacerse es la de la columna de PL/I en esta página, y aquí es un hecho
documentado**: **muchos clínicos veteranos prefieren la interfaz de texto**.

```text
La razón no es nostalgia: es que en la pantalla de texto
  - todo está en un sitio fijo, siempre
  - se navega con teclado, sin ratón
  - y una orden de diez pasos se teclea en cinco segundos
```

**Y las interfaces gráficas que las sustituyeron a menudo requerían más clics para lo mismo.**

Es un caso real y bien estudiado, y la lección es la del cierre de esta clase aplicada al diseño: **la
interfaz se diseña para quien la usa, no para quien la compra**.

Y esta clase debe recoger la aportación técnica que este dominio ha hecho y que resuelve la segunda regla
del cierre mejor que la mayoría: **SMART on FHIR**.

```text
Una aplicación clínica de terceros:
  - se autentica con OAuth2 contra el sistema del hospital
  - pide los datos del paciente por FHIR, con permisos acotados
  - y se muestra DENTRO de la historia clínica, como un componente
```

**Es un modelo de complementos con contrato estándar y permisos explícitos** (clase 153), y funciona entre
fabricantes distintos.

**Y eso es exactamente lo que la segunda regla del cierre pide**: el frontal —aquí, una aplicación
entera— **no conoce el sistema, conoce un contrato**, así que **la misma aplicación funciona sobre VistA,
sobre Epic o sobre Cerner**.

Es uno de los pocos ecosistemas donde la interoperabilidad de componentes de interfaz entre fabricantes
funciona de verdad, y merece conocerse como modelo.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'items=', n printString, ' render=ok'; cr.
""", """
**Smalltalk y la capa de presentación.** Y aquí conviene decir lo que esta parte del curso ha ido
repitiendo, porque en esta clase es el origen directo: **la interfaz gráfica con ventanas, iconos, menús
y ratón se inventó en Smalltalk**.

```text
Xerox PARC, Smalltalk-76 y Smalltalk-80:
  - ventanas solapadas y redimensionables
  - menús emergentes
  - el ratón como dispositivo principal
  - copiar y pegar entre aplicaciones
  - el portapapeles
  - y MVC para organizarlo todo (clase 149)
```

**Steve Jobs visitó PARC en 1979, vio Smalltalk funcionando, y de ahí salieron el Lisa y el Macintosh** —
y de ahí, Windows y todo lo demás.

**Cada ventana que se abre hoy en cualquier sistema desciende de eso.**

Y merece señalar la idea de aquel diseño que esta clase debe destacar y que sigue siendo la mejor
respuesta a la tercera regla del cierre: **el modelo no sabe que existe la vista**.

```smalltalk
modelo addDependent: vista.
modelo changed: #total.        "el modelo AVISA; no sabe a quién"
```

**Separar el estado de negocio del estado de la interfaz** es lo que permite tener dos vistas del mismo
dato, deshacer, probar el modelo sin interfaz y cambiar la presentación sin tocar la lógica.

Y Smalltalk llega hoy al navegador por caminos reales:

| Proyecto | Qué es |
|---|---|
| **Seaside** | el marco de continuaciones (clase 168) |
| **Amber / PharoJS** | Smalltalk **compilado a JavaScript** |
| **SqueakJS** | la máquina virtual en el navegador (clase 162) |
| **Scratch** | **construido sobre Squeak**: el lenguaje visual del MIT |

**Y Scratch merece cerrar esta clase**, porque es el descendiente más directo del propósito original de
PARC: **que personas que no son programadores construyan cosas**.

Decenas de millones de niños han escrito su primer programa en un entorno **que nació como una aplicación
Smalltalk**, arrastrando bloques en una interfaz que desciende, en línea recta, de las mismas ideas de
1979.

Es la mejor forma de terminar una clase sobre la capa de presentación: **la interfaz gráfica no se
inventó para hacer bonito el software — se inventó para que más gente pudiera usarlo y modificarlo**, y
ese sigue siendo el criterio con el que conviene juzgarla.
"""),
    },
)

# ---------------------------------------------------------------------------
# 170 — Componente de datos y consultas SQL
# ---------------------------------------------------------------------------
SPECS["170"] = dict(
    gancho="""
Sumar una lista: `total=60`. Es lo que hace un `SUM()` en SQL, y esta clase trata de la decisión que hay
detrás: **quién hace el trabajo con los datos, el lenguaje o la base**. Y aquí hay dos de esta página que
no tienen el problema que todos los demás sufren: **M y Smalltalk con GemStone no tienen desajuste entre
el modelo del lenguaje y el de la base**, porque **su base de datos guarda lo mismo que su lenguaje
manipula**.
""",
    porque="""
Aquí el concepto es el **acceso a datos como componente**, y estos lenguajes lo enseñan porque **cubren
los tres modelos que existen**: el **navegacional** —moverse registro a registro por índices— que
COBOL, RPG y M practican; el **relacional** con SQL embebido, que todos adoptaron; y el **de objetos
persistentes**, que M y GemStone tienen de fábrica.

Y aparece la tensión que ordena la clase: **el desajuste de impedancia** — que las tablas y las
estructuras del lenguaje no encajan, y que treinta años de mapeadores objeto-relacionales han intentado
tapar.
""",
    cierre="""
Lo transferible: **la regla que más rendimiento gana en un sistema con base de datos es pedir por
conjuntos, no por filas**. Un bucle que hace mil consultas cuesta mil viajes; una consulta que devuelve
mil filas cuesta uno — y es la misma diferencia dos órdenes de magnitud (clase 152). De ahí las dos
prácticas: **dejar que la base haga lo que sabe hacer** —filtrar, agregar, ordenar, unir— **en lugar de
traérselo todo y hacerlo en el lenguaje**; y **nunca construir SQL concatenando** (clase 153), que es la
misma regla vista desde la seguridad.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. DATOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  C       PIC X.
01  NUM     PIC S9(9) COMP VALUE 0.
01  TOTAL   PIC S9(9) COMP VALUE 0.
01  ENNUM   PIC 9      VALUE 0.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        MOVE LINEA(I:1) TO C
        IF C IS NUMERIC
            COMPUTE NUM = NUM * 10 + FUNCTION NUMVAL(C)
            MOVE 1 TO ENNUM
        ELSE
            IF ENNUM = 1
                COMPUTE TOTAL = TOTAL + NUM
                MOVE 0 TO NUM
                MOVE 0 TO ENNUM
            END-IF
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED
    DISPLAY "total=" FUNCTION TRIM(ED)
    STOP RUN.
""", """
**COBOL y el componente de datos.** COBOL vivió los dos modelos del "por qué" de esta clase, y merece
verlos juntos porque la comparación es el contenido de la clase.

**El navegacional, con VSAM:**

```cobol
           START CLIENTES KEY >= WS-ID
           PERFORM UNTIL FIN
               READ CLIENTES NEXT
                   AT END SET FIN TO TRUE
               END-READ
               ADD CLI-IMPORTE TO WS-TOTAL
           END-PERFORM
```

**Y el relacional, con SQL embebido:**

```cobol
           EXEC SQL
               SELECT SUM(IMPORTE) INTO :WS-TOTAL
                 FROM CLIENTES
                WHERE ZONA = :WS-ZONA
           END-EXEC
```

**Y la diferencia es la del cierre de esta clase**: el primero trae **todas las filas al programa** y suma
una a una; el segundo **suma en la base y trae un número**.

Con un millón de filas, **la diferencia es de dos órdenes de magnitud** — y no por el lenguaje, sino por
cuántas veces se cruza la frontera (clase 155).

Y merece decir cuándo el navegacional sigue siendo correcto, porque no es nunca: **cuando hay que hacer
algo con cada fila**.

```text
Un proceso de cierre que recorre 20 millones de pólizas
y aplica una regla distinta a cada una NO se puede expresar en SQL,
y el acceso secuencial por bloques es lo más rápido que existe (clase 152).
```

**Y ahí la técnica de la clase 152 es la que manda**: **ordenar los ficheros por la misma clave y
recorrerlos en paralelo**, en lugar de consultar por cada fila.

Y esta clase debe recoger la propiedad de COBOL que más importa en el componente de datos y que la clase
072 explicó: **el tipo decimal**.

```cobol
       01  IMPORTE PIC S9(13)V99 COMP-3.
```

```sql
CREATE TABLE ... (importe DECIMAL(15,2))
```

**Los dos son decimales exactos, y encajan sin pérdida.** Es una de las pocas correspondencias perfectas
entre un lenguaje y una base de datos de esta página, y es la razón por la que **migrar esa aritmética a
un lenguaje con `double` es un problema** (clase 140).
"""),
        "fortran": ("""
program datos
   implicit none
   character(len=200) :: linea
   integer :: total, valor, ios, pos

   read(*, '(A)') linea
   total = 0
   pos = 1

   do
      read(linea(pos:), *, iostat=ios) valor
      if (ios /= 0) exit
      total = total + valor
      pos = pos + index(linea(pos:), ' ')
      if (pos > len_trim(linea)) exit
   end do

   write(*, '(A,I0)') 'total=', total
end program datos
""", """
**Fortran y el componente de datos.** El cálculo científico casi no usa bases de datos relacionales, y
merece explicar por qué, porque la razón es técnica y buena: **sus datos no son filas**.

```text
Un resultado de simulación es un ARREGLO de 1.000 × 1.000 × 500 valores,
con coordenadas, tiempo y metadatos.

Guardarlo como 500 millones de filas en una tabla sería absurdo:
  - el tamaño se multiplicaría por diez
  - y leer un corte sería lentísimo
```

**Y por eso este dominio usa formatos de arreglos** (clase 159): **NetCDF, HDF5 y hoy Zarr**.

Y sus capacidades merecen enumerarse, porque son las de una base de datos para este tipo de dato:

| Capacidad | Cómo |
|---|---|
| **Consulta por rebanada** | leer solo `datos(100:200, :, 5)` sin cargar el resto |
| **Compresión por trozos** | cada bloque comprimido por separado |
| **Metadatos** | unidades, coordenadas, procedencia (clase 160) |
| **Acceso paralelo** | HDF5 sobre MPI-IO: mil procesos escribiendo a la vez |
| **Y en la nube** | Zarr: cada trozo es un objeto, leíble por rango HTTP |

**La primera es la clave y es exactamente la regla del cierre de esta clase**: **pedir solo lo que hace
falta, y que el sistema de almacenamiento haga el trabajo de localizarlo**.

Es lo mismo que un índice en SQL, con otro nombre y sobre otra forma de dato.

Y donde Fortran sí toca bases de datos relacionales es en los metadatos, y merece nombrarlo: **el
catálogo de ejecuciones**.

```sql
-- qué se ejecutó, con qué parámetros, cuándo, y dónde está el resultado
CREATE TABLE ejecuciones (id, fecha, version_codigo, hash_config, ruta_salida, ...)
```

**Y eso resuelve el problema de la clase 154** —la deuda de reproducibilidad— **mejor que cualquier otra
cosa**: si cada ejecución queda registrada con su versión de código y su configuración, **un resultado de
hace cinco años se puede rastrear**.

Es una práctica barata, poco extendida, y de las que más valor dan en este dominio.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Datos is
   Total, Valor : Integer := 0;
begin
   Total := 0;
   loop
      begin
         Get (Valor);
         Total := Total + Valor;
      exception
         when others => exit;
      end;
   end loop;

   Put_Line ("total=" & Ada.Strings.Fixed.Trim (Total'Image, Ada.Strings.Both));
end Datos;
""", """
**Ada y el componente de datos.** Ada tiene acceso a bases de datos —GNATCOLL.SQL, APQ— y esta clase es el
sitio para una capacidad suya que resuelve el desajuste del "por qué" mejor que un mapeador:
**GNATCOLL.SQL genera código Ada desde el esquema**.

```bash
gnatcoll_db2ada -dbmodel=esquema.txt -api=Base
```

```ada
--  Y a partir de ahí, las consultas se escriben con TIPOS COMPROBADOS:
Q : constant SQL_Query :=
      SQL_Select (Fields  => Clientes.Nombre & Clientes.Saldo,
                  From    => Clientes,
                  Where   => Clientes.Zona = Text_Param (1));
```

**Y lo que eso da es lo que esta clase busca**: **un error de nombre de columna o de tipo es un error de
compilación**, no un fallo en producción.

Es la misma idea que jOOQ en Java, sqlc en Go y Diesel en Rust — **generar el acceso desde el esquema en
lugar de escribir cadenas** — y es la respuesta correcta al desajuste de impedancia: **no tapar la
diferencia, sino comprobarla**.

Y merece añadir la aportación de Ada al componente de datos que su sistema de tipos permite y que la
clase 124 explicó: **el dominio en el tipo**.

```ada
subtype Codigo_Postal is String (1 .. 5)
   with Dynamic_Predicate => (for all C of Codigo_Postal => C in '0' .. '9');
type Saldo is delta 0.01 range -1_000_000.00 .. 1_000_000.00;
```

**Y ahí está la propiedad valiosa**: **la restricción que la base de datos tiene en un `CHECK` está
también en el programa**, con el mismo significado.

En la mayoría de los sistemas, **la validación está escrita dos veces —en la base y en el código— y
diverge** (clase 140). Aquí, **al menos, las dos son explícitas y revisables**.

Y merece cerrar con la observación práctica que este dominio impone y que casi nadie más se plantea: **en
un sistema de tiempo real, una consulta a base de datos no es aceptable en el camino crítico**, porque
**su tiempo no está acotado**.

Así que el reparto es: **el control trabaja con datos en memoria, y la persistencia ocurre fuera del
lazo** — que es otra vez la separación por plazos de la clase 165.
"""),
        "pascal": ("""
program Datos;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Total: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';
  Total := 0;
  Tok := '';

  for I := 1 to Length(Linea) do
    if Linea[I] = ' ' then
    begin
      if Tok <> '' then Total := Total + StrToInt(Tok);
      Tok := '';
    end
    else
      Tok := Tok + Linea[I];

  WriteLn('total=', IntToStr(Total));
end.
""", """
**Pascal y el componente de datos.** El ecosistema Delphi tiene una abstracción de datos muy influyente y
merece explicarla porque su modelo se copió mucho: **el `TDataSet`**.

```pascal
Query.SQL.Text := 'SELECT nombre, saldo FROM clientes WHERE zona = :zona';
Query.ParamByName('zona').AsString := Zona;      { ← parametrizado (clase 153) }
Query.Open;

while not Query.Eof do
begin
  Total := Total + Query.FieldByName('saldo').AsCurrency;
  Query.Next;
end;
```

**`TDataSet` es un cursor navegable con una API común**, y de ahí sale la propiedad que hizo famoso a
Delphi: **cualquier control visual se conecta a él** (clase 169).

Y merece señalar dos cosas de ese fragmento, porque son las reglas del cierre de esta clase:

**Una, `ParamByName` en lugar de concatenar** — la defensa contra la inyección, y además **permite que la
base reutilice el plan de ejecución** (clase 152).

**Y dos, ese bucle es exactamente lo que el cierre desaconseja.**

```pascal
{ ✓ que sume la base }
Query.SQL.Text := 'SELECT SUM(saldo) FROM clientes WHERE zona = :zona';
```

Y `Currency` merece la mención porque es una decisión acertada del lenguaje: **es un entero de 64 bits
escalado por 10.000**, así que **es decimal exacto con cuatro decimales** — el tipo correcto para dinero
(clase 072), y encaja con `DECIMAL` de SQL sin pérdida.

Y el ecosistema moderno:

| Herramienta | Notas |
|---|---|
| **FireDAC** | el acceso a datos actual de Delphi, con muchos motores |
| **SQLdb / ZeosLib** | los de Free Pascal |
| **mORMot ORM** | mapeo objeto-relacional rápido (clase 168) |
| **`TFDMemTable`** | conjuntos de datos en memoria, para pruebas |

**El último merece la mención** porque resuelve un problema de la clase 139: **probar el código de datos
sin base de datos**, cargando un conjunto en memoria con la misma API.
"""),
        "lisp": ("""
(let ((total 0))
  (with-input-from-string (s (read-line))
    (loop for valor = (read s nil nil)
          while valor
          do (incf total valor)))
  (format t "total=~D~%" total))
""", """
**Lisp y el componente de datos.** Lisp tiene una relación con SQL que merece contarse porque su enfoque
es distinto: **generar la consulta como estructura, no como texto**.

```lisp
(select (:sum :saldo)
  (from :clientes)
  (where (:= :zona zona)))
;; → "SELECT SUM(saldo) FROM clientes WHERE zona = ?"  con el parámetro aparte
```

**La consulta se construye como listas anidadas** —que es como Lisp representa todo (clase 123)— y **la
biblioteca la traduce a SQL con parámetros**.

Y las ventajas son exactamente las dos reglas del cierre de esta clase:

**Una, es imposible la inyección**: los valores **nunca se concatenan**, van como parámetros por
construcción.

**Y dos, la consulta se puede componer con funciones**:

```lisp
(defun con-filtro-zona (consulta zona)
  (if zona (append consulta `((where (:= :zona ,zona)))) consulta))
```

**Construir consultas dinámicas concatenando cadenas es la fuente número uno de inyecciones**; hacerlo
con estructuras **es seguro por construcción**.

Es la misma idea que las consultas como árbol de jOOQ, de SQLAlchemy y de Ecto, y en Lisp sale del propio
lenguaje.

Y el ecosistema:

| Biblioteca | Notas |
|---|---|
| **Postmodern** | PostgreSQL, con S-SQL: consultas como formas Lisp |
| **CLSQL** | veterana, varios motores |
| **Mito** | mapeador objeto-relacional |
| **cl-dbi** | interfaz común, al estilo de DBI (clase 158) |

Y merece cerrar con una idea que Lisp permite y que este componente agradece: **la base de datos también
puede ejecutar Lisp**.

```sql
CREATE FUNCTION calcular(...) RETURNS numeric AS $$ ... $$ LANGUAGE plpgsql;
```

**PostgreSQL admite funciones en varios lenguajes**, y existe `pl/lisp` entre ellos.

Y el criterio para usarlo es el del cierre: **la lógica que necesita muchos datos debe ejecutarse donde
están los datos**. Mover un cálculo a la base es la misma optimización que mover un cálculo al núcleo
numérico (clase 155): **acercar el código al dato en lugar del dato al código**.
"""),
        "tcl": ("""
gets stdin linea

set total 0
foreach v [split [string trim $linea]] {
    if {$v ne ""} { incr total $v }
}

puts "total=$total"
""", """
**Tcl y el componente de datos.** Tcl tiene una interfaz de bases de datos con un diseño limpio y merece
verla: **TDBC**, del propio núcleo desde Tcl 8.6.

```tcl
package require tdbc::postgres

tdbc::postgres::connection create db -host localhost -db midb

set stmt [db prepare {SELECT SUM(saldo) AS total FROM clientes WHERE zona = :zona}]
$stmt foreach fila {
    puts [dict get $fila total]
} -as dicts
```

**Y tres detalles merecen destacarse porque son buenas decisiones:**

**`:zona` con dos puntos toma el valor de la variable Tcl del mismo nombre** — parametrizado por defecto,
y sin escribir la vinculación.

**`foreach` sobre la sentencia recorre las filas sin cargarlas todas**, que es lo correcto con conjuntos
grandes.

**Y `-as dicts` devuelve cada fila como diccionario**, con los nombres de columna — lo que hace el código
legible sin mapeador.

Y Tcl aporta a esta clase una capacidad que su modelo de datos hace natural y que la clase 152 explicó:
**la representación dual**.

```tcl
# Una fila de la base llega como diccionario; y es a la vez una cadena
set fila [dict create id 1 nombre "Ana" saldo 100.50]
puts $fila         ;# id 1 nombre Ana saldo 100.50
```

**Así que serializar el resultado para pasarlo a otro proceso** (clase 161) **es imprimirlo**, y volver a
interpretarlo es leerlo.

Y merece cerrar con el papel real de Tcl en este componente y que es el de la clase 165: **el pegamento de
datos**.

```tcl
# Extraer de un sistema, transformar, cargar en otro: en veinte líneas
$origen foreach fila {
    set transformada [transformar $fila]
    $destino allrows -- $insert $transformada
}
```

**Es el ETL de Perl en esta página** (clase 165), con la ventaja de que **TDBC da la misma API para todos
los motores**, así que el guion no cambia al cambiar de base.
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

print "total=", sum0(split ' ', $linea), "\\n";
""", """
**Perl y el componente de datos.** Perl tiene **DBI**, que la clase 158 ya presentó como el modelo que
copiaron JDBC y DB-API, y esta clase es el sitio para ver sus decisiones de uso:

```perl
my $dbh = DBI->connect($dsn, $usuario, $clave, {
    RaiseError  => 1,        # ← los errores LANZAN, no devuelven undef
    AutoCommit  => 0,        # ← transacciones explícitas
    PrintError  => 0,
});

my $total = $dbh->selectrow_array(
    'SELECT SUM(saldo) FROM clientes WHERE zona = ?', undef, $zona);

$dbh->commit;
```

**`RaiseError => 1` es la primera línea que hay que escribir**, y merece explicarlo: **sin él, DBI
devuelve `undef` en caso de error y el programa sigue** — con lo que un fallo de base de datos se
convierte en un cálculo con datos incompletos.

Es el mismo argumento que los avisos como errores de la clase 147: **hacer que el fallo sea imposible de
ignorar**.

Y `selectrow_array` con una consulta agregada es la regla del cierre en una línea: **la base suma, el
programa recibe un número**.

Y merece contrastar con el antipatrón que esta clase quiere señalar y que tiene nombre: **el problema
N+1**.

```perl
# ✗ N+1: una consulta para los pedidos, y UNA MÁS por cada uno
my $pedidos = $dbh->selectall_arrayref('SELECT id FROM pedidos');
for my $p (@$pedidos) {
    my $lineas = $dbh->selectall_arrayref(
        'SELECT * FROM lineas WHERE pedido = ?', undef, $p->[0]);   # ← ¡mil viajes!
}

# ✓ una consulta con unión, o dos consultas y agrupar en memoria
my $todo = $dbh->selectall_arrayref(
    'SELECT p.id, l.* FROM pedidos p JOIN lineas l ON l.pedido = p.id',
    { Slice => {} });
```

**El problema N+1 es el fallo de rendimiento más común de cualquier aplicación con base de datos**, y lo
producen sobre todo los mapeadores objeto-relacionales, porque **hacen que cada acceso a una relación
parezca un atributo**.

Es la consecuencia directa del desajuste del "por qué" de esta clase: **la abstracción que oculta la
frontera hace fácil cruzarla mil veces sin darse cuenta** (clase 155).

Y la defensa práctica es la de la clase 152: **medir**. Un registro de consultas por petición, con el
número y el tiempo total, **hace visible el N+1 el día que aparece** en lugar de seis meses después.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long total = 0, valor = 0;
    while (std::cin >> valor) total += valor;

    std::cout << "total=" << total << '\\n';
    return 0;
}
""", """
**C++ y el componente de datos.** C++ es, otra vez, **el suelo**: PostgreSQL, MySQL, SQLite, MongoDB,
ClickHouse y RocksDB están escritos en C o C++.

Y para usarlas desde C++, el ecosistema:

| Biblioteca | Notas |
|---|---|
| **libpq / libmysqlclient** | las de C, oficiales |
| **SOCI** | interfaz común, al estilo de DBI |
| **sqlpp11** | **consultas comprobadas en compilación**, con el esquema en C++ |
| **ODB** | mapeador objeto-relacional con generador de código |
| **SQLite embebido** | la base de datos **dentro** del proceso |

**`sqlpp11` merece la mención** porque hace en C++ lo que GNATCOLL en Ada de esta página: **la consulta se
escribe con tipos, y una columna mal escrita no compila**.

Y **SQLite embebido merece un apartado propio**, porque cambia el reparto de esta clase:

```cpp
sqlite3_open("datos.db", &db);
```

**No hay servidor, ni conexión, ni red**: la base de datos es **una biblioteca dentro del proceso** y los
datos, **un fichero**.

Y sus consecuencias merecen enumerarse porque son las que la han hecho la base de datos más desplegada del
mundo —está en todos los teléfonos, todos los navegadores y casi todas las aplicaciones de escritorio—:

| Propiedad | Consecuencia |
|---|---|
| **Sin proceso servidor** | cero administración, cero configuración |
| **Un fichero** | copiar la base es copiar un fichero |
| **Transacciones ACID reales** | con confirmación en dos fases sobre el sistema de ficheros |
| **Y una consulta no cruza ninguna frontera** | microsegundos, no milisegundos |

**La última es la que conecta con el cierre de esta clase**: **con SQLite, el problema N+1 casi
desaparece**, porque cada consulta cuesta microsegundos y no hay viaje de red.

**Y eso cambia el diseño**: lo que en una base cliente-servidor sería un antipatrón, aquí puede ser
razonable.

Es un buen recordatorio de que **las reglas de rendimiento dependen de la frontera** (clase 155), y de
que conviene saber cuál se tiene delante antes de aplicar una receta.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi DATOS;
  linea char(200) const;
end-pi;

dcl-s texto varchar(200);
dcl-s pos   int(10);
dcl-s total int(20);

texto = %trim(linea) + ' ';
total = 0;

dow %len(%trim(texto)) > 0;
  pos = %scan(' ' : texto);
  if pos = 0;
    leave;
  endif;
  if pos > 1;
    total += %int(%subst(texto : 1 : pos - 1));
  endif;
  texto = %trim(%subst(texto : pos + 1));
enddo;

dsply ('total=' + %char(total));

*inlr = *on;
return;
""", """
**RPG y el componente de datos.** IBM i tiene la integración más estrecha de esta página entre lenguaje y
base de datos, y esta clase es el sitio para el detalle que la explica: **Db2 for i y el sistema son la
misma cosa** (clase 139).

```rpgle
// El acceso NATIVO: los ficheros son parte del programa
dcl-f clientes keyed;
chain (idCliente) clientes;
if %found(clientes);
  total += saldo;
endif;

// Y el SQL, embebido y comprobado en compilación (clase 163)
exec sql SELECT SUM(saldo) INTO :total
           FROM clientes WHERE zona = :zona;
```

**Y las dos formas acceden a los MISMOS datos** — no hay dos motores ni sincronización: **una tabla SQL y
un fichero físico son el mismo objeto visto de dos maneras**.

Es una propiedad poco común y merece destacarla: **el mismo dato se puede leer registro a registro con
acceso nativo y por conjuntos con SQL, indistintamente**.

Y por eso la transición de esta plataforma —**de navegacional a SQL** (clase 152)— pudo hacerse **fila a
fila y programa a programa**, sin migrar nada.

Y las razones para preferir SQL, que son las del cierre de esta clase, merecen enumerarse porque en esta
plataforma son medibles:

| SQL gana en | Por qué |
|---|---|
| **Agregar y filtrar** | el optimizador elige el plan (clase 152) |
| **Uniones** | imposibles de expresar bien con acceso nativo |
| **Paralelismo** | Db2 puede repartir la consulta |
| **Índices nuevos sin tocar el programa** | el Index Advisor los sugiere |

**Y el acceso nativo gana en un caso**: **procesar cada fila de un fichero enorme en orden de clave**, que
es el proceso de lote de la clase 152.

Y merece cerrar con la capacidad de esta plataforma que la clase 142 ya nombró y que aquí es el
complemento del componente de datos: **todo el catálogo es consultable con SQL**.

```sql
SELECT * FROM QSYS2.SYSTABLES WHERE TABLE_SCHEMA = 'MIBIB';
SELECT * FROM QSYS2.SYSIXADV ORDER BY TIMES_ADVISED DESC;
```

**Preguntar al sistema qué tablas hay, qué índices faltan y qué consultas van lentas es SQL** — lo que
convierte el mantenimiento del componente de datos en algo que cualquiera con SQL puede hacer.
"""),
        "pli": ("""
 datos: procedure options(main);

    declare valor fixed binary(31);
    declare total fixed binary(31) initial(0);

    on endfile(sysin) goto fin;

    do while ('1'b);
       get list (valor);
       total = total + valor;
    end;

 fin:
    put skip list ('total=' || trim(char(total)));

 end datos;
""", """
**PL/I y el componente de datos.** PL/I vivió una generación de bases de datos que merece conocerse porque
precede a lo relacional y sigue en producción: **IMS DB, jerárquica, de 1966**.

```pli
 call plitdli(cuatro, 'GU      ', pcb, area, ssa1);   /* Get Unique */
 call plitdli(cuatro, 'GNP     ', pcb, area, ssa2);    /* Get Next in Parent */
```

**IMS organiza los datos en árboles**: un cliente tiene pedidos, un pedido tiene líneas — **y se navega
por la jerarquía**.

Y merece la comparación, porque explica por qué lo relacional ganó y también qué se perdió:

| | IMS jerárquica | Relacional |
|---|---|---|
| Consultas previstas | **rapidísimas** | rápidas |
| Consultas **no** previstas | **muy difíciles** | naturales |
| Modelo de datos | fijo, decidido al diseñar | flexible |
| Uniones arbitrarias | no | sí |
| **Rendimiento máximo** | **el más alto que existe** | muy bueno |

**La última fila merece la mención porque es real**: **IMS sigue procesando algunas de las cargas
transaccionales más altas del mundo** —miles de millones de transacciones al día en bancos grandes—
porque **cuando el patrón de acceso se conoce de antemano, una jerarquía optimizada es imbatible**.

Y lo relacional ganó por lo que la clase 164 llamaría la razón correcta: **no por rendimiento, sino
porque permite preguntar cosas que nadie previó** — y eso resultó valer más.

Y merece señalar el paralelismo con hoy, porque es exacto: **las bases de datos de clave y valor y las
documentales son jerárquicas**, y su compromiso es el mismo — **rapidísimas para el acceso previsto,
incómodas para lo demás** (clase 099).

Es la misma decisión, redescubierta cuarenta años después, y con las mismas consecuencias: **el modelo de
datos se elige por los patrones de acceso, y cambiarlo después cuesta**.
"""),
        "mumps": ("""
DATOS ; Componente de datos -- clase 170
 read linea
 new i, total, n
 set total = 0
 for i = 1:1:$length(linea, " ") do
 . set n = $piece(linea, " ", i)
 . if n '= "" set total = total + n
 write "total=", total, !
 quit
""", """
**M y el componente de datos.** Aquí está la primera mitad del gancho, y merece desarrollarla porque es la
propiedad más valiosa de M: **no hay desajuste de impedancia, porque no hay dos modelos**.

```mumps
 set ^PEDIDO(4711, "CLIENTE") = "ACME"
 set total = 0
 set art = ""
 for  set art = $order(^PEDIDO(4711, "LINEA", art)) quit:art=""  do
 . set total = total + $piece(^PEDIDO(4711, "LINEA", art), "^", 2)
```

**Ahí no hay consulta, ni conexión, ni conversión de tipos, ni mapeador**: **la variable persistente es la
estructura de datos** (clase 099).

Y merece enumerar lo que eso ahorra, porque es todo lo que las demás columnas de esta página gestionan:

```text
Sin: cadena de conexión, conjunto de conexiones, SQL, parámetros,
     conversión de tipos, mapeo objeto-relacional, problema N+1,
     ni diferencia entre "el objeto" y "la fila".
```

**Y el coste es el que la clase 099 explicó**: **no hay consultas ad hoc**. Para responder "cuántos
pedidos hay por zona" **hay que tener un índice que lo permita, o recorrerlo todo**.

Es exactamente el compromiso de IMS en esta página, y el mismo de las bases de clave y valor modernas.

Y por eso los sistemas M serios tienen **una capa de índices explícita**, mantenida por el programa:

```mumps
 ; al guardar, se actualizan los índices
 set ^PEDIDO(id, "ZONA") = zona
 set ^PEDIDOX("ZONA", zona, id) = ""      ; índice secundario
```

**Y ahí está el riesgo del cierre de esta clase**: **si alguien escribe sin actualizar el índice, el
índice miente** — y no hay motor que lo impida.

**FileMan resuelve eso** (clase 149): **escribir por su API mantiene los índices automáticamente**, y por
eso el estándar de VistA prohíbe escribir directamente en las globals de otro paquete (clase 166).

Y merece cerrar con lo que las implementaciones modernas han añadido y que cambia el cuadro: **SQL sobre
las mismas globals**.

```sql
-- InterSystems IRIS y YottaDB Octo: SQL sobre datos M
SELECT SUM(importe) FROM Pedidos WHERE zona = 'NORTE'
```

**Y con eso se tienen las dos cosas**: el acceso directo sin impedancia para lo que el programa hace todos
los días, y SQL para las preguntas que nadie previó — que es, exactamente, lo que este componente
necesita.
"""),
        "smalltalk": ("""
| linea total |

linea := stdin nextLine trimBoth.
total := 0.

(linea substrings: ' ') do: [ :p | total := total + p asNumber ].

Transcript show: 'total=', total printString; cr.
""", """
**Smalltalk y el componente de datos.** Y aquí está la segunda mitad del gancho, y merece contarla porque
es una tecnología notable y poco conocida: **GemStone/S**.

```smalltalk
"Un objeto persistente NO se guarda: simplemente se referencia desde el árbol raíz"
System myUserProfile symbolList at: #Pedidos put: (Set new).
Pedidos add: unPedido.
System commitTransaction.
```

**No hay mapeo, ni consultas, ni serialización**: **los objetos viven en un repositorio compartido y
transaccional**, y **varias máquinas virtuales trabajan sobre él a la vez** (clase 161).

Y las propiedades merecen enumerarse porque son las de una base de datos de verdad:

| Propiedad | Detalle |
|---|---|
| **Transacciones ACID** | con detección de conflictos y reintento |
| **Objetos compartidos entre procesos y máquinas** | el repositorio es el estado |
| **Índices sobre colecciones** | consultas rápidas sin SQL |
| **Y el mismo lenguaje** | el código de negocio corre **dentro** del repositorio |

**La última es la más interesante y conecta con Lisp en esta página**: **la lógica se ejecuta donde están
los datos**, sin viaje de red — que es la regla del cierre de esta clase llevada al extremo.

Y GemStone lleva en producción desde los años noventa en sistemas financieros, con volúmenes serios.

Y merece añadir la observación general que este componente permite hacer al cerrar la clase: **el
desajuste de impedancia no es una ley de la naturaleza — es la consecuencia de que el lenguaje y la base
de datos evolucionaran por separado**.

```text
Los que NO lo tienen:
  M          → la variable es la base de datos
  GemStone    → el objeto es persistente
  SQLite en proceso  → la frontera casi no existe
  Y los lenguajes con consultas integradas y comprobadas (LINQ, sqlpp11, GNATCOLL)
     → el desajuste sigue, pero al menos el compilador lo vigila
```

**Y el resto del mundo lo tapa con mapeadores objeto-relacionales**, que funcionan bien hasta que
esconden un problema N+1 o generan una consulta que nadie entiende.

Es la lección práctica de esta clase, y la más útil para el proyecto de esta parte: **el mapeador es una
comodidad, no una abstracción**. Conviene saber siempre qué SQL se está ejecutando — y las herramientas
que lo enseñan valen más que las que lo esconden.
"""),
    },
)
