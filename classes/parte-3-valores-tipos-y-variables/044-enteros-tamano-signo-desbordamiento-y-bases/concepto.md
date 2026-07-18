# Concepto — Enteros: tamaño, signo, desbordamiento y bases

Conocimiento independiente del lenguaje.

Entender que un entero es un valor único que puede **representarse** en varias bases. La conversión revela diferencias reales: casi todos tienen formateo de hex/octal/binario, pero **C carece de especificador para binario** (hay que construirlo) y SQL solo formatea hex.

## Definiciones

- **Base numérica** — sistema para escribir un número (10, 16, 8, 2). Clave: cambia la representación, no el valor.
- **Hexadecimal** — base 16 (0-9, a-f). Clave: compacta y común en memoria/colores.
- **Octal** — base 8. Clave: usada en permisos de archivos Unix.
- **Binario** — base 2 (0 y 1). Clave: la representación real en la máquina.

## Forma neutral

```text
LEER n
ESCRIBIR "dec=" n " hex=" BASE(n,16) " oct=" BASE(n,8) " bin=" BASE(n,2)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
