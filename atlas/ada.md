# ✈️ Ada — 1983

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El lenguaje que no puede fallar.** Si vuelas, si tomas un metro automático o si un satélite
mantiene su órbita, hay una probabilidad razonable de que Ada esté ejecutándose. Es un nicho
pequeño y es, seguramente, el nicho con las consecuencias más graves.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: Ada se ejecuta hoy en aviónica, espacio, ferrocarril y defensa**, con
> revisión del estándar en 2022 y un ecosistema activo (GNAT, Alire, SPARK). Es un nicho pequeño,
> pero es el nicho donde un fallo se cuenta en vidas.
>
> Entra porque **deja a la vista un concepto que el núcleo esconde**: que **el tipo puede llevar
> encima una regla del dominio**, no solo un tamaño de máquina. En casi todo el núcleo, un descuento
> es un `float` y "entre 0 y 1" es un comentario o un `if` que alguien recordó escribir. En Ada,
> `range 0.0 .. 1.0` forma parte del tipo y el programa se niega a continuar si se viola. Es la
> versión llevada al extremo de lo que Rust hace con la nulabilidad y TypeScript con los tipos
> literales — y verla en Ada aclara de dónde viene esa idea.

| | |
|---|---|
| **Año** | 1983 (MIL-STD-1815); revisiones 95, 2005, 2012, 2022 |
| **Autoría** | Equipo de **Jean Ichbiah** en CII Honeywell Bull, por encargo del DoD de EE. UU. |
| **Familia** | Pascal / ALGOL, rama de sistemas críticos |
| **Paradigma** | Imperativo, modular, concurrente y OO (desde Ada 95) |
| **Tipado** | Estático, **fuerte y nominal**, con subtipos y rangos comprobados |
| **Memoria** | Pila y montículo con control explícito; sin recolector obligatorio |
| **Ejecución** | Compilado a nativo, con comprobaciones en tiempo de ejecución activables |
| **Estado** | 🟢 **Nicho pequeño, importancia extrema** — aviónica, defensa, espacio, ferrocarril |

---

## 📜 Historia

A mediados de los 70 el Departamento de Defensa de Estados Unidos hizo un inventario y encontró que
sus sistemas embebidos usaban **más de 450 lenguajes y dialectos distintos**. Cada proveedor traía el
suyo; nada era reutilizable, nada era auditable y formar gente era carísimo. En 1975 se creó un grupo
de trabajo para definir un lenguaje único, y en 1977 se convocó un concurso internacional con
propuestas anónimas identificadas por colores. En 1979 ganó la propuesta **Verde**, del equipo de
**Jean Ichbiah**.

El lenguaje se llamó **Ada** en honor a **Ada Lovelace**, y su estándar militar recibió el número
**MIL-STD-1815**: 1815 es el año de nacimiento de Lovelace. Es probablemente el número de norma más
deliberado de la historia de la informática.

La evolución fue quitando rigidez sin quitar garantías. **Ada 95** fue el primer lenguaje orientado a
objetos con estándar ISO. **Ada 2005** añadió interfaces y mejoras de tiempo real. **Ada 2012**
introdujo lo que hoy es su sello: los **contratos** —precondiciones, postcondiciones e invariantes de
tipo— escritos como parte de la declaración y comprobables por el compilador o en ejecución.
**Ada 2022** es la revisión vigente.

En paralelo creció **SPARK**, un subconjunto de Ada con anotaciones que permite **demostrar
matemáticamente** la ausencia de errores en tiempo de ejecución: no que los tests pasen, sino que
ciertos fallos son imposibles. Es de las pocas tecnologías de verificación formal que se usa de
verdad en industria.

## 🏭 Dónde sobrevive hoy

- **Aviónica**: sistemas de control de vuelo y gestión de misión, certificados bajo **DO-178C**.
- **Espacio**: software de a bordo de satélites y lanzadores; la Agencia Espacial Europea lo ha
  usado extensamente.
- **Ferrocarril y metro**: señalización y control automático de trenes bajo **EN 50128**.
- **Defensa**: sistemas de armas, radar, mando y control.
- **Gestión del tráfico aéreo** y sistemas industriales de alta integridad.

## 🧠 Por qué no ha muerto

**1. El sistema de tipos convierte errores de dominio en errores de compilación.** Ada permite
declarar tipos con **rango**, y comprobarlos. Esto no es un comentario ni un `assert`:

```ada
type Altitud_Pies  is range 0 .. 60_000;
type Velocidad_Nudos is range 0 .. 900;

A : Altitud_Pies  := 35_000;
V : Velocidad_Nudos := 450;
-- A := A + V;  --  ERROR DE COMPILACIÓN: son tipos distintos
```

Dos enteros con la misma representación pero distinto significado **no son intercambiables**. Sumar
pies a nudos no compila. En C, en Python o en JavaScript, esa suma es perfectamente válida y
perfectamente absurda. La pérdida de la sonda **Mars Climate Orbiter** en 1999 fue exactamente ese
error —libras-fuerza contra newtons— en un sistema que no era Ada.

**2. Las comprobaciones son parte del lenguaje, no de la disciplina del equipo.** Índices fuera de
rango, desbordamiento, desreferencia nula: Ada los detecta y lanza una excepción en lugar de
producir comportamiento indefinido. Se pueden desactivar (`pragma Suppress`) cuando el rendimiento
lo exija, pero **la decisión es explícita y queda escrita**.

**3. La concurrencia está en el lenguaje.** Las **tareas** (`task`), las **citas** (*rendezvous*) y
los **objetos protegidos** son construcciones del lenguaje, no de una biblioteca. El perfil
**Ravenscar** define un subconjunto de concurrencia con comportamiento temporal analizable, que es
lo que permite certificar un sistema de tiempo real: no basta con que funcione, hay que poder
demostrar que siempre cumple sus plazos.

**4. Legibilidad como requisito de certificación.** El diseño prioriza al lector sobre el escritor
—`begin`/`end` con nombre, sin abreviaturas crípticas— porque el código de un avión lo audita gente
que no lo escribió, años después.

**5. Reescribirlo requeriría recertificar.** Y la certificación de un sistema crítico cuesta más que
el desarrollo.

> **La lección de Ariane 5.** El fallo del vuelo 501 en 1996 se cita a veces como un fallo de Ada.
> Fue lo contrario: una conversión de un real de 64 bits a un entero de 16 desbordó, Ada **detectó**
> el desbordamiento y lanzó la excepción prevista. El defecto fue de ingeniería de sistemas —se
> reutilizó código de Ariane 4 con las comprobaciones desactivadas por rendimiento, en un cohete con
> una trayectoria distinta— y de gestión del fallo. El lenguaje avisó; el diseño no supo qué hacer
> con el aviso.

## 🔄 Lo que se ha modernizado

- **Contratos en el lenguaje** (Ada 2012, ampliados en 2022): `with Pre =>`, `with Post =>`,
  `Type_Invariant` y `Subtype_Predicate`. La especificación de una función deja de ser un comentario y
  se convierte en algo que el compilador comprueba —o que **GNATprove demuestra**— antes de ejecutar
  nada.
- **SPARK como herramienta industrial.** La verificación formal dejó de ser un ejercicio académico:
  hoy se aplica a componentes concretos de sistemas reales, con niveles graduales (desde "no hay
  errores de ejecución" hasta "cumple la especificación funcional"). Es de las pocas tecnologías de
  demostración formal con uso comercial sostenido.
- **Alire (`alr`)**, un gestor de paquetes moderno al estilo de `cargo`, que resolvió el mayor
  problema práctico del lenguaje: la dificultad de compartir y reutilizar bibliotecas.
- **Ada 2022** añadió literales definidos por el usuario, expresiones `declare`, imágenes de tipo
  personalizables y paralelismo ligero.
- **Objetivos actuales**: **RISC-V**, ARM Cortex-M y microcontroladores; **GNAT-LLVM** amplía las
  arquitecturas soportadas; existen bibliotecas para programar placas de bajo consumo.
- **La conversación con Rust.** La discusión pública sobre *memory safety* —las recomendaciones de
  agencias de ciberseguridad sobre lenguajes seguros por diseño— ha traído a Ada/SPARK de vuelta a la
  mesa, porque llevaba cuarenta años resolviendo el mismo problema con otras herramientas.

## ⚙️ Cómo se ejecuta hoy

```bash
# GNAT, el compilador Ada de GCC
sudo apt-get install -y gnat

# El nombre del fichero DEBE coincidir con el de la unidad: total_venta.adb
gnatmake total_venta.adb
echo "15000 2 0.10" | ./total_venta
# Total: 27000.00
```

**Herramientas.** **GNAT** (AdaCore, basado en GCC) es el compilador dominante, con edición libre
(GNAT FSF, en las distribuciones) y comercial (GNAT Pro, con soporte para certificación).
**`gprbuild`** es el sistema de construcción por proyectos, y **[Alire](https://alire.ada.dev/)**
(`alr`) es el gestor de paquetes moderno, equivalente a `cargo`. Para verificación formal,
**GNATprove** sobre **SPARK**.

## 🧪 El programa de la clase 041 en Ada

```ada
with Ada.Text_IO;            use Ada.Text_IO;
with Ada.Long_Float_Text_IO; use Ada.Long_Float_Text_IO;

procedure Total_Venta is

   --  El tipo dice lo que el negocio permite, no solo lo que la máquina guarda.
   subtype Descuento_T is Long_Float range 0.0 .. 1.0;

   Precio, Cantidad : Long_Float;
   Descuento        : Descuento_T;
   Total            : Long_Float;

begin
   Get (Precio);
   Get (Cantidad);
   Get (Descuento);          --  un 1.5 aquí levanta Constraint_Error

   Total := Precio * Cantidad * (1.0 - Descuento);

   Put ("Total: ");
   Put (Total, Fore => 1, Aft => 2, Exp => 0);
   New_Line;
end Total_Venta;
```

**Recorrido, línea a línea.**

- `with` importa una unidad; `use` hace visibles sus nombres sin cualificar. Se separan a propósito:
  puedes importar sin contaminar el espacio de nombres, y en código de alta integridad es común
  escribir `Ada.Text_IO.Put_Line (...)` completo y prescindir del `use`.
- `subtype Descuento_T is Long_Float range 0.0 .. 1.0` es la línea que resume el lenguaje. No define
  un tipo nuevo incompatible, sino un **subtipo** con una restricción: cualquier asignación fuera de
  `[0.0, 1.0]` levanta `Constraint_Error` en el punto exacto en que se produce. La regla de negocio
  "un descuento es una fracción" deja de ser un comentario y pasa a ser comprobable.
- `Get` está sobrecargado por tipo: al declarar `Descuento` como `Descuento_T`, la lectura ya valida.
  No hay un `if descuento > 1` en ninguna parte, y aun así el caso está cubierto.
- `Long_Float` es el real de doble precisión. `Float` sería simple precisión y, con siete dígitos
  significativos, empezaría a dar sorpresas en totales grandes.
- `Put (Total, Fore => 1, Aft => 2, Exp => 0)` formatea sin `printf`: `Fore` son los dígitos mínimos
  antes del punto, `Aft` los de después, y `Exp => 0` suprime la notación exponencial. La sintaxis
  `Nombre => Valor` es la **asociación por nombre**, disponible en cualquier llamada de Ada; hace que
  el sitio de llamada se lea solo, sin ir a buscar la firma.
- El `procedure` de nivel superior es el punto de entrada, y el fichero debe llamarse igual en
  minúsculas: `total_venta.adb`. GNAT usa esa convención para localizar unidades.

Compáralo con la versión en C de la misma clase: el mismo cálculo, pero aquí el rango del descuento
está **en el tipo**, y ni el compilador ni el lector tienen que confiar en que alguien lo validó.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En Ada es… |
|---|---|
| `int x = 5;` | `X : Integer := 5;` — el nombre primero, `:=` para asignar |
| `==` | `=` (comparación); `:=` es la asignación, como en Pascal |
| `struct` | `record` |
| `enum` | `type Color is (Rojo, Verde, Azul);` — un tipo de verdad, no un entero |
| `typedef` de C | `subtype` (compatible) frente a `type` (incompatible a propósito) |
| Genéricos / plantillas | `generic` — instanciados explícitamente, sin sorpresas |
| `throw` / `try` | `raise` / `exception when ... =>` |
| Hilos y `mutex` | `task` y `protected` — en el lenguaje, no en una librería |
| `assert` | `with Pre => ...`, `with Post => ...`, `with Type_Invariant => ...` |
| `1000000` | `1_000_000` — el subrayado como separador, idea que Ada popularizó |

## ⚠️ Errores comunes al leerlo

- **Confundir `type` y `subtype`.** `type Metros is new Float` crea un tipo **incompatible** con
  `Float`: no se pueden mezclar sin conversión explícita, y eso es la mitad del valor de Ada.
  `subtype` solo restringe y sigue siendo compatible.
- **Creer que las comprobaciones cuestan siempre.** El compilador elimina las que puede demostrar
  innecesarias. Lo que queda se paga solo donde hace falta, y se puede suprimir explícitamente.
- **Buscar recolector de basura.** No lo hay por defecto. La memoria dinámica se gestiona con tipos
  de acceso y, en sistemas críticos, muchas veces se **prohíbe** por completo: si no hay asignación
  dinámica, no hay fragmentación ni fallos de memoria imprevisibles.
- **Leer la verbosidad como burocracia.** `end Total_Venta;` repite el nombre porque, en un fichero
  de 2000 líneas que revisa un auditor, saber qué se está cerrando importa más que ahorrar teclas.
- **Ignorar mayúsculas y minúsculas.** Ada **no** distingue entre ellas; `Total`, `total` y `TOTAL`
  son el mismo identificador. La convención `Palabra_Con_Guiones` es estilo, no sintaxis.

## 📚 Fuentes y bibliografía

- [Ada Resource Association](https://www.adaic.org/) — el punto de entrada oficial, con el estándar
  y su fundamento (*Rationale*).
- [AdaCore Learn](https://learn.adacore.com/) — cursos interactivos gratuitos de Ada y SPARK, con
  compilador en el navegador.
- [Alire](https://alire.ada.dev/) — el gestor de paquetes y el ecosistema moderno.
- **John Barnes**, *Programming in Ada 2012 with a Preview of Ada 2022*, Cambridge University Press
  — la referencia canónica; Barnes lleva desde Ada 83 explicando el lenguaje.
- **John McCormick, Frank Singhoff, Jérôme Hugues**, *Building Parallel, Embedded, and Real-Time
  Applications with Ada*, Cambridge — el libro para la parte de concurrencia y tiempo real.
- **John McCormick, Peter Chapin**, *Building High Integrity Applications with SPARK*, Cambridge —
  verificación formal aplicada, no teórica.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [Pascal](pascal.md) · [Delphi / Object Pascal](delphi.md) · [Fortran](fortran.md)
