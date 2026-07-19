# Clase 025 — Familia concurrente/actor: Erlang, Elixir y el CSP de Go

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes diseñados para hacer muchas cosas a la vez de forma segura. Erlang y Elixir usan el modelo de actores (procesos aislados que se comunican por mensajes, con supervisión y 'let it crash'); Go (en el núcleo) usa CSP (goroutines y canales). Dos respuestas al mismo problema: la concurrencia.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el modelo de actores y por qué favorece la tolerancia a fallos.
2. Distinguir actores (Erlang/Elixir) de CSP (Go).
3. Entender la filosofía 'let it crash' y la supervisión.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El problema de la concurrencia | Hacer muchas cosas a la vez sin corromper datos |
| 2 | Modelo de actores | Procesos aislados que solo se comunican por mensajes |
| 3 | Let it crash y supervisión | Dejar morir un proceso y reiniciarlo desde arriba |
| 4 | CSP en Go | Goroutines y canales: 'comparte comunicando' |

## 📖 Definiciones y características

- **Modelo de actores** — concurrencia mediante procesos aislados que intercambian mensajes. Clave: sin memoria compartida, no hay condiciones de carrera.
- **Erlang** — 1986 (Ericsson, Joe Armstrong) para telecomunicaciones. Clave: tolerancia a fallos extrema; corre sobre la máquina BEAM.
- **Elixir** — 2011 (José Valim), sintaxis moderna sobre la BEAM de Erlang. Clave: actores + productividad; base de Phoenix.
- **CSP** — Communicating Sequential Processes (Hoare, 1978): procesos que se sincronizan por canales. Clave: modelo de la concurrencia de Go.

## 🧩 Situación

Un sistema de mensajería debe seguir funcionando aunque parte de él falle. En vez de evitar todos los errores, Erlang deja que un proceso muera y un supervisor lo reinicia limpio. La resiliencia nace de aislar, no de blindar.

## 🔎 Ejemplo

Dos modelos de concurrencia:

```text
Actores (Elixir):  send(pid, {:hola, "Ada"})     # mensaje a un proceso
CSP (Go):          canal <- "hola"                // enviar por un canal
                   msg := <-canal                 // recibir
```

## ✍️ Práctica

Go está en el núcleo y usa CSP. Busca 'goroutine' y 'channel'. ¿En qué se parece un canal de Go a enviar un mensaje a un actor, y en qué se diferencia?

## ⚠️ Errores comunes

- **Compartir memoria entre hilos sin protección** → causa: condiciones de carrera → solución: preferir el paso de mensajes (actores/canales) al estado compartido
- **Intentar prevenir todos los fallos** → causa: código defensivo frágil → solución: adoptar 'let it crash': aislar y supervisar en vez de blindar

## ❓ Preguntas frecuentes

- **¿Qué es la BEAM?** La máquina virtual de Erlang/Elixir, optimizada para millones de procesos ligeros y tolerancia a fallos.
- **¿Go es de actores?** No exactamente: usa CSP (canales), un primo cercano del modelo de actores.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 024](../../parte-1-atlas-y-genealogia-de-los-lenguajes/024-familia-logica-y-declarativa-sql-prolog-datalog/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 026 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/026-familia-de-sistemas-c-c-plus-plus-rust-zig/README.md)
