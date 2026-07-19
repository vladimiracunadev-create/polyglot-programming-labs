# Clase 030 — Compilado vs. interpretado vs. transpilado vs. bytecode/VM

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

«¿Es compilado o interpretado?» es una de las primeras preguntas que se hacen sobre un lenguaje, y casi siempre está mal planteada, porque la realidad tiene cuatro respuestas, no dos. Un lenguaje puede compilarse a código máquina (C, Rust, Go), interpretarse recorriendo el fuente (los orígenes de Python y PHP), transpilarse a otro lenguaje de alto nivel (TypeScript a JavaScript) o compilarse a *bytecode* que ejecuta una máquina virtual (Java sobre la JVM, C# sobre el CLR). El objetivo de esta clase es que sepas ubicar cada lenguaje del núcleo en su modelo de ejecución y, sobre todo, que entiendas qué consecuencias prácticas se derivan de esa ubicación: cuándo aparecen los errores, cuánto tarda en arrancar, qué rendimiento esperar y qué necesitas instalar en la máquina destino.

No es una taxonomía académica. El modelo de ejecución es la variable oculta detrás de decisiones de ingeniería reales: por qué un microservicio Java «tarda en calentar», por qué un script de Python se despliega copiando archivos pero un binario de Go se despliega copiando *un* archivo, por qué un error de tipos en C te detiene antes de correr y el mismo error en Python te explota en producción.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Clasificar cada lenguaje del núcleo por su modelo de ejecución dominante.
2. Predecir en qué momento (compilación o ejecución) aparecerá un error según el modelo.
3. Explicar qué es una máquina virtual, qué es un JIT y qué es transpilar.
4. Relacionar el modelo con el arranque, el rendimiento y lo que hay que instalar para ejecutar.

## 🧩 Situación

Escribes `total = cantida * precio` (con `cantida` mal escrito) en dos proyectos. En el proyecto en C, `gcc` se niega a compilar: `error: 'cantida' undeclared`. El programa no llega a existir, y por tanto no puede fallar en el cliente. En el proyecto en Python, el programa arranca, procesa cientos de líneas correctas y muere con `NameError: name 'cantida' is not defined` justo cuando la ejecución alcanza esa línea —quizá minutos después, quizá en producción con datos reales. El mismo error tipográfico se manifiesta en momentos radicalmente distintos, y la única causa es el modelo de ejecución. Entenderlo cambia cómo pruebas: en lenguajes interpretados necesitas ejecutar *cada* camino para que los errores afloren; en compilados, el compilador barre muchos antes de arrancar.

## 📖 Cuatro caminos al mismo destino

**Compilación a código máquina.** El compilador traduce todo el programa a instrucciones nativas de la CPU antes de ejecutar nada. El resultado es un binario que la máquina corre directamente, sin intermediarios. Es el modelo de máximo rendimiento y de errores tempranos: el análisis completo del programa ocurre en compilación, así que muchos fallos (tipos incompatibles, variables sin declarar) se atrapan ahí. El precio es un ciclo editar-compilar-ejecutar más lento y un binario atado a una arquitectura y sistema operativo concretos. C, Rust y Go viven aquí.

**Interpretación.** Un intérprete lee el fuente y lo ejecuta sobre la marcha, sin producir un artefacto traducido por adelantado. La ventaja es la inmediatez —cambias una línea y la corres— que hace de estos lenguajes herramientas magníficas para explorar e iterar, en el espíritu de las herramientas ágiles que celebra *The Unix Programming Environment*. La contrapartida es que los errores esperan agazapados hasta que la ejecución llega a la línea, y que se paga el coste de traducir en cada corrida. En la práctica «puro interpretado» casi no existe: Python y PHP compilan internamente a bytecode antes de ejecutarlo.

**Bytecode sobre máquina virtual.** El compilador no produce código de una CPU real, sino de una CPU *imaginaria y portátil*: la máquina virtual. Java compila a bytecode de la JVM y C# a IL del CLR. Ese bytecode corre igual en cualquier sistema que tenga la VM instalada —el famoso «compila una vez, ejecuta en cualquier parte»— y la VM suele incluir un **JIT** (*Just-In-Time*) que compila las partes calientes a código máquina durante la ejecución. De ahí el «calentamiento»: el programa arranca interpretando bytecode y acelera a medida que el JIT optimiza. Portabilidad y rendimiento alto en estado estacionario, a cambio de un arranque más lento y de necesitar la VM en el destino.

**Transpilación.** Compilar de un lenguaje de alto nivel a *otro* lenguaje de alto nivel. TypeScript no se ejecuta: se transpila a JavaScript y es JavaScript lo que corre. El objetivo no es acercarse a la máquina, sino aprovechar un runtime que ya existe (aquí, el motor JS del navegador o Node) añadiendo por encima características —el sistema de tipos— que desaparecen tras la transpilación. Es la razón por la que los tipos de TypeScript no cuestan nada en tiempo de ejecución: para cuando el código corre, ya no están.

## 🔬 Laboratorio guiado: ver cada modelo en acción

Comprueba tú mismo cuándo aparecen los errores. Con C, un símbolo inexistente detiene la compilación:

```bash
gcc programa.c -o programa      # si hay un typo: error de compilación, no genera binario
./programa                      # solo llegas aquí si compiló sin errores
```

Con Python, el mismo tipo de error espera a la ejecución:

```bash
python programa.py              # arranca y falla al ALCANZAR la línea con el error
python -m py_compile programa.py  # atrapa errores de SINTAXIS, pero no de nombres/tipos
```

Observa la portabilidad del bytecode de Java y su desensamblado:

```bash
javac Programa.java     # -> Programa.class (bytecode de la JVM, no de tu CPU)
java Programa           # la JVM ejecuta y el JIT optimiza lo que se repite
javap -c Programa       # ves las instrucciones de la máquina VIRTUAL
```

Mira la transpilación de TypeScript, donde los tipos se evaporan:

```bash
tsc programa.ts         # produce programa.js SIN anotaciones de tipo
node programa.js        # lo que realmente se ejecuta es JavaScript
tsx programa.ts         # atajo que transpila y ejecuta en un solo paso
```

Y contrasta el rendimiento del mismo cálculo entre un compilado y un interpretado con `time`, que en Unix mide cuánto tarda un comando:

```bash
go build -o bench_go bench.go && time ./bench_go   # nativo: arranque instantáneo
time python bench.py                               # interpretado: cómodo, más lento en cómputo
```

Resumen del núcleo, para tenerlo a mano:

```text
Modelo                 Lenguajes del núcleo
---------------------  --------------------------------
Compilado a máquina    C, Rust, Go
Interpretado (+bytecode interno)  Python, PHP
Bytecode + VM          Java (JVM), C# (CLR)
Transpilado            TypeScript (-> JavaScript)
JIT sobre la marcha    JavaScript (V8 interpreta y compila)
Declarativo / motor    SQL (lo planifica y ejecuta la base de datos)
```

## ✍️ Práctica

Toma un programa corto con un cálculo repetitivo (por ejemplo, sumar los primeros diez millones de enteros) y compáralo en dos modelos. Implémentalo en Go y en Python, mide ambos con `time`, y anota la diferencia de tiempo de cómputo *y* de arranque. Después introduce a propósito un error de nombre de variable en cada uno y observa cuándo se manifiesta: en Go, al construir; en Python, al ejecutar. Finalmente, transpila un `.ts` con `tsc` y abre el `.js` resultante: localiza dónde estaban tus anotaciones de tipo y comprueba que ya no aparecen. Con estas tres observaciones habrás tocado con las manos las tres consecuencias del modelo: rendimiento, momento del error y coste en tiempo de ejecución.

## ⚠️ Errores comunes

| Síntoma / creencia | Causa y cómo corregir |
|--------------------|-----------------------|
| «Compilado siempre es mejor» | Ignora el valor de iterar rápido. Elige según el caso: cómputo intenso vs. velocidad de desarrollo |
| «Interpretado = sin compilación» | Falso: Python y PHP compilan a bytecode internamente. La compilación existe, solo es transparente |
| Esperar tipos de TypeScript en ejecución | Se borran al transpilar. No validan datos en runtime; para eso hace falta código explícito |
| Extrañarse de que Java «tarde en arrancar» | La VM debe cargar clases y calentar el JIT. Es esperado; se estabiliza con el tiempo |
| Distribuir un binario compilado a otra arquitectura | Un ejecutable nativo está atado a CPU y SO. Recompila para el destino o usa un modelo portátil |

## ❓ Preguntas frecuentes

- **¿Qué es exactamente un JIT?** Un compilador *Just-In-Time* que traduce a código máquina durante la ejecución, concentrándose en las partes que más se repiten. Combina la flexibilidad del bytecode con velocidad cercana a la nativa; lo usan la JVM, el CLR y V8.
- **¿JavaScript es interpretado o compilado?** Ambas cosas por turnos: V8 empieza interpretando y va compilando con el JIT lo que se ejecuta con frecuencia. Es el ejemplo de que la dicotomía «compilado/interpretado» se queda corta.
- **¿Por qué SQL no encaja en ninguna categoría?** Porque es declarativo: no describe *cómo* ejecutar, sino *qué* resultado quieres. El motor de la base de datos decide el plan de ejecución. Se compila a un plan, no a instrucciones de CPU.
- **¿El modelo cambia el lenguaje o solo la implementación?** Solo la implementación. Existen intérpretes de C y compiladores de Python; lo dominante es una elección de ingeniería, no una ley del lenguaje.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre elegir la herramienta adecuada al problema.

---

> [⏮️ Clase 029](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/029-que-es-un-toolchain-del-codigo-fuente-al-programa-que-corre/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 031 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/031-anatomia-de-un-comando-nombre-subcomando-flags-argumentos-y-esquema/README.md)
