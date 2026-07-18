# Clase 166 — Diseño: responsabilidades y contratos entre componentes

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Diseñar el sistema definiendo **responsabilidades y contratos entre componentes**. Dos componentes encajan si respetan el mismo contrato en su frontera; aquí se comprueba comparando sus valores.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comprobar la compatibilidad de un contrato.
2. Explicar el papel de los contratos.
3. Reconocer fronteras entre componentes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Contrato | El acuerdo en la frontera |
| 2 | Compatibilidad | Ambos lados coinciden |
| 3 | Responsabilidad | Qué hace cada componente |

## 📖 Definiciones y características

- **Contrato de frontera** — acuerdo de datos y formato entre dos componentes. Clave: permite evolucionar por separado.
- **Compatibilidad** — que emisor y receptor esperan lo mismo. Clave: sin ella, la integración falla.
- **Responsabilidad** — la tarea única de un componente. Clave: define qué expone en el contrato.

## 🧩 Situación

El backend produce un formato que el frontend consume. Si ambos respetan el contrato, encajan; si uno cambia sin avisar, se rompen. Comprobar la compatibilidad evita sorpresas en la integración.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (los valores de contrato de cada componente)
- **Salida** (stdout): `contrato=<compatible|incompatible>`
- **Regla:** compatible si a == b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5 5` | `contrato=compatible` |
| `5 6` | `contrato=incompatible` |
| `0 0` | `contrato=compatible` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; compatible <- (a == b)
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
| Sintáctica | Comparación en cada lenguaje. |
| Semántica | El contrato desacopla los componentes. |
| Paradigmática | SQL compara valores. |

## 🧬 El concepto en la familia

Los tests de contrato (Pact) verifican que servicios independientes respetan su frontera.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 166
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Cambiar el contrato sin versionar** → causa: romper al otro lado → solución: versionar y evolucionar con compatibilidad
- **Fronteras implícitas** → causa: malentendidos → solución: documentar el contrato explícitamente

## ❓ Preguntas frecuentes

- **¿Cómo verificar contratos?** Con tests de contrato entre el consumidor y el proveedor.
- **¿Contrato o integración total?** El contrato permite probar cada lado por separado, más barato.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 165](../../parte-11-proyecto-integrador-poliglota/165-el-proyecto-un-sistema-con-componentes-en-varios-lenguajes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 167 ⏭️](../../parte-11-proyecto-integrador-poliglota/167-componente-cli-lenguaje-de-sistemas/README.md)
