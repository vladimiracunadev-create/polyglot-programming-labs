# Clase 038 — Pruebas desde la terminal: pytest, node --test, go test, cargo test, dotnet test, phpunit

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Aprender a ejecutar pruebas automatizadas desde la línea de comandos en cada lenguaje. Las pruebas son código que verifica tu código: se corren con un comando y te dicen si algo se rompió. Es la base del verificador de equivalencia del curso y de cualquier proyecto profesional.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es una prueba automatizada y para qué sirve.
2. Nombrar el runner de pruebas de cada lenguaje del núcleo.
3. Relacionar las pruebas con el verificador de equivalencia del curso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Qué es una prueba | Código que comprueba que otro código funciona |
| 2 | Runners por lenguaje | pytest, go test, cargo test, dotnet test… |
| 3 | Rojo/verde | La prueba pasa o falla; el CI lo automatiza |
| 4 | Conexión con el curso | casos.json es una prueba de equivalencia |

## 📖 Definiciones y características

- **Prueba automatizada** — código que verifica que otro código produce el resultado esperado. Clave: se ejecuta con un comando y no depende de revisión manual.
- **Runner de pruebas** — herramienta que descubre y ejecuta las pruebas (pytest, cargo test). Clave: un comando corre todas.
- **Aserción** — comprobación de que un valor es el esperado. Clave: si falla, la prueba se pone en rojo.
- **Verde/rojo** — estado de la suite de pruebas: todo pasa (verde) o algo falla (rojo). Clave: el CI lo usa para bloquear cambios.

## 🧩 Situación

Cambias una función y no sabes si rompiste algo más. Ejecutas `pytest` y en segundos sabes si las 200 pruebas siguen en verde. Sin pruebas, ese cambio sería un salto de fe; con ellas, una comprobación.

## 🔎 Ejemplo

Comando de pruebas por lenguaje:

```text
Python   pytest
JS       node --test
Go       go test ./...
Rust     cargo test
C#       dotnet test
PHP      ./vendor/bin/phpunit
```

En este curso, además: python scripts/verificar_equivalencia.py --all

## ✍️ Práctica

El verificador de equivalencia es, en el fondo, una prueba: compara la salida real con la esperada. Ejecútalo sobre la clase 041 y observa el 'verde' de cada implementación.

## ⚠️ Errores comunes

- **Probar solo a mano ejecutando el programa** → causa: verificación lenta y no repetible → solución: escribir pruebas automatizadas que corran con un comando
- **No correr las pruebas antes de subir cambios** → causa: romper el CI → solución: ejecutar la suite localmente antes de hacer push

## ❓ Preguntas frecuentes

- **¿Cuántas pruebas necesito?** Al menos una por comportamiento importante y por caso límite; la calidad importa más que la cantidad.
- **¿casos.json es una prueba?** Sí: define entradas y salidas esperadas; el verificador las comprueba como haría un runner.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

---

> [⏮️ Clase 037](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/037-formateadores-y-linters-black-prettier-gofmt-rustfmt-clang-format-php-cs-fixer/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 039 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/039-empaquetado-y-distribucion-wheels-jars-binarios-contenedores/README.md)
