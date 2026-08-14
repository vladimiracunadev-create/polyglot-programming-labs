# 🏢 RPG — 1959

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El lenguaje que factura.** Miles de empresas medianas —distribuidoras, fábricas, cadenas de
retail, cooperativas de crédito— llevan su ERP sobre IBM i, y ese ERP está escrito en RPG. Es el
sistema que nadie ve y que emite la factura.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: RPG se ejecuta hoy en decenas de miles de instalaciones de IBM i**, IBM
> mantiene el compilador ILE RPG, publica *Technology Refreshes* con novedades del lenguaje y hay
> un ecosistema de herramientas modernas (VS Code, Git, SQL embebido) creciendo alrededor.
>
> Entra porque **deja a la vista un concepto que ningún lenguaje del núcleo tiene**: el **ciclo del
> programa**, un bucle principal *implícito* que el propio runtime ejecuta por ti —lee un registro,
> procesa, escribe, repite— sin que aparezca un solo `while` en el código. Y un segundo concepto:
> **la base de datos como parte del lenguaje**, no como una biblioteca. Ver RPG obliga a preguntarse
> algo que en Python o Java nunca te planteas: *¿quién escribe el bucle principal de mi programa?*

| | |
|---|---|
| **Año** | 1959 (RPG); **RPG IV / ILE RPG** desde 1994; formato totalmente libre desde 2013 |
| **Autoría** | **IBM**, originalmente para el IBM 1401 |
| **Familia** | Negocios / generación de informes sobre datos |
| **Paradigma** | Imperativo con **ciclo implícito**; procedimental modular en ILE |
| **Tipado** | Estático y declarativo, con **decimal empaquetado** como tipo natural |
| **Memoria** | Estática; automática en procedimientos ILE |
| **Ejecución** | Compilado a objetos nativos de **IBM i** sobre Power |
| **Estado** | 🟢 **Legacy empresarial muy activo** — ERP, retail, logística, manufactura, banca |

---

## 📜 Historia

RPG nació en 1959 como *Report Program Generator*: no era un lenguaje de propósito general, era una
herramienta para describir informes. Le decías qué campos tenía la tarjeta perforada de entrada, qué
totales querías y cómo debía salir impreso, y él generaba el programa. La idea central —**declaras la
forma, no el bucle**— venía de que el trabajo real era siempre el mismo: recorrer un fichero, acumular
y romper por grupos.

De ahí sale el **ciclo del programa (*RPG cycle*)**, su rasgo más peculiar: el runtime lee el
siguiente registro, ejecuta tu lógica de detalle, comprueba los cambios de nivel de control, imprime
totales y vuelve a empezar. El programador rellenaba las especificaciones y el bucle lo ponía la
máquina. Es una idea sorprendentemente moderna —programación declarativa, inversión de control— con
sesenta años encima.

La evolución fue larga: **RPG II** (1969), **RPG III** (1978, con el System/38 y su base de datos
integrada), **RPG/400** (AS/400, 1988) y **RPG IV** (1994), que trajo el **ILE** (*Integrated
Language Environment*): procedimientos con parámetros, prototipos, módulos enlazables y llamadas
entre lenguajes. En **2001** llegó el formato libre parcial (`/FREE`) para la lógica de cálculo, y
en **2013** el formato **totalmente libre** (`**FREE`), que eliminó por fin las columnas.

El resultado es un lenguaje con dos caras muy distintas. El RPG de 1985 es un cuadrícula de columnas
ilegible para un ojo moderno. El RPG libre de 2013 en adelante se parece bastante a un Pascal con
tipos decimales.

## 🏭 Dónde sobrevive hoy

- **ERP a medida** en distribución, manufactura y mayoristas — muchísimo software vertical que nunca
  se empaquetó ni se vendió, escrito en casa a lo largo de treinta años.
- **Retail y logística**: gestión de inventario, pedidos, almacén, facturación.
- **Banca y cooperativas de crédito**, sobre todo de tamaño medio.
- **Administración y seguros** de escala regional.

La plataforma es **IBM i** (antes AS/400, iSeries, System i) sobre hardware **Power**. Es un sistema
operativo con una propiedad rara: la compatibilidad binaria hacia atrás es casi total, de modo que un
objeto compilado en un AS/400 de 1990 se ejecuta en un Power actual. Esa es, literalmente, la razón
comercial de que RPG siga vivo.

## 🧠 Por qué no ha muerto

**1. La base de datos es el sistema operativo.** En IBM i, **Db2 for i** no es un servicio que
instalas: es parte del sistema. Un programa RPG declara un fichero y sus campos aparecen como
variables del programa. No hay ORM, no hay cadena de conexión, no hay serialización. La distancia
entre "el registro en disco" y "la variable en memoria" es cero.

**2. Compatibilidad binaria de décadas.** IBM i separa el programa de la máquina mediante una capa de
abstracción (*TIMI*). Cuando IBM cambió de procesador CISC a Power en los 90, los objetos de los
clientes siguieron funcionando tras un simple guardar/restaurar. Un sistema que nunca te obliga a
migrar es un sistema del que nunca migras.

**3. Decimal empaquetado nativo.** Igual que [COBOL](cobol.md): `packed(11:2)` es aritmética decimal
exacta, no punto flotante. Para facturar, es el tipo correcto.

**4. Sigue recibiendo funcionalidad.** SQL embebido, servicios web REST, JSON con `DATA-INTO` y
`DATA-GEN`, integración con Git y VS Code. RPG moderno consume una API REST y devuelve JSON sin salir
del lenguaje.

**5. El conocimiento del negocio está dentro.** El mismo argumento que en COBOL, con un agravante: en
IBM i mucho de ese software es **artesanal y único de cada empresa**, sin proveedor al que pedir la
versión nueva.

## 🔄 Lo que se ha modernizado

RPG es de los casos más llamativos: un lenguaje de 1959 al que se le ha añadido, en los últimos
quince años, casi todo lo que hace falta para un backend actual.

- **Formato totalmente libre** (`**FREE`, 2013): desaparecen las columnas. El RPG que se escribe hoy
  se parece más a Pascal que a una hoja de cálculo.
- **JSON y XML con `DATA-INTO` y `DATA-GEN`**: sentencias del lenguaje que convierten un documento
  JSON en una estructura de datos RPG y al revés. Consumir una API REST desde RPG es hoy tarea de
  media pantalla de código.
- **SQL embebido** (`exec sql`): el acceso a datos moderno en IBM i es SQL escrito dentro del RPG, con
  las variables del programa como parámetros. Y **IBM i Services** expone el propio sistema operativo
  —trabajos, usuarios, ficheros IFS, red— como **vistas SQL** consultables.
- **Servicios web en las dos direcciones**: `HTTPAPI`, las funciones `SYSTOOLS` y el motor
  **IWS** (*Integrated Web Services*) permiten publicar un programa RPG como API REST o consumir una
  externa.
- **`ctl-opt` y procedimientos con prototipos** desde ILE: ámbito local, parámetros con tipo,
  módulos enlazables y llamadas entre RPG, C, COBOL y Java en el mismo programa.
- **Git, VS Code y CI**: la extensión **Code for IBM i** y el constructor **`bob`** trajeron control de
  versiones, revisión de código y construcción reproducible a una plataforma que durante décadas
  guardó los fuentes en miembros de ficheros físicos.
- **Node.js, Python y PHP corren en IBM i**, de modo que lo habitual hoy es un frontend moderno
  llamando a lógica RPG a través de una API.

## ⚙️ Cómo se ejecuta hoy

RPG **solo** se ejecuta sobre IBM i: no hay compilador libre para Linux ni para Windows. Esto es
importante y conviene decirlo sin rodeos — es el lenguaje de esta lista con la barrera de entrada más
alta.

```text
# Desde una línea de comandos de IBM i (CL):
CRTBNDRPG PGM(MILIB/TOTVTA) SRCSTMF('/home/vlad/totvta.rpgle') DFTACTGRP(*NO)
CALL PGM(MILIB/TOTVTA) PARM('15000' '2' '0.10')
```

**Herramientas actuales.** **RDi** (*Rational Developer for i*, basado en Eclipse) es el IDE
comercial clásico; **Code for IBM i**, la extensión de VS Code, es hoy la vía moderna y gratuita —
edita, compila y depura contra un IBM i remoto. **`bob`** (*Better Object Builder*) da construcción
reproducible con Git.

**Para practicar sin un IBM i propio:** los programas de acceso público de IBM
([IBM i Developer / Tech Refresh sandboxes](https://www.ibm.com/products/ibm-i)) o una cuenta en un
proveedor de *cloud* IBM i. No hay atajo local.

## 🧪 El programa de la clase 041 en RPG

> ⚠️ **Contrato adaptado, y declarado.** En IBM i un programa no recibe sus datos por `stdin`: los
> recibe por **parámetros**, por un **fichero de base de datos** o por una **pantalla**. Mantener
> aquí la ficción de `stdin` sería falsear el lenguaje. Así que el contrato es el mismo —tres
> valores de entrada, un total con dos decimales de salida— pero la entrada llega como parámetros.
> Este código **no se verifica en CI**: no hay compilador RPG en los *runners*.

```rpgle
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi TOTVTA;
  precio    packed(11:2) const;
  cantidad  packed(11:2) const;
  descuento packed(5:4)  const;
end-pi;

dcl-s total  packed(15:2);
dcl-s salida char(40);

total = precio * cantidad * (1 - descuento);

salida = 'Total: ' + %char(total);
dsply salida;

*inlr = *on;
return;
```

**Recorrido, línea a línea.**

- `**free` en la primera línea, columna 1, declara el fuente en **formato totalmente libre**. Sin esa
  marca, el compilador vuelve al formato de columnas de 1959.
- `ctl-opt` son las opciones de control del programa. `dftactgrp(*no)` es obligatorio para compilar
  como ILE moderno y no como RPG/400 heredado; es la línea que todo el mundo olvida y que produce el
  primer error de compilación de cualquiera que empieza.
- `dcl-pi TOTVTA ... end-pi` es la **interfaz de programa**: los parámetros que recibe. `const`
  indica que no se modifican, lo que además permite pasar expresiones y no solo variables.
- `packed(11:2)` es **decimal empaquetado**: 11 dígitos en total, 2 de ellos decimales. Cada dígito
  ocupa medio byte. Es el tipo con el que se factura, y la razón es la misma que en COBOL: la
  aritmética es decimal, no binaria.
- `%char(total)` convierte el decimal a su representación en texto sin ceros a la izquierda. Es una
  **función incorporada** (*built-in*): las de RPG empiezan por `%` y hay decenas (`%trim`, `%scan`,
  `%subst`, `%date`).
- `dsply` muestra un mensaje. En un programa real la salida iría a una pantalla (fichero de display),
  a un informe o a un fichero; `dsply` es el equivalente al `print` de depuración.
- **`*inlr = *on` es la línea que hay que entender.** `*INLR` es el **indicador de último registro**.
  Ponerlo a `*ON` le dice al **ciclo del programa** que este es el final: cierra los ficheros, libera
  el almacenamiento y termina. Si se omite, el programa **queda residente en memoria** con sus
  variables intactas y la siguiente llamada continúa donde quedó. Es una fuente inagotable de errores
  fantasma para quien viene de otros lenguajes, y es la huella visible de que aquí el bucle principal
  no lo escribes tú.

**Y así se veía en formato fijo**, que es como está la mayor parte del código en producción:

```text
     H DFTACTGRP(*NO)
     D TOTVTA          PR
     D   precio                      11P 2 CONST
     D   cantidad                    11P 2 CONST
     D   descuento                    5P 4 CONST
     D total           S             15P 2
      /FREE
        total = precio * cantidad * (1 - descuento);
        *inlr = *on;
      /END-FREE
```

La letra de la columna 6 decide qué es cada línea: **H** de control, **F** de ficheros, **D** de
definiciones, **C** de cálculo, **O** de salida. Ese carácter es todo el "parser" del RPG clásico.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En RPG libre es… |
|---|---|
| `int x;` / `decimal x;` | `dcl-s x packed(11:2);` |
| `const` | `const` en la interfaz, o `dcl-c` para una constante nombrada |
| Firma de función | `dcl-pr` (prototipo) y `dcl-pi` (interfaz) |
| `struct` | `dcl-ds` — estructura de datos, con solapamiento de campos incluido |
| `if / else` | `if ... elseif ... else ... endif;` |
| `for` | `for i = 1 to n; ... endfor;` |
| `x.substring(a, b)` | `%subst(x : a : b)` |
| `SELECT ... FROM` | `exec sql select ... into :variable from tabla;` — SQL **dentro** del RPG |
| El bucle principal | **No lo escribes**: lo pone el ciclo del programa |

## ⚠️ Errores comunes al leerlo

- **Olvidar `*inlr = *on`.** El programa no termina de verdad; se queda residente y la siguiente
  llamada arranca con el estado anterior.
- **Confundir `packed` con `float`.** `packed(11:2)` es exacto. `float(8)` existe, pero usarlo para
  dinero en RPG sería tan erróneo como en cualquier otro sitio.
- **Suponer ámbito local.** En RPG clásico todas las variables son globales al programa. Solo los
  **procedimientos** de ILE (`dcl-proc`) introducen variables locales de verdad.
- **Leer los indicadores como booleanos normales.** `*IN01` … `*IN99` son variables globales
  numeradas heredadas del ciclo, y el código antiguo las usa para todo. Un `*IN15` sin comentario
  puede significar cualquier cosa; es la deuda técnica característica del lenguaje.
- **Creer que un fuente `.rpgle` es RPG libre.** La extensión no lo determina: lo determina `**free`
  en la columna 1 de la primera línea.

## 📚 Fuentes y bibliografía

- [IBM i — documentación de ILE RPG](https://www.ibm.com/docs/en/i/7.5?topic=languages-ile-rpg) —
  referencia del lenguaje y guía del programador, versión vigente.
- [Code for IBM i](https://codefori.github.io/docs/) — la cadena de herramientas moderna sobre VS Code.
- [RPG Café (IBM)](https://www.ibm.com/support/pages/rpg-cafe) — dónde IBM publica las novedades del
  lenguaje en cada *Technology Refresh*.
- **Jim Buck, Bryan Meyers, Dan Cruikshank**, *Programming in ILE RPG*, 5.ª ed., MC Press — el manual
  de referencia del RPG moderno.
- **Jim Martin**, *Free-Format RPG IV*, MC Press — específicamente sobre el paso del formato de
  columnas al libre, que es el problema real de cualquiera que herede código RPG.
- **Scott Klement**, artículos y bibliotecas de código abierto para IBM i — la referencia práctica de
  la comunidad para HTTP, JSON y cifrado desde RPG.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [COBOL](cobol.md) · [PL/I](pl-i.md) · [JCL](jcl.md)
