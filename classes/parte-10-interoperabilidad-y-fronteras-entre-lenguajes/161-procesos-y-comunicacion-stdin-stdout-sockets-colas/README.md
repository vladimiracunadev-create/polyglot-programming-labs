# Clase 161 — Procesos y comunicación: stdin/stdout, sockets, colas

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **comunicación entre procesos**: procesos separados intercambian datos por tuberías (stdin/stdout), sockets o colas. Una cola FIFO entrega los datos en orden a un consumidor que los suma.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Recibir datos por una cola.
2. Explicar los mecanismos de comunicación entre procesos.
3. Reconocer stdin/stdout como tubería.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tubería (pipe) | stdout de uno a stdin de otro |
| 2 | Cola/socket | Comunicación asíncrona o en red |
| 3 | Productor/consumidor | Uno envía, otro recibe |

## 📖 Definiciones y características

- **Comunicación entre procesos (IPC)** — mecanismos para que procesos separados intercambien datos. Clave: tuberías, sockets, colas.
- **Tubería** — conecta la salida de un proceso con la entrada de otro. Clave: base de los comandos Unix encadenados.
- **Cola** — buffer FIFO que desacopla productor y consumidor. Clave: comunicación asíncrona.

## 🧩 Situación

En Unix, `productor | consumidor` conecta procesos por una tubería. Este curso usa justo eso: stdin/stdout como frontera común entre implementaciones. Aquí una cola entrega los números y se suman.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (mensajes en la cola)
- **Salida** (stdout): `recibido=<suma de los mensajes>`
- **Regla:** sumar los mensajes recibidos en orden

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `recibido=6` |
| `5` | `recibido=5` |
| `10 20 30 40` | `recibido=100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PARA CADA mensaje de la cola: acumular ; ESCRIBIR suma
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
| Sintáctica | Recorrer la entrada (cola) en cada lenguaje. |
| Semántica | La cola desacopla al productor del consumidor. |
| Paradigmática | SQL no maneja procesos; agrega datos. |

## 🧬 El concepto en la familia

Tuberías Unix, sockets, y colas (RabbitMQ, Kafka) conectan procesos y servicios.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 161
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir orden con múltiples productores** → causa: mensajes entremezclados → solución: una cola por flujo o marcar el orden
- **No cerrar la tubería** → causa: el consumidor espera para siempre → solución: cerrar/EOF al terminar de enviar

## ❓ Preguntas frecuentes

- **¿Tubería o socket?** Tubería para procesos en la misma máquina; socket para red.
- **¿Por qué stdin/stdout?** Es la tubería universal; por eso el curso verifica con ella.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 160](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/160-contratos-de-api-rest-grpc-y-esquemas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 162 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/162-webassembly-como-objetivo-comun/README.md)
