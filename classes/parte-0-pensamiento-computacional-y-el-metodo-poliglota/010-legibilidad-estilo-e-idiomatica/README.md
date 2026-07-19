# Clase 010 — Legibilidad, estilo e idiomática

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Hay un hecho incómodo que todo programador acaba aprendiendo: **el código se lee muchas más veces de las que se escribe**. Lo escribes una vez y luego tú y otros lo leen decenas: para corregir un bug, para añadir una función, para entender qué hacía. Si eso es cierto, entonces optimizar el código para *quien lo lee* —y no para lucir ingenio al escribirlo— no es una cuestión de estética, sino de economía. El objetivo de hoy es entender que la legibilidad es mantenibilidad, y que cada lenguaje tiene una forma **idiomática** —la manera en que un experto lo escribiría— que hay que respetar en vez de imponer el estilo de otro.

Esta idea tiene una formulación célebre que conviene grabarse, la de Abelson y Sussman en el prefacio de SICP: los programas deben escribirse para que las personas los lean, y solo de forma incidental para que las máquinas los ejecuten. Si el lector primario es humano, el código es una forma de *comunicación*, y las reglas de la buena comunicación —claridad sobre astucia, intención explícita, convenciones compartidas— se aplican en pleno.

## 🧩 Situación

Un desarrollador que viene de C escribe en Python un bucle para imprimir una lista de nombres: `for i in range(len(nombres)): print(nombres[i])`. Funciona perfectamente, pasa todos los tests. Pero cualquier pythonista que lo lea sentirá una fricción: en Python eso se escribe `for nombre in nombres: print(nombre)`. La segunda versión no es más rápida ni más corta por casualidad; es que *comunica la intención directamente* —"para cada nombre, imprímelo"— sin el ruido del índice, la longitud y el acceso por posición, que son andamios que Python no necesita. La primera versión es una traducción mecánica del estilo de C; la segunda es Python idiomático. La diferencia no la nota el intérprete, la nota el humano que mantendrá el código dentro de seis meses, y ese humano probablemente serás tú.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar por qué la legibilidad importa más que la brevedad o el ingenio.
2. Reconocer código idiomático frente a una traducción mecánica desde otro lenguaje.
3. Aplicar nombres y estructura que comuniquen la intención.
4. Apoyarte en las guías de estilo de cada lenguaje como criterio objetivo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El código se lee más que se escribe | Optimizar para quien lo lee (incluido tu yo futuro) |
| 2 | Idiomática por lenguaje | Lo natural en Python no lo es en Go |
| 3 | Nombres que comunican | Un buen nombre ahorra un comentario |

## 📖 Definiciones y características

La **legibilidad** es la facilidad con que un ser humano entiende el código. Es una propiedad del lector, no del compilador: dos programas idénticos para la máquina pueden ser abismalmente distintos para la persona. La legibilidad prima sobre la astucia porque el código que nadie entiende no se puede mantener con seguridad, y el código que no se puede mantener es un pasivo, por brillante que sea. Hunt y Thomas condensan esto en su principio **ETC** —*Easier To Change*, más fácil de cambiar—: entre dos formas de escribir algo, la mejor es la que facilitará el cambio futuro, y el cambio futuro lo hace quien lee. La legibilidad es, en el fondo, una inversión en tu propio yo futuro y en tus colegas.

La **idiomática** es escribir como lo haría un experto del lenguaje, aprovechando sus convenciones y su paradigma. Cada lenguaje tiene su "acento": lo natural en Python (comprensiones de listas, iterar sobre el objeto) no lo es en Go (bucles explícitos, manejo de errores por valor), y lo natural en Go no lo es en Rust. Escribir idiomático no es memorizar trucos, es reconocer cuál es la forma que la *comunidad* de ese lenguaje considera clara. La clave —y aquí conecta con la clase 002— es que imponer el idioma de un lenguaje sobre otro produce código que funciona pero se lee como una traducción con diccionario: correcto y ajeno a la vez. El código idiomático, en cambio, se lee como lo escribiría un nativo.

El enemigo a evitar es el **código "listo"** (*clever*): ingenioso, compacto, que se siente inteligente al escribirlo y es un jeroglífico al leerlo. Encadenar cinco operaciones en una línea impenetrable no es una virtud; casi siempre es un error de criterio que sacrifica al lector para lucirse el autor. La herramienta más poderosa contra esto son los **nombres**: un buen nombre de variable o función comunica la intención y ahorra un comentario. `dias_hasta_vencimiento` no necesita explicación; `d` sí. McConnell y Martin dedican capítulos enteros a nombrar bien porque es, medida por medida, la decisión que más impacta en la legibilidad. Y hay una ayuda objetiva que quita subjetividad al asunto: casi todos los lenguajes tienen guías de estilo y formateadores automáticos —PEP 8 y `black` en Python, `gofmt` en Go, `rustfmt` en Rust— que codifican las convenciones de la comunidad. No tienes que inventar el estilo idiomático: en gran medida está escrito y automatizado.

## 🔎 Ejemplo

El mismo resultado, escrito de forma no idiomática y de forma idiomática en Python:

```text
No idiomático (Python con estilo de C):
    for i in range(len(nombres)):
        print(nombres[i])

Idiomático (Python):
    for nombre in nombres:
        print(nombre)
```

Ambos imprimen exactamente lo mismo. Pero el segundo comunica la intención sin ruido: no hay índice `i` que seguir, ni `len`, ni acceso por posición: solo "para cada nombre, imprímelo". Cada elemento que eliminas es una cosa menos que el lector tiene que sostener en la cabeza. La versión idiomática no es más corta por capricho: es más corta porque quita andamios que Python no necesita, y esa reducción *es* la mejora de legibilidad.

## ✍️ Práctica

Busca un fragmento de código que hayas escrito hace unos meses —tuyo, no de un libro— y hazte una prueba honesta: ¿lo entiendes en diez segundos, o tienes que descifrarlo? Si tardas, ahí tienes tu material. Reescríbelo para que un lector (o tú mismo dentro de otro medio año) lo entienda de inmediato: mejora los nombres para que digan qué contienen, sustituye cualquier truco compacto por una versión clara aunque ocupe una línea más, y si conoces la guía de estilo del lenguaje, aplícala. Compara las dos versiones. La sensación de "ahora se lee solo" es exactamente la calidad que persigue esta clase, y es la que agradecerá quien mantenga tu código.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo corregirlo |
|-------------------|--------------------------|
| Código compacto que nadie entiende (ni tú al mes) | Priorizaste brevedad e ingenio sobre claridad. Prefiere lo legible aunque ocupe una línea más |
| Todos tus lenguajes se parecen sospechosamente | Escribes todo con el mismo estilo. Aprende la idiomática de cada lenguaje del núcleo |
| Variables `x`, `d`, `tmp`, `data` por todas partes | Nombres que no comunican. Nómbralas por lo que significan; un buen nombre ahorra un comentario |
| Discusiones de estilo interminables en el equipo | No usas un criterio objetivo. Adopta la guía y el formateador del lenguaje (PEP 8, gofmt, rustfmt) |

## ❓ Preguntas frecuentes

**❓ ¿La idiomática no es puramente subjetiva?** Mucho menos de lo que parece. Cada comunidad tiene guías de estilo explícitas (PEP 8, la guía de efectividad de Go, las convenciones de Rust) y formateadores que las imponen automáticamente. Hay margen de gusto personal, pero el grueso de "qué es idiomático" está escrito y consensuado; no lo estás inventando tú solo.

**❓ ¿Y si el código legible es más lento que el astuto?** Legible por defecto; rápido solo donde midas que hace falta (clase 009). La inmensa mayoría del código no está en el cuello de botella, así que optimizar su velocidad a costa de la claridad es un mal negocio. Donde el rendimiento sí importe, aísla ese trozo, optimízalo y coméntalo bien: la excepción no anula la regla.

**❓ ¿Los comentarios no resuelven la ilegibilidad?** Solo en parte, y son un parche caro: los comentarios mienten con el tiempo, porque el código cambia y el comentario se queda. Un buen nombre o una estructura clara no se desactualizan igual. Prefiere código que se explique solo; reserva los comentarios para el *porqué*, no para el *qué*.

## 🔗 Referencias

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), Prefacio: escribir para que las personas lean — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), principio ETC y buenos nombres.
- R. C. Martin — *Clean Code* (Prentice Hall), capítulos sobre nombres y funciones.
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), sobre legibilidad y nombres.

---

> [⏮️ Clase 009](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/009-complejidad-y-eficiencia-intuicion-de-coste/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 011 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/011-anatomia-de-una-ficha-de-transferencia-y-como-estudiarla/README.md)
