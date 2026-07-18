# Clase 144 — Compilación reproducible y empaquetado

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **compilación reproducible y el empaquetado**: una build reproducible produce siempre el mismo artefacto para la misma entrada, comprobable con una suma de verificación (checksum). Aquí el checksum es la suma de los valores.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular una suma de comprobación.
2. Explicar la reproducibilidad.
3. Relacionar el checksum con la verificación de artefactos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Reproducibilidad | Misma entrada, mismo artefacto |
| 2 | Checksum | Huella de los datos |
| 3 | Verificación | Detectar cambios |

## 📖 Definiciones y características

- **Compilación reproducible** — produce un artefacto idéntico byte a byte para la misma entrada. Clave: confianza y auditoría.
- **Checksum** — valor derivado de los datos que cambia si estos cambian. Clave: detecta alteraciones.
- **Artefacto** — salida de la build (binario, paquete). Clave: se verifica con su checksum.

## 🧩 Situación

Al descargar un binario, su checksum publicado permite verificar que no fue alterado. Una build reproducible da siempre el mismo checksum, lo que hace auditable la cadena de suministro.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `checksum=<suma de los valores>`
- **Regla:** checksum = suma de los valores

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `checksum=6` |
| `5` | `checksum=5` |
| `10 20 30` | `checksum=60` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; checksum <- suma ; ESCRIBIR checksum
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
| Sintáctica | Suma en cada lenguaje (un checksum real usaría un hash). |
| Semántica | La misma entrada da el mismo checksum: reproducibilidad. |
| Paradigmática | SQL suma con SUM. |

## 🧬 El concepto en la familia

Los gestores de paquetes verifican con SHA-256; aquí una suma simple ilustra el concepto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 144
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en un checksum débil** → causa: colisiones → solución: usar hashes criptográficos para seguridad real
- **Builds no reproducibles** → causa: checksums que cambian sin motivo → solución: eliminar fuentes de no-determinismo (fechas, orden)

## ❓ Preguntas frecuentes

- **¿Suma o hash?** Para integridad real se usa un hash (SHA-256); la suma solo ilustra.
- **¿Por qué builds reproducibles?** Auditar que el binario proviene del código y no fue manipulado.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 143](../../parte-9-ingenieria-de-software-poliglota/143-dependencias-versiones-y-lockfiles/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 145 ⏭️](../../parte-9-ingenieria-de-software-poliglota/145-git-y-control-de-versiones-para-proyectos-poliglotas/README.md)
