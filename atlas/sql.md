# 🗄️ SQL — 1974

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

SQL es el lenguaje más usado del mundo por gente que no se considera programadora, el único de esta
lista que **no dice cómo hacer las cosas**, y el que más tiempo lleva sin ser sustituido pese a que
cada década alguien lo intenta. Cincuenta años después, **sigue siendo la forma en que la humanidad le
pregunta cosas a sus datos**.

> **🎯 Por qué está en este programa**
>
> **SQL es uno de los diez lenguajes del núcleo** y el **representante de la familia declarativa**
> ([Atlas](README.md#logica-declarativa)), junto a [Prolog](prolog.md) y [Datalog](datalog.md).
>
> Está en el núcleo porque enseña el paradigma que ningún otro del curso enseña: **describir el
> resultado y dejar que otro decida cómo obtenerlo**
> ([clase 118](../classes/parte-7-paradigmas-de-programacion/118-programacion-declarativa/README.md)).
> Y porque **es la frontera con los datos de casi cualquier sistema real** (clase 170): quien
> programa cualquier cosa acaba escribiendo SQL.

| | |
|---|---|
| **Año** | 1974 (SEQUEL); **SQL-86** el primer estándar; **SQL:2023** el vigente |
| **Autoría** | **Donald Chamberlin** y **Raymond Boyce**, IBM San José, sobre la teoría de **Edgar Codd** |
| **Familia** | Declarativa / lógica — basada en el **álgebra relacional** |
| **Paradigma** | **Declarativo**: se describe el qué, el optimizador decide el cómo |
| **Tipado** | Estático, con tipos del esquema; **`NULL` es un tercer valor lógico** |
| **Memoria** | No aplica: la gestiona el motor |
| **Ejecución** | Se **compila a un plan de acceso** que un optimizador elige por coste |
| **Estado** | 🟢 **Universal e insustituible**; todo lo que quiso reemplazarlo acabó añadiéndolo |

---

## 📜 Historia

En **1970**, **Edgar F. Codd** publicó en IBM *A Relational Model of Data for Large Shared Data
Banks*. La idea era matemática: **los datos son relaciones —conjuntos de tuplas— y se manipulan con
un álgebra**. Nada de punteros, nada de recorridos: **conjuntos**.

Era una idea incómoda. La industria estaba en lo jerárquico ([IMS](pl-i.md)) y en lo navegacional
([CODASYL](cobol.md)), donde el programa recorría los datos a mano (clase 170), y el modelo relacional
parecía lento y académico.

En **1974**, **Chamberlin y Boyce** diseñaron **SEQUEL** —*Structured English Query Language*— como
una forma legible de expresar el álgebra de Codd. Hubo que renombrarlo a **SQL** por un conflicto de
marca con una empresa aeronáutica británica, y por eso muchas personas siguen pronunciándolo
"sícuel".

**System R**, el prototipo de IBM, demostró lo que faltaba: **que un optimizador automático podía
elegir un plan tan bueno como el que escribiría una persona**. Sin eso, el modelo relacional no habría
ganado.

**Larry Ellison** leyó los artículos de IBM y sacó **Oracle** al mercado en **1979**, antes que la
propia IBM. El estándar llegó en **1986**, y desde entonces cada revisión ha ido añadiendo:
integridad referencial y transacciones (**SQL-92**), disparadores y objetos (**SQL:1999**), XML
(**2003**), funciones de ventana (**2003**), `MERGE` (**2008**), tablas temporales (**2011**), **JSON**
(**2016**) y **grafos con `MATCH`** (**2023**).

Y el intento de sustitución más serio —el movimiento **NoSQL** de 2009— acabó en un lugar
instructivo: **casi todas esas bases de datos añadieron después un lenguaje de consulta parecido a
SQL**, porque describir lo que se quiere resultó ser mejor que programar cómo obtenerlo.

## 🏭 Dónde vive hoy

- **Bases de datos relacionales**: PostgreSQL, MySQL/MariaDB, SQL Server, Oracle, **SQLite** —que está
  en todos los teléfonos y navegadores del mundo (clase 170)—, Db2.
- **Almacenes analíticos**: Snowflake, BigQuery, Redshift, ClickHouse, DuckDB.
- **Motores de datos masivos**: Spark SQL, Trino, Presto, Hive, Flink SQL.
- **Bases NoSQL que volvieron**: Cassandra (CQL), MongoDB (con su lenguaje de agregación y ahora
  SQL), Elasticsearch (ES|QL).
- **Y en el flujo de datos moderno**: dbt convirtió SQL en el lenguaje de la transformación analítica,
  con pruebas y control de versiones (clases 139 y 145).

## 🧠 Lo que enseña: declarar en vez de ordenar

La comparación que resume el paradigma:

```sql
SELECT cliente, SUM(importe) AS total
FROM pedidos
WHERE fecha >= '2026-01-01'
GROUP BY cliente
HAVING SUM(importe) > 10000
ORDER BY total DESC;
```

**En ninguna parte se dice cómo.** No se dice si usar un índice, si ordenar antes o después de
agrupar, si hacerlo en paralelo o si leer la tabla entera. **Eso lo decide el optimizador**, con
estadísticas de los datos, y **puede elegir un plan distinto mañana** si los datos cambian.

Y esa es la propiedad que la clase 118 quiere enseñar: **el programa dice el qué y el sistema elige el
cómo**, lo que permite que el mismo programa mejore sin tocarlo.

**Y las tres cosas de SQL que más se malinterpretan** merecen estar aquí:

**Uno, `NULL` no es un valor: es "no se sabe"** (clase 100).

```sql
NULL = NULL        -- ni verdadero ni falso: NULL
WHERE x = NULL      -- nunca devuelve nada; hay que usar IS NULL
COUNT(*) vs COUNT(columna)   -- el segundo NO cuenta los NULL
```

**Es lógica de tres valores**, y es la causa número uno de resultados sorprendentes.

**Dos, el orden lógico de evaluación no es el orden de escritura**:

```text
Se escribe:  SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY
Se evalúa:   FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
```

**Por eso no se puede usar en `WHERE` un alias definido en `SELECT`**, y sí en `ORDER BY`.

**Y tres, las transacciones y el aislamiento** (clases 161 y 172): `READ COMMITTED`, `REPEATABLE
READ` y `SERIALIZABLE` no son detalles de configuración — **cambian qué anomalías puede ver el
programa**, y el nivel por defecto varía entre motores.

## 🔄 Lo que se ha modernizado

- **Funciones de ventana** (`OVER (PARTITION BY … ORDER BY …)`): agregados sin perder las filas.
  Probablemente la característica más infrautilizada del lenguaje.
- **CTE y CTE recursivas** (`WITH RECURSIVE`): consultas legibles y recorrido de jerarquías — que es
  [Datalog](datalog.md) dentro de SQL.
- **JSON como tipo de primera clase** (SQL:2016) con índices: la respuesta a NoSQL, dentro del modelo
  relacional (clase 159).
- **`MERGE`**, tablas temporales por sistema, `GENERATED` y restricciones más expresivas.
- **`GQL` y `MATCH` (SQL:2023)**: consultas de grafos en el estándar (clase 099).
- **Y el ecosistema alrededor**: **dbt** trajo control de versiones, pruebas y documentación al SQL
  analítico (clases 139, 145 y 154) — es decir, **convirtió el SQL en software**.

## ⚙️ Cómo se ejecuta hoy

```bash
sqlite3 :memory: < main.sql          # el comando de la clase 041
psql -f consulta.sql                  # PostgreSQL
duckdb -c "SELECT * FROM 'datos.parquet'"   # analítica local, sin servidor

EXPLAIN ANALYZE SELECT …              # ← el comando más importante de esta ficha (clase 152)
```

> **`EXPLAIN ANALYZE` merece el subrayado**: enseña **el plan que el optimizador eligió y lo que
> costó de verdad**. Es la única forma de saber por qué una consulta va lenta, y es la herramienta
> de la clase 152 aplicada al componente de datos.

## 🧪 El programa de la clase 041 en SQL

```sql
-- SQL es declarativo: no lee stdin como los lenguajes imperativos. En vez de
-- una variable que se asigna, se describe el cálculo sobre una tabla de valores.
-- Esta consulta demuestra la misma fórmula para los tres casos de casos.json.
WITH ventas(precio_unitario, cantidad, descuento) AS (
    VALUES (15000.0, 2, 0.10),
           (999.9, 3, 0.0),
           (5000.0, 0, 0.20)
)
SELECT printf('Total: %.2f', precio_unitario * cantidad * (1 - descuento)) AS resultado
FROM ventas;
```

**Lo que hay que ver, y es lo más interesante de esta ficha.**

- **Este programa no puede tener la forma de los demás**, y esa imposibilidad es el contenido. **SQL
  no lee de la entrada estándar ni tiene variables que se asignan**: se declara un conjunto de filas y
  se describe qué se quiere de él. La clase 040 llama a esto **contrato adaptado**, y declararlo es
  más honesto que fingir.
- **`WITH … AS (VALUES …)`** construye una tabla al vuelo. En el resto de las fichas, los tres valores
  son tres variables; aquí son **tres filas**, y la consulta se aplica a las tres a la vez.
- **No hay bucle.** Esa ausencia es el paradigma: **la operación se define sobre el conjunto**, y el
  motor decide si recorre, si paraleliza o si usa un índice.
- **`printf` es de SQLite**; en PostgreSQL sería `to_char` y en SQL Server `FORMAT`. **El formateo es
  la parte menos estándar de SQL**, y es un recordatorio útil de que "SQL" son varios dialectos con un
  núcleo común (clase 160).

## 📚 Fuentes y bibliografía

- [Documentación de PostgreSQL](https://www.postgresql.org/docs/) — la mejor documentación de base de
  datos que existe, y sirve para aprender SQL aunque uses otro motor.
- [Use The Index, Luke!](https://use-the-index-luke.com/es) — en español; explica índices y planes de
  ejecución mejor que ningún libro (clase 152).
- [Modern SQL](https://modern-sql.com/) — qué hay en el estándar desde SQL-92 y qué motor lo
  implementa. Funciones de ventana y CTE, explicadas de verdad.
- **Markus Winand**, *SQL Performance Explained* — corto, denso y práctico.
- **C. J. Date**, *SQL and Relational Theory*, 3.ª ed., O'Reilly — la teoría, incluido el problema de
  `NULL`, por uno de los que estuvieron desde el principio.
- **Edgar F. Codd**, *A Relational Model of Data for Large Shared Data Banks* (1970) — el artículo
  original; se lee en veinte minutos y explica de dónde viene todo.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Prolog](prolog.md) · [Datalog](datalog.md) · [M/MUMPS](mumps.md) ·
[COBOL](cobol.md) · [PL/I](pl-i.md)
