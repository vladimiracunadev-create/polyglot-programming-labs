# Clase 105 — JSON: serialización y deserialización

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Trabajar con **JSON**: el formato universal de intercambio de datos. Aquí se **serializa** (construye) un objeto JSON con un formato fijo; en la práctica también se deserializa (parsea).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Serializar datos a JSON.
2. Respetar el formato (comillas, dos puntos).
3. Reconocer JSON como formato de intercambio.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | JSON | Formato de intercambio de datos |
| 2 | Serializar | De datos a texto JSON |
| 3 | Deserializar | De texto JSON a datos |

## 📖 Definiciones y características

- **JSON** — formato de texto para datos estructurados (objetos, arreglos). Clave: universal entre lenguajes.
- **Serializar** — convertir datos en su representación de texto (JSON). Clave: para enviarlos o guardarlos.
- **Deserializar** — reconstruir datos desde el texto JSON. Clave: la operación inversa.

## 🧩 Situación

Las APIs web hablan JSON. Un objeto `{"nombre": "Ada", "edad": 36}` viaja entre un servidor en Go y un cliente en JavaScript sin problema: JSON es el idioma común.

## 🧮 Modelo

- **Entrada** (stdin): una línea `nombre edad` (una palabra y un entero)
- **Salida** (stdout): `{"nombre": "<nombre>", "edad": <edad>}`
- **Regla:** objeto JSON con las claves nombre y edad

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada 36` | `{"nombre": "Ada", "edad": 36}` |
| `Bo 5` | `{"nombre": "Bo", "edad": 5}` |
| `Cy 99` | `{"nombre": "Cy", "edad": 99}` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER nombre, edad ; construir objeto ; serializar a JSON
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
| Sintáctica | Librerías `json` (Python), `JSON.stringify` (JS), pero el formato es idéntico. |
| Semántica | Las cadenas van entre comillas dobles; los números sin comillas. |
| Paradigmática | SQL genera JSON con funciones `json_object` (aquí, con printf). |

## 🧬 El concepto en la familia

En Ruby `to_json`. En casi todos hay una librería estándar o popular para JSON; el formato no cambia.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 105
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comillas simples en JSON** → causa: JSON exige comillas dobles → solución: usar comillas dobles siempre
- **Poner comillas a los números** → causa: tipo incorrecto → solución: los números van sin comillas

## ❓ Preguntas frecuentes

- **¿Construir JSON a mano o con librería?** En la práctica, librería (escapa bien); aquí a mano para fijar el formato exacto.
- **¿JSON solo para web?** No: también para configuración, logs y almacenamiento.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 104](../../parte-6-datos-y-estructuras/104-archivos-leer-y-escribir-texto-y-binario/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 106 ⏭️](../../parte-6-datos-y-estructuras/106-otros-formatos-y-persistencia-csv-yaml-binarios-bases-de-datos/README.md)
