# Clase 001 — Qué es programar y por qué comparar lenguajes: la tesis políglota

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender que programar es resolver problemas con instrucciones precisas, y que ese conocimiento es **transferible**: un mismo concepto (una variable, un bucle, una función) existe en todos los lenguajes; lo que cambia es la forma. Aprenderlo una vez permite reconocerlo, compararlo y aplicarlo en cualquier lenguaje.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar la diferencia entre aprender *un* lenguaje y aprender *a programar*.
2. Enunciar la tesis políglota: concepto → forma neutral → implementaciones → comparación → transferencia.
3. Distinguir el conocimiento transferible del detalle sintáctico de un lenguaje.
4. Justificar por qué comparar lenguajes acelera el aprendizaje en vez de dispersarlo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Programar = resolver con precisión | Separa la idea (algoritmo) de su escritura (lenguaje) |
| 2 | Concepto vs. sintaxis | Lo que perdura frente a lo que cambia entre lenguajes |
| 3 | Los 10 lenguajes del núcleo | El terreno práctico que se implementa y verifica |
| 4 | Las ~40 familias del Atlas | Amplían la comprensión sin multiplicar el mantenimiento |
| 5 | Reconocer, comparar, aplicar | El ciclo que convierte teoría en habilidad |

## 📖 Definiciones y características

- **Programar** — expresar la solución de un problema como instrucciones que una máquina ejecuta. Clave: la idea es independiente del lenguaje.
- **Conocimiento transferible** — idea que sobrevive al cambio de lenguaje (p. ej. 'iterar una colección'). Clave: es lo que de verdad se aprende.
- **Núcleo** — los 10 lenguajes que se implementan y verifican en CI. Clave: profundidad práctica.
- **Atlas** — cobertura de ~40 lenguajes por sus características. Clave: amplitud de comprensión.

## 🧩 Situación

Alguien aprende Python, hace 50 ejercicios y se siente capaz. Le piden mantener un servicio en Go. Se bloquea: cree que no sabe programar, cuando en realidad **sí** sabe — solo no reconoce los mismos conceptos con otra piel. Este programa ataca justamente eso.

## 🔎 Ejemplo

El mismo concepto ("guardar un valor con nombre") en tres lenguajes:

```text
Python:  total = 27000
Go:      total := 27000
Rust:    let total = 27000;
```

Cambia la escritura, **no** la idea: un nombre apunta a un valor. Eso es lo transferible.

## ✍️ Práctica

Escribe en una frase, sin usar ningún lenguaje, qué hace este programa: `precio * cantidad`. Luego búscalo escrito en dos lenguajes que conozcas y subraya qué es idéntico y qué cambia.

## ⚠️ Errores comunes

- **Creer que "sé Python" = "sé programar"** → causa: confundir el lenguaje con la disciplina → solución: estudiar el concepto y luego reconocerlo en otro lenguaje
- **Memorizar sintaxis sin el concepto detrás** → causa: aprender la forma sin el fondo → solución: para cada línea, preguntar "¿qué idea neutral expresa?"

## ❓ Preguntas frecuentes

- **¿Necesito saber los 10 lenguajes antes de empezar?** No. Empiezas por el concepto; los lenguajes se introducen comparándolos.
- **¿No es más fácil dominar uno solo?** Para tu primer empleo, quizá. Para entender de verdad la programación, comparar revela por qué cada lenguaje decide lo que decide.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 002 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/002-las-tres-clases-de-diferencia-sintactica-semantica-y-paradigmatica/README.md)
