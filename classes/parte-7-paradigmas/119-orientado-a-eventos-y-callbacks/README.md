# Clase 119 — Orientado a eventos y callbacks

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **orientado a eventos y callbacks**: en vez de un flujo lineal, se registran manejadores que reaccionan cuando ocurre un evento. Aquí un callback recolecta cada evento emitido.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Registrar un callback.
2. Emitir eventos que lo invocan.
3. Reconocer la inversión de control.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Evento | Algo que ocurre |
| 2 | Callback/manejador | Función que reacciona |
| 3 | Inversión de control | El sistema llama a tu código |

## 📖 Definiciones y características

- **Evento** — suceso al que el programa reacciona (clic, mensaje, dato). Clave: dispara callbacks.
- **Callback** — función registrada para ejecutarse cuando ocurre el evento. Clave: no la llamas tú.
- **Inversión de control** — el sistema invoca tu código, no al revés. Clave: base de la GUI y del servidor.

## 🧩 Situación

Interfaces, servidores, sensores: no siguen un guion lineal, reaccionan a eventos. Registras un callback ('cuando llegue X, haz Y') y el sistema lo invoca.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de eventos, n >= 1)
- **Salida** (stdout): `eventos=<1-2-...-n>` (orden en que llegaron)
- **Regla:** por cada i en 1..n, emitir evento i; el callback lo recolecta

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `eventos=1-2-3` |
| `1` | `eventos=1` |
| `4` | `eventos=1-2-3-4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
registrar callback ; PARA i de 1 a n: emitir(i) ; ESCRIBIR recolectados
```

## 🌐 Implementaciones idiomáticas

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`:

| Lenguaje | Archivo | Cómo ejecutar |
|---|---|---|
| Python | `implementaciones/python/main.py` | `python main.py` |
| JavaScript | `implementaciones/javascript/main.mjs` | `node main.mjs` |
| TypeScript | `implementaciones/typescript/main.ts` | `pnpm exec tsx main.ts` |
| Java | `implementaciones/java/Main.java` | `java Main.java` |
| C# | `implementaciones/csharp/Program.cs` | `dotnet run` |
| Go | `implementaciones/go/main.go` | `go run main.go` |
| Rust | `implementaciones/rust/main.rs` | `rustc main.rs -o main && ./main` |
| C | `implementaciones/c/main.c` | `cc main.c -o main && ./main` |
| SQL | `implementaciones/sql/main.sql` | `sqlite3 :memory: < main.sql` |
| PHP | `implementaciones/php/main.php` | `php main.php` |

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Callback como función pasada (Python/JS/Go), delegate (C#), interfaz (Java). |
| Semántica | El emisor invoca el callback; el flujo no es lineal. |
| Paradigmática | SQL no tiene eventos; procesa datos. |

## 🧬 El concepto en la familia

En JS los EventEmitter y los `addEventListener` del navegador son puro estilo de eventos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 119
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Callback con efectos secundarios ocultos** → causa: estado difícil de seguir → solución: mantener el callback claro y enfocado
- **Olvidar registrar el manejador** → causa: el evento no hace nada → solución: registrar antes de emitir

## ❓ Preguntas frecuentes

- **¿Callback o async/await?** async/await suele leer mejor; ambos manejan lo asíncrono/eventos.
- **¿Qué es inversión de control?** Que el framework/sistema llame a tu código cuando toca, no tú a él.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 118](../../parte-7-paradigmas/118-logico-reglas-hechos-y-unificacion-prolog/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 120 ⏭️](../../parte-7-paradigmas/120-reactivo-y-flujos-de-datos-streams/README.md)
