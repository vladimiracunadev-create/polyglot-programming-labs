# Clase 012 — casos.json y el verificador de equivalencia

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender el mecanismo que hace único a este programa: un archivo `casos.json` con entradas y salidas comunes, y un verificador que ejecuta todas las implementaciones y comprueba que producen la **misma** salida. Es equivalencia demostrada por máquina, no prometida.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué contiene casos.json y qué define.
2. Ejecutar el verificador sobre una clase e interpretar su salida.
3. Entender por qué algunos lenguajes se omiten o se marcan como ilustrativos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El contrato de una clase | Entrada por stdin, salida por stdout, casos esperados |
| 2 | El verificador | Alimenta cada caso a cada implementación y compara |
| 3 | Degradación silenciosa | Si falta un toolchain, se omite e informa |

## 📖 Definiciones y características

- **casos.json** — contrato de la clase: descripción, fórmula y lista de {stdin, esperado}. Clave: es la fuente de verdad de la equivalencia.
- **Verificador de equivalencia** — script que corre las implementaciones contra casos.json. Clave: falla si dos difieren.
- **Ilustrativa** — implementación que no participa en la comparación por stdin (p. ej. SQL). Clave: se muestra pero no se compara igual.

## 🧩 Situación

Afirmar 'estas 10 implementaciones hacen lo mismo' es fácil de decir y fácil de equivocar. El verificador lo convierte en algo comprobable: si la de Rust imprime `27000.0` y las demás `27000.00`, el CI se pone rojo.

## 🔎 Ejemplo

Salida real del verificador sobre la clase 041:

```text
✅ python      3/3 casos
✅ javascript  3/3 casos
✅ java        3/3 casos
⏭️  go          omitido (toolchain 'go' no disponible)
ℹ️  sql         ilustrativa (declarativa, sin stdin)
```

Comando: `python scripts/verificar_equivalencia.py 041`

## ✍️ Práctica

Ejecuta `python scripts/verificar_equivalencia.py 041` en tu máquina. ¿Qué lenguajes verifica y cuáles omite según tus toolchains instalados?

## ⚠️ Errores comunes

- **Confiar en que 'seguro son equivalentes'** → causa: no verificar → solución: correr el verificador: la máquina no se cansa de comparar
- **Formatear distinto en un lenguaje** → causa: locale o decimales diferentes → solución: fijar el formato (cultura invariante, 2 decimales) en todas las implementaciones

## ❓ Preguntas frecuentes

- **¿Qué NO verifica?** El texto de las clases y el Atlas: son material de lectura, no se ejecutan en CI.
- **¿Por qué SQL es ilustrativa?** Es declarativa: no lee stdin como las demás; se muestra la misma fórmula como consulta.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).

---

> [⏮️ Clase 011](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/011-anatomia-de-una-ficha-de-transferencia-y-como-estudiarla/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 013 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/013-el-concepto-en-la-familia-leer-un-lenguaje-que-no-conoces/README.md)
