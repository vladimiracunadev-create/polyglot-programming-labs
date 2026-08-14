# 🏛️ COBOL — 1959

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El lenguaje que mueve el dinero.** Si esta madrugada te cobraron una tarjeta, se liquidó una
nómina o se calculó una prima de seguro, es probable que una máquina IBM Z ejecutara COBOL para
hacerlo. No es una curiosidad de museo: es infraestructura crítica en producción.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: COBOL se ejecuta hoy, en producción, con dinero real encima.** No entra
> por nostalgia ni por capricho histórico; entra porque sigue vivo en banca, seguros, medios de pago
> y administración pública, e IBM sigue vendiendo y actualizando su compilador.
>
> Y entra, sobre todo, porque **deja a la vista un concepto que el núcleo esconde**: la
> **aritmética decimal exacta** y la **declaración explícita de la forma del dato**. En Python
> escribes `0.1 + 0.2` y obtienes `0.30000000000000004` sin que nada te avise; en COBOL el tipo
> `PIC 9(9)V99 COMP-3` te obliga a decidir, antes de calcular, cuántos dígitos y cuántos decimales
> tiene el dinero. Ver el mismo cálculo en los dos sitios es lo que convierte "usa `Decimal` para
> dinero" de receta memorizada en comprensión.

| | |
|---|---|
| **Año** | 1959 (especificación); primeros compiladores en 1960 |
| **Autoría** | Comité **CODASYL**, con Grace Hopper como influencia decisiva vía FLOW-MATIC |
| **Familia** | Negocios / procesamiento de datos por lotes |
| **Paradigma** | Imperativo y procedimental; OO opcional desde COBOL 2002 |
| **Tipado** | Estático, declarativo por **plantilla de imagen** (`PICTURE`) |
| **Memoria** | Estática por defecto — el `WORKING-STORAGE` se dimensiona al compilar |
| **Ejecución** | Compilado a nativo (z/OS, AIX, Linux, Windows) |
| **Estado** | 🟢 **Muy vivo en legacy empresarial** — banca, seguros, gobierno, pensiones, tarjetas |

---

## 📜 Historia

En 1959 el Departamento de Defensa de Estados Unidos convocó en el Pentágono a fabricantes y
usuarios para atacar un problema concreto: cada máquina tenía su propio lenguaje y un programa de
nóminas escrito para un UNIVAC no servía en un IBM. De esa reunión nació el comité **CODASYL**
(*Conference on Data Systems Languages*) y, en pocos meses, la especificación de **COBOL**
(*COmmon Business-Oriented Language*).

La decisión de diseño que lo define se tomó ahí: el lenguaje debía poder ser **leído por alguien que
no fuera programador**. De ahí la sintaxis en inglés casi narrativo — `ADD IVA TO TOTAL GIVING
TOTAL-CON-IVA` — que hoy nos parece verbosa y que entonces era una apuesta deliberada por la
auditabilidad. El trabajo previo de **Grace Hopper** en FLOW-MATIC, el primer lenguaje con
instrucciones en inglés, es el antecedente directo.

La otra decisión estructural fue separar el programa en **cuatro divisiones**: `IDENTIFICATION`
(quién es), `ENVIRONMENT` (en qué máquina y con qué ficheros corre), `DATA` (la forma exacta de
cada dato) y `PROCEDURE` (qué se hace). Esa separación entre **la forma del dato y el proceso** es
la razón de que un COBOL de 1975 siga siendo legible: el `DATA DIVISION` es, en la práctica, un
esquema documentado del negocio.

Los estándares posteriores fueron acumulando: **COBOL-68** y **74** consolidaron el lenguaje;
**COBOL-85** trajo la programación estructurada de verdad (`END-IF`, `EVALUATE`, `PERFORM ... UNTIL`)
y permitió por fin escribir COBOL sin `GO TO`; **COBOL 2002** añadió orientación a objetos y formato
libre; **2014** y **2023** siguen puliendo. El lenguaje no se congeló en los 60: se congeló su
reputación.

## 🏭 Dónde sobrevive hoy

- **Banca central y comercial**: sistemas de cuentas, liquidación interbancaria, compensación.
- **Medios de pago**: autorización y liquidación de tarjetas, procesamiento nocturno de lotes.
- **Seguros**: cálculo de primas, siniestros, reservas actuariales.
- **Gobierno y pensiones**: seguridad social, recaudación fiscal, padrones.
- **Logística y retail** de gran escala, sobre mainframe IBM Z con CICS, IMS y Db2.

Lo típico no es un programa COBOL suelto, sino un **ecosistema**: el COBOL contiene la regla de
negocio, [JCL](jcl.md) orquesta la ejecución por lotes, **CICS** le da la cara transaccional en
línea y **Db2** guarda los datos. Estudiar COBOL sin ver ese entorno es como estudiar JavaScript sin
un navegador.

## 🧠 Por qué no ha muerto

Hay una respuesta perezosa —"porque migrar cuesta caro"— y una respuesta técnica, que es la
interesante.

**1. Aritmética decimal exacta.** COBOL no calcula dinero en punto flotante binario. Su tipo natural
es el **decimal empaquetado** (`COMP-3`): cada dígito decimal se guarda en medio byte, y las
operaciones son decimales, no binarias. En Python o JavaScript, `0.1 + 0.2` no da `0.3`; en COBOL con
`PIC 9(9)V99` da exactamente lo que un contable espera. Los lenguajes modernos han tenido que
**añadir** ese tipo después (`BigDecimal` en Java, `decimal` en C#, `numeric` en SQL). COBOL nació
con él porque nació para eso.

**2. El `PICTURE` es un contrato de datos.** `PIC S9(7)V99 COMP-3` declara a la vez el signo, los
dígitos enteros, los decimales y la representación física en disco. Un fichero de 40 años se sigue
leyendo porque su forma está escrita en el programa, no en una convención perdida.

**3. Décadas de reglas de negocio validadas.** El valor no está en el código: está en los casos
límite que ese código ya resolvió. El tratamiento de un año bisiesto en un cálculo de intereses, la
excepción de un producto retirado en 1994 que aún tiene clientes. Reescribirlo no es traducir
sintaxis, es **redescubrir requisitos que nadie documentó**.

**4. El coste del fallo es asimétrico.** Un error en un microservicio de recomendaciones es una
métrica peor. Un error en la liquidación nocturna de un banco es un incidente regulatorio.

> **Honestidad sobre las cifras.** Circulan estimaciones muy citadas —"800 000 millones de líneas de
> COBOL en producción"— que provienen de informes de la industria y no de un censo verificable.
> Tómalas como orden de magnitud, no como dato. Lo verificable es que
> [IBM sigue desarrollando y vendiendo compiladores COBOL](https://www.ibm.com/products/cobol-compilers)
> y publicando documentación actual para z/OS.

## 🔄 Lo que se ha modernizado

Conviene decirlo con claridad, porque es lo que casi nadie cuenta: **COBOL no se quedó en 1985.** El
estándar y los compiladores han incorporado lo necesario para resolver problemas actuales:

- **JSON y XML nativos.** `JSON GENERATE` y `JSON PARSE` (y sus equivalentes `XML GENERATE`/`XML
  PARSE`) son **sentencias del lenguaje**. Un programa COBOL serializa una estructura de datos a JSON
  sin biblioteca externa. Es exactamente lo que hace falta para hablar con una API.
- **Servicios REST en las dos direcciones.** Con **z/OS Connect**, un programa COBOL existente se
  expone como API REST sin tocarlo, y también puede **consumir** APIs externas. El mainframe dejó de
  ser una isla por lotes.
- **Unicode.** El tipo `NATIONAL` (`PIC N`) maneja UTF-16; el COBOL de los 80 solo entendía EBCDIC.
- **Orientación a objetos** (COBOL 2002) y **formato libre**, que elimina las columnas heredadas de
  la tarjeta perforada.
- **COBOL fuera del mainframe.** Micro Focus/OpenText Visual COBOL compila a **.NET** y a la **JVM**,
  de modo que el mismo código de negocio se ejecuta en un contenedor Linux o en Azure.
- **Herramientas actuales**: depuración desde **VS Code** (extensiones IBM Z Open Editor y COBOL de
  Micro Focus), Git, pipelines de CI/CD sobre z/OS, y asistentes de IA para traducir COBOL a Java.
- **Pruebas unitarias** con marcos como **zUnit** o **GnuCOBOL + cobol-check**: el COBOL también
  entró en la disciplina de las pruebas automatizadas.

## ⚙️ Cómo se ejecuta hoy

**En producción:** *IBM Enterprise COBOL for z/OS* (compilador de pago, integrado con CICS/Db2/IMS)
y *Micro Focus / OpenText Visual COBOL* (COBOL sobre Linux, Windows, .NET y JVM).

**Para aprender, gratis:** **GnuCOBOL**, que traduce COBOL a C y lo compila con el compilador de C
del sistema.

```bash
# Debian / Ubuntu
sudo apt-get install -y gnucobol

# Compilar a ejecutable, en formato libre (sin las columnas históricas)
cobc -x -free total.cob -o total

echo "15000 2 0.10" | ./total
# Total: 27000.00
```

**Formato fijo vs. formato libre.** El COBOL histórico hereda la **tarjeta perforada de 80
columnas**: las columnas 1–6 eran el número de secuencia, la 7 el indicador (un `*` ahí es un
comentario, un `-` es continuación), las 8–11 el "Área A" donde van las divisiones y los niveles
`01`, las 12–72 el "Área B" con las sentencias, y las 73–80 la identificación del programa. Ese
formato sigue siendo el de la mayoría del código en producción. El **formato libre** (`-free`) lo
elimina y es lo que verás en material nuevo. Si abres un fuente real y todo parece indentado de
forma extraña, no es estilo: son columnas.

## 🧪 El programa de la clase 041 en COBOL

Mismo contrato que en toda la [clase 041](../classes/parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md):
leer `precio cantidad descuento` de una línea y escribir `Total: <total con 2 decimales>`.

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. TOTAL-VENTA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA           PIC X(80).
01  TXT-PRECIO      PIC X(20).
01  TXT-CANTIDAD    PIC X(20).
01  TXT-DESCUENTO   PIC X(20).
01  PRECIO          PIC 9(9)V99   COMP-3.
01  CANTIDAD        PIC 9(9)V99   COMP-3.
01  DESCUENTO       PIC 9V9(4)    COMP-3.
01  TOTAL-CALC      PIC 9(12)V99  COMP-3.
01  TOTAL-EDITADO   PIC ZZZZZZZZZ9.99.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO TXT-PRECIO TXT-CANTIDAD TXT-DESCUENTO
    END-UNSTRING
    MOVE FUNCTION NUMVAL(TXT-PRECIO)    TO PRECIO
    MOVE FUNCTION NUMVAL(TXT-CANTIDAD)  TO CANTIDAD
    MOVE FUNCTION NUMVAL(TXT-DESCUENTO) TO DESCUENTO
    COMPUTE TOTAL-CALC ROUNDED = PRECIO * CANTIDAD * (1 - DESCUENTO)
    MOVE TOTAL-CALC TO TOTAL-EDITADO
    DISPLAY "Total: " FUNCTION TRIM(TOTAL-EDITADO)
    STOP RUN.
```

**Recorrido, línea a línea.**

- `PROGRAM-ID` es la identidad del módulo; en un mainframe ese nombre es también el del miembro en
  la librería de carga, y por eso suele estar limitado a 8 caracteres.
- Todas las variables se declaran en `WORKING-STORAGE`, **antes** de cualquier sentencia. No existe
  "declarar donde se usa": el `DATA DIVISION` es el inventario completo de la memoria del programa.
  Esa rigidez es la que hace que se pueda auditar un COBOL sin ejecutarlo.
- El nivel `01` marca un elemento de primer orden. Los niveles `05`, `10`… anidan campos dentro de
  una estructura, que es como COBOL representa un registro de fichero.
- `PIC 9(9)V99` se lee literalmente como una plantilla: nueve dígitos, una **coma decimal implícita**
  (`V` no ocupa espacio, solo dice dónde está el punto) y dos decimales. `COMP-3` pide que se guarde
  como decimal empaquetado. Nada de esto es float.
- `ACCEPT LINEA` lee una línea de la entrada estándar y la deja rellenada con espacios hasta 80.
- `UNSTRING ... DELIMITED BY ALL SPACES` es el `split` de COBOL: parte la línea por rachas de
  espacios y reparte los trozos en los tres campos de texto. `ALL` es lo que colapsa espacios
  consecutivos; sin él, dos espacios seguidos producirían un campo vacío.
- `FUNCTION NUMVAL` convierte el texto a número. Es una **función intrínseca**, incorporada al
  estándar en COBOL-85; antes había que escribir la conversión a mano.
- `COMPUTE ... ROUNDED` es la única forma de escribir una expresión aritmética completa; las formas
  verbales (`MULTIPLY A BY B GIVING C`) son las originales. `ROUNDED` aplica redondeo comercial al
  guardar en los dos decimales del destino, y es explícito **a propósito**: en dinero, redondear en
  silencio es un defecto.
- `TOTAL-EDITADO` con `PIC ZZZZZZZZZ9.99` es un **campo editado para presentación**: cada `Z`
  suprime un cero a la izquierda y lo sustituye por espacio, el `9` final garantiza que un total de
  cero se imprima como `0.00` y no como una cadena vacía. `FUNCTION TRIM` quita el relleno.

Fíjate en lo que **no** hay: ni tipo inferido, ni conversión implícita, ni formateo con
`printf`. Cada transformación —texto a número, número a texto presentable— está escrita.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En COBOL es… |
|---|---|
| `x = 3` | `MOVE 3 TO X` — mover, no asignar; el verbo es deliberado |
| `total = a * b` | `COMPUTE TOTAL = A * B` |
| `const IVA = 0.19` | `01 IVA PIC 9V99 VALUE 0.19.` (y `CONSTANT` desde COBOL 2002) |
| `if/else if/else` | `EVALUATE ... WHEN ... WHEN OTHER ... END-EVALUATE` |
| `for` / `while` | `PERFORM VARYING I FROM 1 BY 1 UNTIL I > N` |
| Función | `PERFORM PARRAFO` (sección de código) o `CALL "SUBPROG" USING ...` |
| `struct` / registro | Niveles anidados `01 / 05 / 10` |
| `decimal` / `BigDecimal` | `PIC 9(9)V99 COMP-3` — nativo, no una librería |
| `split(línea)` | `UNSTRING` |
| `"%.2f" % x` | Un campo `PIC ZZZ9.99` al que se mueve el valor |

## ⚠️ Errores comunes al leerlo

- **Confundir `V` con un punto.** `PIC 9(5)V99` ocupa 7 dígitos, no 8: la coma decimal es implícita
  y no existe en memoria. Un `PIC 9(5).99` sí imprime el punto, pero ya es un campo de presentación.
- **Creer que la indentación es estilo.** En formato fijo, mover una línea dos columnas puede sacarla
  del Área B y romper la compilación.
- **Leer `PERFORM` como una llamada a función.** `PERFORM` ejecuta un párrafo y vuelve, pero no crea
  ámbito ni recibe parámetros: todas las variables son globales al programa. Es la fuente número uno
  de sorpresas para quien viene de un lenguaje con funciones de verdad.
- **Asumir recursión.** El COBOL clásico no la permite: el `WORKING-STORAGE` es estático. Hace falta
  declarar el programa `RECURSIVE` (COBOL 2002) o usar `LOCAL-STORAGE`.
- **Ignorar el punto final.** El `.` cierra sentencias y, en el COBOL antiguo, delimita el alcance de
  un `IF`. Un punto de más dentro de un `IF` cambia el flujo del programa sin dar error.

## 📚 Fuentes y bibliografía

- [IBM COBOL compilers](https://www.ibm.com/products/cobol-compilers) — familia de compiladores
  vigente para z/OS, AIX y Linux on Z.
- [IBM Enterprise COBOL for z/OS — documentación](https://www.ibm.com/docs/en/cobol-zos) — referencia
  del lenguaje y guía de programación.
- [GnuCOBOL](https://gnucobol.sourceforge.io/) — implementación libre, la que puedes instalar hoy.
- **Michael Coughlan**, *Beginning COBOL for Programmers*, Apress, 2014 — la entrada correcta si ya
  programas en otro lenguaje: asume que sabes programar y explica solo lo que COBOL hace distinto.
- **Mike Murach, Anne Prince, Raul Menendez**, *Murach's Mainframe COBOL* — el manual de referencia
  del COBOL empresarial con CICS, VSAM y Db2.
- **Gary DeWard Brown**, *z/OS JCL*, Wiley — porque el COBOL de producción no se ejecuta solo; ver
  también la ficha de [JCL](jcl.md).

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [PL/I](pl-i.md) · [RPG](rpg.md) · [JCL](jcl.md)
