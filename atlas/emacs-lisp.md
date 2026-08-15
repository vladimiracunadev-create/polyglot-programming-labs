# 📝 Emacs Lisp — 1985

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Emacs Lisp es, probablemente, **el lenguaje incrustado con más código escrito de la historia** — y el
único cuyo anfitrión es tan indistinguible de él que la pregunta "¿Emacs es un editor o un intérprete
de Lisp?" tiene una respuesta clara: **es un intérprete de Lisp que resulta que edita texto**.

> **🎯 Por qué está en este programa**
>
> Emacs Lisp es un **primo de la familia Lisp** ([Atlas](README.md#lisp)).
>
> Aporta al programa el caso de estudio más grande y más antiguo de
> **[incrustar un lenguaje en otro](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md)**:
> cuarenta años de una aplicación cuyo 90 % está escrito en su propio lenguaje de extensión,
> **modificable en marcha**. Y es el último lugar de uso masivo donde sobrevive el **alcance dinámico**
> (clase 088), que aquí se puede estudiar en vivo.

| | |
|---|---|
| **Año** | 1985 (GNU Emacs 13); Emacs es de 1976, con otro lenguaje |
| **Autoría** | **Richard Stallman**, sobre el Emacs original de Stallman y Guy Steele |
| **Familia** | Lisp; más cerca de MacLisp que de [Scheme](scheme.md) o Common Lisp |
| **Paradigma** | Imperativo y funcional; orientado a objetos con EIEIO |
| **Tipado** | **Dinámico**; con alcance **dinámico por defecto** hasta hace poco |
| **Memoria** | Recolección de basura |
| **Ejecución** | Bytecode interpretado; **compilación nativa a C** desde Emacs 28 |
| **Estado** | 🟢 **Muy vivo** dentro de su ecosistema; irrelevante fuera |

---

## 📜 Historia

**Emacs** nació en 1976 en el MIT como un conjunto de macros para el editor TECO —de ahí el nombre,
*Editor MACroS*—. Cuando **Richard Stallman** arrancó el proyecto GNU en 1984, reescribió Emacs desde
cero y tomó una decisión que lo definió todo: **el editor tendría un intérprete de Lisp dentro, y
todo lo que no fuera imprescindible se escribiría en Lisp**.

El resultado es una arquitectura de dos capas exacta a la que Ousterhout describiría trece años
después (clase 155):

```text
Un núcleo en C:  el intérprete de Lisp, la gestión de búferes, el dibujado
                  y las primitivas de bajo nivel.

Todo lo demás en Emacs Lisp:  los modos de edición, el cliente de correo,
                               la interfaz de git, el gestor de ficheros,
                               el depurador, el calendario, el organizador…
```

Y con una propiedad que ningún otro sistema de esta lista tiene igual: **todo eso es modificable en
marcha, sin reiniciar y sin recompilar** (clase 124).

**Org mode** —un sistema de notas, tareas, agenda y documentos reproducibles— es, por sí solo, uno de
los programas Lisp más grandes que existen, y está escrito íntegramente en Emacs Lisp por gente que no
es programadora de lenguajes.

Y en **2021, Emacs 28** trajo el cambio más importante en décadas: **compilación nativa**. Emacs Lisp
se traduce a C y se compila con GCC, con mejoras de rendimiento de varias veces.

## 🏭 Dónde vive hoy

- **GNU Emacs**: decenas de miles de paquetes en MELPA, todos en Emacs Lisp.
- **Org mode**: notas, agenda, y **documentos con código ejecutable** —`org-babel` ejecuta bloques de
  Python, R, SQL o shell dentro del documento y captura la salida (clase 154)—.
- **Magit**: una interfaz de git que muchos consideran mejor que cualquier cliente dedicado, escrita
  entera en Emacs Lisp.
- **Y como entorno de desarrollo** para [Common Lisp](common-lisp.md) —con SLIME—, Haskell, Clojure y
  media docena más.

## 🧠 Lo que enseña: el alcance dinámico, en vivo

Emacs Lisp es **el último sitio de uso masivo donde el alcance dinámico es el comportamiento por
defecto**, y eso lo hace un laboratorio perfecto para la clase 088:

```elisp
(defvar *nivel* 0)                     ; variable especial: alcance DINÁMICO

(defun escribir (msg)
  (message "%s%s" (make-string *nivel* ?\s) msg))

(defun con-sangria (f)
  (let ((*nivel* (+ *nivel* 2)))       ; ← afecta a TODO lo que se llame desde aquí
    (funcall f)))
```

**`let` sobre una variable especial no crea una variable local: cambia temporalmente la global**, y
todo lo que se ejecute dentro —incluidas funciones que no sabían nada de esto— ve el valor nuevo.

**Y en un editor eso resulta ser exactamente lo que hace falta**: `case-fold-search`,
`default-directory`, `inhibit-read-only` son variables que se enlazan alrededor de una operación para
cambiar cómo se comporta todo el código que participa.

Es la razón por la que Emacs Lisp lo conservó cuando el resto del mundo Lisp se pasó al alcance
léxico — y desde Emacs 24 **se puede activar el léxico por fichero**, que es hoy la recomendación:

```elisp
;;; -*- lexical-binding: t -*-
```

Y hay una segunda cosa que Emacs enseña, y es de la clase 163: **el anfitrión y el lenguaje incrustado
casi no tienen frontera**.

```elisp
(defun mi-comando ()
  (interactive)                        ; ← esto lo convierte en un comando invocable
  (insert (format-time-string "%Y-%m-%d")))

(global-set-key (kbd "C-c d") #'mi-comando)
```

**No hay API que registrar ni puente que cruzar**: las funciones del editor **son** funciones Lisp, y
las funciones propias **son** comandos del editor. Es el extremo opuesto de los alias de
[Safe-Tcl](tcl.md), donde la frontera está cerrada a propósito (clase 153).

> **Y el precio es el que la clase 163 advierte**: **no hay aislamiento**. Un paquete de MELPA puede
> hacer cualquier cosa, y la seguridad depende por completo de la confianza en quien lo escribió.

## 🔄 Lo que se ha modernizado

- **Compilación nativa** (28): Emacs Lisp a C y a código máquina con GCC.
- **Enlace léxico** por fichero, hoy recomendado siempre; y `cl-lib` con las construcciones de Common
  Lisp.
- **Hilos** (26) —cooperativos— y **`seq`/`map`** como bibliotecas genéricas de colecciones.
- **Tree-sitter** (29) para el análisis sintáctico de los modos de lenguaje, sustituyendo décadas de
  expresiones regulares (clase 123).
- **Y `use-package` y `straight.el`** como gestión declarativa de la configuración y de las
  dependencias (clase 143).

## ⚙️ Cómo se ejecuta hoy

```bash
emacs --batch -l main.el                   # ejecutar un guion sin interfaz
emacs --batch -f batch-byte-compile *.el    # compilar a bytecode
emacs --batch -l ert -f ert-run-tests-batch-and-exit   # pruebas (clase 139)

# Y dentro de Emacs: C-x C-e evalúa la expresión anterior, EN EL SISTEMA VIVO
```

## 🧪 El programa de la clase 041 en Emacs Lisp

Emacs Lisp puede ejecutarse en lote, aunque no sea su uso natural. **No está verificado en CI**
(clase 040).

```elisp
;;; -*- lexical-binding: t -*-
(let* ((linea (read-string ""))
       (campos (split-string linea))
       (nums (mapcar #'string-to-number campos))
       (total (* (nth 0 nums) (nth 1 nums) (- 1 (nth 2 nums)))))
  (princ (format "Total: %.2f\n" total)))
```

**Lo que hay que ver.**

- **La primera línea, con `lexical-binding: t`, no es un comentario decorativo**: **cambia la
  semántica del fichero entero** (clase 088). Sin ella, `let*` crearía enlaces dinámicos. Es una de
  las pocas veces en que un comentario mágico cambia el significado del programa.
- **`#'string-to-number`** usa la comilla de función: en un *Lisp-2* como este, **funciones y valores
  viven en espacios de nombres distintos** —a diferencia de [Scheme](scheme.md), que es un *Lisp-1*—.
- **`princ` y no `message`**: en modo lote, `message` va al error estándar y `princ` a la salida
  (clase 167).
- **`%.2f` en `format`** es, otra vez, la herencia de [C](c.md).
- **Y este programa es lo menos representativo del lenguaje que se puede escribir**: Emacs Lisp está
  hecho para manipular búferes, no para leer de la entrada estándar. Es un **contrato adaptado**
  (clase 040), y decirlo es más honesto que fingir.

## 📚 Fuentes y bibliografía

- [An Introduction to Programming in Emacs Lisp](https://www.gnu.org/software/emacs/manual/eintr.html)
  — **Robert Chassell**, incluido en Emacs; escrito para quien no ha programado nunca.
- [Emacs Lisp Reference Manual](https://www.gnu.org/software/emacs/manual/elisp.html) — completo y
  disponible dentro del propio editor con `C-h i`.
- [Mastering Emacs](https://www.masteringemacs.org/) — **Mickey Petersen**; el mejor libro sobre el
  editor y su modelo de extensión.
- **Org mode** y **`org-babel`** — para ver la idea de documento reproducible (clase 154) en su forma
  más madura.
- [MELPA](https://melpa.org/) — el archivo de paquetes; útil como ejemplo de ecosistema sin
  aislamiento (clase 153).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Common Lisp](common-lisp.md) · [Scheme](scheme.md) · [AutoLISP](autolisp.md) ·
[Tcl](tcl.md) · [Lua](lua.md)
