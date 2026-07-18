# Clase 159 — Serialización entre lenguajes: JSON, Protobuf, MessagePack

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **serialización entre lenguajes** (JSON, Protobuf, MessagePack): convertir datos a un formato común para que un componente en un lenguaje los envíe y otro en otro lenguaje los reciba. Aquí se serializa un par a texto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Serializar un dato a un formato de intercambio.
2. Explicar por qué se necesita un formato común.
3. Reconocer JSON/Protobuf/MessagePack.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Serialización | De datos a formato de intercambio |
| 2 | Formato común | Entendido por todos |
| 3 | Esquema | Estructura acordada |

## 📖 Definiciones y características

- **Serialización** — convertir datos en un formato transmisible (texto o binario). Clave: cruzar la frontera de lenguaje.
- **Formato de intercambio** — representación común (JSON, Protobuf). Clave: independiente del lenguaje.
- **Esquema** — estructura acordada de los datos. Clave: emisor y receptor lo comparten.

## 🧩 Situación

Un servicio en Go envía datos a uno en Python: los serializa (a JSON o Protobuf), viajan como bytes y el otro los deserializa. El formato común es lo que permite el diálogo entre lenguajes.

## 🧮 Modelo

- **Entrada** (stdin): una línea `clave valor`
- **Salida** (stdout): `serializado=<clave>:<valor>`
- **Regla:** unir clave y valor con ':'

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `x 5` | `serializado=x:5` |
| `edad 30` | `serializado=edad:30` |
| `n 100` | `serializado=n:100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER clave, valor ; ESCRIBIR clave:valor
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
| Sintáctica | Concatenación (aquí); librerías JSON/Protobuf en la práctica. |
| Semántica | El formato debe interpretarse igual en ambos lados. |
| Paradigmática | SQL exporta a JSON con funciones del motor. |

## 🧬 El concepto en la familia

JSON (texto, universal), Protobuf/MessagePack (binarios, compactos y con esquema) son los formatos habituales.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 159
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Formato ambiguo sin esquema** → causa: el receptor no sabe interpretar → solución: acordar un esquema o formato estándar
- **Diferencias de codificación** → causa: acentos/emoji corruptos → solución: usar UTF-8 y formatos bien definidos

## ❓ Preguntas frecuentes

- **¿JSON o Protobuf?** JSON es legible y universal; Protobuf es compacto y tipado. Según el caso.
- **¿Serializar y deserializar son inversos?** Sí: uno convierte a formato, el otro reconstruye el dato.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 158](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/158-enlaces-bindings-y-wrappers/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 160 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/160-contratos-de-api-rest-grpc-y-esquemas/README.md)
