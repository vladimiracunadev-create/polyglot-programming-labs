# 🟨 JavaScript — 1995

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

JavaScript se diseñó **en diez días**, se le puso el nombre de otro lenguaje por marketing, y hoy es
el único que ejecutan todos los navegadores del mundo. Es el caso más claro de que **la suerte de una
tecnología no depende solo de su calidad** — y también de que un lenguaje puede mejorar muchísimo sin
poder romper nada.

> **🎯 Por qué está en este programa**
>
> **JavaScript es uno de los diez lenguajes del núcleo**, y es el **representante de la familia
> web** ([Atlas](README.md#javascript-web)) junto con [TypeScript](typescript.md).
>
> Aporta al programa tres conceptos que ningún otro del núcleo enseña igual: **la herencia por
> prototipos** en vez de por clases
> ([clase 112](../classes/parte-7-paradigmas-de-programacion/112-prototipos-frente-a-clases/README.md)),
> **el bucle de eventos con un solo hilo**
> ([clase 134](../classes/parte-8-como-funcionan-los-lenguajes/134-corrutinas-generadores-y-canales/README.md))
> y **la coerción débil de tipos**, que es el mejor ejemplo posible de por qué la igualdad es un tema
> (clase 100).

| | |
|---|---|
| **Año** | 1995; **ES5** en 2009; **ES6/ES2015**, el punto de inflexión; anual desde entonces |
| **Autoría** | **Brendan Eich**, Netscape — el prototipo, en diez días |
| **Familia** | JavaScript / web; sintaxis de C, semántica de Scheme y Self |
| **Paradigma** | Multiparadigma: funcional, orientado a objetos por prototipos, imperativo |
| **Tipado** | **Dinámico y débil**: las conversiones implícitas son parte del diseño |
| **Memoria** | Automática, con recolector generacional |
| **Ejecución** | JIT (V8, SpiderMonkey, JavaScriptCore); también AOT en algunos entornos |
| **Estado** | 🟢 **Ubicuo** — navegador, servidor, escritorio, móvil y sistemas embebidos |

---

## 📜 Historia

En **1995**, Netscape quería un lenguaje de guion para su navegador. Contrató a **Brendan Eich** con
el encargo de que **se pareciera a Java** —que era lo que estaba de moda— y le dio **diez días** para
el prototipo.

Eich quería hacer un Scheme para el navegador. El resultado fue un compromiso que explica casi todas
las rarezas del lenguaje: **funciones de primera clase y cierres de Scheme, herencia por prototipos de
Self, y sintaxis de llaves de Java**. Se llamó primero Mocha, luego LiveScript, y finalmente
**JavaScript** por un acuerdo comercial con Sun — un nombre que ha causado confusión durante treinta
años, porque **Java y JavaScript no tienen relación**.

Microsoft respondió con **JScript**, y de ahí nació la estandarización en **ECMA** — de donde viene el
nombre feo pero correcto: **ECMAScript**.

Los años de **ES3 a ES5 (1999-2009)** fueron de estancamiento: ES4 se abandonó tras una guerra
política, y el lenguaje se quedó congelado mientras la web crecía. Lo que sí ocurrió en esa década fue
**jQuery** —que tapó las diferencias entre navegadores— y **V8** (2008), el motor de Chrome con JIT
que **multiplicó por cien el rendimiento** y cambió lo que se podía hacer con el lenguaje.

**Node.js (2009)** sacó JavaScript del navegador usando V8, y **ES2015 (ES6)** lo modernizó de golpe:
`let`/`const`, clases, módulos, promesas, funciones flecha, desestructuración, plantillas de cadena.
Desde entonces hay **una versión anual**, y el lenguaje ha crecido con `async`/`await`, opcional
encadenado, `BigInt` y el emparejamiento de patrones en camino.

## 🏭 Dónde vive hoy

- **Todos los navegadores**: es el único lenguaje que ejecutan de forma nativa, y por eso todo lo
  demás compila a él o a [WebAssembly](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/162-webassembly-como-objetivo-comun/README.md).
- **Servidores**: Node.js, Deno y Bun mueven una parte enorme de la web.
- **Escritorio**: Electron — VS Code, Slack, Discord, Figma.
- **Móvil**: React Native.
- **Herramientas de construcción** de casi todos los ecosistemas front-end.
- **Sistemas embebidos y bases de datos**: motores ligeros como QuickJS y Duktape se incrustan en
  routers, televisores y bases de datos como lenguaje de extensión (clase 163).

## 🧠 Lo que enseña y nadie más enseña igual

**Uno, los prototipos** (clase 112). En JavaScript **no hay clases de verdad**: `class` es azúcar
sobre un mecanismo donde **cada objeto tiene un enlace a otro objeto**, y la búsqueda de una propiedad
sube por esa cadena. Es más simple y más flexible que las clases, y es el modelo que
[Self](smalltalk.md) inventó.

**Dos, el bucle de eventos** (clases 134 y 161). JavaScript tiene **un solo hilo**, y toda la
concurrencia es asíncrona: la operación se registra y se sigue; cuando termina, el bucle ejecuta la
retrollamada. Es el mismo modelo que [Tcl](tcl.md) tenía en 1993 con `fileevent`, y es lo que permite
atender decenas de miles de conexiones sin un hilo por cada una.

**Y tres, la coerción débil**, que es el ejemplo didáctico perfecto de la clase 100:

```javascript
0 == "0"          // true
0 == []           // true
"0" == []         // false   ← la igualdad NO es transitiva
[] + {}           // "[object Object]"
0.1 + 0.2         // 0.30000000000000004   (clase 073: esto pasa en TODOS)
```

> **Y aquí conviene ser justo.** La última línea **no es un defecto de JavaScript**: es IEEE 754, y
> ocurre igual en Python, Java y C (clase 073). Las anteriores sí lo son, y la respuesta del
> ecosistema fue clara: **usar siempre `===`**, que no convierte. Es exactamente el patrón de la
> clase 146 — **una regla de estilo que corrige una decisión del lenguaje** y que los analizadores
> hacen cumplir.

## 🔄 Lo que se ha modernizado

- **De `var` a `let`/`const`**, que arregla el alcance por función y el *hoisting* (clase 087).
- **Módulos ESM** en el estándar, tras años de CommonJS y de empaquetadores.
- **`async`/`await`** sobre promesas: código asíncrono con aspecto secuencial (clase 134).
- **`BigInt`** para enteros de precisión arbitraria, y `Temporal` para fechas —la corrección de la
  peor API de la biblioteca estándar—.
- **Ejecutores nuevos**: **Deno** (seguro por capacidades desde el arranque, clase 153) y **Bun**
  (rapidez y herramientas integradas).
- **Aislamiento real**: los *realms* y los objetos endurecidos, herederos directos de la investigación
  en capacidades de [Smalltalk](smalltalk.md) y del lenguaje E (clase 153).

## ⚙️ Cómo se ejecuta hoy

```bash
node main.mjs < entrada.txt        # el comando de la clase 041
deno run --allow-read main.mjs      # con permisos EXPLÍCITOS
bun run main.mjs

npx eslint . && npx prettier --check .    # calidad (clase 146)
node --test                                # pruebas, en el propio Node
```

## 🧪 El programa de la clase 041 en JavaScript

```javascript
import { readFileSync } from "node:fs";

// Números en JS: un solo tipo `number` (doble de 64 bits) para todo.
const [precio, cantidad, descuento] = readFileSync(0, "utf8")
  .trim()
  .split(/\s+/)
  .map(Number);

const subtotal = precio * cantidad;
const total = subtotal * (1 - descuento);

console.log(`Total: ${total.toFixed(2)}`);
```

**Lo que hay que ver.**

- **Hay un solo tipo numérico.** No existe `int`: `cantidad` es un **doble de 64 bits**, igual que el
  precio. Eso simplifica el lenguaje y trae la consecuencia de la clase 072: **los enteros por encima
  de 2⁵³ pierden precisión**, que es la razón de que las APIs envíen los identificadores grandes como
  cadenas (clase 159).
- **`const` no significa constante**: significa que **el nombre no se reasigna**. Un objeto declarado
  con `const` sigue siendo mutable — una distinción que la clase 102 desarrolla.
- **La cadena de `.trim().split().map()`** es el estilo funcional del lenguaje, heredado de Scheme y
  popularizado por las bibliotecas.
- **`readFileSync(0, ...)`** lee el descriptor 0, que es la entrada estándar: Node no tiene una
  lectura de línea síncrona sencilla, y este es el idioma habitual.

## 📚 Fuentes y bibliografía

- [MDN Web Docs](https://developer.mozilla.org/es/docs/Web/JavaScript) — la referencia, y está en
  español.
- [Especificación ECMA-262](https://tc39.es/ecma262/) y las [propuestas de TC39](https://github.com/tc39/proposals)
  — para saber qué viene y en qué etapa está.
- **Kyle Simpson**, *You Don't Know JS Yet*, 2.ª ed. — libre en línea; la mejor explicación de
  cierres, `this` y prototipos.
- **Axel Rauschmayer**, *JavaScript for impatient programmers* — libre en línea, actualizado cada año.
- **Douglas Crockford**, *JavaScript: The Good Parts* — histórico y discutible hoy, pero explica por
  qué el ecosistema adoptó `===` y el modo estricto.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [TypeScript](typescript.md) · [Dart](dart.md) · [Elm](elm.md) ·
[ActionScript](actionscript.md) · [Lua](lua.md)
