# 📞 Erlang — 1986

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Erlang se diseñó en Ericsson para centralitas telefónicas, con un requisito que ningún otro lenguaje
de esta lista tuvo: **no puede pararse nunca**. De ahí salió un modelo de concurrencia y de tolerancia
a fallos tan distinto del resto que **su lema es "déjalo fallar"** — y funciona.

> **🎯 Por qué está en este programa**
>
> Erlang es el representante de la **familia concurrente / actor** ([Atlas](README.md#concurrente-actor)),
> que **no tiene representante en el núcleo** — su parienta más cercana es la concurrencia CSP de
> [Go](go.md).
>
> Aporta al programa **el modelo de actores**
> ([clase 133](../classes/parte-8-como-funcionan-los-lenguajes/133-actores-y-paso-de-mensajes/README.md))
> y, sobre todo, **una filosofía de tolerancia a fallos distinta de todo lo demás del curso**: no
> intentar que el código no falle, sino **organizar el sistema para que fallar no importe** (clases
> 116 y 148).

| | |
|---|---|
| **Año** | 1986; libre desde 1998; OTP desde 1996 |
| **Autoría** | **Joe Armstrong**, Robert Virding y Mike Williams — Ericsson |
| **Familia** | Concurrente / actor; con influencia de [Prolog](prolog.md) —su sintaxis— y de ML |
| **Paradigma** | **Funcional, concurrente y distribuido**, sin estado compartido |
| **Tipado** | **Dinámico y fuerte**; con Dialyzer para análisis estático opcional |
| **Memoria** | **Un montón y un recolector POR PROCESO** — sin pausas globales |
| **Ejecución** | Bytecode sobre la **BEAM**, con JIT desde OTP 24 |
| **Estado** | 🟢 **Vivo y estratégico**: telecomunicaciones, mensajería y sistemas distribuidos |

---

## 📜 Historia

En **1986**, el laboratorio de Ericsson buscaba una forma mejor de programar centralitas telefónicas.
Los requisitos eran, literalmente, los más exigentes de esta lista:

- **Nueve nueves de disponibilidad**: menos de 32 milisegundos de parada al año.
- **Millones de llamadas simultáneas.**
- **Actualización del software sin cortar el servicio** (clase 148).
- **Y que un fallo en una llamada no afecte a las demás.**

**Joe Armstrong** y su equipo probaron primero con [Prolog](prolog.md) —de ahí viene la sintaxis, con
los puntos al final de las cláusulas— y acabaron construyendo un lenguaje propio.

**Y la decisión de diseño es la que hay que entender**: en lugar de intentar escribir código que no
falle, **aceptaron que el software falla** y construyeron el sistema para que eso no importe:

> **"Let it crash"** — deja que falle. **No programes defensivamente**: si algo va mal, que el proceso
> muera limpiamente y que otro lo reinicie en un estado conocido.

**OTP** —*Open Telecom Platform*, 1996— es el conjunto de bibliotecas que hace eso práctico: árboles
de supervisión, comportamientos estándar y actualización en caliente.

El resultado se midió: el conmutador **AXD301**, con más de un millón de líneas de Erlang, alcanzó
**nueve nueves de disponibilidad** en producción — uno de los datos de fiabilidad más citados de la
industria.

Ericsson llegó a **prohibir Erlang internamente** en 1998 para estandarizar en C++; el equipo lo
liberó como software libre, y ahí empezó su segunda vida.

## 🏭 Dónde vive hoy

- **Telecomunicaciones**: sigue en el núcleo de infraestructura de Ericsson y de otros operadores.
- **Mensajería**: **WhatsApp** atendió a cientos de millones de usuarios con un equipo de ingeniería
  diminuto gracias a Erlang; es el caso más citado.
- **Colas y bases de datos**: **RabbitMQ**, **CouchDB**, **Riak**.
- **Videojuegos en línea y apuestas**: sistemas con muchas conexiones concurrentes y de larga
  duración.
- **Y como plataforma de [Elixir](elixir.md)**, que ha traído gente nueva a la misma máquina virtual.

## 🧠 Lo que enseña: actores, supervisión y aislamiento

**Uno, los procesos de Erlang no son hilos** (clase 133):

```erlang
Pid = spawn(fun() -> bucle(0) end),     % ← unos cientos de bytes, no un hilo del sistema
Pid ! {sumar, 5},                        % enviar un mensaje: asíncrono, sin bloquear

bucle(Estado) ->
    receive
        {sumar, N} -> bucle(Estado + N);
        {leer, Quien} -> Quien ! Estado, bucle(Estado)
    end.
```

**Y las propiedades que los hacen distintos de todo lo demás del curso:**

- **No comparten memoria.** Cada proceso tiene **su propio montón y su propio recolector**, así que
  **no hay pausas globales** y **no puede haber carreras de datos** (clase 136) — por construcción, no
  por disciplina.
- **Son baratísimos**: cientos de miles o millones en una máquina.
- **Y el planificador es apropiativo**: la máquina virtual **quita el turno** a un proceso que lleva
  mucho ejecutando, así que **uno lento no bloquea a los demás** — a diferencia de la mayoría de los
  modelos cooperativos (clase 134).

**Dos, la supervisión**, que es lo que hace útil el "déjalo fallar":

```text
             Supervisor
            /     |     \
      Trabajador  Trab.  Trab.
```

**Un supervisor vigila procesos hijos y los reinicia cuando mueren**, con una estrategia declarada:
reiniciar solo al que murió, reiniciar a todos, o rendirse y morir él también —lo que escala el
problema a su propio supervisor—.

**Y el efecto práctico es enorme**: el código de negocio **no lleva manejo de errores defensivo**. Se
escribe el caso correcto, y **la estructura del sistema se ocupa del resto** (clase 116).

**Y tres, la distribución transparente:**

```erlang
Pid ! Mensaje      % ← funciona igual si Pid está en OTRA MÁQUINA
```

**Enviar un mensaje a un proceso remoto es idéntico a enviarlo a uno local**. Y aquí la clase 161
obliga a la advertencia: **esa transparencia esconde el fallo de red** —el mismo problema del anexo E
de [Ada](ada.md) y de CORBA (clase 160)—. Erlang lo compensa porque **el modelo ya asume que las cosas
mueren**, así que un fallo de red es un caso más de lo que el supervisor sabe manejar.

## 🔄 Lo que se ha modernizado

- **JIT en la BEAM** (OTP 24), con mejoras de rendimiento notables.
- **Dialyzer** y las especificaciones de tipo (`-spec`): análisis estático **de tipado exitoso** —solo
  señala lo que seguro está mal, nunca da falsos positivos (clase 146)—.
- **`gen_statem`** y los comportamientos modernos de OTP.
- **Actualización de código en caliente** madura, con cambio de versión de módulo y migración de
  estado (clase 148).
- **Y [Elixir](elixir.md)**, que ha rejuvenecido el ecosistema entero manteniendo la máquina virtual.

## ⚙️ Cómo se ejecuta hoy

```bash
escript main.erl < entrada.txt        # como guion
erl                                    # consola interactiva
rebar3 compile eunit dialyzer          # construcción, pruebas y análisis
```

## 🧪 El programa de la clase 041 en Erlang

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```erlang
#!/usr/bin/env escript

main(_) ->
    Linea = io:get_line(""),
    [P, C, D] = [list_to_float(X) || X <- string:tokens(string:trim(Linea), " ")],
    io:format("Total: ~.2f~n", [P * C * (1 - D)]).
```

**Lo que hay que ver.**

- **`[P, C, D] = ...` es emparejamiento de patrones**, no asignación: **une la lista con el patrón de
  tres elementos**, y falla si no encaja. Es la misma idea que en [Prolog](prolog.md), de donde viene
  la sintaxis, y que en [Scala](scala.md).
- **`[X || X <- lista]` es una comprensión de listas**, tomada de Prolog y de Haskell.
- **Las variables empiezan por mayúscula**, como en Prolog — y **se ligan una sola vez**: en Erlang
  **no hay variables mutables** (clase 102). Reasignar `P` sería un error de patrón.
- **`~.2f` es la directiva de formato** con dos decimales; y las cadenas de Erlang son **listas de
  números**, lo que explica `list_to_float` y es una peculiaridad histórica que
  [Elixir](elixir.md) corrigió.
- **Y este programa no enseña nada del lenguaje real**: Erlang es un sistema de procesos y
  supervisores, no un guion secuencial. Es un **contrato adaptado** (clase 040).

## 📚 Fuentes y bibliografía

- [Learn You Some Erlang for Great Good!](https://learnyousomeerlang.com/) — **Fred Hébert**, libre en
  línea; la mejor introducción, con OTP explicado de verdad.
- **Joe Armstrong**, *Programming Erlang*, 2.ª ed., Pragmatic — del creador del lenguaje.
- **Joe Armstrong**, *Making reliable distributed systems in the presence of software errors* (tesis,
  2003) — libre; **la mejor exposición que existe del principio "déjalo fallar"**, y lectura
  recomendada para la clase 116 aunque no se use Erlang.
- [Documentación de Erlang/OTP](https://www.erlang.org/docs) — el *Design Principles* sobre árboles de
  supervisión es material directo de la clase 165.
- **Fred Hébert**, *Erlang in Anger* — libre; qué hacer cuando un sistema en producción se comporta
  mal (clases 141 y 142).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Elixir](elixir.md) · [Go](go.md) · [Prolog](prolog.md) · [Smalltalk](smalltalk.md) ·
[Ada](ada.md)
