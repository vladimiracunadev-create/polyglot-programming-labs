# Parte 11 — Proyecto integrador políglota

> [⏮️ Parte 10](../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md)

**12 clases** · rango 165–176 · clases de **proyecto** · nivel avanzado · **~36 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **Un sistema real con cinco componentes en cinco lenguajes, construido, probado, desplegado y defendido.**

---

## 🧭 De qué trata esta parte

El proyecto integrador reúne las once partes anteriores en un solo sistema: una CLI en un lenguaje de sistemas, un servicio backend, un frontend web, una capa de datos en SQL y scripts de automatización. No es un ejercicio ilustrativo — es la forma que tiene de verdad un sistema profesional.

El orden reproduce el de un proyecto real: primero el inventario de componentes, después los **contratos** entre ellos (antes de escribir código), luego cada pieza, después la persistencia, las pruebas end-to-end y el empaquetado, y por último la documentación. Cada clase añade al mismo sistema, así que saltarse una deja un hueco visible en la siguiente.

El cierre no es el despliegue sino la **defensa razonada**: un sistema con cinco lenguajes sin justificación escrita es un sistema que nadie querrá mantener. La clase 176 devuelve la tesis del programa convertida en método: cómo abordar solo el lenguaje número once.

## 🎒 Qué necesitas traer

Todo el programa anterior. En particular la Parte 9 (pruebas, CI, despliegue) y la Parte 10 (contratos y fronteras), que aquí se aplican en vez de estudiarse.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Descomponer un sistema en componentes con responsabilidades disjuntas y contratos explícitos.
2. Implementar cada componente en el lenguaje adecuado y justificar la elección con criterios.
3. Hacer que cinco componentes en cinco lenguajes se comuniquen sin acoplarse innecesariamente.
4. Probar el sistema completo de extremo a extremo y detectar los fallos de contrato entre piezas.
5. Empaquetar y desplegar un sistema políglota de forma reproducible.
6. Defender por escrito cada decisión de lenguaje ante alguien que no participó en el proyecto.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 Diseño · clases 165–166

Inventario de componentes y definición de responsabilidades y contratos antes de codificar.

- **[165 · El proyecto: un sistema con componentes en varios lenguajes](165-el-proyecto-un-sistema-con-componentes-en-varios-lenguajes/README.md)** — Arranca el proyecto integrador con la última idea del programa: un sistema real casi nunca es un programa monolítico sino una **federación de componentes** que colaboran. Aquí se inventaría qué piezas hacen falta.
- **[166 · Diseño: responsabilidades y contratos entre componentes](166-diseno-responsabilidades-y-contratos-entre-componentes/README.md)** — Con el inventario en la mano, definir **responsabilidades** y **contratos** entre piezas: qué entra, qué sale, qué errores son posibles y quién es dueño de cada dato. El diseño se hace antes, no se documenta después.

### 🔹 Los cinco componentes · clases 167–171

CLI, servicio, frontend, datos y automatización: cada pieza en su lenguaje natural.

- **[167 · Componente CLI (lenguaje de sistemas)](167-componente-cli-lenguaje-de-sistemas/README.md)** — El primer componente concreto: la **CLI**, territorio natural de los lenguajes de sistemas que compilan a un binario sin runtime. Argumentos, códigos de salida y salida legible por humanos y por máquinas.
- **[168 · Componente de API/servicio (backend)](168-componente-de-api-servicio-backend/README.md)** — El corazón del sistema: el **servicio backend** donde vive la lógica de negocio. Recibe una petición y devuelve una respuesta con dos partes que conviene no mezclar: el dato y el estado de la operación.
- **[169 · Componente web/frontend (JS/TS)](169-componente-web-frontend-js-ts/README.md)** — La cara visible: el **frontend** en JavaScript o TypeScript, único lenguaje que el navegador ejecuta de forma nativa. Consume el contrato definido en la clase 166 y demuestra si ese contrato era bueno.
- **[170 · Componente de datos y consultas (SQL)](170-componente-de-datos-y-consultas-sql/README.md)** — El **componente de datos**: la fuente de verdad del sistema, en SQL. Modelar el esquema y escribir consultas es ejercer el paradigma declarativo de la Parte 7 sobre datos que ahora son del proyecto.
- **[171 · Componente de automatización/scripting](171-componente-de-automatizacion-scripting/README.md)** — El **pegamento**: los scripts que ejecutan tareas repetitivas sin que nadie mire —limpiar, respaldar, desplegar, informar—. Poco glamuroso y decisivo, porque es lo que hace que el sistema se opere solo.

### 🔹 Datos, pruebas y despliegue · clases 172–174

Persistencia, pruebas end-to-end y empaquetado en contenedores.

- **[172 · Persistencia y almacenamiento](172-persistencia-y-almacenamiento/README.md)** — Guardar un dato para recuperarlo cuando el proceso que lo escribió ya no exista. Dónde vive el estado, qué se persiste y qué se recalcula, y las garantías que se están asumiendo sin decirlo.
- **[173 · Pruebas end-to-end del sistema completo](173-pruebas-end-to-end-del-sistema-completo/README.md)** — Ejercitar el sistema **completo**, de la entrada a la salida, como lo haría un usuario real. Es la única prueba que puede fallar por un contrato mal entendido entre dos componentes que individualmente pasaban sus pruebas.
- **[174 · Empaquetado, contenedores y despliegue](174-empaquetado-contenedores-y-despliegue/README.md)** — Empaquetar el sistema y su entorno en un artefacto reproducible y ponerlo a correr. Es el momento en que un proyecto políglota deja de ser un problema y pasa a ser una ventaja: cada componente trae su propio toolchain, aislado.

### 🔹 Defender y transferir · clases 175–176

La documentación de decisiones y el cierre del programa con el método de transferencia.

- **[175 · Documentación y defensa de las decisiones de lenguaje](175-documentacion-y-defensa-de-las-decisiones-de-lenguaje/README.md)** — Escribir la parte que no se ejecuta y decide si el sistema sobrevive: la **defensa razonada** de cada elección de lenguaje. Un sistema con cinco lenguajes sin justificación escrita es un sistema que nadie querrá mantener.
- **[176 · Cierre: retrospectiva y transferencia a nuevos lenguajes](176-cierre-retrospectiva-y-transferencia-a-nuevos-lenguajes/README.md)** — Cierre del programa: mirar atrás las 176 clases y, sobre todo, adelante — hacia el lenguaje que todavía no conoces. La tesis de la clase 001 se cierra aquí, convertida en un método de transferencia que puedes aplicar solo.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «Un sistema políglota es una decisión estética.» | Cada frontera cuesta: serialización, despliegue, depuración y equipo. Solo se justifica si la ventaja del lenguaje elegido supera ese coste. |
| «Si cada componente pasa sus pruebas, el sistema funciona.» | Los fallos de un sistema distribuido viven en los contratos entre piezas, que ninguna prueba unitaria mira. |
| «La documentación se escribe al final si sobra tiempo.» | La defensa de las decisiones es lo que permite que otro equipo mantenga el sistema. Sin ella, el sistema se reescribe. |

## 🧪 Cómo estudiar esta parte

1. **Trabaja el proyecto de corrido, no clase a clase suelta.** Cada clase añade un componente al mismo sistema; saltarse una deja un hueco en el siguiente.
2. **Escribe el contrato antes que el código** de cada componente: entradas, salidas, errores y quién es responsable de qué.
3. **Ejecuta el sistema completo al cerrar cada clase**, aunque la pieza nueva sea mínima. Un sistema políglota que solo funciona por partes no funciona.
4. **Justifica cada elección de lenguaje por escrito.** La defensa razonada es parte entregable del proyecto, no un adorno.

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- M. Nygard — *Release It!* (2ª ed., Pragmatic Bookshelf).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

## 🔗 Qué abre esta parte

El programa termina donde empezó, en la clase 001, pero con una diferencia: ahora el método de transferencia lo aplicas tú, sobre el lenguaje que elijas.

---

> [⏮️ Parte 10](../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md)
