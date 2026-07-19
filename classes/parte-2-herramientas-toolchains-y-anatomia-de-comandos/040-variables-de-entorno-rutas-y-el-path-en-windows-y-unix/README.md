# Clase 040 — Variables de entorno, rutas y el PATH en Windows y Unix

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Cuando escribes `python` y pulsas Enter, ocurre algo que casi nadie se para a pensar: el sistema no sabe dónde está Python. Tiene que buscarlo, y lo hace recorriendo en orden una lista de carpetas que alguien configuró antes. Esa lista es el **PATH**, y es una de las varias **variables de entorno** que el sistema entrega a cada programa que arranca. Esta clase trata de ese entorno invisible en el que corren tus comandos, y de por qué entenderlo explica de golpe una familia entera de problemas que de otro modo parecen magia negra: el `command not found` de una herramienta que acabas de instalar, la versión equivocada de un intérprete que aparece sin motivo, el script que funciona en tu terminal y falla en el servidor de integración continua.

El mecanismo importa porque es la frontera entre tu programa y el sistema que lo hospeda. Kernighan y Pike describen el entorno como parte del contexto que un proceso hereda al nacer, y esa palabra —**heredar**— es la clave que ordena todo lo demás. Shotts dedica en *The Linux Command Line* un capítulo entero a este asunto por la misma razón: quien no entiende cómo se propaga el entorno no puede diagnosticar por qué su configuración funciona en un sitio y no en otro. Al terminar deberías poder abrir una terminal ante un `command not found` y llegar a la causa en menos de un minuto, en lugar de reinstalar cosas al azar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es una variable de entorno, cómo se hereda y para qué sirve el PATH.
2. Diagnosticar un `command not found` razonando sobre el PATH y su orden de búsqueda.
3. Explicar por qué un comando resuelve a una versión inesperada y cómo comprobar cuál se está ejecutando.
4. Reconocer las diferencias reales de rutas y separadores entre Windows y Unix, y escribir código que no dependa de ellas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Variables de entorno | Configuración que reciben los programas |
| 2 | El PATH | Dónde busca el sistema los ejecutables |
| 3 | Rutas Windows vs. Unix | Separadores, mayúsculas, barras |
| 4 | Diagnóstico | Por qué 'command not found' y cómo resolverlo |
| 5 | Herencia del entorno | Por qué un cambio en un script no afecta a tu terminal |

## 📖 Definiciones y características

Una **variable de entorno** es un par nombre-valor que el sistema operativo entrega a un proceso cuando lo arranca. Su propiedad fundamental, y la que explica casi todo su comportamiento desconcertante, es la **herencia**: cada proceso recibe una *copia* del entorno de quien lo lanzó, y los cambios que haga sobre esa copia afectan a él y a los procesos que él arranque después, pero jamás a su padre. De ahí que un script que exporta una variable no modifique la terminal desde la que lo lanzaste, y que para conseguirlo haya que ejecutarlo *dentro* de la sesión actual con `source` en lugar de como proceso aparte. No es una rareza del shell: es la semántica del entorno, y una vez entendida deja de sorprender que el `cd` de un script no cambie tu directorio actual. El valor de este mecanismo es que permite configurar un programa sin tocar su código ni sus argumentos, que es justamente lo que se necesita cuando el mismo binario debe comportarse distinto en desarrollo y en producción.

El **PATH** es la variable con mayor impacto diario. Contiene una lista ordenada de carpetas y el sistema la recorre **en orden, deteniéndose en la primera coincidencia**, cuando le pides ejecutar un comando por su nombre. De ese "en orden" y "la primera" se derivan dos consecuencias prácticas. La primera es el `command not found`: si el ejecutable existe pero su carpeta no está en la lista, el sistema no lo encuentra, exactamente igual que no encontrarías un libro que está en una estantería que no miraste. El programa no está roto, está fuera del alcance de la búsqueda. La segunda es más sutil y causa más horas perdidas: el **enmascaramiento**. Si dos carpetas del PATH contienen un ejecutable con el mismo nombre, gana la que aparece antes. Así es como acabas ejecutando el Python del sistema cuando creías estar usando el de tu gestor de versiones, o una herramienta vieja que quedó en `/usr/local/bin` sobre la nueva. La pregunta correcta ante cualquier duda no es "¿está instalado?" sino "¿cuál se está ejecutando?", y se responde preguntándole al propio sistema con `which` en Unix o `Get-Command` en PowerShell, que muestran la ruta que ganó la búsqueda. Todos los gestores de versiones de la clase 032 —pyenv, nvm, rustup, sdkman— funcionan manipulando este orden: no reinstalan nada, solo colocan delante la carpeta de la versión que has activado.

Las **rutas** difieren entre sistemas más de lo que parece, y no solo en el símbolo. Unix separa componentes con `/` y las entradas del PATH con `:`; Windows usa `\` y separa el PATH con `;`. Esa diferencia de separador de lista no es arbitraria: en Windows los dos puntos ya estaban ocupados por la letra de unidad (`C:`), así que hubo que elegir otro carácter. La barra invertida trae un problema añadido en el mundo Unix, donde `\` es el carácter de escape, y por eso las rutas de Windows escritas en cadenas de código suelen requerir duplicarla o usar literales sin escape. Hay otras dos asimetrías que muerden en la práctica. Una es que los sistemas de archivos de Unix distinguen mayúsculas y minúsculas mientras que los de Windows normalmente no: un `import Utils` que funciona en tu portátil puede fallar en el servidor Linux porque el archivo se llama `utils.py`, y es un fallo que solo aparece en integración continua. La otra afecta a cómo se ejecuta un programa del directorio actual: en Unix hay que escribir `./main` porque el directorio actual **no** está en el PATH por diseño —incluirlo permitiría que un ejecutable malicioso dejado en una carpeta compartida se ejecutara al teclear un nombre común—, mientras que Windows sí busca primero en el directorio actual y además consulta la variable `PATHEXT` para saber qué extensiones considera ejecutables.

Conviene cerrar con el uso más habitual de las variables de entorno fuera del PATH: la **configuración y los secretos**. Sacar una clave de API o una cadena de conexión del código y ponerla en el entorno es una buena práctica sólida, porque separa la configuración —que cambia entre entornos— del programa, que no debería cambiar, y evita que una credencial acabe en el repositorio, donde vivirá para siempre en el historial aunque la borres después. Pero conviene no exagerar la garantía: el entorno de un proceso es legible por ese proceso y por todos sus hijos, y a menudo inspeccionable desde fuera por el propio usuario. Es mucho mejor que codificar el secreto, y bastante menos que un gestor de secretos dedicado. Ese matiz es la diferencia entre aplicar una práctica y entenderla.

- **Variable de entorno** — valor con nombre que el sistema pasa a los programas (PATH, HOME). Clave: configura sin tocar el código.
- **PATH** — lista de carpetas donde se buscan los ejecutables. Clave: si un programa no está en el PATH, 'no se encuentra'.
- **Ruta absoluta vs. relativa** — desde la raíz (/usr/bin) o desde la carpeta actual (./main). Clave: evita ambigüedad sobre qué se ejecuta.
- **Separador de rutas** — ':' en Unix y ';' en Windows para el PATH; '/' vs. '\' en las rutas. Clave: fuente de errores multiplataforma.

## 🧩 Situación

Instalas una herramienta, abres la terminal, escribes su nombre y el sistema responde `command not found`. El instinto lleva a desinstalar y reinstalar, o a sospechar que la descarga se corrompió. Casi nunca es eso. El ejecutable está donde el instalador lo dejó; lo que falta es que esa carpeta figure en el PATH, así que el sistema busca en las estanterías que conoce, no lo encuentra y lo dice. La prueba es inmediata: si invocas el programa por su ruta completa, funciona. Ahí queda claro que el problema no era el programa sino la búsqueda.

La variante más traicionera de esta escena es la contraria: el comando **sí** se encuentra, pero es el equivocado. Escribes `python --version` y obtienes una versión que no instalaste tú, porque otra carpeta del PATH aparece antes y contiene otro ejecutable con el mismo nombre. Aquí no hay ningún mensaje de error que te avise: el sistema hizo exactamente lo que le pediste, ejecutar el primer `python` que encontró. Por eso la herramienta de diagnóstico más rentable de toda esta clase es preguntar por la ruta resuelta antes que por la versión, y por eso el orden del PATH merece tratarse como configuración deliberada y no como una acumulación de líneas que fueron añadiendo los instaladores.

## 🔎 Ejemplo

Ver y usar variables de entorno y el PATH:

```text
Unix (bash):
  echo $PATH                    # ver el PATH
  export API_KEY="abc123"       # definir una variable

Windows (PowerShell):
  $env:PATH                     # ver el PATH
  $env:API_KEY = "abc123"       # definir una variable
```

Hay tres cosas que conviene notar en estas cuatro líneas. La primera es que la sintaxis difiere pero el modelo es idéntico: en ambos sistemas existe un diccionario de nombre a valor asociado al proceso, y ambos ofrecen una forma de leerlo y otra de escribirlo. La segunda es qué significa exactamente `export` en bash: sin él, la variable existe solo para el shell actual y **no** se hereda a los programas que lances; con él, pasa a formar parte del entorno que se copia a cada proceso hijo. Esa distinción entre variable de shell y variable de entorno explica muchos "pero si la definí" que terminan en desconcierto.

La tercera es que ambos comandos son temporales y solo afectan a esa sesión. Al cerrar la terminal, la variable desaparece, porque el proceso que la contenía murió y con él su copia del entorno. Para que persista hay que escribirla donde se construye el entorno de cada nueva sesión: los archivos de perfil del shell en Unix, el perfil de PowerShell o la configuración de variables del usuario en Windows. Y esa temporalidad, lejos de ser un inconveniente, es la forma más limpia de fijar configuración para una sola ejecución sin contaminar el sistema, que es exactamente lo que hacen los sistemas de integración continua al inyectar sus secretos.

## ✍️ Práctica

Muestra tu PATH (`echo $PATH` o `$env:PATH`), cuenta cuántas carpetas incluye y comprueba si está la del lenguaje que instalaste. Después haz el ejercicio de diagnóstico completo, que es lo que de verdad se transfiere:

1. **Pregunta qué se ejecuta, no si está instalado.** Usa `which python` (Unix) o `Get-Command python` (PowerShell) y anota la ruta exacta que devuelve. Compárala con la que esperabas.
2. **Busca enmascaramientos.** En Unix, `which -a python` lista *todos* los candidatos en orden; el primero es el que gana. Si hay más de uno, ya sabes por qué a veces obtienes una versión inesperada.
3. **Comprueba la herencia.** Define una variable sin exportarla, lanza un programa que la lea y observa que no la ve. Expórtala y repite. Estás viendo la frontera entre el shell y los procesos hijos.
4. **Verifica la temporalidad.** Define una variable, cierra la terminal, ábrela de nuevo y comprueba que ya no está. Averigua después dónde tendrías que escribirla para que persistiera en tu sistema.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| `command not found` justo después de instalar algo | La carpeta del ejecutable no está en el PATH. Añádela, o comprueba que funciona invocándolo por su ruta completa |
| El comando existe pero responde una versión inesperada | Otra carpeta del PATH aparece antes y contiene un ejecutable homónimo. Resuelve con `which -a` o `Get-Command` y reordena el PATH |
| La variable que definí "no le llega" al programa | En bash, sin `export` es variable de shell, no de entorno, y no se hereda. Expórtala |
| El script cambia el PATH o el directorio y al volver nada cambió | Un proceso hijo no puede modificar el entorno del padre. Ejecútalo con `source` para que corra en la sesión actual |
| Funciona en local y falla en el servidor Linux por un archivo "que existe" | Unix distingue mayúsculas y minúsculas y Windows normalmente no. Unifica los nombres y respétalos siempre |
| Rutas con `\` o `/` escritas a mano en el código | Cada sistema usa un separador distinto y `\` además escapa en muchas cadenas. Usa la biblioteca de rutas del lenguaje y rutas relativas |
| Una credencial acaba subida al repositorio | Estaba escrita en el código. Léela del entorno y no la incluyas nunca en el control de versiones |

## ❓ Preguntas frecuentes

- **¿Dónde guardo secretos como una clave de API?** En variables de entorno, nunca en el código ni en un archivo versionado. Dicho esto, el entorno no es una caja fuerte: cualquier proceso hijo lo hereda y el propio usuario suele poder inspeccionarlo. Para datos realmente sensibles en producción, un gestor de secretos dedicado es el siguiente paso.
- **¿Por qué en Unix hay que escribir `./main` y en Windows no?** Porque en Unix el directorio actual no está en el PATH deliberadamente. Si lo estuviera, bastaría con dejar un ejecutable malicioso llamado como un comando habitual en una carpeta compartida para que alguien lo ejecutara sin darse cuenta. Windows sí busca primero en el directorio actual, herencia de su tradición de sistema monousuario.
- **¿Por qué el PATH usa `:` en Unix y `;` en Windows?** Porque en Windows los dos puntos ya estaban ocupados por la letra de unidad (`C:`), así que hacía falta otro carácter. Es una consecuencia de decisiones históricas de cada sistema, no de una preferencia estética.
- **¿Modificar el PATH puede romper mi sistema?** Sí, si lo sobrescribes en lugar de añadirle una carpeta. Un PATH sin `/usr/bin` deja la terminal casi inservible. La regla es siempre extender el valor existente, nunca reemplazarlo, y probar en una sesión temporal antes de hacerlo permanente.
- **¿Cómo consigo que mi programa funcione igual en Windows y en Unix?** No construyendo rutas a mano. Todos los lenguajes del núcleo ofrecen una biblioteca que compone rutas con el separador correcto del sistema y lee el entorno de forma uniforme. Usarla, junto con rutas relativas al proyecto, elimina la mayoría de estos problemas antes de que aparezcan.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press), cap. sobre el entorno y su configuración — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall), sobre el contexto que un proceso hereda.
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre separar la configuración del código.

---

> [⏮️ Clase 039](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/039-empaquetado-y-distribucion-wheels-jars-binarios-contenedores/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 041 ⏭️](../../parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md)
