# 🔗 Prolog — 1972

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Prolog es el lenguaje que más lejos lleva la idea declarativa: **no se escriben instrucciones, se
escriben hechos y reglas**, y el sistema busca por sí mismo las respuestas que se derivan de ellos.
Escribir Prolog exige desaprender casi todo lo demás — y por eso enseña tanto.

> **🎯 Por qué está en este programa**
>
> Prolog es un **primo de la familia lógica y declarativa** ([Atlas](README.md#logica-declarativa)),
> cuyo representante en el núcleo es [SQL](sql.md).
>
> Aporta al programa el paradigma lógico en su forma pura
> ([clase 119](../classes/parte-7-paradigmas/118-logico-reglas-hechos-y-unificacion-prolog/README.md)):
> **unificación** en lugar de asignación, **vuelta atrás** en lugar de bucles, y **una relación que se
> puede recorrer en las dos direcciones**. Es el contraste más fuerte de todo el Atlas frente a los
> lenguajes imperativos.

| | |
|---|---|
| **Año** | 1972; **ISO Prolog** en 1995 |
| **Autoría** | **Alain Colmerauer** y Philippe Roussel, Marsella; teoría de **Robert Kowalski** |
| **Familia** | Lógica; basado en la **resolución SLD** sobre cláusulas de Horn |
| **Paradigma** | **Lógico declarativo** |
| **Tipado** | **Dinámico y sin tipos declarados**; los términos son la única estructura |
| **Memoria** | Recolección de basura, con pila de puntos de elección |
| **Ejecución** | Máquina abstracta de Warren (WAM); compilado o interpretado |
| **Estado** | 🟢 **Vivo en nichos**: IA simbólica, procesamiento de lenguaje, verificación |

---

## 📜 Historia

En **1972**, **Alain Colmerauer** trabajaba en Marsella en **procesamiento de lenguaje natural** —
concretamente, en responder preguntas en francés—. Necesitaba una forma de expresar reglas
gramaticales y deducir consecuencias, y con la base teórica de **Robert Kowalski** —que había
demostrado que un subconjunto de la lógica de primer orden, las **cláusulas de Horn**, se puede
ejecutar— nació **Prolog**: *programmation en logique*.

La idea de Kowalski se resume en una ecuación famosa:

> **Algoritmo = Lógica + Control.**

Es decir: **lo que se quiere calcular** y **cómo se busca** son cosas separables. El programa
Prolog expresa la lógica; el motor aporta el control.

**David H. D. Warren** hizo Prolog práctico en 1983 con la **WAM**, una máquina abstracta que se
convirtió en el objetivo de compilación estándar — y cuyo papel es el mismo que la JVM tendría
después (clase 125).

El momento de máxima atención llegó con el **Proyecto de Quinta Generación japonés (1982-1992)**, que
apostó mil millones de dólares por construir ordenadores basados en lógica y en paralelismo. **No
alcanzó sus objetivos**, y su fracaso —junto con el del auge de los sistemas expertos— arrastró la
reputación de Prolog durante décadas.

Y hoy sus ideas están más vivas que su nombre: **Datalog** en bases de datos, **la programación por
restricciones** en logística e industria, y **la unificación** en los sistemas de tipos de casi todos
los lenguajes con inferencia.

## 🏭 Dónde vive hoy

- **Procesamiento de lenguaje natural** y sistemas de reglas, sobre todo donde hay que explicar por
  qué se llegó a una conclusión.
- **Programación por restricciones**: SWI-Prolog y SICStus con **CLP(FD)** resuelven horarios,
  asignación de recursos, rutas y planificación industrial — es su uso más rentable hoy.
- **Verificación y análisis de programas**, con motores de deducción.
- **IBM Watson** usó Prolog para el análisis sintáctico en el sistema que ganó *Jeopardy!*.
- **Enseñanza**: sigue siendo la forma estándar de enseñar programación lógica.

## 🧠 Lo que enseña: unificación y relaciones reversibles

**La unificación no es asignación** (clase 119):

```prolog
X = 3.          % ← liga X con 3, o comprueba que ya vale 3
persona(ana, 30).
persona(luis, 25).

?- persona(Quien, 30).      % ← ¿quién tiene 30 años?
Quien = ana.
```

**El mismo `=` sirve para ligar y para comprobar**, y **una variable solo se liga una vez** — es lo
que la clase 041 llamaría una constante, no una variable.

Y de ahí sale la propiedad más asombrosa del paradigma: **una relación se puede recorrer en cualquier
dirección**.

```prolog
concat([], L, L).
concat([H|T], L, [H|R]) :- concat(T, L, R).

?- concat([1,2], [3], X).      % X = [1,2,3]        ← concatenar
?- concat(X, [3], [1,2,3]).     % X = [1,2]          ← ¡DESCONCATENAR!
?- concat(X, Y, [1,2,3]).        % TODAS las formas de partir la lista
```

**Se define una vez y se usa de tres maneras.** En un lenguaje imperativo habría que escribir tres
funciones. **Esa reversibilidad es lo que ningún otro paradigma da**, y es la razón de que Prolog siga
enseñándose.

Y la **vuelta atrás** es el mecanismo de control:

```prolog
?- persona(X, E), E > 26.       % prueba ana → sí; prueba luis → no; devuelve ana
```

**El motor prueba alternativas y deshace lo que no funciona**, automáticamente. Es búsqueda con
retroceso, integrada en el lenguaje.

> **Y la honestidad exige decir dónde se rompe la abstracción**: **el orden de las cláusulas importa**,
> y un programa lógicamente correcto puede entrar en un bucle infinito según cómo esté escrito. Por eso
> existe **el corte (`!`)**, que poda la búsqueda — y con él vuelve el control imperativo por la puerta
> de atrás. **La ecuación de Kowalski es un ideal; la práctica es más sucia**, y saberlo forma parte
> de entender el paradigma.

## 🔄 Lo que se ha modernizado

- **CLP(FD)** y la programación por restricciones: en lugar de generar y probar, **se propagan
  restricciones** y se poda el espacio de búsqueda. Es lo que hace útil a Prolog en optimización real.
- **SWI-Prolog** como implementación moderna: servidor web integrado, JSON, interfaz con Python
  (`janus`), depurador gráfico y gestor de paquetes (clase 143).
- **Tabulación (*tabling*)**: memorización de subobjetivos que **evita bucles infinitos** y acerca
  Prolog a [Datalog](datalog.md) en sus garantías.
- **Scryer Prolog** y **Trealla**: implementaciones nuevas escritas en [Rust](rust.md) y en C,
  centradas en el estándar y en el rigor.
- **Y el renacimiento por la IA**: los sistemas neurosimbólicos combinan modelos de lenguaje con
  motores lógicos, precisamente porque **la deducción es explicable y el modelo no**.

## ⚙️ Cómo se ejecuta hoy

```bash
swipl -g main -t halt main.pl < entrada.txt     # ejecutar un guion
swipl                                            # consola interactiva: el uso natural

?- [main].          % cargar
?- trace.            % ← depurador de resolución, paso a paso (clase 141)
```

## 🧪 El programa de la clase 041 en Prolog

Es la versión que aparece en el
[`primos.md` de la clase 041](../classes/parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/primos.md).

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [Precio, Cantidad, Descuento]),
    Total is Precio * Cantidad * (1 - Descuento),
    format("Total: ~2f~n", [Total]).
```

**Lo que hay que ver.**

- **`Total is ...` NO es una asignación.** `is` evalúa la expresión aritmética y **unifica** el
  resultado con `Total`. Si `Total` ya estuviera ligado, **esto sería una comprobación**, no una
  escritura (clase 041).
- **Las mayúsculas son variables y las minúsculas son átomos.** `Precio` es una variable; `main` es
  un átomo. Es al revés de la convención de casi todos los lenguajes.
- **La coma es una conjunción lógica**, no un separador de sentencias: `A, B` significa "demuestra A
  **y** demuestra B", y si B falla, **se vuelve atrás sobre A** para probar otra alternativa.
- **`maplist` con `[S,N]>>...`** es una lambda (biblioteca `yall`), y aplica la relación
  `number_string` a cada elemento — la misma idea que `map` en el resto de las fichas (clase 115).
- **Y `main` no es una función: es un predicado que se demuestra.** Si algo falla, el predicado falla
  y el programa termina sin salida — que es la semántica lógica, no la imperativa.

## 📚 Fuentes y bibliografía

- [The Power of Prolog](https://www.metalevel.at/prolog) — **Markus Triska**; libre en línea y de lo
  mejor escrito sobre el lenguaje, con mucha atención a hacerlo bien y no solo a que funcione.
- [Learn Prolog Now!](http://www.learnprolognow.org/) — libre; la introducción académica estándar.
- [Manual de SWI-Prolog](https://www.swi-prolog.org/pldoc/doc_for?object=manual) — la implementación
  más completa.
- **Leon Sterling, Ehud Shapiro**, *The Art of Prolog*, MIT Press — el clásico.
- **Robert Kowalski**, *Algorithm = Logic + Control* (1979) — el artículo que fundamenta el paradigma;
  corto y sigue siendo lúcido.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Datalog](datalog.md) · [SQL](sql.md) · [Erlang](erlang.md) ·
[Common Lisp](common-lisp.md)
