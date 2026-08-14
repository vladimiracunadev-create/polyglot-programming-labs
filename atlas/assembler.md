# ⚙️ Assembler — desde 1949

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**Nunca desapareció; se concentró.** El ensamblador dejó de usarse para escribir aplicaciones y se
replegó a las capas donde alguien tiene que hablarle a la máquina sin intermediarios: el arranque del
sistema, el cambio de contexto del planificador, el firmware, la criptografía de tiempo constante y
los núcleos vectoriales que hacen rápido a todo lo demás.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: se escribe ensamblador hoy, todos los días.** Cada núcleo de sistema
> operativo tiene su capa de arranque y de conmutación de tareas en ensamblador; cada biblioteca
> criptográfica seria (OpenSSL, BoringSSL) lleva rutinas escritas a mano por seguridad y rendimiento;
> cada microcontrolador tiene su vector de interrupciones; y en el mundo mainframe, **HLASM** sigue
> siendo un lenguaje de desarrollo activo en IBM Z.
>
> Entra porque es **el suelo de todo el programa**. La
> [Parte 8](../classes/parte-8-como-funcionan-los-lenguajes/README.md) trata de cómo funcionan los
> lenguajes por dentro: qué es una llamada a función, qué es la pila, qué significa "paso por valor",
> por qué una variable local es más barata que una del montículo, qué hace realmente un `for`. Todas
> esas preguntas tienen **una sola respuesta definitiva**, y está aquí. Leer el ensamblador que genera
> tu compilador no es nostalgia: es la única forma de dejar de creer y empezar a saber.

| | |
|---|---|
| **Año** | Finales de los 40 — el primer ensamblador simbólico se atribuye al EDSAC (1949) |
| **Autoría** | No hay una: cada arquitectura define el suyo |
| **Familia** | Lenguajes de bajo nivel, correspondencia casi 1:1 con el código máquina |
| **Paradigma** | Imperativo puro: mover datos, operar, saltar |
| **Tipado** | **Ninguno.** Solo hay bytes; el significado lo pone la instrucción que los usa |
| **Memoria** | Totalmente manual: registros, pila y direcciones |
| **Ejecución** | Ensamblado a código máquina; ejecución directa por el procesador |
| **Estado** | 🟢 **Vivo donde importa** — firmware, núcleos, criptografía, SIMD, embebidos, seguridad |

---

## 📜 Historia

Los primeros ordenadores se programaban en **código máquina**: números escritos a mano, con las
direcciones calculadas por el programador. Cambiar una instrucción en medio de un programa obligaba a
recalcular todos los saltos.

El **ensamblador** resolvió eso con dos ideas simples y decisivas: **nombres simbólicos para las
instrucciones** (`MOV` en vez de un opcode numérico) y, sobre todo, **etiquetas para las direcciones**,
de modo que el programa se reubica solo. **Kathleen Booth** es reconocida como autora del primer
lenguaje ensamblador junto a su trabajo en el ARC2 a finales de los 40, y **Maurice Wilkes** y su
equipo desarrollaron el *Initial Orders* del EDSAC en 1949, uno de los primeros ensambladores
funcionales.

Durante los años 50 y 60, el ensamblador **era** la programación. FORTRAN tuvo que demostrar que un
compilador podía generar código comparable, y COBOL tuvo que demostrar que la legibilidad valía la
pena. Cuando ambas cosas quedaron probadas, el ensamblador empezó a retirarse de la escritura de
aplicaciones — sin desaparecer nunca de las capas bajas.

**Un punto que conviene fijar:** "ensamblador" **no es un lenguaje**, es una **categoría**. Hay tantos
como arquitecturas, y no se parecen entre sí:

| Arquitectura | Dónde vive | Rasgo |
|---|---|---|
| **x86-64** | PC, servidores, nube | Muy complejo (CISC), instrucciones de longitud variable, dos sintaxis rivales (Intel y AT&T) |
| **ARM / AArch64** | Móviles, Apple Silicon, embebidos, servidores | RISC, instrucciones de tamaño fijo, muchos registros |
| **RISC-V** | Embebidos, académico, industria creciente | RISC abierto y modular, sin licencia |
| **z/Architecture (HLASM)** | Mainframe IBM Z | Ensamblador empresarial con macros muy potentes |
| **AVR / PIC / MSP430** | Microcontroladores | Recursos mínimos, control directo de patillas |
| **PTX / SASS** | GPU NVIDIA | Ensamblador paralelo para miles de hilos |

## 🏭 Dónde sobrevive hoy

- **Arranque y núcleo**: el código que se ejecuta antes de que exista una pila utilizable, la
  conmutación de contexto entre procesos, los manejadores de interrupción, las barreras de memoria.
  El núcleo de Linux contiene decenas de miles de líneas de ensamblador por arquitectura, y no se
  pueden escribir en C.
- **Criptografía**: las implementaciones de AES, ChaCha20, curvas elípticas o SHA en OpenSSL llevan
  rutinas en ensamblador, por dos razones: aprovechar instrucciones específicas del procesador
  (AES-NI) y garantizar **tiempo constante**, porque un compilador puede introducir un salto
  condicional que filtre información por canal lateral.
- **Núcleos vectoriales (SIMD)**: códecs de vídeo, procesamiento de imagen, álgebra lineal.
  **FFmpeg** y **dav1d** son ejemplos públicos con enormes cantidades de ensamblador optimizado a
  mano, con ganancias que el compilador no alcanza.
- **Sistemas embebidos y tiempo real**: microcontroladores con kilobytes de memoria, donde cada ciclo
  y cada byte cuentan.
- **Seguridad ofensiva y defensiva**: ingeniería inversa, análisis de malware, desarrollo de exploits,
  CTF. Aquí no se escribe ensamblador tanto como **se lee**, porque es lo único que hay.
- **Mainframe**: **HLASM** sobre z/OS, para rutinas de sistema y salidas de personalización.
- **Compiladores y máquinas virtuales**: los generadores de código de LLVM y de la JVM emiten
  ensamblador, y sus autores lo leen a diario.

## 🧠 Por qué no ha muerto

**1. Hay cosas que ningún lenguaje de alto nivel puede expresar.** No existe forma en C de decir
"escribe este valor en el registro de control del procesador", "invalida la TLB" o "ejecuta esta
instrucción atómica concreta". El código de arranque, el cambio de contexto y los manejadores de
interrupción **tienen** que ser ensamblador.

**2. El compilador es muy bueno, pero no lo sabe todo.** En el 99 % de los casos, escribir C bien es
más rápido que escribir ensamblador a mano. En el 1 % restante —transformaciones vectoriales con
patrones de acceso concretos, bucles internos de un códec— la persona que conoce el procesador gana,
y gana por factores, no por porcentajes.

**3. Garantías que el compilador no ofrece.** El tiempo constante en criptografía es el ejemplo
canónico: el compilador tiene derecho a convertir tu operación sin ramas en un salto condicional, y
eso abre un canal lateral. La única forma de garantizarlo es escribir las instrucciones.

**4. Leerlo es una destreza imprescindible.** Depurar un fallo de optimización, entender un volcado
de memoria, analizar un binario sin fuentes, verificar que una mitigación de seguridad se aplicó de
verdad: todo eso es lectura de ensamblador.

**5. Es el único lugar donde las abstracciones se pueden comprobar.** Cuando en la
[Parte 5](../classes/parte-5-funciones-y-modularidad/README.md) se afirma que "una llamada a función
guarda la dirección de retorno en la pila", eso es una afirmación verificable: se compila, se mira el
ensamblador y se ve.

## 🔄 Lo que se ha modernizado

- **Extensiones vectoriales continuas**: AVX-512 en x86-64, **SVE/SVE2** en ARM (de longitud vectorial
  variable), la extensión **V** de RISC-V. Cada generación de procesador añade instrucciones nuevas
  que alguien tiene que usar primero a mano.
- **Instrucciones para acelerar cosas concretas**: cifrado (AES-NI, SHA-NI), multiplicación de
  matrices para IA (AMX en Intel, las extensiones matriciales de ARM), operaciones atómicas más
  finas.
- **RISC-V**, una arquitectura **abierta y modular** diseñada en los 2010, con adopción industrial
  creciente. Es la primera ISA importante en décadas que se puede estudiar e implementar sin licencia,
  y ha revitalizado la enseñanza de la arquitectura de computadores.
- **Herramientas incomparablemente mejores**: **[Compiler Explorer](https://godbolt.org/)** muestra en
  el navegador, en tiempo real y con colores, qué ensamblador genera tu código en decenas de
  compiladores y arquitecturas. Lo que antes exigía `objdump` y paciencia hoy es inmediato.
- **Ensamblador en línea con restricciones** (`asm` de GCC/Clang, `asm!` de Rust): permite insertar
  instrucciones concretas dentro de código de alto nivel, describiendo al compilador qué registros y
  qué memoria se tocan, para que siga optimizando alrededor con seguridad.
- **Verificación formal de rutinas críticas**: proyectos como HACL\*/EverCrypt generan e incluso
  demuestran la corrección de código criptográfico de bajo nivel.

## ⚙️ Cómo se ejecuta hoy

```bash
# Ensamblar y enlazar (GNU as, sintaxis AT&T, x86-64 Linux)
gcc -no-pie total.s -o total
echo "15000 2 0.10" | ./total
# Total: 27000.00

# Ver el ensamblador que genera TU código C — el uso más frecuente hoy:
gcc -O2 -S -masm=intel programa.c -o programa.s

# Desensamblar un binario existente:
objdump -d -M intel ./programa | less
```

**Herramientas:** **GAS** (`as`, el ensamblador de GNU, sintaxis AT&T por defecto), **NASM** y
**YASM** (sintaxis Intel, muy usados en proyectos multimedia), **MASM** (Microsoft), **LLVM-MC**.
Para leer y analizar: `objdump`, **Ghidra** (libre, de la NSA), **IDA Pro**, **radare2/rizin** y
**Compiler Explorer**.

**Las dos sintaxis de x86, que confunden a todo el mundo:**

```text
AT&T (GNU as):   movq  $5, %rax     # destino a la DERECHA, $ para literales, % para registros
Intel (NASM):    mov   rax, 5       # destino a la IZQUIERDA, sin prefijos
```

Es el mismo código máquina escrito de dos maneras. Al leer documentación conviene comprobar siempre
cuál se está usando.

## 🧪 El programa de la clase 041 en ensamblador x86-64

> ⚠️ **Específico de una arquitectura, y declarado.** Este código es x86-64 con la ABI System V de
> Linux y sintaxis AT&T. **No es portable**: en ARM64, en RISC-V o en Windows sería otro programa.
> Esa dependencia es, precisamente, la característica que define al ensamblador.

```gas
        .section .rodata
fmt_in:  .asciz  "%lf %lf %lf"
fmt_out: .asciz  "Total: %.2f\n"
uno:     .double 1.0

        .text
        .globl  main
main:
        pushq   %rbp                    # prólogo: guardar el marco del llamante
        movq    %rsp, %rbp              # establecer el marco propio
        subq    $32, %rsp               # reservar 32 bytes en la pila (3 doubles + alineación)

        # --- scanf("%lf %lf %lf", &precio, &cantidad, &descuento) ---
        leaq    fmt_in(%rip), %rdi      # 1.er argumento: el formato
        leaq    -8(%rbp),  %rsi         # 2.º: &precio
        leaq    -16(%rbp), %rdx         # 3.º: &cantidad
        leaq    -24(%rbp), %rcx         # 4.º: &descuento
        xorl    %eax, %eax              # 0 argumentos en registros vectoriales
        call    scanf@PLT

        # --- total = precio * cantidad * (1 - descuento) ---
        movsd   uno(%rip), %xmm0        # xmm0 = 1.0
        subsd   -24(%rbp), %xmm0        # xmm0 = 1.0 - descuento
        mulsd   -8(%rbp),  %xmm0        # xmm0 *= precio
        mulsd   -16(%rbp), %xmm0        # xmm0 *= cantidad

        # --- printf("Total: %.2f\n", total) ---
        leaq    fmt_out(%rip), %rdi     # 1.er argumento: el formato
        movl    $1, %eax                # 1 argumento en registros vectoriales (xmm0)
        call    printf@PLT

        xorl    %eax, %eax              # return 0
        leave                           # epílogo: deshacer el marco
        ret
```

**Recorrido, y lo que enseña cada bloque.**

- **No hay variables.** `precio`, `cantidad` y `descuento` no existen: hay tres huecos de 8 bytes en
  la pila, en `-8(%rbp)`, `-16(%rbp)` y `-24(%rbp)`. El nombre era una comodidad del compilador. Esto
  es lo que **es** una variable local: un desplazamiento respecto al puntero de marco.
- **`pushq %rbp` / `movq %rsp, %rbp` / `leave` es el marco de pila**, y aparece idéntico en el código
  generado por cualquier compilador. Cuando en la
  [Parte 5](../classes/parte-5-funciones-y-modularidad/README.md) se habla de "el ámbito de una
  función" o de "la pila de llamadas", **esto** es la pila de llamadas.
- **`subq $32, %rsp` es reservar memoria local**, y por eso es gratis comparado con el montículo: una
  resta. Liberarla es `leave`. Ahí está, en dos instrucciones, la respuesta a por qué una variable
  local es más barata que una asignación dinámica.
- **La convención de llamada es un contrato.** En la ABI System V de x86-64, los argumentos enteros y
  punteros van en `%rdi, %rsi, %rdx, %rcx, %r8, %r9`, y los reales en `%xmm0`–`%xmm7`. Nadie lo
  comprueba: si te equivocas de registro, el programa lee basura. Esa convención es lo que hace
  posible que Rust llame a C, que Python cargue una biblioteca `.so` y que la
  [Parte 10](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/README.md) tenga
  sentido. **La interoperabilidad entre lenguajes se define en este nivel, no en el sintáctico.**
- **`movl $1, %eax` antes de `printf` no es adorno.** En una función variádica, `%eax` debe contener
  **cuántos argumentos viajan en registros vectoriales**, porque `printf` lo necesita para recorrerlos.
  Olvidarlo suele producir un fallo de segmentación desconcertante. Es un detalle de la ABI que casi
  nadie conoce hasta que lo sufre.
- **`subsd`, `mulsd`: aritmética de doble precisión en registros SSE.** La `s` final es *scalar* (un
  valor por registro); las variantes `subpd`/`mulpd` operan sobre **varios valores a la vez**, y en
  esa diferencia de una letra está todo el paralelismo SIMD.
- **`(%rip)` es direccionamiento relativo al contador de programa**, lo que permite que el código sea
  reubicable. Es la base técnica de las bibliotecas compartidas y de las mitigaciones de seguridad
  como ASLR.
- **`@PLT`** indica que el símbolo se resuelve en tiempo de enlace dinámico, a través de la tabla de
  enlace de procedimientos. Es cómo funciona realmente cargar una biblioteca.
- **No hay tipos.** Los mismos 8 bytes se tratan como puntero con `leaq` y como real con `movsd`. El
  procesador no sabe qué son: lo decide la instrucción. Cuando en la
  [Parte 3](../classes/parte-3-valores-tipos-y-variables/README.md) se dice que "el tipo es una
  interpretación de los bits", esta es la demostración.

**El uso real de esto no es escribirlo, es leerlo.** Compila la versión en C de la clase 041 con
`gcc -O2 -S` y compárala con este código: verás que el compilador elimina el marco de pila, mantiene
los valores en registros y reordena las multiplicaciones. Ese ejercicio —tres minutos en
[Compiler Explorer](https://godbolt.org/)— enseña más sobre optimización que cualquier explicación.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En ensamblador es… |
|---|---|
| Variable local | Un desplazamiento en la pila: `-8(%rbp)` |
| Variable global | Una etiqueta en `.data` o `.bss` |
| Constante | Una etiqueta en `.rodata` |
| `x = y` | `mov` — copiar bytes de un sitio a otro |
| `x + y` | `add` (enteros) o `addsd` (reales de doble precisión) |
| `if (a > b)` | `cmp` seguido de un salto condicional (`jg`, `jle`, …) |
| `while` / `for` | Una etiqueta y un salto hacia atrás |
| Llamada a función | `call` — apila la dirección de retorno y salta |
| `return` | `ret` — desapila la dirección y salta a ella |
| Argumentos | Registros según la ABI, y la pila a partir del séptimo |
| Valor devuelto | `%rax` (entero) o `%xmm0` (real) |
| `struct` | Un bloque de bytes; los campos son desplazamientos |
| Puntero | Una dirección; `leaq` la calcula, `movq (%reg)` la sigue |

## ⚠️ Errores comunes al leerlo

- **Confundir las sintaxis.** `mov %rax, %rbx` mueve rax→rbx en AT&T y rbx→rax en Intel. La misma
  línea, sentido contrario. Comprueba siempre cuál estás leyendo.
- **Romper la alineación de la pila.** La ABI exige que `%rsp` esté alineado a 16 bytes en el momento
  del `call`. Si no lo está, una instrucción SSE dentro de `printf` provoca un fallo de segmentación
  aparentemente aleatorio. Es el error más frustrante para quien empieza.
- **Olvidar qué registros preserva quién.** La ABI divide los registros entre los que el llamado debe
  conservar (`%rbx`, `%rbp`, `%r12`–`%r15`) y los que puede destruir. Suponer lo contrario produce
  errores que solo aparecen a veces.
- **Leer código optimizado como si fuera el original.** Con `-O2`, el compilador reordena, fusiona y
  elimina. La correspondencia línea a línea con el fuente desaparece. Para estudiar, empieza con
  `-O0`.
- **Suponer portabilidad.** Este programa no funciona en un Mac con Apple Silicon ni en una Raspberry
  Pi. Es la naturaleza del lenguaje.
- **Creer que a mano siempre es más rápido.** Casi nunca lo es. Antes de escribir una sola
  instrucción, mide, y comprueba qué generó ya el compilador.

## 📚 Fuentes y bibliografía

- [Compiler Explorer (godbolt.org)](https://godbolt.org/) — la herramienta con la que aprender a leer
  ensamblador. Empieza aquí.
- [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/sdm) — la
  referencia completa de x86-64.
- [Arm Architecture Reference Manual](https://developer.arm.com/documentation/ddi0487/latest/) — el
  equivalente para AArch64.
- [The RISC-V Instruction Set Manual](https://riscv.org/technical/specifications/) — abierta y
  notablemente más legible que las anteriores; buena para aprender.
- [IBM High Level Assembler (HLASM)](https://www.ibm.com/docs/en/hla-and-tf) — el ensamblador del
  mainframe, con su sistema de macros.
- **Randal Bryant, David O'Hallaron**, *Computer Systems: A Programmer's Perspective*, 3.ª ed.,
  Pearson — **el libro** para entender qué hay debajo de tu código. Si solo lees uno de esta lista,
  que sea este.
- **Jonathan Bartlett**, *Programming from the Ground Up* —
  [gratis en línea](https://savannah.nongnu.org/projects/pgubook/); enseña a programar empezando por
  el ensamblador.
- **Randall Hyde**, *The Art of 64-bit Assembly*, No Starch Press — el tratado moderno y exhaustivo.
- **David Patterson, John Hennessy**, *Computer Organization and Design (RISC-V Edition)*, Morgan
  Kaufmann — la arquitectura de computadores desde la ISA hacia arriba.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [C](c.md) · [C++](cpp.md) · [Fortran](fortran.md)
