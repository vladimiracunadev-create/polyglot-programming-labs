# Clase 006 — Algoritmos: corrección y terminación

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Un algoritmo es una receta: una secuencia finita y precisa de pasos que resuelve un problema. Pero no cualquier receta sirve. Para confiar en un algoritmo necesita cumplir dos propiedades que hoy vamos a hacer explícitas: **corrección** (produce el resultado correcto para *toda* entrada válida, no solo para las que probaste) y **terminación** (siempre acaba, nunca se queda dando vueltas para siempre). Un algoritmo incorrecto da respuestas malas; uno que no termina no da ninguna. Ambos son inútiles, y ambos fallos se pueden razonar *antes* de ejecutar.

Cormen construye *Introduction to Algorithms* sobre exactamente estas dos exigencias, y presenta una herramienta para razonarlas con rigor pero sin fórmulas intimidantes: el **invariante de bucle**. El objetivo de hoy no es demostrar teoremas, sino que adquieras el reflejo de preguntarte, ante cualquier bucle que escribas, dos cosas: "¿por qué esto da la respuesta correcta?" y "¿por qué esto acaba?". Quien se hace esas preguntas escribe muchos menos bugs que quien confía en que "parece que funciona".

## 🧩 Situación

Un algoritmo de búsqueda binaria es una maravilla de eficiencia: encuentra un elemento en un millón de datos ordenados en unas veinte comparaciones. Un programador lo escribe, funciona en sus pruebas y lo despliega. Semanas después, con cierta entrada, el programa se cuelga: consume 100 % de CPU y no responde. La causa es una sola línea: escribió `fin = medio` donde debía escribir `fin = medio - 1`. Con ese cambio, en un caso concreto el rango de búsqueda deja de encogerse —`medio` vuelve a caer en el mismo sitio vuelta tras vuelta— y el bucle nunca alcanza su condición de salida. No hay error, no hay excepción: hay un bucle inmortal. La terminación no es un detalle académico; es la diferencia entre un servicio que responde y uno que hay que reiniciar a mano.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir qué es un algoritmo y sus dos propiedades esenciales.
2. Argumentar de forma informal por qué un algoritmo es correcto, usando un invariante.
3. Detectar por qué un bucle podría no terminar y cómo garantizar que lo haga.
4. Distinguir corrección de terminación como dos preguntas separadas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Qué es un algoritmo | Una receta precisa y finita de pasos |
| 2 | Corrección | Da la respuesta correcta para toda entrada válida |
| 3 | Terminación | Siempre acaba; el bucle avanza hacia su fin |
| 4 | Invariante y variante | Herramientas para razonar sobre bucles |

## 📖 Definiciones y características

Un **algoritmo** es una secuencia finita y precisa de pasos que, partiendo de una entrada válida, produce la salida especificada. Las dos palabras que importan son *finita* (tiene un número acotado de pasos, no una lista infinita) y *precisa* (cada paso es inequívoco, sin lugar para la interpretación). Una receta de cocina que dijera "añade sal al gusto" no sería un algoritmo: "al gusto" es ambiguo. La precisión es lo que permite que una máquina, que no interpreta, lo ejecute.

La **corrección** es la propiedad de producir la salida correcta para *toda* entrada válida. La palabra clave es *toda*: no basta con que funcione en los casos que probaste. La corrección se *argumenta*, no se supone. Y la herramienta para argumentarla sobre un bucle es el **invariante de bucle**: una condición que es verdadera antes de empezar el bucle y sigue siendo verdadera al final de cada vuelta. Cormen lo usa así: si demuestras que el invariante se cumple al inicio, que cada iteración lo preserva, y que al terminar el invariante implica lo que querías, entonces has probado que el bucle es correcto. Es un razonamiento por inducción disfrazado de sentido común. Por ejemplo, en un bucle que busca el máximo, el invariante "la variable `mayor` contiene el máximo de todos los elementos vistos hasta ahora" lo dice todo: si es cierto en cada vuelta, al ver el último elemento `mayor` contiene el máximo de todos.

La **terminación** es la propiedad de acabar en un número finito de pasos. La herramienta aquí es la idea de **variante** (o *función de cota*): algo que decrece en cada iteración hacia un límite inferior. Si en cada vuelta una cantidad medible se hace estrictamente más pequeña y no puede bajar de cierto suelo, el bucle no puede repetirse para siempre. En la búsqueda binaria, ese "algo" es el tamaño del rango de búsqueda: si en cada vuelta se reduce al menos a la mitad, en un número finito de pasos llega a cero y el bucle para. El bug del `fin = medio` rompe exactamente esto: el rango deja de decrecer, el variante se estanca, la terminación se pierde. Corrección y terminación son preguntas *independientes*: un algoritmo puede terminar siempre y dar respuestas erróneas, o dar respuestas correctas cuando termina pero no terminar nunca. Hay que verificar las dos.

## 🔎 Ejemplo

Un algoritmo para hallar el mayor de una lista, con su corrección y su terminación razonadas al lado:

```text
ALGORITMO mayor(lista):        # precondición: lista no vacía
    mayor <- lista[0]
    PARA cada x en lista[1..]:
        SI x > mayor:
            mayor <- x
    DEVOLVER mayor

Invariante (corrección):
    Antes de mirar cada x, 'mayor' es el máximo de los elementos
    ya vistos. Al terminar se han visto todos ⇒ 'mayor' es el máximo total.

Variante (terminación):
    Quedan por visitar (n - 1), luego (n - 2), ... hasta 0.
    Esa cantidad decrece en cada vuelta y no baja de 0 ⇒ el bucle acaba.
```

Nota cómo ambos argumentos son informales pero completos: no hay álgebra, solo una afirmación clara de por qué el resultado es correcto (el invariante) y por qué el proceso acaba (algo finito decrece). Ese es exactamente el nivel de rigor que este curso te pide: suficiente para convencer a un colega escéptico, sin necesidad de una demostración formal.

## ✍️ Práctica

Escribe en pseudocódigo un algoritmo que cuente cuántos números pares hay en una lista. Luego, en una frase cada uno, argumenta: (1) su invariante de corrección —¿qué es siempre cierto sobre tu contador en cada vuelta?— y (2) su variante de terminación —¿qué decrece hacia un límite y por qué garantiza que el bucle acaba?—. Después, como ejercicio de contraste, cambia deliberadamente el algoritmo para que *no* termine (por ejemplo, olvidando avanzar el índice) e identifica exactamente qué propiedad rompiste. Ver el fallo a propósito enseña a evitarlo por accidente.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo corregirlo |
|-------------------|--------------------------|
| El programa se cuelga, CPU al 100 % | Bucle que no decrece. Asegura que algo cambia en cada vuelta acercándose al límite de salida |
| Índice o condición que nunca avanza | Variante estancada (p. ej. `fin = medio` en vez de `medio - 1`). Revisa que el rango se encoja de verdad |
| "Parece correcto" pero falla en un caso | Corrección asumida, no argumentada. Busca el invariante que debería cumplirse y comprueba si se rompe |
| Funciona con listas normales, falla con la vacía | Precondición no verificada (`lista[0]` sobre lista vacía). Trata el caso límite explícitamente |

## ❓ Preguntas frecuentes

**❓ ¿Tengo que demostrar formalmente todos mis algoritmos?** No en este curso. Basta con un argumento informal pero claro: una frase que diga por qué el resultado es correcto (el invariante) y otra que diga por qué el proceso acaba (algo finito decrece). Lo importante es adquirir el *reflejo* de hacerte esas dos preguntas, no llenar páginas de lógica formal.

**❓ ¿Un programa que no termina es siempre un bug?** Casi siempre, sí. La excepción son los programas diseñados para correr en un bucle indefinido *a propósito*: un servidor web, un sistema operativo, el bucle de eventos de una interfaz. Esos "no terminan" porque su trabajo es esperar y responder sin fin. La diferencia es que su no-terminación es deliberada y controlada, no accidental.

**❓ ¿Corrección y terminación se pueden verificar por separado?** Sí, y conviene hacerlo. Son propiedades independientes: un algoritmo puede terminar siempre pero calcular mal, o calcular bien cuando termina pero colgarse en ciertos casos. Verifica las dos como preguntas distintas; responder una no responde la otra.

## 🔗 Referencias

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), cap. 2: invariantes de bucle.
- G. Polya — *How to Solve It* (Princeton University Press), fase "Looking Back": verificar el resultado.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), procesos iterativos y recursivos — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre aserciones para verificar supuestos.

---

> [⏮️ Clase 005](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/005-abstraccion-restricciones-y-casos-limite/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 007 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/007-pseudocodigo-neutral-escribir-sin-lenguaje/README.md)
