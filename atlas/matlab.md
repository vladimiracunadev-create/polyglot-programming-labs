# 📐 MATLAB — 1984

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

MATLAB empezó como una interfaz cómoda para las bibliotecas de álgebra lineal en
[Fortran](fortran.md) —de ahí el nombre, *MATrix LABoratory*— y se convirtió en el entorno estándar de
la ingeniería mundial. Es de los pocos lenguajes de esta lista que **es a la vez un lenguaje y un
producto comercial**, y esa dualidad explica sus fortalezas y su principal debilidad.

> **🎯 Por qué está en este programa**
>
> MATLAB es un **primo de la familia array / científica** ([Atlas](README.md#array-cientifica)), junto
> a [APL](apl.md), [J](j.md), [R](r.md), [Julia](julia.md) y [Fortran](fortran.md).
>
> Aporta al programa dos cosas: **la programación vectorizada aplicada a la ingeniería**
> ([clase 089](../classes/parte-6-datos-y-estructuras/089-arreglos-y-vectores/README.md)) y el caso de
> estudio más claro de **generación de código desde un modelo** —Simulink— que la clase 155 nombra
> como cuarta capa de un sistema poliglota, y que en aviación y automoción es donde de verdad se
> escribe el software.

| | |
|---|---|
| **Año** | 1984 (comercial); el prototipo, de finales de los setenta |
| **Autoría** | **Cleve Moler**, Universidad de Nuevo México; **MathWorks** desde 1984 |
| **Familia** | Array / científica; construido sobre **LINPACK** y **EISPACK** ([Fortran](fortran.md)) |
| **Paradigma** | Imperativo y vectorizado; con objetos añadidos después |
| **Tipado** | **Dinámico**; **todo es una matriz** de dobles por defecto |
| **Memoria** | Automática, con **copia al modificar** |
| **Ejecución** | Interpretado con JIT; con generación de C y de HDL como productos |
| **Estado** | 🟢 **Dominante en ingeniería**; **propietario y caro**, con GNU Octave como alternativa |

---

## 📜 Historia

**Cleve Moler** enseñaba análisis numérico en la Universidad de Nuevo México en los años setenta, y
sus estudiantes tenían que escribir [Fortran](fortran.md) para usar **LINPACK** y **EISPACK** —las
bibliotecas de álgebra lineal de la época, precursoras de [LAPACK](fortran.md) (clase 149)—.

Escribir Fortran para hacer un ejercicio de matrices era desproporcionado, así que Moler hizo **un
intérprete que llamaba a esas bibliotecas** con una notación matricial directa. **No pretendía ser un
producto**: era material docente, y lo repartía libremente.

En **1983**, el ingeniero **Jack Little** vio el potencial, lo reescribió en [C](c.md), le añadió
funciones y gráficos, y fundó **MathWorks** con Moler y Steve Bangert. **MATLAB salió al mercado en
1984**.

Y el momento que definió su posición industrial fue **Simulink (1990)**: un entorno **gráfico** de
modelado por bloques para sistemas dinámicos y de control. Con **Simulink Coder** y **Embedded Coder**,
**del modelo se genera código C o [Ada](ada.md) certificable** que se ejecuta en el vehículo real.

**Eso cambió qué significa "programar" en esos sectores**: en buena parte de la automoción y la
aviación, **el ingeniero de control dibuja el modelo y el código lo genera la herramienta** (clase
155) — y lo que se certifica es la cadena de generación, no el código a mano.

## 🏭 Dónde vive hoy

- **Ingeniería de control y sistemas embebidos**: automoción, aeroespacial, energía. **Simulink es el
  estándar del sector.**
- **Procesamiento de señales e imágenes**, comunicaciones y radar.
- **Investigación en ingeniería y enseñanza universitaria**: casi cualquier titulación de ingeniería
  del mundo pasa por MATLAB.
- **Biomedicina y neurociencia**, con herramientas específicas muy asentadas.
- **Y en modelos financieros**, con las cajas de herramientas correspondientes.

## 🧠 Lo que enseña: matrices por defecto, y el coste de un ecosistema propietario

**La vectorización, que es la misma idea de [R](r.md) y [APL](apl.md)** (clase 089):

```matlab
A = [1 2; 3 4];
b = [5; 6];
x = A \ b;              % ← resolver Ax = b. Una barra invertida.
y = sin(0:0.1:2*pi);     % la función se aplica a TODO el vector
```

**`A \ b` es probablemente la operación más elegante de esta lista**: resuelve el sistema lineal
eligiendo el algoritmo según la forma de la matriz —LU, QR, Cholesky o mínimos cuadrados—. **Es
LAPACK por debajo** (clase 149), y esa es exactamente la razón de ser del lenguaje.

Y hay dos peculiaridades que conviene conocer:

**Una, todo es una matriz de dobles.** Un escalar es una matriz 1×1, y el tipo por defecto es
`double`. Eso simplifica el modelo y **hace que trabajar con enteros o con memoria sea antinatural**.

**Y dos, los índices empiezan en 1 y se usan paréntesis**: `A(1,2)` es a la vez la indexación de una
matriz y la llamada a una función, según qué sea `A` — una ambigüedad sintáctica que
[Julia](julia.md) heredó y que [Fortran](fortran.md) también tiene.

> **Y la ficha debe ser honesta con lo que más pesa en la clase 164: MATLAB es propietario y caro.**
>
> Una licencia completa con cajas de herramientas cuesta miles de euros al año, y **cada caja de
> herramientas se compra aparte**. Eso tiene tres consecuencias reales: **el código no se puede
> ejecutar sin licencia**, lo que complica la reproducibilidad (clase 154); **la comunidad no puede
> corregir el lenguaje**; y **quien aprende MATLAB en la universidad se encuentra con que en su
> empresa no hay licencias**.
>
> **GNU Octave** es una reimplementación libre muy compatible para el lenguaje base, y **no cubre
> Simulink** — que es justamente donde está el valor industrial. Y esa es la razón por la que
> [Julia](julia.md) y Python+SciPy le han ido ganando terreno en investigación, aunque no en
> ingeniería de control.

## 🔄 Lo que se ha modernizado

- **JIT** desde 2002 y mejoras continuas: los bucles ya no son catastróficos, aunque la vectorización
  sigue siendo lo idiomático.
- **`arguments` blocks** (R2019b): validación de argumentos declarativa, con tipos y restricciones —
  contratos en el lenguaje (clase 118).
- **`string` como tipo** (2016), separado de los arreglos de caracteres — la corrección de un problema
  histórico (clase 093).
- **Interoperabilidad**: llamar a Python, C++, Java y .NET desde MATLAB, y al revés (clase 156).
- **MATLAB Online y Live Scripts**: cuadernos ejecutables con texto, código y resultados (clase 154).
- **Y la generación de código** cada vez más central: C, C++, HDL para FPGA y CUDA para GPU.

## ⚙️ Cómo se ejecuta hoy

```bash
matlab -batch "main"                  # ejecutar sin interfaz
octave --no-gui main.m < entrada.txt   # ← la alternativa libre

# Y dentro: runtests para las pruebas, y el Profiler para la clase 152
```

## 🧪 El programa de la clase 041 en MATLAB

Esta versión se escribe aquí y **no está verificada en CI** (clase 040). Funciona igual en **GNU
Octave**.

```matlab
v = sscanf(input('', 's'), '%f');
total = v(1) * v(2) * (1 - v(3));
fprintf('Total: %.2f\n', total);
```

**Lo que hay que ver.**

- **`sscanf(..., '%f')` devuelve un VECTOR con todos los números que encuentra**, no uno solo. Es el
  reflejo de la familia: **la unidad es el arreglo**, igual que en [R](r.md) y [APL](apl.md).
- **`v(1)` con paréntesis**, no con corchetes: en MATLAB la indexación usa la misma sintaxis que la
  llamada a función.
- **Los índices empiezan en 1** (clase 089).
- **`fprintf` con `%.2f`** es, otra vez, la herencia de [C](c.md) — MATLAB está escrito en C y su
  entrada y salida lo refleja.
- **Y el detalle que delata al lenguaje**: `v` es un `double` de 64 bits **aunque los tres valores
  fueran enteros**. En MATLAB **todo es coma flotante salvo que se pida lo contrario**, con las
  consecuencias de la clase 072.

## 📚 Fuentes y bibliografía

- [Documentación de MathWorks](https://www.mathworks.com/help/matlab/) — extensa y de calidad alta;
  la sección de rendimiento es material de la clase 152.
- **Cleve Moler**, *Numerical Computing with MATLAB* — libre en la web de MathWorks; escrito por el
  autor original y excelente como libro de análisis numérico.
- [Blog de Cleve Moler](https://blogs.mathworks.com/cleve/) — historia del lenguaje y del cálculo
  numérico, contada por quien estuvo.
- [GNU Octave](https://octave.org/doc/latest/) — la alternativa libre y su documentación.
- **Documentación de Simulink y Embedded Coder** — para entender la generación de código certificable
  (clases 155 y 174).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Fortran](fortran.md) · [Julia](julia.md) · [R](r.md) · [APL](apl.md) ·
[Ada](ada.md)
