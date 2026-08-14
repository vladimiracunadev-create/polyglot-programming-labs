# 🏥 M / MUMPS — 1966

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El lenguaje de tu historia clínica.** Si te han atendido en un hospital grande, es muy probable que
tu expediente viva en una base de datos MUMPS. Es un lenguaje de 1966 que sostiene una parte enorme
de la sanidad mundial y que casi nadie fuera de ese sector ha visto nunca.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: M se ejecuta hoy en los sistemas de información clínica más grandes del
> mundo.** VistA, el sistema del Departamento de Veteranos de EE. UU., tiene componentes escritos en
> M y su documentación oficial lo declara. InterSystems (IRIS, antes Caché) y YottaDB son productos
> vivos y en desarrollo activo, no arqueología.
>
> Entra porque **encarna una idea que ningún lenguaje del núcleo tiene**: **el lenguaje y la base de
> datos son la misma cosa**. En M no existe un ORM, ni un driver, ni una conexión, ni un `COMMIT`
> obligatorio para guardar. Escribes `set ^VENTAS(id)=total` y eso **ya está en disco**, con la misma
> sintaxis con la que escribirías una variable local. Todo lo que en el núcleo se estudia como
> "persistencia" —serialización, mapeo objeto-relacional, capas de acceso a datos— aquí simplemente
> **no existe como problema**. Ver eso una vez cambia la forma de mirar cualquier ORM.

| | |
|---|---|
| **Año** | 1966; primer estándar ANSI en 1977; ISO/IEC 11756 |
| **Autoría** | **Neil Pappalardo**, Robert Greenes y Curt Marble, Massachusetts General Hospital |
| **Familia** | Lenguajes de base de datos / sanidad |
| **Paradigma** | Imperativo y procedimental, con persistencia integrada |
| **Tipado** | **Dinámico y sin tipos**: todo es una cadena que se interpreta según el uso |
| **Memoria** | Gestionada; los datos persistentes viven en árboles en disco |
| **Ejecución** | Interpretado / compilado a bytecode según la implementación |
| **Estado** | 🟡 **Muy especializado y difícil de sustituir** — sanidad, algo de finanzas |

---

## 📜 Historia

En 1966, en el laboratorio de computación del **Massachusetts General Hospital**, un equipo dirigido
por Neil Pappalardo necesitaba algo que no existía: un sistema en el que varios terminales pudieran
consultar y actualizar historiales de pacientes **a la vez**, sobre un PDP-7 con memoria ridícula
para los estándares actuales. Las bases de datos comerciales de la época eran caras, rígidas y
pensadas para lotes, no para consultas interactivas de datos muy irregulares.

La solución fue radical: hacer que **el lenguaje incorporara el almacenamiento**. Nació **MUMPS**
(*Massachusetts General Hospital Utility Multi-Programming System*), luego estandarizado
simplemente como **M**.

Su estructura de datos única es el **array disperso multidimensional**. Un array de M no tiene
tamaño ni índices numéricos obligatorios: las claves pueden ser números o texto, y solo existen los
nodos que has creado. Y aquí está la idea decisiva: si el nombre del array empieza por `^`, **es
persistente**. `PACIENTE("nombre")` vive en memoria y desaparece; `^PACIENTE(1234,"nombre")` está en
disco, es transaccional y lo ven todos los procesos. Misma sintaxis, dos mundos.

El otro rasgo llamativo es la **brevedad extrema**. En 1966 la memoria se contaba en kilobytes y cada
carácter del programa fuente ocupaba espacio, así que todos los comandos admiten abreviatura a una
letra: `S` por `SET`, `W` por `WRITE`, `I` por `IF`, `F` por `FOR`, `Q` por `QUIT`, `D` por `DO`. El
código real de producción está escrito así, y para un ojo no entrenado resulta casi ilegible.

## 🏭 Dónde sobrevive hoy

- **Historia clínica electrónica**: **Epic Systems**, el sistema de historia clínica de mayor cuota
  en los hospitales de Estados Unidos, se construye sobre tecnología InterSystems (Caché/IRIS), cuyo
  motor de datos y lenguaje descienden directamente de M. **MEDITECH** también viene de esta familia.
- **VistA**, el sistema del Departamento de Asuntos de Veteranos de EE. UU. — uno de los despliegues
  de software sanitario más grandes del mundo, con código abierto y componentes en M.
- **Laboratorios y sistemas departamentales** hospitalarios.
- **Sector financiero**: algunos sistemas de banca y trading europeos sobre Caché/IRIS, por la misma
  razón que la sanidad — rendimiento en escrituras y esquemas irregulares.

**Descendiente moderno:** **InterSystems ObjectScript**, que añade orientación a objetos, SQL y
persistencia de clases sobre el mismo motor de *globals*. Un desarrollador de IRIS trabaja hoy en
ObjectScript, pero el `^global` sigue estando debajo.

## 🧠 Por qué no ha muerto

**1. El modelo de datos encaja con la medicina.** Un historial clínico es irregular por naturaleza:
un paciente tiene tres alergias y otro ninguna; una consulta tiene quince campos y otra dos. En un
modelo relacional eso produce tablas anchas llenas de nulos o decenas de tablas de detalle. En M, un
árbol disperso guarda exactamente lo que hay. Es, en la práctica, una base de datos **jerárquica y
sin esquema** treinta años antes de que se acuñara "NoSQL".

**2. Latencia mínima.** No hay traducción entre el modelo del lenguaje y el del almacenamiento, ni
capa de red, ni parseo de SQL. Una escritura es una escritura. En sistemas con miles de terminales
concurrentes, eso se nota.

**3. Sustituirlo obliga a reescribir el hospital.** No es solo el código: es que las reglas clínicas,
los formularios, los protocolos y las integraciones están tejidos en esa base de datos. Y un fallo
en un sistema clínico tiene consecuencias directas sobre pacientes.

**4. Los productos están vivos.** InterSystems IRIS y YottaDB reciben versiones nuevas, soportan
contenedores, SQL sobre los mismos datos, APIs REST y FHIR. El lenguaje es viejo; la plataforma no.

## 🔄 Lo que se ha modernizado

El lenguaje apenas ha cambiado; **la plataforma se ha reinventado entera**, y esa es justo la
estrategia que lo mantiene vivo:

- **Enlaces para lenguajes actuales.** YottaDB expone sus *globals* a **C, Go, Python, Node.js, Rust,
  Perl y Java**. Puedes escribir la lógica nueva en Go y seguir leyendo y escribiendo el mismo árbol
  de datos que el código M de 1990. Es una estrategia de convivencia, no de migración.
- **Contenedores y nube.** Hay imágenes Docker oficiales de YottaDB e InterSystems IRIS; IRIS se
  despliega en Kubernetes con alta disponibilidad.
- **SQL sobre los mismos datos.** IRIS permite consultar con SQL estándar las estructuras persistentes
  y exponerlas por ODBC/JDBC, sin duplicar la información.
- **FHIR y HL7 nativos.** IRIS for Health implementa los estándares actuales de interoperabilidad
  sanitaria; es la razón principal de que la plataforma siga ganando contratos.
- **APIs REST y JSON** directamente desde el lenguaje, y un motor de aprendizaje automático
  (IntegratedML) que se invoca desde SQL.
- **ObjectScript** añadió clases, herencia, excepciones estructuradas y persistencia de objetos sobre
  el mismo motor. Un desarrollador de IRIS de 2026 rara vez escribe M puro, pero el `^global` sigue
  debajo de todo.

## ⚙️ Cómo se ejecuta hoy

```bash
# YottaDB: implementación libre de M, con paquetes .deb/.rpm y contenedor oficial
docker run --rm -it yottadb/yottadb-debian:latest

# Dentro del contenedor, el shell directo del lenguaje:
$ydb_dist/yottadb -direct
YDB> write "hola",!
```

**Implementaciones actuales:** **YottaDB** (libre, derivada de GT.M, con enlaces para C, Go, Python,
Node.js, Rust y Perl), **GT.M** (FIS), e **InterSystems IRIS** (comercial, con ObjectScript, SQL,
analítica e interoperabilidad FHIR). Para trastear con VistA existen distribuciones empaquetadas de
la comunidad.

## 🧪 El programa de la clase 041 en M

> ⚠️ **Material de lectura, no verificado.** No hay intérprete M en los *runners* de CI.

```mumps
TOTVTA ; Total de una venta -- clase 041
 read linea
 set precio    = $piece(linea, " ", 1)
 set cantidad  = $piece(linea, " ", 2)
 set descuento = $piece(linea, " ", 3)
 set total     = precio * cantidad * (1 - descuento)
 write "Total: ", $justify(total, 0, 2), !
 quit
```

**Recorrido, línea a línea.**

- La **primera columna es sagrada.** Una etiqueta (`TOTVTA`) empieza en la columna 1; **toda línea de
  código debe empezar con al menos un espacio**. Es la regla que más rompe quien empieza, y no da un
  error claro: el intérprete cree que estás definiendo una etiqueta.
- `;` inicia un comentario.
- `read linea` lee de la entrada. En M la E/S va contra un **dispositivo actual**, y `use` cambia cuál
  es; no hay una noción separada de "entrada estándar".
- `$piece(cadena, delimitador, n)` —abreviado `$P`— es la función más usada del lenguaje: devuelve el
  trozo *n* de una cadena partida por un delimitador. **No hay listas ni arrays de resultado**: en M
  la cadena delimitada *es* la estructura de datos ligera, y `$piece` es cómo se accede a ella. Verás
  registros enteros guardados como `"Pérez^María^1978-04-12^O+"` y accedidos con `$P(dato,"^",3)`.
- `$justify(valor, ancho, decimales)` —abreviado `$J`— formatea con decimales y justifica a la
  derecha. Con ancho `0` no añade relleno, así que da exactamente `27000.00`. Es el `printf("%.2f")`
  de M.
- `!` dentro de un `write` es el salto de línea. No es una cadena: es un **código de formato** del
  comando `write`.
- No hay declaración de tipos en ninguna parte. `precio` contiene la cadena `"15000"`, y al
  multiplicarla se interpreta como número. M es el caso extremo del tipado débil: **todo dato es una
  cadena** y el operador decide cómo leerla.

**Y ahora la parte que hace único a M.** Añade una línea:

```mumps
 set ^VENTAS($horolog, "total") = total
```

Eso **ya está en disco**. Sin `INSERT`, sin conexión, sin `commit`, sin ORM, sin fichero abierto.
`^VENTAS` es un *global*: un árbol persistente, transaccional y compartido por todos los procesos.
Otro proceso puede leerlo inmediatamente con `set x = ^VENTAS(clave,"total")`. Y se puede recorrer
sin conocer las claves:

```mumps
 set clave = ""
 for  set clave = $order(^VENTAS(clave))  quit:clave = ""  do
 . write clave, " -> ", ^VENTAS(clave, "total"), !
```

`$order` da la siguiente clave existente en orden. Es el `SELECT` de M: no describes qué quieres,
recorres el árbol. El `quit:condición` es un **postcondicional**, otra marca de la casa: casi
cualquier comando admite `:condición` para ejecutarse solo si se cumple. Y el punto que abre la
última línea marca el **nivel de anidamiento del bloque**.

Si esta sintaxis te parece de otro planeta, es porque lo es: M no desciende de ALGOL como casi todo
lo demás en este Atlas. Es una rama evolutiva independiente.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En M es… |
|---|---|
| `x = 5` | `set x=5` (o `S x=5`) |
| `print(x)` | `write x,!` |
| `if cond: ...` | `if cond do ...` o el postcondicional `write:cond x` |
| `for i in range(1,10)` | `for i=1:1:10 do ...` |
| `dict["a"]["b"]` | `array("a","b")` — arrays multidimensionales dispersos |
| `INSERT INTO ventas ...` | `set ^VENTAS(clave)=valor` — sin más |
| `SELECT ... ORDER BY` | Recorrido con `$order` sobre el global |
| `"a,b,c".split(",")[2]` | `$piece("a,b,c", ",", 2)` |
| `f"{x:.2f}"` | `$justify(x, 0, 2)` |
| Transacción | `tstart` / `tcommit` — existen, pero no hacen falta para persistir |

## ⚠️ Errores comunes al leerlo

- **La columna 1.** Código en la columna 1 = etiqueta. Es el error de novato universal en M.
- **Confundir `^` con "puntero" o con XOR.** El circunflejo al inicio de un nombre significa
  **persistente**. En medio de una cadena de datos, suele ser simplemente el delimitador de campos
  por convención — dos usos distintos del mismo carácter.
- **Buscar tipos.** No hay. `1` y `"1"` son lo mismo. `"12ABC" + 1` da `13`, porque M convierte
  leyendo el prefijo numérico y descartando el resto, sin avisar.
- **Leer el código abreviado como ofuscación intencionada.** `S X=$P(L,U,2)` es idioma normal, no
  código sucio. Aprende las abreviaturas antes de juzgar.
- **Espacios que importan.** Un `for` sin argumentos (bucle infinito) lleva **dos espacios** antes del
  siguiente comando. Un espacio de más o de menos cambia el significado.
- **El punto de anidamiento.** Los `.` al comienzo de línea marcan bloques dentro de un `do`. No son
  decoración.

## 📚 Fuentes y bibliografía

- [YottaDB — documentación](https://docs.yottadb.com/) — la implementación libre; el
  *Programmer's Guide* es la mejor referencia gratuita del lenguaje.
- [InterSystems IRIS](https://docs.intersystems.com/) — documentación del producto comercial y de
  **ObjectScript**, el descendiente moderno.
- [VistA — Departamento de Asuntos de Veteranos de EE. UU.](https://www.va.gov/health/vista.asp) — el
  sistema abierto donde ver M aplicado a escala real.
- [The M Technology Association (MTA)](https://mtaonline.org/) — comunidad y materiales del estándar.
- **Richard Walters**, *M Programming: A Comprehensive Guide*, Digital Press — el libro clásico y
  todavía el más completo sobre el lenguaje.
- **Ed de Moel**, *M[UMPS] by Example* — referencia práctica y compacta, disponible en línea.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [Common Lisp](common-lisp.md) · [Smalltalk](smalltalk.md) · [COBOL](cobol.md)
