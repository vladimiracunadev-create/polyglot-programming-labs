# Concepto — Parámetros por defecto y opcionales

Conocimiento independiente del lenguaje.

Usar **parámetros por defecto**: un parámetro que toma un valor predefinido si no se pasa. Permite funciones flexibles sin sobrecargarlas. C y Go no los tienen; se simula.

## Definiciones

- **Parámetro por defecto** — toma un valor predefinido si el argumento se omite. Clave: `exp=2`.
- **Argumento opcional** — el que se puede no pasar. Clave: cae en el valor por defecto.
- **Sobrecarga** — varias funciones con el mismo nombre y distinta firma. Clave: alternativa en Java/C.
- **Simular defecto** — en C/Go, con dos funciones o comprobando la ausencia. Clave: no es nativo.

## Forma neutral

```text
LEER tokens
base <- tokens[0] ; exp <- tokens[1] SI EXISTE SINO 2
ESCRIBIR "resultado=" base^exp
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
