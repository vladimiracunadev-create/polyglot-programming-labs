# 🔷 TypeScript — 2012

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

TypeScript es un experimento que salió bien: **añadir tipos estáticos a un lenguaje dinámico que ya
tenía millones de líneas escritas**, sin romper ninguna. Su diseño está lleno de decisiones pragmáticas
que un lenguaje nuevo no habría tomado, y esas decisiones son exactamente lo que lo hizo funcionar.

> **🎯 Por qué está en este programa**
>
> **TypeScript es uno de los diez lenguajes del núcleo**, y está junto a
> [JavaScript](javascript.md) por una razón pedagógica: **es el mismo lenguaje con una capa de
> comprobación encima**, así que **la comparación entre los dos aísla exactamente lo que aportan los
> tipos**.
>
> Aporta al programa el concepto de **tipado gradual** —tipos donde compensan, dinámico donde no— y
> el de **borrado de tipos**: en TypeScript los tipos **desaparecen al compilar** y no existen en
> ejecución
> ([clase 108](../classes/parte-6-datos-y-estructuras/108-reflexion-e-introspeccion/README.md)),
> que es una decisión con consecuencias muy visibles.

| | |
|---|---|
| **Año** | 2012; **2.0** con `strictNullChecks` (2016); versión cada 3 meses |
| **Autoría** | **Anders Hejlsberg** y equipo, Microsoft — el mismo autor de [Delphi](delphi.md) y [C#](csharp.md) |
| **Familia** | JavaScript / web — superconjunto sintáctico estricto de JS |
| **Paradigma** | El de JavaScript, con un sistema de tipos estructural muy expresivo |
| **Tipado** | **Estático, estructural y gradual**; **borrado** en tiempo de compilación |
| **Memoria** | La de JavaScript: recolector automático |
| **Ejecución** | Se **transpila** a JavaScript; también se ejecuta directo en Deno, Bun y Node 22+ |
| **Estado** | 🟢 **Estándar de facto** para JavaScript a escala |

---

## 📜 Historia

Hacia 2010, Microsoft construía aplicaciones web grandes —Office en el navegador— y se encontraba con
el problema que todo equipo grande encuentra en JavaScript: **sin tipos, refactorizar es adivinar**
(clase 150).

**Anders Hejlsberg**, que ya había diseñado Turbo Pascal, [Delphi](delphi.md) y [C#](csharp.md),
dirigió el proyecto. Y la decisión de diseño clave, la que lo hizo posible, fue esta:

> **TypeScript es un superconjunto de JavaScript.** Todo programa JavaScript válido es un programa
> TypeScript válido. Los tipos son **opcionales** y **se borran al compilar**.

Eso permitió lo que ningún lenguaje nuevo consigue: **adoptarlo fichero a fichero**, en una base de
código existente, sin reescribir nada.

**TypeScript 2.0 (2016)** añadió `strictNullChecks`, que separa `string` de `string | null` y elimina
por comprobación la familia de errores más común de JavaScript. **2.8** trajo los tipos condicionales,
y a partir de ahí el sistema de tipos creció hasta ser **Turing-completo**: se pueden escribir cosas
como un analizador de rutas en el propio sistema de tipos.

El lenguaje se hizo estándar de facto con **Angular** (2016) y después con casi todo el ecosistema.
Y en **2025** el compilador se está reescribiendo en Go —el proyecto *Corsa*— buscando un orden de
magnitud de mejora en velocidad, que es la queja histórica.

## 🏭 Dónde vive hoy

- **Front-end**: React, Angular, Vue, Svelte — el ecosistema entero está tipado.
- **Node.js del lado del servidor**: NestJS, tRPC, y la mayoría de las bibliotecas publican tipos.
- **Herramientas de desarrollo**: VS Code está escrito en TypeScript.
- **Definiciones de tipos para bibliotecas JS**: el repositorio **DefinitelyTyped** tiene tipos para
  decenas de miles de paquetes que no los traen.
- **Contratos entre servicios**: generar tipos de TypeScript desde OpenAPI o Protobuf es una práctica
  estándar (clase 160).

## 🧠 Las tres decisiones que lo explican

**Una, el tipado estructural.** TypeScript no mira el nombre del tipo, mira **su forma**:

```typescript
interface Punto { x: number; y: number }
function dibujar(p: Punto) { /* ... */ }

dibujar({ x: 1, y: 2, color: "rojo" });   // ✓ compatible: tiene x e y
```

Es lo contrario del **tipado nominal** de [Java](java.md), [C#](csharp.md) y [Ada](ada.md), donde
hay que **declarar** que se implementa la interfaz. Y encaja con JavaScript, donde los objetos se
crean al vuelo (clase 112).

**Dos, los tipos se borran.** Esto es lo que más sorprende y lo que más consecuencias tiene:

```typescript
interface Usuario { nombre: string }
const u = JSON.parse(texto) as Usuario;    // ← ¡NADIE comprueba esto!
```

**En ejecución no hay tipos**, así que un `as` es una promesa sin verificación (clase 108). La defensa
del ecosistema es validar en la frontera con bibliotecas como **Zod** o **Valibot**, que **generan el
tipo a partir del validador** — la aplicación exacta de la regla de la clase 153: **validar donde
entra el dato**.

**Y tres, la escotilla de escape.** `any` desactiva la comprobación, y `strict` la vuelve exigente.
El lenguaje deja elegir **cuánta garantía se quiere**, y esa es la definición del tipado gradual.

> **El coste de esa flexibilidad es real.** Un proyecto sin `strict`, con `any` repartidos y con
> aserciones `as`, **tiene la ceremonia de un lenguaje tipado y las garantías de uno dinámico**. Por
> eso la primera decisión de cualquier proyecto TypeScript debería ser `"strict": true`, y las
> excepciones, justificadas una a una (clase 146).

## 🔄 Lo que se ha modernizado

- **`satisfies`** (4.9): comprobar que un valor encaja con un tipo **sin perder su tipo concreto**.
- **`const` en parámetros de tipo** y tipos literales de plantilla, que permiten expresar contratos
  muy precisos.
- **Decoradores** del estándar (5.0), tras años con la versión experimental.
- **Ejecución directa**: Deno, Bun y Node 22+ ejecutan `.ts` **borrando los tipos sin comprobarlos**,
  lo que separa la comprobación —que se hace en la integración continua (clase 147)— de la ejecución.
- **`tsgo`**, el compilador reescrito en Go, con mejoras de un orden de magnitud en proyectos grandes.

## ⚙️ Cómo se ejecuta hoy

```bash
npx tsc main.ts --target es2022 && node main.js    # el camino clásico
npx tsx main.ts                                     # ejecutar directo
deno run --allow-read main.ts

npx tsc --noEmit                 # solo COMPROBAR, sin generar (para CI, clase 147)
```

```jsonc
// tsconfig.json — la primera decisión del proyecto
{ "compilerOptions": { "strict": true, "noUncheckedIndexedAccess": true } }
```

## 🧪 El programa de la clase 041 en TypeScript

```typescript
import { readFileSync } from "node:fs";

// TypeScript añade tipos estáticos sobre JavaScript: se comprueban al compilar.
const [precio, cantidad, descuento]: number[] = readFileSync(0, "utf8")
  .trim()
  .split(/\s+/)
  .map(Number);

const subtotal: number = precio * cantidad;
const total: number = subtotal * (1 - descuento);

console.log(`Total: ${total.toFixed(2)}`);
```

**Lo que hay que ver, comparado con [la versión JavaScript](javascript.md).**

- **Es el mismo programa con anotaciones.** Quitando `: number[]` y `: number`, se obtiene JavaScript
  válido — que es la tesis del lenguaje.
- **`number[]` es una promesa que el compilador no puede cumplir del todo**: con
  `noUncheckedIndexedAccess`, `precio` sería `number | undefined`, porque **el compilador no sabe que
  la línea trae tres campos**. Esa opción, que casi nadie activa, es la que hace honesto el tipo.
- **Sigue habiendo un solo tipo numérico**, con lo que las consecuencias de la clase 072 son las de
  JavaScript: TypeScript **no añade enteros**, añade comprobación.
- **Y todas las anotaciones desaparecen** al compilar: el `.js` resultante es exactamente el de la
  ficha de JavaScript.

## 📚 Fuentes y bibliografía

- [Manual oficial de TypeScript](https://www.typescriptlang.org/docs/handbook/intro.html) — y el
  [playground](https://www.typescriptlang.org/play), que enseña el JavaScript generado.
- [Notas de versión](https://www.typescriptlang.org/docs/handbook/release-notes/overview.html) — cada
  versión con ejemplos.
- **Marius Schulz**, *TypeScript Evolution* — la historia de cada característica y por qué se añadió.
- **Boris Cherny**, *Programming TypeScript*, O'Reilly — el sistema de tipos explicado a fondo.
- **Dan Vanderkam**, *Effective TypeScript*, 2.ª ed., O'Reilly — 83 recomendaciones concretas; el
  mejor libro para pasar de "compila" a "está bien tipado".

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [JavaScript](javascript.md) · [C#](csharp.md) · [Dart](dart.md) · [Elm](elm.md)
