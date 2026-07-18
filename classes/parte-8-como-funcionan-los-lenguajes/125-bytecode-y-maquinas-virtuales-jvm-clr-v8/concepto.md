# Concepto — Bytecode y máquinas virtuales (JVM, CLR, V8)

Conocimiento independiente del lenguaje.

Entender el **bytecode y las máquinas virtuales**: una VM ejecuta instրucciones simples sobre una pila. La notación polaca inversa (RPN) es exactamente cómo trabaja una VM de pila: apila operandos y aplica operadores.

## Definiciones

- **Bytecode** — código intermedio de instrucciones simples que ejecuta una VM. Clave: portable (JVM, CLR).
- **Máquina virtual de pila** — VM que opera apilando y desapilando valores. Clave: `push 3, push 4, add`.
- **RPN** — notación donde el operador va tras los operandos. Clave: `3 4 +` = 7.

## Forma neutral

```text
PARA cada token: SI número, apilar; SI operador, desapilar 2, aplicar, apilar
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
