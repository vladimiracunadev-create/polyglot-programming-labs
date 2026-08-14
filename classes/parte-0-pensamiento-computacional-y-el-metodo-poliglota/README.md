# Parte 0 — Pensamiento computacional y el método políglota

> [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 1](../parte-1-atlas-y-genealogia-de-los-lenguajes/README.md)

**14 clases** · rango 001–014 · clases de **método** · nivel fundamentos · **~21 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **Aprender a pensar el problema antes de elegir con qué escribirlo.**

---

## 🧭 De qué trata esta parte

Esta parte existe porque la mayor parte de lo que hace bueno a un programador **no está dentro de ningún lenguaje**. Modelar un problema, descomponerlo, escribir un algoritmo que se sepa correcto y estimar lo que costará son habilidades que sobreviven a cualquier cambio de tecnología, y son exactamente las que un curso «de Python» o «de Java» da por supuestas mientras enseña sintaxis.

Aquí no se escribe código en ningún lenguaje del núcleo. Se escribe **pseudocódigo neutral**, se traza a mano y se discute qué significa que dos programas hagan «lo mismo». Ese vocabulario es el que hace posible que a partir de la Parte 3 se pongan diez implementaciones lado a lado y la comparación enseñe algo en vez de ser un desfile de sintaxis.

La parte cierra con el método del propio curso —la ficha de transferencia, el `casos.json`, el verificador— para que sepas exactamente qué estás leyendo en cada clase posterior y qué garantía tiene cada afirmación.

## 🎒 Qué necesitas traer

Nada. Es el punto de entrada del programa y no requiere haber programado antes, aunque haber peleado con algún lenguaje hace que varias clases resuenen más.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Modelar un problema como entradas, proceso, salidas, reglas y restricciones.
2. Escribir un algoritmo en pseudocódigo neutral y trazarlo a mano sobre un caso concreto.
3. Argumentar corrección y terminación en lugar de confiar en que «parece funcionar».
4. Clasificar cualquier diferencia entre dos lenguajes como sintáctica, semántica o paradigmática.
5. Estimar el orden de coste de un algoritmo antes de escribirlo.
6. Leer una clase de código del curso sacándole todo el partido, y saber qué verifica la máquina.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 La tesis y la brújula · clases 001–002

Las dos clases que fijan de qué va el curso y con qué criterio se compara. Todo lo demás las usa.

- **[001 · Qué es programar y por qué comparar lenguajes: la tesis políglota](001-que-es-programar-y-por-que-comparar-lenguajes-la-tesis-poliglota/README.md)** — Separa programar de «saber la sintaxis de un lenguaje»: programar es expresar la solución de un problema con precisión suficiente para que una máquina, que no entiende nada, la ejecute sin ambigüedad. De ahí sale la tesis del curso: si lo esencial es el problema y el algoritmo, el lenguaje es la forma — y compararlo con otros es lo que revela cuál es cuál.
- **[002 · Las tres clases de diferencia: sintáctica, semántica y paradigmática](002-las-tres-clases-de-diferencia-sintactica-semantica-y-paradigmatica/README.md)** — Instala la brújula que se usa en las 175 clases restantes: toda diferencia entre dos lenguajes es **sintáctica** (cómo se escribe), **semántica** (qué ocurre al ejecutarse) o **paradigmática** (qué considera una pieza legítima de solución). Confundirlas es la causa número uno de las discusiones estériles sobre lenguajes.

### 🔹 Modelar el problema · clases 003–006

Antes del algoritmo está el modelo: qué entra, qué sale, qué se descarta y qué casos lo rompen.

- **[003 · Problema, contexto, entradas, proceso y salidas](003-problema-contexto-entradas-proceso-y-salidas/README.md)** — Modelar antes de teclear: decidir qué datos entran, qué resultado sale, bajo qué reglas ocurre la transformación y en qué contexto tiene sentido. Ese modelo es exactamente lo que después se escribe como `casos.json` y lo que diez implementaciones deben satisfacer por igual.
- **[004 · Descomposición y reconocimiento de patrones](004-descomposicion-y-reconocimiento-de-patrones/README.md)** — Partir un problema grande en subproblemas manejables y reconocer cuándo un subproblema ya lo resolviste antes con otra forma. Es la habilidad que separa a quien programa cosas pequeñas de quien construye sistemas, y la que evita reescribir tres veces la misma solución sin notarlo.
- **[005 · Abstracción, restricciones y casos límite](005-abstraccion-restricciones-y-casos-limite/README.md)** — Tres herramientas que trabajan juntas: **abstraer** (quedarse con lo esencial y descartar el resto), **restringir** (declarar las reglas que la solución debe cumplir) y buscar deliberadamente los **casos límite** —el vacío, el cero, el negativo, el máximo— que es donde los programas se rompen de verdad.
- **[006 · Algoritmos: corrección y terminación](006-algoritmos-correccion-y-terminacion/README.md)** — Un algoritmo no vale por «parece que funciona»: necesita **corrección** (produce el resultado esperado para toda entrada válida) y **terminación** (garantiza que acaba). Aquí aprendes a argumentar ambas con invariantes y variantes en lugar de con intuición.

### 🔹 Del papel al algoritmo · clases 007–010

Escribirlo sin lenguaje, comprobarlo a mano, estimar su coste y hacerlo legible.

- **[007 · Pseudocódigo neutral: escribir sin lenguaje](007-pseudocodigo-neutral-escribir-sin-lenguaje/README.md)** — El **pseudocódigo neutral** es la notación que hace posible todo el curso: describe el algoritmo sin comprometerse con ningún lenguaje real, de modo que las diez implementaciones sean traducciones de un mismo texto y no diez invenciones distintas.
- **[008 · Trazado manual y ejecución simbólica](008-trazado-manual-y-ejecucion-simbolica/README.md)** — Ejecutar el algoritmo con papel y lápiz, siguiendo el valor de cada variable paso a paso. Es la habilidad de depuración más fundamental que existe: la única que funciona antes de tener código, y la que convierte un bug en una hipótesis comprobable.
- **[009 · Complejidad y eficiencia: intuición de coste](009-complejidad-y-eficiencia-intuicion-de-coste/README.md)** — Pasar de «¿funciona?» a «¿cuánto **cuesta** cuando la entrada crece?». Intuición de órdenes de magnitud —constante, logarítmico, lineal, cuadrático— suficiente para elegir estructura de datos antes de medir, sin necesidad de formalismo pesado.
- **[010 · Legibilidad, estilo e idiomática](010-legibilidad-estilo-e-idiomatica/README.md)** — El código se lee muchas más veces de las que se escribe. Aquí se distingue **estilo** (convención de forma, automatizable) de **idiomática** (la manera natural de decir algo en ese lenguaje concreto), que es justo lo que hace que el mismo algoritmo se vea distinto en Python y en Go sin que ninguno esté peor escrito.

### 🔹 El método del curso en la práctica · clases 011–014

Cómo está hecha una clase de código, cómo se verifica y cómo se lee un lenguaje ajeno.

- **[011 · Anatomía de una ficha de transferencia y cómo estudiarla](011-anatomia-de-una-ficha-de-transferencia-y-como-estudiarla/README.md)** — El manual de instrucciones del curso: cómo está montada una clase de código —modelo, pseudocódigo, diez implementaciones, comparación, `casos.json`, primos y reto— y en qué orden conviene leerla para que el contraste enseñe en vez de abrumar.
- **[012 · casos.json y el verificador de equivalencia](012-casos-json-y-el-verificador-de-equivalencia/README.md)** — La afirmación «estas diez implementaciones resuelven el mismo problema» es fácil de escribir y facilísima de equivocar. Aquí ves el mecanismo que la comprueba por máquina: mismo stdin, misma salida esperada, ejecutado en CI para los diez lenguajes.
- **[013 · El concepto en la familia: leer un lenguaje que no conoces](013-el-concepto-en-la-familia-leer-un-lenguaje-que-no-conoces/README.md)** — La habilidad más rentable del enfoque políglota: **leer con provecho código de un lenguaje que nunca estudiaste**. No escribirlo bien ni dominarlo — leerlo: entender qué hace y seguir su lógica apoyándote en la familia a la que pertenece.
- **[014 · Cómo elegir lenguaje para un problema](014-como-elegir-lenguaje-para-un-problema/README.md)** — Cierra la parte con la pregunta que solo ahora se puede responder: dado un problema y su contexto —equipo, plataforma, ecosistema, plazo, riesgo—, qué lenguaje conviene y con qué argumentos se defiende esa elección ante otros.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «Aprender a programar es aprender un lenguaje.» | El lenguaje es la última decisión, no la primera: sin modelo ni algoritmo, la sintaxis no te lleva a ninguna parte. |
| «Los lenguajes son todos iguales, solo cambia la sintaxis.» | Falso en el eje semántico y en el paradigmático. Lo que cambia de verdad es qué se puede expresar y qué garantiza el lenguaje. |
| «El pseudocódigo es una pérdida de tiempo.» | Es la única forma de escribir una vez lo que después se traduce diez veces — y de detectar que el problema estaba mal planteado antes de codificarlo. |

## 🧪 Cómo estudiar esta parte

1. **Lee la clase entera antes de opinar.** Son clases de razonamiento: el valor está en el argumento completo, no en la definición suelta.
2. **Contesta la pregunta que abre cada clase** con tus palabras antes de seguir a la siguiente. Si no puedes, vuelve al párrafo del objetivo.
3. **Aplícalo a un problema tuyo.** Estas clases no se verifican con una máquina; se verifican usándolas sobre código real que ya escribiste.
4. **Anota los términos nuevos.** Aparecen otra vez, con código delante, a partir de la Parte 3 — y están todos en el [glosario](../../glosario/README.md).

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- G. Polya — *How to Solve It* (Princeton University Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).

## 🔗 Qué abre esta parte

Con el método fijado, la Parte 1 lo aplica al mapa completo de los lenguajes: de dónde viene cada uno y a qué familia pertenece.

---

> [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 1](../parte-1-atlas-y-genealogia-de-los-lenguajes/README.md)
