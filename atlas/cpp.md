# 🚀 C++ — 1985

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**Como [C](c.md), está en esta lista sin ser legacy.** C++ tiene cuarenta años y una revisión del
estándar cada tres. Lo que ejecuta el videojuego que juegas, el navegador con el que lees esto, el
motor de la base de datos que guarda tus datos y el sistema que ejecuta una orden en bolsa en
microsegundos está, con altísima probabilidad, escrito en C++.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: C++ está completamente vigente**, con estándar nuevo cada tres años
> (C++20, C++23, C++26 en camino) y presencia dominante en varios dominios donde no tiene rival
> práctico.
>
> Entra porque **encarna un concepto que ningún otro lenguaje del núcleo expresa igual**: la
> **abstracción de coste cero**. La promesa de C++ es que puedes escribir código de alto nivel
> —plantillas, objetos, algoritmos genéricos— y obtener el mismo código máquina que habrías escrito a
> mano en [C](c.md). Y su segunda gran idea, **RAII**, resuelve la gestión de recursos atándola al
> tiempo de vida de un objeto: es la respuesta que precede al *ownership* de Rust y al `defer` de Go,
> y entenderla ilumina a las dos. C++ ya aparece como primo de la familia C en cada
> [`primos.md`](../classes/parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/primos.md)
> del programa; esta ficha es su historia y su porqué.

| | |
|---|---|
| **Año** | 1979 como "C con clases"; **1985** como C++; ISO desde 1998 |
| **Autoría** | **Bjarne Stroustrup**, Bell Labs |
| **Familia** | C / llaves |
| **Paradigma** | Multiparadigma: procedimental, OO, **genérico** y funcional |
| **Tipado** | Estático, fuerte, con inferencia (`auto`) y metaprogramación de tipos |
| **Memoria** | **Manual con RAII**: punteros inteligentes, destructores deterministas |
| **Ejecución** | Compilado a nativo |
| **Estado** | 🟢 **Completamente vigente** — videojuegos, navegadores, finanzas, HPC, robótica |

---

## 📜 Historia

**Bjarne Stroustrup** había trabajado con **Simula 67**, el lenguaje que inventó las clases, y le
había convencido su capacidad para modelar problemas. También le había desesperado su lentitud.
Cuando en 1979 llegó a Bell Labs, quiso las abstracciones de Simula **con el rendimiento y el acceso
al hardware de [C](c.md)**. Empezó con un preprocesador llamado *C con clases*, y en **1985** publicó
el lenguaje con el nombre **C++** —el operador de incremento de C, un chiste que se convirtió en
marca.

La regla de diseño que ha gobernado el lenguaje desde entonces es explícita y explica casi todo lo
demás: **no debes pagar por lo que no usas**. Si no utilizas excepciones, no cuestan; si no usas
funciones virtuales, no hay tabla de despacho. Esa promesa es lo que le permitió entrar donde ningún
otro lenguaje de alto nivel podía.

La cronología moderna se divide en dos épocas:

- **Hasta C++03**: crecimiento acumulativo. En 1998 llegó el primer estándar ISO, con la **STL** de
  Alexander Stepanov —contenedores, iteradores y algoritmos genéricos separados entre sí— que fue una
  aportación conceptual de primer orden y sigue influyendo en el diseño de bibliotecas de todos los
  lenguajes.
- **Desde C++11**: renacimiento. `auto`, lambdas, **semántica de movimiento**, punteros inteligentes,
  `nullptr`, bucles `for` sobre rangos, hilos en la biblioteca estándar. Stroustrup lo resumió así:
  *"C++11 se siente como un lenguaje nuevo."* Desde entonces el comité publica una revisión **cada
  tres años**: C++14, C++17, C++20, C++23, y C++26 en preparación.

La crítica constante es su tamaño: el estándar supera las mil quinientas páginas y hay más de un
"C++" posible según el subconjunto que se elija. Es una crítica justa, y la comunidad responde con
guías —las **C++ Core Guidelines** de Stroustrup y Herb Sutter— que definen qué subconjunto usar.

## 🏭 Dónde vive hoy

- **Videojuegos y gráficos**: **Unreal Engine**, el núcleo de **Unity**, motores propios de estudio,
  y los controladores gráficos por debajo.
- **Navegadores**: **Chromium/Blink**, **Firefox/Gecko**, **WebKit**, y los motores de JavaScript
  **V8** y **SpiderMonkey** — es decir, tu JavaScript se ejecuta dentro de C++.
- **Bases de datos**: MySQL, MongoDB, ClickHouse, RocksDB, el motor de SQL Server.
- **Finanzas de baja latencia**: sistemas de negociación donde importan los microsegundos.
- **HPC e IA**: los núcleos de cómputo de **PyTorch** y **TensorFlow** son C++ con CUDA; Python es la
  interfaz.
- **Robótica y automoción**: **ROS 2**, **AUTOSAR Adaptive**, conducción asistida, visión artificial.
- **Aplicaciones de escritorio**: Adobe Photoshop, la suite de Autodesk, gran parte de Windows y de
  Office, **Qt** como marco multiplataforma.
- **Infraestructura**: **LLVM** (el compilador que usan Rust, Swift y Clang está escrito en C++).

## 🧠 Por qué no es legacy

**1. Nadie más ocupa ese punto exacto.** C++ es el único lenguaje ampliamente disponible que combina
control total sobre la memoria y el hardware, abstracción de alto nivel sin sobrecoste, y un
ecosistema maduro en gráficos, cálculo científico y sistemas. Rust se acerca por un lado, pero su
ecosistema en dominios como los motores gráficos o la instrumentación científica está a décadas de
distancia.

**2. Rendimiento predecible sin recolector de basura.** En un motor de videojuego que debe entregar
un fotograma cada 16 milisegundos, o en un sistema de trading, una pausa de recolección es
inaceptable. **RAII** —destructores deterministas ligados al ámbito— da liberación automática de
recursos **sin** pausas impredecibles.

**3. La metaprogramación con plantillas es única.** Permite generar código especializado en tiempo de
compilación: bibliotecas como **Eigen** producen operaciones con matrices tan rápidas como el
ensamblador escrito a mano, a partir de expresiones legibles. Con `constexpr` y `consteval`, hoy se
puede ejecutar prácticamente cualquier cálculo durante la compilación.

**4. Interoperabilidad total con C** y, a través de ella, con todo lo demás.

**5. Compatibilidad hacia atrás casi obsesiva.** Código de 1998 sigue compilando. Es su mayor lastre
—arrastra construcciones que nadie recomienda— y a la vez la razón de que la industria haya podido
apostar por él durante treinta años sin reescribir.

## 🔄 Lo que se ha modernizado

El C++ que se escribe hoy no se parece al de 1998, y esa es la parte que más se ignora desde fuera:

- **Gestión de memoria sin `new`/`delete` a mano.** `std::unique_ptr` y `std::shared_ptr` con
  `make_unique`/`make_shared` cubren casi todos los casos. La guía moderna es sencilla: **si escribes
  `delete`, probablemente te has equivocado**.
- **Semántica de movimiento** (C++11): transferir la propiedad de un recurso en lugar de copiarlo.
  Es el antepasado directo del sistema de *ownership* de Rust.
- **`constexpr` y `consteval`**: cálculo en tiempo de compilación con sintaxis normal, en lugar de
  metaprogramación de plantillas ilegible.
- **Conceptos** (C++20): restricciones sobre los parámetros de plantilla que producen mensajes de
  error comprensibles. Resuelven el problema más doloroso del C++ genérico clásico.
- **Rangos** (C++20): componer algoritmos con `|`, al estilo de las tuberías funcionales, sin
  iteradores explícitos.
- **Módulos** (C++20): sustituto de `#include`, que elimina la inclusión textual y acelera
  drásticamente la compilación. Su adopción va despacio, pero es el cambio estructural más grande del
  lenguaje.
- **Corrutinas** (C++20) y `std::format` (C++20) / `std::print` (C++23), que por fin dan un formateo
  seguro con tipos, al estilo de Python.
- **Herramientas**: *sanitizers*, `clang-tidy`, análisis estático, **vcpkg** y **Conan** como gestores
  de paquetes, y CMake como estándar de facto para construir.
- **Y una respuesta explícita al debate de seguridad de memoria**: los perfiles de seguridad
  propuestos para C++26 y las **C++ Core Guidelines** buscan garantizar por construcción propiedades
  que Rust obtiene del compilador. Es un trabajo en curso y merece seguirse.

## ⚙️ Cómo se ejecuta hoy

```bash
g++ -std=c++23 -Wall -Wextra -O2 total.cpp -o total
clang++ -std=c++23 -fsanitize=address,undefined -g total.cpp -o total

echo "15000 2 0.10" | ./total
# Total: 27000.00
```

**Compiladores:** **GCC**, **Clang/LLVM**, **MSVC** e **Intel oneAPI**. **Construcción:** CMake,
Meson, Bazel. **Dependencias:** vcpkg, Conan.

## 🧪 El programa de la clase 041 en C++

```cpp
#include <iomanip>
#include <iostream>

int main() {
    double precio{}, cantidad{}, descuento{};

    if (!(std::cin >> precio >> cantidad >> descuento)) {
        return 1;
    }

    const double total = precio * cantidad * (1 - descuento);

    std::cout << "Total: " << std::fixed << std::setprecision(2) << total << '\n';
    return 0;
}
```

**Recorrido, y la comparación que importa.**

- `std::cin >> precio` usa **sobrecarga de operadores**: `>>` está definido para cada tipo, así que la
  misma línea lee un `double`, un `int` o una cadena según lo que reciba. Compara con el `scanf("%lf",
  &precio)` de [C](c.md): allí el formato y el tipo se declaran por separado y **nada comprueba que
  coincidan**; aquí el tipo lo decide el compilador. Es el mismo problema resuelto con seguridad de
  tipos.
- `double precio{}` es **inicialización uniforme con llaves** (C++11). Además de inicializar a cero,
  prohíbe las conversiones que pierden información (*narrowing*), que con `=` pasarían en silencio.
  Es un ejemplo pequeño y muy representativo de la dirección del lenguaje moderno: cerrar puertas que
  C dejó abiertas, sin coste en ejecución.
- `if (!(std::cin >> ...))` funciona porque el flujo se convierte a booleano según su estado. Igual
  que en C hay que comprobar `scanf`, aquí hay que comprobar el flujo — con la diferencia de que si no
  lo haces, las variables ya están inicializadas a `0` gracias a `{}`, en lugar de contener basura.
- `std::fixed` y `std::setprecision(2)` son **manipuladores**: objetos que modifican el estado del
  flujo. Son notoriamente incómodos —el estado persiste para las siguientes escrituras—, y por eso
  C++20 introdujo `std::format` y C++23 `std::print`:

  ```cpp
  #include <print>
  std::print("Total: {:.2f}\n", total);   // C++23
  ```

  Esa línea es el C++ que se escribirá a partir de ahora: seguro con los tipos, legible y sin estado
  global. Merece la pena verla al lado de la anterior para entender hacia dónde va el lenguaje.
- **Y lo que no aparece porque no hace falta**: no hay `free`, ni `delete`, ni fugas posibles. El
  ámbito gestiona todo. Eso es **RAII**, y es la idea que hay que llevarse.

## ⚠️ Errores comunes al leerlo

- **Confundir "C++" con "C con clases".** Escribir C++ como si fuera C —punteros crudos, `new`/`delete`,
  arrays de C— es la fuente principal de su mala fama. El C++ moderno es otro lenguaje.
- **`using namespace std;` en una cabecera.** Contamina el espacio de nombres de todo quien la
  incluya. En un `.cpp` pequeño es discutible; en un `.hpp` es un error.
- **Copias silenciosas.** Pasar un `std::vector` por valor copia todos sus elementos. Se pasa por
  referencia constante (`const std::vector<T>&`) salvo que quieras la copia.
- **Ignorar la regla de cero/tres/cinco.** Si una clase gestiona un recurso, necesita destructor,
  constructor de copia, asignación, movimiento y asignación por movimiento — o mejor, ninguno de los
  cinco, delegando en tipos que ya lo hacen (**la regla de cero**).
- **Suponer que las plantillas son genéricos de Java.** Se instancian en compilación y generan código
  distinto por cada tipo. Eso da rendimiento y también tiempos de compilación largos y errores
  descomunales (hasta que llegaron los conceptos).
- **Leer código antiguo como si fuera actual.** Fíjate siempre en el estándar con que se compila:
  `-std=c++98` y `-std=c++23` son lenguajes distintos.

## 📚 Fuentes y bibliografía

- [cppreference.com](https://en.cppreference.com/w/) — la mejor referencia del lenguaje y la
  biblioteca; imprescindible.
- [isocpp.org](https://isocpp.org/) — sitio oficial del estándar, con las FAQ de Stroustrup.
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — Stroustrup y
  Sutter definiendo qué subconjunto del lenguaje usar y por qué. La respuesta práctica a "C++ es
  demasiado grande".
- **Bjarne Stroustrup**, *A Tour of C++*, 3.ª ed., Addison-Wesley — el mejor punto de entrada si ya
  programas: el lenguaje moderno completo en unas doscientas páginas, por su autor.
- **Bjarne Stroustrup**, *The C++ Programming Language*, 4.ª ed. — la referencia extensa.
- **Scott Meyers**, *Effective Modern C++*, O'Reilly — cuarenta y dos consejos sobre C++11/14; sigue
  siendo el libro que convierte a un programador de C++ en uno bueno.
- **Nicolai Josuttis**, *C++ Move Semantics* y *C++20: The Complete Guide* — para las dos piezas más
  difíciles del lenguaje moderno.
- **Bjarne Stroustrup**, *The Design and Evolution of C++* — por qué el lenguaje es como es, contado
  por quien tomó las decisiones. Excelente lectura sobre diseño de lenguajes en general.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [C](c.md) · [Assembler](assembler.md) · [Delphi / Object Pascal](delphi.md)
