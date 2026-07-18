# Clase 147 — Integración continua (CI) multi-lenguaje

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **integración continua (CI)**: cada cambio dispara un pipeline de pasos (compilar, probar, lint); si todos pasan, el resultado es 'verde'. Si uno falla, es 'rojo' y el cambio se bloquea.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Combinar el resultado de varios pasos.
2. Explicar el pipeline de CI.
3. Reconocer el valor de bloquear en rojo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | CI | Verificar cada cambio |
| 2 | Pipeline | Pasos encadenados |
| 3 | Verde/rojo | Todo pasa o algo falla |

## 📖 Definiciones y características

- **Integración continua** — ejecutar automáticamente pruebas y checks en cada cambio. Clave: detecta errores pronto.
- **Pipeline** — secuencia de pasos (build, test, lint). Clave: todos deben pasar.
- **Verde/rojo** — estado del pipeline: todo pasa (verde) o algo falla (rojo). Clave: bloquea lo roto.

## 🧩 Situación

Al subir un cambio, el CI compila, prueba y revisa el estilo. Si algún paso falla, el pipeline se pone rojo y el cambio no se integra. Es lo que mantiene verde este repositorio.

## 🧮 Modelo

- **Entrada** (stdin): una línea con 0 y 1 (resultado de cada paso; 1 = pasó)
- **Salida** (stdout): `ci=<verde|rojo>`
- **Regla:** verde si todos los pasos son 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 1 1` | `ci=verde` |
| `1 0 1` | `ci=rojo` |
| `1 1` | `ci=verde` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER pasos ; verde <- todos == 1
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
| Sintáctica | all/every/reduce en cada lenguaje. |
| Semántica | Basta un paso en rojo para que el pipeline falle. |
| Paradigmática | SQL usa MIN sobre los pasos. |

## 🧬 El concepto en la familia

GitHub Actions, GitLab CI, Jenkins ejecutan pipelines que bloquean en rojo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 147
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ignorar el rojo del CI** → causa: integrar código roto → solución: no fusionar hasta que esté verde
- **Pipelines lentísimos** → causa: el equipo los evita → solución: optimizar con caché y paralelismo

## ❓ Preguntas frecuentes

- **¿Qué pasos debe tener?** Al menos compilar, probar y lint; según el proyecto, más.
- **¿CI y CD?** CI verifica; CD (entrega/despliegue continuos) automatiza la publicación.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 146](../../parte-9-ingenieria-de-software-poliglota/146-revision-de-codigo-y-estandares/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 148 ⏭️](../../parte-9-ingenieria-de-software-poliglota/148-entrega-y-despliegue/README.md)
