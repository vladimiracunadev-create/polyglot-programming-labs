# Clase 021 — Familia JavaScript y web: JS, TypeScript, Dart

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la familia que domina la web. **JavaScript** nació en 1995, en diez días de trabajo febril de Brendan Eich en Netscape, para animar páginas en el navegador; hoy corre en todas partes: navegador, servidor, móvil y hasta dispositivos embebidos. **TypeScript** le añade un sistema de tipos estáticos sin dejar de ser JavaScript. **Dart**, de Google, es su primo para construir aplicaciones (el motor de Flutter). Los tres comparten la sintaxis de llaves heredada de C y un modelo de ejecución **asíncrono basado en eventos** que es su rasgo más distintivo y más malentendido.

Esto importa porque JavaScript es probablemente el lenguaje más consecuente de la historia por accidente: pensado para pequeños adornos, acabó siendo el único lenguaje nativo del navegador y, por tanto, ineludible. Su genealogía es peculiar y vale la pena conocerla: tomó la sintaxis de Java (por marketing), las funciones de primera clase de Scheme (un Lisp) y la herencia por prototipos de Self. Entender esa mezcla explica por qué JavaScript se siente a la vez familiar y extraño.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar por qué JavaScript es omnipresente (navegador, servidor con Node, móvil).
2. Entender qué añade TypeScript sobre JavaScript y por qué es un *superset*.
3. Reconocer el modelo asíncrono de eventos (bucle de eventos, promesas, async/await).
4. Situar la herencia por prototipos frente a la herencia por clases.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | JavaScript: el lenguaje de la web | Único nativo en el navegador; también servidor (Node) |
| 2 | TypeScript: tipos sobre JS | Comprobación estática que transpila a JS |
| 3 | Prototipos | Herencia entre objetos, no entre clases |
| 4 | Asincronía y bucle de eventos | Callbacks, promesas y async/await |
| 5 | Dart y otros primos | Alternativas que compilan a/para la web y móvil |

## 📖 Definiciones y características

**JavaScript** (Brendan Eich, Netscape, 1995) es un lenguaje dinámico, de tipado débil y basado en **prototipos**. Su historia de diseño es una mezcla deliberada: la dirección de Netscape quería que "se pareciera a Java" para subirse a la moda del momento, de ahí las llaves, los `if` y los `for` de la familia C; pero Eich, admirador de Scheme, le dio funciones de primera clase (se pasan como valores, se anidan, forman clausuras), y tomó de Self la idea de que los objetos heredan directamente de otros objetos en lugar de instanciar clases. Esa herencia por prototipos es lo que distingue a JavaScript de casi todos sus vecinos de llaves. Estandarizado como **ECMAScript** por Ecma International, el lenguaje pasó años estancado hasta que la edición **ES2015** (ES6) lo modernizó con clases sintácticas, `let`/`const`, módulos, promesas y funciones flecha. En 2009, Node.js incrustó el motor V8 de Google fuera del navegador y convirtió a JavaScript en un lenguaje de propósito general, capaz de correr servidores.

El talón de Aquiles de JavaScript es su falta de tipos estáticos: en una base de código grande, errores como llamar a un método que no existe o pasar un número donde se esperaba un texto solo aparecen en ejecución, a veces en producción. **TypeScript** (Microsoft, 2012, también obra de Anders Hejlsberg) es la respuesta: un **superset** de JavaScript, es decir, todo JavaScript válido es TypeScript válido, al que se le añade un sistema de tipos estáticos opcional y gradual. El compilador de TypeScript comprueba esos tipos y luego los **borra por completo**: el resultado es JavaScript corriente que el navegador ejecuta. Esto es clave y suele confundirse: los tipos de TypeScript no existen en tiempo de ejecución, solo sirven durante el desarrollo para atrapar errores antes. Es un modelo distinto al de Java o Rust, donde los tipos también informan la representación en memoria; en TypeScript son puramente una capa de comprobación que desaparece al transpilar.

El tercer rasgo compartido —y el que más cuesta a los recién llegados— es el modelo **asíncrono de un solo hilo**. JavaScript no bloquea esperando a que termine una operación lenta (una petición de red, leer un archivo): registra qué hacer cuando termine y sigue. Un **bucle de eventos** va sacando esas tareas completadas de una cola y ejecutando sus continuaciones. Históricamente esto se escribía con *callbacks* anidados (el temido "callback hell"), luego con **promesas**, y desde ES2017 con `async/await`, que hace que el código asíncrono se lea como secuencial sin bloquear. **Dart** (Google, 2011), primo de esta familia, comparte la sintaxis de llaves y un modelo asíncrono similar, pero añade tipado sólido y compilación a nativo; es el lenguaje de Flutter para apps móviles multiplataforma.

- **JavaScript** — 1995 (Brendan Eich, Netscape), dinámico y basado en prototipos. Clave: único lenguaje nativo del navegador; núcleo del curso.
- **TypeScript** — 2012 (Microsoft), superset de JS con tipos estáticos que se borran al compilar. Clave: red de seguridad en desarrollo; núcleo del curso.
- **Prototipos** — modelo de OO donde los objetos heredan de otros objetos, no de clases. Clave: rasgo distintivo de JavaScript.
- **Bucle de eventos** — mecanismo que ejecuta continuaciones de tareas asíncronas en un solo hilo. Clave: el corazón del modelo async de la familia.

## 🧩 Situación

Un proyecto que empezó como un prototipo de mil líneas de JavaScript crece hasta cincuenta mil, y con él se multiplican los errores del tipo `undefined is not a function`, que solo estallan cuando un usuario recorre justo esa ruta poco probada. El equipo adopta TypeScript de forma gradual: al añadir tipos, el compilador empieza a señalar, antes de ejecutar nada, todas las llamadas mal escritas y los campos que a veces son nulos. No cambian de familia ni reescriben el proyecto —sigue siendo JavaScript al ejecutarse—, solo le colocan una red de seguridad que atrapa en la mesa del programador lo que antes caía sobre el usuario.

## 🔎 Ejemplo

TypeScript es JavaScript con tipos: el mismo código, con garantías añadidas que desaparecen al ejecutar.

```text
JavaScript:  function doble(x)          { return x * 2; }
TypeScript:  function doble(x: number): number { return x * 2; }
```

El **delta** es la anotación `: number`. En JavaScript, `doble("hola")` no falla al escribirlo: se ejecuta y devuelve `NaN`, un error silencioso que puede propagarse lejos antes de notarse. En TypeScript, esa misma llamada no compila: el error se detecta en el editor, meses antes de llegar a producción. Y sin embargo, tras transpilar, ambos producen exactamente el mismo JavaScript: los tipos ya cumplieron su función y se borraron.

## ✍️ Práctica

TypeScript infiere y comprueba tipos como Java o Rust, pero —a diferencia de ellos— sus tipos desaparecen al ejecutar (se transpila a JavaScript). Escribe en dos frases a qué modelo del núcleo se parece más y en qué se diferencia. Luego busca un ejemplo de `async/await` en JavaScript y explica qué haría el bucle de eventos mientras la operación `await` está pendiente.

## ⚠️ Errores comunes

- **Creer que TypeScript es un lenguaje distinto de JavaScript** → causa: no ver que es un superset → solución: recordar que todo JS válido es TS válido; TS solo añade una capa de tipos que se borra.
- **Esperar que los tipos de TypeScript existan en ejecución** → causa: confundir comprobación estática con información de runtime → solución: recordar que se borran al transpilar; para validar datos externos hacen falta comprobaciones explícitas.
- **Programar asíncrono como si fuera secuencial** → causa: ignorar el bucle de eventos → solución: entender promesas y `async/await` desde el inicio, y que un solo hilo no bloquea sino que agenda.

## ❓ Preguntas frecuentes

- **¿TypeScript reemplaza a JavaScript?** No: lo complementa. Al final se convierte en JavaScript para poder ejecutarse en el navegador o en Node.
- **¿Por qué JavaScript corre en el servidor?** Porque Node.js (2009) incrustó el motor V8 fuera del navegador, convirtiendo a JS en un lenguaje de propósito general con acceso al sistema de archivos y la red.
- **¿Por qué la herencia por prototipos y no por clases?** Es una decisión de diseño heredada de Self; las `class` de ES2015 son azúcar sintáctico que por dentro siguen usando prototipos.

## 🔗 Referencias

- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 2 (origen de JavaScript) y cap. 12 (soporte para OO y prototipos).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).

---

> [⏮️ Clase 020](../../parte-1-atlas-y-genealogia-de-los-lenguajes/020-familia-net-c-sharp-f-sharp-vb-net/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 022 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/022-familia-funcional-tipada-ml-haskell-ocaml-f-sharp-y-la-influencia-en-rust/README.md)
