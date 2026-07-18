# Concepto — Declaración, asignación e inicialización

Conocimiento independiente del lenguaje.

Distinguir tres actos que a menudo se confunden: **declarar** (introducir un nombre), **inicializar** (darle su primer valor) y **asignar** (cambiarlo después). El intercambio de dos variables los ejercita todos y revela cómo cada lenguaje los expresa (variable temporal vs. asignación múltiple).

## Definiciones

- **Declaración** — introducir un nombre en un ámbito. Clave: en lenguajes estáticos fija el tipo.
- **Inicialización** — dar el primer valor a una variable. Clave: usarla sin inicializar es un error clásico.
- **Asignación** — cambiar el valor de una variable existente. Clave: solo posible si es mutable.
- **Asignación múltiple** — asignar varias variables a la vez (a, b = b, a). Clave: evita la temporal en Python, JS, Go, Rust.

## Forma neutral

```text
LEER a, b
tmp <- a ; a <- b ; b <- tmp   (o bien: a, b <- b, a)
ESCRIBIR "a=" a " b=" b
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
