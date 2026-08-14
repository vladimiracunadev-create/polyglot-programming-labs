# 📋 JCL — década de 1960

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**No es un lenguaje de programación, y por eso hay que estudiarlo.** JCL no calcula nada: describe
**qué programa ejecutar, con qué datos y en qué orden**. Todo el proceso nocturno por lotes de la
banca mundial —el momento en que se liquidan las operaciones del día— está descrito en JCL.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: JCL se ejecuta cada noche en cada mainframe z/OS del planeta.** Es la
> pieza sin la cual el [COBOL](cobol.md) y el [PL/I](pl-i.md) de producción no arrancan. Quien
> trabaje profesionalmente con mainframe escribe JCL a diario, aunque no escriba COBOL.
>
> Y entra, sobre todo, porque **enseña una separación que los lenguajes del núcleo tienen borrosa**:
> la que hay entre **el programa** y **su entorno de ejecución**. Un programa COBOL no sabe dónde
> están sus ficheros: se refiere a nombres lógicos (*ddnames*), y es el JCL quien los conecta a
> ficheros reales **en el momento de ejecutar**. Eso es inyección de dependencias a nivel de sistema
> operativo, en 1964. La misma idea que hoy llamamos "configuración por entorno", "volúmenes de
> Docker" o "los doce factores" estaba resuelta —de otra manera y con otro vocabulario— antes de que
> existiera Unix. Y su `COND` sobre códigos de retorno es el antepasado directo de cualquier
> pipeline de CI que decide si el siguiente paso se ejecuta.

| | |
|---|---|
| **Año** | 1964, con el **IBM System/360** y el sistema operativo OS/360 |
| **Autoría** | **IBM** |
| **Familia** | Lenguajes de control de trabajos (*job control*) |
| **Paradigma** | **Declarativo**: describe recursos y secuencia, no algoritmos |
| **Tipado** | No aplica — describe recursos, no valores |
| **Memoria** | No aplica; sí gestiona **asignación de espacio en disco** |
| **Ejecución** | Interpretado por el **subsistema de entrada de trabajos** (JES2/JES3) de z/OS |
| **Estado** | 🟢 **Imprescindible en el mundo mainframe** — banca, seguros, gobierno, retail |

---

## 📜 Historia

Cuando IBM lanzó el **System/360** en 1964, resolvió un problema que hoy ni nos planteamos: **cómo
decirle a un ordenador compartido qué hacer a continuación**. No había línea de comandos, ni sesión
interactiva, ni terminal. Se entregaba una bandeja de tarjetas perforadas al operador, y esa bandeja
tenía que explicarse a sí misma: qué programa cargar, cuánta memoria necesitaba, en qué unidad de
cinta estaba la entrada, dónde dejar la salida, cuánto podía tardar y qué hacer si fallaba.

**JCL** es ese lenguaje de descripción. Sus rarezas se explican todas por la tarjeta perforada:

- Cada sentencia empieza por `//` en las **columnas 1 y 2**, porque así se distinguía de una tarjeta
  de datos.
- El campo de nombre va en la columna 3, la operación después, y **las columnas 73 a 80 se ignoran**
  porque ahí iba el número de secuencia de la tarjeta (para reordenar la bandeja si se caía al suelo).
- La continuación de línea se marca con una coma final y el `//` de la siguiente.

Sesenta años después, esas columnas siguen siendo obligatorias.

El modelo conceptual es de tres niveles, y no ha cambiado:

- **JOB** — la unidad de trabajo: quién lo envía, con qué prioridad, con qué límites de recursos.
- **EXEC** — un **paso**: qué programa (o qué procedimiento) ejecutar. Un trabajo tiene de uno a
  cientos de pasos.
- **DD** (*Data Definition*) — la conexión entre **un nombre lógico que el programa conoce** y **un
  fichero real del sistema**.

## 🏭 Dónde sobrevive hoy

- **El proceso nocturno por lotes** de bancos, aseguradoras, procesadores de tarjetas y organismos
  públicos: la "ventana batch" en la que se consolidan las operaciones del día, se calculan intereses,
  se generan extractos y se cuadran los saldos.
- **Compilación y despliegue** en z/OS: compilar un COBOL, enlazarlo y copiarlo a la librería de carga
  se hace enviando un trabajo JCL.
- **Operación y explotación**: cargas masivas, copias de seguridad, reorganización de bases de datos,
  intercambio de ficheros entre entidades.
- **Planificación**: herramientas como IBM Workload Scheduler o Control-M orquestan miles de trabajos
  JCL con dependencias entre ellos. La "malla batch" de una entidad grande son decenas de miles de
  ejecuciones diarias.

## 🧠 Por qué no ha muerto

**1. Porque el proceso por lotes no ha muerto.** Hay trabajo que solo tiene sentido hacer en bloque a
una hora fija: cerrar un día contable, calcular intereses sobre todas las cuentas, compensar entre
bancos. Eso no es un microservicio, es un lote, y necesita alguien que lo describa.

**2. El desacoplamiento programa/datos es real y sigue siendo útil.** El programa dice `SELECT
CLIENTES ASSIGN TO ENTRADA`; el JCL dice `//ENTRADA DD DSN=PROD.CLIENTES.2026,DISP=SHR`. Cambiar de
fichero de prueba a fichero de producción no toca ni una línea del programa ni requiere recompilar.
Es exactamente el problema que resuelven hoy las variables de entorno y los volúmenes montados.

**3. La gestión de recursos es explícita y auditable.** El JCL declara cuánto espacio pedir, en qué
volumen, con qué disposición si el trabajo falla, y qué hacer con el fichero después. En un sistema
compartido por miles de trabajos con SLA, esa explicitud es una característica, no una molestia.

**4. Los códigos de retorno gobiernan el flujo.** `COND` —y su forma moderna `IF/THEN/ELSE`— decide si
un paso se ejecuta según cómo terminaron los anteriores. Es el mismo modelo mental que `&&` en un
shell o `needs:` en GitHub Actions.

**5. Décadas de mallas de trabajos con dependencias.** Rehacerlo implica reconstruir el mapa completo
de qué depende de qué, y ese mapa muchas veces solo existe en la propia malla.

## 🔄 Lo que se ha modernizado

- **`IF/THEN/ELSE/ENDIF`** sustituyó al críptico `COND=(4,LT,PASO)`, cuya lógica invertida —se
  ejecuta el paso si la condición es **falsa**— ha confundido a generaciones enteras.
- **JCL simbólico y `SET`**: variables y sustitución para escribir procedimientos parametrizados y no
  copiar el mismo trabajo veinte veces.
- **Zowe**: el marco de código abierto (bajo la Open Mainframe Project) que expone z/OS mediante
  **API REST**, una **CLI** y extensiones de **VS Code**. Hoy se puede enviar un trabajo JCL y leer su
  salida desde un terminal de Linux o desde un pipeline de GitHub Actions. Eso ha cambiado de verdad
  la forma de trabajar.
- **DevOps sobre z/OS**: IBM Dependency Based Build y Git para los fuentes, con pipelines que
  construyen y despliegan en el mainframe igual que en cualquier otra plataforma.
- **JSON, REST y contenedores en z/OS**: z/OS Connect expone programas por lotes y transaccionales
  como APIs, y z/OS Container Extensions ejecuta contenedores Linux en la misma máquina.

## ⚙️ Cómo se ejecuta hoy

```text
# Desde ISPF/TSO en el propio mainframe: se edita el JCL y se teclea
SUBMIT

# Desde fuera, con Zowe CLI — así es como se hace hoy desde un portátil:
zowe jobs submit local-file "./totvta.jcl" --view-all-spool-content
zowe jobs list jobs --owner VLAD
```

**Para aprender sin acceso a un mainframe:** **IBM Z Xplore** ofrece un entorno gratuito con
ejercicios guiados; el emulador **Hercules** con **MVS 3.8j** (de dominio público) permite montar un
mainframe de los 70 en un portátil, con su JCL auténtico.

## 🧪 El programa de la clase 041… en JCL

> ⚠️ **Aquí el contrato cambia de naturaleza, y es justo el punto.** JCL **no puede** calcular el
> total de una venta: no tiene variables, ni aritmética, ni expresiones. Lo que hace es **compilar el
> programa COBOL de la clase 041, ejecutarlo, darle la entrada y recoger la salida**. Fingir un JCL
> que multiplica números sería inventar un lenguaje que no existe. **No se verifica en CI**: requiere
> z/OS.

```text
//TOTVTA   JOB (CONTAB),'TOTAL VENTA',CLASS=A,MSGCLASS=X,
//             NOTIFY=&SYSUID,REGION=0M
//*
//* ---------------------------------------------------------------
//* PASO 1 - COMPILAR Y ENLAZAR EL COBOL DE LA CLASE 041
//* ---------------------------------------------------------------
//COMPILA  EXEC IGYWCL
//COBOL.SYSIN    DD DSN=VLAD.FUENTE.COBOL(TOTVTA),DISP=SHR
//LKED.SYSLMOD   DD DSN=VLAD.LOADLIB(TOTVTA),DISP=SHR
//*
//* ---------------------------------------------------------------
//* PASO 2 - EJECUTARLO, SOLO SI EL PASO ANTERIOR FUE LIMPIO
//* ---------------------------------------------------------------
//EJECUTA  EXEC PGM=TOTVTA
//STEPLIB  DD DSN=VLAD.LOADLIB,DISP=SHR
//SYSOUT   DD SYSOUT=*
//SYSIN    DD *
15000 2 0.10
/*
//
```

Y con la sintaxis condicional moderna, que es como se escribe hoy:

```text
//  IF (COMPILA.LKED.RC <= 4) THEN
//EJECUTA  EXEC PGM=TOTVTA
//STEPLIB  DD DSN=VLAD.LOADLIB,DISP=SHR
//SYSOUT   DD SYSOUT=*
//SYSIN    DD *
15000 2 0.10
/*
//  ENDIF
```

**Recorrido, línea a línea.**

- `//TOTVTA JOB ...` — la sentencia **JOB**. `TOTVTA` es el nombre del trabajo (máximo 8 caracteres),
  `(CONTAB)` es la información de contabilidad —a quién se le imputa el consumo de CPU, porque en un
  mainframe **los recursos se facturan por departamento**—, `CLASS` define la cola de ejecución,
  `MSGCLASS` dónde va el registro, `NOTIFY=&SYSUID` avisa al usuario al terminar y `REGION=0M` pide
  memoria sin límite artificial.
- La **coma final** de la primera línea indica continuación; la siguiente empieza también por `//` y
  deja espacios antes del parámetro.
- `//*` es un comentario.
- `//COMPILA EXEC IGYWCL` — un **paso** llamado `COMPILA`. `IGYWCL` no es un programa: es un
  **procedimiento catalogado** de IBM que ya contiene los pasos de compilar (`COBOL`) y enlazar
  (`LKED`). Es reutilización de JCL: el equivalente a una *action* reutilizable de un pipeline.
- `//COBOL.SYSIN DD ...` — el punto en `COBOL.SYSIN` significa "la sentencia DD llamada `SYSIN`
  **dentro del paso `COBOL`** del procedimiento". Así se parametriza un procedimiento desde fuera:
  se sobrescriben sus DD.
- `DSN=VLAD.FUENTE.COBOL(TOTVTA)` — el nombre del *dataset*. Los conjuntos de datos de z/OS no forman
  un árbol de directorios: son **nombres jerárquicos de hasta 44 caracteres** en calificadores
  separados por puntos. Los paréntesis indican un **miembro** dentro de un dataset particionado (PDS),
  que es lo más parecido a una carpeta.
- `DISP=SHR` es la **disposición**: puede compartirse con otros trabajos. Las otras opciones —`OLD`
  (uso exclusivo), `NEW` (créalo), `MOD` (añade al final)— y la disposición **al terminar** (`CATLG`,
  `DELETE`, `KEEP`) son la mitad del oficio: describen qué pasa con el fichero si el trabajo va bien y
  si va mal.
- `//STEPLIB DD ...` indica dónde buscar el programa ejecutable. Es, literalmente, el `PATH` de ese
  paso.
- `//SYSOUT DD SYSOUT=*` envía la salida al *spool* del sistema, de donde se recoge después.
- **`//SYSIN DD *` es la clave de la conexión con la clase.** El asterisco significa "los datos vienen
  aquí mismo, en las líneas siguientes, hasta el `/*`". Ese es el `stdin` del programa: exactamente el
  `15000 2 0.10` del `casos.json` de la clase 041. El programa COBOL lo lee con `ACCEPT` sin saber que
  venía incrustado en el JCL, y mañana el mismo programa puede leerlo de un fichero de un millón de
  registros cambiando solo esta línea.
- `//` a solas cierra el trabajo.

**La lección, en una frase:** el programa declara *qué nombres lógicos usa*; el JCL decide *a qué
apuntan de verdad*, en el momento de ejecutar. Cuando en la
[Parte 9](../classes/parte-9-ingenieria-de-software-poliglota/README.md) se hable de configuración
externa y de entornos, este es el ejemplo más antiguo y más literal que existe.

## 🔍 Qué reconocer si vienes de otro mundo

| Si conoces… | En JCL es… |
|---|---|
| Un script de shell | El **JOB** completo |
| `command args` | `//PASO EXEC PGM=PROGRAMA,PARM='...'` |
| `< entrada.txt` | `//SYSIN DD DSN=...` o `//SYSIN DD *` con datos en línea |
| `> salida.txt` | `//SALIDA DD DSN=...,DISP=(NEW,CATLG)` |
| `$PATH` | `//STEPLIB DD DSN=...` |
| Variable de entorno | Parámetro simbólico (`&VAR`) y `// SET VAR=valor` |
| `cmd1 && cmd2` | `COND=` o `IF (PASO.RC = 0) THEN` |
| `needs:` de GitHub Actions | La secuencia de pasos con sus condiciones de código de retorno |
| Función reutilizable | **Procedimiento catalogado** (`PROC` … `PEND`) |
| Volumen de Docker | La sentencia **DD**: monta un recurso externo con un nombre lógico |
| `docker run --memory` | `REGION=` |

## ⚠️ Errores comunes al leerlo

- **La lógica invertida de `COND`.** `COND=(4,LT,PASO1)` significa "**omite** este paso si 4 es menor
  que el código de retorno de PASO1". Se lee al revés de lo que la intuición sugiere y ha causado más
  incidentes que ninguna otra construcción del lenguaje. Por eso existe `IF/THEN`.
- **Ignorar las columnas.** `//` en 1–2 sin excepción, y todo lo escrito a partir de la columna 73 se
  descarta en silencio. Un parámetro que "no se aplica" suele ser un parámetro que cruzó la columna 72.
- **Confundir un espacio con un separador cualquiera.** El espacio tras el campo de operandos
  **termina** los operandos; lo que venga después es comentario. Un espacio de más dentro de los
  parámetros corta la sentencia.
- **Creer que un dataset es un fichero de Unix.** Tiene formato de registro (`RECFM`), longitud de
  registro (`LRECL`) y tamaño de bloque declarados. Un `LRECL` equivocado no da un error bonito: da
  datos ilegibles.
- **Suponer que existe aritmética.** No la hay. Ni variables de usuario, ni bucles, ni expresiones. Si
  algo hay que calcular, lo calcula un programa y JCL decide qué hacer con su código de retorno.
- **Olvidar la disposición de fallo.** `DISP=(NEW,CATLG,DELETE)` significa: nuevo, catalógalo si va
  bien, **bórralo si falla**. Escribir `CATLG` en el tercer campo deja basura tras cada error y, en
  la siguiente ejecución, el dataset ya existe y el trabajo falla por otra razón.

## 📚 Fuentes y bibliografía

- [z/OS MVS JCL Reference (IBM)](https://www.ibm.com/docs/en/zos/3.1.0?topic=mvs-zos-jcl-reference) —
  la referencia completa de cada sentencia y parámetro.
- [z/OS MVS JCL User's Guide (IBM)](https://www.ibm.com/docs/en/zos/3.1.0?topic=mvs-zos-jcl-users-guide)
  — la guía con el porqué y los ejemplos.
- [IBM Z Xplore](https://www.ibmzxplore.com/) — entorno gratuito con ejercicios guiados sobre un z/OS
  real; la forma práctica de tocar JCL sin tener un mainframe.
- [Zowe](https://www.zowe.org/) — la CLI, las APIs REST y la extensión de VS Code que conectan z/OS
  con herramientas modernas.
- **Gary DeWard Brown**, *z/OS JCL*, 6.ª ed., Wiley — el libro de referencia sobre JCL desde hace
  décadas.
- **Mike Murach, Raul Menendez, Doug Lowe**, *Murach's OS/390 and z/OS JCL* — el manual didáctico, con
  el enfoque práctico del programador de aplicaciones.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [COBOL](cobol.md) · [PL/I](pl-i.md) · [RPG](rpg.md)
