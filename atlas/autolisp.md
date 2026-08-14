# 📐 AutoLISP — 1986

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**Probablemente el Lisp con más usuarios del mundo, y casi ninguno se considera programador.**
Arquitectos, ingenieros civiles, delineantes y proyectistas llevan cuarenta años automatizando
AutoCAD con AutoLISP. Muchos estudios tienen miles de líneas de `.lsp` acumuladas que son, en la
práctica, su ventaja competitiva.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: AutoLISP viene incluido en AutoCAD y Autodesk lo mantiene explícitamente**
> como el mecanismo de automatización del producto, con documentación actualizada en cada versión
> anual. No es un lenguaje que sobreviva en un rincón: se distribuye con uno de los programas de
> ingeniería más instalados del planeta.
>
> Entra porque **es el mejor ejemplo vivo de un concepto que el núcleo no toca**: el **lenguaje
> incrustado en una aplicación anfitriona**. AutoLISP no tiene `main`, no tiene fichero ejecutable y
> no sirve para nada fuera de AutoCAD: su "biblioteca estándar" son los objetos del dibujo. Es la
> misma relación que [VBA](vba.md) tiene con Excel y que Lua tiene con un motor de videojuegos, y es
> el modelo de la [Parte 10](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md):
> **el lenguaje como capa de guion sobre un programa que ya existe**. Entenderlo cambia cómo se lee
> cualquier sistema de plugins.

| | |
|---|---|
| **Año** | 1986, en AutoCAD Release 2.18 |
| **Autoría** | **Autodesk**, sobre el intérprete **XLISP** de David Betz |
| **Familia** | [Lisp](common-lisp.md) — dialecto reducido y especializado |
| **Paradigma** | Funcional e imperativo, orientado a la manipulación del dibujo |
| **Tipado** | **Dinámico**, con los tipos del dibujo (puntos, nombres de entidad, conjuntos) |
| **Memoria** | Gestionada por el intérprete de AutoCAD |
| **Ejecución** | **Interpretado dentro de AutoCAD**; compilable a `.fas` / `.vlx` |
| **Estado** | 🟢 **Muy vivo dentro de su nicho** — arquitectura, ingeniería, construcción, CAD |

---

## 📜 Historia

En 1986 Autodesk necesitaba que AutoCAD fuera personalizable sin recompilarlo. La solución fue
incrustar un intérprete de Lisp: se partió de **XLISP**, una implementación pequeña y libre de David
Betz, y se le añadieron funciones para hablar con el dibujo. La elección de Lisp no fue casual — un
intérprete de Lisp es notablemente pequeño y fácil de empotrar, la misma razón por la que Lua triunfó
después en los videojuegos.

En 1997 Autodesk adquirió Vital LISP, de Basis Software, y lo integró como **Visual LISP**: un
entorno de desarrollo dentro de AutoCAD (`VLIDE`), un compilador a ficheros `.fas`/`.vlx` para
proteger el código, y —lo más importante— el acceso al **modelo de objetos ActiveX** de AutoCAD a
través de las funciones `vla-*`. Eso duplicó de golpe lo que se podía hacer.

Durante casi cuarenta años Autodesk ha añadido lenguajes alternativos —VBA, ObjectARX en C++, .NET,
más recientemente extensiones en JavaScript— y AutoLISP ha sobrevivido a todos. La razón es
sociológica más que técnica: es el único que un ingeniero sin formación en programación aprende en
una tarde y usa el mismo día.

## 🏭 Dónde sobrevive hoy

- **Estudios de arquitectura e ingeniería**: rutinas de acotado automático, generación de leyendas,
  numeración de elementos, cumplimiento de normas de capas y estilos.
- **Ingeniería civil y topografía**: importación de puntos, perfiles, cubicaciones.
- **Instalaciones y fabricación**: generación paramétrica de piezas, listas de materiales extraídas
  del dibujo.
- **Estandarización interna**: casi cualquier oficina técnica con muchos planos tiene un `acaddoc.lsp`
  que impone la plantilla de la casa.

Existen además dialectos compatibles en clones de AutoCAD (BricsCAD, ZWCAD, GstarCAD), lo que amplía
su alcance más allá de Autodesk.

## 🧠 Por qué no ha muerto

**1. Está donde está el dibujo.** Una rutina de AutoLISP accede a la geometría, a las capas, a los
bloques y a los atributos **directamente**, sin API externa, sin instalación y sin permisos de
administrador. Ese último punto no es menor: en muchas empresas, un ingeniero puede cargar un `.lsp`
pero no puede instalar software.

**2. La curva de entrada es diminuta.** Tres funciones —`setq`, `command` y `getpoint`— bastan para
ser útil. Y como el intérprete está vivo dentro de AutoCAD, se prueba escribiendo en la línea de
comandos y viendo el resultado en pantalla al instante. Es un REPL con salida gráfica.

**3. Cuarenta años de código acumulado.** Miles de estudios dependen de rutinas escritas por alguien
que ya no está, que funcionan y que nadie va a reescribir.

**4. Autodesk lo mantiene deliberadamente.** Romper AutoLISP rompería a una parte sustancial de su
base instalada.

## 🔄 Lo que se ha modernizado

Autodesk ha invertido en AutoLISP más recientemente de lo que la gente supone:

- **Extensión oficial para Visual Studio Code**, publicada y mantenida por Autodesk: resaltado,
  autocompletado, y **depuración paso a paso conectada a una sesión de AutoCAD en marcha**. Sustituye
  al viejo VLIDE, que apenas cambió en veinte años.
- **Unicode completo**, imprescindible para trabajar con planos en cualquier idioma.
- **Ampliación de plataforma**: Autodesk ha ido llevando el soporte de AutoLISP más allá de la
  versión completa de AutoCAD para escritorio, respondiendo a la presión de una base de usuarios que
  dependía de sus rutinas. Consulta la documentación de tu versión concreta, porque este punto ha
  cambiado varias veces.
- **Funciones `vl-*` y `vla-*`** de Visual LISP para manipulación de listas, cadenas, ficheros,
  registro del sistema y el modelo de objetos ActiveX completo — muy por encima del AutoLISP de 1986.
- **Convive con las alternativas**: .NET, ObjectARX (C++) y las extensiones en JavaScript cubren lo
  que AutoLISP no alcanza, y se llaman entre sí. Ese es el patrón realista: AutoLISP para la
  automatización cotidiana del delineante, .NET para el producto empaquetado.

## ⚙️ Cómo se ejecuta hoy

AutoLISP **solo** existe dentro de AutoCAD (o de un clon compatible). No hay intérprete de línea de
comandos, no hay ejecutable, no hay CI posible.

```lisp
; Cargar desde la línea de comandos de AutoCAD:
(load "C:/rutinas/totalventa.lsp")

; O con el cuadro de diálogo:  APPLOAD
; Y para que se cargue en cada dibujo: incluirlo en acaddoc.lsp
```

**Ficheros del ecosistema:** `.lsp` (fuente), `.fas` (compilado con Visual LISP), `.vlx` (aplicación
empaquetada), `.mnl` (se carga automáticamente con el menú del mismo nombre), `acad.lsp` y
`acaddoc.lsp` (carga automática al arrancar y por cada dibujo, respectivamente).

**Herramientas:** el editor integrado **VLIDE** (`VLISP` en la línea de comandos), y hoy también la
extensión **AutoCAD AutoLISP Extension** para **Visual Studio Code**, que Autodesk publica y que
permite editar y depurar contra una sesión de AutoCAD abierta.

## 🧪 El programa de la clase 041 en AutoLISP

> ⚠️ **Contrato adaptado, y declarado.** AutoLISP no tiene `stdin` ni `stdout`: sus entradas son la
> línea de comandos de AutoCAD y el usuario, y su salida es el dibujo o la propia línea de comandos.
> El cálculo es el mismo; la forma de entrar y salir es la del anfitrión. **No se verifica en CI**:
> requiere una instalación de AutoCAD.

```lisp
;;; totalventa.lsp — clase 041 adaptada a AutoCAD
;;; El prefijo c: convierte la función en un COMANDO de AutoCAD.

(defun c:TOTALVENTA ( / precio cantidad descuento total )

  (setq precio    (getreal "\nPrecio unitario: "))
  (setq cantidad  (getreal "\nCantidad: "))
  (setq descuento (getreal "\nDescuento (0 a 1): "))

  (setq total (* precio cantidad (- 1.0 descuento)))

  (princ (strcat "\nTotal: " (rtos total 2 2)))
  (princ)
)
```

**Recorrido, línea a línea.**

- `(defun c:TOTALVENTA ...)` — el prefijo **`c:`** es la convención que convierte una función en un
  **comando de AutoCAD**: a partir de que se carga el fichero, el usuario escribe `TOTALVENTA` en la
  línea de comandos y se ejecuta. Sin ese prefijo sería una función normal, invocable solo desde
  otro código Lisp.
- **La barra en la lista de argumentos es la rareza que hay que conocer.** `( / precio cantidad ... )`
  significa: cero parámetros, y todo lo que va **detrás de la barra** son **variables locales**. Si se
  olvida la barra, esas variables quedan **globales** y contaminan la sesión de AutoCAD entera hasta
  que se cierre el dibujo. Es la primera causa de errores fantasma en AutoLISP: una rutina que
  funciona sola y falla cuando se ejecuta después de otra.
- `getreal` pide un número al usuario por la línea de comandos, con su mensaje. La familia completa
  —`getpoint`, `getdist`, `getangle`, `getstring`, `getkword`, `entsel`— es la interfaz de entrada, y
  toda ella entiende que el usuario puede responder **haciendo clic en el dibujo**. `getpoint`
  devuelve una lista `(x y z)`: los puntos son listas de números, sin tipo especial.
- `rtos` es *real to string*: `(rtos total 2 2)` significa modo **2** (decimal) con **2** decimales.
  Los modos son 1 científico, 2 decimal, 3 pies y pulgadas, 4 arquitectónico, 5 fraccionario —
  la lista delata para qué se diseñó el lenguaje.
- `princ` imprime. **El `(princ)` final y sin argumentos no es un descuido**: es el idioma
  obligatorio para que la función devuelva "nada" y AutoCAD no eche un eco del último valor en la
  línea de comandos. Todo el código AutoLISP del mundo termina así.

**Y ahora lo que hace de AutoLISP lo que es:** el acceso al dibujo.

```lisp
(defun c:RADIO ( / ent datos )
  (setq ent   (car (entsel "\nSelecciona un círculo: ")))
  (setq datos (entget ent))
  (princ (strcat "\nTipo: "  (cdr (assoc 0  datos))))
  (princ (strcat "\nRadio: " (rtos (cdr (assoc 40 datos)) 2 3)))
  (princ)
)
```

`entsel` deja al usuario **señalar un objeto con el ratón**; `entget` devuelve ese objeto como una
**lista de asociaciones**, y `assoc` extrae un campo por su número. Esos números son los **códigos de
grupo DXF**: el `0` es el tipo de entidad, el `8` la capa, el `10` el punto de inserción, el `40` el
radio. No son arbitrarios: son el formato de intercambio de AutoCAD, y aprenderlos es aprender el
modelo de datos del programa.

Ahí está la lección: **la biblioteca estándar de un lenguaje incrustado es el modelo de objetos del
anfitrión.** Aprender AutoLISP es, en un 20 %, aprender Lisp, y en un 80 %, aprender AutoCAD.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En AutoLISP es… |
|---|---|
| `x = 5` | `(setq x 5)` |
| `def f(a, b):` | `(defun f (a b / locales) ...)` |
| Variable local | Detrás de la `/` en la lista de argumentos — **no hay `let` clásico** |
| `print(x)` | `(princ x)` / `(prompt x)` / `(alert x)` |
| `str(x)` | `(rtos x 2 2)` para reales, `(itoa x)` para enteros |
| `int(s)` / `float(s)` | `(atoi s)` / `(atof s)` |
| `a + b` | `(+ a b)` |
| `if / else` | `(if condicion entonces si-no)` |
| `for x in lista` | `(foreach x lista ...)` |
| `dict["clave"]` | `(cdr (assoc clave lista))` — listas de asociación |
| Llamar a la app anfitriona | `(command "_LINE" p1 p2 "")` — ejecuta un comando de AutoCAD |
| API orientada a objetos | Las funciones `vla-*` de Visual LISP sobre ActiveX |

## ⚠️ Errores comunes al leerlo

- **Olvidar la `/` de variables locales.** Efectos entre rutinas imposibles de reproducir.
- **Olvidar el `(princ)` final.** La función devuelve el último valor y AutoCAD lo imprime, ensuciando
  la línea de comandos.
- **Usar `command` con nombres de comando localizados.** En un AutoCAD en español, `(command "LINEA")`
  funciona y `(command "LINE")` no. El prefijo de subrayado —`(command "_LINE")`— fuerza el nombre en
  inglés, y el prefijo de punto —`"._LINE"`— fuerza además el comando original aunque esté
  redefinido. Escribir `"._LINE"` no es manía: es la única forma de que la rutina funcione en
  cualquier instalación.
- **Confundir `setq` con `set`.** `setq` no evalúa el nombre de la variable; `set` sí, y se usa con
  símbolos entrecomillados.
- **Suponer aritmética real.** `(/ 7 2)` da **3**, no 3.5: si todos los argumentos son enteros, la
  división es entera. Hay que escribir `(/ 7.0 2)`.
- **Esperar Common Lisp.** No hay macros, ni CLOS, ni condiciones, ni paquetes. AutoLISP es un Lisp
  pequeño; el manejo de errores se hace con `vl-catch-all-apply` y con una función `*error*` propia.

## 📚 Fuentes y bibliografía

- [AutoLISP Developer's Guide (Autodesk)](https://help.autodesk.com/view/OARX/2026/ENU/?guid=GUID-4CEE5072-8817-4920-8A2D-7060F5E16547)
  — la guía oficial vigente.
- [AutoLISP Reference — funciones](https://help.autodesk.com/view/OARX/2026/ENU/?guid=GUID-A1301F70-D9DE-4E31-B0AD-B9E1B24CB0E0)
  — el catálogo completo de funciones, la página que se tiene siempre abierta.
- [DXF Reference](https://help.autodesk.com/view/ACD/2026/ENU/?guid=GUID-235B22E0-A567-4CF6-92D3-38A2306D73F3)
  — los códigos de grupo; imprescindible para trabajar con `entget`.
- [AutoCAD AutoLISP Extension para VS Code](https://marketplace.visualstudio.com/items?itemName=Autodesk.autolispext)
  — el entorno moderno de edición y depuración.
- **Lee Ambrosius**, *AutoCAD Platform Customization: AutoLISP*, Sybex — el libro de referencia
  actual; el autor escribe la documentación oficial de Autodesk.
- **Lee Mac**, [lee-mac.com](https://www.lee-mac.com/) — colección pública de rutinas y tutoriales
  que es, de facto, la escuela de la comunidad hispanohablante y anglosajona.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [Common Lisp](common-lisp.md) · [VBA](vba.md) · [Tcl/Tk](tcl.md)
