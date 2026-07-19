# Clase 039 — Empaquetado y distribución: wheels, jars, binarios, contenedores

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Un programa que funciona en tu máquina todavía no es un producto. Entre "compila y pasa las pruebas aquí" y "otra persona lo ejecuta allí" hay un paso que casi nunca se enseña y que decide buena parte del éxito de un proyecto: el **empaquetado**, el acto de convertir tu código y todo lo que necesita en un artefacto que alguien pueda instalar o ejecutar sin repetir tu entorno. Según el lenguaje ese artefacto se llama wheel, jar, binario, dll o imagen de contenedor, pero todos responden a la misma pregunta: qué se lleva el usuario y qué se espera que ya tenga.

Debajo de la variedad de formatos hay un solo eje que los ordena, y entenderlo vale más que memorizar comandos: **cuándo se resuelven las dependencias**. Un binario estático de Go las resuelve en tiempo de compilación y las lleva dentro, de modo que en destino no hace falta nada. Una wheel de Python las resuelve en tiempo de instalación, cuando `pip` lee sus requisitos y los descarga. Un jar las resuelve en tiempo de ejecución y además exige que la máquina virtual de Java ya esté presente. Y un contenedor toma el camino radical: no resuelve nada en destino porque se lleva el entorno entero consigo. Cada opción reparte de manera distinta el trabajo y el riesgo entre quien publica y quien instala, y esa repartición es exactamente la decisión de ingeniería que esta clase enseña a tomar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Nombrar el formato de distribución típico de cada lenguaje del núcleo y decir qué asume del entorno destino.
2. Explicar el eje que los ordena: cuándo se resuelven las dependencias y quién paga ese trabajo.
3. Explicar qué resuelve un contenedor frente a distribuir solo el artefacto, y qué cuesta.
4. Relacionar el empaquetado con la reproducibilidad y con el clásico "en mi máquina funciona".

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Formatos de artefacto | wheel, jar, binario, dll |
| 2 | El binario autocontenido | Go y Rust producen un solo archivo |
| 3 | Contenedores | Empaquetan el programa con su entorno |
| 4 | Distribución | Repositorios, registries y releases |
| 5 | Cuándo se resuelven las dependencias | El eje que explica todos los formatos |

## 📖 Definiciones y características

**Empaquetar** es preparar un programa y sus dependencias para que otra persona lo use, y la palabra decisiva es *dependencias*. Todo programa no trivial se apoya en cosas que no escribiste: bibliotecas de terceros, la biblioteca estándar del lenguaje, un intérprete o una máquina virtual, y por debajo de todo eso, bibliotecas del sistema operativo como la libc. Empaquetar consiste en decidir cuáles de esas capas viajan con el artefacto y cuáles se dan por presentes en destino. Cada capa que incluyes engorda el paquete pero elimina un supuesto sobre la máquina ajena; cada capa que excluyes lo aligera pero añade un requisito que puede no cumplirse. No hay respuesta universal: hay un compromiso que se elige según a quién distribuyes.

Los formatos del núcleo se entienden bien colocados sobre ese eje. Una **wheel** de Python (`.whl`) es un paquete ya construido —frente a un `sdist`, que es código fuente y obliga a compilar en destino— que `pip` descomprime e instala, resolviendo entonces las dependencias declaradas y descargándolas del índice. Asume que hay un Python compatible instalado, y si el paquete contiene extensiones en C, asume además una plataforma concreta, que es por lo que el nombre del archivo incluye versión de Python, ABI y sistema. Un **jar** de Java es un archivo comprimido con bytecode y un manifiesto que indica la clase de arranque; su promesa es la portabilidad entre sistemas operativos, pero a cambio exige una máquina virtual en destino y, si tiene dependencias, o bien las incluye dentro (el llamado *fat jar*) o bien deben estar en el classpath. Un **binario autocontenido**, típico de Go y alcanzable en Rust y C, es el extremo opuesto: el enlazado estático mete todo dentro del ejecutable, así que se copia y funciona sin instalar nada. Su coste es el tamaño y que el binario es específico de una arquitectura y un sistema, aunque compiladores como el de Go hacen la compilación cruzada casi trivial. En .NET la misma tensión aparece explícitamente como la elección entre publicar *dependiente del framework* —pequeño, exige el runtime instalado— o *autocontenido* —grande, no exige nada—.

Un **contenedor** cambia la pregunta en lugar de responderla mejor. En vez de decidir qué dependencias incluir, incluye el sistema de archivos entero: tu programa, sus bibliotecas, sus binarios de sistema y una distribución mínima de Linux, todo en una imagen que se ejecuta con un aislamiento proporcionado por el núcleo del anfitrión. Conviene ser preciso aquí, porque es la confusión más común: un contenedor **no** es una máquina virtual. No emula hardware ni arranca un sistema operativo completo; comparte el núcleo del anfitrión y se apoya en mecanismos de aislamiento de ese núcleo, lo que explica que arranque en milisegundos y ocupe una fracción de lo que ocuparía una máquina virtual. Lo que gana es la eliminación de la clase entera de fallos por diferencia de entorno, la que Hunt y Thomas atacan cuando insisten en automatizar y hacer reproducible todo lo que se repita: si la imagen es la misma, el entorno es el mismo en desarrollo, en pruebas y en producción. Lo que cuesta es una capa más de herramientas que aprender y mantener, imágenes que hay que actualizar cuando aparecen vulnerabilidades en sus capas base, y un artefacto mucho más pesado de mover.

La **distribución** es el último tramo y tiene su propia disciplina. Cada ecosistema tiene su repositorio público —PyPI, Maven Central, crates.io, npm, NuGet, Packagist, los registros de imágenes— donde se publica el artefacto bajo un nombre y una versión. Ahí la convención dominante es el versionado semántico, con sus tres números que comunican si un cambio rompe la compatibilidad, añade funcionalidad o solo corrige; respetarlo es lo que permite a quien depende de ti actualizar sin miedo, y saltárselo es una de las formas más eficaces de perder la confianza de tus usuarios. La regla operativa que enlaza empaquetado y distribución es la reproducibilidad: el mismo código fuente y las mismas versiones de dependencias deberían producir el mismo artefacto, lo que exige fijar versiones exactas con un lockfile (clase 035) y construir en un entorno limpio y automatizado, no en el portátil de quien publica.

- **Empaquetado** — preparar un programa y sus dependencias para distribuirlo. Clave: define cómo lo instala el usuario final.
- **wheel/jar** — formatos empaquetados de Python y Java. Clave: instalables sin recompilar.
- **Binario autocontenido** — un único ejecutable con todo dentro (típico de Go). Clave: se copia y corre sin instalar nada más.
- **Contenedor** — imagen que incluye el programa y su sistema operativo mínimo (Docker). Clave: elimina el 'funciona en mi máquina'.

## 🧩 Situación

Un servicio en Python funciona perfectamente en desarrollo y falla al desplegarlo. El error no menciona tu código: se queja de un símbolo que no encuentra en una biblioteca del sistema. La causa es que el servidor tiene una versión distinta de esa biblioteca y una dependencia tuya trae una extensión compilada contra otra. Nadie escribió mal ni una línea; simplemente el artefacto que distribuiste daba por supuesto un entorno que en destino no existía.

Aquí se ve por qué el eje de las dependencias es lo que hay que mirar. Reinstalar paquetes en el servidor no arregla el problema de fondo, porque el supuesto sigue ahí y volverá a fallar en la siguiente máquina. Empaquetar el servicio en un contenedor lo elimina de raíz: la imagen lleva su propia versión de esa biblioteca y ya no depende de lo que haya instalado el anfitrión. La misma lógica explica por qué los equipos que despliegan servicios en Go rara vez sufren esto: su artefacto ya resolvió todo en tiempo de compilación. Elegir formato es, en el fondo, elegir cuántos supuestos sobre la máquina ajena estás dispuesto a arriesgar.

## 🔎 Ejemplo

Formato de distribución por lenguaje:

```text
Python   wheel (.whl) / sdist       → pip install
Java     jar (.jar)                → java -jar app.jar
Go/Rust  binario único             → copiar y ejecutar
C#       dll / ejecutable .NET
Cualquiera  imagen Docker          → docker run
```

Lee la tabla por su columna implícita, la que no está escrita: qué exige cada fila de la máquina destino. Para la wheel, un intérprete de Python compatible y, si trae extensiones nativas, la plataforma correcta. Para el jar, una máquina virtual de Java de versión suficiente. Para el binario, nada en absoluto salvo la arquitectura y el sistema para los que se compiló. Para .NET, el runtime, salvo que publiques en modo autocontenido. Para la imagen, un motor de contenedores y un núcleo compatible.

Esa columna invisible es la que decide en la práctica. Si distribuyes a desarrolladores del mismo ecosistema, la wheel o el jar son ideales, porque son pequeños y el usuario ya tiene la plataforma. Si distribuyes una herramienta de línea de comandos a usuarios que no quieren saber en qué está escrita, el binario único gana sin discusión: es la razón principal de que tantas herramientas modernas de infraestructura estén escritas en Go. Y si despliegas un servicio en una flota de máquinas cuyo estado no controlas del todo, la imagen es la que elimina la variable. Mismo programa, cuatro respuestas correctas según a quién se lo entregas.

## ✍️ Práctica

Piensa cómo entregarías un programa a alguien sin tu entorno, y hazlo con método en vez de por intuición. Toma tres destinatarios distintos para el **mismo** programa: (a) un compañero de equipo que tiene tu mismo toolchain instalado, (b) un usuario final que solo quiere ejecutar una herramienta de línea de comandos y no sabe qué es un intérprete, y (c) un servidor de producción donde el servicio debe correr igual que en pruebas.

Para cada uno, responde por escrito tres preguntas: qué formato elegirías, qué asumes que ya existe en la máquina destino y qué falla concreto podría ocurrir si ese supuesto no se cumple. Verás que la respuesta cambia con el destinatario aunque el código sea idéntico, y que casi siempre el criterio decisivo no es técnico sino de quién paga el trabajo de resolver las dependencias: tú al empaquetar, o el usuario al instalar.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Distribuir el código fuente y pedir "que lo compilen" | Traslada al usuario toda la complejidad del toolchain. Entrega un artefacto construido o una imagen lista para ejecutar |
| "En mi máquina funciona" | El artefacto asume un entorno que en destino no existe. Identifica el supuesto y elimínalo: enlaza estático o empaqueta el entorno |
| Falta un símbolo de una biblioteca del sistema al arrancar | Una dependencia nativa se compiló contra otra versión de la libc. Construye en el mismo entorno de destino o usa un contenedor |
| Publicar sin fijar versiones de dependencias | Cada construcción produce un artefacto distinto. Usa un lockfile y construye en un entorno limpio y automatizado |
| Publicar un cambio incompatible sin subir la versión mayor | Rompes a todos los que dependen de ti sin avisar. Respeta el versionado semántico |
| Construir el artefacto a mano en el portátil de quien publica | No es reproducible ni auditable. Constrúyelo en integración continua, desde el repositorio |
| Meter secretos o credenciales dentro de la imagen o el paquete | Quedan en el artefacto publicado y en el historial de capas. Pásalos por variables de entorno en tiempo de ejecución (clase 040) |

## ❓ Preguntas frecuentes

- **¿Un contenedor es una máquina virtual?** No. Una máquina virtual emula hardware y arranca un sistema operativo completo con su propio núcleo; un contenedor comparte el núcleo del anfitrión y solo aísla el sistema de archivos, los procesos y la red. Por eso arranca en milisegundos y pesa una fracción. Lo que empaqueta es el entorno de usuario, no un sistema operativo entero.
- **¿Por qué Go es tan cómodo de distribuir?** Porque enlaza estáticamente por defecto y produce un ejecutable único sin dependencias externas, y porque compilar para otra plataforma es cuestión de dos variables de entorno. Ese es el motivo de que buena parte de las herramientas modernas de infraestructura estén escritas en Go, más allá del lenguaje en sí.
- **¿Entonces el contenedor sustituye al empaquetado del lenguaje?** No, lo envuelve. Dentro de la imagen sigue habiendo una wheel, un jar o un binario; el contenedor añade el entorno alrededor. Son capas complementarias, y la imagen de un binario estático puede ser diminuta precisamente porque ya no necesita casi nada alrededor.
- **¿Qué diferencia hay entre una wheel y un sdist?** La wheel es una distribución ya construida: se instala descomprimiendo, sin compilar nada. El sdist es el código fuente y obliga a construir en la máquina destino, lo que exige un compilador y cabeceras de desarrollo, y es la causa habitual de instalaciones que fallan de forma incomprensible en máquinas ajenas.
- **¿Qué significa que una construcción sea reproducible?** Que a partir del mismo código y las mismas versiones de dependencias se obtiene el mismo artefacto, sin importar quién ni cuándo la ejecute. Es lo que permite auditar qué hay realmente dentro de lo que publicas y volver atrás con confianza cuando algo se rompe.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall), sobre programas como componentes que se entregan y combinan.
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre automatizar la construcción y hacer reproducible todo lo repetible.

---

> [⏮️ Clase 038](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/038-pruebas-desde-la-terminal-pytest-node-test-go-test-cargo-test-dotnet-test-phpunit/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 040 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/040-variables-de-entorno-rutas-y-el-path-en-windows-y-unix/README.md)
