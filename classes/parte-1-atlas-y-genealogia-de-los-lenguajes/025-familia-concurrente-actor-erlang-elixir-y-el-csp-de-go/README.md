# Clase 025 — Familia concurrente/actor: Erlang, Elixir y el CSP de Go

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes diseñados desde su base para hacer muchas cosas a la vez de forma segura. **Erlang** y **Elixir** implementan el **modelo de actores**: procesos aislados, sin memoria compartida, que solo se comunican enviándose mensajes, con supervisión jerárquica y la célebre filosofía "let it crash" (déjalo fallar). **Go** —que está en el núcleo— usa **CSP** (Communicating Sequential Processes): goroutines ligeras que se coordinan mediante canales. Son dos respuestas distintas, ambas elegantes, a uno de los problemas más difíciles de la programación: la concurrencia.

Esto importa porque la concurrencia es la fuente de los bugs más traicioneros —condiciones de carrera, interbloqueos, corrupción de datos compartidos— y porque el hardware moderno, con sus múltiples núcleos, la hace ineludible. Sebesta dedica un capítulo a la concurrencia; Van Roy y Haridi construyen buena parte de su libro sobre modelos de concurrencia, y defienden que el paso de mensajes es más fácil de razonar que la memoria compartida. Estas familias encarnan esa tesis en lenguajes reales y en producción.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el modelo de actores y por qué favorece la tolerancia a fallos.
2. Distinguir actores (Erlang/Elixir) de CSP (Go) y ver qué comparten.
3. Entender la filosofía "let it crash" y el papel de los supervisores.
4. Reconocer por qué el paso de mensajes evita las condiciones de carrera.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El problema de la concurrencia | Hacer muchas cosas a la vez sin corromper datos |
| 2 | Modelo de actores | Procesos aislados que solo hablan por mensajes |
| 3 | Let it crash y supervisión | Dejar morir un proceso y reiniciarlo limpio |
| 4 | CSP en Go | Goroutines y canales: "comparte comunicando" |
| 5 | Actores vs. CSP | Buzón por proceso vs. canal como punto de encuentro |

## 📖 Definiciones y características

El **modelo de actores**, formulado teóricamente por Carl Hewitt en 1973, propone una idea radical: en lugar de que varios hilos compartan memoria y compitan por ella con candados, el sistema se compone de **actores** —unidades de cómputo completamente aisladas, cada una con su propio estado privado, que solo pueden hacer tres cosas: enviar mensajes a otros actores, crear actores nuevos y decidir cómo reaccionar al siguiente mensaje—. Como no hay memoria compartida, no puede haber condiciones de carrera sobre ella: el problema desaparece por diseño en vez de gestionarse con candados. Cada actor procesa sus mensajes de uno en uno, desde un buzón, en orden.

**Erlang** (Joe Armstrong, Robert Virding y Mike Williams, en Ericsson, 1986) llevó este modelo a la práctica industrial con un objetivo extremo: construir centralitas telefónicas que no se caen, con "nueve nueves" de disponibilidad. Para lograrlo, Erlang combina actores con dos ideas más. Los procesos son ligerísimos —la máquina virtual **BEAM** maneja millones de ellos— y baratos de crear y destruir. Y la filosofía es **"let it crash"**: en vez de blindar cada proceso con código defensivo que intente prever todos los errores, se deja que un proceso que encuentra un estado inesperado simplemente muera, y un **supervisor** —un proceso cuya única misión es vigilar a otros— lo reinicia desde un estado limpio conocido. La resiliencia no nace de evitar los fallos, sino de aislarlos y recuperarse rápido de ellos. Armstrong lo resumía así: un sistema tolerante a fallos necesita al menos dos ordenadores, y ese principio de aislamiento se lleva hasta dentro del propio programa. **Elixir** (José Valim, 2011) puso una sintaxis moderna y productiva sobre la misma BEAM, heredando todo el modelo de Erlang y popularizándolo con el framework web Phoenix.

**Go** (Google, 2009) resuelve la concurrencia con un modelo emparentado pero distinto: **CSP**, formalizado por Tony Hoare en 1978. En lugar de actores con buzones, Go tiene **goroutines** —funciones ligeras que corren concurrentemente, gestionadas por el runtime— y **canales**, conductos tipados por los que las goroutines se pasan valores y se sincronizan. El lema de Go lo resume: "no comuniques compartiendo memoria; comparte memoria comunicando". La diferencia con los actores es sutil pero real: en el modelo de actores el mensaje se dirige a un actor concreto identificado (su buzón), mientras que en CSP el canal es un punto de encuentro anónimo donde emisor y receptor se citan; cualquiera puede leer o escribir. Ambos evitan la memoria compartida y sus carreras, pero organizan la comunicación de forma diferente. Como Go está en el núcleo, es el mejor sitio para experimentar de primera mano estas ideas.

- **Modelo de actores** — concurrencia mediante procesos aislados que intercambian mensajes. Clave: sin memoria compartida, no hay condiciones de carrera.
- **Erlang** — 1986 (Ericsson, Joe Armstrong y otros), para telecomunicaciones. Clave: tolerancia a fallos extrema sobre la máquina BEAM.
- **Elixir** — 2011 (José Valim), sintaxis moderna sobre la BEAM. Clave: actores más productividad; base de Phoenix.
- **CSP** — Communicating Sequential Processes (Hoare, 1978): procesos que se sincronizan por canales. Clave: el modelo de concurrencia de Go.

## 🧩 Situación

Un sistema de mensajería debe seguir sirviendo a millones de usuarios aunque una parte falle: un mensaje mal formado, una conexión que se corta, un bug en una ruta poco usada. El enfoque tradicional intentaría blindar cada función con comprobaciones defensivas, y aun así un caso no previsto tumbaría el proceso entero. El enfoque de Erlang es el opuesto: cada conversación corre en su propio proceso aislado; si uno encuentra un estado imposible, se le deja morir, y su supervisor lo reinicia limpio en microsegundos, sin arrastrar al resto. El usuario ni se entera. La lección —contraintuitiva pero poderosa— es que la robustez nace de aislar y recuperarse, no de intentar que nada falle nunca.

## 🔎 Ejemplo

Dos modelos de comunicación entre unidades concurrentes:

```text
Actores (Elixir):   send(pid, {:saludo, "Ada"})   # mensaje a un proceso concreto (pid)
                    receive do
                      {:saludo, nombre} -> IO.puts("Hola, #{nombre}")
                    end

CSP (Go):           canal <- "Ada"                 // enviar por un canal (punto de encuentro)
                    nombre := <-canal              // otra goroutine recibe
```

El **delta** es a quién va dirigida la comunicación. En Elixir, el mensaje se envía a un **pid**, el identificador de un proceso concreto que lo recibirá en su buzón. En Go, el valor se pone en un **canal**, y quien esté leyendo ese canal lo recogerá, sin que emisor y receptor se conozcan. Ambos comparten lo esencial —ningún dato mutable se comparte entre las partes— y por eso ambos esquivan las condiciones de carrera que atormentan al modelo de hilos con memoria compartida.

## ✍️ Práctica

Go está en el núcleo y usa CSP. Busca en material de Go los términos `goroutine` y `channel`. Escribe en dos o tres frases: ¿en qué se parece enviar un valor por un canal de Go a enviar un mensaje a un actor de Elixir, y en qué se diferencia (pista: destinatario concreto vs. punto de encuentro anónimo)? ¿Qué problema clásico de la concurrencia evitan ambos por diseño?

## ⚠️ Errores comunes

- **Compartir memoria mutable entre hilos sin protección** → causa: condiciones de carrera → solución: preferir el paso de mensajes (actores o canales) al estado compartido.
- **Intentar prevenir todos los fallos con código defensivo** → causa: código frágil y enrevesado → solución: adoptar "let it crash": aislar en procesos y supervisar, en vez de blindar.
- **Creer que Go usa el modelo de actores** → causa: mezclar CSP con actores → solución: recordar que Go usa canales (puntos de encuentro), no buzones dirigidos a un pid.

## ❓ Preguntas frecuentes

- **¿Qué es la BEAM?** La máquina virtual de Erlang y Elixir, diseñada para ejecutar millones de procesos ligeros con planificación justa y tolerancia a fallos.
- **¿Go es de actores o de CSP?** De CSP: usa canales, un primo cercano pero distinto del modelo de actores; la diferencia está en cómo se dirige la comunicación.
- **¿"Let it crash" no es peligroso?** Al contrario: al reiniciar desde un estado limpio conocido, evita que un proceso corrupto siga operando; la clave es el aislamiento, que impide que el fallo se propague.

## 🔗 Referencias

- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), cap. de goroutines y canales.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 13 "Concurrency".
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press), cap. 5 (concurrencia por paso de mensajes).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf), cap. de Erlang.

---

> [⏮️ Clase 024](../../parte-1-atlas-y-genealogia-de-los-lenguajes/024-familia-logica-y-declarativa-sql-prolog-datalog/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 026 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/026-familia-de-sistemas-c-c-plus-plus-rust-zig/README.md)
