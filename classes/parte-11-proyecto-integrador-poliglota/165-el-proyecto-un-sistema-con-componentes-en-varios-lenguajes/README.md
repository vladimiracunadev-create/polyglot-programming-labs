# Clase 165 — El proyecto: un sistema con componentes en varios lenguajes

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Arrancar el **proyecto integrador**: un sistema real hecho de componentes en varios lenguajes. El primer paso es inventariar los componentes que lo forman.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Inventariar los componentes de un sistema.
2. Nombrar cada pieza.
3. Entender el proyecto como suma de componentes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Sistema | El todo integrado |
| 2 | Componente | Cada pieza con su lenguaje |
| 3 | Inventario | Qué partes lo forman |

## 📖 Definiciones y características

- **Sistema integrador** — producto compuesto por varios componentes que colaboran. Clave: cada uno en su lenguaje idóneo.
- **Componente** — pieza con una responsabilidad. Clave: se integra con las demás.
- **Inventario** — lista de las partes del sistema. Clave: primer paso del diseño.

## 🧩 Situación

Antes de construir, se enumeran los componentes: CLI, API, web, datos. Ese inventario define el alcance del proyecto integrador y qué lenguaje usará cada pieza.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de componentes (palabras)
- **Salida** (stdout): `componentes=<N> nombres=<unidos por ->`
- **Regla:** contar y listar los componentes

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3 nombres=cli-api-web` |
| `app` | `componentes=1 nombres=app` |
| `web api datos cache` | `componentes=4 nombres=web-api-datos-cache` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER componentes ; ESCRIBIR conteo y nombres unidos
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
| Sintáctica | Contar y unir en cada lenguaje. |
| Semántica | Cada componente puede estar en otro lenguaje. |
| Paradigmática | SQL agrega con group_concat. |

## 🧬 El concepto en la familia

Todo sistema real es un inventario de componentes con responsabilidades y lenguajes propios.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 165
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Componentes sin responsabilidad clara** → causa: solapamientos → solución: una responsabilidad por componente
- **Olvidar un componente** → causa: integración incompleta → solución: inventariar todas las piezas

## ❓ Preguntas frecuentes

- **¿Cuántos componentes?** Los que el problema justifique; ni de más ni de menos.
- **¿Por dónde empezar?** Por el inventario y los contratos entre componentes.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 164](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/164-elegir-el-lenguaje-correcto-para-cada-componente/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 166 ⏭️](../../parte-11-proyecto-integrador-poliglota/166-diseno-responsabilidades-y-contratos-entre-componentes/README.md)
