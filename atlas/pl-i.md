# 🧩 PL/I — 1964

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El lenguaje que quiso ser todos los lenguajes.** IBM lo diseñó para unificar el mundo científico de
[Fortran](fortran.md) y el mundo empresarial de [COBOL](cobol.md) en una sola herramienta. No lo
consiguió, pero por el camino inventó buena parte de lo que hoy damos por sentado.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: PL/I sigue en producción sobre z/OS.** IBM mantiene y vende *Enterprise
> PL/I for z/OS*, integrado con CICS, Db2 e IMS, y publica documentación actual. Es un nicho mucho
> menor que el de COBOL, pero es un nicho real: bancos y aseguradoras con aplicaciones críticas que
> nunca se reescribieron.
>
> Entra por dos conceptos que **el núcleo no muestra**. El primero es técnico: PL/I tuvo
> **manejo estructurado de excepciones (`ON` conditions), punteros, multitarea y aritmética decimal
> a la vez, en 1964** — antes de que ninguna de esas ideas se considerara normal. Leerlo es ver el
> origen del `try/catch`. El segundo es una lección de **diseño de lenguajes**, que es de lo que
> trata la [Parte 1](../classes/parte-1-atlas-y-genealogia-de-los-lenguajes/README.md): PL/I es el
> caso de estudio canónico de qué pasa cuando un lenguaje intenta cubrirlo todo. Dijkstra lo usó
> como advertencia; entender **por qué** es más útil que memorizar la anécdota.

| | |
|---|---|
| **Año** | 1964 (como *NPL*); estándar ANSI en 1976 |
| **Autoría** | **IBM** con el comité de usuarios **SHARE**, para el System/360 |
| **Familia** | Propósito general — síntesis deliberada de ALGOL, FORTRAN y COBOL |
| **Paradigma** | Imperativo, procedimental, estructurado, con concurrencia |
| **Tipado** | Estático, con **conversión implícita muy permisiva** entre tipos |
| **Memoria** | Cuatro clases de almacenamiento: `STATIC`, `AUTOMATIC`, `CONTROLLED`, `BASED` |
| **Ejecución** | Compilado a nativo (z/OS, AIX, Windows, OS/2) |
| **Estado** | 🟡 **Vivo pero minoritario** — mainframe empresarial, mucho menor que COBOL |

---

## 📜 Historia

En 1963 IBM tenía un problema de estrategia. Sus clientes científicos usaban FORTRAN, sus clientes
empresariales usaban COBOL, y la nueva línea **System/360** pretendía ser *una sola familia de
máquinas para todos*. Tener dos lenguajes y dos comunidades separadas contradecía la idea. El comité
*Advanced Language Development* del grupo de usuarios **SHARE** recibió el encargo de diseñar un
lenguaje único.

El resultado, primero llamado **NPL** (*New Programming Language*) y renombrado **PL/I** por conflicto
de marcas, se publicó en 1964. Su ambición era total: cálculo científico en punto flotante y
aritmética decimal empresarial, procesamiento de cadenas, ficheros, punteros y estructuras dinámicas,
multitarea, y **manejo de condiciones excepcionales** con `ON ERROR`, `ON ENDFILE`, `ON OVERFLOW`.
Todo eso, en 1964, cuando FORTRAN no tenía siquiera estructuras de datos y COBOL no tenía punteros.

También llevó al extremo una idea peligrosa: **no hay palabras reservadas**. `IF IF = THEN THEN THEN
= ELSE;` es una sentencia legal de PL/I, porque `IF`, `THEN` y `ELSE` pueden ser nombres de variable
y el compilador lo resuelve por contexto. Sumado a la conversión automática entre casi cualquier par
de tipos, el lenguaje se volvió difícil de compilar y, sobre todo, difícil de predecir.

Esa es la crítica que lo persigue. **Edsger Dijkstra** escribió en 1972, en su conferencia del Premio
Turing *The Humble Programmer*, uno de los juicios más citados de la disciplina: describió a PL/I
como un lenguaje cuya complejidad lo hacía inmanejable, comparándolo con una enfermedad fatal. La
frase es célebre y algo injusta —PL/I hizo cosas notables— pero señala un problema real: **la
generalidad tiene un coste cognitivo, y ese coste lo paga quien lee el código.**

Un dato que compensa la mala fama: **Multics**, el sistema operativo del MIT/Bell Labs que inspiró
directamente a Unix, se escribió en un subconjunto de PL/I llamado EPL. Fue de los primeros sistemas
operativos escritos en un lenguaje de alto nivel, y esa decisión influyó en que Ken Thompson y Dennis
Ritchie escribieran Unix en [C](c.md).

## 🏭 Dónde sobrevive hoy

- **Banca y seguros** con aplicaciones z/OS heredadas, típicamente conviviendo con COBOL en el mismo
  sistema.
- **Grandes corporaciones** con desarrollos de los 70 y 80 que resultaron más baratos de mantener que
  de reescribir.
- Integrado con **CICS** (transaccional), **Db2** (datos) e **IMS** (jerárquico), como el resto del
  ecosistema mainframe.

Un patrón habitual: PL/I para la lógica compleja y de cálculo, COBOL para el grueso del proceso por
lotes, ambos orquestados por [JCL](jcl.md).

## 🧠 Por qué no ha muerto

**1. Estaba donde estaba el dinero, y funcionó.** Las razones son las de COBOL: reglas de negocio
sedimentadas, riesgo asimétrico y coste de migración.

**2. IBM lo sigue manteniendo.** *Enterprise PL/I for z/OS* recibe versiones nuevas, con explotación
de las instrucciones modernas del procesador z e interoperabilidad con COBOL, C y Java en el mismo
sistema. No es un compilador abandonado.

**3. Es más expresivo que COBOL para cálculo.** Donde COBOL necesita rodeos, PL/I tiene expresiones,
recursión, punteros y estructuras dinámicas. En aplicaciones actuariales o de riesgo, eso importaba.

**4. Su modelo de excepciones es genuinamente bueno.** Las `ON` conditions permiten instalar
manejadores por condición (`ZERODIVIDE`, `OVERFLOW`, `ENDFILE`, `KEY`) y, en muchos casos,
**continuar** la ejecución. Es más parecido al sistema de condiciones y reinicios de
[Common Lisp](common-lisp.md) que al `try/catch` que heredamos.

## 🔄 Lo que se ha modernizado

Menos que COBOL, pero más de lo que su fama sugiere:

- **Aritmética decimal de 64 bits** y explotación de las instrucciones vectoriales del procesador
  **z/Architecture**, con optimización específica para el hardware actual.
- **JSON y XML**: el compilador incorpora soporte para generar y analizar ambos formatos, igual que
  COBOL, para poder participar en integraciones modernas.
- **Interoperabilidad**: llamadas entre PL/I, COBOL, C/C++ y Java dentro del mismo entorno **Language
  Environment**, lo que permite mantener PL/I como componente dentro de un sistema mixto.
- **Direccionamiento de 64 bits** y soporte Unicode (UTF-8/UTF-16).
- **Herramientas actuales**: depuración desde **VS Code** con IBM Z Open Editor, integración con Git y
  pipelines de CI/CD sobre z/OS mediante IBM Dependency Based Build.

Lo que **no** ha ocurrido: no hay una comunidad libre significativa ni un compilador abierto de
referencia. Esa es la diferencia práctica con COBOL, que sí tiene GnuCOBOL, y la razón por la que PL/I
está en 🟡 y no en 🟢.

## ⚙️ Cómo se ejecuta hoy

**En producción:** *IBM Enterprise PL/I for z/OS*. Compilación mediante JCL invocando el compilador,
enlace y ejecución.

**Fuera del mainframe:** existen implementaciones para otras plataformas —**Micro Focus / OpenText
Open PL/I** y **Iron Spring PL/I** (un subconjunto para Linux y OS/2)— pero son minoritarias y
parciales.

```text
//COMPILA  EXEC PGM=IBMZPLI,PARM='OBJECT,SOURCE'
//SYSIN    DD   DSN=MI.FUENTE(TOTVTA),DISP=SHR
//SYSLIN   DD   DSN=&&OBJ,DISP=(NEW,PASS)
```

Es decir: para compilar PL/I hay que escribir [JCL](jcl.md). Otro recordatorio de que en el mainframe
ningún lenguaje se usa solo.

## 🧪 El programa de la clase 041 en PL/I

> ⚠️ **Material de lectura, no verificado.** No hay compilador PL/I en los *runners* de CI. El código
> está escrito para ser correcto e idiomático, pero **sin el sello de la máquina**, y así se declara.

```pli
 total_venta: procedure options(main);

    declare precio     fixed decimal(11,2);
    declare cantidad   fixed decimal(11,2);
    declare descuento  fixed decimal(5,4);
    declare total      fixed decimal(15,2);
    declare presenta   picture 'ZZZZZZZZZ9V.99';

    on endfile(sysin) stop;

    get list (precio, cantidad, descuento);

    total = precio * cantidad * (1 - descuento);

    presenta = total;
    put skip list ('Total: ' || trim(presenta));

 end total_venta;
```

**Recorrido, línea a línea.**

- `procedure options(main)` marca el punto de entrada. En PL/I **todo es un procedimiento**, incluido
  el programa principal; no hay una sintaxis especial para el `main`.
- `fixed decimal(11,2)` es aritmética **decimal de coma fija**: 11 dígitos, 2 decimales, exacta. Es el
  mismo tipo conceptual que el `PIC 9(9)V99 COMP-3` de COBOL, pero declarado como un tipo y no como
  una plantilla de imagen. Junto a él conviven `fixed binary`, `float decimal` y `float binary`: PL/I
  es de los pocos lenguajes que distingue explícitamente **base** (decimal o binaria) de **escala**
  (fija o flotante). Esa matriz de cuatro combinaciones es exactamente la unión de FORTRAN y COBOL
  que el lenguaje buscaba.
- `on endfile(sysin) stop;` **instala un manejador de condición**. No es un `try` que envuelve un
  bloque: es una declaración que dice "de aquí en adelante, si se alcanza el fin de fichero en
  `sysin`, ejecuta esto". El ámbito es dinámico y el manejador queda activo durante toda la
  ejecución. Esta línea es, cronológicamente, uno de los primeros mecanismos de manejo estructurado
  de errores de la historia.
- `get list (...)` es la lectura dirigida por lista, igual que el `read(*,*)` de Fortran: lee tantos
  valores como variables haya, separados por espacios o comas.
- `picture 'ZZZZZZZZZ9V.99'` es un **dato numérico de imagen**, el mismo concepto que el campo editado
  de COBOL: cada `Z` suprime un cero a la izquierda, el `9` garantiza que el cero se imprima, y `V.`
  marca a la vez el punto decimal supuesto y el punto que se imprime. Asignar `total` a `presenta`
  **convierte automáticamente** de decimal a texto formateado.
- `||` es la concatenación de cadenas, y `trim` recorta los espacios que deja la supresión de ceros.

**Lo que no se ve pero define al lenguaje:** casi cualquier asignación entre tipos distintos
funcionaría aquí. Asignar una cadena `'27000'` a un `fixed decimal` compila y convierte. Es cómodo y
es, a la vez, exactamente la propiedad que hace que los errores de PL/I se manifiesten tarde. Compara
con [Ada](ada.md), diseñado veinte años después con la filosofía contraria.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En PL/I es… |
|---|---|
| `int` / `double` | `fixed binary(31)` / `float binary(53)` |
| `decimal` / `BigDecimal` | `fixed decimal(15,2)` — nativo |
| `try { } catch (E e) { }` | `on condition ... ;` — instalado, no envuelto |
| `struct` | `declare 1 registro, 2 campo ...;` — niveles, como COBOL |
| Puntero | `pointer` con variables `based` |
| `malloc` / `free` | `allocate` / `free` sobre almacenamiento `controlled` o `based` |
| `static` / variable local | `static` / `automatic` — las clases de almacenamiento son explícitas |
| Hilos | `task` — multitarea en el lenguaje, en 1964 |
| `printf("%s", x)` | `put skip list (x)` o `put edit (x) (formato)` |

## ⚠️ Errores comunes al leerlo

- **Suponer palabras reservadas.** Una variable puede llamarse `IF` o `DO`. Al leer código antiguo,
  no des por hecho que una palabra clave lo es.
- **Ignorar las conversiones implícitas.** PL/I convierte casi todo a casi todo. Una operación entre
  `fixed decimal` y `fixed binary` produce reglas de precisión que hay que consultar en el manual;
  no son intuitivas y son fuente de errores de redondeo silenciosos.
- **Leer `on` como `try`.** El manejador se instala y permanece; no delimita un bloque. Dos `on` para
  la misma condición en el mismo ámbito significan que el segundo sustituye al primero.
- **Confundir `%INCLUDE` con un `import`.** Es una inclusión textual en tiempo de preproceso, como el
  `#include` de C, con las mismas consecuencias.
- **Olvidar la columna.** Igual que COBOL, el PL/I clásico usa formato de columnas fijas heredado de
  la tarjeta perforada (habitualmente 2–72).

## 📚 Fuentes y bibliografía

- [IBM Enterprise PL/I for z/OS — documentación](https://www.ibm.com/docs/en/epfz) — referencia del
  lenguaje y guía de programación, versión vigente.
- [IBM Enterprise PL/I (producto)](https://www.ibm.com/products/pli-compiler-zos) — el compilador que
  IBM mantiene y vende hoy.
- **Edsger W. Dijkstra**, *The Humble Programmer*, ACM Turing Award Lecture, 1972 —
  [texto original](https://www.cs.utexas.edu/~EWD/transcriptions/EWD03xx/EWD340.html). Léelo por el
  argumento sobre la complejidad, no por la frase suelta.
- **Joan K. Hughes**, *PL/I Structured Programming*, Wiley — el manual clásico del lenguaje.
- **Robin A. Vowels**, *Introduction to PL/I and Algorithms* — enfoque didáctico y accesible.
- **Multics History** ([multicians.org](https://www.multicians.org/)) — la historia del sistema
  operativo escrito en PL/I que llevó, por reacción, a Unix y a C.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [COBOL](cobol.md) · [RPG](rpg.md) · [JCL](jcl.md) · [C](c.md)
