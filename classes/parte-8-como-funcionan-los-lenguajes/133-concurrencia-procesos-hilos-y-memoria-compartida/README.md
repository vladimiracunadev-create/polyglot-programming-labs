# Clase 133 — Concurrencia: procesos, hilos y memoria compartida

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir la **concurrencia con memoria compartida**: varios hilos acceden a los mismos datos. Contar con un acumulador compartido ilustra el modelo; en concurrencia real, ese acceso debe protegerse.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar con un acumulador compartido.
2. Explicar procesos, hilos y memoria compartida.
3. Reconocer el riesgo de acceso concurrente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Proceso vs. hilo | Aislado vs. comparte memoria |
| 2 | Memoria compartida | Varios hilos, mismos datos |
| 3 | Protección | Evitar el acceso simultáneo inseguro |

## 📖 Definiciones y características

- **Proceso** — programa en ejecución con su propia memoria aislada. Clave: no comparte por defecto.
- **Hilo** — línea de ejecución dentro de un proceso; comparte su memoria. Clave: acceso concurrente a los datos.
- **Memoria compartida** — datos accesibles por varios hilos. Clave: requiere sincronización para ser segura.

## 🧩 Situación

Los hilos de un proceso comparten memoria: es rápido comunicar, pero peligroso si dos escriben a la vez el mismo dato. Contar con un acumulador es el ejemplo de un estado compartido.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `cuenta=<número de elementos>`
- **Regla:** acumulador compartido que cuenta los elementos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `cuenta=3` |
| `5` | `cuenta=1` |
| `10 20 30 40` | `cuenta=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
cuenta <- 0 ; PARA CADA elemento: cuenta <- cuenta + 1
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
| Sintáctica | Un contador compartido en cada lenguaje. |
| Semántica | Con hilos reales haría falta un mutex; aquí es secuencial. |
| Paradigmática | SQL delega el paralelismo al motor. |

## 🧬 El concepto en la familia

Java/C#/C++ comparten memoria entre hilos (con locks); Go y Erlang prefieren comunicar en vez de compartir.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 133
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Compartir sin sincronizar** → causa: condiciones de carrera → solución: proteger el acceso con mutex o preferir mensajes
- **Sobre-sincronizar** → causa: cuellos de botella → solución: minimizar la sección crítica

## ❓ Preguntas frecuentes

- **¿Compartir memoria o comunicar?** 'No comuniques compartiendo memoria; comparte comunicando' (lema de Go).
- **¿Proceso o hilo?** Hilo para compartir datos rápido; proceso para aislar y ser robusto.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 132](../../parte-8-como-funcionan-los-lenguajes/132-raii-propiedad-y-prestamos-rust-c-plus-plus/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 134 ⏭️](../../parte-8-como-funcionan-los-lenguajes/134-tareas-corrutinas-y-canales/README.md)
