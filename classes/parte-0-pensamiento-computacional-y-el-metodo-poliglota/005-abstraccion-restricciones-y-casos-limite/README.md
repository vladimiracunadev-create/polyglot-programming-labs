# Clase 005 — Abstracción, restricciones y casos límite

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Esta clase reúne tres herramientas del pensamiento que trabajan juntas. La **abstracción** consiste en quedarse con lo esencial de un problema e ignorar deliberadamente el resto. Las **restricciones** son las reglas que la solución debe cumplir para ser válida. Y los **casos límite** son las entradas extremas o inusuales —el vacío, el cero, el negativo, el máximo— donde los programas que "funcionan" se rompen. Dominar las tres es la diferencia entre un programa que pasa la demo y uno que sobrevive a la realidad.

Las tres ideas se sostienen mutuamente. Abstraes para poder razonar sin ahogarte en detalles; enumeras restricciones para saber qué cuenta como solución correcta; y buscas casos límite porque es justo en las fronteras de las restricciones donde la abstracción, si fue descuidada, se derrumba. SICP presenta la abstracción como el arma central contra la complejidad, y Cormen exige razonar sobre *toda* entrada válida, no solo sobre la cómoda. Hoy juntamos ambas exigencias.

## 🧩 Situación

Un programa suma precios y calcula el promedio de una lista de productos. En las demos funciona impecable: listas de cinco, diez, veinte elementos, todo correcto. Pasa a producción y, un martes cualquiera, se cae con una excepción. ¿La causa? Llegó una lista **vacía** —un pedido sin líneas— y al calcular el promedio dividió la suma (cero) entre la cantidad (cero). El caso límite "lista vacía" nunca se pensó porque nunca apareció en las pruebas cómodas. No fue un fallo de sintaxis ni de lógica compleja: fue una frontera que nadie miró. Esta clase existe para que esa frontera se mire *antes*, cuando cuesta un minuto, y no *después*, cuando cuesta una llamada a soporte a las tres de la mañana.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Abstraer un problema quedándote con lo relevante e ignorando el ruido.
2. Enumerar las restricciones explícitas e implícitas de un problema.
3. Identificar los casos límite antes de programar y decidir su comportamiento.
4. Convertir cada caso límite en una decisión de diseño explícita (y futuro caso de prueba).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Abstracción | Ignorar el ruido para razonar sobre lo esencial |
| 2 | Restricciones | Definen qué soluciones son válidas |
| 3 | Casos límite | El vacío, el cero, el negativo, el máximo: donde se rompen los programas |

## 📖 Definiciones y características

**Abstraer** es representar solo los aspectos relevantes de algo, descartando el resto. La metáfora clásica es la del mapa: un mapa es útil *porque* no es el territorio, porque omite los árboles individuales y conserva las carreteras. Un programa que calcula un promedio no necesita saber de dónde vienen los números —si son notas, precios o temperaturas—; le basta con que sean números. Esa omisión deliberada es lo que permite reutilizar la misma solución para problemas distintos. SICP construye todo su edificio sobre esta idea: las *barreras de abstracción* separan "qué hace" algo de "cómo lo hace", y esa separación es lo que hace manejables los sistemas grandes. Abstraer mal —quedarse sin datos que el problema sí necesita, o cargar con detalles que no— es una fuente silenciosa de errores.

Una **restricción** es una condición que la solución debe respetar: un rango de valores válidos, un formato de salida obligatorio, un límite de rendimiento, una regla del dominio. Las restricciones acotan el espacio de lo aceptable. Algunas son *explícitas* (el enunciado dice "el descuento está entre 0 y 1") y otras son *implícitas* (nadie lo dijo, pero una edad no puede ser negativa). Hacer explícitas las restricciones implícitas es medio trabajo de especificar bien un problema. Hunt y Thomas recomiendan expresar estas condiciones como *aserciones* dentro del código —afirmaciones de lo que siempre debe ser cierto— para que, si alguna vez se violan, el programa lo grite de inmediato en vez de continuar con datos corruptos.

Un **caso límite** es una entrada extrema o inusual: la colección vacía, el cero, el número negativo, el valor máximo representable, el único elemento, la cadena sin caracteres. La observación empírica que hay que grabarse es que **la mayoría de los bugs viven en los casos límite**, no en el caso típico. El caso feliz —una lista de números normales— casi siempre funciona a la primera; es el vacío el que divide entre cero, el máximo el que desborda, el negativo el que rompe una suposición tácita. Por eso los casos límite no son un añadido opcional: son la *semilla de los tests*. Cada caso límite que identificas hoy debería convertirse en una entrada de `casos.json` mañana. Cormen refuerza esto al exigir que un algoritmo sea correcto para *toda* entrada válida: si tu argumento de corrección solo cubre las entradas cómodas, no has demostrado nada sobre las incómodas, que son precisamente las que fallarán.

## 🔎 Ejemplo

Apliquemos las tres herramientas al problema "promedio de una lista de números":

```text
Problema: promedio de una lista de números reales

Abstracción:  solo importan los números y cuántos son;
              no importa de dónde vienen ni qué representan.

Restricciones: - la entrada es una lista de reales
               - el resultado es un real
               - (implícita) el promedio de una lista no vacía
                 está entre el mínimo y el máximo de la lista

Casos límite:
  - lista vacía        ⇒ ¿0.0? ¿error? ¡hay que DECIDIRLO y escribirlo!
  - un solo elemento   ⇒ el promedio es ese elemento
  - todos iguales      ⇒ el promedio es ese valor
  - números enormes    ⇒ ¿la suma desborda antes de dividir?
```

La restricción implícita —"el promedio está entre el mínimo y el máximo"— es además un regalo: te da una forma barata de detectar errores. Si tu programa devuelve un promedio mayor que el mayor de los números, algo está mal, y lo sabes sin comparar contra la respuesta correcta. Y el caso límite "lista vacía" ya no te va a sorprender en producción, porque lo decidiste aquí, con la cabeza fría.

## ✍️ Práctica

Para el problema "buscar el mayor de una lista", haz tres cosas. Primero, abstrae: ¿qué es lo único que importa de los elementos para poder compararlos? Segundo, enumera al menos tres casos límite (lista vacía, un solo elemento, todos iguales, negativos...). Tercero, y esto es lo esencial, **decide y escribe** qué hace el programa en cada caso límite: ¿qué devuelve ante una lista vacía, un error o un valor centinela? No hay una única respuesta correcta, pero sí hay una regla: la decisión debe ser *explícita*. Un programa que "no sabe" qué hacer con la lista vacía es un bug esperando su turno.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo corregirlo |
|-------------------|--------------------------|
| Funciona en la demo, se cae en producción | Probaste solo el caso feliz. Escribe los casos límite en `casos.json` desde el inicio |
| `ZeroDivisionError` / división entre cero | El caso "colección vacía" no se contempló. Decídelo explícitamente antes de dividir |
| La abstracción deja fuera un dato necesario | Abstrajiste de más. Revisa que conserve todo lo que el problema realmente usa |
| El código arrastra detalles irrelevantes | Abstrajiste de menos. Quédate con lo esencial, descarta el ruido |
| Una entrada "imposible" corrompe el resultado | Restricción implícita no verificada. Exprésala como aserción y comprueba en la frontera |

## ❓ Preguntas frecuentes

**❓ ¿Los casos límite son lo mismo que los tests?** No exactamente: son la *semilla* de los tests. Cada caso límite que identificas debería convertirse en un caso de prueba concreto. Pensar los límites primero y probarlos después es el flujo natural que culmina en el `casos.json` de la clase 012.

**❓ ¿Cómo sé si abstraje bien?** Con una prueba simple: si puedes resolver el problema entero usando solo tu abstracción, sin volver a mirar los detalles que descartaste, abstrajiste bien. Si a mitad de camino necesitas recuperar un detalle que habías tirado, te pasaste; si el código se llena de datos que nunca usas, te quedaste corto.

**❓ ¿Vale la pena enumerar restricciones "obvias" como que una edad no es negativa?** Sí, sobre todo las obvias, porque son las que nadie escribe y todos asumen de forma distinta. Convertirlas en aserciones explícitas cuesta una línea y atrapa datos corruptos en el punto exacto donde entran, en vez de dejar que contaminen medio programa.

## 🔗 Referencias

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), barreras de abstracción — [gratis online](https://mitpress.mit.edu/9780262510875/).
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), corrección sobre toda entrada válida.
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre aserciones y diseño por contrato.
- G. Polya — *How to Solve It* (Princeton University Press), examinar casos especiales.

---

> [⏮️ Clase 004](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/004-descomposicion-y-reconocimiento-de-patrones/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 006 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/006-algoritmos-correccion-y-terminacion/README.md)
