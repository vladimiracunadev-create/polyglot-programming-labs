# 🐍 Python — 1991

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Python es hoy el lenguaje más enseñado del mundo y el que más gente escribe sin llamarse
programadora. Su historia explica las dos cosas: **nació para ser legible**, y treinta años después
esa decisión resultó valer más que casi cualquier otra característica técnica.

> **🎯 Por qué está en este programa**
>
> **Python es uno de los diez lenguajes del núcleo**: se implementa y se verifica en CI en las 136
> clases de código. Esta ficha no repite eso — cuenta su historia y responde a por qué se eligió
> como representante.
>
> Python es el **representante del scripting dinámico**
> ([Atlas](README.md#scripting-dinamico)): tipado dinámico, poca ceremonia, y una biblioteca
> estándar que cubre casi todo. Quien entiende la versión Python de una clase reconoce después la de
> [Ruby](ruby.md), [Perl](perl.md), [Lua](lua.md), [Tcl](tcl.md) o [R](r.md) sin haberlas visto.
> Y es, además, el lenguaje con el que hoy se pega el resto del sistema
> ([clase 155](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/155-por-que-los-sistemas-reales-son-poliglotas/README.md)).

| | |
|---|---|
| **Año** | 1991; **2.0** en 2000; **3.0** en 2008; ciclo anual desde **3.9** |
| **Autoría** | **Guido van Rossum**, CWI (Ámsterdam), como sucesor de **ABC** |
| **Familia** | Scripting dinámico — con influencia de ABC, Modula-3, C y Lisp |
| **Paradigma** | Multiparadigma: imperativo, orientado a objetos y funcional |
| **Tipado** | **Dinámico y fuerte**; anotaciones opcionales comprobadas por herramientas |
| **Memoria** | Automática: **conteo de referencias** + recolector de ciclos |
| **Ejecución** | Compilado a bytecode e interpretado (CPython); PyPy con JIT |
| **Estado** | 🟢 **Dominante** en ciencia de datos, IA, automatización y enseñanza |

---

## 📜 Historia

Guido van Rossum trabajaba en el CWI de Ámsterdam en **ABC**, un lenguaje de enseñanza muy cuidado
que nunca despegó. De ABC se llevó una obsesión —**que el código se lea**— y una lección: ABC era
cerrado y no se podía extender, y por eso murió.

En las navidades de **1989** empezó Python como proyecto personal. El nombre no viene del reptil sino
de **Monty Python's Flying Circus**, y esa broma marcó el tono de toda la documentación durante
décadas.

Las decisiones que lo definieron estaban ahí desde el principio: **la indentación como sintaxis** —el
bloque se marca con espacios, no con llaves—, **todo es un objeto**, y una biblioteca estándar
grande, la política de las **"baterías incluidas"**.

**Python 2.0 (2000)** trajo la comprensión de listas y el recolector de ciclos. **Python 3.0 (2008)**
rompió la compatibilidad para arreglar lo que estaba mal —sobre todo la distinción entre **bytes y
texto**, que en Python 2 era una fuente constante de errores (clase 093)— y la migración costó
**doce años**: el soporte de Python 2 terminó en 2020.

Esa transición es un caso de estudio de la
[clase 143](../classes/parte-9-ingenieria-de-software-poliglota/143-dependencias-versiones-y-lockfiles/README.md):
una ruptura necesaria, técnicamente correcta y socialmente carísima.

Desde **3.9** hay una versión anual con fecha fija, y el lenguaje ha ido incorporando **anotaciones de
tipo** (2015), `async`/`await` (2015), el operador morsa (2018), el emparejamiento estructural (2021)
y, en marcha, la eliminación del bloqueo global del intérprete.

## 🏭 Dónde vive hoy

- **Ciencia de datos e inteligencia artificial**: NumPy, pandas, scikit-learn, PyTorch, TensorFlow.
  Es el idioma común del campo, sin discusión.
- **Automatización y administración de sistemas**: el sucesor natural de los guiones de
  [Perl](perl.md) y de shell.
- **Web de servidor**: Django, FastAPI, Flask.
- **Enseñanza**: es el primer lenguaje en la mayoría de las universidades del mundo.
- **Herramientas de desarrollo**: Ansible, dbt, buena parte de los sistemas de construcción y de
  despliegue.
- **Investigación científica**: la sustitución de MATLAB en muchos laboratorios, con el ecosistema
  SciPy.

## 🧠 La decisión que lo explica: legibilidad sobre todo lo demás

Python renuncia a cosas que otros lenguajes consideran irrenunciables, y **cada renuncia compra
legibilidad**:

- **No hay llaves ni `end`**: la indentación *es* el bloque. Elimina de golpe la discusión de estilo y
  hace imposible que el sangrado mienta sobre la estructura.
- **No hay asignación dentro de una expresión** —hasta el operador morsa, y con reservas—, ni
  incremento `++`, ni operador ternario con `?:`.
- **`self` explícito** en los métodos: se ve de dónde viene cada atributo.
- **Solo hay una forma obvia de hacerlo**: es la línea más citada del *Zen de Python*, y es lo
  contrario del lema de [Perl](perl.md) (clase 146).

Y el coste hay que decirlo con la misma claridad:

> **El precio es el rendimiento y la concurrencia.** CPython interpreta bytecode y tiene un **bloqueo
> global del intérprete** (el GIL) que impide que dos hilos ejecuten bytecode a la vez. Por eso el
> Python que va rápido **casi nunca es Python**: NumPy, PyTorch y pandas son C, C++ y
> [Fortran](fortran.md) por debajo (clase 155), y Python es la capa que los compone. Entender eso es
> entender por qué el lenguaje "lento" domina el cálculo intensivo.

## 🔄 Lo que se ha modernizado

- **Anotaciones de tipo y comprobadores estáticos**: `mypy`, `pyright`, `ty`. El tipado sigue siendo
  dinámico en ejecución, pero **el análisis previo caza una familia entera de errores** — es la misma
  idea que la clase 146 defiende para todos los lenguajes.
- **`async`/`await`** y el ecosistema asíncrono (asyncio, anyio, FastAPI) — clase 134.
- **Emparejamiento estructural** (`match`/`case`) desde 3.10, al estilo ML.
- **Herramientas de una generación nueva escritas en Rust**: `ruff` (análisis y formato), `uv`
  (gestor de paquetes y entornos), que han reducido de minutos a segundos operaciones cotidianas.
- **PEP 703: el intérprete sin GIL**, opcional desde 3.13 y en camino de ser el modo por defecto. Es
  el cambio más profundo del lenguaje desde Python 3.
- **Mejoras de rendimiento sostenidas** desde 3.11 (el proyecto *Faster CPython*), con intérprete
  especializado y un JIT experimental.

## ⚙️ Cómo se ejecuta hoy

```bash
python3 main.py < entrada.txt          # el comando de la clase 041

# Entorno y dependencias reproducibles (clase 143):
uv venv && uv pip install -r requirements.txt
uv run main.py

# Calidad, como en la clase 146:
ruff check . && ruff format --check .
mypy .
pytest
```

## 🧪 El programa de la clase 041 en Python

Es el que se ejecuta y se verifica en la
[clase 041](../classes/parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md).

```python
import sys

# Literales y constantes: los valores se leen y se nombran.
precio_str, cantidad_str, descuento_str = sys.stdin.readline().split()

PRECIO_UNITARIO = float(precio_str)   # tipo dinámico, inferido en tiempo de ejecución
CANTIDAD = int(cantidad_str)
DESCUENTO = float(descuento_str)

subtotal = PRECIO_UNITARIO * CANTIDAD
total = subtotal * (1 - DESCUENTO)

print(f"Total: {total:.2f}")
```

**Lo que hay que ver, comparando con las otras fichas.**

- **La desestructuración en la primera línea** —tres nombres para tres trozos— es la misma que hacen
  [Ruby](ruby.md), [Kotlin](kotlin.md) y [Rust](rust.md), y que [Java](java.md) no permite.
- **`PRECIO_UNITARIO` en mayúsculas no es una constante**: es una convención. Python **no tiene
  constantes** (clase 041), y esa ausencia es una decisión: el lenguaje confía en el acuerdo y no
  en el compilador. Compárese con [Ada](ada.md), donde una constante es un tipo con dominio.
- **La conversión es explícita** (`float`, `int`) porque Python tiene **tipado fuerte**: `"3" + 4` es
  un error, a diferencia de [JavaScript](javascript.md) o [PHP](php.md) (clase 100).
- **`f"{total:.2f}"`** es interpolación con formato; la misma familia de `%.2f` que aparece en casi
  todas las fichas, con otra sintaxis.

## 📚 Fuentes y bibliografía

- [Documentación oficial de Python](https://docs.python.org/3/) — el tutorial y la referencia de la
  biblioteca estándar siguen siendo de lo mejor escrito en cualquier lenguaje.
- [Índice de PEP](https://peps.python.org/) — cada decisión del lenguaje, con su discusión. **PEP 8**
  (estilo), **PEP 20** (el Zen), **PEP 484** (tipos), **PEP 703** (sin GIL).
- **Luciano Ramalho**, *Fluent Python*, 2.ª ed., O'Reilly — el libro que enseña a escribir Python
  como Python y no como Java con otra sintaxis.
- **Brett Slatkin**, *Effective Python*, 3.ª ed., Addison-Wesley — 125 consejos concretos.
- **David Beazley, Brian K. Jones**, *Python Cookbook*, 3.ª ed., O'Reilly — recetas con explicación.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Ruby](ruby.md) · [Perl](perl.md) · [Lua](lua.md) · [C](c.md) · [Julia](julia.md)
