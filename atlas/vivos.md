# 🧟 Lenguajes que siguen vivos

> [⬅️ Atlas](README.md) · [📚 Índice de clases](../classes/README.md) · [🧭 Rutas](../rutas/README.md) ·
> [⬅️ Volver al programa](../README.md)

## 🎯 Por qué esta sección existe

**Ninguno de estos lenguajes está aquí por curiosidad histórica, por nostalgia ni por capricho.**
Están aquí porque **siguen en producción hoy**, y porque cada uno **deja a la vista un concepto que
los diez lenguajes del núcleo esconden o dan por resuelto**.

El criterio de inclusión es doble y se aplica a todos por igual:

1. **Uso actual verificable.** Hay un fabricante que mantiene el compilador o el intérprete, hay
   documentación con fecha reciente, y hay sectores identificables donde el lenguaje ejecuta trabajo
   real todos los días. Cada ficha lo declara y lo enlaza.
2. **Aporte pedagógico propio.** El lenguaje enseña algo que el núcleo no enseña. No se incluye
   ningún lenguaje "porque es antiguo": se incluye porque **verlo cambia lo que entiendes de los
   modernos**.

> ### Dos precisiones que este material no oculta
>
> **Primera: no todo se puede resolver con estos lenguajes, y donde no se puede, se dice.**
> [JCL](jcl.md) no calcula: orquesta trabajos. [VBA](vba.md) vive dentro de Excel y no tiene `stdin`.
> [AutoLISP](autolisp.md) no existe fuera de AutoCAD. [RPG](rpg.md) recibe sus datos por parámetros o
> por fichero, no por la entrada estándar. En esos casos **el contrato se adapta y la adaptación se
> declara en la página**, en lugar de inventar un programa falso que finja lo contrario. Un JCL que
> multiplicara números no enseñaría JCL: enseñaría una mentira.
>
> **Segunda: muchos de estos lenguajes se han actualizado para resolver problemas actuales.** No son
> fotos fijas. COBOL genera y analiza JSON con sentencias del lenguaje; Fortran descarga bucles a la
> GPU con `do concurrent`; RPG consume APIs REST con `DATA-INTO`; Ada 2022 comprueba contratos y SPARK
> los demuestra; Tcl 9.0 trajo Unicode completo; Perl 5.40 tiene `try/catch` y firmas de función;
> Delphi compila para iOS y Android; MUMPS habla FHIR y corre en contenedores. Por eso **cada ficha
> tiene una sección `🔄 Lo que se ha modernizado`**: sin ella, la lista parecería un cementerio, y no
> lo es.

---

## 🗺️ Los dieciocho, en una tabla

| Lenguaje | Año | Dónde sobrevive | Estado | El concepto que deja a la vista |
|---|---|---|---|---|
| [COBOL](cobol.md) | 1959 | Banca, seguros, gobierno, tarjetas, pensiones | 🟢 | Aritmética **decimal exacta** y la forma del dato declarada |
| [Fortran](fortran.md) | 1957 | HPC, clima, física, CFD, BLAS/LAPACK | 🟢 | El **array** como ciudadano de primera; el coste del *aliasing* |
| [Ada](ada.md) | 1983 | Aviónica, espacio, ferrocarril, defensa | 🟢 | El **tipo lleva una regla del dominio**, no solo un tamaño |
| [RPG](rpg.md) | 1959 | IBM i: ERP, retail, logística, manufactura | 🟢 | El **ciclo del programa**: un bucle principal implícito |
| [PL/I](pl-i.md) | 1964 | Mainframe z/OS: banca, seguros | 🟡 | El origen del `try/catch`; el coste de querer abarcarlo todo |
| [M / MUMPS](mumps.md) | 1966 | Sanidad, historia clínica, VistA, Epic | 🟡 | **El lenguaje y la base de datos son la misma cosa** |
| [Smalltalk](smalltalk.md) | 1970s | Banca, seguros, trading, telecomunicaciones | 🟡 | OO puro: hasta el `if` **es un mensaje a un objeto** |
| [Common Lisp](common-lisp.md) | 1958 | IA simbólica, CAD, investigación, DSL | 🟡 | **Homoiconicidad y macros**: el código es un dato |
| [AutoLISP](autolisp.md) | 1986 | AutoCAD: arquitectura, ingeniería, construcción | 🟢 | El **lenguaje incrustado** en una aplicación anfitriona |
| [Tcl/Tk](tcl.md) | 1988 | EDA (diseño de chips), redes, testing, GUI | 🟡 | **No hay sintaxis, solo comandos**: el `if` es de usuario |
| [Perl](perl.md) | 1987 | Sysadmin, texto, bioinformática, web heredada | 🟡 | **Regex en la sintaxis** y el **contexto** de evaluación |
| [Delphi / Object Pascal](delphi.md) | 1995 | Escritorio empresarial, TPV, industria, ERP | 🟢 | **RAD y modelo de componentes**: propiedades y eventos |
| [VBA](vba.md) | 1993 | Excel, Word, Access, AutoCAD, SolidWorks | 🟢 | **Una hoja de cálculo es un programa**; la UDF que extiende la fórmula |
| [Pascal](pascal.md) | 1970 | Educación, y sobre todo vía Delphi/Free Pascal | 🟡 | Tipos definidos por el usuario: **subrangos y enumerados reales** |
| [JCL](jcl.md) | 1964 | z/OS: proceso por lotes de banca y seguros | 🟢 | **Programa y entorno separados**: inyección de dependencias del SO |
| [Assembler](assembler.md) | 1949 | Firmware, núcleos, cripto, SIMD, embebidos | 🟢 | **El suelo**: qué es de verdad una variable, una pila, una llamada |
| [C](c.md) | 1972 | SO, firmware, redes, bases de datos, intérpretes | 🟢 | La **ABI universal**: el idioma en que los lenguajes se hablan |
| [C++](cpp.md) | 1985 | Videojuegos, navegadores, finanzas, HPC, robótica | 🟢 | **Abstracción de coste cero** y **RAII** |

🟢 uso amplio y activo · 🟡 nicho vivo pero minoritario

---

## 🧪 Tres niveles de rigor, declarados

Este programa distingue siempre lo que **verifica una máquina** de lo que es **material de lectura**.
Con estos dieciocho lenguajes, la clasificación es la siguiente:

### Nivel 1 — Se ejecutan en CI contra el mismo `casos.json`

[COBOL](cobol.md) (GnuCOBOL), [Fortran](fortran.md) (gfortran), [Ada](ada.md) (GNAT),
[Pascal](pascal.md) y [Object Pascal](delphi.md) (Free Pascal), [Common Lisp](common-lisp.md) (SBCL),
[Tcl](tcl.md) (tclsh), [Perl](perl.md), [C](c.md) y [C++](cpp.md).

Su código se extrae del Markdown, se compila o interpreta y se ejecuta contra los mismos casos de
prueba que las diez implementaciones del núcleo. Si el resultado no coincide, **la CI falla**. Es el
mismo estándar que se aplica al núcleo, sin excepciones.

### Nivel 2 — Contrato adaptado y declarado

[RPG](rpg.md), [JCL](jcl.md), [VBA](vba.md) y [AutoLISP](autolisp.md).

Estos lenguajes **no pueden** cumplir el contrato `stdin → stdout` sin falsearse: no es una limitación
del material, es la naturaleza del lenguaje. RPG recibe parámetros, JCL orquesta un programa que sí
calcula, VBA lee celdas y AutoLISP pregunta al usuario o señala un objeto del dibujo. En cada página
se explica cómo se adapta el contrato y por qué. **No se verifican**, y así se declara en cada
aparición.

### Nivel 3 — Correctos pero sin sello de máquina

[PL/I](pl-i.md), [M / MUMPS](mumps.md), [Smalltalk](smalltalk.md) y [Assembler](assembler.md).

Sí pueden expresar el contrato, pero su cadena de herramientas no está en los *runners* de CI: PL/I
necesita z/OS, MUMPS y Smalltalk requieren instalaciones pesadas, y el ensamblador depende de la
arquitectura concreta. El código está escrito para ser correcto e idiomático, **sin el sello de la
máquina**. Verificar diez de dieciocho no es verificarlos todos, y conviene no vender lo contrario.

---

## 📖 Cómo está organizado el material

Cada lenguaje tiene **dos apariciones distintas**, que responden a dos preguntas distintas:

**1. Su ficha en el Atlas** — *¿qué es este lenguaje y por qué sigue vivo?*

Una página por lenguaje, con la misma estructura en las dieciocho: por qué está en el programa,
historia, dónde sobrevive, por qué no ha muerto, **lo que se ha modernizado**, cómo se ejecuta hoy,
el programa de la clase 041 explicado línea a línea, la tabla "si vienes de X…", los errores comunes
al leerlo, y bibliografía real con libros concretos y documentación oficial fechada.

**2. Su sección en cada clase** — *¿cómo se ve ESTE concepto en este lenguaje?*

Cada clase de código del programa tiene un fichero `vivos.md` que resuelve **el problema de esa
clase** en los lenguajes vivos que aporten algo a **ese concepto concreto**, con código y explicación.
No es el mismo texto repetido 136 veces: la nulabilidad en COBOL (que no tiene `null`, y usa niveles
`88`) no se parece en nada a la nulabilidad en Ada (que tiene `not null access`), y ahí está el valor.

**Son 1632 programas**, y cada página los agrupa por el rigor con que están respaldados:

| Nivel | Lenguajes | Qué significa |
|---|---|---|
| 🟢 Se ejecuta en CI | COBOL, Fortran, Ada, Pascal, Common Lisp, Tcl, Perl, C++ | Se compila y se ejecuta contra el mismo `casos.json` que las diez implementaciones del núcleo |
| 🟡 Contrato adaptado | [RPG](rpg.md), [JCL](jcl.md), [VBA](vba.md), [AutoLISP](autolisp.md) | El lenguaje no puede expresar `stdin→stdout`; la adaptación se declara |
| ⚪ Sin sello de máquina | [PL/I](pl-i.md), [MUMPS](mumps.md), [Smalltalk](smalltalk.md), [ensamblador](assembler.md) | Correctos y revisados, pero ningún compilador libre los verifica aquí |

> 🗂️ **Y más allá de estos dieciocho**, todos los lenguajes del repositorio tienen ficha con esta
> misma anatomía: **[el índice de las 60 fichas](lenguajes.md)** incluye los diez del núcleo y los
> primos del Atlas.

---

## 🧭 Por dónde empezar

| Si te interesa… | Empieza por |
|---|---|
| Entender el software que mueve dinero | [COBOL](cobol.md) → [JCL](jcl.md) → [PL/I](pl-i.md) |
| El cálculo científico y el rendimiento | [Fortran](fortran.md) → [C](c.md) → [Assembler](assembler.md) |
| Los sistemas donde un fallo cuesta vidas | [Ada](ada.md) → [Pascal](pascal.md) |
| De dónde salió la orientación a objetos | [Smalltalk](smalltalk.md) → [C++](cpp.md) → [Delphi](delphi.md) |
| Metaprogramación y lenguajes que se extienden | [Common Lisp](common-lisp.md) → [Tcl](tcl.md) |
| Automatizar la herramienta que ya usas | [VBA](vba.md) → [AutoLISP](autolisp.md) |
| El software sanitario y las bases de datos raras | [M / MUMPS](mumps.md) |
| Procesar texto mejor que nadie | [Perl](perl.md) → [Tcl](tcl.md) |
| Aplicaciones de escritorio empresariales | [Delphi / Object Pascal](delphi.md) → [Pascal](pascal.md) |
| El ERP que factura en media Europa | [RPG](rpg.md) → [COBOL](cobol.md) |

---

## 📚 Bibliografía transversal

Libros que ayudan a leer **toda** esta sección, no un lenguaje concreto:

- **Robert W. Sebesta**, *Concepts of Programming Languages*, Pearson — el manual de referencia sobre
  diseño de lenguajes; dedica espacio real a COBOL, Fortran, Ada, Lisp y Smalltalk en su contexto
  histórico, que es exactamente lo que esta sección necesita.
- **Michael L. Scott**, *Programming Language Pragmatics*, Morgan Kaufmann — el porqué de las
  decisiones de implementación: tiempos de enlace, modelos de memoria, sistemas de tipos.
- **Bruce Tate**, *Seven Languages in Seven Weeks* y *Seven More Languages in Seven Weeks*, Pragmatic
  Bookshelf — el método de aprender un lenguaje por lo que aporta, que es el método de este programa.
- **Federico Biancuzzi, Shane Warden**, *Masterminds of Programming*, O'Reilly — entrevistas con los
  creadores de C++, Perl, Smalltalk, Objective-C, APL, Forth, Lua y varios más. La mejor fuente sobre
  *por qué* cada lenguaje es como es.
- **Jean Sammet**, *Programming Languages: History and Fundamentals*, 1969 — el censo clásico de los
  lenguajes de la primera era, escrito por alguien que estuvo en el comité de COBOL.
- **Peter Seibel**, *Coders at Work*, Apress — conversaciones con programadores que trabajaron con
  varios de estos lenguajes cuando eran la corriente principal.
- **ACM HOPL** (*History of Programming Languages*) — las actas de las cuatro conferencias
  ([hopl.info](https://hopl.info/)) contienen los relatos de primera mano de los diseñadores de
  COBOL, Fortran, Ada, Lisp, Smalltalk, C++ y Pascal. Fuente primaria y de acceso público.

---

⏮️ [Volver al Atlas](README.md) · 📚 [Índice de clases](../classes/README.md) ·
🏠 [Volver al programa](../README.md)
