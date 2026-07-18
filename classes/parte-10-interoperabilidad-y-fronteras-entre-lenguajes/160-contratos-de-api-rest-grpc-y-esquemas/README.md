# Clase 160 — Contratos de API: REST, gRPC y esquemas

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender los **contratos de API (REST, gRPC)**: la frontera entre servicios se define con un contrato (qué operaciones, qué datos). Un endpoint REST combina un método (GET, POST) con un recurso (/users).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir un endpoint a partir de método y recurso.
2. Explicar qué es un contrato de API.
3. Distinguir REST de gRPC.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Contrato de API | El acuerdo entre servicios |
| 2 | REST | Recursos y métodos HTTP |
| 3 | gRPC | Contratos con esquema (Protobuf) |

## 📖 Definiciones y características

- **Contrato de API** — acuerdo de qué operaciones y datos expone un servicio. Clave: frontera estable entre componentes.
- **REST** — estilo basado en recursos y métodos HTTP (GET, POST, PUT). Clave: simple y universal.
- **gRPC** — framework de RPC con contratos definidos en Protobuf. Clave: eficiente y tipado.

## 🧩 Situación

El frontend habla con el backend a través de una API: `GET /users` pide los usuarios. El contrato define esos endpoints; mientras se respete, cada lado puede evolucionar por separado.

## 🧮 Modelo

- **Entrada** (stdin): una línea `metodo recurso`
- **Salida** (stdout): `contrato=<METODO> /<recurso>`
- **Regla:** combinar método y recurso en un endpoint

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `GET users` | `contrato=GET /users` |
| `POST items` | `contrato=POST /items` |
| `PUT data` | `contrato=PUT /data` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER metodo, recurso ; ESCRIBIR metodo + ' /' + recurso
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
| Sintáctica | Concatenación en cada lenguaje. |
| Semántica | El contrato desacopla cliente y servidor. |
| Paradigmática | SQL expone datos vía vistas/procedimientos. |

## 🧬 El concepto en la familia

REST (HTTP), gRPC (Protobuf), GraphQL son estilos de contrato entre servicios.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 160
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Cambiar el contrato sin versionar** → causa: romper a los clientes → solución: versionar la API y evolucionar con compatibilidad
- **Endpoints ambiguos** → causa: confusión y errores → solución: seguir convenciones REST claras

## ❓ Preguntas frecuentes

- **¿REST o gRPC?** REST para APIs públicas y simples; gRPC para comunicación interna eficiente y tipada.
- **¿Qué es un endpoint?** Un punto de acceso: método + ruta que ofrece una operación.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 159](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/159-serializacion-entre-lenguajes-json-protobuf-messagepack/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 161 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/161-procesos-y-comunicacion-stdin-stdout-sockets-colas/README.md)
